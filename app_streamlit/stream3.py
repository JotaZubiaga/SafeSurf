import streamlit as st
import pickle
import re
import numpy as np
import time

# Cargar el modelo entrenado
with open("../models/final_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

# Palabras seguras
SAFE_WORDS = ["google.com", "amazon.com", "bbva.com", "santander.com", "slack.com", "kaggle.com", "x.com", "github.com"]
DANGER_WORDS = {
    "google": "https://www.google.com",
    "amazon": "https://www.amazon.com",
    "bbva": "https://www.bbva.com",
    "santander": "https://www.santander.com",
    "correos": "https://www.correos.es",
    "whatsapp": "https://www.whatsapp.com",
    "netflix": "https://www.netflix.com",
    "aeat": "https://www.agenciatributaria.es"
}

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
    page_title='SAFE SURF:  Analiza tu URL',
    page_icon='🌐',
    layout='wide'
)

# Estilos CSS
st.markdown(
    """
    <style>
        body {
            background: linear-gradient(90deg, #00008B, #000000);
            color: white;
        }
        .stButton>button {
            background-color: #4CAF50; 
            color: white; 
            border-radius: 5px;
        }
        .stTextInput>div>div>input {
            border-radius: 10px;
        }
        .footer {
            position: fixed; 
            bottom: 0; 
            left: 0; 
            width: 100%; 
            background-color: black; 
            color: white; 
            text-align: center; 
            padding: 5px; 
            font-size: 12px;
        }
        .stSidebar {
            width: 220px; /* Reduce the sidebar width */
        }
        iframe {
            width: 100%;
            height: 200px;
        }
        /* Pestañas con fondo azul muy oscuro */
        .tab-content {
            display: flex;
            justify-content: center;
            padding: 10px;
        }
        .tabs {
            display: flex;
            justify-content: center;
            background-color: #1c1c1c;
            border-radius: 20px;
        }
        .tabs div {
            padding: 10px 20px;
            cursor: pointer;
            border-radius: 20px;
            color: white;
            font-weight: bold;
        }
        .tabs div:hover {
            background-color: #333;
        }
        .tabs .active {
            background-color: #00CED1;
            color: black;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Pestañas en la parte superior
tabs = ["Inicio", "Análisis de URL con IA", "Análisis por imagen", "Acerca de"]
selected_tab = st.radio("Selecciona una pestaña", tabs, index=0, horizontal=True)

# Video en la parte superior
st.markdown("""
<div style="position: relative; width: 100%; height: 0; padding-top: 56.2500%;
 padding-bottom: 0; box-shadow: 0 2px 8px 0 rgba(63,69,81,0.16); margin-top: 1.6em; margin-bottom: 0.9em; overflow: hidden;
 border-radius: 8px; will-change: transform;">
  <iframe loading="lazy" style="position: absolute; width: 100%; height: 100%; top: 0; left: 0; border: none; padding: 0;margin: 0;"
    src="https://www.canva.com/design/DAGfpxvPiCk/LYUYFN463gNhK_CvUHHaKw/watch?embed" allowfullscreen="allowfullscreen" allow="fullscreen">
  </iframe>
</div>
""", unsafe_allow_html=True)

if selected_tab == "Inicio":
    st.markdown("<h1 style='text-align: center; color: #00CED1;'>SAFE SURF</h1>", unsafe_allow_html=True)
    st.image("../img/logo.jpeg", width=300)
    st.markdown("<h3 style='text-align: center;'>Bienvenido a la herramienta de análisis de URLs y detección de riesgos cibernéticos</h3>", unsafe_allow_html=True)
    st.write("Esta aplicación utiliza un modelo de Machine Learning para analizar enlaces web y detectar elementos de posible phishing, malware, y otros riesgos a la seguridad de su dispositivo")

elif selected_tab == "Análisis de URL con IA":
    st.markdown("<h2 style='text-align:center; color: #00CED1;'>Chequea la seguridad de tu URL</h2>", unsafe_allow_html=True)
    st.image("../img/logo2.png", width=300)
    type_input = st.radio("Cómo quieres analizar la URL?", ("Introducir URL", "Ingresar características manualmente"))

    features = {}
    contiene_safe_word = False  # Variable para evaluar seguridad directa

    if type_input == "Introducir URL":
        url = st.text_input("Introduce una URL para analizar:")
        if url:
            features = extract_features(url)
            contiene_safe_word = any(word in url for word in SAFE_WORDS)
            for key, value in DANGER_WORDS.items():
                if key in url.lower():
                    st.write(f"⚠️ Esta URL parece sospechosa y está imitando a **{key}**.")
                    st.write(f"URL segura sugerida: {value}")
                    break
    
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

elif selected_tab == "Análisis por imagen":
    st.markdown("<h2>PROXIMAMENTE<br>PÁGINA EN DESARROLLO</h2>", unsafe_allow_html=True)

elif selected_tab == "Acerca de":
    st.markdown("<h2>Acerca de esta herramienta</h2>", unsafe_allow_html=True)
    st.image("../img/logo3.png", width=300)

    st.write("### Autor")
    st.write("**Juan Zubiaga Delclaux** | The Bridge")

    st.write("### Contacto")
    st.write("📂 GITHUB: [Juan Zubiaga](https://github.com/JZubiaga13)")
    st.image("../img/qr.png",width=10)
    
    st.write("### ¿Qué es esta herramienta?")
    st.write("Este proyecto fue creado para ayudar a los usuarios a detectar URLs potencialmente peligrosas, como sitios de phishing o estafas en línea.")
    st.write("El objetivo es proporcionar una forma rápida y sencilla de analizar enlaces antes de hacer clic en ellos.")

    st.write("### ¿Cómo funciona?")
    st.write("La herramienta analiza las características de un enlace (como su estructura y longitud) para predecir si es seguro o no.")
    st.write("Usa un modelo de Machine Learning que ha sido entrenado con miles de URLs seguras y maliciosas.")

    st.write("### ¿Qué es el Machine Learning en este contexto?")
    st.write("El modelo aprende de ejemplos previos para reconocer patrones sospechosos en los enlaces.")
    st.write("No se basa solo en listas negras, sino que detecta señales que podrían indicar un intento de fraude.")

    st.write("### ¿Es 100% preciso?")
    st.write("Ningún sistema de seguridad es infalible. Aunque el modelo tiene una alta precisión, siempre es recomendable ser cauteloso y verificar cualquier enlace sospechoso manualmente.")



