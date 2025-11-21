# 📝 Catatan App Backend (Python)

Backend untuk aplikasi **Catatan**, dibangun dengan Python + FastAPI.  

---

## 📂 Struktur Proyek

```log
backend/
├── api/
│ ├── init.py
│ ├── index.py # Entry point untuk Vercel
│ ├── models.py # Pydantic Schemas
│ └── service.py # Business Logic
├── requirements.txt
└── vercel.json
```


---

## 🚀 Fitur Utama

- ⚡ FastAPI untuk performa cepat dan modern  
- 🧹 Validasi clean code dengan Pydantic  
- 🧠 Service-layer architecture untuk pemisahan logic  

---

## 🛠 Instalasi & Setup

### 1. Clone repository
```bash
git clone <repo-url>
cd backend
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Jalankan server lokal
```bash
uvicorn api.index:app --reload
```

Akses via:
http://localhost:8000
