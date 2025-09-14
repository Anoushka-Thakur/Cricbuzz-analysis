-- # Core reference tables

CREATE TABLE IF NOT EXISTS teams (
  team_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  country TEXT
);

CREATE TABLE IF NOT EXISTS players (
  player_id INTEGER PRIMARY KEY AUTOINCREMENT,
  full_name TEXT NOT NULL,
  role TEXT,
  batting_style TEXT,
  bowling_style TEXT,
  team_id INTEGER,
  FOREIGN KEY(team_id) REFERENCES teams(team_id)
);

CREATE TABLE IF NOT EXISTS venues (
  venue_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  city TEXT,
  country TEXT,
  capacity INTEGER
);

CREATE TABLE IF NOT EXISTS series (
  series_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  host_country TEXT,
  match_type TEXT,
  start_date TEXT,
  end_date TEXT
);

CREATE TABLE IF NOT EXISTS matches (
  match_id INTEGER PRIMARY KEY AUTOINCREMENT,
  series_id INTEGER,
  home_team_id INTEGER,
  away_team_id INTEGER,
  venue_id INTEGER,
  match_date TEXT,
  result TEXT,
  toss_winner_id INTEGER,
  toss_decision TEXT,
  winner_team_id INTEGER,
  victory_margin INTEGER,
  victory_type TEXT,
  FOREIGN KEY(series_id) REFERENCES series(series_id),
  FOREIGN KEY(home_team_id) REFERENCES teams(team_id),
  FOREIGN KEY(away_team_id) REFERENCES teams(team_id),
  FOREIGN KEY(venue_id) REFERENCES venues(venue_id)
);

CREATE TABLE IF NOT EXISTS innings_batting (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  match_id INTEGER,
  innings_no INTEGER,
  player_id INTEGER,
  runs INTEGER,
  balls INTEGER,
  fours INTEGER,
  sixes INTEGER,
  strike_rate REAL,
  batting_pos INTEGER,
  FOREIGN KEY(match_id) REFERENCES matches(match_id),
  FOREIGN KEY(player_id) REFERENCES players(player_id)
);

CREATE TABLE IF NOT EXISTS innings_bowling (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  match_id INTEGER,
  innings_no INTEGER,
  player_id INTEGER,
  overs REAL,
  maidens INTEGER,
  runs_conceded INTEGER,
  wickets INTEGER,
  economy REAL,
  FOREIGN KEY(match_id) REFERENCES matches(match_id),
  FOREIGN KEY(player_id) REFERENCES players(player_id)
);

CREATE TABLE IF NOT EXISTS partnerships (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  match_id INTEGER,
  innings_no INTEGER,
  striker_id INTEGER,
  non_striker_id INTEGER,
  runs INTEGER,
  FOREIGN KEY(match_id) REFERENCES matches(match_id)
);

CREATE INDEX IF NOT EXISTS idx_batting_player ON innings_batting(player_id);
CREATE INDEX IF NOT EXISTS idx_bowling_player ON innings_bowling(player_id);
CREATE INDEX IF NOT EXISTS idx_matches_date ON matches(match_date);
