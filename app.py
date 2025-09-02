from flask import Flask, render_template, request, jsonify # type: ignore
from entropy import POSSIBLE_WORDS, filterCandidates, bestGuessVectorized, getFeedback

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
