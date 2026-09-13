**# assignment-data-pipeline-Rafif-Razaan-Ananto**
Assignment 1 data cleanning, pipeline, and transformation
**# Automobile Data Pipeline Project**

## Deskripsi Singkat Dataset
Dataset ini memuat informasi mengenai berbagai jenis mobil, meliputi karakteristik spesifikasi kendaraan (seperti jenis bahan bakar, gaya bodi, dimensi, spesifikasi mesin) serta tingkat risiko asuransi (symboling) dan nilai kerugian (normalized-losses). Dataset ini digunakan untuk kebutuhan analisis data otomotif dan prediksi harga.

## Sumber Dataset
File dataset mentah diambil dari file CSV internal yang berlokasi di dalam folder `raw/` dengan nama `automobileEDA_dirty_training.csv`.

## Struktur Folder Project
'''text
Data Pipeline assignment/
├── data/
│   ├── raw/
│   │   └── automobileEDA_dirty_training.csv
│   ├── pipeline.py
│   └── processed_dataset.csv
└── README.md
└── Requirement.txt
'''
## Struktur Folder Project
Dataset ini memiliki 209 baris dengan 30 kolom sebelum dilakukan cleanning, setelah dilakukan cleanning terdapat baris sebanyak 189 dengan 31 kolom

## Permasalahan yang ditemukan
1. Tipe Data Tidak Sesuai: Kolom transaction_date dibaca sebagai string dengan format tanggal yang acak/bercampur, bukan datetime.
2. Missing Values (Nilai Kosong): Terdapat nilai NaN (kosong) pada kolom stroke, horsepower, price, horsepower-binned, dll.  Format Teks Tidak Konsisten: Pada kolom kategori seperti 'make', terdapat penulisan huruf besar/kecil yang bercampur (contoh: "audi" dan "Audi", "alfa-romero" dan "ALFA-ROMERO").
3. Terdapat juga tambahan spasi yang tidak perlu di akhir kata (contoh: "dodge " atau "mercury ").
4. Data Numerik Ditulis sebagai String: Kolom num-of-doors dan num-of-cylinders ditulis dengan huruf bahasa Inggris (contoh: "two", "four", "six") alih-alih angka.
5. Kolom NaN di drop karena persentase nya sangat kecil

## Transformasi yang dilakukan
1. Ordinal Encoding: Diterapkan pada kolom horsepower-binned. Mengubah tingkat ['Low', 'Medium', 'High'] menjadi urutan numerik (0, 1, 2) karena nilainya memiliki tingkatan (hierarki).
2. One-Hot Encoding: Diterapkan pada kolom nominal (seperti make, body-style, engine-type, dll). Mengubah 1 kolom teks menjadi banyak kolom matriks binary (0 dan 1) karena Machine Learning hanya memahami angka.

3. Min-Max Scaling: Diterapkan pada seluruh variabel numerik kontinu (seperti price, engine-size, length). Skala diubah agar rentangnya seragam antara 0 dan 1, mencegah angka bernilai puluhan ribu mendominasi perhitungan algoritma.

## Contoh data sebelum dan sesudah dilakukan transformasi

Berikut adalah perbandingan nilai pada beberapa kolom sebelum dan sesudah tahap *Data Transformation*:

| Nama Kolom Asli | Jenis Transformasi | Contoh Nilai Sebelum | Hasil Sesudah Transformasi (Nilai / Kolom Baru) |
| :--- | :--- | :--- | :--- |
| `horsepower-binned` | **Ordinal Encoding** | `"Medium"` | `1.0` |
| `horsepower-binned` | **Ordinal Encoding** | `"Low"` | `0.0` |
| `engine-size` | **Min-Max Scaling** | `130` | `0.2604` |
| `peak-rpm` | **Min-Max Scaling** | `5000.0` | `0.3469` |
| `fuel-system` | **One-Hot Encoding** | `"mpfi"` | `fuel-system_mpfi` = `1`, `fuel-system_2bbl` = `0` |
| `make` | **One-Hot Encoding** | `"audi"` | `make_audi` = `1`, `make_bmw` = `0`, `make_honda` = `0` |

## Cara menjalankan code
python pipeline.py

## Penjelasan sederhana ETL
1. Extract (Mengekstrak): Script akan memuat data mentah (raw/automobileEDA_dirty_training.csv) ke dalam struktur data Pandas DataFrame.

2. Transform (Mengubah): Data dibersihkan dari missing values dan format yang salah. Setelah itu, tipe data diubah melalui skema Encoding (untuk teks) dan Scaling (untuk angka) agar siap dimasukkan ke dalam model Machine Learning.

3. Load (Memuat/Menyimpan): Data bersih dan tertransformasi kemudian disimpan atau di-ekspor menjadi sebuah file CSV baru.
