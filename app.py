from flask import Flask, render_template, request, jsonify # type: ignore
from math import log2
import numpy as np # type: ignore
import time

POSSIBLE_WORDS = set()

with open("wordle_words.txt", "r") as f:
    for line in f:
        POSSIBLE_WORDS.add(line.strip())

# There are {len(POSSIBLE_WORDS)} possible words loaded

def getFeedback(guess: str, answer: str) -> int:
    """
    This function returns the feedback for a given guess and answer.
    The feedback is a list of 5 integers, where 0 means grey, 1 means yellow, and 2 means green.
    """
    chars = list(answer)
    feedback = [2 if guess[i] == chars[i] else 0 for i in range(5)]
    for i in range(5):
        if feedback[i] == 0 and guess[i] in chars:
            feedback[i] = 1  # yellow
            chars[chars.index(guess[i])] = None  # consume letter
    optimized = 0
    for f in feedback:
        optimized = 3 * optimized + f
    return optimized # optimized encoding of feedback stores guesses as decimal numbers

def filterCandidates(candidates: set, guess: str, feedback: int) -> set:
    """
    This function filters the current candidates based on our guess and feedback.
    """
    filtered = set(word for word in candidates if getFeedback(guess, word) == feedback)
    return filtered

def bestGuessVectorized(candidates: set, allWords: set):
    """
    This function returns the best guess for the next round.
    It uses a vectorized approach to compute the best guess.
    """
    bestWord = None
    bestEntropy = -np.inf
    L = len(candidates)
    for guess in allWords:
        counts = np.zeros(3**5)
        for answer in candidates:
            counts[getFeedback(guess, answer)] += 1
        # Filter out zero counts to avoid log(0)
        nonzero_counts = counts[counts > 0]
        probabilities = nonzero_counts / L
        entropy = -np.sum(probabilities * np.log2(probabilities))
        if entropy > bestEntropy:
            bestEntropy = entropy
            bestWord = guess
    return bestWord

def solveWordle(candidates: set[str], answer: str, maxGuesses: int = 6, allWords: set[str] = None):
    """
    Solve Wordle by always starting with 'arise' and then using entropy-based scoring.
    This has an average solve of 3.89 guesses.
    """

    guesses = []

    # --- First guess: fixed word ---
    firstGuess = "arise"
    guesses.append(firstGuess)
    feedback = getFeedback(firstGuess, answer)
    print(f"Round 1: guess = {firstGuess}, feedback = {feedback}")

    if feedback == 242:
        print("Solved in 1 guess!")
        return guesses

    candidates = filterCandidates(candidates, firstGuess, feedback)
    print(f"After first guess, {len(candidates)} candidates remain")

    # --- Remaining guesses ---
    for i in range(2, maxGuesses + 1):
        if len(candidates) == 0:
            print("No candidates remaining!")
            break
        if len(candidates) == 1:
            # If only one candidate remains, just guess it
            nextGuess = list(candidates)[0]
        else:
            nextGuess = bestGuessVectorized(candidates, allWords if allWords else candidates)
        guesses.append(nextGuess)
        feedback = getFeedback(nextGuess, answer)
        print(f"Round {i}: guess = {nextGuess}, feedback = {feedback}")

        if feedback == 242:
            print(f"Solved in {i} guesses!")
            return guesses

        candidates = filterCandidates(candidates, nextGuess, feedback)
        print(f"After round {i}, {len(candidates)} candidates remain")
    print(f"Failed to solve Wordle.")
    return guesses

def playWordle(allWords: set[str], maxGuesses: int = 6):
    """
    Interactive Wordle solver for real gameplay.
    """
    candidates = allWords.copy()
    guesses = []
    
    print("Welcome to the Wordle Solver!")
    print("Enter feedback as 5 characters: 'g' for green, 'y' for yellow, 'b' for black/grey")
    print("Example: 'gybbb' means first letter is green, second is yellow, rest are black")
    print()
    
    # First guess: always "arise"
    firstGuess = "arise"
    print(f"Suggested guess 1: {firstGuess.upper()}")
    
    while True:
        feedback_str = input("Enter feedback for this guess (or 'q' to quit): ").strip().lower()
        if feedback_str == 'q':
            return
        if len(feedback_str) == 5 and all(c in 'gyb' for c in feedback_str):
            break
        print("Invalid input. Please enter exactly 5 characters using only 'g', 'y', 'b'")
    
    # Convert feedback to our integer format
    feedback_list = []
    for c in feedback_str:
        if c == 'g': feedback_list.append(2)
        elif c == 'y': feedback_list.append(1)
        else: feedback_list.append(0)
    
    feedback = 0
    for f in feedback_list:
        feedback = 3 * feedback + f
    
    guesses.append(firstGuess)
    
    if feedback == 242:  # All green
        print("Congratulations! Solved in 1 guess!")
        return
    
    candidates = filterCandidates(candidates, firstGuess, feedback)
    print(f"Remaining candidates: {len(candidates)}")
    
    # Remaining guesses
    for round_num in range(2, maxGuesses + 1):
        if len(candidates) == 0:
            print("No valid words remain. There might be an error in the feedback.")
            return
        
        if len(candidates) == 1:
            nextGuess = list(candidates)[0]
        else:
            nextGuess = bestGuessVectorized(candidates, allWords)
        
        print(f"\nSuggested guess {round_num}: {nextGuess.upper()}")
        
        while True:
            feedback_str = input("Enter feedback for this guess (or 'q' to quit): ").strip().lower()
            if feedback_str == 'q':
                return
            if len(feedback_str) == 5 and all(c in 'gyb' for c in feedback_str):
                break
            print("Invalid input. Please enter exactly 5 characters using only 'g', 'y', 'b'")
        
        # Convert feedback to our integer format
        feedback_list = []
        for c in feedback_str:
            if c == 'g': feedback_list.append(2)
            elif c == 'y': feedback_list.append(1)
            else: feedback_list.append(0)
        
        feedback = 0
        for f in feedback_list:
            feedback = 3 * feedback + f
        
        guesses.append(nextGuess)
        
        if feedback == 242:  # All green
            print(f"Congratulations! Solved in {round_num} guesses!")
            return
        
        candidates = filterCandidates(candidates, nextGuess, feedback)
        print(f"Remaining candidates: {len(candidates)}")
    
    print("Reached maximum guesses. Better luck next time!")

def testSolverOnHistoricalWordles(allWords: set[str], testWords: list[str], maxGuesses: int = 6):
    """
    Test the solver against a list of historical Wordle answers to measure success rate.
    """
    results = []
    total_guesses = 0
    successes = 0
    
    print(f"Testing solver on {len(testWords)} historical Wordle answers...")
    print("=" * 60)
    
    for i, word in enumerate(testWords, 1):
        print(f"Test {i}/{len(testWords)}: {word.upper()}")
        
        # Use the existing solveWordle function but capture results
        candidates = allWords.copy()
        guesses = []
        solved = False
        
        # First guess: always "arise"
        firstGuess = "arise"
        guesses.append(firstGuess)
        feedback = getFeedback(firstGuess, word)
        
        if feedback == 242:  # All green
            solved = True
            num_guesses = 1
        else:
            candidates = filterCandidates(candidates, firstGuess, feedback)
            
            # Remaining guesses
            for round_num in range(2, maxGuesses + 1):
                if len(candidates) == 0:
                    break
                
                if len(candidates) == 1:
                    nextGuess = list(candidates)[0]
                else:
                    nextGuess = bestGuessVectorized(candidates, allWords)
                
                guesses.append(nextGuess)
                feedback = getFeedback(nextGuess, word)
                
                if feedback == 242:  # All green
                    solved = True
                    num_guesses = round_num
                    break
                
                candidates = filterCandidates(candidates, nextGuess, feedback)
            else:
                num_guesses = maxGuesses
        
        # Record results
        result = {
            'word': word,
            'solved': solved,
            'guesses': num_guesses,
            'guess_sequence': guesses[:num_guesses] if solved else guesses
        }
        results.append(result)
        
        if solved:
            successes += 1
            total_guesses += num_guesses
            print(f"  ✓ Solved in {num_guesses} guesses: {' → '.join(g.upper() for g in result['guess_sequence'])}")
        else:
            print(f"  ✗ Failed to solve: {' → '.join(g.upper() for g in result['guess_sequence'])}")
    
    # Calculate and display statistics
    success_rate = (successes / len(testWords)) * 100
    avg_guesses = total_guesses / successes if successes > 0 else 0
    
    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)
    print(f"Total tests: {len(testWords)}")
    print(f"Successes: {successes}")
    print(f"Failures: {len(testWords) - successes}")
    print(f"Success rate: {success_rate:.1f}%")
    print(f"Average guesses (for successful solves): {avg_guesses:.2f}")
    
    # Guess distribution
    guess_distribution = {i: 0 for i in range(1, maxGuesses + 1)}
    for result in results:
        if result['solved']:
            guess_distribution[result['guesses']] += 1
    
    print(f"\nGuess distribution:")
    for guesses in range(1, maxGuesses + 1):
        count = guess_distribution[guesses]
        percentage = (count / successes) * 100 if successes > 0 else 0
        print(f"  {guesses} guesses: {count:3d} ({percentage:4.1f}%)")
    
    return results

def loadHistoricalWordles(filename: str = "all_historical_wordles.txt"):
    """
    Load historical Wordle answers from a file.
    """
    try:
        with open(filename, 'r') as f:
            words = [line.strip().lower() for line in f if line.strip()]
        print(f"Loaded {len(words)} historical Wordle answers from {filename}")
        return words
    except FileNotFoundError:
        print(f"File {filename} not found. You can create it with historical Wordle answers.")
        return []

app = Flask(__name__)

# Global state to track the game
game_state = {
    'candidates': POSSIBLE_WORDS.copy(),
    'current_word': 'arise',
    'guesses': [],
    'round': 0
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_next_word', methods=['POST'])
def get_next_word():
    global game_state
    
    data = request.json
    feedback_string = data.get('feedback', '')
    
    # Convert feedback string (byg) to our integer format
    feedback_int = 0
    for char in feedback_string:
        if char == 'b':
            feedback_int = feedback_int * 3 + 0  # absent
        elif char == 'y':
            feedback_int = feedback_int * 3 + 1  # present
        elif char == 'g':
            feedback_int = feedback_int * 3 + 2  # correct
    
    # Filter candidates based on feedback
    current_word = game_state['current_word']
    game_state['candidates'] = filterCandidates(game_state['candidates'], current_word, feedback_int)
    game_state['guesses'].append(current_word)
    game_state['round'] += 1
    
    # Get next best word
    if len(game_state['candidates']) == 0:
        return jsonify({'word': 'ERROR', 'candidates_remaining': 0})
    elif len(game_state['candidates']) == 1:
        next_word = list(game_state['candidates'])[0]
    else:
        next_word = bestGuessVectorized(game_state['candidates'], POSSIBLE_WORDS)
    
    game_state['current_word'] = next_word
    
    return jsonify({
        'word': next_word.upper(),
        'candidates_remaining': len(game_state['candidates'])
    })

@app.route('/reset_game', methods=['POST'])
def reset_game():
    global game_state
    game_state = {
        'candidates': POSSIBLE_WORDS.copy(),
        'current_word': 'arise',
        'guesses': [],
        'round': 0
    }
    return jsonify({'word': 'ARISE'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7860)
