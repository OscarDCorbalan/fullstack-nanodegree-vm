#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *

def resetTables():
    deleteByes()
    deleteMatches()
    deletePlayers()

def testDeleteMatches():
    deleteMatches()
    print "1. Old matches can be deleted."


def testDelete():
    resetTables()
    print "2. Player records can be deleted."


def testCount():
    resetTables()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."


def testRegister():
    resetTables()
    registerPlayer("Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete():
    resetTables()
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
    registerPlayer("Melpomene Murray")
    registerPlayer("Randy Schwartz")
    standings = playerStandings()
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."


def testReportMatches():
    resetTables()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    standings = playerStandings()
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings."


def testPairings():
    resetTables()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    pairings = swissPairings()
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
    registerPlayer("Shaquille O'Neal")
    registerPlayer("Michael Jordan")
    standings = playerStandings()
    [id1, id2] = [row[0] for row in standings]
    reportMatch(id1, id2)
    try:
        reportMatch(id1, id2)
    except psycopg2.IntegrityError:
        try:
            reportMatch(id2, id1)
        except psycopg2.IntegrityError:
            print "9. Rematches between players are not allowed."
    else:
        raise ValueError(
            "Rematches between players are allowed.")


def testOddPlayers():
    resetTables()
    registerPlayer("Lionel Messi")
    registerPlayer("Cristiano Ronaldo")
    registerPlayer("Arjen Robben")
    registerPlayer("Zlatan Ibrahimovic")
    registerPlayer("Franz Beckenbauer")
    registerPlayer("Andres Iniesta")
    registerPlayer("James Rodriguez")
    registerPlayer("Manuel Neuer")
    registerPlayer("Andres Iniesta")

    firstRound = True;
    # Any second bye to the same player would throw a duplicate key error
    for round in range(1, 3):
        pairings = swissPairings()
        [(id1, name1, id2, name2), (id3, name3, id4, name4),
        (id5, name5, id6, name6), (id7, name7, id8, name8)] = swissPairings()

        # In 1st round he's the first since no one else still reported a match
        if firstRound:
            firstRound = False
            last = playerStandings()[0]
            if last[1] != "Andres Iniesta":
                raise ValueError("Last player didn't get a bye.")

        reportMatch(id1, id2)
        reportMatch(id3, id4)
        reportMatch(id5, id6)
        reportMatch(id7, id8)

    print "10. With odd #players, last receives a bye and no one receives 2+."


def testTournament():
    resetTables()
    registerPlayer("P1")
    registerPlayer("P2")
    registerPlayer("P3")
    registerPlayer("P4")
    registerPlayer("P5")
    registerPlayer("P6")
    registerPlayer("P7")
    registerPlayer("P8")

    for round in range(1, 4):
        #print "round", round
        pairings = swissPairings()
        [(id1, name1, id2, name2), (id3, name3, id4, name4),
        (id5, name5, id6, name6), (id7, name7, id8, name8)] = pairings
        #print name1, name2, name3, name4, name5, name6, name7, name8
        reportMatch(id1, id2)
        reportMatch(id3, id4)
        reportMatch(id5, id6)
        reportMatch(id7, id8)
    print "*. Real tournament works."

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
    #testTournament()
    print "Success!  All tests pass!"
