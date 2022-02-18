DROP TABLE IF EXISTS historical_zones
CREATE TABLE IF NOT EXISTS historical_zones (
    month_id                            VARCHAR(7)   NOT NULL,
    pick_up                        VARCHAR(128)  NOT NULL,
    drop_off		    			VARCHAR(128)  NOT NULL,
    rank_id								INT           NOT NULL
);

