import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
import os

# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="EDA — PMK Detection",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background: #080C14; color: #E8EDF5; }

    [data-testid="stSidebar"] {
        background: #0D1220 !important;
        border-right: 1px solid #1E2D45;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1200px;
    }
    
            
    /* Sembunyikan daftar file pages di sidebar */
    [data-testid="stSidebarNavItems"] {
        display: none !important;
    }

    [data-testid="stSidebarNavSeparator"] {
        display: none !important;
    }

    section[data-testid="stSidebar"] > div:first-child {
        padding-top: 1rem;
    }

    /* ===== PAGE HEADER ===== */
    .page-header {
        background: linear-gradient(135deg, #080C14 0%, #0D1F3C 50%, #071428 100%);
        border: 1px solid #1A2E4A;
        border-radius: 16px;
        padding: 36px 40px;
        margin-bottom: 32px;
        position: relative;
        overflow: hidden;
    }

    .page-header::before {
        content: "";
        position: absolute;
        top: -80px; right: -80px;
        width: 300px; height: 300px;
        background: radial-gradient(circle, rgba(0,149,255,0.07) 0%, transparent 70%);
        pointer-events: none;
    }

    .page-badge {
        display: inline-block;
        background: rgba(0,149,255,0.12);
        border: 1px solid rgba(0,149,255,0.3);
        color: #00A3FF;
        padding: 5px 14px;
        border-radius: 100px;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 16px;
    }

    .page-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 36px;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 10px;
        line-height: 1.2;
    }

    .page-title span {
        background: linear-gradient(135deg, #00A3FF, #00FFA3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .page-desc {
        font-size: 14px;
        color: #6B80A0;
        line-height: 1.7;
        max-width: 600px;
    }

    /* ===== SECTION ===== */
    .section-header {
        margin-bottom: 20px;
        padding-bottom: 14px;
        border-bottom: 1px solid #1A2640;
    }

    .section-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 18px;
        font-weight: 600;
        color: #E8EDF5;
        margin-bottom: 4px;
    }

    .section-desc {
        font-size: 13px;
        color: #6B80A0;
    }

    /* ===== STAT CARDS ===== */
    .stat-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 14px;
        margin-bottom: 32px;
    }

    .stat-card {
        background: #0D1220;
        border: 1px solid #1A2640;
        border-radius: 12px;
        padding: 20px;
        position: relative;
        overflow: hidden;
    }

    .stat-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        border-radius: 12px 12px 0 0;
    }

    .stat-card.blue::before  { background: linear-gradient(90deg, #00A3FF, transparent); }
    .stat-card.green::before { background: linear-gradient(90deg, #00FFA3, transparent); }
    .stat-card.red::before   { background: linear-gradient(90deg, #FF4560, transparent); }
    .stat-card.purple::before{ background: linear-gradient(90deg, #A855F7, transparent); }

    .stat-icon  { font-size: 20px; margin-bottom: 10px; }
    .stat-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 28px;
        font-weight: 700;
        color: #FFFFFF;
        line-height: 1;
        margin-bottom: 4px;
    }
    .stat-label {
        font-size: 11px;
        color: #6B80A0;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    .stat-sub {
        font-size: 11px;
        color: #4A6080;
        margin-top: 6px;
    }

    /* ===== CHART CARD ===== */
    .chart-card {
        background: #0D1220;
        border: 1px solid #1A2640;
        border-radius: 14px;
        padding: 24px;
        margin-bottom: 24px;
    }

    .chart-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 15px;
        font-weight: 600;
        color: #E8EDF5;
        margin-bottom: 4px;
    }

    .chart-sub {
        font-size: 12px;
        color: #6B80A0;
        margin-bottom: 16px;
    }

    /* ===== IMAGE GALLERY ===== */
    .gallery-label {
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        text-align: center;
        margin-top: 8px;
        padding: 6px 12px;
        border-radius: 6px;
    }

    .gallery-label.sehat {
        background: rgba(0,255,163,0.1);
        color: #00FFA3;
        border: 1px solid rgba(0,255,163,0.2);
    }

    .gallery-label.sakit {
        background: rgba(255,69,96,0.1);
        color: #FF4560;
        border: 1px solid rgba(255,69,96,0.2);
    }

    /* ===== INSIGHT BOX ===== */
    .insight-box {
        background: rgba(0,163,255,0.06);
        border: 1px solid rgba(0,163,255,0.2);
        border-radius: 10px;
        padding: 16px 20px;
        margin-top: 16px;
    }

    .insight-title {
        font-size: 12px;
        font-weight: 600;
        color: #00A3FF;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }

    .insight-text {
        font-size: 13px;
        color: #8A9BB5;
        line-height: 1.7;
    }

    /* ===== SPLIT TABLE ===== */
    .split-table {
        width: 100%;
        border-collapse: collapse;
    }

    .split-table th {
        background: #111827;
        color: #6B80A0;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        padding: 12px 16px;
        text-align: left;
        border-bottom: 1px solid #1A2640;
    }

    .split-table td {
        padding: 12px 16px;
        font-size: 13px;
        color: #C8D5E8;
        border-bottom: 1px solid #0F1A2E;
    }

    .split-table tr:last-child td { border-bottom: none; }

    .badge-blue   { background: rgba(0,163,255,0.1); color: #00A3FF; padding: 3px 10px; border-radius: 6px; font-size: 12px; font-weight: 600; }
    .badge-green  { background: rgba(0,255,163,0.1); color: #00FFA3; padding: 3px 10px; border-radius: 6px; font-size: 12px; font-weight: 600; }
    .badge-purple { background: rgba(168,85,247,0.1); color: #A855F7; padding: 3px 10px; border-radius: 6px; font-size: 12px; font-weight: 600; }

    /* ===== SIDEBAR ===== */
    .sidebar-header {
        background: linear-gradient(135deg, #0D1F3C, #071428);
        border: 1px solid #1A2E4A;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 20px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0D1F3C,#071428);
    border:1px solid #1A2E4A;border-radius:12px;padding:16px;
    margin-bottom:20px;text-align:center;">
        <div style="font-size:32px;margin-bottom:8px;">🐄</div>
        <div style="font-family:'Space Grotesk',sans-serif;font-size:16px;
        font-weight:700;color:#FFF;margin-bottom:4px;">PMK Detection</div>
        <div style="font-size:11px;color:#6B80A0;">VGG19 + Triplet Attention</div>
    </div>
    <div style="font-size:11px;color:#6B80A0;text-transform:uppercase;
    letter-spacing:1px;font-weight:600;margin-bottom:12px;">Navigasi</div>
    """, unsafe_allow_html=True)

    # Deteksi halaman aktif
    current = __file__.split("\\")[-1].split("/")[-1].replace(".py", "")

    nav_items = [
        ("beranda",       "🏠", "Beranda",               "pages/beranda.py"),
        ("eda",           "📊", "Analisis Dataset (EDA)", "pages/eda.py"),
        ("preprocessing", "🔧", "Prapemrosesan",          "pages/preprocessing.py"),
        ("predict",       "🔍", "Prediksi PMK",           "pages/predict.py"),
    ]

    for key, icon, label, path in nav_items:
        is_active = current == key
        bg    = "rgba(0,163,255,0.12)" if is_active else "rgba(255,255,255,0.03)"
        border= "rgba(0,163,255,0.4)"  if is_active else "#1A2640"
        color = "#00A3FF"              if is_active else "#C8D5E8"

        st.markdown(f"""
        <div style="background:{bg};border:1px solid {border};
        border-radius:10px;padding:2px 4px;margin-bottom:6px;">
        """, unsafe_allow_html=True)

        st.page_link(
            path,
            label=f"{icon}  {label}",
            use_container_width=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="font-size:11px;color:#6B80A0;text-align:center;line-height:1.8;">
        Skripsi — Teknik Informatika<br>
        <span style="color:#00A3FF;">2025/2026</span>
    </div>
    """, unsafe_allow_html=True)

# =========================
# PAGE HEADER
# =========================
st.markdown("""
<div class="page-header">
    <div class="page-badge">📊 Exploratory Data Analysis</div>
    <div class="page-title">Analisis <span>Dataset PMK</span></div>
    <div class="page-desc">
        Eksplorasi mendalam terhadap karakteristik dataset yang digunakan —
        distribusi kelas, komposisi pembagian data, dan visualisasi
        sampel citra untuk memvalidasi kualitas dan keseimbangan dataset.
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# STAT CARDS
# =========================
st.markdown("""
<div class="stat-grid">
    <div class="stat-card blue">
        <div class="stat-icon">🗃️</div>
        <div class="stat-value">308</div>
        <div class="stat-label">Total Citra</div>
        <div class="stat-sub">Setelah kurasi dari 380 citra mentah</div>
    </div>
    <div class="stat-card green">
        <div class="stat-icon">✅</div>
        <div class="stat-value">150</div>
        <div class="stat-label">Kelas Sehat</div>
        <div class="stat-sub">49.0% dari total dataset</div>
    </div>
    <div class="stat-card red">
        <div class="stat-icon">🦠</div>
        <div class="stat-value">158</div>
        <div class="stat-label">Kelas Sakit PMK</div>
        <div class="stat-sub">51.0% dari total dataset</div>
    </div>
    <div class="stat-card purple">
        <div class="stat-icon">✂️</div>
        <div class="stat-value">70:15:15</div>
        <div class="stat-label">Rasio Split</div>
        <div class="stat-sub">Train · Validasi · Test</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# CHART ROW 1 — PIE & BAR
# =========================
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="chart-card">
        <div class="chart-title">Distribusi Kelas Dataset</div>
        <div class="chart-sub">Proporsi kelas Sehat vs Sakit PMK</div>
    """, unsafe_allow_html=True)

    fig_pie = go.Figure(data=[go.Pie(
        labels=['Sehat', 'Sakit PMK'],
        values=[150, 158],
        hole=0.6,
        marker=dict(
            colors=['#00FFA3', '#FF4560'],
            line=dict(color='#080C14', width=3)
        ),
        textinfo='label+percent',
        textfont=dict(color='#E8EDF5', size=13),
        hovertemplate='<b>%{label}</b><br>Jumlah: %{value}<br>Proporsi: %{percent}<extra></extra>'
    )])

    fig_pie.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E8EDF5', family='Inter'),
        showlegend=True,
        legend=dict(
            font=dict(color='#8A9BB5', size=12),
            bgcolor='rgba(0,0,0,0)'
        ),
        margin=dict(t=10, b=10, l=10, r=10),
        height=280,
        annotations=[dict(
            text='<b>308</b><br><span style="color:#6B80A0">Total</span>',
            x=0.5, y=0.5,
            font=dict(size=16, color='#FFFFFF'),
            showarrow=False
        )]
    )

    st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
        <div class="insight-title">💡 Insight</div>
        <div class="insight-text">
            Dataset memiliki distribusi kelas yang <b style="color:#00FFA3">hampir seimbang</b>
            (150 Sehat vs 158 PMK). Keseimbangan ini meminimalkan risiko model
            belajar bias terhadap salah satu kelas selama proses pelatihan.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="chart-card">
        <div class="chart-title">Distribusi Per Split Dataset</div>
        <div class="chart-sub">Jumlah citra pada setiap subset data</div>
    """, unsafe_allow_html=True)

    splits     = ['Training (70%)', 'Validasi (15%)', 'Testing (15%)']
    sehat_vals = [105, 22, 23]
    pmk_vals   = [110, 24, 24]

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        name='Sehat',
        x=splits, y=sehat_vals,
        marker_color='#00FFA3',
        marker_line=dict(color='#080C14', width=1),
        text=sehat_vals,
        textposition='outside',
        textfont=dict(color='#00FFA3', size=12)
    ))
    fig_bar.add_trace(go.Bar(
        name='Sakit PMK',
        x=splits, y=pmk_vals,
        marker_color='#FF4560',
        marker_line=dict(color='#080C14', width=1),
        text=pmk_vals,
        textposition='outside',
        textfont=dict(color='#FF4560', size=12)
    ))

    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E8EDF5', family='Inter'),
        barmode='group',
        bargap=0.25,
        bargroupgap=0.1,
        legend=dict(
            font=dict(color='#8A9BB5', size=12),
            bgcolor='rgba(0,0,0,0)',
            orientation='h',
            y=1.1, x=0.5, xanchor='center'
        ),
        xaxis=dict(
            gridcolor='#1A2640',
            tickfont=dict(color='#8A9BB5', size=11),
            showline=False
        ),
        yaxis=dict(
            gridcolor='#1A2640',
            tickfont=dict(color='#8A9BB5', size=11),
            showline=False,
            range=[0, 140]
        ),
        margin=dict(t=40, b=10, l=10, r=10),
        height=280
    )

    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
        <div class="insight-title">💡 Insight</div>
        <div class="insight-text">
            Metode <b style="color:#00A3FF">Stratified Random Sampling</b>
            memastikan proporsi kelas Sehat dan PMK terjaga seimbang
            di setiap subset — Training, Validasi, maupun Testing.
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# TABEL DISTRIBUSI SPLIT
# =========================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div class="section-header">
    <div class="section-title">📋 Ringkasan Distribusi Dataset</div>
    <div class="section-desc">Detail jumlah citra per kelas pada setiap subset pembagian data</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="chart-card">
<table class="split-table">
    <thead>
        <tr>
            <th>Subset Data</th>
            <th>Proporsi</th>
            <th>Kelas Sehat</th>
            <th>Kelas Sakit PMK</th>
            <th>Total Citra</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><span class="badge-blue">Training</span></td>
            <td>70%</td>
            <td>105 citra</td>
            <td>110 citra</td>
            <td><b style="color:#E8EDF5">217 citra</b></td>
        </tr>
        <tr>
            <td><span class="badge-purple">Validasi</span></td>
            <td>15%</td>
            <td>22 citra</td>
            <td>24 citra</td>
            <td><b style="color:#E8EDF5">46 citra</b></td>
        </tr>
        <tr>
            <td><span class="badge-green">Testing</span></td>
            <td>15%</td>
            <td>23 citra</td>
            <td>24 citra</td>
            <td><b style="color:#E8EDF5">47 citra</b></td>
        </tr>
        <tr style="background:#111827;">
            <td><b style="color:#E8EDF5">Total</b></td>
            <td>100%</td>
            <td><b style="color:#00FFA3">150 citra</b></td>
            <td><b style="color:#FF4560">158 citra</b></td>
            <td><b style="color:#00A3FF">308 citra</b></td>
        </tr>
    </tbody>
</table>
</div>
""", unsafe_allow_html=True)

# =========================
# GALLERY SEHAT
# =========================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div class="section-header">
    <div class="section-title">🟢 Sampel Citra — Kelas Sehat</div>
    <div class="section-desc">Contoh citra sapi sehat dari dataset yang digunakan dalam penelitian</div>
</div>
""", unsafe_allow_html=True)

sehat_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "sehat")
sehat_files = [f"sehat{i}.jpg" for i in range(10)]

cols_sehat = st.columns(10)
for i, (col, fname) in enumerate(zip(cols_sehat, sehat_files)):
    path = os.path.join(sehat_dir, fname)
    with col:
        try:
            img = Image.open(path)
            st.image(img, use_container_width=True)   # ← ganti ini
            st.markdown(f"""
            <div class="gallery-label sehat">Sehat {i}</div>
            """, unsafe_allow_html=True)
        except:
            st.markdown(f"""
            <div style="background:#0D1220;border:1px dashed #1A2640;
            border-radius:8px;height:80px;display:flex;align-items:center;
            justify-content:center;color:#4A6080;font-size:10px;">
            No Image</div>
            <div class="gallery-label sehat">Sehat {i}</div>
            """, unsafe_allow_html=True)

# =========================
# GALLERY SAKIT PMK
# =========================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div class="section-header">
    <div class="section-title">🔴 Sampel Citra — Kelas Sakit PMK</div>
    <div class="section-desc">Contoh citra sapi terjangkit PMK — terlihat lesi vesikel pada area mulut dan kuku</div>
</div>
""", unsafe_allow_html=True)

sakit_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "sakit")
sakit_files = [f"sakit{i}.jpg" for i in range(10)]

cols_sakit = st.columns(10)
for i, (col, fname) in enumerate(zip(cols_sakit, sakit_files)):
    path = os.path.join(sakit_dir, fname)
    with col:
        try:
            img = Image.open(path)
            st.image(img, use_container_width=True)   # ← ganti ini
            st.markdown(f"""
            <div class="gallery-label sakit">PMK {i}</div>
            """, unsafe_allow_html=True)
        except:
            st.markdown(f"""
            <div style="background:#0D1220;border:1px dashed #1A2640;
            border-radius:8px;height:80px;display:flex;align-items:center;
            justify-content:center;color:#4A6080;font-size:10px;">
            No Image</div>
            <div class="gallery-label sakit">PMK {i}</div>
            """, unsafe_allow_html=True)

# =========================
# PERBEDAAN VISUAL
# =========================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div class="section-header">
    <div class="section-title">🔍 Perbedaan Visual Kedua Kelas</div>
    <div class="section-desc">Karakteristik visual yang membedakan citra Sehat dan Sakit PMK</div>
</div>
""", unsafe_allow_html=True)

col_a, col_b = st.columns(2)

with col_a:
    st.markdown("""
    <div class="chart-card">
        <div class="chart-title" style="color:#00FFA3;">✅ Ciri Kelas Sehat</div>
        <br>
        <div style="display:flex;flex-direction:column;gap:10px;">
            <div style="display:flex;align-items:flex-start;gap:10px;">
                <span style="color:#00FFA3;font-size:14px;margin-top:2px;">●</span>
                <span style="font-size:13px;color:#8A9BB5;line-height:1.6;">
                    Kulit sekitar mulut dan kuku terlihat <b style="color:#C8D5E8">mulus dan bersih</b>
                    tanpa tanda-tanda lesi atau vesikel
                </span>
            </div>
            <div style="display:flex;align-items:flex-start;gap:10px;">
                <span style="color:#00FFA3;font-size:14px;margin-top:2px;">●</span>
                <span style="font-size:13px;color:#8A9BB5;line-height:1.6;">
                    Tekstur kulit <b style="color:#C8D5E8">homogen dan normal</b>
                    dengan warna yang merata
                </span>
            </div>
            <div style="display:flex;align-items:flex-start;gap:10px;">
                <span style="color:#00FFA3;font-size:14px;margin-top:2px;">●</span>
                <span style="font-size:13px;color:#8A9BB5;line-height:1.6;">
                    Area mulut <b style="color:#C8D5E8">tidak menunjukkan</b>
                    pembengkakan, kemerahan, atau cairan abnormal
                </span>
            </div>
            <div style="display:flex;align-items:flex-start;gap:10px;">
                <span style="color:#00FFA3;font-size:14px;margin-top:2px;">●</span>
                <span style="font-size:13px;color:#8A9BB5;line-height:1.6;">
                    Kuku terlihat <b style="color:#C8D5E8">utuh dan normal</b>
                    tanpa luka atau peradangan di sekitarnya
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_b:
    st.markdown("""
    <div class="chart-card">
        <div class="chart-title" style="color:#FF4560;">🦠 Ciri Kelas Sakit PMK</div>
        <br>
        <div style="display:flex;flex-direction:column;gap:10px;">
            <div style="display:flex;align-items:flex-start;gap:10px;">
                <span style="color:#FF4560;font-size:14px;margin-top:2px;">●</span>
                <span style="font-size:13px;color:#8A9BB5;line-height:1.6;">
                    Terdapat <b style="color:#C8D5E8">vesikel (lepuhan berisi cairan)</b>
                    pada area lidah, gusi, dan bibir sapi
                </span>
            </div>
            <div style="display:flex;align-items:flex-start;gap:10px;">
                <span style="color:#FF4560;font-size:14px;margin-top:2px;">●</span>
                <span style="font-size:13px;color:#8A9BB5;line-height:1.6;">
                    Terlihat <b style="color:#C8D5E8">lesi terbuka dan kemerahan</b>
                    akibat pecahnya vesikel pada area yang terinfeksi
                </span>
            </div>
            <div style="display:flex;align-items:flex-start;gap:10px;">
                <span style="color:#FF4560;font-size:14px;margin-top:2px;">●</span>
                <span style="font-size:13px;color:#8A9BB5;line-height:1.6;">
                    Sering terlihat <b style="color:#C8D5E8">air liur berlebihan</b>
                    dan kondisi mulut yang tidak normal
                </span>
            </div>
            <div style="display:flex;align-items:flex-start;gap:10px;">
                <span style="color:#FF4560;font-size:14px;margin-top:2px;">●</span>
                <span style="font-size:13px;color:#8A9BB5;line-height:1.6;">
                    Area kuku menunjukkan <b style="color:#C8D5E8">peradangan dan luka</b>
                    yang menyebabkan sapi kesulitan berjalan
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# FOOTER
# =========================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="background:#0D1220;border:1px solid #1A2640;border-radius:14px;
padding:20px 30px;text-align:center;">
    <div style="font-size:13px;color:#6B80A0;line-height:1.8;">
        <span style="color:#00A3FF;font-weight:600;">Analisis Dataset (EDA)</span> —
        Sistem Klasifikasi PMK pada Sapi · VGG19 + Triplet Attention
    </div>
</div>
""", unsafe_allow_html=True)