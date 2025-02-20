import streamlit as st
import pickle
import re
import numpy as np
import time
import os

# Cargar el modelo entrenado
MODEL_PATH = "phishing_rf_model.pkl"

if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, "rb") as model_file:
        model = pickle.load(model_file)
else:
    st.error("⚠️ No se encontró el archivo del modelo. Asegúrate de que 'phishing_rf_model.pkl' está en la carpeta correcta.")
    st.stop()

# Palabras seguras
SAFE_WORDS = ["google.com", "amazon.com", "bbva.com", "santander.com", "slack.com", "kaggle.com", "x.com", "github.com"]

st.set_page_config(
    page_title='Analiza tu URL',
    page_icon='🌐',
    layout='wide'
)
# Diccionario de nombres en español para las características
features_es = {
    "NumDash": "Número de guiones",
    "NumDots": "Número de puntos",
    "NumDashInHostname": "Número de guiones en el hostname",
    "NumQueryComponents": "Número de parámetros en la query",
    "IpAddress": "¿Contiene una IP en lugar de dominio?",
    "DomainInSubdomains": "¿El dominio está en los subdominios?",
    "DomainInPaths": "¿El dominio aparece en la ruta?",
    "HostnameLength": "Longitud del hostname",
    "PathLevel": "Nivel del path",
    "UrlLength": "Longitud del URL"
}

# Función para extraer características del URL
def extract_features(url):
    try:
        split_url = url.split("/")
        hostname = split_url[2] if len(split_url) > 2 else ""
        return {
            "NumDash": url.count("-"),
            "NumDots": url.count("."),
            "NumDashInHostname": hostname.count("-"),
            "NumQueryComponents": url.count("&") + url.count("="),
            "IpAddress": 1 if re.match(r"(\d{1,3}\.){3}\d{1,3}", url) else 0,
            "DomainInSubdomains": 1 if len(hostname.split(".")) > 2 else 0,
            "DomainInPaths": 1 if "/" in url.split("?")[0] else 0,
            "HostnameLength": len(hostname),
            "PathLevel": url.count("/"),
            "UrlLength": len(url)
        }
    except Exception as e:
        st.error(f"⚠️ Error al extraer características: {e}")
        return None

# Interfaz en Streamlit
st.title("SAFE SURFING")
st.image("Safe copia.jpg", width=300)
st.subheader('CHEQUEA LA SEGURIDAD DE TU URL CON MACHINE LEARNING')

# Modo de entrada
type_input = st.radio("Cómo quieres analizar la URL?", ("Introducir URL", "Ingresar características manualmente"))

features = None
contiene_safe_word = False  # Variable para evaluar seguridad directa

if type_input == "Introducir URL":
    url = st.text_input("Introduce una URL para analizar:")
    if url:
        features = extract_features(url)
        if features:
            contiene_safe_word = any(word in url for word in SAFE_WORDS)

elif type_input == "Ingresar características manualmente":
    features = {
        "NumDash": st.number_input(features_es["NumDash"], min_value=0, value=0),
        "NumDots": st.number_input(features_es["NumDots"], min_value=0, value=0),
        "NumDashInHostname": st.number_input(features_es["NumDashInHostname"], min_value=0, value=0),
        "NumQueryComponents": st.number_input(features_es["NumQueryComponents"], min_value=0, value=0),
        "IpAddress": st.selectbox(features_es["IpAddress"], [0, 1]),
        "DomainInSubdomains": st.selectbox(features_es["DomainInSubdomains"], [0, 1]),
        "DomainInPaths": st.selectbox(features_es["DomainInPaths"], [0, 1]),
        "HostnameLength": st.number_input(features_es["HostnameLength"], min_value=0, value=10),
        "PathLevel": st.number_input(features_es["PathLevel"], min_value=0, value=1),
        "UrlLength": st.number_input(features_es["UrlLength"], min_value=0, value=10)
    }

if st.button("🔍 Analizar"):
    if features is None:
        st.error("⚠️ No se pudieron extraer características de la URL. Verifica la URL ingresada.")
    else:
        progress_bar = st.progress(0)  # Inicializa la barra en 0

        for percent_complete in range(0, 101, 5):  # Incrementa de 5 en 5
            time.sleep(0.05)  # Ajusta la velocidad de llenado (total ~2 segundos)
            progress_bar.progress(percent_complete)  # Actualiza la barra


# Después de llenarse completamente, se oculta automáticamente


        feature_values = np.array(list(features.values())).reshape(1, -1)
        prediction = model.predict(feature_values)[0]
        prob = model.predict_proba(feature_values)[0]

        # Si la URL contiene una palabra segura, ajustamos la probabilidad de seguridad
        if contiene_safe_word:
            prob[0] = min(prob[0] + 0.25, 1.0)  
            prob[1] = 1.0 - prob[0]

        # Evaluar seguridad
        if prob[0] >= 0.75:
            result = "🎉 La URL parece **MUY SEGURA** ✅"
            st.balloons()
        elif 0.60 < prob[0] < 0.75:
            result = "La URL parece **SEGURA** 🟢"
        elif 0.50 <= prob[0] <= 0.60:
            result = "La URL parece **SEGURA** ☑️ Continúa con precaución"
        elif 0.25 <= prob[0] < 0.50:
            result = "Parece **INSEGURA** ⚠️ No compartas información personal"
        else:
            result = "🚩 ALTAMENTE **INSEGURA** 🏴‍☠️ NO ENTRAR ⛔️"

        st.write(result)

        # Mostrar detalles con nombres en español
        st.write("**Probabilidad:**")
        st.write(f"✔️ Potencial de seguridad: {prob[0]:.2%} | ❌ Potencial de peligro: {prob[1]:.2%}")

        st.write("🔍 **Características extraídas:**")
        features_traducidas = {features_es[key]: value for key, value in features.items()}
        features_traducidas["Contiene un elemento de confianza"] = "Sí" if contiene_safe_word else "No"
        st.json(features_traducidas)

# Barra inferior negra
st.markdown("""
    <style>
        .footer {
            position: fixed; bottom: 0; left: 0; width: 100%; 
            background-color: black; color: white; text-align: 
            center; padding: 5px; font-size: 12px;}
    </style>
    <div class="footer">JUAN ZUBIAGA DELCLAUX – THE BRIDGE – Más proyectos como este en: https://github.com/JZubiaga13</div>
""", unsafe_allow_html=True)
