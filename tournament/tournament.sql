-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--

-- DROP existing tables before re-creating them.
DROP TABLE IF EXISTS players CASCADE;
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS byes;

-- CREATE the tables we need;
CREATE TABLE players (
    id      serial PRIMARY KEY,
    name    varchar(20) NOT NULL
);

CREATE TABLE matches (
    winner      integer NOT NULL REFERENCES players(id),
    loser       integer NOT NULL REFERENCES players(id),
    CHECK (winner != loser),
    PRIMARY KEY (winner, loser)
); -- plus check the trigger on this table at the bottom


-- The UNIQUE prevents more than one bye per player
CREATE TABLE byes (
    player      integer UNIQUE NOT NULL REFERENCES players(id)
);

CREATE VIEW standings AS
    SELECT
        players.id,
        players.name,
        (SELECT COUNT(*) FROM matches WHERE matches.winner = players.id) --real
        + (SELECT COUNT(*) FROM byes WHERE byes.player = players.id)     --bye
            as wins,
        (SELECT COUNT(*) FROM matches
            WHERE matches.winner = players.id OR matches.loser = players.id)
            as games,
        (SELECT COUNT(*) FROM byes WHERE byes.player = players.id)
            as bye --not needed but useful
    FROM players
    ORDER BY
        wins DESC,
        games DESC;

-- TRIGGERS

-- Checks that a match between same players with different result does not exist
-- Trigger info: http://www.postgresql.org/docs/9.2/static/plpgsql-trigger.html
CREATE OR REPLACE FUNCTION check_inverse_match() RETURNS trigger AS $$
BEGIN
    IF EXISTS(SELECT * FROM matches WHERE winner=NEW.loser AND loser=NEW.winner)
        THEN RAISE 'Key (winner, loser)=(%, %) already exists', NEW.loser, NEW.winner
        USING ERRCODE = 'unique_violation';
    END IF;
    RETURN NEW;
END;
$$ language plpgsql;

CREATE TRIGGER check_inverse_match BEFORE INSERT ON matches
    FOR EACH ROW EXECUTE PROCEDURE check_inverse_match();
