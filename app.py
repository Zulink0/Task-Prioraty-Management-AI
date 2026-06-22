import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, date, timedelta
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from engine.expert_system import analisis_semua_tugas
from utils.storage import load_tasks, tambah_tugas, tandai_selesai, hapus_tugas

st.set_page_config(
    page_title="AI Prioritas Tugas",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .block-container { padding: 2rem 2.5rem; }
    [data-testid="InputInstructions"] { display: none !important; }

    .page-title { font-size:1.6rem; font-weight:700; color:#e8e8ff; margin-bottom:0; }
    .page-sub   { font-size:0.85rem; color:#6666aa; margin-top:0.2rem; margin-bottom:1rem; }

    .card { border-left:3px solid #444; border-radius:8px; padding:0.85rem 1.1rem; margin-bottom:0.5rem; background:#13131f; }
    .card-kritis { border-color:#cc3333; }
    .card-tinggi { border-color:#cc6600; }
    .card-sedang { border-color:#aaaa00; }
    .card-rendah { border-color:#008844; }

    .badge { display:inline-block; padding:1px 9px; border-radius:4px; font-size:0.7rem; font-weight:700; letter-spacing:0.05em; }
    .badge-kritis { background:#cc3333; color:#fff; }
    .badge-tinggi { background:#cc6600; color:#fff; }
    .badge-sedang { background:#aaaa00; color:#111; }
    .badge-rendah { background:#008844; color:#fff; }

    .task-name  { font-size:0.98rem; font-weight:600; color:#ddddf0; }
    .task-meta  { font-size:0.78rem; color:#6666aa; margin-top:3px; }
    .task-saran { font-size:0.82rem; color:#9999bb; margin-top:5px; }

    .stat-box   { background:#13131f; border:1px solid #222238; border-radius:8px; padding:1rem; text-align:center; }
    .stat-num   { font-size:1.8rem; font-weight:700; }
    .stat-label { font-size:0.75rem; color:#6666aa; margin-top:2px; }

    .warning-bar { background:#1e0a0a; border-left:3px solid #cc3333; border-radius:6px; padding:0.7rem 1rem; margin-bottom:1rem; color:#cc9999; font-size:0.85rem; }

    div[data-testid="stSidebar"] { background:#0d0d1a; border-right:1px solid #1a1a30; }
    div[data-testid="stSidebar"] * { color:#bbbbdd !important; }

    .stButton > button { background:#1a1a30; color:#bbbbdd; border:1px solid #333355; border-radius:6px; font-size:0.82rem; transition:all 0.15s; }
    .stButton > button:hover { background:#25253a; border-color:#5555aa; }

    .stTextInput input, .stSelectbox select, .stDateInput input, .stTextArea textarea {
        background:#13131f !important; color:#ddddee !important;
        border:1px solid #222238 !important; border-radius:6px !important; font-size:0.88rem !important;
    }
    .stTabs [data-baseweb="tab"] { font-size:0.85rem; padding:6px 16px; }
</style>
""", unsafe_allow_html=True)

color_map = {"KRITIS": "#cc3333", "TINGGI": "#cc6600", "SEDANG": "#aaaa00", "RENDAH": "#008844"}


# ─── SIDEBAR ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Tambah Tugas")
    st.markdown("---")
    with st.form("form_tugas", clear_on_submit=True):
        nama      = st.text_input("Nama Tugas", placeholder="Contoh: Tugas Makalah AI")
        kategori  = st.selectbox("Kategori", ["Kuliah", "Organisasi", "Pribadi"])
        deadline  = st.date_input("Deadline (Tanggal)", min_value=date.today(), value=date.today() + timedelta(days=3))
        col_jam, col_menit = st.columns(2)
        with col_jam:
            jam   = st.number_input("Jam", min_value=0, max_value=23, value=23, step=1)
        with col_menit:
            menit = st.number_input("Menit", min_value=0, max_value=59, value=59, step=1)
        kesulitan = st.radio("Kesulitan", ["Mudah", "Sedang", "Sulit"], horizontal=True)
        deskripsi = st.text_area("Deskripsi (opsional)", placeholder="Detail tugas...", height=70)
        submit    = st.form_submit_button("Tambahkan", use_container_width=True)
        if submit:
            if nama.strip():
                deadline_str = f"{deadline} {jam:02d}:{menit:02d}"
                tambah_tugas(nama.strip(), kategori, deadline_str, kesulitan, deskripsi)
                st.success("Tugas berhasil ditambahkan.")
                st.rerun()
            else:
                st.error("Nama tugas tidak boleh kosong.")

    st.markdown("---")
    st.markdown("### Tentang Sistem")
    st.markdown("""
**Jenis AI:** Expert System  
**Teknik:** Forward Chaining  
**Rules:** 7 aturan IF-THEN  

Sistem mencocokkan kondisi tugas dengan rule base untuk menentukan prioritas.
    """)

# ─── HEADER ───────────────────────────────────────────────
st.markdown('<div class="page-title">AI Penentu Prioritas Tugas</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Expert System — Forward Chaining</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── LOAD DATA ────────────────────────────────────────────
semua_tugas    = load_tasks()
tugas_aktif    = [t for t in semua_tugas if not t.get("selesai", False)]
tugas_selesai  = [t for t in semua_tugas if t.get("selesai", False)]
hasil_analisis = analisis_semua_tugas(tugas_aktif)

jml_kritis = sum(1 for t in hasil_analisis if t["prioritas"] == "KRITIS")
jml_tinggi = sum(1 for t in hasil_analisis if t["prioritas"] == "TINGGI")
jml_sedang = sum(1 for t in hasil_analisis if t["prioritas"] == "SEDANG")
jml_rendah = sum(1 for t in hasil_analisis if t["prioritas"] == "RENDAH")

# ─── STATISTIK ────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)
for col, num, label, warna in [
    (c1, len(tugas_aktif), "Total Aktif", "#aaaacc"),
    (c2, jml_kritis,       "Kritis",      "#cc3333"),
    (c3, jml_tinggi,       "Tinggi",      "#cc6600"),
    (c4, jml_sedang,       "Sedang",      "#aaaa00"),
    (c5, jml_rendah,       "Rendah",      "#008844"),
]:
    with col:
        st.markdown(f'<div class="stat-box"><div class="stat-num" style="color:{warna}">{num}</div><div class="stat-label">{label}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── WARNING ──────────────────────────────────────────────
if jml_kritis > 0:
    nama_kritis = ", ".join(t["nama"] for t in hasil_analisis if t["prioritas"] == "KRITIS")
    st.markdown(f'<div class="warning-bar"><strong>Perhatian:</strong> {jml_kritis} tugas kritis — {nama_kritis}</div>', unsafe_allow_html=True)

# ─── TABS ─────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["Ranking Prioritas", "Countdown", "Visualisasi", "Selesai"])

# ══ TAB 1: RANKING ════════════════════════════════════════
with tab1:
    if not hasil_analisis:
        st.info("Belum ada tugas. Tambahkan tugas baru di sidebar.")
    else:
        st.markdown(f"**{len(hasil_analisis)} tugas aktif** — diurutkan berdasarkan prioritas")
        st.markdown("---")
        for i, tugas in enumerate(hasil_analisis, 1):
            p         = tugas["prioritas"]
            sisa      = tugas["sisa_hari"]
            sisa_text = f"{sisa} hari lagi" if sisa > 0 else ("Hari ini" if sisa == 0 else f"{abs(sisa)} hari lewat")
            col_main, col_aksi = st.columns([5, 1])
            with col_main:
                st.markdown(f"""
                <div class="card card-{p.lower()}">
                    <div style="display:flex;align-items:center;gap:8px;margin-bottom:3px;">
                        <span style="font-size:0.85rem;color:#444466;font-weight:700;">#{i}</span>
                        <span class="task-name">{tugas['nama']}</span>
                        <span class="badge badge-{p.lower()}">{p}</span>
                    </div>
                    <div class="task-meta">
                        {tugas['kategori']} &nbsp;·&nbsp; Deadline: {tugas['deadline']} &nbsp;·&nbsp;
                        {sisa_text} &nbsp;·&nbsp; {tugas['kesulitan']} &nbsp;·&nbsp;
                        Skor: {tugas['skor']} &nbsp;·&nbsp; {tugas['rule_id']}
                    </div>
                    <div class="task-saran">{tugas['saran']}</div>
                    {f'<div class="task-meta" style="margin-top:4px;">{tugas["deskripsi"]}</div>' if tugas.get("deskripsi") else ""}
                </div>
                """, unsafe_allow_html=True)
            with col_aksi:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Selesai", key=f"done_{tugas['id']}"):
                    tandai_selesai(tugas["id"])
                    st.rerun()
                if st.button("Hapus", key=f"del_{tugas['id']}"):
                    hapus_tugas(tugas["id"])
                    st.rerun()

# ══ TAB 2: COUNTDOWN ══════════════════════════════════════
with tab2:
    st.markdown("**Countdown Deadline**")
    if not hasil_analisis:
        st.info("Belum ada tugas aktif.")
    else:
        tugas_cd = [t for t in hasil_analisis if t["sisa_hari"] <= 7] or hasil_analisis[:5]

        tasks_json = ""
        for tugas in tugas_cd[:5]:
            nama_safe = tugas["nama"].replace('"', '').replace("'", "")
            dl = tugas["deadline"]
            dl_js = dl.replace(" ", "T") + ":00" if len(dl) == 16 else dl + "T23:59:59"
            tasks_json += f'{{nama:"{nama_safe}",kategori:"{tugas["kategori"]}",kesulitan:"{tugas["kesulitan"]}",deadline:new Date("{dl_js}")}},'

        html_countdown = f"""
        <div id="cd-wrap"></div>
        <style>
            .cd-box {{
                background:#13131f;
                border:1px solid #222238;
                border-radius:8px;
                padding:0.8rem 1.1rem;
                margin-bottom:0.5rem;
                display:flex;
                justify-content:space-between;
                align-items:center;
            }}
            .cd-name  {{ font-size:0.95rem; color:#aaaacc; font-weight:600; }}
            .cd-sub   {{ font-size:0.78rem; color:#555577; margin-top:3px; }}
            .cd-time  {{ font-size:1.3rem; font-weight:700; color:#8877cc; font-variant-numeric:tabular-nums; }}
            .cd-lewat {{ color:#cc3333; }}
        </style>
        <script>
        const tasks = [{tasks_json}];

        function fmt(deadline) {{
            const diff = deadline - new Date();
            if (diff <= 0) return '<span class="cd-lewat">Lewat deadline</span>';
            const d = Math.floor(diff / 86400000);
            const h = Math.floor((diff % 86400000) / 3600000);
            const m = Math.floor((diff % 3600000) / 60000);
            const s = Math.floor((diff % 60000) / 1000);
            return d + "h " + String(h).padStart(2,"0") + "j " +
                   String(m).padStart(2,"0") + "m " +
                   String(s).padStart(2,"0") + "d";
        }}

        function render() {{
            const el = document.getElementById("cd-wrap");
            if (!el) return;
            let html = "";
            tasks.forEach(t => {{
                const tgl = t.deadline.toISOString().split("T")[0];
                html += `<div class="cd-box">
                    <div>
                        <div class="cd-name">${{t.nama}}</div>
                        <div class="cd-sub">${{t.kategori}} &nbsp;·&nbsp; ${{t.kesulitan}} &nbsp;·&nbsp; ${{tgl}}</div>
                    </div>
                    <div class="cd-time">${{fmt(t.deadline)}}</div>
                </div>`;
            }});
            el.innerHTML = html;
        }}

        render();
        setInterval(render, 1000);
        </script>
        """

        components.html(html_countdown, height=len(tugas_cd[:5]) * 90 + 20)
        st.caption("Menampilkan tugas dengan deadline dalam 7 hari ke depan.")

# ══ TAB 3: VISUALISASI ════════════════════════════════════
with tab3:
    st.markdown("**Visualisasi Data**")
    if not hasil_analisis:
        st.info("Belum ada data.")
    else:
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.markdown("Distribusi Prioritas")
            labels, sizes, colors_pie = [], [], []
            for p, jml in [("KRITIS",jml_kritis),("TINGGI",jml_tinggi),("SEDANG",jml_sedang),("RENDAH",jml_rendah)]:
                if jml > 0:
                    labels.append(p); sizes.append(jml); colors_pie.append(color_map[p])
            fig1, ax1 = plt.subplots(figsize=(4, 3.5))
            fig1.patch.set_facecolor("#0d0d1a")
            ax1.set_facecolor("#0d0d1a")
            _, _, autotexts = ax1.pie(sizes, labels=labels, colors=colors_pie,
                autopct='%1.0f%%', startangle=90, textprops={'color':'#aaaacc','fontsize':9})
            for at in autotexts:
                at.set_color('#0d0d1a'); at.set_fontweight('bold')
            st.pyplot(fig1)

        with col_g2:
            st.markdown("Sisa Hari per Tugas")
            nama_list  = [t["nama"][:20]+"..." if len(t["nama"])>20 else t["nama"] for t in hasil_analisis]
            sisa_list  = [max(t["sisa_hari"],0) for t in hasil_analisis]
            bar_colors = [color_map[t["prioritas"]] for t in hasil_analisis]
            fig2, ax2  = plt.subplots(figsize=(4, 3.5))
            fig2.patch.set_facecolor("#0d0d1a")
            ax2.set_facecolor("#13131f")
            bars = ax2.barh(nama_list, sisa_list, color=bar_colors, edgecolor='none', height=0.5)
            ax2.set_xlabel("Sisa Hari", color="#6666aa", fontsize=8)
            ax2.tick_params(colors="#6666aa", labelsize=8)
            ax2.spines[:].set_color("#222238")
            for bar, val in zip(bars, sisa_list):
                ax2.text(bar.get_width()+0.1, bar.get_y()+bar.get_height()/2,
                    f"{val}h", va='center', color='#aaaacc', fontsize=8)
            st.pyplot(fig2)

        st.markdown("---")
        df_data = [{"Rank":i, "Nama":t["nama"], "Kategori":t["kategori"],
                    "Deadline":t["deadline"], "Sisa Hari":t["sisa_hari"],
                    "Kesulitan":t["kesulitan"], "Prioritas":t["prioritas"], "Skor":t["skor"]}
                   for i,t in enumerate(hasil_analisis,1)]
        st.dataframe(pd.DataFrame(df_data), use_container_width=True, hide_index=True)

# ══ TAB 4: SELESAI ════════════════════════════════════════
with tab4:
    st.markdown("**Tugas Selesai**")
    if not tugas_selesai:
        st.info("Belum ada tugas yang diselesaikan.")
    else:
        st.success(f"Kamu sudah menyelesaikan {len(tugas_selesai)} tugas.")
        for t in reversed(tugas_selesai):
            col_t, col_h = st.columns([5, 1])
            with col_t:
                tgl = t.get("tanggal_selesai", "-")
                st.markdown(f"""
                <div style="background:#0d1a0d;border-left:3px solid #008844;border-radius:6px;
                            padding:0.7rem 1rem;margin-bottom:0.4rem;opacity:0.8;">
                    <span style="color:#008844;font-weight:600;font-size:0.9rem;">{t['nama']}</span>
                    <span style="color:#335533;font-size:0.78rem;margin-left:10px;">
                        {t['kategori']} · {t['deadline']} · {t['kesulitan']} · Selesai: {tgl}
                    </span>
                </div>
                """, unsafe_allow_html=True)
            with col_h:
                if st.button("Hapus", key=f"del_done_{t['id']}"):
                    hapus_tugas(t["id"])
                    st.rerun()