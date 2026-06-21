import json
import os
from datetime import datetime

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/tasks.json")


def load_tasks():
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            return []
        return json.loads(content)


def save_tasks(tasks):
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def tambah_tugas(nama, kategori, deadline, kesulitan, deskripsi=""):
    tasks = load_tasks()
    tugas_baru = {
        "id":       datetime.now().strftime("%Y%m%d%H%M%S"),
        "nama":     nama,
        "kategori": kategori,
        "deadline": deadline,
        "kesulitan":kesulitan,
        "deskripsi":deskripsi,
        "selesai":  False,
        "dibuat":   datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    tasks.append(tugas_baru)
    save_tasks(tasks)
    return tugas_baru


def tandai_selesai(task_id):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["selesai"]         = True
            t["tanggal_selesai"] = datetime.now().strftime("%Y-%m-%d")
    save_tasks(tasks)


def hapus_tugas(task_id):
    tasks = load_tasks()
    tasks = [t for t in tasks if t["id"] != task_id]
    save_tasks(tasks)