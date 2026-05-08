CREATE VIEW VistaImpactoDimension AS
SELECT 
    lider.name,
    lider.diameter_avg_m,
    g.localization,
    g.gravity_value,
    ROUND((lider.diameter_avg_m) / (g.gravity_value / 10), 2) AS impacto_dimension
FROM (
    SELECT name, diameter_avg_m
    FROM dimension_ranking
    ORDER BY diameter_avg_m DESC
    LIMIT 1
) AS lider, 
gravity.gravity AS g
WHERE g.localization IN ('Monte Everest', 'Fosa de las marianas')
LIMIT 5;

CREATE VIEW VistaImpactoVelocidad AS
SELECT 
    lider.name,
    lider.velocity_km_h,
    g.localization,
    g.gravity_value,
    ROUND((lider.velocity_km_h / 1000) / (g.gravity_value / 10), 2) AS impacto_velocidad
FROM (
    SELECT name, velocity_km_h
    FROM asteroides_ranking
    ORDER BY velocity_km_h DESC
    LIMIT 1
) AS lider, 
gravity.gravity AS g
WHERE g.localization IN ('Monte Everest', 'Fosa de las marianas')
LIMIT 5;


        