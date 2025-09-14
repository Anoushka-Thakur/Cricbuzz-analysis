INSERT INTO teams(name, country) VALUES
('India', 'India'),
('Australia', 'Australia'),
('England', 'England');

INSERT INTO players(full_name, role, batting_style, bowling_style, team_id) VALUES
('Rohit Sharma', 'Batsman', 'RHB', NULL, 1),
('Virat Kohli', 'Batsman', 'RHB', NULL, 1),
('Jasprit Bumrah', 'Bowler', NULL, 'Right-arm fast', 1),
('Pat Cummins', 'Bowler', NULL, 'Right-arm fast', 2),
('Joe Root', 'Batsman', 'RHB', 'Offbreak', 3);

INSERT INTO venues(name, city, country, capacity) VALUES
('Wankhede Stadium', 'Mumbai', 'India', 33500),
('MCG', 'Melbourne', 'Australia', 100024),
('Lord''s', 'London', 'England', 30000);

INSERT INTO series(name, host_country, match_type, start_date, end_date) VALUES
('Border-Gavaskar Trophy 2024', 'India', 'Test', '2024-02-01', '2024-03-30'),
('ODI Tri-Series 2024', 'Australia', 'ODI', '2024-07-10', '2024-07-25');

INSERT INTO matches(series_id, home_team_id, away_team_id, venue_id, match_date, result, toss_winner_id, toss_decision, winner_team_id, victory_margin, victory_type) VALUES
(1, 1, 2, 1, '2024-02-10', 'India won by 120 runs', 1, 'bat', 1, 120, 'runs'),
(2, 2, 3, 2, '2024-07-12', 'Australia won by 5 wickets', 2, 'bowl', 2, 5, 'wickets');

INSERT INTO innings_batting(match_id, innings_no, player_id, runs, balls, fours, sixes, strike_rate, batting_pos) VALUES
(1, 1, 1, 85, 90, 10, 2, 94.4, 1),
(1, 1, 2, 120, 110, 12, 3, 109.1, 3),
(1, 2, 4, 40, 55, 4, 1, 72.7, 5),
(2, 1, 5, 70, 80, 8, 1, 87.5, 4);

INSERT INTO innings_bowling(match_id, innings_no, player_id, overs, maidens, runs_conceded, wickets, economy) VALUES
(1, 2, 3, 20.0, 4, 60, 5, 3.0),
(2, 2, 4, 8.0, 0, 45, 2, 5.6);

INSERT INTO partnerships(match_id, innings_no, striker_id, non_striker_id, runs) VALUES
(1, 1, 1, 2, 145),
(2, 1, 5, 1, 60);
