import random
from django.shortcuts import render, redirect


def dungeon_game(request):
    # Initialize session keys if new session or missing keys
    if 'hp' not in request.session or 'won' not in request.session:
        request.session['hp'] = 100
        request.session['monster_hp'] = 50
        request.session['gold'] = 0
        request.session['room'] = 1
        request.session['log'] = ["You entered the dark dungeon. A monster approaches!"]
        request.session['game_over'] = False
        request.session['won'] = False

    if request.method == 'POST':
        if 'reset' in request.POST:
            request.session.flush()
            return redirect('dungeon_game')

        action = request.POST.get('action')
        log = request.session.get('log', [])

        game_over = request.session.get('game_over', False)
        won = request.session.get('won', False)

        if not game_over and not won:
            if action == 'attack':
                damage = random.randint(15, 30)
                request.session['monster_hp'] -= damage
                log.append(f"You hit the monster for {damage} damage!")

                if request.session['monster_hp'] <= 0:
                    earned = random.randint(20, 50)
                    request.session['gold'] += earned

                    if request.session['room'] >= 5:
                        request.session['won'] = True
                        log.append("🎉 VICTORY! You defeated the Boss and escaped the dungeon!")
                    else:
                        request.session['room'] += 1
                        request.session['monster_hp'] = 40 + (request.session['room'] * 15)
                        log.append(f"Victory! Found {earned} gold. Moved to Room {request.session['room']}.")
                else:
                    monster_damage = random.randint(5, 18)
                    request.session['hp'] -= monster_damage
                    log.append(f"The monster dealt {monster_damage} damage to you!")

            elif action == 'heal':
                if request.session['gold'] >= 15:
                    request.session['gold'] -= 15
                    heal_amount = random.randint(25, 40)
                    request.session['hp'] = min(100, request.session['hp'] + heal_amount)
                    log.append(f"You drank a potion and restored {heal_amount} HP!")
                else:
                    log.append("Not enough gold! Potions cost 15 gold.")

            elif action == 'flee':
                if request.session['room'] >= 5:
                    log.append("Cannot flee from the Final Boss room!")
                elif random.choice([True, False]):
                    log.append("You escaped successfully to the next room!")
                    request.session['room'] += 1
                    request.session['monster_hp'] = 40 + (request.session['room'] * 15)
                else:
                    monster_damage = random.randint(10, 20)
                    request.session['hp'] -= monster_damage
                    log.append(f"Escape failed! Monster hit you for {monster_damage} damage!")

            if request.session['hp'] <= 0:
                request.session['hp'] = 0
                request.session['game_over'] = True
                log.append("💀 You died in the dungeon! Game Over.")

            request.session['log'] = log[-5:]
            request.session.modified = True

        return redirect('dungeon_game')

    context = {
        'hp': request.session.get('hp', 100),
        'monster_hp': request.session.get('monster_hp', 50),
        'gold': request.session.get('gold', 0),
        'room': request.session.get('room', 1),
        'log': request.session.get('log', []),
        'game_over': request.session.get('game_over', False),
        'won': request.session.get('won', False),
    }
    return render(request, 'Dungeon_Escape/index.html', context)