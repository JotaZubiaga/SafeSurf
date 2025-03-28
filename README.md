# SafeSurf – Proyecto de ML para la detección de Riesgos en URLs 
**Proyecto de ML para analizar la seguridad de una URL introducida.**

Este proyecto tiene como objetivo desarrollar un modelo de aprendizaje automático capaz de identificar URLs sospechosas basándose en sus características estructurales. En esta primera versión, utiliza un enfoque basado en la extracción de features directamente desde la URL sin necesidad de acceder a la página web.

## 📌 Características Principales
- **Extracción Automática de Características:** Se analizan las URL ingresadas en Streamlit para extraer información relevante como la longitud, cantidad de guiones, si contiene HTTPS, entre otros.
- **Comparación de Modelos:** Se han probado distintos algoritmos de clasificación como Regresión Logística, Random Forest, Support Vector Machines (SVM), K-Nearest Neighbors (KNN) y árboles de decisión.
- **Optimización con GridSearchCV:** Se han utilizado técnicas de búsqueda de hiperparámetros para mejorar la precisión del modelo.
- **Interfaz en Streamlit:** Permite al usuario ingresar una URL y obtener una evaluación en tiempo real sobre su potencial de ser peligrosa.

## 📊 Dataset y Variables Utilizadas
El conjunto de datos contiene diversas variables que describen la estructura de las URLs. Algunas de las más relevantes incluyen:

### 🔗 Variables relacionadas con la estructura de la URL:
- **NumDots:** Número de puntos en la URL.
- **NumDash:** Número de guiones en la URL.
- **NumDashInHostname:** Número de guiones en el hostname.
- **UrlLength:** Longitud total de la URL.
- **NumQueryComponents:** Número de componentes en la consulta de la URL.
- **IpAddress:** Si la URL contiene una dirección IP en lugar de un dominio.
- **DomainInSubdomains:** Si el dominio principal aparece en los subdominios.
- **DomainInPaths:** Si el dominio aparece en la ruta de la URL.
- **HostnameLength:** Longitud del hostname.
- **PathLevel:** Profundidad del path en la URL.

### 🔍 Variables relacionadas con el contenido de la página:
- **NumSensitiveWords:** Cantidad de palabras clave como "login", "bank", "password" en la URL.
- **IframeOrFrame:** Si la página usa iframes para ocultar contenido.
- **InsecureForms:** Presencia de formularios inseguros.
- **PctExtHyperlinks:** Porcentaje de enlaces externos en la página.
- **FakeLinkInStatusBar:** Uso de enlaces falsos en la barra de estado del navegador.

## 🚀 Modelos de Machine Learning Utilizados
Para la clasificación de URLs, se probaron diversos modelos:

1. **Random Forest**
   - Nº de estimadores (n_estimators)= `[50, 100, 200]`
   - Profundidad maxima (max_depth)= `[20, 30]`
   - Minima division en samples (min_samples_split) = `[2, 5, 10]`
   - Minima division en hojas (min_samples_leaf) = `[1, 2, 4]`

2. **Regresión Logística**
   - Solver: `liblinear`, `lbfgs`
   - Penalización: `l1`, `l2`
   - Regularización: `C = [0.1, 1, 10]`

3. **Support Vector Machines (SVM)**
   - `C = [0.001, 0.5, 1, 5, 10, 100]`
   - `kernel = ['linear', 'rbf']`
   - `gamma = ['scale', 'auto']`

4. **K-Nearest Neighbors (KNN)**
   - `n_neighbors = [3, 5, 7]`
   - `weights = ['uniform', 'distance']`

5. **Decision Tree**
   - `max_depth = [None, 10, 20]`
   - `min_samples_split = [2, 5]`
   - `min_samples_leaf = [1, 2, 4]`

Se utilizó `GridSearchCV` para encontrar la mejor combinación de hiperparámetros y mejorar la precisión del modelo.

## 📈 Resultados y Mejor Modelo
Tras la comparación de modelos, el mejor rendimiento se obtuvo con **Random Forest** utilizando los siguientes hiperparámetros:

- `max_depth=20`
- `n_estimators=50`
- `min_samples_leaf=4`
- `bootstrap=True`
- `min_samples_split=2`

## 🖥️ Implementación en Streamlit
La aplicación en **Streamlit** permite al usuario ingresar una URL y obtener una predicción en tiempo real sobre su seguridad.

### Pasos para ejecutar la aplicación:
1. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Ejecutar la aplicación:
   ```bash
   streamlit run app.py
   ```
3. Introducir la URL en el campo de entrada y recibir el resultado de la evaluación.

## 📂 Estructura del Proyecto
```
├── data
│   ├── Phishing_Legitimate_full.csv  # Dataset original
├── models
│   ├── phishing_rf_model.pkl  # Modelo entrenado
├── notebooks
│   ├── Exploratory_Analysis.ipynb  # Análisis exploratorio
├── app.py  # Aplicación Streamlit
├── requirements.txt  # Dependencias del proyecto
├── README.md  # Documentación
```

## 📌 Conclusiones
- Se logró desarrollar un modelo de clasificación de URLs de phishing con una alta precisión.
- Se utilizó **Feature Engineering** para extraer información directamente desde la URL sin necesidad de acceder a la página.
- Se optimizó el modelo con **GridSearchCV** para obtener los mejores hiperparámetros.
- Se implementó una interfaz sencilla en **Streamlit** para evaluar URLs en tiempo real.

Este proyecto seguirá evolucionando incorporando análisis más avanzados como el uso de **Redes Neuronales** o **Modelos Basados en Transformers** para detección de phishing.

---
📌 **Autor:** Juan Zubiaga Delclaux  
📧 **Contacto:** https://github.com/JZubiaga13

