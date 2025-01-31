const container_pencarian = document.getElementById('container-pencarian');
const form_input_cari_anime = document.getElementById('form_input_cari_anime');

form_input_cari_anime.addEventListener('submit', function(e) {
    e.preventDefault();
    const input_cari_anime = document.getElementById('input_cari_anime');
    Pencarian(input_cari_anime.value)
})


// -------------------------------------------------------------------
async function Pencarian(judul_anime){
    
    try
    {
        container_pencarian.innerHTML = `
            <div class="container-lazy-load">
                <div class="text-top-lazy loaded-lazy"></div>
                <div class="hr-lazy loaded-lazy"></div>
                <div class="wrapper-lazy">
                    <div class="card-lazy loaded-lazy-2"></div>
                    <div class="card-lazy loaded-lazy-2"></div>
                    <div class="card-lazy loaded-lazy-2"></div>
                    <div class="card-lazy loaded-lazy-2"></div>
                    <div class="card-lazy loaded-lazy-2"></div>
                </div>
            </div>
        `;

        const url_api = `http://localhost:5000/search?anime_title=${judul_anime}`;
        const response_api = await axios.get(url_api)
        const data_api = response_api.data[0]['anime']

        container_pencarian.innerHTML = `
            <p class="fw-bold fs-3">Mencari : ${judul_anime}</p>
            <hr class="w-100 border-1">
            <div class="d-grid gap-2 p-3 container-hasil-pencarian"></div>
        `;
        const container_hasil_pencarian = document.querySelector('.container-hasil-pencarian');

        if (data_api == 'null') 
        {
            container_pencarian.innerHTML =  `
                <p class="fw-bold fs-3">Mencari : ${judul_anime}</p>
                <hr class="w-100 border-1">
                <div class="border p-3 container-hasil-pencarian">
                    <p class="fs-3 fw-semibold text-danger">${judul_anime} tidak ditemukan!</p>
                </div>
            `
        }
        else
        {
            for (let [keys, data] of Object.entries(data_api)) {
                let card = document.createElement('div'); 
                card.classList.add('card', 'border-0', 'rounded-3', 'p-1', 'shadow'); 
                card.innerHTML = `
                    <div class="card-header p-0 border-0 position-relative">
                        <div class='card-status position-absolute end-0 top-0 text-end bg-primary text-light px-2 py-1 w-50' style='clip-path: polygon(0 0, 100% 0,  100% 100%, 50% 100%, 0 0);'>
                            ${data['status']}
                        </div>
                        <img src='${data["gambar"]}' class='w-100' style='object-fit: cover; min-height: 180px; aspect-ratio: 5/4;' />
                        </div>
                    <div class="card-body d-flex flex-column justify-content-end w-100" style='height: 100%;'>
                        <div>
                            <small class='rounded-pill btn btn-outline-success px-1 py-0' style="font-size: 70%;">${data['tipe']}</small>
                            <p class='fw-bold' style='font-size: 85%;'>${data['judul'].length > 18 ? data['judul'].slice(0, 18) + '...' : data['judul']} </p>
                        </div>
                        <div>
                            <button class='btn btn-warning rounded w-100 py-1' onclick="Detail('${data['link_detail_halaman']}')">
                                Tonton
                            </button>
                        </div>
                    </div>
                `;
                container_hasil_pencarian.appendChild(card);
            }
        }
    }

    catch (error) 
    {
        const pesan_error = `Pencarian Anda Gagal dikarenakan masalah jaringan (${error})`
        Swal.fire({
            title: 'Oops!',
            text: pesan_error,
            icon: 'error',
            confirmButtonText: 'Oke'
          }).then((result) => {
              window.location.href = './index.html'
          });
          
    }


    
}




// -------------------------------------------------------------------
async function Detail(url){
    try 
    {
        container_pencarian.innerHTML = `
                 <div class="container-lazy-load-detail gap-2" style="display: grid;">
                    <div class="card-lazy-load-detail"></div>
                    <div>
                        <div class="top-text-lazy-detail"></div>
                        <div class="bottom-text-lazy-detail"></div>
                    </div>
                </div>
        `;

        const url_api =  ` http://localhost:5000/search/detail?anime_url=${url}`;
        const response = await axios.get(url_api);
        const data_api = response.data[0]['anime'];

        let judul = data_api['judul'];
        let gambar = data_api['gambar'];
        let peringkat = data_api['peringkat'];
        let kumpulan_informasi = data_api['kumpulan_informasi'];
        let sinopsis = data_api['sinopsis'];
        let list_episode =  data_api['list_episode'];

        container_pencarian.innerHTML = `
            <div class='row'>
                <div class='col-12 col-md-4'>
                    <img src='${gambar}' class='w-75 w-sm-100 rounded-1' />
                </div>
                <div class='col-12 col-md-8'>
                    <p class='fs-4 fw-bold mb-1'>${judul}</p>
                    <p class='fw-semibold text-warning' style='font-size: 80%;'>
                        <i class="fas fa-star"></i> ${peringkat}
                    </p>
                    <div class='kumpulan-informasi d-grid' style='grid-template-columns: 1fr 2fr;'></div>
                    <button class="btn btn-outline-danger mt-3">Tonton Sekarang</button>
                </div>
            </div>
        `;

        const kumpulan_informasi_container = document.querySelector('.kumpulan-informasi');

        for (let [key, value] of Object.entries(kumpulan_informasi)) {
            const span = document.createElement('span')
            span.style = `font-size: 80%;`
            span.innerHTML = `${value}`;
            kumpulan_informasi_container.appendChild(span);
        }

        container_pencarian.innerHTML += `
            <div class="my-4 shadow card w-100 border-0 card-header">
                <p class='fs-4 fw-bold'>Deskripsi : </p>
                <hr>
                <p>${sinopsis}</p>
            </div>
            <table classs='table table-bordered w-100 mt-4 shadow table-responsive'>
                <thead>
                    <tr class="text-center">
                        <td>Episode</td>
                        <td>Tangga Rilis</td>
                    </tr>
                </thead>
                <tbody  id='table-body'>
                </tbody>
            </table>
        `;

        const table_body = document.getElementById('table-body');
        for (let [key, value] of Object.entries(list_episode)) {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td class='p-1 text-center'>
                    <button onclick="Film('${value['link_episode']}')" class='btn btn-warning px-1 py-0'>
                        Episode ${value['episode']}
                    </button>
                </td>
                <td class='text-center'>${value['tanggal_rilis']}</td>
            `;
            table_body.appendChild(tr);
        }
    }

    catch(error)
    {
        const pesan_error = `Pencarian Anda Gagal dikarenakan masalah jaringan (${error})`
        Swal.fire({
            title: 'Oops!',
            text: pesan_error,
            icon: 'error',
            confirmButtonText: 'Oke'
          }).then((result) => {
              window.location.href = './index.html'
          });
    }
}



// -------------------------------------------------------------------
function Film() {

}
// 