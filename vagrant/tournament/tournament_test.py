#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *

def resetTables():
    # Since the point where we support multiple tournaments, there's no longer
    # the need to reset the tables. So we can eitehr comment or uncomment the
    # following lines.
    #deleteRegistry()
    #deleteMatches()
    #deleteTournaments() We support multiple tournaments, so no need to reset!
    #deletePlayers()
    pass

def testDeleteMatches():
    deleteMatches()
    print "1. Old matches can be deleted."


def testDelete():
    deletePlayers()
    print "2. Player records can be deleted."


def testCount():
    deletePlayers()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."


def testRegister():
    deletePlayers()
    registerPlayer("Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete():
    deletePlayers()
    registerPlayer("Markov Chaney")
    registerPlayer("Joe Malik")
    registerPlayer("Mao Tsu-hsi")
    registerPlayer("Atlanta Hope")

    c = countPlayers()
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."


def testStandingsBeforeMatches():
    resetTables()
    pid1 = registerPlayer("Melpomene Murray")
    pid2 = registerPlayer("Randy Schwartz")
    tid = registerTournament("Test Before Matches")
    registerEntry(pid1, tid)
    registerEntry(pid2, tid)
    standings = playerStandings(tid)
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 5:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1, omw1),
        (id2, name2, wins2, matches2, omw2)] = standings

    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings,"
                         " even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."


def testReportMatches():
    resetTables()
    tid = registerTournament("Test Reporting")

    registerEntry( registerPlayer("Bruno Walton"), tid )
    registerEntry( registerPlayer("Boots O'Neal"), tid )
    registerEntry( registerPlayer("Cathy Burton"), tid )
    registerEntry( registerPlayer("Diane Grant"), tid )

    standings = playerStandings(tid)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(tid, id1, id2, id1)
    reportMatch(tid, id3, id4, id3)

    standings = playerStandings(tid)
    for (i, n, w, m, o) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings."


def testPairings():
    resetTables()
    tid = registerTournament("Test Pairings")
    registerEntry( registerPlayer("Twilight Sparkle"), tid )
    registerEntry( registerPlayer("Fluttershy"), tid )
    registerEntry( registerPlayer("Applejack"), tid )
    registerEntry( registerPlayer("Pinkie Pie"), tid )

    standings = playerStandings(tid)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(tid, id1, id2, id1)
    reportMatch(tid, id3, id4, id3)

    pairings = swissPairings(tid)
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "8. After one match, players with one win are paired."


def testRematches():
    resetTables()
    tid = registerTournament("Test Rematches")
    registerEntry( registerPlayer("Shaquille O'Neal"), tid )
    registerEntry( registerPlayer("Michael Jordan"), tid )

    [id1, id2] = [row[0] for row in playerStandings(tid) ]
    reportMatch(tid, id1, id2, id1)
    try:
        reportMatch(tid, id1, id2, id1)
    except psycopg2.IntegrityError:
        try:
            reportMatch(tid, id2, id1, id2)
        except psycopg2.IntegrityError:
            print "9. Rematches between players are not allowed."
    else:
        raise ValueError(
            "Rematches between players are allowed.")


def testOddPlayers():
    resetTables()
    tid = registerTournament("Test Odd #Players")
    registerEntry( registerPlayer("Lionel Messi"), tid)
    registerEntry( registerPlayer("Cristiano Ronaldo"), tid)
    registerEntry( registerPlayer("Arjen Robben"), tid)
    registerEntry( registerPlayer("Zlatan Ibrahimovic"), tid)
    registerEntry( registerPlayer("Franz Beckenbauer"), tid)
    registerEntry( registerPlayer("Andres Iniesta"), tid)
    registerEntry( registerPlayer("James Rodriguez"), tid)
    registerEntry( registerPlayer("Manuel Neuer"), tid)
    registerEntry( registerPlayer("Andres Iniesta"), tid)

    firstRound = True;
    # Any second bye to the same player would throw a duplicate key error
    for round in range(1, 3):
        [(id1, name1, id2, name2), (id3, name3, id4, name4),
        (id5, name5, id6, name6), (id7, name7, id8, name8)] = swissPairings(tid)

        # In 1st round he's the first since no one else still reported a match
        if firstRound:
            firstRound = False
            last = playerStandings(tid)[0]
            if last[1] != "Andres Iniesta":
                raise ValueError("Last player didn't get a bye.")

        reportMatch(tid, id1, id2, id1)
        reportMatch(tid, id3, id4, id3)
        reportMatch(tid, id5, id6, id5)
        reportMatch(tid, id7, id8, id7)

    print "10. With odd #players, last receives a bye and no one receives 2+."


def testDraws():
    resetTables()
    tid = registerTournament("Test Draws")
    registerEntry( registerPlayer("Pencil"), tid)
    registerEntry( registerPlayer("Rubber"), tid)

    [id1, id2] = [row[0] for row in playerStandings(tid)]
    reportMatch(tid, id1, id2, None)

    [(id1, name1, wins1, games1, omw1),
    (id2, name2, wins2, games2, omw2)] = playerStandings(tid)

    if wins1 == 1 or wins2 == 1:
        raise ValueError("Draws shouldn't count as a win.")
    if games1 == 0 or games2 == 0:
        raise ValueError("Draws should count as a played game.")

    print "11. Matches can result in a draw."

def testOpponentMatchWins():
    resetTables()
    tid = registerTournament("Test OMWs")
    registerEntry( registerPlayer("P1"), tid)
    registerEntry( registerPlayer("P2"), tid)
    registerEntry( registerPlayer("P3"), tid)
    registerEntry( registerPlayer("P4"), tid)

    # Round 1, check winners end with omw=0, and losers with omw=1
    [(id1, name1, id2, name2), (id3, name3, id4, name4)] = swissPairings(tid)
    reportMatch(tid, id1, id2, id1)
    reportMatch(tid, id3, id4, id3)
    if [0, 0, 1, 1] != [row[4] for row in playerStandings(tid)]:
        raise ValueError("Bad OMW count. Correct is [P1,P2,P3,P4]=[0,0,1,1].")

    # Round 2, everyone ends with 2 omws
    [(id1, name1, id2, name2), (id3, name3, id4, name4)] = swissPairings(tid)
    reportMatch(tid, id1, id2, id1)
    reportMatch(tid, id3, id4, id4)
    standings = playerStandings(tid)
    if [1, 3, 1, 3] != [row[4] for row in standings]:
        raise ValueError("Bad OMW count. Correct is [P1,P2,P3,P4]=[1,3,1,3].")
    if ["P1", "P3", "P4", "P2"] != [row[1] for row in standings]:
            raise ValueError("OMW is not taken into account to undo ties.")


    # Round 3, check final omw count and its use in undoing ties
    [(id1, name1, id2, name2), (id3, name3, id4, name4)] = swissPairings(tid)
    reportMatch(tid, id1, id2, id1)
    reportMatch(tid, id3, id4, id3)
    if [3, 4, 5, 6] != [row[4] for row in playerStandings(tid)]:
        raise ValueError("Bad OMW count. Correct is [P1,P2,P3,P4]=[3,4,5,6].")

    print "12. When 2 players have the same #wins, rank them according to OMW."


def testMultipleTournaments():
    # If resetTables content is commented, we can be sure the system Supports
    # multiple tournaments (as they've not been deleted between tests!). Just
    # to be thorough, we write this dedicated test.
    resetTables()

    # tournaments created for other tests
    numTours = countTournaments()

    tid1 = registerTournament("T1")
    tid2 = registerTournament("T2")
    if countTournaments() != numTours+2:
        raise ValueError("countTournaments() should return ", str(numTours+2))

    pid1 = registerPlayer("P1")
    pid2 = registerPlayer("P2")

    # Check that players can join multiple tournaments
    registerEntry(pid1, tid1)
    registerEntry(pid1, tid2)
    registerEntry(pid2, tid1)
    registerEntry(pid2, tid2)

    # Check matches/standings aren't crossed
    reportMatch(tid1, pid1, pid2, pid1)
    reportMatch(tid2, pid1, pid2, pid2)
    if [pid1, pid2] != [row[0] for row in playerStandings(tid1)]:
        raise ValueError("P1 should be first in T1")
    if [pid2, pid1] != [row[0] for row in playerStandings(tid2)]:
        raise ValueError("P2 should be first in T2")

    # Check that a player can't play in a tournament where it's not registered
    pid3 = registerPlayer("P3")
    try:
        reportMatch(tid1, pid1, pid3, pid1)
    except psycopg2.IntegrityError:
        print "13. Supports correctly more than one tournament in the database."
    else:
        raise ValueError ("Player must by registered in a tournament to play.")


if __name__ == '__main__':
    testDeleteMatches()
    testDelete()
    testCount()
    testRegister()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    testRematches()
    testOddPlayers()
    testDraws()
    testOpponentMatchWins()
    testMultipleTournaments()
    print "Success!  All tests pass!"
