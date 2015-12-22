-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--

-- Regenerate the DB and connect
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

-- DROP existing tables before re-creating them.
DROP TABLE IF EXISTS players CASCADE;
DROP TABLE IF EXISTS tournaments CASCADE;
DROP TABLE IF EXISTS registry CASCADE;
DROP TABLE IF EXISTS matches CASCADE;

-- CREATE the tables we need;
CREATE TABLE players (
    id          serial PRIMARY KEY,
    name        varchar(20) NOT NULL
);

CREATE TABLE tournaments (
    id          serial PRIMARY KEY,
    name        varchar(20)
);

CREATE TABLE registry (
    player      integer NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    tournament  integer NOT NULL REFERENCES tournaments(id) ON DELETE CASCADE,
    bye         smallint NOT NULL DEFAULT 0,
    CHECK (bye IN (0, 1)), -- Players can have at most 1 bye per tournament
    PRIMARY KEY (tournament, player)
);


-- !! This table has a trigger just after it
CREATE TABLE matches (
    tournament  integer NOT NULL REFERENCES tournaments(id) ON DELETE CASCADE,
    player1     integer NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    player2     integer NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    winner      integer REFERENCES players(id) ON DELETE CASCADE,

    -- a player can't play againts himself
    CHECK (player1 != player2),

    -- the winner must be one of the players that played, or none (draw)
    CHECK (winner = player1 OR winner = player2 OR winner = NULL),

    -- compund key avoids repeating (T+P1+P2), but not inserting (T+P2+P1)
    -- we avoid this second case with the trigger below
    PRIMARY KEY (tournament, player1, player2),

    -- These compound FK make sure players are registered into the tournament
    FOREIGN KEY (tournament, player1) REFERENCES registry(tournament, player),
    FOREIGN KEY (tournament, player2) REFERENCES registry(tournament, player)
);

-- Trigger checks that a match between same players in different order doesn't
-- exist
-- Trigger info: http://www.postgresql.org/docs/9.2/static/plpgsql-trigger.html
CREATE OR REPLACE FUNCTION check_match() RETURNS trigger AS $$
BEGIN
    -- Throw unique key violation if a match between the players, in different
    -- order, alredy exists
    IF EXISTS(SELECT * FROM matches
            WHERE tournament = NEW.tournament
            AND player1=NEW.player2 AND player2=NEW.player1)
        THEN RAISE 'Players % and % already played in tournament %',
            NEW.player2, NEW.player1, NEW.tournament
        USING ERRCODE = 'unique_violation';
    END IF;
    RETURN NEW;
END;
$$ language plpgsql;

CREATE TRIGGER check_match BEFORE INSERT ON matches
    FOR EACH ROW EXECUTE PROCEDURE check_match();


-- VIEWS

-- number of wins by player-tournament
CREATE VIEW playerWins AS
    -- for each player/tournament...
    SELECT
        r.player AS player,
        r.tournament AS tournament,
        (r.bye + COUNT(m)) AS wins
    FROM registry AS r
-- ...match the matches (ha!) he won
-- Note: The left join lets us have rows with 0 wins, whereas an inner
-- join would only output rows with players with at least 1 win.
    LEFT JOIN matches AS m ON
        r.tournament = m.tournament
        AND m.winner = r.player
    GROUP BY player, r.tournament, r.bye
    ORDER BY r.tournament, player;


-- number of games by player-tournament
-- very similar to playerWins = not commented
CREATE VIEW playerGames AS
    SELECT
        r.player AS player,
        r.tournament AS tournament,
        COUNT(m) AS games
    FROM registry AS r
    LEFT JOIN matches as m ON
        r.tournament = m.tournament
        AND (m.player1 = r.player OR m.player2 = r.player)
    GROUP BY player, r.tournament
    ORDER BY r.tournament, player;


-- number of OMW by player-tournament
CREATE VIEW playerOMWs AS
    -- for each player/tournament...
    SELECT
        r.player AS player,
        r.tournament AS tournament,
        COALESCE(SUM(pw.wins), 0) AS omws
        -- note: coalesce puts a 0 when there'd be no pw.wins(sum=null)
    FROM registry AS r
    -- ... get matches where s/he played ...
    LEFT JOIN matches AS m
        ON r.tournament = m.tournament
        AND r.player IN (m.player1, m.player2)
    -- ... and match the opponent,so we SUM its .wins in the SELECT operator
    LEFT JOIN playerWins AS pw
        ON pw.tournament = m.tournament
        AND pw.player IN (m.player1, m.player2)
        AND pw.player != r.player
    GROUP BY r.player, r.tournament
    ORDER BY r.tournament, player;


-- This view just puts together the numbers from the 3 views that extract the
-- number of wins, games and omw.
CREATE VIEW standings AS
SELECT
    r.player as player,
    p.name as name,
    r.tournament AS tournament,
    (SELECT wins FROM playerWins AS pw WHERE
        r.player = pw.player AND r.tournament = pw.tournament) as wins,
    (SELECT games FROM playerGames AS pg WHERE
        r.player = pg.player AND r.tournament = pg.tournament) as games,
    (SELECT omws FROM playerOMWs AS po WHERE
        r.player = po.player AND r.tournament = po.tournament) as omw
FROM registry AS r
INNER JOIN players AS p ON r.player = p.id
ORDER BY
    tournament ASC, -- this order is just for easier human-reading
    wins DESC,
    omw DESC,
    games ASC; -- ASC improves the pairing heurestic (vs DESC) to avoid giving
               -- a player 2 byes
