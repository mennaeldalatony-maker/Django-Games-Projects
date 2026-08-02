import random
from django.shortcuts import render, redirect

WORDS = [
    "PYTHON", "DJANGO", "CIPHER", "CODING", "SERVER", 
    "BUFFER", "CLIENT", "BINARY", "SCRIPT", "OBJECT"
]

def word_cipher_game(request):
    if 'target_word' not in request.session or 'attempts' not in request.session:
        request.session['target_word'] = random.choice(WORDS)
        request.session['attempts'] = []
        request.session['game_over'] = False
        request.session['won'] = False
        request.session['message'] = "Enter a 6-letter word to break the cipher!"

    if request.method == 'POST':
        if 'reset' in request.POST:
            request.session.flush()
            return redirect('word_cipher_game')

        guess = request.POST.get('guess', '').strip().upper()
        target = request.session.get('target_word', 'PYTHON')
        attempts = request.session.get('attempts', [])
        game_over = request.session.get('game_over', False)

        if not game_over and len(attempts) < 6:
            if len(guess) != 6 or not guess.isalpha():
                request.session['message'] = "⚠️ Please enter a valid 6-letter English word!"
            else:
                feedback = []
                for i in range(6):
                    char = guess[i]
                    if char == target[i]:
                        status = 'correct'     # Green
                    elif char in target:
                        status = 'present'     # Yellow
                    else:
                        status = 'absent'      # Gray
                    feedback.append({'letter': char, 'status': status})

                attempts.append({'guess_word': guess, 'feedback': feedback})
                request.session['attempts'] = attempts

                if guess == target:
                    request.session['won'] = True
                    request.session['game_over'] = True
                    request.session['message'] = f"🎉 ACCESS GRANTED! You cracked the cipher: {target}!"
                elif len(attempts) >= 6:
                    request.session['game_over'] = True
                    request.session['message'] = f"💀 ACCESS DENIED! The cipher word was: {target}."
                else:
                    request.session['message'] = f"Attempt {len(attempts)}/6 recorded. Keep guessing!"

            request.session.modified = True

        return redirect('word_cipher_game')

    context = {
        'attempts': request.session.get('attempts', []),
        'remaining_attempts': 6 - len(request.session.get('attempts', [])),
        'game_over': request.session.get('game_over', False),
        'won': request.session.get('won', False),
        'message': request.session.get('message', ''),
    }
    return render(request, 'Word_Cipher/index.html', context)