import pandas as pd
import numpy as np
import json
import os
import statsmodels.api as sm

def weighted_mean(df, value_col, weight_col):
    """Calcula la media ponderada."""
    try:
        if df[weight_col].sum() == 0:
            return 0
        return float(np.average(df[value_col], weights=df[weight_col]))
    except:
        return 0

def procesar_datos(input_path="data_raw/encuesta_mock.csv", output_path="assets/data/dashboard_data.json"):
    print("Leyendo datos crudos...")
    if not os.path.exists(input_path):
        print(f"Error: No se encontro el archivo {input_path}")
        return
        
    df = pd.read_csv(input_path, sep=";")
    
    # 1. Indicadores Generales (Global)
    total_poblacion = float(df['fex'].sum())
    pob_internet = float(df[df['uso_internet'] == 1]['fex'].sum())
    tasa_global = pob_internet / total_poblacion if total_poblacion > 0 else 0
    
    # KPIs
    kpis = {
        "tasa_global": round(tasa_global * 100, 1),
        "total_usuarios": int(pob_internet),
        "total_poblacion": int(total_poblacion),
        "brecha_urb_rur": 0 # Se calcula abajo
    }
    
    # 2. Desagregaciones (Brechas)
    def calc_agregado(variable):
        agregado = []
        for valor, grupo in df.groupby(variable):
            pob = grupo['fex'].sum()
            uso = grupo[grupo['uso_internet'] == 1]['fex'].sum()
            tasa = uso / pob if pob > 0 else 0
            agregado.append({
                "categoria": str(valor),
                "tasa": round(float(tasa) * 100, 1),
                "poblacion": int(pob)
            })
        # Ordenar por tasa descendente excepto si es grupo de edad o quintil
        if variable not in ['grupo_edad', 'quintil_ingreso', 'nivel_edu']:
            agregado.sort(key=lambda x: x['tasa'], reverse=True)
        return agregado

    brechas = {
        "sexo": calc_agregado('sexo'),
        "area": calc_agregado('area'),
        "nivel_edu": calc_agregado('nivel_edu'),
        "quintil_ingreso": calc_agregado('quintil_ingreso'),
        "grupo_edad": calc_agregado('grupo_edad'),
        "dpto": calc_agregado('dpto')
    }
    
    # Calcular brecha urbana / rural para KPI
    tasa_urbana = next((x['tasa'] for x in brechas['area'] if x['categoria'] == 'Urbana'), 0)
    tasa_rural = next((x['tasa'] for x in brechas['area'] if x['categoria'] == 'Rural'), 0)
    kpis["brecha_urb_rur"] = round(tasa_urbana - tasa_rural, 1)

    # 3. Datos para pirámide o cruces (Edad promedio por uso)
    edad_promedio_usuarios = weighted_mean(df[df['uso_internet']==1], 'edad', 'fex')
    edad_promedio_no_usuarios = weighted_mean(df[df['uso_internet']==0], 'edad', 'fex')
    
    perfil_demografico = {
        "edad_promedio": {
            "usuarios": round(edad_promedio_usuarios, 1),
            "no_usuarios": round(edad_promedio_no_usuarios, 1)
        }
    }

    # 4. Modelo Logístico (Determinantes)
    print("Ajustando modelo logístico (Regresión)...")
    df_model = df.copy()
    # Crear dummies
    df_model['Mujer'] = (df_model['sexo'] == 'Mujer').astype(int)
    df_model['Urbana'] = (df_model['area'] == 'Urbana').astype(int)
    df_model['Edu_Media'] = (df_model['nivel_edu'] == 'Media').astype(int)
    df_model['Edu_Superior'] = (df_model['nivel_edu'] == 'Superior').astype(int)
    
    # Quintiles como ordinal o numérico simple para el modelo
    q_map = {'Q1': 1, 'Q2': 2, 'Q3': 3, 'Q4': 4, 'Q5': 5}
    df_model['Quintil_Num'] = df_model['quintil_ingreso'].map(q_map)

    # Ecuación: Uso_internet ~ Mujer + Urbana + Edad + NivelEdu + Quintil
    X_cols = ['Mujer', 'Urbana', 'edad', 'Edu_Media', 'Edu_Superior', 'Quintil_Num']
    X = df_model[X_cols]
    X = sm.add_constant(X)
    y = df_model['uso_internet']
    
    # Pesos (usamos GLM con freq_weights si es exacto, pero para simplificar usamos Logit con weights=fex es experimental, usamos Logit estandar como aproximacion para Odds Ratios direccionales)
    # Statmodels GLM soporta weights
    try:
        modelo = sm.GLM(y, X, family=sm.families.Binomial(), freq_weights=df_model['fex'])
        res = modelo.fit()
        
        # Calcular Odds Ratios
        odds_ratios = np.exp(res.params).round(2)
        pvalues = res.pvalues.round(4)
        
        # Formatear para frontend
        factores = []
        labels_map = {
            'Mujer': 'Ser Mujer (vs Hombre)',
            'Urbana': 'Residir en Área Urbana (vs Rural)',
            'edad': 'Edad (por cada año adicional)',
            'Edu_Media': 'Educación Media (vs Básica)',
            'Edu_Superior': 'Educación Superior (vs Básica)',
            'Quintil_Num': 'Aumento de 1 Quintil de Ingreso'
        }
        
        for col in X_cols:
            factores.append({
                "variable": labels_map.get(col, col),
                "odds_ratio": float(odds_ratios[col]),
                "p_valor": float(pvalues[col]),
                "significativo": bool(pvalues[col] < 0.05)
            })
            
        # Ordenar por impacto (Odds Ratio)
        factores.sort(key=lambda x: x['odds_ratio'], reverse=True)
        
        modelo_res = {
            "status": "success",
            "factores": factores
        }
    except Exception as e:
        print(f"Error en modelo: {e}")
        modelo_res = {"status": "error", "mensaje": str(e)}

    # Consolidar JSON final
    dashboard_data = {
        "metadata": {
            "fuente": "Encuesta Mock Generada",
            "universo": "Población de 15 a 80 años",
            "fecha_actualizacion": pd.Timestamp.now().strftime("%Y-%m-%d")
        },
        "kpis": kpis,
        "brechas": brechas,
        "perfil_demografico": perfil_demografico,
        "modelo": modelo_res
    }

    # Guardar archivo
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(dashboard_data, f, ensure_ascii=False, indent=2)
        
    print(f"Datos procesados y guardados en {output_path}")

if __name__ == "__main__":
    procesar_datos()
