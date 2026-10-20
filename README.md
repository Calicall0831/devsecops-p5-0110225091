# TaskTracker API (devsecops-p5-0110225091)

## 1. Nama Aplikasi & Fungsi
**TaskTracker API** adalah REST API sederhana untuk mengelola daftar tugas (to-do):
membuat, melihat, memperbarui, menghapus, menyaring tugas berdasarkan status/prioritas,
serta menampilkan statistik penyelesaian tugas. Data disimpan in-memory.

## 2. Bahasa / Framework
- Python 3.11+
- Flask 3 (web framework)
- pytest + pytest-cov (unit test & coverage)
- Bandit (SAST)

Struktur source code:
```
app/__init__.py     # application factory
app/models.py       # dataclass Task
app/storage.py      # penyimpanan in-memory
app/validators.py   # validasi input
app/stats.py        # statistik tugas
app/routes.py       # endpoint REST
run.py              # entry point
tests/              # 21 unit test
scripts/quality_gate.py
.github/workflows/devsecops.yml
```

## 3. Cara Menjalankan
```bash
git clone https://github.com/USERNAME/devsecops-p5-0110225091.git
cd devsecops-p5-0110225091
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
python run.py                                       # http://127.0.0.1:5000
pytest --cov=app                                    # menjalankan unit test
```
Contoh pemakaian:
```bash
curl -X POST http://127.0.0.1:5000/tasks -H "Content-Type: application/json" \
     -d '{"title":"Belajar DevSecOps","priority":"high"}'
curl http://127.0.0.1:5000/tasks
curl http://127.0.0.1:5000/stats
```

| Method | Endpoint | Fungsi |
|---|---|---|
| GET | /health | Cek status |
| GET/POST | /tasks | Daftar / buat tugas |
| GET/PUT/DELETE | /tasks/{id} | Detail / ubah / hapus |
| GET | /stats | Statistik tugas |

## 4. Overview Pipeline CI/CD
Workflow `.github/workflows/devsecops.yml` terpicu pada **push** dan **pull_request** ke `main`,
berjalan di `ubuntu-latest`, dengan tiga job berurutan:

1. **build** - install dependencies, jalankan unit test, Quality Gate coverage >= 80%.
2. **sast-scan** (`needs: build`) - Bandit memindai kode, laporan JSON diunggah sebagai artifact.
3. **quality-gate** (`needs: sast-scan`) - pipeline gagal bila ada temuan severity HIGH atau MEDIUM.
