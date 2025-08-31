import random
import sys
import time
from itertools import combinations
from treys import Card, Evaluator, Deck

# Color codes for terminal output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    
    # Card colors
    HEARTS = '\033[91m'  # Red
    DIAMONDS = '\033[91m'  # Red
    SPADES = '\033[97m'  # White
    CLUBS = '\033[97m'  # White

class PokerGame:
    def __init__(self):
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.suits = ['H', 'D', 'S', 'C']
        self.rank_values = {rank: i for i, rank in enumerate(self.ranks)}
        self.deck = None
        self.players = 0
        self.player_cards = []
        self.community_cards = []
        self.player_names = []
        self.folded_players = set()
        self.evaluator = Evaluator()
        
    def create_deck(self):
        """Create and shuffle a new treys deck"""
        self.deck = Deck()
        
    def _draw_one(self, deck=None):
        """Draw exactly one card int from a treys Deck, regardless of return type."""
        d = deck or self.deck
        c = d.draw(1)  # some treys forks return [int] for n=1; others return int for draw()
        if isinstance(c, list):
            if not c:
                raise RuntimeError("Deck is empty")
            return c[0]
        return c
        
    def get_player_count(self):
        """Get number of players from user input"""
        while True:
            try:
                self.players = int(input(f"{Colors.CYAN}Enter number of players (2-10): {Colors.END}"))
                if 2 <= self.players <= 10:
                    break
                print(f"{Colors.YELLOW}Please enter a number between 2 and 10{Colors.END}")
            except ValueError:
                print(f"{Colors.RED}Please enter a valid number{Colors.END}")
        
        self.player_cards = [[] for _ in range(self.players)]
        self.player_names = [f"Player {i+1}" for i in range(self.players)]
        
    def deal_cards(self):
        """Deal 2 cards to each player with visual effects"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}🎯 Dealing hole cards...{Colors.END}")
        time.sleep(1)
        
        for round_num in range(2):
            print(f"{Colors.CYAN}Dealing round {round_num + 1}...{Colors.END}")
            for player_idx in range(self.players):
                card = self._draw_one()
                self.player_cards[player_idx].append(card)
                print(f"  {Colors.GREEN}→{Colors.END} {self.player_names[player_idx]}: {self.format_card(card)}")
                time.sleep(0.3)
            time.sleep(0.5)
            
    def deal_flop(self):
        """Deal the flop (3 community cards) with visual effects"""
        print(f"\n{Colors.BOLD}{Colors.PURPLE}🔥 Dealing the FLOP...{Colors.END}")
        time.sleep(1)
        
        self._draw_one()  # Burn card
        print(f"{Colors.YELLOW}🔥 Burn card{Colors.END}")
        time.sleep(0.5)
        
        for i in range(3):
            card = self._draw_one()
            self.community_cards.append(card)
            print(f"  {Colors.GREEN}→{Colors.END} Community card {i+1}: {self.format_card(card)}")
            time.sleep(0.4)
            
    def deal_turn(self):
        """Deal the turn (1 community card) with visual effects"""
        print(f"\n{Colors.BOLD}{Colors.PURPLE}🔄 Dealing the TURN...{Colors.END}")
        time.sleep(1)
        
        self._draw_one()  # Burn card
        print(f"{Colors.YELLOW}🔥 Burn card{Colors.END}")
        time.sleep(0.5)
        
        card = self._draw_one()
        self.community_cards.append(card)
        print(f"  {Colors.GREEN}→{Colors.END} Turn card: {self.format_card(card)}")
        time.sleep(0.5)
        
    def deal_river(self):
        """Deal the river (1 community card) with visual effects"""
        print(f"\n{Colors.BOLD}{Colors.PURPLE}🌊 Dealing the RIVER...{Colors.END}")
        time.sleep(1)
        
        self._draw_one()  # Burn card
        print(f"{Colors.YELLOW}🔥 Burn card{Colors.END}")
        time.sleep(0.5)
        
        card = self._draw_one()
        self.community_cards.append(card)
        print(f"  {Colors.GREEN}→{Colors.END} River card: {self.format_card(card)}")
        time.sleep(0.5)
        
    def format_card(self, treys_card):
        """Format a treys card with colors and symbols"""
        # Convert treys card to string format first
        card_str = Card.int_to_str(treys_card)
        
        # Extract rank and suit
        rank = card_str[0]
        suit = card_str[1]
        
        # Convert rank to display format
        if rank == 'T':
            rank = '10'
        elif rank == 'J':
            rank = 'J'
        elif rank == 'Q':
            rank = 'Q'
        elif rank == 'K':
            rank = 'K'
        elif rank == 'A':
            rank = 'A'
            
        # Convert suit to uppercase for display
        suit_upper = suit.upper()
        
        suit_symbols = {'H': '♥', 'D': '♦', 'S': '♠', 'C': '♣'}
        suit_colors = {'H': Colors.HEARTS, 'D': Colors.HEARTS, 'S': Colors.SPADES, 'C': Colors.SPADES}
        
        return f"{suit_colors[suit_upper]}{rank}{suit_symbols[suit_upper]}{Colors.END}"
        
    def sort_player_hand(self, hand):
        """Sort player hand by rank (high first), then suit (stable)."""
        def card_sort_key(card):
            # treys: higher rank is a larger int from get_rank_int
            return (-Card.get_rank_int(card), Card.get_suit_int(card))
        return sorted(hand, key=card_sort_key)
        
    def display_game_state(self, round_name):
        """Display current game state with enhanced visuals"""
        print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}{round_name.upper():^60}{Colors.END}")
        print(f"{Colors.BOLD}{'='*60}{Colors.END}")
        
        # Show community cards with visual enhancement
        if self.community_cards:
            community_display = ' '.join([self.format_card(card) for card in self.community_cards])
            print(f"\n{Colors.BOLD}{Colors.YELLOW}Community Cards:{Colors.END}")
            print(f"{Colors.WHITE}┌{'─' * (len(community_display) + 4)}┐{Colors.END}")
            print(f"{Colors.WHITE}│ {community_display} │{Colors.END}")
            print(f"{Colors.WHITE}└{'─' * (len(community_display) + 4)}┘{Colors.END}")
        
        # Show player hands with visual enhancement (sorted)
        print(f"\n{Colors.BOLD}{Colors.BLUE}Player Hands:{Colors.END}")
        for i in range(self.players):
            if i in self.folded_players:
                print(f"{Colors.RED}❌ {self.player_names[i]}: FOLDED{Colors.END}")
            else:
                # Sort the player's hand before displaying
                sorted_hand = self.sort_player_hand(self.player_cards[i])
                cards = ' '.join([self.format_card(card) for card in sorted_hand])
                print(f"{Colors.GREEN}✅ {self.player_names[i]}: {cards}{Colors.END}")
        print()
        
    def get_equity_guesses(self):
        """Get equity guesses from user for each player with enhanced UI"""
        print(f"{Colors.BOLD}{Colors.CYAN}🎯 Guess the equity percentage for each player (0-100):{Colors.END}")
        guesses = {}
        
        for i in range(self.players):
            if i in self.folded_players:
                continue
                
            while True:
                try:
                    guess = float(input(f"{Colors.YELLOW}Enter equity for {self.player_names[i]}: {Colors.END}"))
                    if 0 <= guess <= 100:
                        guesses[i] = guess
                        break
                    print(f"{Colors.RED}Please enter a number between 0 and 100{Colors.END}")
                except ValueError:
                    print(f"{Colors.RED}Please enter a valid number{Colors.END}")
        
        return guesses
        
    def calculate_equity(self):
        """Calculate true equity using treys library"""
        if len(self.community_cards) < 5:
            # Use treys for accurate equity calculation with incomplete board
            active_players = [i for i in range(self.players) if i not in self.folded_players]
            if len(active_players) < 2:
                return {active_players[0]: 100.0} if active_players else {}
                
            # Get player hands (already in treys format)
            player_hands = [self.player_cards[i] for i in active_players]
                
            # Get all dealt cards to exclude from simulation
            dealt_cards = set()
            for hand in player_hands:
                dealt_cards.update(hand)
            dealt_cards.update(self.community_cards)
                
            # Calculate equity using treys
            equity = {}
            simulations = 10000  # More simulations for accuracy
            
            wins = [0] * len(active_players)
            ties = [0] * len(active_players)
            
            for _ in range(simulations):
                # Create a new deck for each simulation
                deck = Deck()
                
                # Deal remaining community cards (avoiding dealt cards)
                sim_board = self.community_cards.copy()
                remaining_cards_needed = 5 - len(sim_board)
                
                for _ in range(remaining_cards_needed):
                    while True:
                        card = self._draw_one(deck)
                        if card not in dealt_cards:
                            sim_board.append(card)
                            break
                    
                # Evaluate each player's hand
                best_score = float('inf')  # Lower is better in treys
                winners = []
                
                for i, hand in enumerate(player_hands):
                    score = self.evaluator.evaluate(hand, sim_board)
                    if score < best_score:
                        best_score = score
                        winners = [i]
                    elif score == best_score:
                        winners.append(i)
                        
                # Award wins/ties
                if len(winners) == 1:
                    wins[winners[0]] += 1
                else:
                    for winner in winners:
                        ties[winner] += 1
                    
            # Calculate equity percentages
            for i, player_idx in enumerate(active_players):
                total_equity = (wins[i] + ties[i] / len(active_players)) / simulations * 100
                equity[player_idx] = total_equity
                
            return equity
        else:
            # All cards are dealt, calculate exact equity
            active_players = [i for i in range(self.players) if i not in self.folded_players]
            if len(active_players) < 2:
                return {active_players[0]: 100.0} if active_players else {}
                
            # Get player hands (already in treys format)
            player_hands = [self.player_cards[i] for i in active_players]
            board = self.community_cards
            
            # Evaluate each player's hand
            best_score = float('inf')
            winners = []
            
            for i, hand in enumerate(player_hands):
                score = self.evaluator.evaluate(hand, board)
                if score < best_score:
                    best_score = score
                    winners = [i]
                elif score == best_score:
                    winners.append(i)
                    
            # Award equity
            equity = {}
            for i, player_idx in enumerate(active_players):
                if i in winners:
                    equity[player_idx] = 100.0 / len(winners)
                else:
                    equity[player_idx] = 0.0
                    
            return equity
            
    def show_results(self, guesses, true_equity):
        """Show comparison between guesses and true equity with enhanced visuals"""
        print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.PURPLE}{'EQUITY RESULTS':^60}{Colors.END}")
        print(f"{Colors.BOLD}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}{'Player':<15} {'Your Guess':<12} {'True Equity':<12} {'Difference':<12} {'Accuracy':<10}{Colors.END}")
        print(f"{Colors.WHITE}{'-' * 60}{Colors.END}")
        
        total_accuracy = 0
        valid_guesses = 0
        
        for i in range(self.players):
            if i in self.folded_players:
                continue
            guess = guesses.get(i, 0)
            true = true_equity.get(i, 0)
            diff = abs(guess - true)
            
            # Calculate accuracy percentage
            if true > 0:
                accuracy = max(0, 100 - (diff / true * 100))
            else:
                accuracy = 100 if guess == 0 else 0
                
            total_accuracy += accuracy
            valid_guesses += 1
            
            # Color code the accuracy
            if accuracy >= 80:
                accuracy_color = Colors.GREEN
            elif accuracy >= 60:
                accuracy_color = Colors.YELLOW
            else:
                accuracy_color = Colors.RED
                
            print(f"{self.player_names[i]:<15} {guess:<12.1f} {true:<12.1f} {diff:<12.1f} {accuracy_color}{accuracy:<10.1f}%{Colors.END}")
            
        if valid_guesses > 0:
            avg_accuracy = total_accuracy / valid_guesses
            print(f"\n{Colors.BOLD}{Colors.CYAN}Average Accuracy: {avg_accuracy:.1f}%{Colors.END}")
            
    def reset_game(self):
        """Reset the game state for a new round"""
        print(f"\n{Colors.BOLD}{Colors.PURPLE}🔄 Resetting game...{Colors.END}")
        time.sleep(0.5)
        
        # Cool terminal effect - "shuffling" animation
        print(f"{Colors.CYAN}🎰 Shuffling the deck...{Colors.END}")
        for i in range(3):
            print(f"{Colors.YELLOW}  {'🃏' * (i+1)}{Colors.END}")
            time.sleep(0.3)
        print(f"{Colors.GREEN}  🃏🃏🃏 Ready!{Colors.END}")
        time.sleep(0.5)
        
        # Reset game state
        self.deck = Deck()
        self.player_cards = []
        self.community_cards = []
        self.folded_players = set()
        
    def fold_players(self):
        """Allow user to fold players with enhanced UI"""
        # Skip folding if only one player is left
        active_players = [i for i in range(self.players) if i not in self.folded_players]
        if len(active_players) <= 1:
            print(f"\n{Colors.YELLOW}🎯 Only {len(active_players)} player(s) remaining - skipping fold phase{Colors.END}")
            time.sleep(1)
            return
            
        print(f"\n{Colors.BOLD}{Colors.YELLOW}🎯 Which players would you like to fold?{Colors.END}")
        print(f"{Colors.CYAN}Enter player numbers separated by spaces, or 'none': {Colors.END}")
        response = input().strip().lower()
        
        if response == 'none':
            return
            
        try:
            fold_indices = [int(x) - 1 for x in response.split()]
            for idx in fold_indices:
                if 0 <= idx < self.players and idx not in self.folded_players:
                    self.folded_players.add(idx)
                    print(f"{Colors.RED}❌ {self.player_names[idx]} has been folded{Colors.END}")
                    time.sleep(0.5)
        except ValueError:
            print(f"{Colors.YELLOW}Invalid input, no players folded{Colors.END}")
            
    def ask_play_again(self):
        """Ask if user wants to play another game"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}🎮 Would you like to play another game?{Colors.END}")
        while True:
            response = input(f"{Colors.YELLOW}Enter 'y' for yes or 'n' for no: {Colors.END}").strip().lower()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            else:
                print(f"{Colors.RED}Please enter 'y' or 'n'{Colors.END}")
                
    def show_winner(self):
        """Show the final winner with enhanced visuals"""
        if len(self.community_cards) == 5:
            equity = self.calculate_equity()
            winners = [i for i, eq in equity.items() if eq > 0 and i not in self.folded_players]
            
            print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
            print(f"{Colors.BOLD}{Colors.GREEN}{'🏆 FINAL RESULTS 🏆':^60}{Colors.END}")
            print(f"{Colors.BOLD}{'='*60}{Colors.END}")
            
            if winners:
                if len(winners) == 1:
                    winner = winners[0]
                    print(f"\n{Colors.BOLD}{Colors.GREEN}🎉 {self.player_names[winner]} WINS! 🎉{Colors.END}")
                    # Evaluate winning hand (already in treys format)
                    hand = self.player_cards[winner]
                    board = self.community_cards
                    score = self.evaluator.evaluate(hand, board)
                    hand_class = self.evaluator.get_rank_class(score)
                    hand_name = self.evaluator.class_to_string(hand_class)
                    print(f"{Colors.CYAN}Winning hand: {Colors.BOLD}{hand_name}{Colors.END}")
                    
                    # Show winning cards
                    winning_cards = ' '.join([self.format_card(card) for card in hand])
                    print(f"{Colors.YELLOW}Winning cards: {winning_cards}{Colors.END}")
                else:
                    print(f"\n{Colors.BOLD}{Colors.YELLOW}🤝 It's a tie between:{Colors.END}")
                    for winner in winners:
                        print(f"  {Colors.GREEN}🏆 {self.player_names[winner]}{Colors.END}")
            else:
                print(f"\n{Colors.RED}❌ No active players remaining!{Colors.END}")
                
    def play_game(self):
        """Main game loop with enhanced visuals and timing"""
        while True:  # Main game loop
            print(f"\n{Colors.BOLD}{Colors.CYAN}{'🎰 WELCOME TO POKER EQUITY GUESSING GAME 🎰':^60}{Colors.END}")
            print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.END}")
            time.sleep(1)
            
            self.get_player_count()
            self.create_deck()
            
            print(f"\n{Colors.BOLD}{Colors.GREEN}🎯 Starting new game with {self.players} players...{Colors.END}")
            time.sleep(1)
            
            self.deal_cards()
            
            # Pre-flop
            self.display_game_state("Pre-flop")
            time.sleep(2)  # Give time to process
            
            # Flop
            self.deal_flop()
            self.display_game_state("Flop")
            time.sleep(2)  # Give time to process
            
            guesses = self.get_equity_guesses()
            true_equity = self.calculate_equity()
            self.show_results(guesses, true_equity)
            time.sleep(2)  # Give time to review results
            
            self.fold_players()
            
            # Turn
            self.deal_turn()
            self.display_game_state("Turn")
            time.sleep(2)  # Give time to process
            
            guesses = self.get_equity_guesses()
            true_equity = self.calculate_equity()
            self.show_results(guesses, true_equity)
            time.sleep(2)  # Give time to review results
            
            self.fold_players()
            
            # River
            self.deal_river()
            self.display_game_state("River")
            time.sleep(2)  # Give time to process
            
            guesses = self.get_equity_guesses()
            true_equity = self.calculate_equity()
            self.show_results(guesses, true_equity)
            time.sleep(2)  # Give time to review results
            
            self.show_winner()
            time.sleep(1)
            
            print(f"\n{Colors.BOLD}{Colors.CYAN}🎉 Thanks for playing! 🎉{Colors.END}")
            
            # Ask if they want to play again
            if not self.ask_play_again():
                print(f"\n{Colors.BOLD}{Colors.GREEN}👋 Thanks for playing! Goodbye! 👋{Colors.END}")
                break
                
            # Reset for next game
            self.reset_game()

if __name__ == "__main__":
    game = PokerGame()
    game.play_game()