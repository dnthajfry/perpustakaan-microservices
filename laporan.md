# Laporan Tugas Pengganti — Microservice Perpustakaan

**Nama:** Dentha Jefry Antara
**Framework:** FastAPI (Python)

---

## 1. Yang Saya Kerjakan

Saya membuat sebuah sistem perpustakaan sederhana, lalu memecahnya menjadi
**3 service terpisah**. Tiap service saya buat di folder sendiri, saya
jalankan sebagai proses sendiri, dan saya beri port yang berbeda.

| Service          | Port | Tugas yang saya berikan                |
|------------------|------|----------------------------------------|
| `book-service`   | 8001 | Mengelola data buku & stok             |
| `member-service` | 8002 | Mengelola data anggota perpustakaan    |
| `loan-service`   | 8003 | Mencatat peminjaman & pengembalian     |

```
   ┌──────────────┐     ┌────────────────┐
   │ book-service │     │ member-service │
   │    :8001     │     │     :8002      │
   └──────▲───────┘     └────────▲───────┘
          │  HTTP                │  HTTP
          │                      │
          └─────────┬────────────┘
                    │
            ┌───────┴────────┐
            │  loan-service  │
            │     :8003      │
            └────────────────┘
```

Saya sengaja **tidak menyimpan** data buku atau anggota di dalam
`loan-service`. Ketika ada peminjaman, saya membuat `loan-service` menghubungi
`book-service` dan `member-service` lewat HTTP (menggunakan library `httpx`)
untuk memvalidasi data dan mengurangi stok buku.

---

## 2. Alasan Saya Menyebut Ini Microservice (Bukan Monolith)

### a. Saya memisahkan kode dan data tiap domain

Saya membuat folder `book-service/`, `member-service/`, dan `loan-service/`
yang berdiri sendiri. Tiap service saya beri `database` (list in-memory)
miliknya sendiri di dalam folder `services/`. Saya tidak pernah meng-`import`
data antar service. Kalau saya menggabung ketiganya jadi satu folder dengan
satu database bersama, itu sudah menjadi monolith.

### b. Saya menjalankan tiap service sebagai proses berbeda

Saat menguji, saya membuka **3 terminal**, lalu di tiap terminal saya
menjalankan perintah `uvicorn` yang berbeda dengan port yang berbeda
(8001, 8002, 8003). Artinya saya benar-benar punya 3 aplikasi yang hidup
sendiri-sendiri. Pada monolith saya cukup menjalankan 1 perintah `uvicorn`
karena hanya ada 1 aplikasi.

### c. Saya membuat antar service berkomunikasi lewat **permintaan HTTP**

Ketika `loan-service` butuh data buku, saya membuatnya **mengirim permintaan
HTTP** ke `book-service` lewat jaringan (alamat `http://127.0.0.1:8001`),
mirip seperti browser meminta halaman web. Ini bisa dilihat di
[loan-service/services/loan_services.py](loan-service/services/loan_services.py):

```python
r = httpx.get(f"{BOOK_SERVICE_URL}/books/{book_id}", timeout=5.0)
```

Kalau saya menggabungnya jadi monolith, saya cukup menulis
`from book_services import get_book_by_id` di file `loan` lalu memanggil
fungsinya langsung — tanpa jaringan, tanpa HTTP, semua di proses yang sama.

Perbedaan yang saya alami sendiri:

| Aspek                     | Monolith                              | Yang saya buat                          |
|---------------------------|---------------------------------------|-----------------------------------------|
| Cara memanggil            | `get_book_by_id(1)` (fungsi Python)   | `httpx.get(".../books/1")` (HTTP)       |
| Lokasi service tujuan     | Di dalam proses yang sama             | Proses lain, port lain (8001)           |
| Format data               | Object Python                         | JSON                                    |
| Kalau service tujuan mati | Tidak mungkin — satu proses           | Permintaan HTTP gagal (timeout / 503)   |

Karena `loan-service` yang saya buat hanya tahu **alamat URL** dan **kontrak
API** milik `book-service` (bukan kode internalnya), keduanya benar-benar
terpisah.

### d. Saya bisa me-restart satu service tanpa mengganggu yang lain

Ketika saya mengubah kode di `loan-service`, saya cukup me-restart terminal
port 8003 saja. Service di port 8001 dan 8002 tetap melayani permintaan tanpa
saya sentuh. Pada monolith, satu perubahan kecil di mana pun memaksa saya
me-restart seluruh aplikasi.

### e. Saya menguji **fault isolation** dan terbukti

Saya mematikan `member-service` di port 8002 dengan Ctrl+C, lalu saya coba:

- Di port 8001, `GET /books/` → **tetap jalan normal**.
- Di port 8003, `POST /loans/` → **gagal dengan 503** "Member Service tidak
  dapat dihubungi".
- Di port 8003, `GET /loans/` → **tetap jalan** karena tidak butuh data
  anggota.

Hasil ini menunjukkan satu service yang mati tidak menjatuhkan service lain.
Kalau saya satukan jadi monolith, modul `member` yang error akan menjatuhkan
seluruh aplikasi (termasuk fitur buku dan peminjaman).

### f. Saya bisa men-scale tiap service secara terpisah

Kalau saya tahu endpoint buku adalah yang paling sibuk, saya bisa menjalankan
beberapa instance `book-service` sekaligus, sementara `member-service` cukup
1 instance. Pada monolith saya tidak bisa memilih — saya terpaksa
menggandakan seluruh aplikasi meskipun hanya 1 fitur yang sibuk.

---

## 3. Ringkasan Perbandingan

| Aspek                       | Monolith                  | Yang saya buat                   |
|-----------------------------|---------------------------|----------------------------------|
| Jumlah proses berjalan      | 1                         | 3 (book, member, loan)           |
| Cara antar modul memanggil  | Import fungsi             | HTTP request (`httpx`)           |
| Database                    | 1 database bersama        | 1 data store per service         |
| Restart 1 fitur             | Restart semua             | Restart service itu saja         |
| 1 modul crash               | Seluruh aplikasi down     | Hanya service itu yang terdampak |
| Scaling                     | Bareng-bareng             | Per service                      |

---

## 4. Hasil Uji Coba yang Saya Lakukan

Saya menguji sistem lewat Swagger UI dengan alur berikut:

1. Saya membuka `8001/docs` lalu memanggil `GET /books/` — data buku seed
   muncul.
2. Saya memanggil `POST /loans/` di `8003/docs` dengan
   `{"member_id": 1, "book_id": 1}`. Responsnya berisi data anggota (yang
   diambil dari port 8002) dan data buku (yang diambil dari port 8001) —
   bukti bahwa `loan-service` benar-benar memanggil dua service lain.
3. Saya memanggil lagi `GET /books/1` dan stok buku **berkurang 1**. Ini
   memastikan `loan-service` tidak hanya membaca tetapi juga memerintahkan
   `book-service` untuk mengubah stok.
4. Saya memanggil `POST /loans/1/kembalikan` — stok buku **naik kembali**.
5. Saya menguji kasus error: `member_id` yang tidak ada → 404, stok habis →
   400. Semua tertangani dengan benar.
6. Saya mematikan `member-service` untuk membuktikan fault isolation, dan
   hasilnya seperti yang saya jelaskan di poin 2.e.

---

## 5. Kesimpulan

Saya menyebut sistem ini sebagai **microservice** karena saya benar-benar
memisahkan **kode, data, proses, dan jalur komunikasinya** sesuai prinsip
microservice. Kalau saya menggabung ketiga domain ini menjadi 1 aplikasi
FastAPI — 1 `main.py`, 1 database, 1 proses uvicorn — yang saya buat akan
menjadi **monolith**, karena seluruh tanggung jawab menyatu dalam satu unit
yang deploy-nya, datanya, dan siklus hidupnya tidak bisa dipisahkan.
