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
    player1     integer NOT NULL REFERENCES players(id),
    player2     integer NOT NULL REFERENCES players(id),
    winner      integer NOT NULL REFERENCES players(id)
);

INSERT INTO players (name) VALUES
    ('Oscar'),
    ('Tuvok'),
    ('Mary'),
    ('James');

INSERT INTO matches (player1, player2, winner) VALUES
    (1, 2, 1),
    (3, 4, 3),
    (1, 3, 1),
    (2, 4, 2);
