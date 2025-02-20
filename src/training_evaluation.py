import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from sklearn.metrics import roc_curve, auc
import pickle

# Cargar los datos procesados 
df = pd.read_csv("../data/Processed/dataset_processed.csv")

#Tras un análisis de correlaciones, VIF, SFM, Feature Selection y estudio de la aplicabilidad de las variables a Streamlit, se selecciona un grupo de variables útiles y eficaces. 
Xr = df[['NumDash','NumDots','NumDashInHostname','UrlLength','NumQueryComponents','IpAddress','DomainInSubdomains', 'DomainInPaths','HostnameLength', 'PathLevel']]
y = df['CLASS_LABEL']  # Variable Target 

# Dividir los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(Xr, y, test_size=0.2, random_state=42)

# Escalar los datos
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Guardar los datasets de entrenamiento y prueba 
# X_train.to_csv("../data/Train/X_train.csv")
# X_test.to_csv("../data/Test/X_test.csv")
# y_train.to_csv("../data/Train/y_train.csv")
# y_test.to_csv("../data/Test/y_test.csv")
#(Comentado para no sobreescribir)

# Crear el modelo de Random Forest (Los parametros se obtienen por un Pipeline-GridSearchCV)
modelorf = RandomForestClassifier(max_depth=20,
                                  n_estimators=100,
                                  min_samples_leaf=2,
                                  bootstrap=True,
                                  min_samples_split=10,
                                  random_state=42)

# Entrenar el modelo
modelorf.fit(X_train_scaled, y_train)

# Realizar las predicciones
prediccionesrf = modelorf.predict(X_test_scaled)

# Calcular las métricas
accuracyrf = accuracy_score(y_test, prediccionesrf)
precisionrf = precision_score(y_test, prediccionesrf)
recallrf = recall_score(y_test, prediccionesrf)
f1rf = f1_score(y_test, prediccionesrf)

# Imprimir las métricas
print(f'Accuracy: {accuracyrf * 100:.2f}%')
print(f'Precision: {precisionrf * 100:.2f}%')
print(f'Recall: {recallrf * 100:.2f}%')
print(f'F1 Score: {f1rf * 100:.2f}%')

# Matriz de confusión
cmrf = confusion_matrix(y_test, prediccionesrf)
print(f'Confusion Matrix:\n{cmrf}')

# Reporte de clasificación
print(classification_report(y_test, prediccionesrf))

# Calcular la curva ROC
y_probs = modelorf.predict_proba(X_test_scaled)[:, 1]
fpr, tpr, _ = roc_curve(y_test, y_probs)
roc_aucrf = auc(fpr, tpr)

# Imprimir el AUC de la curva ROC
print(f'ROC AUC: {roc_aucrf:.2f}')

#with open("../models/final_model.pkl", "wb") as model_file:
    #pickle.dump(modelorf, model_file) #FUNCIONA PERO NO QUIERO QUE ME SOBRESCRIBA