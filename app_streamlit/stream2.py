import streamlit as st
import pickle
import re
import numpy as np
import time

# Cargar el modelo entrenado
with open("./models/_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

# Palabras seguras
SAFE_WORDS = ["google.com", "amazon.com", "bbva.com", "santander.com", "slack.com", "kaggle.com", "x.com", "github.com"]

# Función para extraer características del URL
def extract_features(url):
    return {
        "NumDash": url.count("-"),
        "NumDots": url.count("."),
        "NumDashInHostname": url.split("/")[2].count("-") if len(url.split("/")) > 2 else 0,
        "NumQueryComponents": url.count("&") + url.count("="),
        "IpAddress": 1 if re.match(r"(\d{1,3}\.){3}\d{1,3}", url) else 0,
        "DomainInSubdomains": 1 if len(url.split(".")) > 2 else 0,
        "DomainInPaths": 1 if "/" in url.split("?")[0] else 0,
        "HostnameLength": len(url.split("/")[2]) if len(url.split("/")) > 2 else 0,
        "PathLevel": url.count("/"),
        "UrlLength": len(url)
    }
# Configuración de la página
st.set_page_config(
    page_title='Analiza tu URL',
    page_icon='🌐',
    layout='wide'
)
# Estilos CSS
st.markdown(
    """
    <style>
        body {background-color: #f5f7fa;}
        .stButton>button {background-color: #4CAF50; color: white; border-radius: 5px;}
        .stTextInput>div>div>input {border-radius: 10px;}
        .footer {position: fixed; bottom: 0; left: 0; width: 100%; 
                 background-color: black; color: white; text-align: center; 
                 padding: 5px; font-size: 12px;}
    </style>
    """,
    unsafe_allow_html=True
)

# Barra lateral para navegación
menu = st.sidebar.selectbox("Navegación", ["Inicio", "Análisis de URL", "Acerca de"])

if menu == "Inicio":
    st.markdown("<h1 style='text-align: center; color: #004080;'>🔎 SAFE SURFINGZ</h1>", unsafe_allow_html=True)
    st.image("./img/Safe copia.jpg", width=300)
    st.markdown("<h3 style='text-align: center;'>Bienvenido a la herramienta de análisis de URLs y detección de riesgos cibernéticos</h3>", unsafe_allow_html=True)
    st.write("Esta aplicación utiliza un modelo de Machine Learning para analizar enlaces web y detectar elementos de posible phishing, malware, y otros riesgos a laseguridad de su dispositivo")

elif menu == "Análisis de URL":
    st.markdown("<h2 style='text-align:center; color: #004080;'>Chequea la seguridad de tu URL</h2>", unsafe_allow_html=True)
    st.image("Safe copia.jpg", width=300)
    type_input = st.radio("Cómo quieres analizar la URL?", ("Introducir URL", "Ingresar características manualmente"))
    
    features = {}
    contiene_safe_word = False  # Variable para evaluar seguridad directa

    if type_input == "Introducir URL":
        url = st.text_input("Introduce una URL para analizar:")
        if url:
            features = extract_features(url)
            contiene_safe_word = any(word in url for word in SAFE_WORDS)
    
    elif type_input == "Ingresar características manualmente":
        features = {
            "NumDash": st.number_input("Número de guiones", min_value=0, value=0),
            "NumDots": st.number_input("Número de puntos", min_value=0, value=0),
            "NumDashInHostname": st.number_input("Número de guiones en el hostname", min_value=0, value=0),
            "NumQueryComponents": st.number_input("Número de parámetros en la query", min_value=0, value=0),
            "IpAddress": st.selectbox("¿Contiene una IP en lugar de dominio?", [0, 1]),
            "DomainInSubdomains": st.selectbox("¿El dominio está en los subdominios?", [0, 1]),
            "DomainInPaths": st.selectbox("¿El dominio aparece en la ruta?", [0, 1]),
            "HostnameLength": st.number_input("Longitud del hostname", min_value=0, value=10),
            "PathLevel": st.number_input("Nivel del path", min_value=0, value=1),
            "UrlLength": st.number_input("Longitud del URL", min_value=0, value=10)
        }
    
    if st.button("🔍 Analizar"):
        st.progress(100)
        time.sleep(1)
        
        feature_values = np.array(list(features.values())).reshape(1, -1)
        prob = model.predict_proba(feature_values)[0]
        
        # Ajustar probabilidad si la URL tiene una palabra segura
        if contiene_safe_word:
            prob[0] = min(prob[0] + 0.25, 1.0)
            prob[1] = 1.0 - prob[0]
        
        # Evaluar seguridad y mostrar resultados
        with st.container():
            if prob[0] >= 0.75:
                st.markdown("<div style='background-color:#d4edda;padding:10px;border-radius:10px;'> <h3>🎉 La URL parece MUY SEGURA ✅</h3></div>", unsafe_allow_html=True)
                st.balloons()
            elif 0.60 < prob[0] < 0.75:
                st.markdown("<div style='background-color:#c3e6cb;padding:10px;border-radius:10px;'> <h3>🟢 La URL parece SEGURA</h3></div>", unsafe_allow_html=True)
            elif 0.50 <= prob[0] <= 0.60:
                st.markdown("<div style='background-color:#ffeeba;padding:10px;border-radius:10px;'> <h3>☑️ La URL parece SEGURA pero ten cuidado</h3></div>", unsafe_allow_html=True)
            elif 0.25 <= prob[0] < 0.50:
                st.markdown("<div style='background-color:#f5c6cb;padding:10px;border-radius:10px;'> <h3>⚠️ Parece PELIGROSA, evita compartir información personal</h3></div>", unsafe_allow_html=True)
            else:
                st.markdown("<div style='background-color:#f8d7da;padding:10px;border-radius:10px;'> <h3>🚩 ALTAMENTE INSEGURA ⛔️ NO ENTRAR</h3></div>", unsafe_allow_html=True)
        st.write("**Probabilidad:**")
        st.write(f"✔️ Potencial de seguridad: {prob[0]:.2%} | ❌ Potencial de peligro: {prob[1]:.2%}")

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
        st.write("🔍 **Características extraídas:**")
        features_traducidas = {features_es[key]: value for key, value in features.items()}
        features_traducidas["Contiene un elemento de confianza"] = "Sí" if contiene_safe_word else "No"
        st.json(features_traducidas)

elif menu == "Acerca de":
    st.markdown("<h2>Acerca de esta herramienta</h2>", unsafe_allow_html=True)
    st.write("Esta aplicación fue desarrollada como parte de un proyecto de Machine Learning para detectar URLs de phishing.")
    st.write("Autor: **Juan Zubiaga Delclaux** | The Bridge")
    st.write("**CONTACTO**")
    st.write("GITHUB: https://github.com/JZubiaga13")
