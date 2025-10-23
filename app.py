import streamlit as st
import os
import time
import glob
import cv2
import numpy as np
import pytesseract
from PIL import Image
from gtts import gTTS
from googletrans import Translator


# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="OCR Galáctico", page_icon="✨", layout="wide")

# --- ESTILO GALÁCTICO ---
st.markdown("""
    <style>
        /* Fondo de galaxia degradado */
        body {
            background: radial-gradient(circle at top, #0b0033, #000010 80%);
            color: #e0e0ff;
        }
        [data-testid="stAppViewContainer"] {
            background: radial-gradient(circle at top, #12003a, #000010 85%);
            color: #ffffff;
        }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0a0024, #16004b);
            color: #ffffff;
        }
        [data-testid="stHeader"] {
            background: rgba(0, 0, 0, 0);
        }
        h1, h2, h3, h4 {
            color: #a29bfe !important;
            text-shadow: 0px 0px 8px #7f5af0;
        }
        .stButton>button {
            background: linear-gradient(90deg, #4e00c2, #8e2de2);
            color: white;
            border-radius: 12px;
            border: none;
            padding: 0.6em 1.2em;
            font-weight: bold;
            box-shadow: 0 0 10px #8e2de2;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background: linear-gradient(90deg, #8e2de2, #4e00c2);
            transform: scale(1.05);
            box-shadow: 0 0 20px #a29bfe;
        }
        .stCheckbox label, .stRadio label, .stSelectbox label {
            color: #cfcfff !important;
        }
    </style>
""", unsafe_allow_html=True)


# --- INICIO DE APP ---
st.title("✨ Reconocimiento Óptico de Caracteres Galáctico ✨")
st.subheader("Escanea, traduce y convierte texto a voz, ¡como un explorador interestelar! 🚀")

translator = Translator()
text = " "


def text_to_speech(input_language, output_language, text, tld):
    translation = translator.translate(text, src=input_language, dest=output_language)
    trans_text = translation.text
    tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, trans_text


def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)


remove_files(7)

# --- SELECCIÓN DE FUENTE DE IMAGEN ---
st.markdown("### 🪐 Elige la fuente de tu imagen:")
cam_ = st.checkbox("Usar Cámara")

if cam_:
    img_file_buffer = st.camera_input("Toma una Foto 📸")
else:
    img_file_buffer = None

with st.sidebar:
    st.subheader("⚙️ Procesamiento para Cámara")
    filtro = st.radio("Aplicar filtro a imagen de cámara", ('Sí', 'No'))

# --- CARGAR IMAGEN DESDE ARCHIVO ---
bg_image = st.file_uploader("📁 Cargar Imagen desde tus archivos:", type=["png", "jpg", "jpeg"])
if bg_image is not None:
    uploaded_file = bg_image
    st.image(uploaded_file, caption='🖼️ Imagen cargada.', use_container_width=True)

    with open(uploaded_file.name, 'wb') as f:
        f.write(uploaded_file.read())

    st.success(f"✅ Imagen guardada como {uploaded_file.name}")
    img_cv = cv2.imread(f'{uploaded_file.name}')
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(img_rgb)
st.write(text)

# --- PROCESAR IMAGEN DE CÁMARA ---
if img_file_buffer is not None:
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    if filtro == 'Sí':
        cv2_img = cv2.bitwise_not(cv2_img)

    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(img_rgb)
    st.write(text)

# --- SIDEBAR DE TRADUCCIÓN ---
with st.sidebar:
    st.subheader("🌌 Parámetros de Traducción Galáctica")

    try:
        os.mkdir("temp")
    except:
        pass

    in_lang = st.selectbox(
        "🌍 Lenguaje de entrada",
        ("Ingles", "Español", "Bengali", "Koreano", "Mandarin", "Japones"),
    )
    lang_map = {
        "Ingles": "en",
        "Español": "es",
        "Bengali": "bn",
        "Koreano": "ko",
        "Mandarin": "zh-cn",
        "Japones": "ja",
    }
    input_language = lang_map[in_lang]

    out_lang = st.selectbox(
        "🚀 Lenguaje de salida",
        ("Ingles", "Español", "Bengali", "Koreano", "Mandarin", "Japones"),
    )
    output_language = lang_map[out_lang]

    english_accent = st.selectbox(
        "🌠 Selecciona acento (solo inglés)",
        (
            "Default",
            "India",
            "United Kingdom",
            "United States",
            "Canada",
            "Australia",
            "Ireland",
            "South Africa",
        ),
    )

    tld_map = {
        "Default": "com",
        "India": "co.in",
        "United Kingdom": "co.uk",
        "United States": "com",
        "Canada": "ca",
        "Australia": "com.au",
        "Ireland": "ie",
        "South Africa": "co.za",
    }
    tld = tld_map[english_accent]

    display_output_text = st.checkbox("Mostrar texto traducido")

    if st.button("🔊 Convertir a Audio Galáctico"):
        result, output_text = text_to_speech(input_language, output_language, text, tld)
        audio_file = open(f"temp/{result}.mp3", "rb")
        audio_bytes = audio_file.read()
        st.markdown("### 🎧 Tu audio está listo:")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)

        if display_output_text:
            st.markdown("### 📝 Texto traducido:")
            st.write(output_text)
