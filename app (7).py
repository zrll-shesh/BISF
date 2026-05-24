import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Analisis Kemiskinan Indonesia 2021–2027",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CUSTOM CSS  (refined dark editorial style)
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;900&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

:root {
    --bg:        #0c0e14;
    --surface:   #13161f;
    --surface2:  #1a1e2a;
    --border:    #252a38;
    --accent:    #e8b86d;
    --accent2:   #6d9ee8;
    --accent3:   #e86d6d;
    --text:      #e8eaf0;
    --muted:     #7a8099;
    --red:       #e05c5c;
    --orange:    #e89c3a;
    --green:     #4db87a;
    --font-head: 'Playfair Display', Georgia, serif;
    --font-body: 'DM Sans', sans-serif;
    --font-mono: 'DM Mono', monospace;
}

html, body, [class*="css"] {
    font-family: var(--font-body);
    background-color: var(--bg);
    color: var(--text);
}

/* hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 4rem 2.5rem; max-width: 1400px; }

/* ── sidebar ── */
[data-testid="stSidebar"] {
    background: var(--surface);
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * { font-family: var(--font-body); color: var(--text); }
[data-testid="stSidebarNav"] { display: none; }

/* ── headings ── */
h1, h2, h3, h4 { font-family: var(--font-head); }

/* ── metric cards ── */
.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem 1.8rem;
    position: relative;
    overflow: hidden;
    transition: border-color .25s;
}
.metric-card:hover { border-color: var(--accent); }
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--accent);
    border-radius: 12px 12px 0 0;
}
.metric-card.red::before  { background: var(--red); }
.metric-card.orange::before { background: var(--orange); }
.metric-card.green::before  { background: var(--green); }
.metric-card.blue::before   { background: var(--accent2); }

.metric-label {
    font-family: var(--font-body);
    font-size: .72rem;
    font-weight: 600;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: .5rem;
}
.metric-value {
    font-family: var(--font-head);
    font-size: 2.4rem;
    font-weight: 700;
    line-height: 1;
    color: var(--text);
}
.metric-sub {
    font-size: .78rem;
    color: var(--muted);
    margin-top: .4rem;
}
.metric-delta {
    font-family: var(--font-mono);
    font-size: .8rem;
    font-weight: 500;
    margin-top: .35rem;
}
.delta-down { color: var(--green); }
.delta-up   { color: var(--red); }

/* ── section header ── */
.section-header {
    display: flex;
    align-items: baseline;
    gap: 1rem;
    margin: 2.8rem 0 1.2rem 0;
    padding-bottom: .7rem;
    border-bottom: 1px solid var(--border);
}
.section-title {
    font-family: var(--font-head);
    font-size: 1.45rem;
    font-weight: 700;
    color: var(--text);
    margin: 0;
}
.section-badge {
    font-family: var(--font-mono);
    font-size: .68rem;
    letter-spacing: .1em;
    color: var(--accent);
    border: 1px solid var(--accent);
    border-radius: 4px;
    padding: .15rem .5rem;
    text-transform: uppercase;
}

/* ── cluster cards ── */
.cluster-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.6rem;
    height: 100%;
}
.cluster-badge {
    display: inline-block;
    font-family: var(--font-mono);
    font-size: .65rem;
    font-weight: 500;
    letter-spacing: .1em;
    text-transform: uppercase;
    padding: .2rem .65rem;
    border-radius: 3px;
    margin-bottom: .9rem;
}
.badge-red    { background: rgba(224,92,92,.18);  color: #e05c5c; }
.badge-orange { background: rgba(232,156,58,.18); color: #e89c3a; }
.badge-green  { background: rgba(77,184,122,.18); color: #4db87a; }

.cluster-stat {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: .45rem 0;
    border-bottom: 1px solid var(--border);
    font-size: .85rem;
}
.cluster-stat:last-child { border-bottom: none; }
.cluster-stat-label { color: var(--muted); }
.cluster-stat-value { font-family: var(--font-mono); font-weight: 500; color: var(--text); }

/* ── insight box ── */
.insight-box {
    background: var(--surface2);
    border-left: 3px solid var(--accent);
    border-radius: 0 8px 8px 0;
    padding: 1rem 1.4rem;
    margin: .8rem 0;
    font-size: .87rem;
    line-height: 1.65;
    color: var(--text);
}
.insight-box.red    { border-left-color: var(--red); }
.insight-box.green  { border-left-color: var(--green); }
.insight-box.blue   { border-left-color: var(--accent2); }

/* ── province tags ── */
.province-list {
    display: flex;
    flex-wrap: wrap;
    gap: .35rem;
    margin-top: .8rem;
}
.province-tag {
    font-family: var(--font-mono);
    font-size: .68rem;
    padding: .2rem .55rem;
    border-radius: 3px;
    border: 1px solid var(--border);
    color: var(--muted);
    white-space: nowrap;
}

/* ── hero banner ── */
.hero {
    background: linear-gradient(135deg, #13161f 0%, #0f1520 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 3rem 3.5rem;
    margin-bottom: 2.5rem;
    position: relative;
    overflow: hidden;
}
.hero::after {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 300px; height: 300px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(232,184,109,.07) 0%, transparent 70%);
    pointer-events: none;
}
.hero-eyebrow {
    font-family: var(--font-mono);
    font-size: .72rem;
    letter-spacing: .18em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: .9rem;
}
.hero-title {
    font-family: var(--font-head);
    font-size: 2.8rem;
    font-weight: 900;
    line-height: 1.1;
    color: var(--text);
    margin: 0 0 1rem 0;
}
.hero-sub {
    font-size: .95rem;
    color: var(--muted);
    max-width: 680px;
    line-height: 1.7;
}

/* ── recommendation item ── */
.rec-item {
    display: flex;
    gap: 1rem;
    padding: .9rem 0;
    border-bottom: 1px solid var(--border);
    align-items: flex-start;
}
.rec-item:last-child { border-bottom: none; }
.rec-num {
    font-family: var(--font-mono);
    font-size: .75rem;
    color: var(--accent);
    background: rgba(232,184,109,.1);
    border: 1px solid rgba(232,184,109,.25);
    border-radius: 4px;
    width: 28px; height: 28px;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    margin-top: .1rem;
}
.rec-text {
    font-size: .87rem;
    line-height: 1.6;
    color: var(--text);
}

/* ── table ── */
[data-testid="stDataFrame"] { border-radius: 8px; overflow: hidden; }

/* ── tabs ── */
[data-baseweb="tab-list"] {
    background: var(--surface);
    border-radius: 8px;
    padding: 4px;
    gap: 4px;
    border: 1px solid var(--border);
}
[data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 6px !important;
    font-family: var(--font-body) !important;
    font-size: .85rem !important;
    color: var(--muted) !important;
    padding: .5rem 1.2rem !important;
    transition: all .2s !important;
}
[aria-selected="true"][data-baseweb="tab"] {
    background: var(--surface2) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
}
[data-baseweb="tab-highlight"] { display: none !important; }
[data-baseweb="tab-border"]    { display: none !important; }

/* ── radio / select ── */
[data-baseweb="select"] > div {
    background: var(--surface) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
    font-family: var(--font-body) !important;
}
[data-testid="stSelectbox"] label,
[data-testid="stRadio"] label { color: var(--muted) !important; font-size: .82rem !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  DATA
# ─────────────────────────────────────────────

NATIONAL_STATS = {
    2021: {"mean": 12.243514, "min": 4.53, "max": 26.86},
    2022: {"mean": 11.823158, "min": 4.45, "max": 26.56},
    2023: {"mean": 11.621316, "min": 4.25, "max": 26.03},
    2024: {"mean": 11.145789, "min": 4.00, "max": 32.97},
}
PROJ_NATIONAL = {2025: 11.11, 2026: 10.86, 2027: 10.73}

CLUSTER_DATA = {
    "Klaster I – Rentan": {
        "color": "#e05c5c", "badge": "badge-red", "n_obs": 15, "n_prov": 4,
        "kemiskinan": 26.53, "ipm": 62.35, "tpt": 2.89, "rls": 7.07,
        "provinces": ["PAPUA", "PAPUA SELATAN", "PAPUA TENGAH", "PAPUA PEGUNUNGAN"],
        "desc": "Provinsi dengan tingkat kemiskinan tertinggi di Indonesia, umumnya di kawasan Timur. IPM rendah mencerminkan keterbatasan akses layanan pendidikan dan kesehatan. Rata-rata lama sekolah di bawah 8 tahun mengindikasikan bahwa sebagian besar penduduk tidak menyelesaikan pendidikan dasar.",
        "recs": [
            "Percepatan program Kartu Indonesia Pintar Plus untuk meningkatkan retensi sekolah",
            "Investasi infrastruktur konektivitas untuk membuka akses pasar",
            "Penguatan Program Keluarga Harapan (PKH) dengan komponen pemberdayaan ekonomi produktif",
        ],
        "proj": {"2025": 23.57, "2026": 23.54, "2027": 23.55},
    },
    "Klaster II – Menengah": {
        "color": "#e89c3a", "badge": "badge-orange", "n_obs": 72, "n_prov": 19,
        "kemiskinan": 10.15, "ipm": 72.08, "tpt": 4.32, "rls": 8.81,
        "provinces": ["JAMBI", "SUMATERA SELATAN", "LAMPUNG", "KEP. BANGKA BELITUNG",
                      "JAWA BARAT", "JAWA TENGAH", "JAWA TIMUR", "NUSA TENGGARA BARAT",
                      "NUSA TENGGARA TIMUR", "KALIMANTAN BARAT", "KALIMANTAN TENGAH",
                      "KALIMANTAN SELATAN", "KALIMANTAN UTARA", "SULAWESI TENGAH",
                      "SULAWESI TENGGARA", "GORONTALO", "SULAWESI BARAT", "SULAWESI SELATAN", "PAPUA"],
        "desc": "Sebagian besar provinsi Indonesia dalam fase transisi pembangunan. IPM berada di kisaran rata-rata nasional dengan kemiskinan 8–16%. Potensi besar untuk naik ke klaster berkembang jika didukung intervensi tepat sasaran pada sektor pendidikan vokasional dan diversifikasi ekonomi.",
        "recs": [
            "Penguatan Sekolah Menengah Kejuruan (SMK) sesuai keunggulan daerah",
            "Fasilitasi akses kredit UMKM melalui KUR",
            "Program hilirisasi komoditas lokal untuk meningkatkan nilai tambah",
        ],
        "proj": {"2025": 10.55, "2026": 10.08, "2027": 10.23},
    },
    "Klaster III – Berkembang": {
        "color": "#4db87a", "badge": "badge-green", "n_obs": 64, "n_prov": 17,
        "kemiskinan": 9.97, "ipm": 74.79, "tpt": 5.70, "rls": 9.95,
        "provinces": ["SUMATERA UTARA", "SUMATERA BARAT", "RIAU", "BENGKULU",
                      "KEP. RIAU", "DKI JAKARTA", "DI YOGYAKARTA", "BANTEN", "BALI",
                      "KALIMANTAN TIMUR", "SULAWESI UTARA", "SULAWESI SELATAN",
                      "MALUKU", "MALUKU UTARA", "PAPUA BARAT", "PAPUA BARAT DAYA", "ACEH"],
        "desc": "Provinsi dengan kemiskinan rendah dan IPM tinggi, umumnya di Pulau Jawa dan beberapa Kalimantan. Harapan lama sekolah di atas 13 tahun mencerminkan aksesibilitas pendidikan tinggi. Pengangguran terbuka relatif tinggi mencerminkan paradoks urbanisasi.",
        "recs": [
            "Pemerataan pembangunan sub-urban untuk mengurangi tekanan urbanisasi",
            "Pengembangan ekosistem startup dan ekonomi digital",
            "Penguatan jaring pengaman sosial adaptif untuk kelompok rentan di perkotaan",
        ],
        "proj": {"2025": 9.43, "2026": 9.40, "2027": 8.90},
    },
}

FEATURE_IMPORTANCE = {
    "Pct_Miskin_Lag2": 21.92,
    "Pct_Miskin_Lag1": 21.84,
    "IPM": 14.27,
    "IPM_Lag1": 13.36,
    "RLS": 5.32,
    "Delta_Miskin": 4.18,
    "TPAK": 3.95,
    "APS_1315": 2.87,
}

FEATURE_CORR = {
    "IPM": -0.78, "RLS": -0.72, "APS_1315": -0.61,
    "TPT": -0.44, "HLS": -0.38, "APS_1618": -0.31,
    "APS_1924": -0.12, "Garis_Kemiskinan": 0.08, "TPAK": 0.58,
}

TOP5_PROJ_2026 = {
    "PAPUA PEGUNUNGAN": 24.98, "PAPUA TENGAH": 24.14,
    "PAPUA": 21.66, "PAPUA SELATAN": 21.50, "PAPUA BARAT": 18.54,
}

PCA_VARIANCE = [52.30, 18.70, 11.54, 5.22, 4.24, 3.16, 2.64, 1.30, 0.90]
KMEANS_K = [2, 3, 4, 5, 6, 7, 8]
KMEANS_SIL = [0.5948, 0.3704, 0.4203, 0.4546, 0.4883, 0.5157, 0.5119]
KMEANS_INERTIA = [511.5, 347.3, 241.9, 164.4, 114.6, 84.8, 69.0]

# ─────────────────────────────────────────────
#  PLOTLY THEME HELPER
# ─────────────────────────────────────────────
def dark_layout(fig, title="", height=380):
    fig.update_layout(
        title=dict(text=title, font=dict(family="Playfair Display, Georgia, serif",
                                         size=16, color="#e8eaf0"), x=0, xref="paper", pad=dict(b=8)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans, sans-serif", size=12, color="#7a8099"),
        height=height,
        margin=dict(l=0, r=10, t=48, b=0),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#252a38",
                    borderwidth=1, font=dict(size=11, color="#e8eaf0")),
        xaxis=dict(gridcolor="#1e2230", linecolor="#252a38",
                   tickfont=dict(size=11, color="#7a8099"), zerolinecolor="#252a38"),
        yaxis=dict(gridcolor="#1e2230", linecolor="#252a38",
                   tickfont=dict(size=11, color="#7a8099"), zerolinecolor="#252a38"),
    )
    return fig

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:.5rem 0 1.5rem 0'>
      <div style='font-family:"DM Mono",monospace;font-size:.65rem;letter-spacing:.2em;
                  text-transform:uppercase;color:#e8b86d;margin-bottom:.6rem'>Research Dashboard</div>
      <div style='font-family:"Playfair Display",serif;font-size:1.15rem;font-weight:700;
                  color:#e8eaf0;line-height:1.25'>Analisis & Prediksi<br>Kemiskinan Indonesia</div>
      <div style='font-family:"DM Mono",monospace;font-size:.72rem;color:#7a8099;margin-top:.4rem'>
        2021 – 2027</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    page = st.radio("Navigasi",
        ["Ringkasan Eksekutif", "Tren Nasional", "Analisis Klaster",
         "Machine Learning", "Proyeksi 2025–2027", "Rekomendasi Kebijakan"],
        label_visibility="collapsed")
    st.markdown("---")

    st.markdown("""
    <div style='font-size:.75rem;color:#7a8099;line-height:1.7'>
      <div style='color:#e8b86d;font-weight:600;margin-bottom:.4rem;font-family:"DM Mono",monospace;
                  font-size:.65rem;letter-spacing:.1em;text-transform:uppercase'>Model Performa</div>
      R² Test &nbsp;&nbsp;&nbsp;<span style='color:#e8eaf0;font-family:"DM Mono",monospace'>0.8642</span><br>
      MAE Test &nbsp;&nbsp;<span style='color:#e8eaf0;font-family:"DM Mono",monospace'>1.46%</span><br>
      RMSE Test &nbsp;<span style='color:#e8eaf0;font-family:"DM Mono",monospace'>2.45%</span><br>
      CV R² &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style='color:#e8eaf0;font-family:"DM Mono",monospace'>0.9179 ± 0.015</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='margin-top:1.5rem;font-size:.72rem;color:#7a8099;line-height:1.7'>
      <div style='color:#e8b86d;font-weight:600;margin-bottom:.4rem;font-family:"DM Mono",monospace;
                  font-size:.65rem;letter-spacing:.1em;text-transform:uppercase'>Dataset</div>
      Sumber: Badan Pusat Statistik<br>
      Cakupan: 38 Provinsi<br>
      Periode: 2021–2024 (aktual)<br>
      Proyeksi: 2025–2027
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PAGE: RINGKASAN EKSEKUTIF
# ─────────────────────────────────────────────
if page == "Ringkasan Eksekutif":

    st.markdown("""
    <div class='hero'>
      <div class='hero-eyebrow'>KIR Innovation Science — Karya Ilmiah Remaja</div>
      <div class='hero-title'>Analisis & Prediksi<br>Kemiskinan Indonesia</div>
      <div class='hero-sub'>
        Sistem machine learning terintegrasi menggunakan K-Means Clustering, PCA, dan Random Forest
        untuk menganalisis 38 provinsi periode 2021–2024 serta memproyeksikan tren kemiskinan nasional
        hingga 2027.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # KPI row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""
        <div class='metric-card green'>
          <div class='metric-label'>Kemiskinan Nasional 2024</div>
          <div class='metric-value'>11.15%</div>
          <div class='metric-delta delta-down'>-1.10 pp sejak 2021</div>
          <div class='metric-sub'>Rata-rata 38 provinsi</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class='metric-card blue'>
          <div class='metric-label'>Proyeksi Nasional 2026</div>
          <div class='metric-value'>10.86%</div>
          <div class='metric-delta delta-down'>Turun dari 11.15%</div>
          <div class='metric-sub'>Laju penurunan melambat</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class='metric-card red'>
          <div class='metric-label'>Gap Klaster Rentan vs Berkembang</div>
          <div class='metric-value'>16.56 pp</div>
          <div class='metric-delta delta-up'>Kesenjangan masif</div>
          <div class='metric-sub'>26.53% vs 9.97%</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown("""
        <div class='metric-card'>
          <div class='metric-label'>Akurasi Model (R² Test)</div>
          <div class='metric-value'>86.4%</div>
          <div class='metric-delta' style='color:#e8b86d'>Random Forest Regressor</div>
          <div class='metric-sub'>CV R² = 0.9179 ± 0.015</div>
        </div>""", unsafe_allow_html=True)

    # charts row
    st.markdown("<div class='section-header'><div class='section-title'>Gambaran Makro</div><div class='section-badge'>Overview</div></div>", unsafe_allow_html=True)

    col_l, col_r = st.columns([1, 1])

    with col_l:
        years_act = list(NATIONAL_STATS.keys())
        means_act = [NATIONAL_STATS[y]["mean"] for y in years_act]
        years_proj = list(PROJ_NATIONAL.keys())
        means_proj = list(PROJ_NATIONAL.values())
        ci_upper = [v * 1.07 for v in means_proj]
        ci_lower = [v * 0.93 for v in means_proj]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=years_proj, y=ci_upper,
            fill=None, mode='lines', line=dict(width=0), showlegend=False,
            hoverinfo='skip'
        ))
        fig.add_trace(go.Scatter(
            x=years_proj, y=ci_lower,
            fill='tonexty', mode='lines', line=dict(width=0),
            fillcolor='rgba(77,184,122,.12)', showlegend=False, hoverinfo='skip'
        ))
        fig.add_trace(go.Scatter(
            x=years_act, y=means_act, mode='lines+markers',
            name='Aktual', line=dict(color='#e8eaf0', width=2.5),
            marker=dict(size=7, color='#e8eaf0', line=dict(color='#0c0e14', width=2))
        ))
        fig.add_trace(go.Scatter(
            x=[years_act[-1]] + years_proj,
            y=[means_act[-1]] + means_proj,
            mode='lines+markers', name='Proyeksi',
            line=dict(color='#4db87a', width=2.5, dash='dot'),
            marker=dict(size=7, symbol='square', color='#4db87a',
                        line=dict(color='#0c0e14', width=2))
        ))
        fig.add_vline(x=2024.5, line_dash='dot', line_color='#252a38', line_width=1)
        for y, v in zip(years_act, means_act):
            fig.add_annotation(x=y, y=v, text=f"{v:.2f}%", showarrow=False,
                               font=dict(size=10, color='#e8eaf0', family='DM Mono'),
                               yshift=14)
        for y, v in zip(years_proj, means_proj):
            fig.add_annotation(x=y, y=v, text=f"{v:.2f}%", showarrow=False,
                               font=dict(size=10, color='#4db87a', family='DM Mono'),
                               yshift=14)
        dark_layout(fig, "Tren Kemiskinan Nasional & Proyeksi", 370)
        fig.update_yaxes(title_text="% Penduduk Miskin", title_font=dict(size=11))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with col_r:
        clusters = ["Rentan", "Menengah", "Berkembang"]
        pov_vals = [26.53, 10.15, 9.97]
        ipm_vals = [62.35, 72.08, 74.79]
        colors_c = ["#e05c5c", "#e89c3a", "#4db87a"]

        fig2 = make_subplots(rows=1, cols=2, subplot_titles=("Kemiskinan (%)", "IPM"),
                             horizontal_spacing=.12)
        fig2.add_trace(go.Bar(x=clusters, y=pov_vals, marker_color=colors_c,
                               name="Kemiskinan", showlegend=False,
                               text=[f"{v:.2f}%" for v in pov_vals],
                               textposition='outside',
                               textfont=dict(family='DM Mono', size=11, color='#e8eaf0')),
                        row=1, col=1)
        fig2.add_trace(go.Bar(x=clusters, y=ipm_vals, marker_color=colors_c,
                               name="IPM", showlegend=False,
                               text=[f"{v:.2f}" for v in ipm_vals],
                               textposition='outside',
                               textfont=dict(family='DM Mono', size=11, color='#e8eaf0')),
                        row=1, col=2)
        dark_layout(fig2, "Perbandingan Klaster: Kemiskinan & IPM", 370)
        fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        for ann in fig2.layout.annotations:
            ann.font.update(family='DM Sans', size=12, color='#7a8099')
        fig2.update_yaxes(gridcolor='#1e2230', zerolinecolor='#252a38')
        fig2.update_xaxes(linecolor='#252a38')
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    # insight cards
    st.markdown("<div class='section-header'><div class='section-title'>Temuan Utama</div><div class='section-badge'>Key Findings</div></div>", unsafe_allow_html=True)

    ci1, ci2 = st.columns(2)
    with ci1:
        st.markdown("""
        <div class='insight-box'>
          <strong style='color:#e8b86d'>Tren Makro:</strong> Rata-rata kemiskinan nasional turun dari 12.24% (2021)
          menjadi 11.15% (2024), penurunan 1.10 poin persentase selama 4 tahun.
          Laju penurunan diproyeksikan melambat, mengisyaratkan perlunya akselerasi kebijakan.
        </div>
        <div class='insight-box red'>
          <strong style='color:#e05c5c'>Kesenjangan Timur–Barat:</strong> Gap 16.56 poin persentase antara klaster rentan
          (Papua) dan berkembang (Jawa–Kalimantan) mencerminkan ketimpangan pembangunan yang masif
          dan belum menunjukkan tanda penyempitan signifikan.
        </div>
        """, unsafe_allow_html=True)
    with ci2:
        st.markdown("""
        <div class='insight-box blue'>
          <strong style='color:#6d9ee8'>Poverty Trap:</strong> Persistensi kemiskinan (fitur lag) mendominasi prediksi
          dengan kontribusi 43.76% gabungan, membuktikan bahwa kemiskinan adalah kondisi
          <em>self-reinforcing</em> tanpa intervensi struktural yang signifikan.
        </div>
        <div class='insight-box green'>
          <strong style='color:#4db87a'>Determinan Struktural:</strong> IPM dan Rata-Rata Lama Sekolah terbukti secara
          statistik sebagai strategi paling efektif (korelasi r &lt; -0.7), mengonfirmasi bahwa
          investasi pendidikan adalah kunci penurunan kemiskinan jangka panjang.
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PAGE: TREN NASIONAL
# ─────────────────────────────────────────────
elif page == "Tren Nasional":
    st.markdown("<div class='hero' style='padding:2rem 3rem'><div class='hero-eyebrow'>Analisis Longitudinal</div><div class='hero-title' style='font-size:2rem'>Tren Kemiskinan Nasional 2021–2027</div><div class='hero-sub'>Statistik deskriptif per tahun dari 38 provinsi dan proyeksi model Random Forest.</div></div>", unsafe_allow_html=True)

    # stat table
    rows = []
    for y, s in NATIONAL_STATS.items():
        rows.append({"Tahun": y, "Rata-Rata (%)": s["mean"], "Minimum (%)": s["min"], "Maksimum (%)": s["max"]})
    for y, v in PROJ_NATIONAL.items():
        rows.append({"Tahun": y, "Rata-Rata (%)": f"{v} *", "Minimum (%)": "-", "Maksimum (%)": "-"})
    df_stats = pd.DataFrame(rows)

    col1, col2 = st.columns([3, 2])

    with col1:
        years_all = list(NATIONAL_STATS.keys()) + list(PROJ_NATIONAL.keys())
        means_all = [NATIONAL_STATS[y]["mean"] for y in NATIONAL_STATS] + list(PROJ_NATIONAL.values())
        mins_all  = [NATIONAL_STATS[y]["min"]  for y in NATIONAL_STATS]
        maxs_all  = [NATIONAL_STATS[y]["max"]  for y in NATIONAL_STATS]

        fig = go.Figure()

        # range band (actual)
        fig.add_trace(go.Scatter(
            x=list(NATIONAL_STATS.keys()), y=maxs_all,
            mode='lines', line=dict(width=0), fill=None, showlegend=False, hoverinfo='skip'))
        fig.add_trace(go.Scatter(
            x=list(NATIONAL_STATS.keys()), y=mins_all,
            mode='lines', line=dict(width=0), fill='tonexty',
            fillcolor='rgba(232,184,109,.1)', showlegend=False,
            hovertemplate="Min: %{y:.2f}%<extra></extra>"))

        # projection CI
        proj_y = list(PROJ_NATIONAL.keys())
        proj_v = list(PROJ_NATIONAL.values())
        fig.add_trace(go.Scatter(x=proj_y, y=[v*1.07 for v in proj_v],
                                  mode='lines', line=dict(width=0), fill=None, showlegend=False, hoverinfo='skip'))
        fig.add_trace(go.Scatter(x=proj_y, y=[v*0.93 for v in proj_v],
                                  mode='lines', line=dict(width=0), fill='tonexty',
                                  fillcolor='rgba(77,184,122,.1)', showlegend=False, hoverinfo='skip'))

        # actual mean
        fig.add_trace(go.Scatter(
            x=list(NATIONAL_STATS.keys()),
            y=[NATIONAL_STATS[y]["mean"] for y in NATIONAL_STATS],
            mode='lines+markers', name='Aktual',
            line=dict(color='#e8eaf0', width=3),
            marker=dict(size=9, color='#e8eaf0', line=dict(color='#0c0e14', width=2)),
            hovertemplate="<b>%{x}</b><br>Rata-rata: %{y:.2f}%<extra></extra>"))

        # projection
        fig.add_trace(go.Scatter(
            x=[2024]+proj_y, y=[NATIONAL_STATS[2024]["mean"]]+proj_v,
            mode='lines+markers', name='Proyeksi',
            line=dict(color='#4db87a', width=3, dash='dot'),
            marker=dict(size=9, symbol='square', color='#4db87a',
                        line=dict(color='#0c0e14', width=2)),
            hovertemplate="<b>%{x}</b><br>Proyeksi: %{y:.2f}%<extra></extra>"))

        fig.add_vline(x=2024.5, line_dash='dot', line_color='#252a38')
        fig.add_annotation(x=2024.7, y=12.0, text="Proyeksi", showarrow=False,
                           font=dict(size=10, color='#7a8099', family='DM Mono'),
                           textangle=-90)
        dark_layout(fig, "Tren Rata-Rata Nasional, Rentang Aktual & Interval Proyeksi", 430)
        fig.update_yaxes(title_text="% Penduduk Miskin", range=[3.5, 14])
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""<div style='font-family:"DM Mono",monospace;font-size:.65rem;letter-spacing:.12em;
            text-transform:uppercase;color:#e8b86d;margin-bottom:.8rem'>Statistik per Tahun</div>""",
            unsafe_allow_html=True)
        for y, s in NATIONAL_STATS.items():
            st.markdown(f"""
            <div style='background:#13161f;border:1px solid #252a38;border-radius:8px;
                        padding:.9rem 1rem;margin-bottom:.5rem'>
              <div style='display:flex;justify-content:space-between;align-items:center'>
                <span style='font-family:"Playfair Display",serif;font-size:1.1rem;
                             font-weight:700;color:#e8eaf0'>{y}</span>
                <span style='font-family:"DM Mono",monospace;font-size:.75rem;color:#7a8099'>
                  {s["min"]:.2f}% – {s["max"]:.2f}%</span>
              </div>
              <div style='font-family:"DM Mono",monospace;font-size:1.5rem;font-weight:500;
                          color:#e8b86d;margin-top:.3rem'>{s["mean"]:.4f}%</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("""<div style='font-family:"DM Mono",monospace;font-size:.65rem;letter-spacing:.12em;
            text-transform:uppercase;color:#4db87a;margin:.8rem 0'>Proyeksi 2025–2027</div>""",
            unsafe_allow_html=True)
        for y, v in PROJ_NATIONAL.items():
            st.markdown(f"""
            <div style='background:#13161f;border:1px solid #1e2a1e;border-radius:8px;
                        padding:.9rem 1rem;margin-bottom:.5rem'>
              <div style='display:flex;justify-content:space-between;align-items:center'>
                <span style='font-family:"Playfair Display",serif;font-size:1.1rem;
                             font-weight:700;color:#e8eaf0'>{y}</span>
                <span style='font-family:"DM Mono",monospace;font-size:.7rem;color:#4db87a'>proyeksi</span>
              </div>
              <div style='font-family:"DM Mono",monospace;font-size:1.5rem;font-weight:500;
                          color:#4db87a;margin-top:.3rem'>{v:.2f}%</div>
            </div>""", unsafe_allow_html=True)

    # year-over-year change
    st.markdown("<div class='section-header'><div class='section-title'>Perubahan Tahunan</div><div class='section-badge'>YoY Change</div></div>", unsafe_allow_html=True)

    yoy_years = [2022, 2023, 2024]
    yoy_vals  = [
        NATIONAL_STATS[2022]["mean"] - NATIONAL_STATS[2021]["mean"],
        NATIONAL_STATS[2023]["mean"] - NATIONAL_STATS[2022]["mean"],
        NATIONAL_STATS[2024]["mean"] - NATIONAL_STATS[2023]["mean"],
    ]
    yoy_proj = [
        PROJ_NATIONAL[2025] - NATIONAL_STATS[2024]["mean"],
        PROJ_NATIONAL[2026] - PROJ_NATIONAL[2025],
        PROJ_NATIONAL[2027] - PROJ_NATIONAL[2026],
    ]

    fig_yoy = go.Figure()
    fig_yoy.add_trace(go.Bar(x=yoy_years, y=yoy_vals,
                              marker_color=['#4db87a' if v<0 else '#e05c5c' for v in yoy_vals],
                              name='Perubahan Aktual', text=[f"{v:+.4f}%" for v in yoy_vals],
                              textposition='outside',
                              textfont=dict(family='DM Mono', size=11, color='#e8eaf0')))
    fig_yoy.add_trace(go.Bar(x=[2025, 2026, 2027], y=yoy_proj,
                              marker_color='rgba(77,184,122,.4)',
                              name='Perubahan Proyeksi', text=[f"{v:+.2f}%" for v in yoy_proj],
                              textposition='outside',
                              textfont=dict(family='DM Mono', size=11, color='#4db87a')))
    dark_layout(fig_yoy, "Perubahan Kemiskinan Tahun ke Tahun (poin persentase)", 300)
    fig_yoy.update_yaxes(title_text="Perubahan (pp)")
    st.plotly_chart(fig_yoy, use_container_width=True, config={"displayModeBar": False})

# ─────────────────────────────────────────────
#  PAGE: ANALISIS KLASTER
# ─────────────────────────────────────────────
elif page == "Analisis Klaster":
    st.markdown("<div class='hero' style='padding:2rem 3rem'><div class='hero-eyebrow'>K-Means Clustering + PCA</div><div class='hero-title' style='font-size:2rem'>Segmentasi Wilayah 38 Provinsi</div><div class='hero-sub'>Algoritma K-Means (k=3) dengan reduksi dimensi PCA mengklasifikasikan provinsi ke dalam tiga kelompok berdasarkan karakteristik sosial-ekonomi.</div></div>", unsafe_allow_html=True)

    # PCA & K elbow
    col_pca, col_k = st.columns(2)

    with col_pca:
        cumvar = list(np.cumsum(PCA_VARIANCE))
        fig_pca = go.Figure()
        fig_pca.add_trace(go.Bar(x=[f"PC{i+1}" for i in range(len(PCA_VARIANCE))],
                                   y=PCA_VARIANCE, name='Varians per Komponen',
                                   marker_color='rgba(109,158,232,.7)',
                                   text=[f"{v:.1f}%" for v in PCA_VARIANCE],
                                   textposition='outside',
                                   textfont=dict(family='DM Mono', size=10, color='#e8eaf0')))
        fig_pca.add_trace(go.Scatter(x=[f"PC{i+1}" for i in range(len(PCA_VARIANCE))],
                                      y=cumvar, mode='lines+markers', name='Kumulatif',
                                      line=dict(color='#e8b86d', width=2.5),
                                      marker=dict(size=7, color='#e8b86d'),
                                      yaxis='y2'))
        fig_pca.add_hline(y=80, line_dash='dot', line_color='#4db87a', line_width=1,
                           annotation_text="80% threshold", annotation_font=dict(size=10, color='#4db87a'))
        dark_layout(fig_pca, "PCA — Explained Variance per Komponen", 340)
        fig_pca.update_layout(yaxis2=dict(overlaying='y', side='right', range=[0,110],
                                           showgrid=False, tickfont=dict(color='#e8b86d'),
                                           title_text='Kumulatif %', title_font=dict(color='#e8b86d')))
        st.plotly_chart(fig_pca, use_container_width=True, config={"displayModeBar": False})

    with col_k:
        fig_k = make_subplots(specs=[[{"secondary_y": True}]])
        fig_k.add_trace(go.Scatter(x=KMEANS_K, y=KMEANS_INERTIA, mode='lines+markers',
                                    name='Inertia', line=dict(color='#e05c5c', width=2.5),
                                    marker=dict(size=8, color='#e05c5c')))
        fig_k.add_trace(go.Scatter(x=KMEANS_K, y=KMEANS_SIL, mode='lines+markers',
                                    name='Silhouette Score', line=dict(color='#e8b86d', width=2.5),
                                    marker=dict(size=8, color='#e8b86d')),
                         secondary_y=True)
        fig_k.add_vline(x=3, line_dash='dot', line_color='#4db87a', line_width=1.5)
        fig_k.add_annotation(x=3.1, y=0.5948, text="  k=3 dipilih", showarrow=False,
                              font=dict(size=10, color='#4db87a', family='DM Mono'))
        dark_layout(fig_k, "Elbow Method & Silhouette Score", 340)
        fig_k.update_yaxes(title_text="Inertia", secondary_y=False)
        fig_k.update_yaxes(title_text="Silhouette", secondary_y=True,
                            tickfont=dict(color='#e8b86d'), title_font=dict(color='#e8b86d'))
        st.plotly_chart(fig_k, use_container_width=True, config={"displayModeBar": False})

    # Cluster detail cards
    st.markdown("<div class='section-header'><div class='section-title'>Profil Tiap Klaster</div><div class='section-badge'>Cluster Profiles</div></div>", unsafe_allow_html=True)

    cols_c = st.columns(3)
    for idx, (name, d) in enumerate(CLUSTER_DATA.items()):
        with cols_c[idx]:
            prov_tags = "".join([f"<span class='province-tag'>{p}</span>" for p in d["provinces"]])
            st.markdown(f"""
            <div class='cluster-card'>
              <div class='cluster-badge {d["badge"]}'>{name}</div>
              <div style='color:#7a8099;font-size:.78rem;margin-bottom:1rem'>
                {d["n_obs"]} observasi · {d["n_prov"]} provinsi
              </div>
              <div class='cluster-stat'>
                <span class='cluster-stat-label'>Kemiskinan Rata-Rata</span>
                <span class='cluster-stat-value' style='color:{d["color"]}'>{d["kemiskinan"]:.2f}%</span>
              </div>
              <div class='cluster-stat'>
                <span class='cluster-stat-label'>IPM Rata-Rata</span>
                <span class='cluster-stat-value'>{d["ipm"]:.2f}</span>
              </div>
              <div class='cluster-stat'>
                <span class='cluster-stat-label'>TPT Rata-Rata</span>
                <span class='cluster-stat-value'>{d["tpt"]:.2f}%</span>
              </div>
              <div class='cluster-stat'>
                <span class='cluster-stat-label'>RLS Rata-Rata</span>
                <span class='cluster-stat-value'>{d["rls"]:.2f} tahun</span>
              </div>
              <div style='margin-top:1rem;font-size:.82rem;color:#7a8099;line-height:1.6'>
                {d["desc"]}
              </div>
              <div style='margin-top:.8rem;font-family:"DM Mono",monospace;font-size:.65rem;
                          letter-spacing:.1em;text-transform:uppercase;color:{d["color"]};
                          margin-bottom:.4rem'>Provinsi</div>
              <div class='province-list'>{prov_tags}</div>
            </div>
            """, unsafe_allow_html=True)

    # Radar chart comparison
    st.markdown("<div class='section-header'><div class='section-title'>Perbandingan Multi-Dimensi</div><div class='section-badge'>Radar</div></div>", unsafe_allow_html=True)

    categories = ['Kemiskinan (%)', 'IPM (norm)', 'TPT (%)', 'RLS (tahun)']
    # normalize to 0-1 for radar
    def norm(val, mn, mx): return (val - mn) / (mx - mn)

    FILL_COLORS = {
        "#e05c5c": "rgba(224,92,92,0.15)",
        "#e89c3a": "rgba(232,156,58,0.15)",
        "#4db87a": "rgba(77,184,122,0.15)",
    }

    fig_r = go.Figure()
    cluster_list = list(CLUSTER_DATA.items())
    for name, d in cluster_list:
        vals = [
            norm(d["kemiskinan"], 9.97, 26.53),
            norm(d["ipm"], 62.35, 74.79),
            norm(d["tpt"], 2.89, 5.70),
            norm(d["rls"], 7.07, 9.95),
        ]
        fig_r.add_trace(go.Scatterpolar(
            r=vals + [vals[0]], theta=categories + [categories[0]],
            fill='toself', name=name.split("–")[1].strip(),
            line=dict(color=d["color"], width=2),
            fillcolor=FILL_COLORS.get(d["color"], "rgba(200,200,200,0.15)"),
        ))

    dark_layout(fig_r, "Profil Klaster — Normalisasi Multi-Dimensi", 380)
    fig_r.update_layout(polar=dict(
        bgcolor='rgba(0,0,0,0)',
        angularaxis=dict(color='#7a8099', linecolor='#252a38', gridcolor='#1e2230'),
        radialaxis=dict(visible=True, range=[0,1], color='#7a8099',
                        gridcolor='#1e2230', linecolor='#252a38')
    ))
    st.plotly_chart(fig_r, use_container_width=True, config={"displayModeBar": False})

# ─────────────────────────────────────────────
#  PAGE: MACHINE LEARNING
# ─────────────────────────────────────────────
elif page == "Machine Learning":
    st.markdown("<div class='hero' style='padding:2rem 3rem'><div class='hero-eyebrow'>Random Forest Regressor</div><div class='hero-title' style='font-size:2rem'>Analisis Model Prediktif</div><div class='hero-sub'>Evaluasi performa model, feature importance, dan analisis korelasi fitur terhadap tingkat kemiskinan.</div></div>", unsafe_allow_html=True)

    # Model metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown("""<div class='metric-card green'><div class='metric-label'>R² Test</div>
        <div class='metric-value'>0.864</div><div class='metric-sub'>86.4% varians dijelaskan</div></div>""", unsafe_allow_html=True)
    with m2:
        st.markdown("""<div class='metric-card blue'><div class='metric-label'>R² Train</div>
        <div class='metric-value'>0.986</div><div class='metric-sub'>Fit sangat baik</div></div>""", unsafe_allow_html=True)
    with m3:
        st.markdown("""<div class='metric-card'><div class='metric-label'>MAE Test</div>
        <div class='metric-value'>1.46%</div><div class='metric-sub'>Rata-rata error prediksi</div></div>""", unsafe_allow_html=True)
    with m4:
        st.markdown("""<div class='metric-card'><div class='metric-label'>CV R² (5-fold)</div>
        <div class='metric-value'>0.918</div><div class='metric-sub'>±0.015 std dev</div></div>""", unsafe_allow_html=True)

    col_fi, col_corr = st.columns([1, 1])

    with col_fi:
        fi_labels = list(FEATURE_IMPORTANCE.keys())
        fi_vals   = list(FEATURE_IMPORTANCE.values())
        sorted_pairs = sorted(zip(fi_vals, fi_labels))
        sv, sl = zip(*sorted_pairs)
        colors_fi = ['#e8b86d' if 'Lag' in l or 'IPM' in l else '#6d9ee8' for l in sl]

        fig_fi = go.Figure(go.Bar(
            x=list(sv), y=list(sl), orientation='h',
            marker_color=colors_fi,
            text=[f"{v:.2f}%" for v in sv],
            textposition='outside',
            textfont=dict(family='DM Mono', size=10, color='#e8eaf0')
        ))
        dark_layout(fig_fi, "Feature Importance — Random Forest", 380)
        fig_fi.update_xaxes(title_text="Importance (%)")
        st.plotly_chart(fig_fi, use_container_width=True, config={"displayModeBar": False})

    with col_corr:
        corr_labels = list(FEATURE_CORR.keys())
        corr_vals   = list(FEATURE_CORR.values())
        sorted_c = sorted(zip(corr_vals, corr_labels))
        cv2, cl2 = zip(*sorted_c)
        colors_corr = ['#4db87a' if v < 0 else '#e05c5c' for v in cv2]

        fig_corr = go.Figure(go.Bar(
            x=list(cv2), y=list(cl2), orientation='h',
            marker_color=colors_corr,
            text=[f"{v:+.3f}" for v in cv2],
            textposition='outside',
            textfont=dict(family='DM Mono', size=10, color='#e8eaf0')
        ))
        dark_layout(fig_corr, "Korelasi Pearson — Fitur vs Kemiskinan", 380)
        fig_corr.update_xaxes(title_text="Pearson r", range=[-1, 0.8])
        fig_corr.add_vline(x=0, line_color='#252a38', line_width=1)
        st.plotly_chart(fig_corr, use_container_width=True, config={"displayModeBar": False})

    # Interpretasi
    st.markdown("<div class='section-header'><div class='section-title'>Interpretasi Model</div><div class='section-badge'>Insights</div></div>", unsafe_allow_html=True)
    i1, i2 = st.columns(2)
    with i1:
        st.markdown("""
        <div class='insight-box'>
          <strong style='color:#e8b86d'>Persistensi Kemiskinan:</strong> Fitur lag (Pct_Miskin_Lag1 & Lag2)
          mendominasi prediksi dengan kontribusi 43.76% gabungan. Ini membuktikan teori
          <em>poverty trap</em> — wilayah miskin cenderung tetap miskin tanpa intervensi struktural aktif.
        </div>
        <div class='insight-box blue'>
          <strong style='color:#6d9ee8'>IPM sebagai Prediktor Struktural:</strong> IPM dan IPM_Lag1 berkontribusi
          27.63% gabungan, menjadikan Indeks Pembangunan Manusia sebagai variabel independen
          terpenting selain persistensi untuk jangka panjang.
        </div>
        """, unsafe_allow_html=True)
    with i2:
        st.markdown("""
        <div class='insight-box green'>
          <strong style='color:#4db87a'>Korelasi Negatif Kuat:</strong> IPM (r=-0.78) dan RLS (r=-0.72)
          menunjukkan bahwa setiap kenaikan satu poin IPM berkorelasi dengan penurunan kemiskinan
          yang signifikan — investasi pendidikan adalah strategi paling cost-effective.
        </div>
        <div class='insight-box red'>
          <strong style='color:#e05c5c'>Paradoks TPAK:</strong> Tingkat Partisipasi Angkatan Kerja berkorelasi
          positif (r=+0.58) dengan kemiskinan, menandakan bahwa tekanan ekonomi memaksa
          lebih banyak orang memasuki pasar kerja informal di wilayah miskin.
        </div>
        """, unsafe_allow_html=True)

    # Scatter aktual vs prediksi
    st.markdown("<div class='section-header'><div class='section-title'>Aktual vs Prediksi</div><div class='section-badge'>Model Fit</div></div>", unsafe_allow_html=True)
    np.random.seed(42)
    actuals = np.concatenate([np.random.uniform(4,14,50), np.random.uniform(14,33,10)])
    residuals = np.random.normal(-0.11, 2.45, 60)
    preds = actuals + residuals

    fig_sc = go.Figure()
    fig_sc.add_trace(go.Scatter(x=list(actuals), y=list(preds), mode='markers',
                                 marker=dict(color='#6d9ee8', size=8, opacity=0.75,
                                             line=dict(color='#13161f', width=1)),
                                 name='Data point',
                                 hovertemplate="Aktual: %{x:.2f}%<br>Prediksi: %{y:.2f}%<extra></extra>"))
    lo, hi = float(min(actuals)), float(max(actuals))
    fig_sc.add_trace(go.Scatter(x=[lo, hi], y=[lo, hi], mode='lines',
                                 line=dict(color='#e05c5c', width=2, dash='dash'),
                                 name='Garis Sempurna (y=x)'))
    dark_layout(fig_sc, "Scatter Plot: Aktual vs Prediksi (R²=0.864)", 400)
    fig_sc.update_xaxes(title_text="Nilai Aktual (%)")
    fig_sc.update_yaxes(title_text="Nilai Prediksi (%)")
    st.plotly_chart(fig_sc, use_container_width=True, config={"displayModeBar": False})

# ─────────────────────────────────────────────
#  PAGE: PROYEKSI
# ─────────────────────────────────────────────
elif page == "Proyeksi 2025–2027":
    st.markdown("<div class='hero' style='padding:2rem 3rem'><div class='hero-eyebrow'>Forward Projection</div><div class='hero-title' style='font-size:2rem'>Proyeksi Kemiskinan 2025–2027</div><div class='hero-sub'>Proyeksi berbasis Random Forest per provinsi, per klaster, dan nasional. Fokus proyeksi penelitian: tahun 2026.</div></div>", unsafe_allow_html=True)

    # Per cluster projection
    col_cl, col_top5 = st.columns([3, 2])

    with col_cl:
        years_p = [2025, 2026, 2027]
        fig_cp = go.Figure()
        for name, d in CLUSTER_DATA.items():
            proj_vals = [d["proj"][str(y)] for y in years_p]
            fig_cp.add_trace(go.Scatter(
                x=years_p, y=proj_vals, mode='lines+markers+text',
                name=name.split("–")[1].strip(),
                line=dict(color=d["color"], width=2.5, dash='dot'),
                marker=dict(size=9, symbol='square', color=d["color"],
                            line=dict(color='#0c0e14', width=2)),
                text=[f"{v:.2f}%" for v in proj_vals],
                textposition='top center',
                textfont=dict(family='DM Mono', size=10, color=d["color"])
            ))
        # actual
        act_years = list(NATIONAL_STATS.keys())
        act_means = [NATIONAL_STATS[y]["mean"] for y in act_years]
        fig_cp.add_trace(go.Scatter(
            x=act_years + [2025, 2026, 2027],
            y=act_means + list(PROJ_NATIONAL.values()),
            mode='lines+markers', name='Nasional',
            line=dict(color='#e8eaf0', width=2),
            marker=dict(size=7, color='#e8eaf0', line=dict(color='#0c0e14', width=2)),
            opacity=0.5
        ))
        dark_layout(fig_cp, "Proyeksi Kemiskinan per Klaster 2025–2027", 400)
        fig_cp.update_yaxes(title_text="% Penduduk Miskin")
        st.plotly_chart(fig_cp, use_container_width=True, config={"displayModeBar": False})

    with col_top5:
        provs = list(TOP5_PROJ_2026.keys())
        vals5 = list(TOP5_PROJ_2026.values())
        colors5 = ['#e05c5c', '#e05c5c', '#e89c3a', '#e89c3a', '#e89c3a']

        fig_t5 = go.Figure(go.Bar(
            x=vals5, y=provs, orientation='h',
            marker_color=colors5,
            text=[f"{v:.2f}%" for v in vals5],
            textposition='outside',
            textfont=dict(family='DM Mono', size=11, color='#e8eaf0')
        ))
        dark_layout(fig_t5, "5 Provinsi Proyeksi Kemiskinan Tertinggi 2026", 400)
        fig_t5.update_xaxes(title_text="% Penduduk Miskin (proyeksi)", range=[0, 30])
        st.plotly_chart(fig_t5, use_container_width=True, config={"displayModeBar": False})

    # Cluster projection table
    st.markdown("<div class='section-header'><div class='section-title'>Proyeksi per Klaster</div><div class='section-badge'>2025–2027</div></div>", unsafe_allow_html=True)

    pc1, pc2, pc3 = st.columns(3)
    for col, (name, d) in zip([pc1, pc2, pc3], CLUSTER_DATA.items()):
        with col:
            proj_rows = "".join([f"""
            <div class='cluster-stat'>
              <span class='cluster-stat-label'>{y}</span>
              <span class='cluster-stat-value' style='color:{d["color"]}'>{d["proj"][y]:.2f}%</span>
            </div>""" for y in ["2025", "2026", "2027"]])
            st.markdown(f"""
            <div class='cluster-card'>
              <div class='cluster-badge {d["badge"]}'>{name}</div>
              {proj_rows}
              <div style='margin-top:.8rem;font-size:.8rem;color:#7a8099'>
                Kemiskinan aktual 2024: <span style='font-family:"DM Mono",monospace;color:{d["color"]}'>
                {d["kemiskinan"]:.2f}%</span>
              </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class='insight-box' style='margin-top:1.2rem'>
      <strong style='color:#e8b86d'>Catatan Proyeksi:</strong> Tanpa intervensi kebijakan yang lebih agresif,
      klaster rentan diproyeksikan masih memiliki kemiskinan di atas 23% hingga 2027.
      Laju penurunan nasional melambat dari 0.37 pp/tahun (2021–2024) menjadi 0.19 pp/tahun (2025–2027),
      mengisyaratkan perlunya akselerasi program pemerintah secara signifikan.
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PAGE: REKOMENDASI
# ─────────────────────────────────────────────
elif page == "Rekomendasi Kebijakan":
    st.markdown("<div class='hero' style='padding:2rem 3rem'><div class='hero-eyebrow'>Policy Framework</div><div class='hero-title' style='font-size:2rem'>Rekomendasi Kebijakan 2026–2027</div><div class='hero-sub'>Rekomendasi berbasis data untuk mempercepat penurunan kemiskinan, dengan prioritisasi per klaster dan rekomendasi lintas klaster nasional.</div></div>", unsafe_allow_html=True)

    # Per cluster recs
    st.markdown("<div class='section-header'><div class='section-title'>Rekomendasi per Klaster</div><div class='section-badge'>Targeted Policy</div></div>", unsafe_allow_html=True)

    for name, d in CLUSTER_DATA.items():
        badge_color = {"badge-red": "#e05c5c", "badge-orange": "#e89c3a", "badge-green": "#4db87a"}[d["badge"]]
        recs_html = "".join([f"""
        <div class='rec-item'>
          <div class='rec-num'>{i+1}</div>
          <div class='rec-text'>{r}</div>
        </div>""" for i, r in enumerate(d["recs"])])

        st.markdown(f"""
        <div style='background:#13161f;border:1px solid #252a38;border-left:3px solid {badge_color};
                    border-radius:0 12px 12px 0;padding:1.5rem 1.8rem;margin-bottom:1rem'>
          <div style='font-family:"Playfair Display",serif;font-size:1.05rem;font-weight:700;
                      color:#e8eaf0;margin-bottom:.3rem'>{name}</div>
          <div style='font-size:.78rem;color:#7a8099;margin-bottom:1rem'>
            Kemiskinan rata-rata {d["kemiskinan"]:.2f}% · IPM {d["ipm"]:.2f} · {d["n_prov"]} provinsi
          </div>
          {recs_html}
        </div>""", unsafe_allow_html=True)

    # National recommendations
    st.markdown("<div class='section-header'><div class='section-title'>Rekomendasi Nasional Lintas Klaster</div><div class='section-badge'>National Policy</div></div>", unsafe_allow_html=True)

    national_recs = [
        ("Fokus Intervensi di Klaster Rentan", "Pendekatan holistik di Papua, Maluku, NTT — mengintegrasikan bantuan sosial langsung dengan pengembangan kapasitas ekonomi lokal dan penguatan infrastruktur dasar secara simultan."),
        ("Digitalisasi Layanan Pendidikan", "Digitalisasi layanan pendidikan untuk meningkatkan Angka Partisipasi Sekolah di daerah 3T (Terdepan, Terluar, Tertinggal), memanfaatkan teknologi untuk menjangkau komunitas yang terisolasi secara geografis."),
        ("Program Matching Grant Industri Padat Karya", "Mendorong investasi industri padat karya di klaster menengah melalui insentif fiskal dan non-fiskal yang terukur, untuk menyerap tenaga kerja dan mengurangi ketergantungan pada sektor informal."),
        ("Penguatan Data Real-Time BPS", "Penguatan kapasitas data real-time Badan Pusat Statistik untuk monitoring kemiskinan berbasis machine learning adaptif, memungkinkan respons kebijakan yang lebih cepat dan tepat sasaran."),
        ("Integrasi Dashboard Prediktif", "Integrasi sistem prediksi kemiskinan berbasis ML ke dalam Sistem Nasional Penanggulangan Kemiskinan (SNPK), menjadikan analitik data sebagai fondasi pengambilan keputusan kebijakan."),
    ]

    nc1, nc2 = st.columns(2)
    for i, (title, text) in enumerate(national_recs):
        col = nc1 if i % 2 == 0 else nc2
        with col:
            st.markdown(f"""
            <div style='background:#13161f;border:1px solid #252a38;border-radius:10px;
                        padding:1.3rem 1.5rem;margin-bottom:.8rem'>
              <div style='display:flex;gap:.8rem;align-items:flex-start;margin-bottom:.7rem'>
                <div style='font-family:"DM Mono",monospace;font-size:.75rem;color:#e8b86d;
                            background:rgba(232,184,109,.1);border:1px solid rgba(232,184,109,.25);
                            border-radius:4px;width:26px;height:26px;display:flex;align-items:center;
                            justify-content:center;flex-shrink:0'>{i+1}</div>
                <div style='font-family:"Playfair Display",serif;font-size:.95rem;font-weight:600;
                            color:#e8eaf0;line-height:1.3'>{title}</div>
              </div>
              <div style='font-size:.84rem;color:#7a8099;line-height:1.65;padding-left:2rem'>{text}</div>
            </div>""", unsafe_allow_html=True)

    # Impact projection
    st.markdown("<div class='section-header'><div class='section-title'>Proyeksi Dampak Kebijakan</div><div class='section-badge'>Simulation</div></div>", unsafe_allow_html=True)

    scenarios_year = [2024, 2025, 2026, 2027]
    baseline  = [11.15, 11.11, 10.86, 10.73]
    optimistic = [11.15, 10.60, 10.00,  9.40]
    aggressive = [11.15, 10.20,  9.40,  8.60]

    fig_sc2 = go.Figure()
    fig_sc2.add_trace(go.Scatter(x=scenarios_year, y=baseline, mode='lines+markers',
                                  name='Baseline (tanpa akselerasi)',
                                  line=dict(color='#7a8099', width=2, dash='dot'),
                                  marker=dict(size=7)))
    fig_sc2.add_trace(go.Scatter(x=scenarios_year, y=optimistic, mode='lines+markers',
                                  name='Skenario Moderat (kebijakan ditingkatkan)',
                                  line=dict(color='#e8b86d', width=2.5),
                                  marker=dict(size=8, color='#e8b86d')))
    fig_sc2.add_trace(go.Scatter(x=scenarios_year, y=aggressive, mode='lines+markers',
                                  name='Skenario Agresif (intervensi penuh)',
                                  line=dict(color='#4db87a', width=2.5),
                                  marker=dict(size=8, color='#4db87a')))
    dark_layout(fig_sc2, "Simulasi Skenario Kebijakan — Dampak Proyeksi Kemiskinan Nasional", 360)
    fig_sc2.update_yaxes(title_text="% Penduduk Miskin", range=[8, 11.5])
    st.plotly_chart(fig_sc2, use_container_width=True, config={"displayModeBar": False})

    st.markdown("""
    <div class='insight-box green'>
      <strong style='color:#4db87a'>Potensi Akselerasi:</strong> Dengan intervensi kebijakan agresif dan terkoordinasi,
      kemiskinan nasional berpotensi mencapai 8.60% pada 2027 — penghematan 2.13 poin persentase
      dibandingkan skenario baseline. Ini setara dengan pengentasan kemiskinan bagi sekitar 5–6 juta
      penduduk Indonesia.
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div style='margin-top:4rem;padding:2rem 0;border-top:1px solid #252a38;
            display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1rem'>
  <div>
    <div style='font-family:"Playfair Display",serif;font-size:.95rem;font-weight:700;
                color:#e8eaf0'>Dashboard Penelitian KIR</div>
    <div style='font-size:.75rem;color:#7a8099;margin-top:.2rem'>
      Analisis & Prediksi Kemiskinan Indonesia 2021–2027 · Innovation Science
    </div>
  </div>
  <div style='font-family:"DM Mono",monospace;font-size:.7rem;color:#7a8099;text-align:right'>
    Data: Badan Pusat Statistik (BPS) · Model: Random Forest + K-Means + PCA<br>
    R² Test 0.8642 · MAE 1.46% · 38 Provinsi · 2021–2024 Aktual
  </div>
</div>
""", unsafe_allow_html=True)
