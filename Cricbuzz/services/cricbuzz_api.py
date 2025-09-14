import os
import requests
import streamlit as st

RAPIDAPI_KEY = st.secrets["RAPIDAPI"]["KEY"]
RAPIDAPI_HOST = st.secrets["RAPIDAPI"]["HOST"]


def get_live_matches_cached():
    url = "https://free-cricbuzz-cricket-api.p.rapidapi.com/cricket-livescores"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }
    response = requests.get(url, headers=headers)
    if not response.ok:
        print(f"Live matches API error: {response.status_code} {response.text}")
    response.raise_for_status()
    return response.json()


def get_match_scorecard_cached(match_id):
    """
    Fetch the scorecard for a given match ID from Cricbuzz API.
    Args:
        match_id (int or str): The match ID for which to fetch the scorecard.
    Returns:
        dict: The scorecard data as returned by the API.
    """
    url = f"https://free-cricbuzz-cricket-api.p.rapidapi.com/cricket-match-scoreboard?matchid=102040"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }
    response = requests.get(url, headers=headers)
    if not response.ok:
        print(f"Scorecard API error: {response.status_code} {response.text}")
    response.raise_for_status()
    return response.json()
