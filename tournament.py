#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE from matches")
    DB.commit()
    c.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE from players")
    DB.commit()
    c.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT COUNT(*) from players")
    playerCount = c.fetchone()
    c.close()
    return playerCount[0]


def registerPlayer(name):
    """Adds a player to the tournament database."""
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO players (name) VALUES (%s)", (name,))
    DB.commit()
    c.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins."""
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT * FROM standings")
    playerRecord = c.fetchall()
    c.close()
    return playerRecord


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players."""
    DB = connect()
    c = DB.cursor()
    c.execute("""INSERT INTO matches (winner, loser)
                 VALUES (%s, %s)""", [(winner,), (loser,)])
    DB.commit()
    c.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match."""

    # Get a list of all our players from our view in the database
    # that has our players ordered by number of wins
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT id, name FROM standings")
    players = c.fetchall()
    c.close()

    # Find pairings by grabbing the next 2 players off our list
    # of players we created above, adding them together, and
    # appending their information to our pairings list
    swPairings = []
    index = 0
    while index < len(players) + 2:
        pair = players.pop()+players.pop()
        swPairings.append(pair)
        # print swPairings
        index = index+1
    return swPairings
