from utils import pause, line, enter
from character import Character

def battle(player, enemy):
    print(f"\n⚔️  {enemy.name} appears!\n")
    pause()

    turn = 1
    while player.is_alive() and enemy.is_alive():
        enter()
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


        
        resolve_turn(player, enemy, player_action, enemy_action)
        input("Press enter to continue")



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
    pa = p_action.get("type", "none")
    ea = e_action.get("type", "none")



    # 2) Apply energy costs (ONLY here)
    player.energy -= p_action.get("energy_cost", 0)
    enemy.energy  -= e_action.get("energy_cost", 0)

    # Safety clamp: don’t go negative energy
    player.energy = max(0, player.energy)
    enemy.energy = max(0, enemy.energy)

    # Helper flags
    enemy_attack = ea in ("attack", "heavy_attack")
    player_attack = pa in ("attack", "heavy_attack")

    # 3) Resolve interactions

    # --- Counter rules ---
    if pa == "counter":
        if enemy_attack:
            # counter succeeds: enemy takes counter dmg, player avoids the hit (your design choice)
            enemy.health -= p_action.get("power", 0)
            print(f"⚡ {player.name} counters and hits {enemy.name} for {p_action.get('power', 0)} damage!")
        else:
            print(f"{player.name}'s counter stance fades — no attack to respond to.")
        # enemy action still “happened” but counter handled it
        player.clamp_stats()
        enemy.clamp_stats()
        return

    # --- Dodge rules ---
    if pa == "dodge":
        if enemy_attack:
            # dodge avoids damage, gains energy
            gain = 30
            player.energy = min(player.max_energy, player.energy + gain)
            print(f"{player.name} dodges and regains {gain} energy! ⚡️")
        elif ea == "heal":
            gain = 15
            player.energy = min(player.max_energy, player.energy + gain)
            print(f"{player.name} dodges nothing but regains {gain} energy. 💨")
            enemy.health += e_action.get("amount", 0)
            print(f"{enemy.name} heals for {e_action.get('amount', 0)} HP. 🧪")
        elif ea == "rest":
            enemy.energy = min(enemy.max_energy, enemy.energy + e_action.get("amount", 0))
            print(f"{enemy.name} rests and regains {e_action.get('amount', 0)} energy.")
        else:
            print("Both fighters hesitate, watching each other closely...")

        player.clamp_stats()
        enemy.clamp_stats()
        return

    # --- Heal rules ---
    if pa == "heal":
        player.health += p_action.get("amount", 0)
        print(f"{player.name} heals for {p_action.get('amount', 0)} HP. 🧪")

        if enemy_attack:
            player.health -= e_action.get("power", 0)
            print(f"{enemy.name} hits {player.name} for {e_action.get('power', 0)} damage! 💥")
        elif ea == "heal":
            enemy.health += e_action.get("amount", 0)
            print(f"{enemy.name} heals for {e_action.get('amount', 0)} HP. 🧪")
        elif ea == "rest":
            enemy.energy = min(enemy.max_energy, enemy.energy + e_action.get("amount", 0))
            print(f"{enemy.name} rests and regains {e_action.get('amount', 0)} energy.")
        else:
            print(f"{enemy.name} does nothing.")

        player.clamp_stats()
        enemy.clamp_stats()
        return

    # --- Attack rules ---
    if player_attack:
        # Player attacks first (your choice). If you want simultaneous, move damage before checks.
        if ea == "dodge":
            gain = 30
            enemy.energy = min(enemy.max_energy, enemy.energy + gain)
            print(f"{enemy.name} dodges and regains {gain} energy! ⚡️")
        else:
            enemy.health -= p_action.get("power", 0)
            print(f"{player.name} hits {enemy.name} for {p_action.get('power', 0)} damage! 💥")

        # Enemy response
        if enemy.is_alive():  # important: dead enemies shouldn’t hit back
            if enemy_attack:
                player.health -= e_action.get("power", 0)
                print(f"{enemy.name} hits {player.name} for {e_action.get('power', 0)} damage! 💥")
            elif ea == "heal":
                enemy.health += e_action.get("amount", 0)
                print(f"{enemy.name} heals for {e_action.get('amount', 0)} HP. 🧪")
            elif ea == "rest":
                enemy.energy = min(enemy.max_energy, enemy.energy + e_action.get("amount", 0))
                print(f"{enemy.name} rests and regains {e_action.get('amount', 0)} energy.")
            else:
                print(f"{enemy.name} does nothing.")

        player.clamp_stats()
        enemy.clamp_stats()
        return

    # --- Rest (enemy only) ---
    if ea == "rest":
        enemy.energy = min(enemy.max_energy, enemy.energy + e_action.get("amount", 0))
        print(f"{enemy.name} catches their breath, regaining {e_action.get('amount', 0)} energy.")
        player.clamp_stats()
        enemy.clamp_stats()
        return

    # Default
    print("Both fighters hesitate, watching each other closely...")
    player.clamp_stats()
    enemy.clamp_stats()
