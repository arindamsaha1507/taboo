"""Streamlit app for the Taboo game."""

import streamlit as st

from components import (
    display_player_state,
    add_player,
    game_controls,
    display_main_interface,
)
from backend import get_shared_game


def main():
    """Main function to run the Streamlit app."""

    st.title("Taboo Game")

    # Display auto-updating game state
    display_player_state()

    # Get the shared game instance for user interactions
    game = get_shared_game()

    # Add player functionality

    if game.ongoing:
        with st.sidebar:
            add_player(game)

        display_main_interface()

    else:
        add_player(game)

    # Add game control buttons
    with st.sidebar:
        st.header("Game Controls")
        game_controls()

    if st.button("Refresh", width="stretch"):
        st.rerun()


if __name__ == "__main__":
    main()
