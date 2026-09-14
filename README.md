Name : Husainah Syamsiah

NPM : 2506589036

Class : PBP B

### Tugas 1
1. Pada Tutorial dan Tugas 1, Anda diberi kebebasan untuk menentukan tampilan dari website portofolio Anda. Saat Anda merancang struktur HTML yang digunakan, apakah Anda menggunakan elemen semantik HTML5 seperti <section>, <article>, atau <aside>? Jika iya, bagaimana elemen tersebut membantu Anda dalam membuat static web? Jika tidak, mengapa tanpa elemen tersebut sudah memenuhi kebutuhan desain Anda?
> Ya,  saya menggunakan elemen <section>. Elemen tersebut memudahkan untuk memberi struktur pada bagian-bagian yang berbeda pada static web untuk informasi yang berbeda. Elemen tersebut juga membantu saya untuk memudahkan penentuan tampilan untuk setiap golongan informasi beda yang saya ingin tampilka, seperti dengan memberi class pada section tersebut.
2. Ketika Anda mengatur CSS Anda agar tetap responsive, tantangan tata letak apa yang Anda temukan? Bagaimana Anda mengevaluasi elemen mana yang harus diubah posisinya atau diprioritaskan ukurannya saat berpindah dari tampilan desktop ke mobile?
> Saat saya mengatur CSS saya, saya menyadari bahwa margin yang ditentukan secara explicit memberi tantangan saat tampilan diubah ke mobile, posisinya jadi tidak sesuai harapan. Saya mengubah posisi elemen-elemen pada hero-grid dengan menggunakan @media. Untuk masalah karena margin saya jadikan auto, untuk masalah foto terlalu kecil saya berikan width yang sesuai dalam @media.
3. Website yang Anda buat saat ini adalah static web murni. Batasan apa yang Anda rasakan saat mencoba menyajikan informasi pada portofolio Anda secara optimal? Berdasarkan batasan tersebut, fungsionalitas dinamis apa yang paling ingin Anda persiapkan dan tambahkan pada iterasi proyek selanjutnya?
> Batasan yang saya rasa adalah susahnya membuat animasi agar memperindah tampilan, setiap informasi harus di-define untuk segala posisinya, sulit untuk menuangkan ide langsung ke dalam kode-kode. Fungsionalitas dinamis yang saya ingin persiapkan adalah keinteraktifan dan responsivitas agar tampilan lebih jelas enak dibaca dan lebih indah.

### Tugas 2
1. Jelaskan alur yang terjadi ketika pengguna membuka halaman portofolio baru, mulai dari permintaan yang diterima proyek hingga data ditampilkan pada browser. Dalam jawabanmu, jelaskan peran urls.py proyek, urls.py aplikasi, view, model, dan template.
> Ketika pengguna membuka halaman portofolio baru, browser memberi request dan dari urls.py pada proyek, akan diroute ke urls.py pada aplikasi dimana akan ditentukan berdasarkan path yang lebih spesifik, view yang mana yang harus menangani request. Pada views.py alur logika diterapkan, termasuk mengambil data yang diperlukan dari model. Model berinteraksi dengan basis data. Pada views.py, setelah mendapatkan data lewat dictionary context, datanya dioper ke template seperti html, lalu views juga membungkus html menjadi response dengan render(). Terakhir, response dikirim kembali ke browser pengguna melalui django ke server lalu ke browser pengguna untuk diterima dan ditampilkan.
2. Mengapa data untuk bagian portofolio baru sebaiknya disimpan pada model dan tidak ditulis langsung di dalam template? Jelaskan dampaknya terhadap kemudahan pemeliharaan dan pengembangan aplikasi.
> Untuk data bagian portofolio, sebaiknya disimpan pada model karena data tersebut berpotensi dan most-likely untuk berubah dan perlu update. Jika ditulis langsung di dalam template, maka setiap kali ada perbuahan pada data, kita harus secara manual edit lagi templatenya.
> Terhadap kemudahan pemeliharaan, kita dapat menambah/mengedit data tanpa harus menyetuh kode. Mudah untuk ditambah/kurang/edit.
> Terhadap pengembangan aplikasi, jika ditulis dalam template, banyak hal yang tidak dapat dilakukan, seperti jika data ingin disort atau filter, lebih mungkin jika data disimpan dalam model.
3. Apa perbedaan fungsi makemigrations dan migrate pada Django? Berikan contoh perubahan model yang mengharuskanmu menjalankan kedua perintah tersebut.
> Makemigration menciptakan berkas migrasi yang berisi perubahan model yang belum diaplikasikan ke dalam basis data, sedangkan fungsi migrate mengaplikasikan perubahan model yang tercantum dalam berkas migrasi ke basis data dengan menjalankan perintah sebelumnya. Contoh perubahan model adalah saat menambah atribut untuk model Experience untuk menghitung berapa lama experience itu terjadi (contoh sekolah SMA 3 yrs), karena perubahan pada model, contohnya untuk atributnya di sini, maka perlu dilakukan migrasi dengan menjalankan kedua perintah tersebut. 

AI disclosure

Log Tugas 1: https://claude.ai/share/fa8b1141-3df1-49ec-a123-7094f922c4a2
Log Tugas 2: https://claude.ai/share/b93d0e6a-b70c-4c36-b220-0f8e8b6e1a1a


Saya belajar banyak hal dari Claude, mulai dari fungsi dan penjelasan dari seluruh elemen-elemen yang ada dari hasil tutorial 1, sampai ke tahap-tahap selanjutnya untuk memenuhi keinginan saya untuk mengganti pengaturan CSS sesuai dengan keinginan saya. Saya meminta Claude untuk menuntun saya secara bertahap dan respons dari Generative AI tersebut kebanyakan menyuruh saya untuk bereksperimen sendiri lalu menjelaskan hasilnya. Dari situ, banyak yang saya pelajari serta bagaimana selanjutnya saya bisa mengatur tampilan tanpa tuntunan Claude lagi, yang mana sudah terjadi sebagaimana Claude itu sendiri tidak mengetahui apa yang berada di kepala saya, saya mulai mengganti secara manual pada design yang menurut saya kurang memnuhi kepuasan saya, saya jadi belajar mengerti isi dari inspection web-web lain secara mandiri sehingga saya dapat belajar dari hal tersebut dibanding sepenuhnya AI.