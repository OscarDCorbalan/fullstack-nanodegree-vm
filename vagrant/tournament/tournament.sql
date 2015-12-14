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
    player1     integer NOT NULL REFERENCES players(id),
    player2     integer NOT NULL REFERENCES players(id),
    winner      integer REFERENCES players(id),
    CHECK (player1 != player2),
    CHECK (winner = player1 OR winner = player2 OR winner = NULL),
    PRIMARY KEY (player1, player2)
); -- plus check the trigger on this table at the bottom


-- The UNIQUE prevents more than one bye per player
CREATE TABLE byes (
    player      integer UNIQUE NOT NULL REFERENCES players(id)
);


-- VIEWS

-- number of wins by player
CREATE VIEW playerWins AS
    SELECT players.id as id,
        -- sum real wins and bye, if any
        (SELECT COUNT(*) FROM matches WHERE matches.winner = players.id)
        + (SELECT COUNT(*) FROM byes WHERE byes.player = players.id)
        as wins
    FROM players;

-- number of games by player
CREATE VIEW playerGames AS
    SELECT players.id as id,
    (SELECT COUNT(*) FROM matches
        WHERE matches.player1 = players.id OR matches.player2 = players.id)
        as games
    FROM players;

-- number of OMW by player
CREATE VIEW playerOMWs AS
    SELECT
        m.winner AS id,
        SUM(wins) AS omws
    FROM matches AS m
    LEFT JOIN playerWins AS pw
    ON pw.id IN (m.player1, m.player2) AND pw.id != m.winner
    GROUP BY m.winner;

CREATE VIEW standings AS
SELECT
    players.id as id,
    players.name as name,
    (SELECT wins from playerWins WHERE players.id = playerWins.id) as wins,
    (SELECT games from playerGames WHERE players.id = playerGames.id) as games,
    COALESCE( -- there's no row when a player has omw=0, so default it to 0
        (SELECT omws from playerOMWs WHERE players.id = playerOMWs.id), 0
    ) as omw
FROM players
ORDER BY
    wins DESC,
    omw DESC,
    games DESC;


-- TRIGGERS

-- Checks that a match between same players with different result does not exist
-- Trigger info: http://www.postgresql.org/docs/9.2/static/plpgsql-trigger.html
CREATE OR REPLACE FUNCTION check_inverse_match() RETURNS trigger AS $$
BEGIN
    IF EXISTS(SELECT *
            FROM matches
            WHERE player1=NEW.player2
            AND player2=NEW.player1)
        THEN RAISE 'Key (player1, player2)=(%, %) already exists',
            NEW.player2, NEW.player1
        USING ERRCODE = 'unique_violation';
    END IF;
    RETURN NEW;
END;
$$ language plpgsql;

CREATE TRIGGER check_inverse_match BEFORE INSERT ON matches
    FOR EACH ROW EXECUTE PROCEDURE check_inverse_match();
