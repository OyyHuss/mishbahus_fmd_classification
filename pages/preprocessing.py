import streamlit as st
import numpy as np
import cv2
from PIL import Image
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="Preprocessing — PMK Detection",
    page_icon="🔧",
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
        background: rgba(168,85,247,0.12);
        border: 1px solid rgba(168,85,247,0.3);
        color: #A855F7;
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
        background: linear-gradient(135deg, #A855F7, #00A3FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .page-desc {
        font-size: 14px;
        color: #6B80A0;
        line-height: 1.7;
        max-width: 650px;
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

    /* ===== PIPELINE STEPS ===== */
    .pipeline-row {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 14px;
        margin-bottom: 32px;
    }

    .pipeline-card {
        background: #0D1220;
        border: 1px solid #1A2640;
        border-radius: 12px;
        padding: 20px;
        position: relative;
        overflow: hidden;
    }

    .pipeline-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        border-radius: 12px 12px 0 0;
    }

    .pipeline-card.p1::before { background: linear-gradient(90deg, #00A3FF, transparent); }
    .pipeline-card.p2::before { background: linear-gradient(90deg, #A855F7, transparent); }
    .pipeline-card.p3::before { background: linear-gradient(90deg, #00FFA3, transparent); }
    .pipeline-card.p4::before { background: linear-gradient(90deg, #FF8C00, transparent); }

    .p-step {
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    .p-step.s1 { color: #00A3FF; }
    .p-step.s2 { color: #A855F7; }
    .p-step.s3 { color: #00FFA3; }
    .p-step.s4 { color: #FF8C00; }

    .p-icon { font-size: 26px; margin-bottom: 10px; display: block; }

    .p-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 14px;
        font-weight: 600;
        color: #E8EDF5;
        margin-bottom: 6px;
    }

    .p-desc {
        font-size: 12px;
        color: #6B80A0;
        line-height: 1.6;
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

    /* ===== PARAM TABLE ===== */
    .param-table {
        width: 100%;
        border-collapse: collapse;
    }

    .param-table th {
        background: #111827;
        color: #6B80A0;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        padding: 10px 16px;
        text-align: left;
        border-bottom: 1px solid #1A2640;
    }

    .param-table td {
        padding: 10px 16px;
        font-size: 13px;
        color: #C8D5E8;
        border-bottom: 1px solid #0F1A2E;
    }

    .param-table tr:last-child td { border-bottom: none; }

    .code-badge {
        background: #1A2640;
        color: #00A3FF;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 12px;
        font-family: monospace;
        font-weight: 600;
    }

    /* ===== INSIGHT BOX ===== */
    .insight-box {
        background: rgba(0,163,255,0.06);
        border: 1px solid rgba(0,163,255,0.2);
        border-radius: 10px;
        padding: 14px 18px;
        margin-top: 16px;
    }

    .insight-title {
        font-size: 11px;
        font-weight: 600;
        color: #00A3FF;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 6px;
    }

    .insight-text {
        font-size: 13px;
        color: #8A9BB5;
        line-height: 1.7;
    }

    /* ===== AUG CARD ===== */
    .aug-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 12px;
        margin-bottom: 24px;
    }

    .aug-param-card {
        background: #0D1220;
        border: 1px solid #1A2640;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
    }

    .aug-param-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 20px;
        font-weight: 700;
        color: #A855F7;
        margin-bottom: 4px;
    }

    .aug-param-name {
        font-size: 12px;
        font-weight: 600;
        color: #C8D5E8;
        margin-bottom: 4px;
    }

    .aug-param-desc {
        font-size: 11px;
        color: #6B80A0;
    }

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
# FUNGSI CLAHE
# =========================
def apply_clahe(image_array):
    img = image_array.astype(np.uint8)
    lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(8, 8))
    l_clahe = clahe.apply(l)
    limg = cv2.merge((l_clahe, a, b))
    final = cv2.cvtColor(limg, cv2.COLOR_LAB2RGB)
    return final

# =========================
# FUNGSI AUGMENTASI MANUAL
# =========================
def augment_image(image_array, aug_type):
    img = image_array.copy()
    h, w = img.shape[:2]

    if aug_type == "rotasi":
        M = cv2.getRotationMatrix2D((w//2, h//2), 15, 1.0)
        return cv2.warpAffine(img, M, (w, h),
               borderMode=cv2.BORDER_REFLECT)

    elif aug_type == "flip":
        return cv2.flip(img, 1)

    elif aug_type == "zoom":
        cx, cy = w//2, h//2
        crop = int(w * 0.1)
        cropped = img[crop:h-crop, crop:w-crop]
        return cv2.resize(cropped, (w, h))

    elif aug_type == "brightness":
        hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV).astype(np.float32)
        hsv[:,:,2] = np.clip(hsv[:,:,2] * 1.1, 0, 255)
        return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)

    elif aug_type == "shift":
        M = np.float32([[1, 0, w*0.1], [0, 1, h*0.1]])
        return cv2.warpAffine(img, M, (w, h),
               borderMode=cv2.BORDER_REFLECT)

    elif aug_type == "shear":
        pts1 = np.float32([[0,0],[w,0],[0,h]])
        pts2 = np.float32([[w*0.1,0],[w,0],[0,h]])
        M = cv2.getAffineTransform(pts1, pts2)
        return cv2.warpAffine(img, M, (w, h),
               borderMode=cv2.BORDER_REFLECT)

    return img

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
    <div class="page-badge">🔧 Image Preprocessing Pipeline</div>
    <div class="page-title">Prapemrosesan <span>& Augmentasi</span> Data</div>
    <div class="page-desc">
        Visualisasi interaktif pipeline prapemrosesan citra yang diterapkan
        dalam penelitian ini — mulai dari peningkatan kontras menggunakan CLAHE,
        normalisasi nilai piksel, hingga augmentasi data untuk memperkaya
        variasi data latih secara dinamis.
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# PIPELINE OVERVIEW
# =========================
st.markdown("""
<div class="pipeline-row">
    <div class="pipeline-card p1">
        <div class="p-step s1">Step 01</div>
        <span class="p-icon">📐</span>
        <div class="p-title">Resize</div>
        <div class="p-desc">Semua citra diubah ukurannya ke <b>224×224 piksel</b> sesuai standar input VGG19</div>
    </div>
    <div class="pipeline-card p2">
        <div class="p-step s2">Step 02</div>
        <span class="p-icon">🎨</span>
        <div class="p-title">CLAHE</div>
        <div class="p-desc">Peningkatan kontras adaptif pada <b>channel L</b> ruang warna LAB secara lokal</div>
    </div>
    <div class="pipeline-card p3">
        <div class="p-step s3">Step 03</div>
        <span class="p-icon">📏</span>
        <div class="p-title">Normalisasi</div>
        <div class="p-desc">Nilai piksel dinormalisasi dari <b>0–255</b> menjadi <b>0.0–1.0</b> untuk stabilitas training</div>
    </div>
    <div class="pipeline-card p4">
        <div class="p-step s4">Step 04</div>
        <span class="p-icon">🔄</span>
        <div class="p-title">Augmentasi</div>
        <div class="p-desc">Variasi transformasi diterapkan <b>eksklusif</b> pada data latih secara on-the-fly</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# DEMO CLAHE INTERAKTIF
# =========================
st.markdown("""
<div class="section-header">
    <div class="section-title">🎨 Demo Interaktif CLAHE</div>
    <div class="section-desc">Upload gambar atau pilih contoh dari dataset untuk melihat efek CLAHE secara langsung</div>
</div>
""", unsafe_allow_html=True)

# Pilih sumber gambar
col_opt1, col_opt2 = st.columns([1, 2])

with col_opt1:
    sumber = st.radio(
        "Sumber Gambar:",
        ["📁 Pilih dari dataset", "📤 Upload gambar sendiri"],
        key="sumber_gambar"
    )

img_input = None
nama_gambar = ""

if sumber == "📁 Pilih dari dataset":
    with col_opt2:
        col_kelas, col_nomor = st.columns(2)
        with col_kelas:
            kelas = st.selectbox("Pilih Kelas:", ["Sehat", "Sakit PMK"])
        with col_nomor:
            nomor = st.selectbox("Pilih Nomor:", list(range(10)))

        prefix = "sehat" if kelas == "Sehat" else "sakit"
        folder = "sehat" if kelas == "Sehat" else "sakit"
        base_dir = os.path.dirname(os.path.dirname(__file__))
        path_img = os.path.join(base_dir, "assets", folder,
                                f"{prefix}{nomor}.jpg")

        if os.path.exists(path_img):
            img_input = np.array(Image.open(path_img).convert("RGB").resize((224, 224)))
            nama_gambar = f"{prefix}{nomor}.jpg"
        else:
            st.warning(f"File tidak ditemukan: {path_img}")

else:
    with col_opt2:
        uploaded = st.file_uploader(
            "Upload Gambar (JPG/PNG):",
            type=["jpg", "jpeg", "png"],
            key="upload_prep"
        )
        if uploaded:
            img_input = np.array(
                Image.open(uploaded).convert("RGB").resize((224, 224))
            )
            nama_gambar = uploaded.name

# Tampilkan hasil CLAHE
if img_input is not None:
    img_clahe = apply_clahe(img_input)
    img_norm  = img_clahe / 255.0

    st.markdown("<br>", unsafe_allow_html=True)

    # ROW 1 — Gambar Asli vs CLAHE
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="chart-card">
            <div class="chart-title">📷 Gambar Asli</div>
            <div class="chart-sub">Sebelum preprocessing — ukuran 224×224 px</div>
        """, unsafe_allow_html=True)
        st.image(img_input, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="chart-card">
            <div class="chart-title" style="color:#A855F7;">✨ Setelah CLAHE</div>
            <div class="chart-sub">Kontras ditingkatkan pada channel L ruang LAB</div>
        """, unsafe_allow_html=True)
        st.image(img_clahe, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="chart-card">
            <div class="chart-title" style="color:#00FFA3;">📏 Setelah Normalisasi</div>
            <div class="chart-sub">Nilai piksel 0–255 → 0.0–1.0</div>
        """, unsafe_allow_html=True)
        st.image(img_norm, use_container_width=True,
                 clamp=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ROW 2 — Histogram
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="section-header">
        <div class="section-title">📈 Perbandingan Histogram Distribusi Piksel</div>
        <div class="section-desc">Distribusi nilai intensitas piksel sebelum dan sesudah CLAHE</div>
    </div>
    """, unsafe_allow_html=True)

    col_h1, col_h2 = st.columns(2)

    def buat_histogram(img_arr, title, color, normalized=False):
        fig, ax = plt.subplots(figsize=(6, 3))
        fig.patch.set_facecolor('#0D1220')
        ax.set_facecolor('#0D1220')

        data = img_arr.flatten()
        ax.hist(data, bins=60, color=color, alpha=0.8, edgecolor='none')
        ax.set_title(title, color='#E8EDF5', fontsize=11, pad=10)
        ax.set_xlabel(
            "Intensitas (0.0–1.0)" if normalized else "Intensitas (0–255)",
            color='#6B80A0', fontsize=9
        )
        ax.set_ylabel("Jumlah Piksel", color='#6B80A0', fontsize=9)
        ax.tick_params(colors='#6B80A0', labelsize=8)
        ax.spines['bottom'].set_color('#1A2640')
        ax.spines['left'].set_color('#1A2640')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='y', color='#1A2640', alpha=0.5, linewidth=0.5)
        plt.tight_layout()
        return fig

    with col_h1:
        st.markdown('<div class="chart-card"><div class="chart-title">Histogram — Gambar Asli</div><div class="chart-sub">Distribusi pixel sebelum CLAHE</div>', unsafe_allow_html=True)
        fig1 = buat_histogram(img_input, "Distribusi Piksel Asli", '#4A9EFF')
        st.pyplot(fig1)
        plt.close(fig1)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_h2:
        st.markdown('<div class="chart-card"><div class="chart-title">Histogram — Setelah CLAHE</div><div class="chart-sub">Distribusi pixel sesudah CLAHE (lebih merata)</div>', unsafe_allow_html=True)
        fig2 = buat_histogram(img_clahe, "Distribusi Piksel CLAHE", '#A855F7')
        st.pyplot(fig2)
        plt.close(fig2)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
        <div class="insight-title">💡 Interpretasi Histogram</div>
        <div class="insight-text">
            Histogram setelah CLAHE menunjukkan distribusi nilai piksel yang
            <b style="color:#A855F7">lebih merata dan menyebar</b> dibandingkan
            histogram asli yang cenderung menumpuk di rentang tertentu.
            Persebaran ini mengonfirmasi bahwa CLAHE berhasil meningkatkan
            kontras citra secara efektif tanpa menyebabkan <i>over-exposure</i>,
            sehingga detail fitur lesi PMK menjadi lebih terlihat jelas.
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# PARAMETER CLAHE
# =========================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div class="section-header">
    <div class="section-title">⚙️ Konfigurasi Parameter CLAHE</div>
    <div class="section-desc">Parameter yang digunakan dalam implementasi CLAHE pada penelitian ini</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="chart-card">
<table class="param-table">
    <thead>
        <tr>
            <th>Parameter</th>
            <th>Nilai</th>
            <th>Penjelasan</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><span class="code-badge">clipLimit</span></td>
            <td><b style="color:#A855F7">1.5</b></td>
            <td style="color:#8A9BB5">
                Batas amplifikasi kontras. Nilai kecil (1.5) dipilih agar peningkatan
                kontras bersifat halus dan natural, tidak berlebihan atau menimbulkan artefak
            </td>
        </tr>
        <tr>
            <td><span class="code-badge">tileGridSize</span></td>
            <td><b style="color:#A855F7">(8, 8)</b></td>
            <td style="color:#8A9BB5">
                Ukuran grid pembagian citra. Gambar dibagi menjadi 64 blok lokal (8×8),
                CLAHE bekerja secara adaptif di setiap blok secara independen
            </td>
        </tr>
        <tr>
            <td><span class="code-badge">Color Space</span></td>
            <td><b style="color:#A855F7">LAB</b></td>
            <td style="color:#8A9BB5">
                CLAHE hanya diterapkan pada channel L (Lightness), memisahkan
                informasi kecerahan dari warna agar warna asli citra tidak berubah
            </td>
        </tr>
        <tr>
            <td><span class="code-badge">Target Size</span></td>
            <td><b style="color:#A855F7">224×224 px</b></td>
            <td style="color:#8A9BB5">
                Ukuran standar input arsitektur VGG19. Semua citra di-resize
                ke dimensi ini sebelum preprocessing dilakukan
            </td>
        </tr>
        <tr>
            <td><span class="code-badge">Rescale</span></td>
            <td><b style="color:#A855F7">÷ 255</b></td>
            <td style="color:#8A9BB5">
                Normalisasi nilai piksel dari rentang 0–255 ke 0.0–1.0
                untuk menstabilkan proses konvergensi model selama pelatihan
            </td>
        </tr>
    </tbody>
</table>
</div>
""", unsafe_allow_html=True)

# =========================
# DEMO AUGMENTASI
# =========================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div class="section-header">
    <div class="section-title">🔄 Demo Augmentasi Data</div>
    <div class="section-desc">
        Augmentasi diterapkan secara eksklusif pada data latih untuk
        memperkaya variasi tanpa mengubah label kelas
    </div>
</div>
""", unsafe_allow_html=True)

# Parameter augmentasi cards
st.markdown("""
<div class="aug-grid">
    <div class="aug-param-card">
        <div class="aug-param-value">±15°</div>
        <div class="aug-param-name">Rotasi</div>
        <div class="aug-param-desc">rotation_range = 15</div>
    </div>
    <div class="aug-param-card">
        <div class="aug-param-value">10%</div>
        <div class="aug-param-name">Pergeseran</div>
        <div class="aug-param-desc">shift_range = 0.1</div>
    </div>
    <div class="aug-param-card">
        <div class="aug-param-value">10%</div>
        <div class="aug-param-name">Zoom</div>
        <div class="aug-param-desc">zoom_range = 0.1</div>
    </div>
    <div class="aug-param-card">
        <div class="aug-param-value">ON</div>
        <div class="aug-param-name">Flip Horizontal</div>
        <div class="aug-param-desc">horizontal_flip = True</div>
    </div>
    <div class="aug-param-card">
        <div class="aug-param-value">10%</div>
        <div class="aug-param-name">Shear</div>
        <div class="aug-param-desc">shear_range = 0.1</div>
    </div>
    <div class="aug-param-card">
        <div class="aug-param-value">±10%</div>
        <div class="aug-param-name">Brightness</div>
        <div class="aug-param-desc">brightness_range=[0.9, 1.1]</div>
    </div>
    <div class="aug-param-card">
        <div class="aug-param-value" style="font-size:14px;">nearest</div>
        <div class="aug-param-name">Fill Mode</div>
        <div class="aug-param-desc">Piksel kosong diisi terdekat</div>
    </div>
    <div class="aug-param-card">
        <div class="aug-param-value" style="color:#00FFA3;">Train</div>
        <div class="aug-param-name">Diterapkan Pada</div>
        <div class="aug-param-desc">Hanya data latih (217 citra)</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Demo visual augmentasi
if img_input is not None:
    st.markdown("""
    <div class="chart-card">
        <div class="chart-title">Visualisasi Hasil Augmentasi</div>
        <div class="chart-sub">6 jenis transformasi augmentasi pada gambar yang dipilih</div>
    </div>
    """, unsafe_allow_html=True)

    aug_types = [
        ("rotasi",     "🔃 Rotasi +15°"),
        ("flip",       "↔️ Flip Horizontal"),
        ("zoom",       "🔍 Zoom In 10%"),
        ("brightness", "☀️ Brightness +10%"),
        ("shift",      "↗️ Shift 10%"),
        ("shear",      "◱ Shear 10%"),
    ]

    cols_aug = st.columns(6)
    for col, (aug_type, aug_label) in zip(cols_aug, aug_types):
        with col:
            img_aug = augment_image(img_input, aug_type)
            st.image(img_aug, use_container_width=True)
            st.markdown(f"""
            <div style="text-align:center;font-size:10px;color:#A855F7;
            background:rgba(168,85,247,0.08);border:1px solid rgba(168,85,247,0.2);
            border-radius:6px;padding:4px 6px;margin-top:4px;">
            {aug_label}</div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box" style="margin-top:16px;">
        <div class="insight-title">💡 Mengapa Augmentasi Hanya untuk Data Latih?</div>
        <div class="insight-text">
            Augmentasi bertujuan membuat model <b style="color:#A855F7">tidak menghafal</b>
            pola data latih. Data Validasi dan Testing harus menggunakan gambar yang
            <b style="color:#A855F7">konsisten dan tidak dimodifikasi</b> agar evaluasi
            model bersifat objektif dan mencerminkan kondisi data nyata di lapangan.
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div style="background:#0D1220;border:2px dashed #1A2640;border-radius:14px;
    padding:40px;text-align:center;margin-top:16px;">
        <div style="font-size:40px;margin-bottom:12px;">🖼️</div>
        <div style="font-size:14px;color:#6B80A0;">
            Pilih gambar dari dataset atau upload gambar<br>
            untuk melihat demo augmentasi
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
        <span style="color:#A855F7;font-weight:600;">Prapemrosesan & Augmentasi</span> —
        Sistem Klasifikasi PMK pada Sapi · VGG19 + Triplet Attention
    </div>
</div>
""", unsafe_allow_html=True)