DROP TABLE IF EXISTS historical_boroughs
CREATE TABLE IF NOT EXISTS historical_boroughs (
    month_id                            VARCHAR(7)   NOT NULL,
    pick_up                    VARCHAR(128)  NOT NULL,
    drop_off					VARCHAR(128)  NOT NULL,
    rank_id								INT           NOT NULL
);