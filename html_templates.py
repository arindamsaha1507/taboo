"""HTML templates and markup for the Taboo game UI components."""


def get_player_board_open():
    """Return opening div for player board."""
    return '<div class="player-board">'


def get_player_board_close():
    """Return closing div for player board."""
    return "</div>"


def get_game_stats_html(player_count: int, ongoing: bool, current_round: int) -> str:
    """Generate HTML for game statistics display."""
    return f"""
    <div class="game-stats">
        <div class="stat-item">
            <div class="stat-number">{player_count}</div>
            <div>Players</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">{"🎮" if ongoing else "⏸️"}</div>
            <div>{"Ongoing" if ongoing else "Waiting"}</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">{current_round}</div>
            <div>Round</div>
        </div>
    </div>
    """


def get_player_table_open():
    """Return opening div for player table."""
    return '<div class="player-table">'


def get_player_table_close():
    """Return closing div for player table."""
    return "</div>"


def get_current_player_html(player_name: str) -> str:
    """Generate HTML for current player highlight."""
    return f'<div class="current-player" style="padding: 10px; border-radius: 8px;"><strong>🫵 {player_name}</strong></div>'


def get_team_html(team_value: str) -> str:
    """Generate HTML for team display based on team value."""
    if team_value == "Team A":
        return '<div class="team-a">Team A</div>'
    elif team_value == "Team B":
        return '<div class="team-b">Team B</div>'
    else:
        return '<div class="unassigned">Unassigned</div>'


def get_role_html(role_value: str) -> str:
    """Generate HTML for role display based on role value."""
    role_templates = {
        "leader": '<div class="role-leader">👑 Leader</div>',
        "checker": '<div class="role-checker">🔍 Checker</div>',
        "card_maker": '<div class="role-card_maker">🎯 Card Maker</div>',
        "guesser": '<div class="role-guesser">🤔 Guesser</div>',
    }
    return role_templates.get(
        role_value, '<div class="role-unassigned">Unassigned</div>'
    )


def get_player_separator():
    """Return HTML for player row separator."""
    return "<hr style='margin: 5px 0; opacity: 0.3;'>"


def get_no_players_html() -> str:
    """Generate HTML for no players state."""
    return """
        <h3>👥 No players yet</h3>
        <em>Waiting for players to join...</em>
    """


def get_taboo_card_html(
    word: str, taboo_words: list, team_color: str = "neutral"
) -> str:
    """Generate HTML for a sticky note style taboo card."""
    # Create taboo words grid (2 columns)
    taboo_items = ""
    for taboo_word in taboo_words:
        taboo_items += f'<span class="taboo-word">• {taboo_word}</span>'

    team_class = (
        f"team-{team_color.lower().replace(' ', '-')}"
        if team_color != "neutral"
        else "team-neutral"
    )

    return f"""<div class="taboo-card {team_class}">
<div class="card-header">
<span class="card-icon">📝</span>
<span class="card-title">TABOO CARD</span>
</div>
<div class="main-word-section">
<div class="main-word">{word.upper()}</div>
<div class="word-underline"></div>
</div>
<div class="taboo-section">
<div class="taboo-header">❌ Forbidden Words:</div>
<div class="taboo-words-grid">
{taboo_items}
</div>
</div>
<div class="team-indicator {team_class}">
{team_color}
</div>
</div>"""
