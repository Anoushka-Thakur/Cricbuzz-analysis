# import libraries and setup path

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.resolve()))

import streamlit as st
from utils.db import ensure_db_ready, get_connection
import pandas as pd
from pathlib import Path
from services.cricbuzz_api import get_live_matches_cached

# Custom CSS for theming

# Sidebar navigation
st.set_page_config(page_title="Cricbuzz LiveStats", layout="wide")
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Home", "Live Matches", "Top Player Stats", "SQL Analytics", "CRUD Operations"],
    format_func=lambda x: x
)

# Ensure DB exists (creates from SQL if needed)
ensure_db_ready()
st.title("🏏 Cricbuzz LiveStats")


# Only show Home page content when Home is selected
if page == "Home":
    # Show quick live stats at the top of the Home page
    st.subheader("Quick live check (sample/cached if offline)")
    try:
        data = get_live_matches_cached()
        if data.get("status") == "success" and "response" in data:
            for series in data["response"]:
                series_name = series.get("seriesName", "Unknown Series")
                st.markdown(f"## {series_name}")
                for match in series.get("matchList", []):
                    match_id = match.get("matchId", "")
                    match_title = match.get("matchTitle", "")
                    match_format = match.get("matchFormat", "")
                    match_venue = match.get("matchVenue", "")
                    match_date = match.get("matchDate", "")
                    match_time = match.get("matchTime", "")
                    team1 = match.get("teamOne", {}).get("name", "Team 1")
                    team1_score = match.get("teamOne", {}).get("score", "-")
                    team2 = match.get("teamTwo", {}).get("name", "Team 2")
                    team2_score = match.get("teamTwo", {}).get("score", "-")
                    match_status = match.get("matchStatus", "")
                    current_status = match.get("currentStatus", "")
                    with st.container():
                        st.markdown(f"### {match_title} ({match_format})")
                        st.markdown(f"**Venue:** {match_venue}, {match_date} {match_time}")
                        st.markdown(f"**{team1}**: {team1_score}")
                        st.markdown(f"**{team2}**: {team2_score}")
                        st.markdown(f"**Status:** {match_status}")
                        st.markdown(f"**Current:** {current_status}")
                        st.markdown("---")
        else:
            st.warning("No live matches found or API response format unexpected.")
    except Exception as e:
        import requests
        if isinstance(e, requests.exceptions.HTTPError) and hasattr(e.response, 'status_code') and e.response.status_code == 429:
            st.error("Live data is temporarily unavailable due to too many requests (API rate limit). Please try again in a few minutes.")
        else:
            st.error(f"Could not fetch live data: {str(e)}")
elif page == "Top Player Stats":
    st.title("📈 Top Player Stats")
    conn = get_connection()
    q_runs = """
SELECT p.player_id, p.full_name, COALESCE(SUM(b.runs),0) AS total_runs
FROM players p
LEFT JOIN innings_batting b ON p.player_id=b.player_id
GROUP BY p.player_id, p.full_name
ORDER BY total_runs DESC
LIMIT 10;
"""
    q_wkts = """
SELECT p.player_id, p.full_name, COALESCE(SUM(w.wickets),0) AS total_wickets
FROM players p
LEFT JOIN innings_bowling w ON p.player_id=w.player_id
GROUP BY p.player_id, p.full_name
ORDER BY total_wickets DESC
LIMIT 10;
"""
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🏏 Top Runs")
        df_runs = pd.read_sql_query(q_runs, conn)
        st.dataframe(df_runs)
    with col2:
        st.subheader("🎯 Top Wickets")
        df_wkts = pd.read_sql_query(q_wkts, conn)
        st.dataframe(df_wkts)

elif page == "SQL Analytics":
    st.title("🧮 SQL Analytics")
    conn = get_connection()
    queries_file = Path("sql/practice_queries.sql")
    prepared = []
    if queries_file.exists():
        content = queries_file.read_text(encoding="utf-8")
        blocks = content.split("\n-- Q")
        for i, b in enumerate(blocks):
            if not b.strip(): 
                continue
            prepared.append("-- Q" + b.strip())
    st.markdown("### Prepared queries")
    if prepared:
        choice = st.selectbox("Pick a prepared query", list(range(1, len(prepared)+1)), format_func=lambda i: f"Q{i}")
        st.code(prepared[choice-1])
    st.markdown("### Run custom SQL (SELECT only recommended)")
    user_sql = st.text_area("SQL", "SELECT * FROM players LIMIT 10;")
    if st.button("Run SQL"):
        try:
            df = pd.read_sql_query(user_sql, conn)
            st.dataframe(df)
        except Exception as e:
            st.error(str(e))

elif page == "CRUD Operations":
    st.title("🛠️ CRUD Operations")
    conn = get_connection()
    st.subheader("Create / Update Player")
    with st.form("player_form_1"):
        pid = st.text_input("Player ID (leave blank to add)")
        name = st.text_input("Full name")
        role = st.selectbox("Role", ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"])
        batting = st.text_input("Batting style")
        bowling = st.text_input("Bowling style")
        submitted = st.form_submit_button("Save")
        if submitted:
            cur = conn.cursor()
            if pid:
                cur.execute("REPLACE INTO players(player_id, full_name, role, batting_style, bowling_style) VALUES(?,?,?,?,?)",
                            (pid, name, role, batting, bowling))
            else:
                cur.execute("INSERT INTO players(full_name, role, batting_style, bowling_style) VALUES(?,?,?,?)",
                            (name, role, batting, bowling))
            conn.commit()
            st.success("Saved")
    st.markdown("---")
    st.subheader("Players (recent)")
    df = pd.read_sql_query("SELECT * FROM players ORDER BY player_id DESC LIMIT 50;", conn)
    st.dataframe(df)
    st.subheader("Delete Player")
    del_id = st.text_input("Player ID to delete")
    if st.button("Delete"):
        cur = conn.cursor()
        cur.execute("DELETE FROM players WHERE player_id=?", (del_id,))
        conn.commit()
        st.success("Deleted (if existed)")


from services.cricbuzz_api import get_live_matches_cached, get_match_scorecard_cached

st.title("📡 Live Matches")
data = get_live_matches_cached()
if isinstance(data, dict) and data.get("type") == "error":
    st.error(data.get("message"))
else:
    matches = data.get("matches", []) if isinstance(data, dict) else []
    st.write(f"Found matches: {len(matches)} (showing up to 10)")
    for m in matches[:10]:
        desc = m.get("matchInfo", {}).get("matchDesc", "Match")
        mid = m.get("matchInfo", {}).get("matchId")
        with st.expander(f"{desc} — id: {mid}"):
            st.json(m)

st.divider()
match_id = st.text_input("Enter match ID to fetch scorecard", key="scorecard_match_id")
if st.button("Fetch Scorecard", key="fetch_scorecard_btn"):
    if not match_id:
        st.warning("Enter a match ID")
    else:
        sc = get_match_scorecard_cached(match_id)
        st.json(sc)


import pandas as pd
from utils.db import get_connection

st.title("📈 Top Player Stats")
conn = get_connection()

q_runs = """
SELECT p.player_id, p.full_name, COALESCE(SUM(b.runs),0) AS total_runs
FROM players p
LEFT JOIN innings_batting b ON p.player_id=b.player_id
GROUP BY p.player_id, p.full_name
ORDER BY total_runs DESC
LIMIT 10;
"""

q_wkts = """
SELECT p.player_id, p.full_name, COALESCE(SUM(w.wickets),0) AS total_wickets
FROM players p
LEFT JOIN innings_bowling w ON p.player_id=w.player_id
GROUP BY p.player_id, p.full_name
ORDER BY total_wickets DESC
LIMIT 10;
"""

col1, col2 = st.columns(2)
with col1:
    st.subheader("🏏 Top Runs")
    df_runs = pd.read_sql_query(q_runs, conn)
    st.dataframe(df_runs)

with col2:
    st.subheader("🎯 Top Wickets")
    df_wkts = pd.read_sql_query(q_wkts, conn)
    st.dataframe(df_wkts)


import pandas as pd
from utils.db import get_connection
from pathlib import Path

st.title("🧮 SQL Analytics")
conn = get_connection()

queries_file = Path("sql/practice_queries.sql")
prepared = []
if queries_file.exists():
    content = queries_file.read_text(encoding="utf-8")
    # split on lines starting with -- Q (simple)
    blocks = content.split("\n-- Q")
    for i, b in enumerate(blocks):
        if not b.strip(): 
            continue
        prepared.append("-- Q" + b.strip())

st.markdown("### Prepared queries")
if prepared:
    choice = st.selectbox("Pick a prepared query", list(range(1, len(prepared)+1)), format_func=lambda i: f"Q{i}")
    st.code(prepared[choice-1])

st.markdown("### Run custom SQL (SELECT only recommended)")
user_sql = st.text_area("SQL", "SELECT * FROM players LIMIT 10;")
if st.button("Run SQL"):
    try:
        df = pd.read_sql_query(user_sql, conn)
        st.dataframe(df)
    except Exception as e:
        st.error(str(e))


import streamlit as st
import pandas as pd
from utils.db import get_connection

st.title("🛠️ CRUD Operations")
conn = get_connection()

st.subheader("Create / Update Player")
with st.form("player_form_2", clear_on_submit=False):
    pid = st.text_input("Player ID (leave blank to add)")
    name = st.text_input("Full name")
    role = st.selectbox("Role", ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"])
    batting = st.text_input("Batting style")
    bowling = st.text_input("Bowling style")
    submitted = st.form_submit_button("Save")
    if submitted:
        cur = conn.cursor()
        if pid:
            cur.execute("REPLACE INTO players(player_id, full_name, role, batting_style, bowling_style) VALUES(?,?,?,?,?)",
                        (pid, name, role, batting, bowling))
        else:
            cur.execute("INSERT INTO players(full_name, role, batting_style, bowling_style) VALUES(?,?,?,?)",
                        (name, role, batting, bowling))
        conn.commit()
        st.success("Saved")

st.markdown("---")
st.subheader("Players (recent)")
df = pd.read_sql_query("SELECT * FROM players ORDER BY player_id DESC LIMIT 50;", conn)
st.dataframe(df)

st.subheader("Delete Player")
del_id = st.text_input("Player ID to delete", key="delete_player_id")
if st.button("Delete", key="delete_player_button"):
    cur = conn.cursor()
    cur.execute("DELETE FROM players WHERE player_id=?", (del_id,))
    conn.commit()
    st.success("Deleted (if existed)")


st.markdown("---")
st.title("🧮 SQL Analysis & Custom Queries")
conn = get_connection()

analysis_queries = {
    "Players from India": "SELECT p.full_name, p.role, p.batting_style, p.bowling_style FROM players p JOIN teams t ON p.team_id = t.team_id WHERE t.country = 'India';",
    "Matches in last 30 days": "SELECT m.match_id, t1.name AS team1, t2.name AS team2, v.name AS venue, v.city, m.match_date FROM matches m JOIN teams t1 ON m.home_team_id = t1.team_id JOIN teams t2 ON m.away_team_id = t2.team_id JOIN venues v ON m.venue_id = v.venue_id WHERE DATE(m.match_date) >= DATE('now','-30 day') ORDER BY m.match_date DESC;",
    "Top run scorers": "SELECT p.full_name, SUM(b.runs) AS total_runs FROM players p JOIN innings_batting b ON p.player_id=b.player_id GROUP BY p.full_name ORDER BY total_runs DESC LIMIT 10;",
    "Venues capacity > 50k": "SELECT name, city, country, capacity FROM venues WHERE capacity > 50000;",
    "Matches won by each team": "SELECT t.name, COUNT(*) AS wins FROM matches m JOIN teams t ON m.winner_team_id = t.team_id GROUP BY t.name ORDER BY wins DESC;",
    "Average runs per player": "SELECT p.full_name, AVG(b.runs) AS avg_runs FROM players p JOIN innings_batting b ON p.player_id = b.player_id GROUP BY p.full_name ORDER BY avg_runs DESC LIMIT 10;",
    "Highest partnerships (top 5)": "SELECT s1.full_name AS striker, s2.full_name AS non_striker, pr.runs, m.match_id FROM partnerships pr JOIN players s1 ON pr.striker_id = s1.player_id JOIN players s2 ON pr.non_striker_id = s2.player_id JOIN matches m ON pr.match_id = m.match_id ORDER BY pr.runs DESC LIMIT 5;",
    "Teams with most matches played": "SELECT t.name, COUNT(*) AS matches_played FROM teams t JOIN matches m ON t.team_id = m.home_team_id OR t.team_id = m.away_team_id GROUP BY t.name ORDER BY matches_played DESC;"
}

st.subheader("Run a prepared analysis query")
query_name = st.selectbox("Select a query", list(analysis_queries.keys()))
if st.button("Run Analysis Query"):
    try:
        df = pd.read_sql_query(analysis_queries[query_name], conn)
        st.dataframe(df)
    except Exception as e:
        st.error(str(e))


