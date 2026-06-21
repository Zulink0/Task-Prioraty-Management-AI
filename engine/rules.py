RULES = [
    {
        "id": "R01",
        "kondisi": {"sisa_hari_maks": 1, "kesulitan": ["Mudah", "Sedang", "Sulit"]},
        "prioritas": "KRITIS",
        "skor_bonus": 50,
        "saran": "Kerjakan SEKARANG! Tinggalkan aktivitas lain terlebih dahulu.",
    },
    {
        "id": "R02",
        "kondisi": {"sisa_hari_maks": 3, "kesulitan": ["Sulit"]},
        "prioritas": "KRITIS",
        "skor_bonus": 40,
        "saran": "Deadline dekat dan tugas berat. Mulai segera, cicil per bagian!",
    },
    {
        "id": "R03",
        "kondisi": {"sisa_hari_maks": 3, "kesulitan": ["Sedang", "Mudah"]},
        "prioritas": "TINGGI",
        "skor_bonus": 30,
        "saran": "Selesaikan dalam 24 jam ke depan. Jangan tunda lagi!",
    },
    {
        "id": "R04",
        "kondisi": {"sisa_hari_maks": 7, "kesulitan": ["Sulit"]},
        "prioritas": "TINGGI",
        "skor_bonus": 25,
        "saran": "Mulai cicil sekarang. Tugas sulit butuh waktu lebih banyak.",
    },
    {
        "id": "R05",
        "kondisi": {"sisa_hari_maks": 7, "kesulitan": ["Sedang"]},
        "prioritas": "SEDANG",
        "skor_bonus": 15,
        "saran": "Rencanakan dan mulai dalam 2-3 hari ini.",
    },
    {
        "id": "R06",
        "kondisi": {"sisa_hari_min": 8, "kesulitan": ["Sulit"]},
        "prioritas": "SEDANG",
        "skor_bonus": 10,
        "saran": "Masih ada waktu, tapi jangan ditunda. Buat jadwal cicilan.",
    },
    {
        "id": "R07",
        "kondisi": {"sisa_hari_min": 8, "kesulitan": ["Mudah", "Sedang"]},
        "prioritas": "RENDAH",
        "skor_bonus": 0,
        "saran": "Jadwalkan di waktu senggang. Masih aman.",
    },
]

BOBOT_KESULITAN = {"Mudah": 1, "Sedang": 2, "Sulit": 3}
BOBOT_KATEGORI  = {"Kuliah": 3, "Organisasi": 2, "Pribadi": 1}
PRIORITAS_ORDER = {"KRITIS": 0, "TINGGI": 1, "SEDANG": 2, "RENDAH": 3}