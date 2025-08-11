"""This module contains components for the Taboo game."""

import time

import streamlit as st

from backend import Card, get_shared_game, Player, Team, Role, Game, MIN_PLAYERS
from css_loader import load_css
from html_templates import (
    get_player_board_open,
    get_player_board_close,
    get_game_stats_html,
    get_player_table_open,
    get_player_table_close,
    get_current_player_html,
    get_team_html,
    get_role_html,
    get_player_separator,
    get_no_players_html,
    get_taboo_card_html,
)


def add_player(game: Game):
    """Add a new player to the game."""

    if "player_name" in st.session_state:
        # Player is already in the game
        st.write(f"Welcome, {st.session_state['player_name']}!")

        player = next(
            (p for p in game.players if p.name == st.session_state["player_name"]), None
        )
        if not player:
            return

        if game.ongoing:
            return

        # Team selection (always available)
        st.subheader("Team Selection")
        team_options = ["Team A", "Team B"]
        current_team_index = 0
        if player.team == Team.B:
            current_team_index = 1

        team_choice = st.selectbox(
            "Select your team:",
            options=team_options,
            index=current_team_index,
            key="team_selector",
        )

        if st.button("Update Team"):
            player.team = Team.A if team_choice == "Team A" else Team.B

            # Reset role when team changes
            player.role = Role.UNASSIGNED
            st.success(f"Team updated to {team_choice}!")
            st.rerun()

        # Role selection (always available if team is assigned)
        if player.team != Team.U:
            st.subheader("Role Selection")

            role_options = (
                ["guesser", "leader"]
                if player.team == game.guessing_team
                else ["checker", "card_maker"]
            )

            current_role_index = 0
            if player.role.value in role_options:
                current_role_index = role_options.index(player.role.value)

            role_choice = st.selectbox(
                "Select your role:",
                options=role_options,
                index=current_role_index,
                key="role_selector",
            )

            if st.button("Update Role"):
                player.role = Role(role_choice)
                st.success(f"Role updated to {role_choice}!")
                st.rerun()
        else:
            st.info("Please update your team selection above to choose your role.")

        return

    # New player joining
    st.subheader("Join the Game")
    name = st.text_input("Enter your name:")
    if st.button("Join Game"):
        if name and name not in [p.name for p in game.players]:
            new_player = Player(name=name)
            game.add_player(new_player)
            st.success(f"{name} has joined!")
            st.session_state["player_name"] = name
            st.rerun()
        elif not name:
            st.error("Please enter a name!")
            time.sleep(2)
            st.rerun()
        else:
            st.info("Rejoining the game...")
            time.sleep(2)
            st.session_state["player_name"] = name
            st.rerun()


def display_player_state():
    """Display the current game state with auto-refresh every 2 seconds."""
    game = get_shared_game()

    # Load external CSS
    load_css("styles.css")

    if game.ongoing:
        # Show compact version in sidebar when game is ongoing
        with st.sidebar:
            display_compact_player_state(game)
        return

    # Show full version in main area when game is not ongoing
    display_full_player_state(game)


@st.fragment(run_every=2)
def display_compact_player_state(game):
    """Display a compact version of player state for the sidebar during gameplay."""
    st.markdown("### 👥 Players")

    # Simple game stats
    st.markdown(f"**Round:** {game.current_round}")
    st.markdown(f"**Players:** {len(game.players)}")

    # Compact player list grouped by team
    team_a_players = [
        p for p in game.players if hasattr(p, "team") and p.team.value == "Team A"
    ]
    team_b_players = [
        p for p in game.players if hasattr(p, "team") and p.team.value == "Team B"
    ]

    if team_a_players:
        st.markdown("**🔴 Team A**")
        for player in team_a_players:
            role_emoji = {
                "leader": "👑",
                "guesser": "🤔",
                "checker": "🔍",
                "card_maker": "🎯",
            }.get(player.role.value, "❓")
            current_marker = (
                "🫵 " if st.session_state.get("player_name") == player.name else ""
            )
            st.markdown(f"- {current_marker}{role_emoji} {player.name}")

    if team_b_players:
        st.markdown("**🔵 Team B**")
        for player in team_b_players:
            role_emoji = {
                "leader": "👑",
                "guesser": "🤔",
                "checker": "🔍",
                "card_maker": "🎯",
            }.get(player.role.value, "❓")
            current_marker = (
                "🫵 " if st.session_state.get("player_name") == player.name else ""
            )
            st.markdown(f"- {current_marker}{role_emoji} {player.name}")


@st.fragment(run_every=2)
def display_full_player_state(game: Game):
    """Display the full player state for the main area during setup."""
    # Game statistics in a fancy card
    st.markdown(get_player_board_open(), unsafe_allow_html=True)

    st.markdown(
        get_game_stats_html(len(game.players), game.ongoing, game.current_round),
        unsafe_allow_html=True,
    )

    # Player table
    if game.players:
        st.markdown(get_player_table_open(), unsafe_allow_html=True)
        st.markdown("### 👥 Player Dashboard")

        # Create the player table
        for i, player in enumerate(game.players):
            is_current_player = st.session_state.get("player_name") == player.name

            # Player row
            (
                col1,
                col2,
                col3,
            ) = st.columns([3, 2, 2])

            with col1:
                # Player name with highlight if current player
                if is_current_player:
                    st.markdown(
                        get_current_player_html(player.name),
                        unsafe_allow_html=True,
                    )
                else:
                    st.write(f"**{player.name}**")

            with col2:
                # Team assignment
                if hasattr(player, "team") and player.team:
                    st.markdown(
                        get_team_html(player.team.value), unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        get_team_html("Unassigned"),
                        unsafe_allow_html=True,
                    )

            with col3:
                # Role display/selection
                st.markdown(
                    get_role_html(player.role.value),
                    unsafe_allow_html=True,
                )

            # Add a subtle separator
            if i < len(game.players) - 1:
                st.markdown(get_player_separator(), unsafe_allow_html=True)

        st.markdown(get_player_table_close(), unsafe_allow_html=True)
    else:
        st.markdown(get_player_table_open(), unsafe_allow_html=True)
        st.markdown(get_no_players_html(), unsafe_allow_html=True)
        st.markdown(get_player_table_close(), unsafe_allow_html=True)

    st.markdown(get_player_board_close(), unsafe_allow_html=True)


@st.fragment(run_every=1)
def display_main_interface():
    """Display the main interface for the Taboo game."""

    game = get_shared_game()

    st.markdown(f"#### Turn {game.current_turn} of Round {game.current_round}")

    player = st.session_state.get("player_name")
    if not player:
        st.warning("Please join the game first!")
        return
    player = next((p for p in get_shared_game().players if p.name == player), None)

    if not player:
        st.warning("Player not found!")
        return

    if player.role.value == "card_maker":
        st.subheader("Card Maker Controls")
        card_maker_controls()

    elif player.role.value == "guesser":
        st.subheader("Guesser Interface")
        guesser_interface()

    elif player.role.value == "checker":
        st.subheader("Checker Interface")
        checker_interface()

    elif player.role.value == "leader":
        st.subheader("Leader Interface")
        leader_interface()

    else:
        st.subheader("General Player Interface")
        st.write("Main interface placeholder")


@st.fragment(run_every=1)
def game_controls():
    """Display game control buttons for refresh, start, and reset."""
    game = get_shared_game()

    # Add buttons for game management

    if not game.ongoing:
        if st.button("🎮 Start Game"):
            if len(game.players) < MIN_PLAYERS:
                st.error(
                    f"At least {MIN_PLAYERS} players are required to start the game!"
                )
                time.sleep(2)
                st.rerun()

            if game.check_teams():
                game.start_game()

            st.rerun()

    if st.button("🗑️ Reset Game"):
        # Clear the cache to get a fresh game instance
        get_shared_game.clear()
        st.success("Game reset!")
        st.rerun()


def display_card(card: Card):
    """Display a single card in sticky note style."""
    if not card:
        st.warning("No card to display.")
        return

    # Get current game to determine team context
    game = get_shared_game()
    current_player_name = st.session_state.get("player_name")
    team_color = "neutral"

    if current_player_name:
        current_player = next(
            (p for p in game.players if p.name == current_player_name), None
        )
        if current_player and hasattr(current_player, "team"):
            team_color = (
                current_player.team.value
                if current_player.team.value != "Unassigned"
                else "neutral"
            )

    # Display the card using HTML template
    st.markdown(
        get_taboo_card_html(card.word, card.taboo_words, team_color),
        unsafe_allow_html=True,
    )


def card_maker_controls():
    """Display card maker controls for creating new cards."""
    game = get_shared_game()

    if not game.ongoing:
        st.warning("Game is not ongoing. Please start the game first.")
        time.sleep(2)
        st.rerun()

    if game.turns and game.turns[-1].card is not None:
        # st.warning("A card has already been created for this turn.")
        display_card(game.turns[-1].card)

    else:
        st.subheader("Create New Card")

        word = st.text_input("Word to guess:")
        taboo_words = st.text_area("Taboo words (comma-separated):")

        if st.button("Create Card"):
            if word and taboo_words:
                taboo_list = [w.strip() for w in taboo_words.split(",") if w.strip()]
                game.make_card(word, taboo_list)
                st.success(
                    f"Card created for '{word}' with taboo words: {', '.join(taboo_list)}"
                )
                time.sleep(2)
                st.rerun()
            else:
                st.error("Please provide both a word and taboo words.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Hints")
        with st.container(height=500):
            if game.turns:
                for hint, hinter in zip(game.turns[-1].hints, game.turns[-1].hinters):
                    st.write(f"💡 {hinter.name}: {hint.capitalize()}")

    with col2:
        st.subheader("Guesses")
        with st.container(height=500):
            if game.turns:
                for guess, guesser in zip(
                    game.turns[-1].guesses, game.turns[-1].guessers
                ):
                    st.write(f"💭 {guesser.name}: {guess.capitalize()}")


def leader_interface():
    """Display the leader interface for managing game state."""
    game = get_shared_game()

    player = st.session_state.get("player_name")
    if not player:
        st.warning("Please join the game first!")
        return
    player = next((p for p in get_shared_game().players if p.name == player), None)

    if not game.ongoing:
        st.warning("Game is not ongoing. Please start the game first.")
        time.sleep(2)
        st.rerun()

    # Display current card if available
    if game.turns and game.turns[-1].card is not None:
        display_card(game.turns[-1].card)
    else:
        st.info("No card created yet. Please create a card first.")

    # Additional leader controls can be added here

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Hints")
        with st.container(height=500):
            if game.turns:
                for hint, hinter in zip(game.turns[-1].hints, game.turns[-1].hinters):
                    st.write(f"💡 {hinter.name}: {hint.capitalize()}")

    with col2:
        st.subheader("Guesses")
        with st.container(height=500):
            if game.turns:
                for guess, guesser in zip(
                    game.turns[-1].guesses, game.turns[-1].guessers
                ):
                    st.write(f"💭 {guesser.name}: {guess.capitalize()}")

    new_hint = st.text_input("Add a new hint:")
    if st.button("Add Hint"):
        if new_hint.strip() and new_hint.strip() not in game.turns[-1].hints:
            game.turns[-1].add_hint(new_hint, player)
            st.rerun()


def guesser_interface():
    """Display the guesser interface for managing game state."""
    game = get_shared_game()

    player = st.session_state.get("player_name")
    if not player:
        st.warning("Please join the game first!")
        return
    player = next((p for p in get_shared_game().players if p.name == player), None)

    if not game.ongoing:
        st.warning("Game is not ongoing. Please start the game first.")
        time.sleep(2)
        st.rerun()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Hints")
        with st.container(height=500):
            if game.turns:
                for hint, hinter in zip(game.turns[-1].hints, game.turns[-1].hinters):
                    st.write(f"💡 {hinter.name}: {hint.capitalize()}")

    with col2:
        st.subheader("Guesses")
        with st.container(height=500):
            if game.turns:
                for guess, guesser in zip(
                    game.turns[-1].guesses, game.turns[-1].guessers
                ):
                    st.write(f"💭 {guesser.name}: {guess.capitalize()}")

    new_guess = st.text_input("Add a new guess:")
    if st.button("Add Guess"):
        if new_guess.strip() and new_guess.strip() not in game.turns[-1].guesses:
            game.turns[-1].add_guess(new_guess, player)
            st.rerun()


def checker_interface():
    """Display the checker interface for managing game state."""
    game = get_shared_game()

    # player = st.session_state.get("player_name")

    if game.turns and game.turns[-1].card is not None:
        display_card(game.turns[-1].card)
    else:
        st.info("No card created yet. Please create a card first.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Hints")
        with st.container(height=500):
            if game.turns:
                for hint, hinter in zip(game.turns[-1].hints, game.turns[-1].hinters):
                    st.write(f"💡 {hinter.name}: {hint.capitalize()}")

    with col2:
        st.subheader("Guesses")
        with st.container(height=500):
            if game.turns:
                for guess, guesser in zip(
                    game.turns[-1].guesses, game.turns[-1].guessers
                ):
                    st.write(f"💭 {guesser.name}: {guess.capitalize()}")
