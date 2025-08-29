from math import log2

POSSIBLE_WORDS = set()

with open("wordle_words.txt", "r") as f:
    for line in f:
        POSSIBLE_WORDS.add(line.strip())

print(f"There are {len(POSSIBLE_WORDS)} possible words")

def getFeedback(guess: str, answer: str) -> str:
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
    return feedback

def filterCandidates(candidates: set, guess: str, feedback: list[int]) -> set:
    """
    This function filters the current candidates based on our guess and feedback.
    """
    filtered = set(word for word in candidates if getFeedback(word, guess) == feedback)
    return filtered

def entropyFunction(candidates: set, guess: str) -> float:
    """
    Compute expected information gain (entropy) if we guess `guess`
    against the current set of possible answers `candidates`.
    """
    feedbackCounts = {}
    for candidate in candidates:
        feedback = getFeedback(guess, candidate)
        key = str(feedback) # List is not hashable so convert to string
        feedbackCounts[key] = feedbackCounts.get(key, 0) + 1

    entropy = 0.0
    N = len(candidates)
    for count in feedbackCounts.values():
        probability = count / N
        entropy -= probability * log2(probability)
    return entropy