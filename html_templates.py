"""HTML templates and markup for the Taboo game UI components."""

import streamlit as st
import os


def load_template(template_name):
    """Load HTML template from file"""
    template_path = os.path.join(os.path.dirname(__file__), "templates", template_name)
    try:
        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        st.error(f"Template {template_name} not found")
        return ""


def get_player_board_open():
    """Return opening div for player board."""
    return load_template("player_board_open.html")


def get_player_board_close():
    """Return closing div for player board."""
    return load_template("player_board_close.html")


def get_game_stats_html(player_count: int, ongoing: bool, current_round: int) -> str:
    """Generate HTML for game statistics display."""
    template = load_template("game_stats.html")
    status_icon = "🎮" if ongoing else "⏸️"
    status_text = "Ongoing" if ongoing else "Waiting"

    return template.format(
        player_count=player_count,
        status_icon=status_icon,
        status_text=status_text,
        current_round=current_round,
    )


def get_player_table_open():
    """Return opening div for player table."""
    return load_template("player_table_open.html")


def get_player_table_close():
    """Return closing div for player table."""
    return load_template("player_table_close.html")


def get_current_player_html(player_name: str) -> str:
    """Generate HTML for current player highlight."""
    template = load_template("current_player.html")
    css_style = "padding: 10px; border-radius: 8px;"
    return template.format(css_style=css_style, player_name=player_name)


def get_team_html(team_value: str) -> str:
    """Generate HTML for team display based on team value."""
    if team_value == "Team A":
        return load_template("team_a.html")
    elif team_value == "Team B":
        return load_template("team_b.html")
    else:
        return load_template("team_unassigned.html")


def get_role_html(role_value: str) -> str:
    """Generate HTML for role display based on role value."""
    role_template_map = {
        "leader": "role_leader.html",
        "checker": "role_checker.html",
        "card_maker": "role_card_maker.html",
        "guesser": "role_guesser.html",
    }
    template_name = role_template_map.get(role_value, "role_unassigned.html")
    return load_template(template_name)


def get_player_separator():
    """Return HTML for player row separator."""
    return load_template("player_separator.html")


def get_no_players_html() -> str:
    """Generate HTML for no players state."""
    return load_template("no_players.html")


def get_taboo_card_html(
    word: str, taboo_words: list, team_color: str = "neutral"
) -> str:
    """Generate HTML for a sticky note style taboo card."""
    template = load_template("taboo_card.html")

    # Create taboo words grid (2 columns)
    taboo_items = ""
    for taboo_word in taboo_words:
        taboo_items += f'<span class="taboo-word">• {taboo_word}</span>'

    team_class = (
        f"team-{team_color.lower().replace(' ', '-')}"
        if team_color != "neutral"
        else "team-neutral"
    )

    return template.format(
        word=word.upper(),
        taboo_items=taboo_items,
        team_class=team_class,
        team_color=team_color,
    )


def get_scorecard_html(
    team_a_score: int,
    team_b_score: int,
    current_round: int,
    total_rounds: int,
    current_turn: int,
    guessing_team: str,
) -> str:
    """Generate HTML for fancy scorecards."""
    template = load_template("scorecard.html")

    # Determine role indicators for each team
    team_a_role = "🤔 Guessing" if guessing_team == "Team A" else "🔍 Checking"
    team_b_role = "🤔 Guessing" if guessing_team == "Team B" else "🔍 Checking"

    # Calculate progress percentages
    total_score = max(team_a_score + team_b_score, 1)
    team_a_progress = (team_a_score / total_score) * 100
    team_b_progress = (team_b_score / total_score) * 100

    return template.format(
        team_a_score=team_a_score,
        team_b_score=team_b_score,
        current_round=current_round,
        total_rounds=total_rounds,
        current_turn=current_turn,
        team_a_role=team_a_role,
        team_b_role=team_b_role,
        team_a_progress=team_a_progress,
        team_b_progress=team_b_progress,
    )
