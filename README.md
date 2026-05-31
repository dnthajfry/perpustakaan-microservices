

1. Buka `http://127.0.0.1:8001/docs`, lihat daftar buku yang sudah di-seed.
2. Buka `http://127.0.0.1:8002/docs`, lihat daftar anggota.
3. Buka `http://127.0.0.1:8003/docs`, panggil `POST /loans/` dengan
   `{"member_id": 1, "book_id": 1}`. Stok buku otomatis berkurang.
4. Panggil `POST /loans/1/kembalikan` untuk mengembalikan buku.
