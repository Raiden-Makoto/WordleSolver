from math import log2
import numpy as np
import time

POSSIBLE_WORDS = set()

with open("wordle_words.txt", "r") as f:
    for line in f:
        POSSIBLE_WORDS.add(line.strip())

print(f"There are {len(POSSIBLE_WORDS)} possible words")

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
    """

    guesses = []

    # --- First guess: fixed "arise" ---
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

if __name__ == "__main__":
    print("Choose mode:")
    print("1. Interactive Wordle solver (for real gameplay)")
    print("2. Test solver with known word")
    
    while True:
        choice = input("Enter choice (1 or 2): ").strip()
        if choice in ['1', '2']:
            break
        print("Please enter 1 or 2")
    
    if choice == '1':
        playWordle(POSSIBLE_WORDS)
    else:
        starttime = time.time()
        word = input("What word will be the mystery word? ").strip()
        solveWordle(POSSIBLE_WORDS, word, allWords=POSSIBLE_WORDS)
        print(f"Time taken: {time.time() - starttime} seconds.")