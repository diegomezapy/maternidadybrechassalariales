# Metodología Sociodemográfica 

## Fuente de Datos
La presente aplicación ejemplifica su funcionalidad con una base de microdatos simulada (mock) que sigue distribuciones poblacionales representativas de una Encuesta de Hogares (EPH/EPHC). 

## Universo de Análisis
El nivel de inferencia está limitado a la población en edades comprendidas entre **15 y 80 años**. Este sesgo normativo se introduce asumiendo que es el segmento que detenta poder de decisión y capacidad económica y/u operativa representativa para la adopción digital analíticamente medible en esta investigación.

## Expansión Muestral
La mayoría de los estadísticos descriptivos se generan utilizando el **Factor de Expansión (FEX)**. Esto quiere decir que los porcentajes observados no corresponden al "n" bruto encuestado, sino al peso ponderado que cada observación tiene en la pirámide poblacional real, lo que permite extrapolar estimaciones numéricas exactas y hablar de "proporciones nacionales".

## Modelado y Regresión Logística (GLM)
En lugar de depender exclusivamente de correlaciones bivariadas (¿los hombres usan más internet?), se incluye un Logit (Regresión Logística multivariada) modelado en la librería `statsmodels` de Python:

- **Ecuación Latente**: 
    $Logit(P(Y=1)) = \alpha + \beta_1(Sexo) + \beta_2(Área) + \beta_3(Edad) + \beta_4(Educación) + \beta_5(Ingresos)$

- **Interpretación (Odds Ratios)**: Se aplican $\exp(\beta_x)$ a los coeficientes. Resultado interpretativo: si el OR para Educación Superior es `12.5`, implica que la chance de usar internet de un graduado universitario es 12.5 veces mayor que la categoría basal (Edu. Básica), manteniendo constante su edad, su área rural/urbana y su ingreso.

## Limitaciones
Si bien el proyecto ajusta modelos, el script no evalúa intrínsecamente multicolinealidad perfecta (p.ej. Quintil Q5 altísimamente correlacionado con Educación Superior) mediante factores VIF. Para avanzar a un paper formal, se sugiere extender `scripts/2_procesamiento_datos.py` agregando rutinas de robustez.
