-- 1. Crear la tabla física para almacenar el análisis
CREATE TABLE analisis_impacto_unificado AS
WITH lider AS (
    SELECT 
        a.name, 
        d.diameter_avg_m,
        a.velocity_km_h
    FROM asteroides_ranking a
    JOIN dimension_ranking d ON a.name = d.name
    ORDER BY d.diameter_avg_m DESC, a.velocity_km_h DESC
    LIMIT 1
)
SELECT 
    l.name,
    l.diameter_avg_m,
    l.velocity_km_h,
    g.localization,
    g.gravity_value,
    ROUND((l.diameter_avg_m * (l.velocity_km_h / 1000)) + g.gravity_value, 2) AS impacto
FROM gravity.gravity g
JOIN lider l ON 1=1
ORDER BY g.gravity_value DESC; -- Orden descendente por gravedad