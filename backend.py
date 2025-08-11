"""This module defines the backend logic for the Taboo game."""

from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum


import streamlit as st

MIN_PLAYERS = 4
NUMBER_OF_TABOO_WORDS = 5


class Team(Enum):
    """Enum to represent the two teams in the game."""

    A = "Team A"
    B = "Team B"
    U = "Unassigned"


class Role(Enum):
    """Enum to represent the roles a player can have in the game."""

    LEADER = "leader"
    CHECKER = "checker"
    CARD_MAKER = "card_maker"
    GUESSER = "guesser"
    UNASSIGNED = "unassigned"


@dataclass
class Card:
    """Data class to represent a card in the game."""

    word: str
    taboo_words: list[str]
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Ensure taboo words are unique."""
        self.taboo_words = list(set(self.taboo_words))
        if len(self.taboo_words) > NUMBER_OF_TABOO_WORDS:
            self.taboo_words = self.taboo_words[:NUMBER_OF_TABOO_WORDS]

        if len(self.taboo_words) < NUMBER_OF_TABOO_WORDS:
            st.error(
                f"Card '{self.word}' has less than {NUMBER_OF_TABOO_WORDS} taboo words. "
                "Please ensure it has enough taboo words."
            )


@dataclass
class Player:
    """Data class to represent a player in the game."""

    name: str
    team: Team = field(default=Team.U)
    role: Role = field(default=Role.UNASSIGNED)

    is_cheating: bool = field(default=False)
    score: int = field(default=0)

    @property
    def is_leader(self) -> bool:
        """Check if the player is a leader."""
        return self.role == Role.LEADER

    @property
    def is_checker(self) -> bool:
        """Check if the player is a checker."""
        return self.role == Role.CHECKER

    @property
    def is_card_maker(self) -> bool:
        """Check if the player is a card maker."""
        return self.role == Role.CARD_MAKER

    @property
    def is_guesser(self) -> bool:
        """Check if the player is a guesser."""
        return self.role == Role.GUESSER


@dataclass
class Turn:
    """Data class to represent a turn in the game."""

    card: Card
    hints: list[str] = field(default_factory=list)
    hinters: list[Player] = field(default_factory=list)
    guesses: list[str] = field(default_factory=list)
    guessers: list[Player] = field(default_factory=list)

    max_guesses: int = 15

    def add_hint(self, hint: str, player: Player):
        """Add a hint to the turn."""
        self.hints.append(hint)
        self.hinters.append(player)

    def add_guess(self, guess: str, player: Player):
        """Add a guess to the turn."""
        self.guesses.append(guess)
        self.guessers.append(player)

    @property
    def successfully_guessed(self) -> bool:
        """Check if the card was successfully guessed."""
        return self.guesses and self.guesses[-1] == self.card.word

    @property
    def unsuccessfully_guessed(self) -> bool:
        """Check if the card was unsuccessfully guessed."""
        return not self.successfully_guessed and len(self.guesses) >= self.max_guesses

    @property
    def is_ongoing(self) -> bool:
        """Check if the turn is ongoing."""
        return (
            not self.successfully_guessed
            and not self.unsuccessfully_guessed
            and len(self.guesses) < self.max_guesses
        )


@dataclass
class Message:
    """Data class to represent a message in the game chat."""

    sender: Player
    content: str


@dataclass
class Chat:
    """Data class to represent the game chat."""

    messages: list[Message] = field(default_factory=list)

    def add_message(self, sender: Player, content: str):
        """Add a message to the chat."""
        message = Message(sender=sender, content=content)
        self.messages.append(message)


@dataclass
class Game:
    """Data class to represent the game state."""

    players: list[Player] = field(default_factory=list)
    current_round: int = 1
    current_turn: int = 1
    max_rounds: int = 5
    ongoing: bool = False
    turns: list[Turn] = field(default_factory=list)
    chat: Chat = field(default_factory=Chat)

    def add_player(self, player: Player):
        """Add a player to the game."""
        self.players.append(player)

    def next_turn(self):
        """Advance to the next turn in the game."""
        self.current_turn += 1
        if self.current_turn >= self.max_turns:
            st.warning("Game over! No more turns left.")
            return False

        if (self.current_turn - 1) % 2 == 0:
            self.current_round += 1
            if self.current_round > self.max_rounds:
                st.warning("Game over! Maximum rounds reached.")
                return False

        self.ongoing = False
        for player in self.players:
            player.role = Role.UNASSIGNED

        return True

    @property
    def max_turns(self) -> int:
        """Calculate the maximum number of turns based on the number of players."""
        return self.max_rounds * 2

    @property
    def checking_team(self) -> Team:
        """Determine which team is currently checking."""
        return Team.A if self.current_turn % 2 == 0 else Team.B

    @property
    def guessing_team(self) -> Team:
        """Determine which team is currently guessing."""
        return Team.B if self.current_turn % 2 == 0 else Team.A

    def check_teams(self):
        """Check if both teams have players assigned."""
        team_a_players = [p for p in self.players if p.team == Team.A]
        team_b_players = [p for p in self.players if p.team == Team.B]

        if not team_a_players or not team_b_players:

            st.error("Both teams must have players assigned to start the game.")
            return False

        card_makers = [p for p in self.players if p.role == Role.CARD_MAKER]
        if len(card_makers) != 1:
            st.error("There must be exactly one card maker assigned.")
            return False

        leaders = [p for p in self.players if p.role == Role.LEADER]
        if len(leaders) != 1:
            st.error("There must be exactly one leader assigned.")
            return False

        checkers = [p for p in self.players if p.role == Role.CHECKER]
        if len(checkers) < 1:
            st.error("At least one checker must be assigned.")
            return False

        guessers = [p for p in self.players if p.role == Role.GUESSER]
        if len(guessers) < 1:
            st.error("At least one guesser must be assigned.")
            return False

        card_maker = card_makers[0]
        if card_maker.team != self.checking_team:
            st.error(f"Card maker must be on {self.checking_team.value}.")
            return False

        leader = leaders[0]
        if leader.team != self.guessing_team:
            st.error(f"Leader must be on {self.guessing_team.value}.")
            return False

        if len(self.players) < MIN_PLAYERS:
            st.error(f"At least {MIN_PLAYERS} players are required to start the game!")
            return False

        unassigned_players = [p for p in self.players if p.team == Team.U]
        if unassigned_players:
            st.error("All players must be assigned to a team before starting the game.")
            return False

        unassigned_roles = [p for p in self.players if p.role == Role.UNASSIGNED]
        if unassigned_roles:
            st.error("All players must have a role assigned before starting the game.")
            return False

        return True

    def start_game(self):
        """Start the game if all conditions are met."""
        if not self.check_teams():
            st.error("Cannot start the game. Please check team and role assignments.")
            return False

        self.ongoing = True
        st.success("Game started successfully!")
        return True

    def make_card(self, word: str, taboo_words: list[str]):
        """Create a new card and add it to the game."""
        card = Card(word=word, taboo_words=taboo_words)
        turn = Turn(card=card)
        self.turns.append(turn)


@st.cache_resource
def get_shared_game():
    """Get or create a shared game instance that persists across all users and sessions."""
    return Game()
