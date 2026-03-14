import pandas as pd
import numpy as np
import os

def generar_datos_mock(n=10000, output_path="data_raw/encuesta_mock.csv"):
    """
    Genera un dataset de ejemplo tipo Encuesta de Hogares para el tablero de internet.
    """
    np.random.seed(42)
    print("Generando datos simulados...")

    # Variables de diseño
    sexo = np.random.choice(["Hombre", "Mujer"], size=n, p=[0.49, 0.51])
    
    # Edad (distribución realista)
    edad = np.random.normal(loc=35, scale=18, size=n).astype(int)
    edad = np.clip(edad, 15, 80) # Solo tomamos población de 15 a 80 años para el análisis

    # Grupos de edad
    bins = [14, 24, 34, 44, 54, 64, 85]
    labels = ["15-24", "25-34", "35-44", "45-54", "55-64", "65+"]
    grupo_edad = pd.cut(edad, bins=bins, labels=labels)

    # Área de residencia
    area = np.random.choice(["Urbana", "Rural"], size=n, p=[0.65, 0.35])

    # Nivel educativo (correlacionado parcialmente con el área)
    edu_probs = {
        "Urbana": [0.2, 0.5, 0.3], # Básica, Media, Superior
        "Rural": [0.5, 0.4, 0.1]
    }
    niveles = ["Básica", "Media", "Superior"]
    nivel_edu = [np.random.choice(niveles, p=edu_probs[a]) for a in area]

    # Quintil de ingreso (correlacionado con educación)
    q_probs = {
        "Básica": [0.4, 0.3, 0.2, 0.08, 0.02],
        "Media": [0.1, 0.2, 0.3, 0.25, 0.15],
        "Superior": [0.02, 0.05, 0.13, 0.3, 0.5]
    }
    quintiles = ["Q1", "Q2", "Q3", "Q4", "Q5"]
    quintil = [np.random.choice(quintiles, p=q_probs[e]) for e in nivel_edu]

    # Departamentos (Capital + Central son mayoría urbana)
    dptos_urbanos = ["Asunción", "Central", "Alto Paraná", "Itapúa"]
    dptos_rurales = ["San Pedro", "Caaguazú", "Concepción", "Caazapá"]
    
    dpto = []
    for a in area:
        if a == "Urbana":
            dpto.append(np.random.choice(dptos_urbanos + dptos_rurales, p=[0.3, 0.4, 0.15, 0.1, 0.01, 0.02, 0.01, 0.01]))
        else:
            dpto.append(np.random.choice(dptos_rurales + dptos_urbanos, p=[0.3, 0.3, 0.2, 0.1, 0.02, 0.03, 0.03, 0.02]))

    # Generar la variable objetivo (Uso de internet) de forma multivariada (Logit real subyacente)
    # Base real = 0 (prob = 0.5)
    z = -2.0  # Base bias
    
    # Efectos
    z += np.array([0.2 if s == "Mujer" else 0.0 for s in sexo])
    z += np.array([-0.06 * (e - 30) for e in edad]) # A mayor edad, menos internet
    z += np.array([1.5 if a == "Urbana" else 0.0 for a in area])
    
    # Efectos educación
    edu_ef = {"Básica": 0.0, "Media": 1.2, "Superior": 2.5}
    z += np.array([edu_ef[e] for e in nivel_edu])
    
    # Efectos quintil
    q_ef = {"Q1": 0.0, "Q2": 0.5, "Q3": 1.0, "Q4": 1.5, "Q5": 2.0}
    z += np.array([q_ef[q] for q in quintil])

    # Convertir a probabilidad
    prob_internet = 1 / (1 + np.exp(-z))
    uso_internet = np.random.binomial(1, prob_internet)

    # Factor de expansión (Ponderador poblacional)
    fex = np.random.uniform(20, 150, size=n).astype(int)

    # Consolidar DataFrame
    df = pd.DataFrame({
        "id_pers": range(1, n+1),
        "sexo": sexo,
        "edad": edad,
        "grupo_edad": grupo_edad,
        "area": area,
        "dpto": dpto,
        "nivel_edu": nivel_edu,
        "quintil_ingreso": quintil,
        "uso_internet": uso_internet,
        "fex": fex
    })

    # Guardar CSV
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8", sep=";")
    print(f"Dataset generado exitosamente en: {output_path}")
    print(df.head())

if __name__ == "__main__":
    generar_datos_mock()
