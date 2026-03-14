# Determinantes Socioeconómicos del Uso de Internet

Tablero estadístico interactivo orientado a analizar los factores socioeconómicos asociados al uso de internet en la población, desarrollado con fines analíticos y enfocado en la usabilidad y rigor estadístico.

## Objetivo Analítico
Identificar y visibilizar cómo características sociodemográficas como la edad, el sexo, la educación, el nivel de ingreso y el área de residencia condicionan las probabilidades de uso de internet. 

## Arquitectura Elegida
El proyecto fue construido bajo una arquitectura estrictamente **Estática en el Frontend acoplada a un Pipeline de Datos Modular en Python**.
- **Frontend (UI/UX)**: HTML5 nativo, Javascript (Vanilla ES6), Tailwind CSS (estilizado ágil) y Apache ECharts (gráficos declarativos y de alto rendimiento).
- **Backend Analytics (Data Pipeline)**: Python 3 con `pandas` y `statsmodels`.

**Justificación:**
1. **Despliegue Cero-Fricciones:** Se despliega directamente en *GitHub Pages* sin necesitar servidores (Gunicorn, Uvicorn, Streamlit, etc).
2. **Performance Frontend:** Al separar el cálculo estadístico (regresiones multivariadas) de la visualización, la web carga *instantáneamente* un JSON pre-calculado, previniendo que los navegadores móviles colapsen realizando operaciones complejas.
3. **Escalabilidad y Transparencia Analítica:** Facilita a otros investigadores actualizar el archivo fuente CSV y ejecutar el script en Python para renovar el tablero completo en segundos.

## Estructura del Repositorio
```text
/
├── README.md                           <- Este documento
├── index.html                          <- Tablero principal
├── assets/
│   ├── css/style.css                   <- Ajustes visuales extra
│   ├── js/main.js                      <- Lógica de carga y renderización de data
│   ├── js/charts.js                    <- Lógica paramétrica de ECharts
│   └── data/dashboard_data.json        <- [GENERADO] Indicadores, brechas y modelo
├── docs/
│   ├── metodologia.md                  <- Documentación metodológica 
│   └── diccionario_datos.md            <- Descriptor de variables del Dataset
├── scripts/
│   ├── 1_generar_mock.py               <- Scaffolding: script que genera data coherente
│   └── 2_procesamiento_datos.py        <- Data Pipeline: modelado y exportación de JSON
├── data_raw/
│   └── encuesta_mock.csv               <- [GENERADO] Microdatos raw para el pipeline
└── .github/
    └── workflows/
        └── deploy.yml                  <- Pipeline CI/CD a Github Pages
```

## Instrucciones de Despliegue e Instalación

### Estructura en GitHub Pages
Para desplegar este proyecto en producción (GitHub Pages), simplemente:
1. Navega a la configuración del repositorio en GitHub: **Settings -> Pages**.
2. Cambia el 'Source' a **GitHub Actions**.
3. El archivo de Workflow configurado en `.github/workflows/deploy.yml` automáticamente levantará el entorno Python, calculará el dataset y exportará el HTML a GitHub Pages cada vez que hagas un *Push* a la rama `main`.

### Ejecución Local
Para probar y modificar el proyecto a nivel local:

1. Clona el repositorio.
2. Instala los requerimientos en tu entorno Python:
   ```bash
   pip install pandas numpy statsmodels
   ```
3. Genera la base mock y extrae el JSON descriptivo:
   ```bash
   python scripts/1_generar_mock.py
   python scripts/2_procesamiento_datos.py
   ```
   *(Esto dejará un archivo en `assets/data/dashboard_data.json` y `data_raw/encuesta_mock.csv`)*
4. Dado que el proyecto usa módulos ES6 JS (`type="module"`), no puedes abrir el archivo HTML directamente por restricción de CORS locales. Debes servir la carpeta. Puedes usar Python para levantar un servidor de prueba:
   ```bash
   python -m http.server 8000
   ```
   Abre el navegador en `http://localhost:8000`.

## Recomendaciones para Actualizar Datos Reales
1. Reemplaza el archivo `data_raw/encuesta_mock.csv` con tu base real final, asegurándote de mapear/cruzar los nombres de columna en `scripts/2_procesamiento_datos.py` (ej. `edad`, `sexo`, `nivel_edu`, `fex`, `uso_internet`).
2. Observar la variable `fex` (factor de expansión muestral): el pipeline está diseñado para recibir un ponderador que represente adecuadamente el macro universo en los indicadores (KPIs). Si no hubiera factor de expansión, usar `.value_counts()` estándar o proveer una columna de `1s`.
3. Haz un `Commit` a `main`. GitHub Actions actualizará transparentemente todo el dashboard y los cálculos paramétricos.
