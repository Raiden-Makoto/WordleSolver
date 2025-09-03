# [Wordle Solver](https://42cummer-entropywordlesolver.hf.space/) 🧩

An intelligent Wordle solver that uses entropy-based algorithms to suggest optimal guesses in real-time.

## ✨ Features

- **🧠 Entropy-based solving**: Uses information theory to maximize information gain with each guess
- **🎨 Interactive interface**: Intuitive color-coded feedback system (Green/Yellow/Gray)
- **⚡ Real-time suggestions**: Get optimal word suggestions instantly after each guess
- **📊 Historical testing**: Tested against all historical Wordle answers
- **🔄 Game reset**: Start fresh anytime with the reset button
- **📱 Responsive design**: Works on desktop and mobile devices

## 🎮 How to Use

1. **Start with "ARISE"**: The solver always suggests "ARISE" as the first guess
2. **Enter feedback**: Use the color buttons to indicate the result:
   - 🟩 **Green**: Letter is correct and in the right position
   - 🟨 **Yellow**: Letter is in the word but wrong position
   - ⬛ **Gray**: Letter is not in the word
3. **Get next suggestion**: Click "Next Row" to receive the optimal next guess
4. **Continue solving**: Repeat until you find the word!

## 🛠️ Technical Details

- **Backend**: Flask (Python)
- **Frontend**: HTML/CSS/JavaScript
- **Algorithm**: Entropy-based information maximization
- **Word database**: ~13,000 possible 5-letter words
- **Performance**: Average solve rate of 3.89 guesses
- **Deployment**: Docker containerized for easy deployment

## 🧪 Testing

The solver has been tested against all historical Wordle answers with:
- **Success rate**: ~99%+ 
- **Average guesses**: 3.80
- **Maximum guesses**: 6

## ⚠️ Disclaimer

This solver is unofficial and not affiliated with the New York Times or Wordle. 
---

**Happy solving! 🎯**
