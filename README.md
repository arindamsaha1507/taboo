# Multiplayer Taboo Game

A simple Streamlit web application for playing the Taboo word game online with multiple players.

## Features

- **Multiplayer Support**: Players can join two teams (Team A and Team B)
- **Role-Based Gameplay**:
  - Guesser team members guess the word
  - One leader gives clues
  - Checker team monitors for rule violations
- **Dynamic Cards**: Pre-loaded cards with main words and taboo words
- **Real-time Interaction**: Live guess log and game state updates
- **Game Controls**:
  - Switch turns between teams
  - Claim cheating functionality
  - Manual game end option
  - Leave game option

## How to Play

1. **Join the Game**: Enter your name and select a team (A or B)
2. **Start Game**: Once both teams have players, click "Start Game"
3. **Turn-Based Play**:
   - One team becomes the "guessing team", the other becomes the "checking team"
   - The guessing team selects a leader
   - The checking team gives a card to the leader
4. **Gameplay**:
   - The leader sees the main word and taboo words
   - The leader gives one-word clues to help teammates guess
   - Non-leader team members submit their guesses
   - The checking team monitors for rule violations
5. **Win Conditions**:
   - Guessing team wins by correctly guessing the main word
   - Checking team wins if they successfully claim cheating
6. **Continue**: Switch turns and repeat with new cards

## Installation and Running

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:

   ```bash
   streamlit run app.py
   ```

3. Open your browser to the displayed URL (usually `http://localhost:8501`)

## Game Rules

- The leader can only give one-word clues
- The leader cannot use any of the taboo words (directly or indirectly)
- The checking team can claim cheating at any point
- Players can manually end the game or switch turns
- Each card is used only once per game session

## File Structure

```
taboo/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Customization

You can easily customize the game by:

- Adding more cards to the `cards` list in `app.py`
- Modifying the number of taboo words per card
- Adjusting the guess log display limit
- Adding new game features or rules

## Notes

- The app uses Streamlit's session state for game management
- Players need to refresh manually or use the refresh button for updates
- The game state persists within a single browser session
- For true multiplayer functionality, consider deploying to a shared server
