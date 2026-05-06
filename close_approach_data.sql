/* 1. Selección de la base de datos */
USE `asteroides_listo_para_sql`;

/* 2. Limpieza de la tabla anterior */
DROP TABLE IF EXISTS `asteroides_ranking`;

/* 3. Creación de la tabla con la estructura limpia de Python */
CREATE TABLE `asteroides_ranking` (
    `nombre_asteroide` VARCHAR(250) PRIMARY KEY,
    `fecha_acercamiento` DATE,
    `velocidad_km_s` FLOAT,
    `potentially_hazardous` VARCHAR(10),
    `orbiting_body` VARCHAR(50) DEFAULT 'Earth'
);

/* 4. EL RANKING: Consulta para el video */
/* Esta consulta filtra por la Tierra y ordena los más rápidos primero */
SELECT 
    `nombre_asteroide`, 
    `velocidad_km_s`, 
    `fecha_acercamiento`
FROM `asteroides_ranking`
WHERE `orbiting_body` = 'Earth'
ORDER BY `velocidad_km_s` DESC
LIMIT 10; -- Muestra el Top 10 de los más rápidos
