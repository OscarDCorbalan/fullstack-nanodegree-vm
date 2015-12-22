#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import bleach
import psycopg2


# The following functions implement reusable code to interact with the DB.

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def execute(query, values, returning = False):
    """Does an Insert or an Update into the database.

    This function helps to avoid repeating code and ensures we don't forget
    to bleach any field that goes into the database.

    Args:
        query: insert or update to execute
        values: array with the values that go into the query
        returning: whether the query has a Returning operator

    Returns:
        If and only if returning=True, returns the value of the Returning
        operator. When returning=False, doesn't return anything
    """
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

    if returning:
        value = cursor.fetchone()[0]

    # Make the changes persistent
    conn.commit()

    # Close communication with the database
    cursor.close()
    conn.close()

    # Return the result of the Returning operator
    if returning:
        return value

def fetchone(query, values):
    """Alias to call the fetch function when we want only 1 resulting row"""
    return fetch(query, values, True)

def fetch(query, values, singlerow = False):
    """Does a SELECT or COUNT to the database.

    This function helps to avoid repeating code and ensures we don not forget
    to bleach any field.

    Args:
        query: select or count to execute
        values: array with the values that go into the query
        singlerow: whether we want only one row or an arbitrary number

    Returns:
        The result of the query. If singlerow=True, returns only the first
        matched row.
    """
    # Connect to the database and open a cursor to perform the operation
    conn = connect()
    cursor = conn.cursor()

    # Execute the command, bleaching the passed values (if any)
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

    # Close communication with the database and return the result
    cursor.close()
    conn.close()
    return rows


# The following functions clean tables from the DB.

def deletePlayers():
    """Remove all the player records from the database."""
    query = "DELETE FROM players;"
    execute(query, None)

def deleteTournaments():
    """Remove all the tournament records from the database."""
    query = "DELETE FROM tournaments;"
    execute(query, None)

def deleteRegistry():
    """Remove all the registry records from the database."""
    query = "DELETE FROM registry;"
    execute(query, None)

def deleteMatches():
    """Remove all the match records from the database."""
    query = "DELETE FROM matches;"
    execute(query, None)


# The following functions count elements in tables.

def countPlayers():
    """Counts the number of players currently registered.

    Returns:
        The number of players currently registered.
    """
    query = "SELECT COUNT(*) FROM players";
    return fetch(query, None, True)[0]

def countTournaments():
    """Counts the number of tournaments currently registered.

    Returns:
        The number of tournaments currently registered.
    """
    query = "SELECT COUNT(*) FROM tournaments";
    return fetch(query, None, True)[0]


# The following functions register (insert/update) things in the DB.

def registerPlayer(name):
    """Adds a player to the players database.

    The database assigns a unique serial id number for the player.

    Args:
        name: the player's full name (need not be unique).

    Returns:
        The id of the player created.
    """
    query = "INSERT INTO players (name) VALUES (%s) RETURNING id;"
    return execute(query, [name], True)

def registerTournament(name):
    """Adds a tournament to the tournaments database.

    The database assigns a unique serial id number for the tournament.

    Args:
        name: the tournaments's name.

    Returns:
        The id of the tournament created.
    """
    query = "INSERT INTO tournaments (name) VALUES (%s) RETURNING id;"
    return execute(query, [name], True)

def registerEntry(player, tournament):
    """Adds a player to a tournament.

    The DB controls that both player and tournament exist via Foreign Keys.

    Args:
        player: the id of the player
        tournament: the id of the tournament
    """
    query = "INSERT INTO registry (player, tournament) VALUES (%s, %s);"
    execute(query, [player, tournament])

def reportMatch(tournament, player1, player2, winner):
    """Records the outcome of a single match between two players.

    The DB will raise an error if the winner is not one of the players, or they
    already matched, or if they're not registered in the tournament.

    Args:
        tournament: the id of the tournament
        player1: the id number of one of the players
        player2: the id number of the other player
        winner:  the id number of the player who won, or None if a draw
    """
    query = """
        INSERT INTO matches(tournament, player1, player2, winner)
        VALUES(%s, %s, %s, %s);
    """
    execute(query, [tournament, player1, player2, winner])

def assignBye(tournament, player):
    """Assigns a bye to a player (a bye counts as a free win).

    The DB controls that a player doesn't receive more than one bye in a
    tournament.

    Args:
        tournament: the id of the tournament
        player: the id number of the players
    """
    # We do a 'bye+1' to get an error from the DB in case the pairing algorithm
    # leaves the same player a second time without a match.
    # A bye=1 would work fine, but then that error would be silenced/missed.
    query = "UPDATE registry SET bye=bye+1 WHERE tournament=%s AND player=%s;"
    execute(query, [tournament, player])


# The following functions read (select) info from the database.

def playerStandings(tournament):
    """Returns, for the given tournament, a list of the players and their win
    records, sorted by wins, then omw, then number of games.

    The first entry in the list is the player in first place, or a player tied
    for first place if there is currently a tie.

    Args:
        tournament: the id of the tournament

    Returns:
        A list of tuples, each of which contains (id, name, wins, matches, omw):
            id: the player's unique id (assigned by the database).
            name: the player's full name (as registered).
            wins: the number of matches the player has won.
            matches: the number of matches the player has played.
            omw: opponent match wins, #wins by players they have played against.
    """
    query = """
        SELECT player, name, wins, games, omw
        FROM standings as s
        WHERE s.tournament = %s;
    """
    rows = fetch(query, [tournament])
    return [(
            int(row[0]),
            str(bleach.clean(row[1])),
            int(row[2]),
            int(row[3]),
            int(row[4])
            ) for row in rows]

def swissPairings(tournament):
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    When there is an odd number of players, the last one is granted a free bye
    instead of being paired with another player to play with.

    Args:
        tournament: the id of the tournament

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    query = """
        SELECT player, name, wins, games
        FROM standings WHERE tournament = %s;
    """
    rows = fetch(query, [tournament])

    # Assign a bye to last player if number of players is odd
    if len(rows) % 2 != 0:
        lastPlayer = rows[-1]
        del rows[-1] # remove it from the list
        assignBye(tournament, lastPlayer[0])

    # Return the matching pairs
    return pairs(tournament, rows)

def playedAgainst(tournament, player1, player2):
    """Checks if two players have already played against each other in the given
    tournament.

    Args:
        tournament: the id of the tournament.
        player1: the id number of one of the players.
        player2: the id number of the other player.

    Returns:
        True if the players already matched, False if not.
    """
    # "Trick" to get a true/false result from the DB, extracted from:
    # http://www.postgresql.org/docs/current/interactive/functions-subquery.html#FUNCTIONS-SUBQUERY-EXISTS
    query = """
        SELECT EXISTS(
            SELECT 1 FROM matches WHERE
            tournament = %s
            AND player1 IN (%s, %s)
            AND player2 IN (%s, %s)
        );
        """
    row = fetch(query, [tournament, player1, player2, player2, player1], True)
    return row[0]

def pairs(tournament, players):
    """Pairs the players avoiding match repetitions; that is, two players can
    only play once versus the other in the same tournament.

    The pairing heuristic is O(n log(n)) and is variation of heapsort (see:
    https://en.wikipedia.org/wiki/Heapsort). In concrete, the algorithm used
    is (example with a list of 6 players):
    0) Given an input list, create an empty pairs list.
        players = [A,B,C,D,E,F]
        pairs = []
    1) While players is not empty, get the first player (highest standing) of
    the current list:
        first = A
    2) Starting at players[1] (second player of the players list), linearly
    search (that is, from highest to lowest score) for a player that hasn't
    played against first:
        first = A
        i = 1  [A,-->B<--,C,D,E,F]   (example: already played)
        i = 2  [A,B,-->C<--,D,E,F]   (example: already played)
        i = 3  [A,B,C,-->D<--,E,F]   (example: match!)
    3) Add the two players to the pairs list, and remove them from players list
        pairs = [{A,D}]
        players = [B,C,E,F]
    4) Go to 1.

    Args:
        tournament: id of the tournament for which we're grouping players.
        players: list of players to match. The list must be even: to accept odd
        lists, the function should return the pairs plus the remaining player.

    Returns:
        A list of the paired players for the next round of matches.
    """
    # The numbers in the comments refer to the algorithm steps explained in
    # the function description.

    pairs = []                                          # 0
    i = 0
    while i < len(players):                             # 1
        p = players[i]                                  # 1

        i = i + 1                                       # 2
        for j in range(i, len(players)):                # 2
            q = players[j]                              # 2
            if playedAgainst(tournament, p[0], q[0]):   # 2
                continue                                # 2

            players.remove(p)                           # 3
            players.remove(q)                           # 3
            #            ( id1, name1, id2, name2)
            pairs.append((p[0], p[1], q[0], q[1]))      # 3

            i = 0                                       # 4
            break;                                      # 4
    return pairs
