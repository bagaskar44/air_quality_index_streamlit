# Dynamic Air Quality Index Dashboard

Dashboard ini menampilkan **kualitas udara (AQI)** secara real-time dari beberapa stasiun pemantauan di Indonesia. Data diambil dari **Air Quality Open Data Platform (WAQI)** dan divisualisasikan menggunakan **Streamlit** dan **Folium** dalam bentuk peta interaktif.

---

### 1. Registrasi & Dapatkan API Token
Daftar terlebih dahulu untuk mendapatkan token API:

https://aqicn.org/data-platform/token/#/

Buat file `.env` pada root project dan masukkan token:
```sh
WAQI_TOKEN=your_api_token_here
```

--- 


### 2. Cari ID Stasiun Target
Cari stasiun yang diinginkan melalui:

https://aqicn.org/station/

Contoh ID stasiun: `A515941` (Tangerang)

---

## 📦 Instalasi

Clone atau download repository ini:

```sh
git clone <your-repo-url>
cd <project-folder>
```

Instal dependency
```sh
pip install -r requirements.txt
```

---

Run Streamlit
```sh
streamlit run app.py
```
