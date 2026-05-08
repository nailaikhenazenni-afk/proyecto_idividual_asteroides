# Proyecto: Análisis Impacto Asteroides

# Objetivo

Análisis del impacto de un asteroide considerando su tamaño y velocidad en función de la intensidad gravitatoria de la zona de su posible caída, orientado a la creación de contenido divulgativo, ejemplo: video YouTube.

# API

Gravity API (1.2.0)

Proporciona acceso a las mediciones de las variaciones gravitacionales del planeta.

# Estructura de la Base de Datos

## Dataset

* **Fuente:** **NASA Near-Earth Asteroids Dataset** — registro de los objetos cercanos a la Tierra con sus propiedades orbitales y físicas
* **Registros originales:** 2000 filas × 39 columnas
* **Registros tras limpieza:** 167 filas × 167 columnas
* **Cobertura temporal:** datos recopilados en el año 2026

### Variables principales utilizadas

| Variable |   Tipo             | Descripción |
|`name` |cadena(texto) | nombre del asteroide|
|`magnitude` | FLOAT| mide la magnitud|
|`velocity_km_h` | FLOAT  |mide la velocidad por km/h |
|`close_approach_date`|DATE| fecha en la que el asteroide se acerca a la Tierra |
|`diameter_avg_m` | FLOAT |mide el diámetro medio del asteroide haciendo una media del diámetro máximo y mínimo presentes en el Dataset original|
|`localization` |  cadena(texto)| localización seleccionada |
|`longitude`| FLOAT | coordenada |
|`latitude`| FLOAT | coordenada |
|`gravity_value`| FLOAT| mide la anomalía gravitacional|

## Proceso de Análisis

# Extracción de los datos de la API

Extraemos los valores de gravedad de las localizaciones que seleccionamos introduciendo sus valores de longitude y latitude en la API.

Definimos la función en Python para obtener la gravedad local, luego definimos la lista de 5 puntos de interés en el planeta con sus respectivas coordenadas. Por último, creamos un bucle con if para sacar los valores de gravedad en las distintas localizaciones.

# 1 Limpieza de datos

Carga e inspección del dataset

* Carga e inspección del dataset (`shape`, `info`, `describe`)
* Eliminamos las columnas que no vamos a necesitar
* Identificación de columnas clave y clasificación de variables
* Eliminamos las columnas 'id', 'neo_id', 'name', 'short_name' , 'designation' y reemplazamos por 'name', así solo nos quedamos con los nombres vernaculares ya que son los públicos que la gente recuerda y además suelen ser los más grandes y necesitan un nombre porque los medios los utilizan
* **Nulos:** eliminación de filas sin `name` ni `velocity_km`
* **Duplicados:** `drop_duplicates()` + `reset_index()`
* Sacar los datos enquistados en la columna 'close_approach_data', paso importante y complicado porque allí estaba la velocidad, dato esencial para nuestro análisis
* Sacamos el Dataset en csv, paso importante porque va a ser nuestra base de datos para crear las tablas en SQL

# 2 Creación de las tablas

* Creamos dos tablas en SQL a partir del Dataset limpio:
* Un ranking de los asteroides por dimensión y magnitud absoluta, calculamos el diámetro medio: `diameter_avg_m` a partir del diámetro máximo: 'diameter_max_m' y del diámetro mínimo: 'diameter_min_m' gracias a la función agregada estándar AVG()
* Un ranking de los asteroides por velocidad en km/h: `velocity_km_h` después de haberla convertido de km/s, que incluye también su fecha de aproximación: `close_approach_date`
* Creamos también una tabla con las 5 localizaciones que escogimos con sus respectivas coordenadas y los valores de gravedad que hemos sacado de la API, clasificamos también estos valores por orden descendente.

## Análisis de los datos obtenidos

# Primera fase del análisis

Con los datos obtenidos de las tablas podemos ver el ranking de los asteroides más rápidos y el ranking de los asteroides más masivos, además de visualizar las localizaciones con más y con menos variaciones de la gravedad.

Partimos de estas tablas para realizar 2 **views** para medir y luego comparar el impacto de un asteroide según su velocidad teniendo en cuenta el valor de gravedad en la localización escogida, eligiendo el más rápido (Marsyas), con el impacto del más masivo (Ganymed). Hacemos **join** entre las tablas 'gravity' y 'velocity_ranking' y luego **join** entre las tablas 'gravity' y 'dimension_ranking'.

Formulas de coeficiente de impacto:

velocidad: **ROUND((lider.velocity_km_h / 1000) / (g.gravity_value / 10), 2)**

dimensión: **ROUND((lider.diameter_avg_m) / (g.gravity_value / 10), 2)**

* Fase final del análisis:
  Al comparar los resultados nos damos cuenta de que la dimensión tiene una influencia más significativa sobre el impacto que la velocidad, así que concluimos que será más pertinente para nuestro análisis final escoger el asteroide más masivo (Ganymed). El cual consiste en calcular el valor del impacto basándolo esta vez sobre el valor de gravedad en las 5 localizaciones que hemos elegido previamente, además de la dimensión y la velocidad del asteroide seleccionado.

Hacemos **join** entre las 3 tablas para crear una tabla final para sacar este valor, que hemos creado anteriormente. Utilizamos esta fórmula: **round((l.diameter_avg_m * (l.velocity_km_h / 1000)) + g.gravity_value, 2)**, para una fórmula de fuerza combinada. No solo mide qué tan grande es el asteroide, sino cómo su energía se ve afectada por la gravedad de la Tierra en puntos específicos.

La energía siendo: Energía (`l.diameter_avg_m * (l.velocity_km_h / 1000)`).

La función **round**, aquí sirve para redondear el resultado, limitándolo a 2 decimales.

# Resultados / Insights

* A mayor diámetro, mayor masa y, por tanto, mayor capacidad de daño, Ganymed: 63.0293 km
* La dimensión parece tener más importancia que la velocidad en la fuerza de impacto
* A mayor valor de gravedad, mayor índice de impacto, pero no varía tanto con un índice de 1,431 millones para el Monte Everest que tiene una variación gravitacional de 663.18 y un índice de impacto de 1,430 millones para la Fosa de las Marianas que tiene una variación gravitacional de -318.59.
* Dato sorprendente: ausencia en los tops de los rankings de asteroides famosos como Apophis.

## Próximos Pasos

* Evolucionar los reportes actuales hacia mapas de calor topográficos que permitan visualizar las consecuencias reales en las cinco localizaciones estratégicas seleccionadas.
* Usar datos que no hemos aprovechado del Dataset final como `min_orbit_intersection (MOID)`, que corresponde a la distancia mínima entre la órbita del asteroide y la de la Tierra, lo cual podría servir como filtro para clasificar los asteroides en: "Potencialmente Peligrosos" vs. "Amenazas Teóricas".
* Adaptaremos el análisis de datos a una narrativa visual más dinámica e impactante, utilizando los datos obtenidos para recrear posibles impactos de asteroides sobre la Tierra de una forma creíble, visual y pensada para divulgación.



---

## Cómo Replicar el Proyecto

1. Clona el repositorio:
```bash
git clone https://github.com/nailaikhenazenni-afk/proyecto_idividual_asteroides
```
2. Instala las dependencias:
```bash
pip install pandas matplotlib
```
3. Abre y ejecuta `Notebook.ipynb` en orden desde el Día 1

#Presentación 
https://canva.link/8i9fs3hs6t0b60v




-

 
