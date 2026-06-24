import streamlit as st

# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="PMK Detection System",
    page_icon="🐄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# CUSTOM CSS — DARK MODERN
# =========================
st.markdown("""
<style>
    /* ===== GLOBAL ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: #080C14;
        color: #E8EDF5;
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

    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background: #0D1220 !important;
        border-right: 1px solid #1E2D45;
    }

    [data-testid="stSidebar"] .stMarkdown p {
        color: #8A9BB5;
        font-size: 13px;
    }

    /* ===== HIDE DEFAULT ELEMENTS ===== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 2rem !important;
        max-width: 1200px;
    }

    /* ===== HERO SECTION ===== */
    .hero-wrapper {
        background: linear-gradient(135deg, #080C14 0%, #0D1F3C 50%, #071428 100%);
        border: 1px solid #1A2E4A;
        border-radius: 20px;
        padding: 60px 50px;
        margin-bottom: 40px;
        position: relative;
        overflow: hidden;
    }

    .hero-wrapper::before {
        content: "";
        position: absolute;
        top: -100px;
        right: -100px;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(0,149,255,0.08) 0%, transparent 70%);
        pointer-events: none;
    }

    .hero-wrapper::after {
        content: "";
        position: absolute;
        bottom: -80px;
        left: -80px;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(0,255,163,0.05) 0%, transparent 70%);
        pointer-events: none;
    }

    .hero-badge {
        display: inline-block;
        background: rgba(0,149,255,0.12);
        border: 1px solid rgba(0,149,255,0.3);
        color: #00A3FF;
        padding: 6px 16px;
        border-radius: 100px;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 24px;
    }

    .hero-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 52px;
        font-weight: 700;
        line-height: 1.1;
        color: #FFFFFF;
        margin-bottom: 8px;
    }

    .hero-title span {
        background: linear-gradient(135deg, #00A3FF, #00FFA3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .hero-subtitle {
        font-size: 16px;
        color: #6B80A0;
        line-height: 1.7;
        max-width: 600px;
        margin-bottom: 36px;
        font-weight: 400;
    }

    .hero-tags {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
    }

    .hero-tag {
        background: rgba(255,255,255,0.04);
        border: 1px solid #1E2D45;
        color: #8A9BB5;
        padding: 6px 14px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 500;
    }

    /* ===== METRIC CARDS ===== */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 40px;
    }

    .metric-card {
        background: #0D1220;
        border: 1px solid #1A2640;
        border-radius: 14px;
        padding: 24px 20px;
        position: relative;
        overflow: hidden;
        transition: border-color 0.3s;
    }

    .metric-card:hover {
        border-color: #2A4A7A;
    }

    .metric-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        border-radius: 14px 14px 0 0;
    }

    .metric-card.blue::before { background: linear-gradient(90deg, #00A3FF, transparent); }
    .metric-card.green::before { background: linear-gradient(90deg, #00FFA3, transparent); }
    .metric-card.purple::before { background: linear-gradient(90deg, #A855F7, transparent); }
    .metric-card.orange::before { background: linear-gradient(90deg, #FF8C00, transparent); }

    .metric-icon {
        font-size: 24px;
        margin-bottom: 12px;
    }

    .metric-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 32px;
        font-weight: 700;
        color: #FFFFFF;
        line-height: 1;
        margin-bottom: 6px;
    }

    .metric-label {
        font-size: 12px;
        color: #6B80A0;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }

    /* ===== SECTION TITLE ===== */
    .section-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 22px;
        font-weight: 600;
        color: #E8EDF5;
        margin-bottom: 6px;
    }

    .section-desc {
        font-size: 14px;
        color: #6B80A0;
        margin-bottom: 24px;
    }

    /* ===== PIPELINE STEPS ===== */
    .pipeline-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 12px;
        margin-bottom: 40px;
    }

    .pipeline-step {
        background: #0D1220;
        border: 1px solid #1A2640;
        border-radius: 12px;
        padding: 20px 16px;
        text-align: center;
        position: relative;
    }

    .pipeline-step-num {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 11px;
        font-weight: 600;
        color: #00A3FF;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    .pipeline-step-icon {
        font-size: 28px;
        margin-bottom: 10px;
        display: block;
    }

    .pipeline-step-title {
        font-size: 13px;
        font-weight: 600;
        color: #C8D5E8;
        margin-bottom: 6px;
    }

    .pipeline-step-desc {
        font-size: 11px;
        color: #6B80A0;
        line-height: 1.5;
    }

    /* ===== INFO CARDS ===== */
    .info-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 16px;
        margin-bottom: 40px;
    }

    .info-card {
        background: #0D1220;
        border: 1px solid #1A2640;
        border-radius: 14px;
        padding: 28px;
    }

    .info-card-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 16px;
        font-weight: 600;
        color: #E8EDF5;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .info-card-body {
        font-size: 13px;
        color: #8A9BB5;
        line-height: 1.8;
    }

    .highlight-text {
        color: #00A3FF;
        font-weight: 600;
    }

    /* ===== TECH STACK ===== */
    .tech-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 12px;
        margin-bottom: 40px;
    }

    .tech-card {
        background: #0D1220;
        border: 1px solid #1A2640;
        border-radius: 12px;
        padding: 18px;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .tech-icon {
        font-size: 22px;
        flex-shrink: 0;
    }

    .tech-name {
        font-size: 13px;
        font-weight: 600;
        color: #C8D5E8;
    }

    .tech-role {
        font-size: 11px;
        color: #6B80A0;
        margin-top: 2px;
    }

    /* ===== FOOTER ===== */
    .footer-wrapper {
        background: #0D1220;
        border: 1px solid #1A2640;
        border-radius: 14px;
        padding: 24px 30px;
        text-align: center;
    }

    .footer-text {
        font-size: 13px;
        color: #6B80A0;
        line-height: 1.8;
    }

    .footer-text span {
        color: #00A3FF;
        font-weight: 600;
    }

    /* ===== SIDEBAR MENU ===== */
    .sidebar-header {
        background: linear-gradient(135deg, #0D1F3C, #071428);
        border: 1px solid #1A2E4A;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 20px;
        text-align: center;
    }

    .sidebar-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 16px;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 4px;
    }

    .sidebar-sub {
        font-size: 11px;
        color: #6B80A0;
    }

    .nav-item {
        background: rgba(255,255,255,0.03);
        border: 1px solid #1A2640;
        border-radius: 10px;
        padding: 12px 16px;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 10px;
        cursor: pointer;
        transition: all 0.2s;
    }

    .nav-item:hover {
        background: rgba(0,163,255,0.08);
        border-color: rgba(0,163,255,0.3);
    }

    .nav-icon { font-size: 16px; }
    .nav-label { font-size: 13px; font-weight: 500; color: #C8D5E8; }
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
# HERO SECTION
# =========================
st.markdown("""
<div class="hero-wrapper">
    <div class="hero-badge">🔬 Deep Learning · Computer Vision · Veterinary AI</div>
    <div class="hero-title">
        Sistem Deteksi <span>Penyakit Mulut</span><br>
        <span>dan Kuku (PMK)</span> pada Sapi
    </div>
    <div class="hero-subtitle">
        Sistem klasifikasi otomatis berbasis Deep Learning menggunakan arsitektur
        VGG19 yang diperkuat mekanisme Triplet Attention untuk mendeteksi
        gejala klinis PMK pada citra sapi secara akurat dan efisien.
    </div>
    <div class="hero-tags">
        <span class="hero-tag">🧠 VGG19 Pretrained ImageNet</span>
        <span class="hero-tag">👁️ Triplet Attention</span>
        <span class="hero-tag">🖼️ CLAHE Enhancement</span>
        <span class="hero-tag">📊 308 Citra Dataset</span>
        <span class="hero-tag">⚡ 97.87% Accuracy</span>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# METRIC CARDS
# =========================
st.markdown("""
<div class="metric-grid">
    <div class="metric-card blue">
        <div class="metric-icon">🎯</div>
        <div class="metric-value">97.87%</div>
        <div class="metric-label">Akurasi Pengujian</div>
    </div>
    <div class="metric-card green">
        <div class="metric-icon">🔍</div>
        <div class="metric-value">100%</div>
        <div class="metric-label">Recall PMK</div>
    </div>
    <div class="metric-card purple">
        <div class="metric-icon">🗃️</div>
        <div class="metric-value">308</div>
        <div class="metric-label">Total Dataset</div>
    </div>
    <div class="metric-card orange">
        <div class="metric-icon">⚙️</div>
        <div class="metric-value">20.1M</div>
        <div class="metric-label">Total Parameter</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# PIPELINE
# =========================
st.markdown("""
<div class="section-title">Alur Sistem</div>
<div class="section-desc">Pipeline pemrosesan dari citra mentah hingga hasil klasifikasi</div>
<div class="pipeline-grid">
    <div class="pipeline-step">
        <div class="pipeline-step-num">Step 01</div>
        <span class="pipeline-step-icon">🗃️</span>
        <div class="pipeline-step-title">Dataset</div>
        <div class="pipeline-step-desc">308 citra sapi terkurasi — Sehat & Sakit PMK</div>
    </div>
    <div class="pipeline-step">
        <div class="pipeline-step-num">Step 02</div>
        <span class="pipeline-step-icon">🔧</span>
        <div class="pipeline-step-title">CLAHE</div>
        <div class="pipeline-step-desc">Peningkatan kontras adaptif pada ruang warna LAB</div>
    </div>
    <div class="pipeline-step">
        <div class="pipeline-step-num">Step 03</div>
        <span class="pipeline-step-icon">🔄</span>
        <div class="pipeline-step-title">Augmentasi</div>
        <div class="pipeline-step-desc">Variasi rotasi, zoom, flip untuk data latih</div>
    </div>
    <div class="pipeline-step">
        <div class="pipeline-step-num">Step 04</div>
        <span class="pipeline-step-icon">🧠</span>
        <div class="pipeline-step-title">VGG19 + TA</div>
        <div class="pipeline-step-desc">Ekstraksi fitur + pembobotan Triplet Attention</div>
    </div>
    <div class="pipeline-step">
        <div class="pipeline-step-num">Step 05</div>
        <span class="pipeline-step-icon">✅</span>
        <div class="pipeline-step-title">Klasifikasi</div>
        <div class="pipeline-step-desc">Output: Sehat atau Sakit PMK + confidence score</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# INFO CARDS
# =========================
st.markdown("""
<div class="info-grid">
    <div class="info-card">
        <div class="info-card-title">🦠 Apa itu PMK?</div>
        <div class="info-card-body">
            Penyakit Mulut dan Kuku (PMK) adalah penyakit hewan menular akut
            yang disebabkan oleh virus <span class="highlight-text">Foot-and-Mouth Disease Virus (FMDV)</span>.
            Penyakit ini menyerang sapi dan hewan berkuku belah lainnya,
            menyebabkan lesi vesikel pada mulut, lidah, dan kuku yang dapat
            mengakibatkan penurunan produktivitas signifikan serta kerugian
            ekonomi besar bagi peternak di Indonesia.
        </div>
    </div>
    <div class="info-card">
        <div class="info-card-title">🧠 Mengapa Deep Learning?</div>
        <div class="info-card-body">
            Diagnosis manual PMK membutuhkan keahlian khusus dan rentan
            terhadap subjektivitas. Sistem ini menggunakan arsitektur
            <span class="highlight-text">VGG19 dengan Triplet Attention</span>
            yang mampu mendeteksi pola visual lesi PMK secara otomatis dari
            citra, memfokuskan perhatian pada area mulut dan kuku sapi yang
            relevan, sehingga dapat mendukung deteksi dini yang cepat,
            akurat, dan konsisten.
        </div>
    </div>
    <div class="info-card">
        <div class="info-card-title">👁️ Apa itu Triplet Attention?</div>
        <div class="info-card-body">
            Triplet Attention adalah mekanisme perhatian yang menganalisis
            <span class="highlight-text">tiga perspektif dimensi</span> secara simultan —
            Spatial (H×W), Channel-Width (C×W), dan Channel-Height (H×C).
            Dengan hanya menambahkan <span class="highlight-text">294 parameter tambahan</span>,
            mekanisme ini mampu membantu model memfokuskan perhatian pada
            fitur visual lesi PMK yang relevan dan mengabaikan noise
            latar belakang secara efisien.
        </div>
    </div>
    <div class="info-card">
        <div class="info-card-title">📊 Hasil Penelitian</div>
        <div class="info-card-body">
            Model VGG19 + Triplet Attention berhasil mencapai
            <span class="highlight-text">Akurasi 97.87%</span> dengan
            <span class="highlight-text">Recall PMK 100%</span> pada 47 citra data uji.
            Dibandingkan VGG19 Baseline, model yang diusulkan menunjukkan
            konvergensi lebih cepat pada epoch ke-26 vs epoch ke-29,
            serta validation loss lebih rendah (0.1649 vs 0.1820),
            membuktikan kontribusi positif mekanisme Triplet Attention.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# TECH STACK
# =========================
st.markdown("""
<div class="section-title">Teknologi yang Digunakan</div>
<div class="section-desc">Library dan framework yang mendukung sistem ini</div>
<div class="tech-grid">
    <div class="tech-card">
        <span class="tech-icon">🔷</span>
        <div>
            <div class="tech-name">TensorFlow & Keras</div>
            <div class="tech-role">Deep Learning Framework</div>
        </div>
    </div>
    <div class="tech-card">
        <span class="tech-icon">🟢</span>
        <div>
            <div class="tech-name">OpenCV</div>
            <div class="tech-role">Image Processing & CLAHE</div>
        </div>
    </div>
    <div class="tech-card">
        <span class="tech-icon">🔴</span>
        <div>
            <div class="tech-name">Streamlit</div>
            <div class="tech-role">Web Application Framework</div>
        </div>
    </div>
    <div class="tech-card">
        <span class="tech-icon">🟡</span>
        <div>
            <div class="tech-name">Scikit-Learn</div>
            <div class="tech-role">Evaluasi & Data Splitting</div>
        </div>
    </div>
    <div class="tech-card">
        <span class="tech-icon">🔵</span>
        <div>
            <div class="tech-name">NumPy & Pandas</div>
            <div class="tech-role">Data Manipulation</div>
        </div>
    </div>
    <div class="tech-card">
        <span class="tech-icon">🟠</span>
        <div>
            <div class="tech-name">Matplotlib</div>
            <div class="tech-role">Visualisasi Data</div>
        </div>
    </div>
    <div class="tech-card">
        <span class="tech-icon">🟣</span>
        <div>
            <div class="tech-name">Plotly</div>
            <div class="tech-role">Interactive Charts</div>
        </div>
    </div>
    <div class="tech-card">
        <span class="tech-icon">⚫</span>
        <div>
            <div class="tech-name">Google Colab</div>
            <div class="tech-role">Training Environment</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# FOOTER
# =========================
st.markdown("""
<div class="footer-wrapper">
    <div style="font-size:28px;margin-bottom:12px;">🐄</div>
    <div class="footer-text">
        <span>Sistem Klasifikasi PMK pada Sapi</span> menggunakan VGG19 + Triplet Attention<br>
        Skripsi — Teknik Informatika &nbsp;·&nbsp;
        Dataset: <span>308 Citra</span> &nbsp;·&nbsp;
        Akurasi: <span>97.87%</span> &nbsp;·&nbsp;
        Recall PMK: <span>100%</span>
    </div>
</div>
""", unsafe_allow_html=True)