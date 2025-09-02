# Wordle Solver

An interactive Wordle solver that uses entropy-based algorithms to suggest optimal guesses.

## Features

- **Entropy-based solving**: Uses information theory to find the best next word
- **Interactive interface**: Color-coded feedback system
- **Real-time suggestions**: Get optimal word suggestions after each guess
- **Historical testing**: Test against all historical Wordle answers

## How to Use

1. Enter color feedback for the suggested word using the color buttons
2. Click "Next Row" to get the next optimal suggestion
3. Continue until you solve the Wordle!

## Technical Details

- Built with Flask and Python
- Uses entropy calculations to maximize information gain
- Processes ~13,000 possible words
- Average solve rate: 3.89 guesses

## Disclaimer

This solver is unofficial and not affiliated with the New York Times or Wordle.
