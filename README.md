# BijakPinjam

## Deskripsi Proyek

BijakPinjam adalah aplikasi berbasis AI yang membantu pengguna mengevaluasi kelayakan pinjaman dan kesehatan finansial sebelum mengambil keputusan kredit. Sistem menggunakan Machine Learning untuk menghasilkan Credit Risk Score, Financial Health Score, serta rekomendasi finansial yang dapat membantu pengguna memahami dampak pinjaman terhadap kondisi keuangan mereka.

## Setup Environment

### 1. Clone Repository

```bash
git clone https://github.com/NoobAgain/BijakPinjam.git
cd BijakPinjam
```

### 2. Buat Virtual Environment

```bash
python -m venv venv
```

Aktivasi virtual environment:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> Catatan: Pastikan menggunakan versi **scikit-learn 1.8.0** karena model dan file preprocessing dibuat menggunakan versi tersebut.

## Model Machine Learning

Model dan file preprocessing tersedia pada repository:

- `machine_learning/model_risiko_pinjaman_xgb.pkl`
- `machine_learning/scaler_finansial.joblib`
- `models/encoder_status_pekerjaan.joblib`

Jika diperlukan, model juga dapat diunduh melalui Google Drive berikut:

```
https://drive.google.com/file/d/1GDOYmUJqxZjcOxiBx_yoshq6qOHqkkJW/view?usp=sharing
```

## Cara Menjalankan Aplikasi

Jalankan aplikasi Streamlit dengan perintah berikut:

```bash
streamlit run app.py
```

Setelah berhasil dijalankan, aplikasi dapat diakses melalui browser pada alamat:

```text
http://localhost:8501
```
