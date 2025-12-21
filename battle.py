from utils import pause, line
from character import Character
import random

def battle(player, enemy):
    print(f"\n⚔️  {enemy.name} appears!\n")
    pause()

    turn = 1
    while player.is_alive() and enemy.is_alive():
        print("\n" * 50)
        line()
        print(f"Turn {turn}")
        print(f"{player.name} — HP: {player.health} | Energy: {player.energy}")
        print(f"{enemy.name} — HP: {enemy.health} | Energy: {enemy.energy}")
        line()

        # -------------------------------
        # PLAYER CHOOSES ACTION
        # -------------------------------
        print("Choose your action:")
        print("1. Attack")
        print("2. Dodge")
        print("3. Heal")
        print("4. Counter Attack")

        choice = input("> ")

        if choice == "1":
            player_action = player.choose_attack()
        elif choice == "2":
            player_action = player.choose_dodge()
        elif choice == "3":
            player_action = player.choose_heal()
        elif choice == "4":
            player_action = player.choose_counter()
        else:
            print("Invalid choice! You hesitate...")
            player_action = {"type": "none"}

        # -------------------------------
        # ENEMY CHOOSES ACTION
        # -------------------------------
        enemy_action = enemy.choose_action()


        pause()
        resolve_turn(player, enemy, player_action, enemy_action)
        pause()


        # -------------------------------
        # CHECK END CONDITIONS
        # -------------------------------
        if not enemy.is_alive():
            print(f"🏆 {enemy.name} is defeated!")
            player.gain_exp(50)
            player.clamp_stats()  # Geralt’s base max HP
            break

        if not player.is_alive():
            print(f"💀 {player.name} has fallen...")
            break

        turn += 1

    line()
    print("🏁 Battle Over 🏁")
    pause()

# ----------------------------------------------------------------------
# TURN RESOLUTION LOGIC
# ----------------------------------------------------------------------

def resolve_turn(player, enemy, p_action, e_action):
    """Determines what happens based on both sides' actions."""
    pa = p_action["type"]
    ea = e_action["type"]
    
    enemy_attack = (ea == "attack" or ea == "heavy_attack")
    
        # --- ATTACK vs REST / NONE ---
    if pa == "attack" and ea == "rest":
        enemy.health -= p_action["power"]
        print(f"{player.name} punishes the rest and hits {enemy.name} for {p_action['power']} damage!")
        print(f"{enemy.name} catches their breath, regaining {e_action['amount']} energy.")

    elif pa == "attack" and ea == "none":
        enemy.health -= p_action["power"]
        print(f"{player.name} lands a clean hit for {p_action['power']} damage!")


    # --- ATTACK vs DODGE / ATTACK ---
    elif pa == "attack" and enemy_attack:
        enemy.health -= p_action["power"]
        player.health -= e_action["power"]
        print(f"💥 Both {player.name} and {enemy.name} trade blows!")
    elif pa == "attack" and ea == "dodge":
        energy_gain = 30
        enemy.energy = min(enemy.max_energy, enemy.energy + energy_gain)
        print(f"{enemy.name} dodges and regains {energy_gain} energy! ⚡️")
        # --- PLAYER didn't attack, but ENEMY dodged nothing ---
    elif ea == "dodge" and pa != "attack":
       energy_gain = 15
       enemy.energy = min(enemy.max_energy, enemy.energy + energy_gain)
       print(f"{enemy.name} dodges nothing but regains {energy_gain} energy. 💨")
    elif pa == "attack" and ea == "heal":
        enemy.health += e_action["amount"]
        enemy.health -= p_action["power"]
        print(f"{player.name} strikes while {enemy.name} heals!")

    # --- DODGE vs ATTACK / HEAL ---
    elif pa == "dodge" and enemy_attack:
        energy_gain = 30
        player.energy = min(player.max_energy, player.energy + energy_gain)
        print(f"{player.name} gains {energy_gain} energy from dodging! ⚡️")
    elif pa == "dodge" and ea == "heal":
        energy_gain = 15
        player.energy = min(player.max_energy, player.energy + energy_gain)
        print(f"{player.name} gains {energy_gain} energy from dodging nothing! ⚡️")

    # --- HEAL cases ---
    elif pa == "heal" and enemy_attack:
        player.health += p_action["amount"]
        player.health -= e_action["power"]
        print(f"{player.name} heals but is hit by {enemy.name}!")
    elif pa == "heal" and ea == "heal":
        player.health += p_action["amount"]
        enemy.health += e_action["amount"]
        print(f"Both sides heal up for a breather 🧘")

    # --- COUNTERATTACK logic ---
    elif pa == "counter" and enemy_attack:
        enemy.health -= p_action["power"]
        print(f"⚡ {player.name} counters {enemy.name}'s attack for {p_action['power']} damage!")
    elif pa == "counter" and not enemy_attack:
        print(f"{player.name}'s counter stance fades — no attack to respond to.")

    # --- REST (enemy only) ---
    elif ea == "rest":
        print(f"{enemy.name} catches their breath, regaining {e_action['amount']} energy.")

    # --- Default case ---
    else:
        print("Both fighters hesitate, watching each other closely...")

    # Clamp health so it doesn’t go negative
    player.clamp_stats()
    enemy.clamp_stats()

