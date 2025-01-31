from selenium import webdriver; import time, re
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

driver_path = r'C:\Users\User\Downloads\chromedriver.exe';
options = Options()
options.add_argument('--headless')
options.add_argument('User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36')

service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

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

def pencarian_tidak_ditemukan():
    data_pencarian= [{'anime' : 'null'}]
    return data_pencarian
    # return jsonify(data_pencarian)
    
def cari_anime(title):
    base_url = f'https://tv0.animisme.net/?s={title}'
    driver.get(base_url)
    time.sleep(10)
    teks_konten_html_hasil_pencarian = driver.execute_script('return document.querySelector(".listupd").textContent') 
    if re.findall('tidak ditemukan', teks_konten_html_hasil_pencarian.lower()):
        pencarian_tidak_ditemukan()
    
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
    return data_pencarian
    # return jsonify(data_pencarian)
    
    
if __name__ == '__main__':
    hasil = cari_anime('naruto')
    import json
    print(json.dumps(hasil[0], indent=3))