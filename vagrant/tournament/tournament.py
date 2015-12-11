#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import bleach
import psycopg2

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

def deleteByes():
    """Remove all the bye records from the database."""
    query = "DELETE FROM byes;"
    execute(query, None)

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

def reportMatch(player1, player2, winner):
    """Records the outcome of a single match between two players.

    Args:
      player1: the id number of one of the players
      player2: the id number of the other player
      winner:  the id number of the player who won, or None if a draw
    """
    # Just do the insert, as the DB will raise an error if the match exists
    query = "INSERT INTO matches(player1, player2, winner) VALUES(%s, %s, %s);"
    execute(query, [player1, player2, winner])


def playedAgainst(player1, player2):
    query = """
        SELECT * FROM matches WHERE
        (player1 = %s AND player2 = %s) OR (player2 = %s AND player1 = %s);
        """
    return fetch(query, [player1, player2, player2, player1], True) is not None


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
    query = "SELECT id, name, wins, games FROM standings;"
    rows = fetch(query, None)

    # Assign a bye to last player if number of players is odd
    if len(rows) % 2 != 0:
        lastPlayer = rows[-1]
        del rows[-1] # remove it from the list
        assignBye(lastPlayer[0])
        # Uncomment to test we can't assign 2 byes to same player:
        #assignBye(lastPlayer[0])
    return group(rows)

def assignBye(idPlayer):
    query = "INSERT INTO byes (player) VALUES (%s);"
    execute(query, [idPlayer])

def group(players):
    pairs = []
    i = 0
    while i < len(players):
        p = players[i]
        i = i + 1
        for j in range(i, len(players)):
            q = players[j]
            if not playedAgainst(p[0], q[0]):
                players.remove(p)
                players.remove(q)
                #              id1, name1, id2, name2
                pairs.append((p[0], p[1], q[0], q[1]))
                i = 0
                break;
    return pairs
