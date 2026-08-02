import random
from django.shortcuts import render, redirect


def generate_problem(wave):
    if wave == 1:
        n1 = random.randint(1, 15)
        n2 = random.randint(1, 15)
        op = '+'
        ans = n1 + n2
    elif wave == 2:
        n1 = random.randint(10, 30)
        n2 = random.randint(1, 15)
        op = '-'
        ans = n1 - n2
    elif wave == 3:
        n1 = random.randint(2, 9)
        n2 = random.randint(2, 9)
        op = '*'
        ans = n1 * n2
    elif wave == 4:
        op = random.choice(['+', '-'])
        n1 = random.randint(15, 50)
        n2 = random.randint(5, 25)
        ans = n1 + n2 if op == '+' else n1 - n2
    else:
        op = random.choice(['+', '-', '*'])
        if op == '*':
            n1 = random.randint(3, 12)
            n2 = random.randint(3, 12)
            ans = n1 * n2
        else:
            n1 = random.randint(20, 80)
            n2 = random.randint(10, 40)
            ans = n1 + n2 if op == '+' else n1 - n2

    return f"{n1} {op} {n2}", ans


def math_defense_game(request):
    if 'castle_hp' not in request.session or 'problem' not in request.session:
        problem_str, correct_ans = generate_problem(1)
        request.session['castle_hp'] = 100
        request.session['monster_hp'] = 40
        request.session['score'] = 0
        request.session['wave'] = 1
        request.session['problem'] = problem_str
        request.session['correct_answer'] = correct_ans
        request.session['log'] = ["Monsters are attacking the castle! Solve math problems to fire cannons!"]
        request.session['game_over'] = False
        request.session['won'] = False

    if request.method == 'POST':
        if 'reset' in request.POST:
            request.session.flush()
            return redirect('math_defense_game')

        user_answer = request.POST.get('answer', '').strip()
        log = request.session.get('log', [])
        correct_ans = request.session.get('correct_answer')
        wave = request.session.get('wave', 1)

        if not request.session.get('game_over') and not request.session.get('won'):
            if user_answer.lstrip('-').isdigit():
                val = int(user_answer)
                if val == correct_ans:
                    damage = random.randint(20, 35)
                    request.session['monster_hp'] -= damage
                    request.session['score'] += 50
                    log.append(f"🎯 CORRECT! Cannon hit monster for {damage} damage! (+50 Score)")

                    if request.session['monster_hp'] <= 0:
                        if wave >= 5:
                            request.session['won'] = True
                            log.append("👑 VICTORY! You defeated the Boss Wave and saved the Kingdom!")
                        else:
                            request.session['wave'] += 1
                            request.session['monster_hp'] = 30 + (request.session['wave'] * 15)
                            log.append(f"⚔️ Wave {wave} Cleared! Advance to Wave {request.session['wave']}!")
                else:
                    dmg = random.randint(10, 22)
                    request.session['castle_hp'] -= dmg
                    log.append(f"💥 WRONG! The correct answer was {correct_ans}. Monster hit castle for {dmg} damage!")
            else:
                log.append("⚠️ Please enter a valid number!")

            if request.session['castle_hp'] <= 0:
                request.session['castle_hp'] = 0
                request.session['game_over'] = True
                log.append("💀 CASTLE DESTROYED! Game Over.")

            if not request.session.get('game_over') and not request.session.get('won'):
                p_str, c_ans = generate_problem(request.session.get('wave', 1))
                request.session['problem'] = p_str
                request.session['correct_answer'] = c_ans

            request.session['log'] = log[-5:]
            request.session.modified = True

        return redirect('math_defense_game')

    context = {
        'castle_hp': request.session.get('castle_hp', 100),
        'monster_hp': request.session.get('monster_hp', 40),
        'score': request.session.get('score', 0),
        'wave': request.session.get('wave', 1),
        'problem': request.session.get('problem', ''),
        'log': request.session.get('log', []),
        'game_over': request.session.get('game_over', False),
        'won': request.session.get('won', False),
    }
    return render(request, 'Math_Defense/index.html', context)