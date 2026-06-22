from datetime import datetime
from engine.rules import RULES, BOBOT_KESULITAN, BOBOT_KATEGORI, PRIORITAS_ORDER


def hitung_sisa_hari(deadline_str):
    try:
        try:
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")
        except:
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d").replace(hour=23, minute=59)
        return (deadline - datetime.now()).days
    except:
        return 999


def hitung_skor(sisa_hari, kesulitan, kategori, bonus):
    if sisa_hari <= 0:
        skor_deadline = 100
    elif sisa_hari <= 1:
        skor_deadline = 90
    elif sisa_hari <= 3:
        skor_deadline = 70
    elif sisa_hari <= 7:
        skor_deadline = 50
    elif sisa_hari <= 14:
        skor_deadline = 30
    else:
        skor_deadline = 10
    skor_kesulitan = BOBOT_KESULITAN.get(kesulitan, 1) * 10
    skor_kategori  = BOBOT_KATEGORI.get(kategori, 1) * 5
    return skor_deadline + skor_kesulitan + skor_kategori + bonus


def forward_chaining(tugas):
    sisa_hari = hitung_sisa_hari(tugas["deadline"])
    kesulitan = tugas["kesulitan"]
    kategori  = tugas["kategori"]

    rule_cocok = None
    for rule in RULES:
        kondisi = rule["kondisi"]
        cocok   = True
        if "sisa_hari_maks" in kondisi and sisa_hari > kondisi["sisa_hari_maks"]:
            cocok = False
        if "sisa_hari_min" in kondisi and sisa_hari < kondisi["sisa_hari_min"]:
            cocok = False
        if "kesulitan" in kondisi and kesulitan not in kondisi["kesulitan"]:
            cocok = False
        if cocok:
            rule_cocok = rule
            break

    if not rule_cocok:
        rule_cocok = RULES[-1]

    skor = hitung_skor(sisa_hari, kesulitan, kategori, rule_cocok["skor_bonus"])

    return {
        "prioritas": rule_cocok["prioritas"],
        "saran":     rule_cocok["saran"],
        "rule_id":   rule_cocok["id"],
        "sisa_hari": sisa_hari,
        "skor":      skor,
    }


def analisis_semua_tugas(daftar_tugas):
    hasil = []
    for tugas in daftar_tugas:
        if tugas.get("selesai", False):
            continue
        analisis = forward_chaining(tugas)
        hasil.append({**tugas, **analisis})
    hasil.sort(key=lambda x: (PRIORITAS_ORDER.get(x["prioritas"], 99), -x["skor"]))
    return hasil