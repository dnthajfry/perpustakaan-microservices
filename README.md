# Tugas Pengganti — Microservice Perpustakaan (FastAPI)

Tiga microservice sederhana untuk simulasi sistem perpustakaan:

| Service          | Port  | Tanggung Jawab                                   |
|------------------|-------|--------------------------------------------------|
| `book-service`   | 8001  | CRUD data buku & manajemen stok                  |
| `member-service` | 8002  | CRUD data anggota perpustakaan                   |
| `loan-service`   | 8003  | Mencatat peminjaman & pengembalian buku          |

`loan-service` memanggil `book-service` dan `member-service` lewat HTTP (`httpx`)
untuk memvalidasi data dan mengubah stok buku.

## Instalasi

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

## Menjalankan (buka 3 terminal terpisah)

**Terminal 1 — Book Service (port 8001)**
```bash
cd book-service
uvicorn main:app --reload --port 8001
```

**Terminal 2 — Member Service (port 8002)**
```bash
cd member-service
uvicorn main:app --reload --port 8002
```

**Terminal 3 — Loan Service (port 8003)**
```bash
cd loan-service
uvicorn main:app --reload --port 8003
```

## Dokumentasi otomatis (Swagger UI)

- Book Service:   <http://127.0.0.1:8001/docs>
- Member Service: <http://127.0.0.1:8002/docs>
- Loan Service:   <http://127.0.0.1:8003/docs>

## Contoh alur uji coba

1. Buka `http://127.0.0.1:8001/docs`, lihat daftar buku yang sudah di-seed.
2. Buka `http://127.0.0.1:8002/docs`, lihat daftar anggota.
3. Buka `http://127.0.0.1:8003/docs`, panggil `POST /loans/` dengan
   `{"member_id": 1, "book_id": 1}`. Stok buku otomatis berkurang.
4. Panggil `POST /loans/1/kembalikan` untuk mengembalikan buku.

Penjelasan lengkap kenapa ini disebut **microservice** (bukan monolith) ada di
[laporan.md](laporan.md).
