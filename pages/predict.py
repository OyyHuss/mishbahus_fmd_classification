import streamlit as st
import tensorflow as tf
import numpy as np
import cv2
from PIL import Image
import os
import time

# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="Prediksi PMK — Detection System",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# TAMBAHKAN ini di paling atas, setelah import (sebelum CSS):
if 'img_to_predict' not in st.session_state:
    st.session_state.img_to_predict = None
if 'img_display' not in st.session_state:
    st.session_state.img_display = None
if 'nama_gambar' not in st.session_state:
    st.session_state.nama_gambar = ""

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
            

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1200px;
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
        background: radial-gradient(circle, rgba(255,69,96,0.07) 0%, transparent 70%);
        pointer-events: none;
    }

    .page-badge {
        display: inline-block;
        background: rgba(255,69,96,0.12);
        border: 1px solid rgba(255,69,96,0.3);
        color: #FF4560;
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
        background: linear-gradient(135deg, #FF4560, #FF8C00);
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

    /* ===== UPLOAD ZONE ===== */
    .upload-zone {
        background: #0D1220;
        border: 2px dashed #1A2640;
        border-radius: 16px;
        padding: 40px;
        text-align: center;
        margin-bottom: 24px;
        transition: border-color 0.3s;
    }

    .upload-zone:hover {
        border-color: #2A4A7A;
    }

    /* ===== RESULT CARDS ===== */
    .result-card {
        background: #0D1220;
        border: 1px solid #1A2640;
        border-radius: 14px;
        padding: 28px;
        margin-bottom: 16px;
    }

    .result-card.sehat {
        border-color: rgba(0,255,163,0.3);
        background: linear-gradient(135deg, #0D1220, #071A10);
    }

    .result-card.pmk {
        border-color: rgba(255,69,96,0.3);
        background: linear-gradient(135deg, #0D1220, #1A0710);
    }

    .result-label {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .result-label.sehat { color: #00FFA3; }
    .result-label.pmk   { color: #FF4560; }

    .result-sub {
        font-size: 13px;
        color: #6B80A0;
        margin-bottom: 20px;
    }

    /* ===== CONFIDENCE BAR ===== */
    .conf-bar-wrapper {
        background: #1A2640;
        border-radius: 100px;
        height: 10px;
        overflow: hidden;
        margin: 8px 0;
    }

    .conf-bar-fill-green {
        height: 100%;
        border-radius: 100px;
        background: linear-gradient(90deg, #00FFA3, #00D4FF);
        transition: width 1s ease;
    }

    .conf-bar-fill-red {
        height: 100%;
        border-radius: 100px;
        background: linear-gradient(90deg, #FF4560, #FF8C00);
        transition: width 1s ease;
    }

    .conf-label {
        display: flex;
        justify-content: space-between;
        font-size: 12px;
        color: #6B80A0;
        margin-bottom: 4px;
    }

    /* ===== PROB CARDS ===== */
    .prob-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        margin-top: 16px;
    }

    .prob-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid #1A2640;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
    }

    .prob-card.sehat { border-color: rgba(0,255,163,0.2); }
    .prob-card.pmk   { border-color: rgba(255,69,96,0.2); }

    .prob-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 26px;
        font-weight: 700;
        margin-bottom: 4px;
    }

    .prob-value.sehat { color: #00FFA3; }
    .prob-value.pmk   { color: #FF4560; }

    .prob-name {
        font-size: 12px;
        color: #6B80A0;
        font-weight: 500;
    }

    /* ===== ALERT BOX ===== */
    .alert-box {
        border-radius: 12px;
        padding: 20px 24px;
        margin-top: 16px;
    }

    .alert-box.sehat {
        background: rgba(0,255,163,0.06);
        border: 1px solid rgba(0,255,163,0.2);
    }

    .alert-box.pmk {
        background: rgba(255,69,96,0.06);
        border: 1px solid rgba(255,69,96,0.2);
    }

    .alert-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 15px;
        font-weight: 600;
        margin-bottom: 8px;
    }

    .alert-title.sehat { color: #00FFA3; }
    .alert-title.pmk   { color: #FF4560; }

    .alert-body {
        font-size: 13px;
        color: #8A9BB5;
        line-height: 1.7;
    }

    /* ===== INFO CARD ===== */
    .info-card {
        background: #0D1220;
        border: 1px solid #1A2640;
        border-radius: 14px;
        padding: 24px;
        margin-bottom: 16px;
    }

    .info-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 15px;
        font-weight: 600;
        color: #E8EDF5;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* ===== STEP LIST ===== */
    .step-list {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    .step-item {
        display: flex;
        align-items: flex-start;
        gap: 12px;
    }

    .step-num {
        background: rgba(0,163,255,0.12);
        border: 1px solid rgba(0,163,255,0.25);
        color: #00A3FF;
        width: 22px;
        height: 22px;
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 11px;
        font-weight: 700;
        flex-shrink: 0;
        margin-top: 1px;
    }

    .step-text {
        font-size: 13px;
        color: #8A9BB5;
        line-height: 1.6;
    }

    /* ===== MODEL INFO TABLE ===== */
    .model-table {
        width: 100%;
        border-collapse: collapse;
    }

    .model-table td {
        padding: 9px 14px;
        font-size: 13px;
        border-bottom: 1px solid #0F1A2E;
    }

    .model-table tr:last-child td { border-bottom: none; }

    .model-table .key   { color: #6B80A0; width: 50%; }
    .model-table .value { color: #C8D5E8; font-weight: 500; }

    /* ===== SIDEBAR ===== */
    .sidebar-header {
        background: linear-gradient(135deg, #0D1F3C, #071428);
        border: 1px solid #1A2E4A;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 20px;
        text-align: center;
    }

    /* ===== EXAMPLE IMAGES ===== */
    .example-label {
        font-size: 10px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        text-align: center;
        margin-top: 6px;
        padding: 4px 8px;
        border-radius: 6px;
    }

    .example-label.sehat {
        background: rgba(0,255,163,0.1);
        color: #00FFA3;
        border: 1px solid rgba(0,255,163,0.2);
    }

    .example-label.pmk {
        background: rgba(255,69,96,0.1);
        color: #FF4560;
        border: 1px solid rgba(255,69,96,0.2);
    }
</style>
""", unsafe_allow_html=True)

# =========================
# CUSTOM LAYER TRIPLET ATTENTION
# =========================
class ZPool(tf.keras.layers.Layer):
    def call(self, inputs):
        max_pool = tf.reduce_max(inputs, axis=-1, keepdims=True)
        avg_pool = tf.reduce_mean(inputs, axis=-1, keepdims=True)
        return tf.concat([max_pool, avg_pool], axis=-1)

class AttentionGate(tf.keras.layers.Layer):
    def __init__(self, **kwargs):
        super(AttentionGate, self).__init__(**kwargs)
        self.zpool = ZPool()
        self.conv = tf.keras.layers.Conv2D(
            filters=1, kernel_size=7,
            padding='same', use_bias=False
        )
        self.activation = tf.keras.layers.Activation('sigmoid')

    def call(self, inputs):
        x = self.zpool(inputs)
        x = self.conv(x)
        x = self.activation(x)
        return x

    def get_config(self):
        return super(AttentionGate, self).get_config()

class TripletAttention(tf.keras.layers.Layer):
    def __init__(self, **kwargs):
        super(TripletAttention, self).__init__(**kwargs)
        self.hw_gate = AttentionGate()
        self.cw_gate = AttentionGate()
        self.hc_gate = AttentionGate()

    def call(self, inputs):
        hw_attn = self.hw_gate(inputs)
        hw_out  = hw_attn * inputs

        x_cw    = tf.keras.layers.Permute((3, 2, 1))(inputs)
        cw_attn = self.cw_gate(x_cw)
        cw_out  = cw_attn * x_cw
        cw_out  = tf.keras.layers.Permute((3, 2, 1))(cw_out)

        x_hc    = tf.keras.layers.Permute((1, 3, 2))(inputs)
        hc_attn = self.hc_gate(x_hc)
        hc_out  = hc_attn * x_hc
        hc_out  = tf.keras.layers.Permute((1, 3, 2))(hc_out)

        out = (hw_out + cw_out + hc_out) / 3.0
        return out

    def get_config(self):
        return super(TripletAttention, self).get_config()

# =========================
# LOAD MODEL
# =========================
def load_model():
    from huggingface_hub import hf_hub_download

    model_path = hf_hub_download(
        repo_id="Mishbahus/FMD_Class_VGG_TA",
        filename="best_model_vgg+triplet.keras",
        local_dir="/tmp/model"
    )

    model = tf.keras.models.load_model(
        model_path,
        custom_objects={
            'TripletAttention': TripletAttention,
            'ZPool': ZPool,
            'AttentionGate': AttentionGate
        }
    )
    return model

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
    return final.astype(np.float32)

# =========================
# FUNGSI PREPROCESSING
# =========================
def preprocess_image(image):
    img       = image.resize((224, 224))
    img_array = np.array(img)
    if img_array.shape[-1] == 4:
        img_array = img_array[:, :, :3]
    img_clahe      = apply_clahe(img_array)
    img_normalized = img_clahe / 255.0
    img_batch      = np.expand_dims(img_normalized, axis=0).astype(np.float32)
    return img_batch

# =========================
# FUNGSI PREDIKSI
# =========================
def predict(model, img_batch):
    prob       = model.predict(img_batch, verbose=0)[0][0]
    is_pmk     = prob > 0.5
    label      = "Sakit PMK" if is_pmk else "Sehat"
    confidence = float(prob) if is_pmk else float(1 - prob)
    return label, confidence, float(prob), is_pmk

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

    # Status model di sidebar
    st.markdown("""
    <div style="font-size:11px;color:#6B80A0;text-transform:uppercase;
    letter-spacing:1px;font-weight:600;margin-bottom:10px;">Status Model</div>
    """, unsafe_allow_html=True)

    try:
        model = load_model()
        st.markdown("""
        <div style="background:rgba(0,255,163,0.08);border:1px solid
        rgba(0,255,163,0.2);border-radius:8px;padding:10px 12px;">
            <div style="font-size:12px;color:#00FFA3;font-weight:600;">
                ✅ Model Siap
            </div>
            <div style="font-size:11px;color:#6B80A0;margin-top:4px;">
                VGG19 + Triplet Attention
            </div>
        </div>
        """, unsafe_allow_html=True)
        model_loaded = True
    except Exception as e:
        st.markdown(f"""
        <div style="background:rgba(255,69,96,0.08);border:1px solid
        rgba(255,69,96,0.2);border-radius:8px;padding:10px 12px;">
            <div style="font-size:12px;color:#FF4560;font-weight:600;">
                ❌ Model Gagal Dimuat
            </div>
            <div style="font-size:11px;color:#6B80A0;margin-top:4px;">
                {str(e)[:60]}...
            </div>
        </div>
        """, unsafe_allow_html=True)
        model_loaded = False

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
    <div class="page-badge">🔍 AI-Powered Classification</div>
    <div class="page-title">Prediksi <span>Penyakit PMK</span></div>
    <div class="page-desc">
        Unggah citra sapi untuk diklasifikasikan secara otomatis
        menggunakan model VGG19 + Triplet Attention yang telah dilatih
        dengan dataset 310 citra dan mencapai akurasi 97.87%.
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# MAIN LAYOUT
# =========================
col_kiri, col_kanan = st.columns([1.2, 1], gap="large")

# ===== KOLOM KIRI — INPUT =====
with col_kiri:
    st.markdown("""
    <div style="font-size:13px;font-weight:600;color:#E8EDF5;
    margin-bottom:12px;">📤 Sumber Gambar</div>
    """, unsafe_allow_html=True)

    tab_upload, tab_contoh = st.tabs(["Upload Gambar", "Pilih Contoh Dataset"])

    # TAB 1 — UPLOAD
    with tab_upload:
        uploaded_file = st.file_uploader(
            "Pilih file gambar (JPG, JPEG, PNG)",
            type=["jpg", "jpeg", "png"],
            key="upload_predict",
            label_visibility="collapsed"
        )
        if uploaded_file:
            img_pil = Image.open(uploaded_file).convert("RGB")
            st.session_state.img_to_predict = img_pil
            st.session_state.img_display    = img_pil
            st.session_state.nama_gambar    = uploaded_file.name
            # ✅ KUNCI: tandai bahwa sumber adalah upload
            st.session_state.sumber_aktif   = "upload"

    # TAB 2 — CONTOH DATASET
    with tab_contoh:
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            kelas_contoh = st.selectbox(
                "Kelas:", ["Sehat", "Sakit PMK"],
                key="kelas_contoh"
            )
        with col_t2:
            nomor_contoh = st.selectbox(
                "Nomor Gambar:", list(range(10)),
                key="nomor_contoh"
            )

        prefix = "sehat" if kelas_contoh == "Sehat" else "sakit"
        folder = "sehat" if kelas_contoh == "Sehat" else "sakit"
        base_d = os.path.dirname(os.path.dirname(__file__))
        path_c = os.path.join(base_d, "assets", folder,
                              f"{prefix}{nomor_contoh}.jpg")

        # Tombol khusus untuk pilih contoh
        btn_pilih = st.button("✅ Gunakan Gambar Ini", key="btn_pilih_contoh")

        if btn_pilih and os.path.exists(path_c):
            img_pil = Image.open(path_c).convert("RGB")
            st.session_state.img_to_predict = img_pil
            st.session_state.img_display    = img_pil
            st.session_state.nama_gambar    = f"{prefix}{nomor_contoh}.jpg"
            # ✅ KUNCI: tandai bahwa sumber adalah contoh
            st.session_state.sumber_aktif   = "contoh"
            st.success(f"✅ Gambar {prefix}{nomor_contoh}.jpg dipilih!")
        elif btn_pilih:
            st.warning("File gambar tidak ditemukan.")

        if os.path.exists(path_c):
            st.markdown(f"""
            <div style="font-size:12px;color:#6B80A0;margin-top:8px;">
                📁 Preview: <span style="color:#00A3FF;">
                {prefix}{nomor_contoh}.jpg</span>
            </div>
            """, unsafe_allow_html=True)
            # Tampilkan preview kecil gambar contoh
            img_preview = Image.open(path_c).convert("RGB")
            st.image(img_preview, use_container_width=True)

    # ===== PREVIEW GAMBAR YANG DIPILIH =====
    if st.session_state.img_display is not None:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size:13px;font-weight:600;color:#E8EDF5;
        margin-bottom:10px;">🖼️ Gambar yang Akan Dianalisis</div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.image(st.session_state.img_display, use_container_width=True)

        w, h = st.session_state.img_display.size
        sumber_info = st.session_state.get('nama_gambar', 'Unknown')
        st.markdown(f"""
        <div style="display:flex;gap:10px;margin-top:10px;flex-wrap:wrap;">
            <div style="background:#1A2640;border-radius:6px;
            padding:4px 10px;font-size:11px;color:#8A9BB5;">
                📐 {w}×{h} px
            </div>
            <div style="background:#1A2640;border-radius:6px;
            padding:4px 10px;font-size:11px;color:#8A9BB5;">
                🔄 → 224×224 px
            </div>
            <div style="background:#1A2640;border-radius:6px;
            padding:4px 10px;font-size:11px;color:#8A9BB5;">
                ✨ CLAHE: Aktif
            </div>
            <div style="background:rgba(0,163,255,0.1);border:1px solid
            rgba(0,163,255,0.2);border-radius:6px;
            padding:4px 10px;font-size:11px;color:#00A3FF;">
                📁 {sumber_info}
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        btn_predict = st.button(
            "🔍  Analisis & Klasifikasi Sekarang",
            use_container_width=True,
            type="primary",
            disabled=not model_loaded,
            key="btn_predict_main"
        )
    else:
        btn_predict = False

# ===== KOLOM KANAN — HASIL =====
with col_kanan:
    st.markdown("""
    <div style="font-size:13px;font-weight:600;color:#E8EDF5;
    margin-bottom:12px;">📊 Hasil Klasifikasi</div>
    """, unsafe_allow_html=True)

    if st.session_state.img_to_predict is None:
        st.markdown("""
        <div style="background:#0D1220;border:2px dashed #1A2640;
        border-radius:16px;padding:60px 30px;text-align:center;">
            <div style="font-size:48px;margin-bottom:16px;">🐄</div>
            <div style="font-size:15px;color:#E8EDF5;font-weight:600;
            margin-bottom:8px;">Belum Ada Gambar</div>
            <div style="font-size:13px;color:#6B80A0;line-height:1.7;">
                Upload gambar atau pilih contoh<br>
                dari tab di sebelah kiri
            </div>
        </div>
        """, unsafe_allow_html=True)

    elif not btn_predict:
        st.markdown("""
        <div style="background:#0D1220;border:2px dashed #1A2640;
        border-radius:16px;padding:60px 30px;text-align:center;">
            <div style="font-size:48px;margin-bottom:16px;">⏳</div>
            <div style="font-size:15px;color:#E8EDF5;font-weight:600;
            margin-bottom:8px;">Gambar Siap Dianalisis</div>
            <div style="font-size:13px;color:#6B80A0;line-height:1.7;">
                Klik tombol
                <b style="color:#00A3FF">Analisis & Klasifikasi</b><br>
                di sebelah kiri untuk memulai
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ✅ PREDIKSI — ada di dalam with col_kanan
    if btn_predict and st.session_state.img_to_predict is not None:
        if not model_loaded:
            st.error("❌ Model belum berhasil dimuat.")
        else:
            with st.spinner("🧠 Menganalisis citra..."):
                time.sleep(0.5)
                img_batch = preprocess_image(
                    st.session_state.img_to_predict
                )
                label, confidence, prob, is_pmk = predict(
                    model, img_batch
                )

            css_class       = "pmk" if is_pmk else "sehat"
            icon            = "🔴" if is_pmk else "🟢"
            conf_pct        = confidence * 100
            prob_sehat      = (1 - prob) * 100
            prob_pmk        = prob * 100
            bar_color       = "red" if is_pmk else "green"
            bar_label_color = "#FF4560" if is_pmk else "#00FFA3"
            status_text     = "Terinfeksi PMK" if is_pmk else "Sehat"

            st.markdown(f"""
            <div class="result-card {css_class}">
                <div style="font-size:11px;font-weight:600;color:#6B80A0;
                text-transform:uppercase;letter-spacing:1px;
                margin-bottom:10px;">Hasil Klasifikasi</div>
                <div class="result-label {css_class}">{icon} {label}</div>
                <div class="result-sub">Model memprediksi sapi ini
                dalam kondisi <b>{status_text}</b> dengan tingkat
                kepercayaan tinggi</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="result-card {css_class}" style="margin-top:-8px;">
                <div class="conf-label">
                    <span>Confidence Score</span>
                    <span style="color:{bar_label_color};font-weight:700;">
                        {conf_pct:.2f}%
                    </span>
                </div>
                <div class="conf-bar-wrapper">
                    <div class="conf-bar-fill-{bar_color}"
                    style="width:{conf_pct:.2f}%;"></div>
                </div>
                <div class="prob-grid">
                    <div class="prob-card sehat">
                        <div class="prob-value sehat">{prob_sehat:.2f}%</div>
                        <div class="prob-name">🟢 Probabilitas Sehat</div>
                    </div>
                    <div class="prob-card pmk">
                        <div class="prob-value pmk">{prob_pmk:.2f}%</div>
                        <div class="prob-name">🔴 Probabilitas PMK</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if is_pmk:
                st.markdown(f"""
                <div class="alert-box pmk">
                    <div class="alert-title pmk">
                        ⚠️ Tindakan Segera Diperlukan
                    </div>
                    <div class="alert-body">
                        Sapi terdeteksi indikasi kuat terjangkit
                        <b style="color:#FF4560">PMK</b>
                        (confidence {conf_pct:.2f}%).<br><br>
                        <b style="color:#FF8C00">① Isolasi</b> — Pisahkan dari kawanan<br>
                        <b style="color:#FF8C00">② Laporkan</b> — Hubungi petugas kesehatan hewan<br>
                        <b style="color:#FF8C00">③ Karantina</b> — Batasi akses kandang<br>
                        <b style="color:#FF8C00">④ Disinfeksi</b> — Bersihkan area kandang
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="alert-box sehat">
                    <div class="alert-title sehat">
                        ✅ Sapi dalam Kondisi Sehat
                    </div>
                    <div class="alert-body">
                        Tidak terdeteksi indikasi PMK
                        (confidence {conf_pct:.2f}%).<br><br>
                        <b style="color:#00FFA3">① Pantau</b> — Periksa kondisi berkala<br>
                        <b style="color:#00FFA3">② Vaksinasi</b> — Pastikan jadwal vaksinasi<br>
                        <b style="color:#00FFA3">③ Sanitasi</b> — Jaga kebersihan kandang<br>
                        <b style="color:#00FFA3">④ Isolasi Baru</b> — Karantina sapi baru
                    </div>
                </div>
                """, unsafe_allow_html=True)

# =========================
# CARA KERJA SISTEM
# =========================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="background:#0D1220;border:1px solid #1A2640;
border-radius:14px;padding:24px;margin-bottom:16px;">
    <div style="font-family:'Space Grotesk',sans-serif;font-size:16px;
    font-weight:600;color:#E8EDF5;margin-bottom:16px;">
        ⚙️ Cara Kerja Sistem Prediksi
    </div>
    <div class="step-list">
        <div class="step-item">
            <div class="step-num">1</div>
            <div class="step-text">
                <b style="color:#C8D5E8">Upload Citra</b> — Citra sapi
                diunggah dalam format JPG atau PNG dengan ukuran bebas
            </div>
        </div>
        <div class="step-item">
            <div class="step-num">2</div>
            <div class="step-text">
                <b style="color:#C8D5E8">Resize</b> — Citra
                diubah ukurannya secara otomatis ke <b>224×224 piksel</b>
                sesuai standar input VGG19
            </div>
        </div>
        <div class="step-item">
            <div class="step-num">3</div>
            <div class="step-text">
                <b style="color:#C8D5E8">CLAHE Enhancement</b> —
                Algoritma CLAHE meningkatkan kontras lokal pada channel
                Lightness ruang warna LAB untuk mempertajam fitur lesi PMK
            </div>
        </div>
        <div class="step-item">
            <div class="step-num">4</div>
            <div class="step-text">
                <b style="color:#C8D5E8">Normalisasi</b> — Nilai piksel
                dinormalisasi dari 0–255 ke 0.0–1.0 untuk stabilitas inferensi
            </div>
        </div>
        <div class="step-item">
            <div class="step-num">5</div>
            <div class="step-text">
                <b style="color:#C8D5E8">VGG19 + Triplet Attention</b> —
                Model mengekstraksi fitur visual dan memfokuskan perhatian
                pada area mulut dan kuku yang relevan dengan gejala PMK
            </div>
        </div>
        <div class="step-item">
            <div class="step-num">6</div>
            <div class="step-text">
                <b style="color:#C8D5E8">Klasifikasi</b> — Output sigmoid
                menghasilkan probabilitas (0.0–1.0). Di atas 0.5 = PMK,
                di bawah 0.5 = Sehat, beserta confidence score
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# INFO MODEL
# =========================
col_m1, col_m2 = st.columns(2)

with col_m1:
    st.markdown("""
    <div class="info-card">
        <div class="info-title">🧠 Informasi Model</div>
        <table class="model-table">
            <tr>
                <td class="key">Arsitektur</td>
                <td class="value">VGG19 + Triplet Attention</td>
            </tr>
            <tr>
                <td class="key">Pretrained</td>
                <td class="value">ImageNet</td>
            </tr>
            <tr>
                <td class="key">Total Parameter</td>
                <td class="value">20.173.543</td>
            </tr>
            <tr>
                <td class="key">Trainable Parameter</td>
                <td class="value">9.587.879</td>
            </tr>
            <tr>
                <td class="key">Input Size</td>
                <td class="value">224 × 224 × 3</td>
            </tr>
            <tr>
                <td class="key">Output</td>
                <td class="value">Sigmoid (0.0 – 1.0)</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

with col_m2:
    st.markdown("""
    <div class="info-card">
        <div class="info-title">📊 Performa Model</div>
        <table class="model-table">
            <tr>
                <td class="key">Akurasi Testing</td>
                <td class="value" style="color:#00A3FF;">97.87%</td>
            </tr>
            <tr>
                <td class="key">Recall PMK</td>
                <td class="value" style="color:#00FFA3;">100%</td>
            </tr>
            <tr>
                <td class="key">Precision PMK</td>
                <td class="value">96%</td>
            </tr>
            <tr>
                <td class="key">F1-Score PMK</td>
                <td class="value">98%</td>
            </tr>
            <tr>
                <td class="key">Dataset Training</td>
                <td class="value">217 citra</td>
            </tr>
            <tr>
                <td class="key">Dataset Testing</td>
                <td class="value">47 citra</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

# =========================
# FOOTER
# =========================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="background:#0D1220;border:1px solid #1A2640;
border-radius:14px;padding:20px 30px;text-align:center;">
    <div style="font-size:13px;color:#6B80A0;line-height:1.8;">
        <span style="color:#FF4560;font-weight:600;">Sistem Prediksi PMK</span> —
        VGG19 + Triplet Attention ·
        Akurasi: <span style="color:#00A3FF;">97.87%</span> ·
        Recall PMK: <span style="color:#00FFA3;">100%</span>
    </div>
</div>
""", unsafe_allow_html=True)