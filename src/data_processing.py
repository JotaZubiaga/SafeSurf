import pandas as pd
import numpy as np

# Cargar el archivo CSV de datos crudos
df = pd.read_csv('../data/Raw/phishing_Legitimate_full.csv').set_index('id')

# Eliminar las columnas no necesarias
df.drop(columns=[
    'NumSensitiveWords', 'EmbeddedBrandName', 'PctExtHyperlinks',
    'PctExtResourceUrls', 'ExtFavicon', 'InsecureForms',
    'RelativeFormAction', 'ExtFormAction', 'AbnormalFormAction',
    'PctNullSelfRedirectHyperlinks', 'FrequentDomainNameMismatch',
    'FakeLinkInStatusBar', 'RightClickDisabled', 'PopUpWindow',
    'SubmitInfoToEmail', 'IframeOrFrame', 'MissingTitle',
    'ImagesOnlyInForm', 'SubdomainLevelRT', 'UrlLengthRT',
    'PctExtResourceUrlsRT', 'AbnormalExtFormActionR', 'ExtMetaScriptLinkRT',
    'PctExtNullSelfRedirectHyperlinksRT'], inplace=True)

df.drop(columns=['HttpsInHostname'],inplace=True)

# Crear nuevas características

# Sumar los caracteres especiales y otra con un ratio de ellos respecto a la longitud del url
df['SpecialChars'] = df['NumDots'] + df['NumDash'] + df['NumUnderscore']
df['SpecialCharRatio'] = df['SpecialChars'] / df['UrlLength']

# Ratio de caracteres numéricos en la URL respecto a la longitud
df['PctNumerics'] = df['NumNumericChars'] / df['UrlLength']

# Ratio de caracteres especiales en el nombre del host
df['SCHostRatio'] = (df['NumDashInHostname'] + df['SubdomainLevel']) / df['HostnameLength'].replace(0, 1)

# Ratio de la longitud del dominio respecto de todo el enlace
df['HostnameRatio'] = df['HostnameLength'] / df['UrlLength']

# Suma de los principales elementos sospechosos binarios
df['SuspiciousElements'] = df['IpAddress'] + df['NoHttps'] + df['DomainInPaths'] + df['DomainInSubdomains'] + df['DoubleSlashInPath']

# Longitud promedio de la ruta según el nivel
df['AvgPathLength'] = df['PathLength'] / df['PathLevel'].replace(0, 1)

# Ratio de parámetros de la consulta
df['QueryRatio'] = df['NumQueryComponents'] / df['QueryLength'].replace(0, 1)

# Logaritmizar las variables con distribuciones sesgadas
df['log_UrlLength'] = np.log1p(df['UrlLength'])
df['log_PathLength'] = np.log1p(df['PathLength'])
df['log_Querylength'] = np.log1p(df['QueryLength'])

# Guardar los datos procesados en un archivo CSV
#df.to_csv("../data/Processed/dataset_processed.csv") 
