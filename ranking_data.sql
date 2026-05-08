CREATE TABLE `asteroides_ranking` (
    `name` VARCHAR(250) NOT NULL,
    `approach_date` DATE NOT NULL,
    `velocity_km_h` FLOAT NOT NULL,
    PRIMARY KEY (`name`)
);
SELECT COUNT(*) FROM asteroides_ranking;