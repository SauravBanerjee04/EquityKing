# EquityKing 🃏

A Python-based interactive poker equity guessing game that helps you practice and improve your poker equity estimation skills. Test your knowledge of hand probabilities at each stage of a Texas Hold'em hand!

## 🎮 Game Overview

EquityKing is an educational poker tool that simulates a complete Texas Hold'em hand and challenges you to guess the equity (winning probability) for each player at different stages:

- **Pre-flop**: After dealing hole cards
- **Flop**: After 3 community cards
- **Turn**: After 4th community card  
- **River**: After 5th community card

After each stage, you'll see how accurate your equity estimates were compared to the true mathematical probabilities.

## ✨ Features

- **Interactive Gameplay**: Choose number of players (2-10) via command line or input
- **Complete Poker Flow**: Pre-flop → Flop → Turn → River progression
- **Equity Guessing**: Estimate winning percentages for each player
- **Accurate Calculations**: Uses professional-grade `treys` library for precise equity calculation
- **Player Folding**: Option to fold players between betting rounds
- **Hand Evaluation**: Complete poker hand ranking system
- **Results Comparison**: Shows your guesses vs. true equity with differences
- **Winner Determination**: Reveals final winner and winning hand type

## 🛠️ Technologies Used

- **Python 3.x**: Core programming language
- **treys**: Fast, accurate poker hand evaluation library
- **itertools**: For card combinations and simulations
- **random**: For deck shuffling and card dealing

## 📋 Requirements

- Python 3.6 or higher
- Virtual environment (recommended)

## 🚀 Installation & Setup

### Option 1: Using Virtual Environment (Recommended)

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd EquityKing
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv pokerenv
   source pokerenv/bin/activate  # On Windows: pokerenv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install treys
   ```

### Option 2: Global Installation

```bash
pip install treys
```

## 🎯 How to Play

### Starting the Game

**Option 1 - Command Line Argument:**
```bash
python poker.py 4  # Start with 4 players
```

**Option 2 - Interactive Input:**
```bash
python poker.py  # Will prompt for player count
```

### Game Flow

1. **Player Selection**: Choose 2-10 players
2. **Pre-flop**: View each player's hole cards
3. **Flop**: 
   - 3 community cards are dealt
   - Guess equity for each player (0-100%)
   - See true equity vs. your guess
   - Option to fold players
4. **Turn**:
   - 4th community card dealt
   - Guess equity again
   - Compare results
   - Fold players if desired
5. **River**:
   - 5th community card dealt
   - Final equity guess
   - See final results
6. **Winner**: Final winner and hand type revealed

### Example Game Session

```
Welcome to Poker Equity Guessing Game!
==================================================

Enter number of players (2-10): 3

==================================================
PRE-FLOP
==================================================
Player 1: AH KD
Player 2: QS JC  
Player 3: 2H 7C

==================================================
FLOP
==================================================
Community cards: 5H TD 9C
Player 1: AH KD
Player 2: QS JC
Player 3: 2H 7C

Guess the equity percentage for each player (0-100):
Enter equity for Player 1: 45
Enter equity for Player 2: 35
Enter equity for Player 3: 20

==================================================
EQUITY RESULTS
==================================================
Player          Your Guess   True Equity  Difference
--------------------------------------------------
Player 1        45.0        42.3         2.7
Player 2        35.0        38.1         3.1
Player 3        20.0        19.6         0.4
```

## 🔧 How It Works

### Core Components

1. **PokerGame Class**: Main game controller
2. **Card Management**: Handles deck creation, shuffling, and dealing
3. **Equity Calculation**: Uses `treys` library for accurate probability calculation
4. **Hand Evaluation**: Professional-grade poker hand ranking
5. **User Interface**: Interactive command-line interface

### Equity Calculation

The game uses the `treys` library for equity calculation:

- **Incomplete Board** (Flop/Turn): Monte Carlo simulation with 10,000 iterations
- **Complete Board** (River): Exact calculation using all possible hand combinations
- **Hand Evaluation**: 7-card to 5-card hand evaluation for optimal hand selection

### Card Format

- **Input Format**: `'AH'` (Ace of Hearts), `'KD'` (King of Diamonds)
- **Internal Conversion**: Converts to treys format (`'Ah'`, `'Kd'`) for evaluation
- **Display**: Shows cards in readable format

## 📊 Learning Benefits

- **Improve Equity Estimation**: Practice guessing hand probabilities
- **Understand Hand Strength**: Learn relative hand rankings
- **Develop Intuition**: Build poker instincts through repeated practice
- **Study Board Texture**: Analyze how community cards affect equity
- **Practice Decision Making**: Make fold/call decisions based on equity

## 🎯 Tips for Better Play

1. **Start Simple**: Begin with 2-3 players to focus on basic equity concepts
2. **Study Patterns**: Notice how equity changes with different board textures
3. **Practice Regularly**: Consistent practice improves estimation accuracy
4. **Analyze Mistakes**: Pay attention to where your guesses differ most from true equity
5. **Consider Position**: Think about how position affects hand strength

## 🔍 Troubleshooting

### Common Issues

**Import Error for treys:**
```bash
pip install treys
```

**Virtual Environment Not Activated:**
```bash
source pokerenv/bin/activate  # On Windows: pokerenv\Scripts\activate
```

**Invalid Player Count:**
- Must be between 2 and 10 players
- Enter a valid integer

## 🤝 Contributing

Feel free to contribute improvements:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **treys library**: For fast and accurate poker hand evaluation
- **Poker community**: For inspiration and feedback

---

**Happy practicing! May your equity estimates be ever accurate! 🃏✨**
