import streamlit as st
import pickle
import numpy as np
import time
import re

# Cargar el modelo entrenado
with open("../models/final_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

# Configuración de la página
st.set_page_config(
    page_title='SAFE SURF: Analiza tu URL',
    page_icon='🌐',
    layout='wide'
)

# Estilos CSS
st.markdown(
    """
    <style>
        body { background-color: #000033 !important; color: #00CED1 !important; }
        .stApp { background-color: #000033; }
        h1, h2, h3, h4, h5, h6, p, label, .stTextInput, .stButton, .stRadio, .stMarkdown { color: #00CED1 !important; }
        .stButton>button {
            background-color: #004080; color: white; border-radius: 10px; border: 1px solid #00CED1;
        }
        .stButton>button:hover { background-color: #0055A4; }
    </style>
    """,
    unsafe_allow_html=True
)

# Pestañas principales
tabs = ["Inicio", "Análisis de URL con IA", "Análisis por imagen", "Acerca de"]
selected_tab = st.radio("", tabs, horizontal=True)

# Video en la parte superior (20% más pequeño)
st.markdown("""
<div style="position: relative; width: 80%; height: 0; padding-top: 45.0000%;
 padding-bottom: 0; box-shadow: 0 2px 8px 0 rgba(63,69,81,0.16); margin: 1.6em auto 0.9em auto; overflow: hidden;
 border-radius: 8px; will-change: transform;">
  <iframe loading="lazy" style="position: absolute; width: 100%; height: 100%; top: 0; left: 0; border: none; padding: 0;margin: 0;"
    src="https://www.canva.com/design/DAGfpxvPiCk/LYUYFN463gNhK_CvUHHaKw/watch?embed" allowfullscreen="allowfullscreen" allow="fullscreen">
  </iframe>
</div>
""", unsafe_allow_html=True)

# Diccionario de URLs seguras conocidas
safe_domains = {
    "google": "https://www.google.com",
    "amazon": "https://www.amazon.com",
    "bbva": "https://www.bbva.com",
    "paypal": "https://www.paypal.com",
    "microsoft": "https://www.microsoft.com",
    "thebridge": "https://campusvirtual.thebridge.tech/my/courses.php",

}

# Función para extraer características de una URL
def extract_features(url):
    features = {
        "NumDash": url.count("-"),
        "NumDots": url.count("."),
        "NumDashInHostname": url.split("/")[2].count("-") if len(url.split("/")) > 2 else 0,
        "NumQueryComponents": url.count("?"),
        "IpAddress": bool(re.search(r'\d+\.\d+\.\d+\.\d+', url)),
        "DomainInSubdomains": any(domain in url.split("/")[2] for domain in safe_domains),
        "DomainInPaths": any(domain in url for domain in safe_domains),
        "HostnameLength": len(url.split("/")[2]) if len(url.split("/")) > 2 else len(url),
        "PathLevel": url.count("/"),
        "UrlLength": len(url)
    }
    return features

# Función para encontrar una URL segura basada en variaciones del dominio
def get_safe_url(url):
    for domain, safe_link in safe_domains.items():
        # Buscar posibles variaciones del dominio, como 'gogle' en lugar de 'google'
        if re.search(f"{domain[:3]}.*{domain[3:]}", url.lower()):
            return safe_link
    return None

if selected_tab == "Inicio":
    st.markdown("<h1 style='text-align: center;'>SAFE SURF</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Bienvenido a la herramienta de análisis de URLs y detección de riesgos cibernéticos</h3>", unsafe_allow_html=True)
    st.write("-")
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

elif selected_tab == "Análisis de URL con IA":
    st.markdown("<h2 style='text-align:center;'>Chequea la seguridad de tu URL</h2>", unsafe_allow_html=True)

    # Pestañas dentro de "Análisis de URL con IA"
    sub_tabs = ["Introducir URL", "Ingresar características manualmente"]
    selected_sub_tab = st.radio("", sub_tabs, horizontal=True)

    if selected_sub_tab == "Introducir URL":
        url = st.text_input("Introduce una URL para analizar:")

        if st.button("🔍 Analizar") or (url and st.session_state.get("enter_pressed", False)):
            if url:
                progress_bar = st.progress(70)  # Inicia en 70%
                time.sleep(1)
                progress_bar.progress(100)  # Se llena hasta 100% en 1 segundo

                # Verificar si la URL contiene algún dominio seguro y asignar 95% de seguridad
                for domain in safe_domains.values():
                    if domain in url.lower():
                        st.markdown("<div style='background-color:#d4edda;padding:10px;border-radius:10px;'> <h3>🎉 La URL parece MUY SEGURA ✅</h3></div>", unsafe_allow_html=True)
                        st.balloons()
                        st.write(f"✔️ Potencial de seguridad: 95% | ❌ Potencial de peligro: 5%")
                        st.stop()

                # Extraer características de la URL
                features = extract_features(url)
                feature_values = np.array(list(features.values())).reshape(1, -1)
                prob = model.predict_proba(feature_values)[0]

                # Comprobar si la URL se parece a una segura
                safe_alternative = get_safe_url(url)

                # Evaluar seguridad y mostrar resultados
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

                # Probabilidades
                st.write("**Probabilidad:**")
                st.write(f"✔️ Potencial de seguridad: {prob[0]:.2%} | ❌ Potencial de peligro: {prob[1]:.2%}")

                # Mostrar características analizadas en una lista expandible
                with st.expander("🔍 **Características extraídas**"):
                    st.write(f"- **Número de guiones**: {features['NumDash']}")
                    st.write(f"- **Número de puntos**: {features['NumDots']}")
                    st.write(f"- **Número de guiones en el hostname**: {features['NumDashInHostname']}")
                    st.write(f"- **Número de componentes en la consulta**: {features['NumQueryComponents']}")
                    st.write(f"- **¿Es una dirección IP?**: {'Sí' if features['IpAddress'] else 'No'}")
                    st.write(f"- **¿Dominio seguro en subdominio?**: {'Sí' if features['DomainInSubdomains'] else 'No'}")
                    st.write(f"- **¿Dominio seguro en la ruta?**: {'Sí' if features['DomainInPaths'] else 'No'}")
                    st.write(f"- **Longitud del hostname**: {features['HostnameLength']}")
                    st.write(f"- **Nivel de la ruta**: {features['PathLevel']}")
                    st.write(f"- **Longitud total de la URL**: {features['UrlLength']}")

                # Sugerir URL segura si se detectó una alternativa
                if safe_alternative:
                    st.markdown(f"🔗 **Este enlace podría ser una alternativa segura:** [Ir a {safe_alternative}]({safe_alternative})")

    elif selected_sub_tab == "Ingresar características manualmente":
        st.write("Ingresa los valores manualmente.")

elif selected_tab == "Análisis por imagen":
    st.markdown("<h2 style='text-align:center; font-size: 36px;'>🚀 PRÓXIMAMENTE<br>🔧 EN DESARROLLO</h2>", unsafe_allow_html=True)

elif selected_tab == "Acerca de":
    st.markdown("<h2>Acerca de esta herramienta</h2>", unsafe_allow_html=True)
    st.image("../img/logo3.png", width=300)

    st.write("### Autor")
    st.write("**Juan Zubiaga Delclaux** | The Bridge")

    st.write("### Contacto")
    st.write("📂 GITHUB: [Juan Zubiaga](https://github.com/JZubiaga13)")
    st.image("../img/qr.png", width=100, use_column_width=False)
