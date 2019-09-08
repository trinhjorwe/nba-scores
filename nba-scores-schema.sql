DROP SCHEMA IF EXISTS nba;
CREATE SCHEMA nba;
USE nba;

CREATE TABLE IF NOT EXISTS points (
	date DATE,
    game_id TINYINT,
    team CHAR(30),
    quarter TINYINT,
    points SMALLINT,
    homeAway CHAR(30),
    PRIMARY KEY (date, game_id, team, quarter)
) ENGINE=INNODB;

	
