# Diccionario de Datos

| Variable | Tipo de Dato | Descripción | Valores Posibles |
|----------|-------------|-------------|:---------------:|
| `id_pers` | Numérico | Identificador único individual | `[1, 2, 3 ... N]` |
| `sexo` | Categórico | Sexo de la persona declarante | `Hombre`, `Mujer` |
| `edad` | Numérico continuo | Edad cronológica en años cumplidos | `[15 ... 80]` |
| `grupo_edad` | Categórico ordinal | Sectorización de ciclo vital | `15-24`, `25-34`, `35-44` ... `65+` |
| `area` | Categórico dicotómico| Área geográfica en la que reside el hogar | `Urbana`, `Rural` |
| `dpto` | Categórico | Departamento de subdivisión geopolítica | `Asunción`, `Central`, `San Pedro`, etc. |
| `nivel_edu`| Categórico ordinal | Máximo nivel educativo formal alcanzado | `Básica`, `Media`, `Superior` |
| `quintil_ingreso`| Categórico ordinal | Segmentación de ingresos de toda la muestra en 5 partes | `Q1`(Más pobre) a `Q5` (Más rico) |
| `uso_internet` | Dummie / Binario | (Variable Objetivo) Indica si usó internet (1) o no (0) | `1`, `0` |
| `fex` | Numérico | Factor de expansión. Representa cuántas personas del país 'emula' esa fila encuestada | E.g. `20 - 150` |

*Nota: Para incorporar nuevas columnas, asegúrate de actualizar ambos scripts `py` en el repositorio, o tu frontend no dispondrá del desglose.*
