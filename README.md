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

### Tugas 3
1. Jelaskan mengapa kita menggunakan ModelForm pada Django alih-alih membuat form HTML secara manual. Selain itu, jelaskan pula mengapa kita diwajibkan menambahkan {% csrf_token %} pada form tersebut!
> Karena ModelForm pada Django menghindari duplikasi kode (dibanding kalau menggunakan HTML secara manual yang menulis kode berulang kali untuk pgae yang berbeda namun informasi header yang sama), ModelForm juga lebih aman dengan menggunakan CSRF, terintegrasi penuh dengan Admin, CSV, dll. Tujuan dari penggunaan CSRF selain diwajibkan oleh Django dalam pembuatan Form adalah untuk mencegah penyerang aplikasi mengubah request yang awalnya ke server Django kalian menjadi ke suatu API yang berbahaya dan mengirimkan data request kalian ke mereka.
2. Pada Tutorial 03, kita membahas format data JSON dan XML. Mengapa JSON lebih disukai dalam pengembangan aplikasi web modern dibandingkan XML?
> JSON lebih disukai dibandingkan XML pada aplikasi web modern karena ukurannya yang lebih ringkas, parser yang sangat cepat, dan integrasi yang sangat natural dengan JavaScript di sisi frontend.
3. Jelaskan alur yang terjadi saat kamu menggunakan fungsi view untuk mengembalikan data portofoliomu dalam bentuk JSON. Mengapa kita perlu melakukan proses serialization pada model Django sebelum datanya dikembalikan?
> Saat view mengembalikan JSON, Django menerima request, mencocokkan URL ke view, mengambil data lewat ORM sebagai objek Python, menserialisasikannya menjadi string JSON, lalu mengirimnya sebagai HttpResponse dengan header application/json. Serialization diperlukan karena objek model dan QuerySet bukan tipe yang dikenali JSON dan tidak bisa dikirim lewat HTTP, banyak tipe data Python harus dikonversi, dan proses ini memberi Anda kendali atas field yang diekspos serta struktur data yang diterima client.

### Tugas 4
AI Disclosure Tugas 4:
Saya menggunakan AI untuk memberi pemahaman atas kesalahpahaman saya terhadap bagaimana kerjanya session dan cookies. Saya juga memintanya untuk menjelaskan bagaimana proses membuat group Editor dan aproach yang bisa diambil. Saya memodifikasikan sendiri sesuai dengan yang diminta pada Tugas 4 agar Editor hanya bisa meng-edit. Saya juga meminta AI untuk debug error yang sudah saya coba men-debug sendiri tetapi kurang teliti.

### Tugas 5
1. Jelaskan apa itu debouncing dan mengapa teknik ini penting diterapkan pada fitur pencarian yang menggunakan AJAX!
> Debouncing adalah teknik untuk menunda sebuah fungsi hingga suatu jeda waktu berlalu tanpa event baru. Selama pengguna masih mengetik, timer sebelumnya dibatalkan dan dimulai lagi. Dengan demikian, browser hanya mengirim permintaan setelah pengguna berhenti mengetik selama sejenak.Teknik ini penting untuk fitur pencarian yang menggunakan AJAX karena otherwise pencarian akan diproses setiap karakter, yang mengakibatkan load server berkali-kali.

2. Jelaskan fungsi dari penggunaan await ketika kita menggunakan fetch()! Apa yang akan terjadi jika kita tidak menggunakan await?
> await adalah keyword yang hanya bisa digunakan di dalam async function dan berfungsi untuk “menunggu” Promise selesai diproses sebelum melanjutkan ke baris kode berikutnya. Tanpa await, sebuah Promise akan tetap berjalan di belakang layar dan kode berikutnya akan langsung dieksekusi tanpa menunggu hasilnya.

3. Jelaskan apa itu serangan XSS (Cross-Site Scripting) dan mengapa data yang ditampilkan melalui AJAX/JavaScript lebih rentan terhadap serangan ini daripada data yang ditampilkan langsung melalui template Django!
> serangan Cross-Site Scripting (XSS) adalah serangan ketika penyerang berhasil menyisipkan kode JavaScript miliknya ke dalam halaman web yang kemudian dijalankan di browser pengguna lain, contohnya jika kode berbahaya disimpan pada database lalu ikut dijalankan setiap kali data tersebut ditampilkan.
> Karena pada template Django, dilakikan auto-escaping pada setiap { variabel }. Karakter seperti < dan > diubah menjadi &lt; dan &gt; sehingga browser menampilkannya sebagai teks biasa, bukan sebagai tag HTML. Perlindungan itu hilang ketika kita pindah ke AJAX. Pada buildProjectCardElement, data dari JSON disisipkan ke dalam template literal lalu dipasang lewat innerHTML. Tidak ada lagi Django yang melakukan escaping sehingga browser akan memperlakukan setiap tag HTML di dalam data sebagai kode sungguhan.

AI disclosure Tugas 5:
Pada Tugas 5, AI saya gunakan untuk membantu debugging terkait logical error yang saya alami. Saya juga menanya mengenai konsep yang kurang saya mengerti.

---

__AI disclosure keseluruhan__

Log Tugas 1: https://claude.ai/share/fa8b1141-3df1-49ec-a123-7094f922c4a2
Log Tugas 2, 3, 4: https://claude.ai/share/b93d0e6a-b70c-4c36-b220-0f8e8b6e1a1a
Log Tugas 5: https://claude.ai/share/05e8dc02-0f93-4fd2-b956-8333c90ae748


Saya belajar banyak hal dari Claude, mulai dari fungsi dan penjelasan dari seluruh elemen-elemen yang ada dari hasil tutorial 1, sampai ke tahap-tahap selanjutnya untuk memenuhi keinginan saya untuk mengganti pengaturan CSS sesuai dengan keinginan saya. Saya meminta Claude untuk menuntun saya secara bertahap dan respons dari Generative AI tersebut kebanyakan menyuruh saya untuk bereksperimen sendiri lalu menjelaskan hasilnya. Dari situ, banyak yang saya pelajari serta bagaimana selanjutnya saya bisa mengatur tampilan tanpa tuntunan Claude lagi, yang mana sudah terjadi sebagaimana Claude itu sendiri tidak mengetahui apa yang berada di kepala saya, saya mulai mengganti secara manual pada design yang menurut saya kurang memnuhi kepuasan saya, saya jadi belajar mengerti isi dari inspection web-web lain secara mandiri sehingga saya dapat belajar dari hal tersebut dibanding sepenuhnya AI.