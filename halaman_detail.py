from selenium import webdriver; import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

driver_path = r'C:\Users\User\downloads\Chromedriver.exe'

options = Options()
options.add_argument('--headless')
options.add_argument('User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36')

service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

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

def scraping_halaman_detail(url):
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

        return data_halaman_detail
        # return jsonify(data_halaman_detail)
        
base_url = 'https://tv0.animisme.net/anime/boruto-naruto-next-generations-sub-indonesia/'

if __name__ == '__main__':
    from json import dumps
    print(dumps(scraping_halaman_detail(base_url), indent=3))
    