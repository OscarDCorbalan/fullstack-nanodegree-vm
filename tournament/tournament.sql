-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--

-- DROP existing tables before re-creating them.
DELETE FROM matches;
DROP TABLE IF EXISTS players CASCADE;
DROP TABLE IF EXISTS matches;

-- CREATE the tables we need;
CREATE TABLE players (
    id      serial PRIMARY KEY,
    name    varchar(16) NOT NULL
);

CREATE TABLE matches (
    winner      integer NOT NULL REFERENCES players(id),
    loser       integer NOT NULL REFERENCES players(id)
);

INSERT INTO players (name) VALUES
    ('Oscar'),
    ('Tuvok'),
    ('Mary'),
    ('James');

INSERT INTO matches (winner, loser) VALUES
    (1, 2),
    (3, 4),
    (1, 3),
    (2, 4);

--SELECT players.name, (SELECT COUNT(*) FROM matches as m WHERE m.winner = players.id) as wins, (SELECT COUNT(*) FROM matches as m WHERE m.winner=players.id OR m.loser = players.id) FROM players ORDER BY wins DESC;
