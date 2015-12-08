#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import bleach
import psycopg2
from itertools import imap

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def execute(query, values):
    # Connect to the database and open a cursor to perform the operation
    conn = connect()
    cursor = conn.cursor()

    # Execute the command, bleaching the passed values (f any)
    if values is None:
        cursor.execute(query)
    else:
        for value in values:
            value = bleach.clean(value)
        cursor.execute(query, values)

    # Make the changes persistent
    conn.commit()

    # Close communication with the database
    cursor.close()
    conn.close()

def fetch(query, values, singlerow = False):
    # Connect to the database and open a cursor to perform the operation
    conn = connect()
    cursor = conn.cursor()

    # Execute the command, bleaching the passed values (f any)
    if values is None:
        cursor.execute(query)
    else:
        for value in values:
            value = bleach.clean(value)
        cursor.execute(query, values)

    # Get the results of the query
    if singlerow:
        rows = cursor.fetchone()
    else:
        rows = cursor.fetchall()

    # Close communication with the database
    cursor.close()
    conn.close()

    return rows

def deleteMatches():
    """Remove all the match records from the database."""
    query = "DELETE FROM matches;"
    execute(query, None)

def deletePlayers():
    """Remove all the player records from the database."""
    query = "DELETE FROM players;"
    execute(query, None)


def countPlayers():
    """Returns the number of players currently registered."""
    query = "SELECT COUNT(*) FROM players";
    return fetch(query, None, True)[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    query = "INSERT INTO players (name) VALUES (%s);"
    execute(query, [name])

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    query = "SELECT * FROM standings;"
    rows = fetch(query, None)
    return [(
            int(row[0]),
            str(bleach.clean(row[1])),
            int(row[2]),
            int(row[3])
            ) for row in rows]

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.


    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    # Just do the insert, as the DB will raise an error if the match exists
    query = "INSERT INTO matches (winner, loser) VALUES (%s, %s);"
    execute(query, [winner, loser])


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    query = "SELECT id, name FROM standings;"
    rows = fetch(query, None)
    #           id1         name1       id2         name2
    return [(pair[0][0], pair[0][1], pair[1][0], pair[0][1])
        for pair in group2(rows)]

def group2(iterator, count = 2):
    """ Returns the list in groups of count elements: s -> (s0,s1), (s2,s3), ...

    Extracted from:
    http://code.activestate.com/recipes/439095-iterator-to-return-items-n-at-a-time/
    """
    return imap(None, *([ iter(iterator) ] * count))
