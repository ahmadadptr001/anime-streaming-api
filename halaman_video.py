from selenium import webdriver; import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC

driver_path = r'C:\Users\User\downloads\Chromedriver.exe'

options = Options()
options.add_argument('--headless')
options.add_argument('User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36')

service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

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

def scraping_halaman_video(url):
    driver.get(url); time.sleep(10)
    
    judul = driver.find_elements(By.CLASS_NAME, 'entry-title')[0].text
    print("[✅] Berhasil mendapatkan judul anime (video)")
    
    driver.execute_script('document.querySelector(".mirror").onchange')
    try:
        link_video = wait(driver, 10).until(EC.presence_of_element_located(By.TAG_NAME, 'iframe')).get_attribute('src')
    except:
        link_video = 'null'
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
        data_film[0]['rekomendasi'][f'anime{i}'] = {
            'judul' : gambar_dan_judul_anime_rekomendasi[i+1].get_attribute('title'),
            'tipe' : tipe_anime_rekomendasi[i+1].text,
            'status' : status_anime_rekomendasi[i+1].text,
            'gambar' : gambar_dan_judul_anime_rekomendasi[i+1].get_attribute('src'),
            'link_detail_halaman' : link_anime_rekomendasi[i+1].get_attribute('href')
        }
    
    return data_film;
    #return jsonify(data_film)        
    
base_url = 'https://tv0.animisme.net/nonton-boruto-naruto-next-generations-episode-244/'

if __name__ == '__main__' : 
    hasil = scraping_halaman_video(base_url)
    from json import dumps
    print(dumps(hasil, indent=3))
    
