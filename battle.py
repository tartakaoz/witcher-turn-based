from utils import pause, line
import random
def battle(player, enemy):
    input("Press enter to continue to the battle")
    print(f"\n⚔️ {enemy.name} appears!\n")
    pause()

    while player.is_alive() and enemy.is_alive():
        print("\n" * 100)
        line()
        print(f"{player.name} HP: {player.health} | {enemy.name} HP: {enemy.health}")
        print(f"Energy: {player.energy}    | Energy: {enemy.energy}")
        print("Choose your action:")
        print("1. Attack")
        print("2. Dodge")
        print("3. Counter Attack")

        choice = input("> ")

        if choice == "1":
            if random.random() < 0.2:
                enemy.dodge(player)

            player.attack(enemy)

            if enemy.enemy_dodge:
                enemy.enemy_dodge = False
                continue

        elif choice == "2":
            player.dodge(enemy)

            player.attack_power = 0
            if random.random() < 0.2:
              enemy.dodge(player)
              enemy.enemy_dodge = False
              player.attack_power = 25
              continue
            player.attack_power = 25


        elif choice == "3":
            player.counter_attack()

        else:
            print("Invalid choice — you lose your turn.")
        
        pause()

        # Enemy's turn
        if not enemy.is_alive():
            print(f"{enemy.name} is defeated! 🎉")
            player.gain_exp(50)
            pause()
            break

        print(f"\n{enemy.name}'s turn...")
        pause()

        if player.dodge_next:
            print(f"{player.name} dodges {enemy.name}'s attack! 💨")
            player.dodge_next = False
        elif player.counter_attack_next:
            print(f"{player.name} counter attacks {enemy.name} for {player.counter_damage} damage! ⚡️")
            enemy.health -= player.counter_damage
            player.counter_attack_next = False
            if not enemy.is_alive():
                print(f"{enemy.name} is defeated by your counter attack! 🎉")
                player.gain_exp(50)
                pause()
                break
        else:
            enemy.attack(player)
           
        pause()

        if not player.is_alive():
            print(f"\n{player.name} has fallen... 💀")
            break

    line()
    print("\n🏁 Battle Over 🏁\n")
