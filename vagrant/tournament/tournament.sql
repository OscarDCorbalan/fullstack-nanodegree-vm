-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--

-- DROP existing tables before re-creating them.
DROP TABLE IF EXISTS players CASCADE;
DROP TABLE IF EXISTS matches;

-- CREATE the tables we need;
CREATE TABLE players (
    id      serial PRIMARY KEY,
    name    varchar(16) NOT NULL
);

CREATE TABLE matches (
    winner      integer NOT NULL REFERENCES players(id),
    loser       integer NOT NULL REFERENCES players(id),
    CHECK (winner != loser), -- winner and loser can't be the same player
    CHECK (winner > 0),
    PRIMARY KEY (winner, loser)
);

--
-- http://www.postgresql.org/docs/9.2/static/plpgsql-trigger.html
CREATE OR REPLACE FUNCTION check_inverse_match() RETURNS trigger AS $$
BEGIN
    IF EXISTS(SELECT * FROM matches WHERE winner=NEW.loser AND loser=NEW.winner)
        THEN RAISE 'Key (winner, loser)=(%, %) already exists', NEW.winner, NEW.loser
        USING ERRCODE = 'unique_violation';
    END IF;
    RETURN NEW;
END;
$$ language plpgsql;

CREATE TRIGGER check_inverse_match BEFORE INSERT ON matches
    FOR EACH ROW EXECUTE PROCEDURE check_inverse_match();

CREATE VIEW standings AS
    SELECT
        players.id,
        players.name,
        (SELECT COUNT(*) FROM matches
            WHERE matches.winner = players.id)
            as wins,
        (SELECT COUNT(*) FROM matches
            WHERE matches.winner = players.id OR matches.loser = players.id)
            as games
    FROM players
    ORDER BY
        wins DESC,
        games DESC;
