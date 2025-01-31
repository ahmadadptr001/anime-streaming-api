from flask import Flask, jsonify, request
from flask_cors import CORS

from selenium import webdriver; import time, re
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC


# konfigurasi selenium sebelum melakukan scrape ke web animisme.net
options = Options()
options.add_argument('--headless')
options.add_argument('User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36')

service = Service(r'C:\Users\User\downloads\Chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)

# initialisasi flask
ahmad_api = Flask(__name__); CORS(ahmad_api)

@ahmad_api.route('/', methods=['GET'])
def halaman_utama():
    return jsonify('halo pengguna')

@ahmad_api.route('/search', methods=['GET']) # http://localhost:5000/search?anime_title={request}
def cari_anime():
    
    print('\n\n[*] Memulai Pencarian..')
    data_pencarian = [{
        'anime' : {
            'anime0' : {
                'judul' : '',
                'tipe' : '',
                'status' : '',
                'gambar' : '',
                'link_detail_halaman' : ''
            }
        }
    }]

    base_url = f'https://tv0.animisme.net/?s={request.args.get('anime_title')}'
    driver.get(base_url); time.sleep(10)
    
    teks_konten_html_hasil_pencarian = driver.execute_script('return document.querySelector(".listupd").textContent') 
    if re.findall('tidak ditemukan', teks_konten_html_hasil_pencarian.lower()):
        data_pencarian= [{'anime' : 'null'}]
        return jsonify(data_pencarian)
    
    tipe_anime = driver.find_elements(By.CLASS_NAME, 'typez') # ambil text nya (text biasa)
    print("[✅] Berhasil mendapatkan type anime list")
    gambar_dan_judul_anime = driver.find_elements(By.CLASS_NAME, 'ts-post-image') # ambil src dan title nya (attribute)
    print("[✅] Berhasil mendapatkan judul dan title anime list")
    status_anime = driver.find_elements(By.CLASS_NAME, 'epx') # ambil text nya (text biasa)
    print("[✅] Berhasil mendapatkan status anime list")
    link_detail_halaman = driver.find_elements(By.CLASS_NAME, 'tip') # ambil href nya (attribute)

    n = len(tipe_anime)
    for i in range(n):
        data_pencarian[0]['anime'][f'anime{i}'] = {
            'judul' : gambar_dan_judul_anime[i].get_attribute('title'),
            'tipe' : tipe_anime[i].text,
            'status' : status_anime[i].text,
            'gambar' : gambar_dan_judul_anime[i].get_attribute('src'),
            'link_detail_halaman' : link_detail_halaman[i].get_attribute('href')
        }

    return jsonify(data_pencarian)

@ahmad_api.route('/search/detail', methods=['GET']) # http://localhost:5000/search/detail?anime_url={request}
def scraping_halaman_detail():
    print('\n\n[*] Memulai Pencarian..')
    
    data_halaman_detail = [{
        'anime' : {
            'judul' : '',
            'gambar' : '',
            'peringkat' : '',
            'kumpulan_informasi' : '',
            'sinopsis' : '',
            'list_episode' : ''
        }
    }]
    
    url = request.args.get('anime_url')
    driver.get(url); time.sleep(10)
    
    judul = driver.find_elements(By.CLASS_NAME, 'ts-post-image')[0].get_attribute('title')
    print("[✅] Berhasil mendapatkan judul anime")
    gambar = driver.find_elements(By.CLASS_NAME, 'ts-post-image')[0].get_attribute('src')
    print("[✅] Berhasil mendapatkan gambar anime")
    peringkat = driver.find_elements(By.CLASS_NAME, 'rating')[0].find_element(By.TAG_NAME, 'strong').text 
    print("[✅] Berhasil mendapatkan peringkat anime")

    kumpulan_informasi = []
    for item in driver.find_element(By.CLASS_NAME, 'spe').find_elements(By.TAG_NAME, 'span'):
        kumpulan_informasi.append(item.text.replace('\\n', '').replace('  ', ''))
    print("[✅] Berhasil mendapatkan kumpulan informasi anime")

    sinopsis = driver.find_elements(By.CLASS_NAME, 'entry-content')[0].text
    print("[✅] Berhasil mendapatkan sinopsis anime")
    
    list_episode = []
    
    for a in driver.find_element(By.CLASS_NAME, 'eplister').find_element(By.TAG_NAME, 'ul').find_elements(By.TAG_NAME, 'a'):
        link_episode = a.get_attribute('href')
        episode = a.find_element(By.CLASS_NAME, 'epl-num').text
        tanggal_rilis = a.find_element(By.CLASS_NAME, 'epl-date').text
        
        data_halaman_detail_episode = {
            'episode' : episode,
            'tanggal_rilis' : tanggal_rilis,
            'link_episode' : link_episode
        }
        
        list_episode.append(data_halaman_detail_episode)
        
    print("[✅] Berhasil mendapatkan data_halaman_detail episode anime")

    data_halaman_detail[0]['anime'] = {
        'judul' : judul,
        'gambar' : gambar,
        'peringkat' : peringkat,
        'kumpulan_informasi' : kumpulan_informasi,
        'sinopsis' : sinopsis,
        'list_episode' : list_episode
    }

    return jsonify(data_halaman_detail)
    
@ahmad_api.route('/search/detail/watch', methods=['GET']) # http://localhost:5000/search/detail/watch?anime_url={request}
def scraping_halaman_video():
    print('\n\n[*] Memulai Pencarian..')
    
    data_film = [{
        'anime' : {
            'judul': '',
            'link_video' : '',
            'peringkat' : ''
        },
        'rekomendasi' : {
            'anime0' : {
                'judul' : '',
                'tipe' : '',
                'status' : '',
                'gambar' : '',
                'link_detail_halaman' : ''
            }
        }
    }]
    
    url = request.args.get('anime_url')
    driver.get(url); time.sleep(10)
    
    judul = driver.find_elements(By.CLASS_NAME, 'entry-title')[0].text
    print("[✅] Berhasil mendapatkan judul anime (video)")
    
    driver.execute_script('document.querySelector(".mirror").onclick')
    driver.execute_script('document.querySelector(".mirror option").onclick')
    link_video = driver.find_elements(By.TAG_NAME, 'iframe')[0].get_attribute('src')
    print("[✅] Berhasil mendapatkan link video anime")
    
    peringkat = driver.find_element(By.CLASS_NAME, 'rating').text
    print("[✅] Berhasil mendapatkan peringkat anime (video)")
    
    data_film[0]['anime'] = {
        'judul': judul,
        'link_video' : link_video,
        'peringkat' : peringkat
    }
    
    tipe_anime_rekomendasi = driver.find_elements(By.CLASS_NAME, 'typez') # ambil text nya (text biasa)
    print("[✅] Berhasil mendapatkan tipe anime rekomendasi")
    gambar_dan_judul_anime_rekomendasi = driver.find_elements(By.CLASS_NAME, 'ts-post-image') # ambil src dan title nya (attribute)
    print("[✅] Berhasil mendapatkan gambar dan judul anime rekomendasi")
    status_anime_rekomendasi = driver.find_elements(By.CLASS_NAME, 'epx') # ambil text nya (text biasa)
    print("[✅] Berhasil mendapatkan status anime rekomendasi")
    link_anime_rekomendasi = driver.find_elements(By.CLASS_NAME, 'tip') # ambil href nya
    print("[✅] Berhasil mendapatkan link anime rekomendasi")
    
    for i in range(len(tipe_anime_rekomendasi)):
        try:
            data_film[0]['rekomendasi'][f'anime{i}'] = {
                'judul' : gambar_dan_judul_anime_rekomendasi[i+1].get_attribute('title'),
                'tipe' : tipe_anime_rekomendasi[i+1].text,
                'status' : status_anime_rekomendasi[i+1].text,
                'gambar' : gambar_dan_judul_anime_rekomendasi[i+1].get_attribute('src'),
                'link_detail_halaman' : link_anime_rekomendasi[i+1].get_attribute('href')
            }
        except IndexError: pass
    
    return jsonify(data_film)        

if __name__ == "__main__":
    ahmad_api.run(port=5000, debug=True, threaded=True)
    