# Anime streaming api

## 📺 Instalation
- git bash:
    ```bash
        $ git clone https://github.com/ahmadadptr001/anime-streaming-api
        $ cd anime-streaming-api
        $ pip install -r requirements.txt
        $ python akses_api.py
    ```

## ⚙️ How to use?
- Search anime: request GET <mark> http://localhost:5000/search?anime_title=`enter title anime here` </mark>
- output:
    ```json
        [{
        'anime' : {
            'anime0' : {
                'judul' : '',
                'tipe' : '',
                'status' : '',
                'gambar' : '',
                'link_detail_halaman' : ''
            }
            'anime1' : {
                'judul' : '',
                'tipe' : '',
                'status' : '',
                'gambar' : '',
                'link_detail_halaman' : ''
            }
            //  etc ...
        }
    }]
    ```
- Search detail anime : request GET <mark> http://localhost:5000/search/detail?anime_url=`link_detail_halaman from search anime` </mark>
- output:
    ```json
         [{
        'anime' : {
            'judul' : '',
            'gambar' : '',
            'peringkat' : '',
            'kumpulan_informasi' : '',
            'sinopsis' : '',
            'list_episode' : ''
        }
    }]
    ```

- Get video : request GET <mark> http://localhost:5000/search/detail/watch?anime_url=`link_detail_halaman from search detail anime` </mark>
- output:
    ```json
        [{
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
            // etc ..
        }
    }]
    ```

## 👥 Contributors
thanks for all:
- [Ahmad Adptr](https://github.com/ahmadadptr001)