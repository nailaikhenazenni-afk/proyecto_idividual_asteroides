import requests

def obtener_gravedad_local(latitud: float, longitud: float, api_key: str) -> dict:
    """
    Consulta la anomalía de gravedad en una ubicación específica usando la API de Amentum.
    
    Args:
        latitud: Latitud en grados decimales.
        longitud: Longitud en grados decimales.
        api_key: Clave de acceso para la API.
        
    Returns:
        Un diccionario con los datos de gravedad o un mensaje de error.
    """
    url: str = 'https://gravity.amentum.io/egm2008/gravity_anomaly'

    # Parámetros con nombres completos para mayor claridad
    params: dict[str, float] = {
        "latitude": latitud,
        "longitude": longitud
    }

    headers: dict[str, str] = {
        "API-Key": api_key,
        "accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        
        # Verificamos si la respuesta es exitosa
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "status": "error",
                "codigo": response.status_code,
                "detalle": response.text
            }
            
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "detalle": f"Error de conexión: {str(e)}"
        }

# --- Ejemplo de uso ---
if __name__ == "__main__":
    # Sustituye con tu API Key real
    MI_API_KEY: str = "tu_api_key_aqui"
    
    # Coordenadas de ejemplo (Monte Everest)
    lat: float = 27.9881
    lon: float = 86.9250
    
    resultado = obtener_gravedad_local(lat, lon, MI_API_KEY)
    
    if "status" in resultado and resultado["status"] == "error":
        print(f"❌ Error al consultar: {resultado['detalle']}")
    else:
        print("✅ Datos de gravedad obtenidos con éxito:")
        print(resultado)

        import pandas as pd
from typing import List

def limpiar_dataset_asteroides(input_file: str, output_file: str) -> None:
    """Carga, limpia y formatea el dataset de asteroides."""
    try:
        df: pd.DataFrame = pd.read_csv(input_file, sep=',')

        # Columnas técnicas e irrelevantes para el análisis de impacto
        columnas_a_eliminar: List[str] = [
            'orbit_id', 'data_arc_days', 'orbit_uncertainty', 'sentry', 'sentry_data', 
            'observations_used', 'jupiter_tisserand', 'epoch', 'eccentricity', 
            'semi_major_axis', 'inclination', 'aphelion_distance', 'perihelion_time', 
            'mean_anomaly', 'neo_id', 'name', 'designation', 'mean_motion', 'equinox', 
            'orbit_class_type', 'orbit_class_desc', 'orbit_class_range', 
            'ascending_node_longitude', 'orbit_determination_date', 
            'perihelion_distance', 'perihelion_argument', 'id', 'api_url'
        ]

        df = df.drop(columns=columnas_a_eliminar, errors='ignore')
        df = df.drop_duplicates()

        if 'short_name' in df.columns:
            df = df.rename(columns={'short_name': 'name'})
        
        df = df.dropna(subset=['name'])

        if 'velocidad_km_s' in df.columns:
            df = df.dropna(subset=['velocidad_km_s'])
            df['velocidad_km_h'] = df['velocidad_km_s'] * 3600

        df.to_csv(output_file, index=False)
        print(f"✅ Archivo '{output_file}' creado con éxito. Shape: {df.shape}")

    except Exception as e:
        print(f"❌ Error en limpieza: {e}")
        
if __name__ == "__main__":
    limpiar_dataset_asteroides('asteroids_data.csv', 'dataset_asteroides_final.csv')
    

    import pandas as pd
import ast
import mysql.connector
from typing import List, Tuple

def cargar_ranking_mysql(input_csv: str) -> None:
    """Extrae datos de aproximación y carga el ranking en MySQL."""
    config = {
        'user': 'root', 'password': 'kP92mXv7R4wQ', 
        'host': '127.0.0.1', 'database': 'asteroides_listo_para_sql'
    }

    try:
        df: pd.DataFrame = pd.read_csv(input_csv)

        def extract_details(row: str) -> pd.Series:
            try:
                data = ast.literal_eval(row)
                if isinstance(data, list) and len(data) > 0:
                    first = data[0]
                    date = first.get('close_approach_date')
                    vel_s = first.get('relative_velocity', {}).get('kilometers_per_second', 0)
                    return pd.Series([date, float(vel_s)])
            except: pass
            return pd.Series([None, 0.0])

        df[['approach_date', 'velocity_km_s']] = df['close_approach_data'].apply(extract_details)
        df['velocity_km_h'] = df['velocity_km_s'] * 3600
        df_sql = df[['name', 'approach_date', 'velocity_km_h']].dropna().copy()
        df_sql = df_sql.sort_values(by='velocity_km_h', ascending=False)

        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        cursor.execute("DROP TABLE IF EXISTS `asteroides_ranking`")
        cursor.execute("""
            CREATE TABLE `asteroides_ranking` (
                `name` VARCHAR(250) PRIMARY KEY,
                `approach_date` DATE,
                `velocity_km_h` FLOAT
            )
        """)

        sql_insert = "INSERT INTO `asteroides_ranking` (name, approach_date, velocity_km_h) VALUES (%s, %s, %s)"
        valores: List[Tuple] = [tuple(x) for x in df_sql.values]
        cursor.executemany(sql_insert, valores)
        conn.commit()
        print(f"✅ Tabla 'asteroides_ranking' cargada. Registros: {len(valores)}")



        import mysql.connector
from typing import List, Dict, Tuple, Any

def gestionar_tabla_gravedad() -> None:
    """
    Crea la base de datos 'gravity' y carga los datos de anomalías gravitatorias
    ordenados de mayor a menor intensidad.
    """
    
    # Datos de entrada obtenidos de la API/Análisis
    gravity_data: List[Dict[str, Any]] = [
        {"nombre": "Monte Everest", "lat": 27.98, "lon": 86.92, "value": 663.1848550445642},
        {"nombre": "Fosa de las Marianas", "lat": 11.37, "lon": 142.59, "value": -318.5888344761341},
        {"nombre": "Ciudad de México", "lat": 19.43, "lon": -99.13, "value": 33.574860133823094},
        {"nombre": "Castellón de la Plana", "lat": 39.9860, "lon": -0.0513, "value": 5.461546490144762},
        {"nombre": "Cuenca de Tanezrouft", "lat": 22.251, "lon": -2.246, "value": -11.470237259214926}
    ]

    config: Dict[str, str] = {
        'user': 'root',
        'password': 'kP92mXv7R4wQ',
        'host': '127.0.0.1'
    }

    try:
        # 1. Conexión inicial
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # 2. Preparación del esquema
        cursor.execute("CREATE DATABASE IF NOT EXISTS gravity")
        cursor.execute("USE gravity")
        print("✅ Base de datos 'gravity' verificada.")

        cursor.execute("DROP TABLE IF EXISTS gravity")
        cursor.execute("""
            CREATE TABLE gravity (
                localization VARCHAR(150),
                latitud FLOAT,
                longitud FLOAT,
                gravity_value FLOAT
            )
        """)
        print("✅ Tabla 'gravity' reiniciada exitosamente.")

        # 3. Procesamiento y Ordenación
        # Ordenamos los datos por valor de gravedad descendente antes de insertar
        gravity_data_sorted = sorted(gravity_data, key=lambda x: x['value'], reverse=True)
        
        sql_insert: str = "INSERT INTO gravity (localization, latitud, longitud, gravity_value) VALUES (%s, %s, %s, %s)"
        
        valores: List[Tuple[str, float, float, float]] = [
            (d['nombre'], d['lat'], d['lon'], d['value']) 
            for d in gravity_data_sorted
        ]

        # 4. Inserción masiva
        cursor.executemany(sql_insert, valores)
        conn.commit()

        print(f"📊 Registros insertados: {len(valores)}")

        # 5. Verificación en consola
        print("\n🌍 RANKING DE ANOMALÍAS GRAVITATORIAS (mGal):")
        print("-" * 50)
        for loc, lat, lon, valor in valores:
            print(f"{loc:25} | Lat: {lat:7.2f} | Lon: {lon:7.2f} | Gravedad: {valor:+.2f} mGal")    

    except Exception as e:
        print(f"❌ Error en SQL: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close(); conn.close()

if __name__ == "__main__":
    cargar_ranking_mysql('dataset_asteroides_final.csv')

    import mysql.connector
from typing import List, Tuple
