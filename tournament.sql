-- Table definitions for the tournament project.
--


-- Create Database
DROP DATABASE tournament;
CREATE DATABASE tournament;

-- Connect to database
\c tournament

-- Create players Table
DROP TABLE players CASCADE;
CREATE TABLE players (id SERIAL PRIMARY KEY,
                      name TEXT);

-- Create matches Table
DROP TABLE matches CASCADE;
CREATE TABLE matches (match_id SERIAL PRIMARY KEY,
                      winner INTEGER references players(id),
                      loser INTEGER references players(id));

-- Create a View to track our standings
DROP VIEW standings;
CREATE VIEW standings AS
    SELECT players.id AS id,
           players.name AS name,
           -- Subquery to count number of wins
           (SELECT count(matches.winner) FROM matches
            WHERE players.id = matches.winner) AS wins,
            -- Subquery to count number of total matches
           (SELECT count(matches.match_id) FROM matches
            WHERE players.id = matches.winner
            OR players.id = matches.loser) AS tot_matches FROM players
    ORDER BY wins DESC;
