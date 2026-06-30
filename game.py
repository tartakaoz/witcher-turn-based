from player import Player
from enemy import Enemy
from battle import battle
from utils import pause, line, enter

# Create the player
# Test for terminal
player = Player("Geralt", 110, 25, 100)

# Create a list of enemies
enemies = [
    Enemy("Drowner", 70, 10, 60, max_focus=2),
    Enemy("Imlerith", 110, 20, 120, max_focus=3),
    Enemy("Eredin", 130, 25, 140, max_focus=4)
]

line()
line()
enter()
print("⚔️  The Witcher Adventure Begins! ⚔️\n")


# Loop through each enemy
for enemy in enemies:
    battle(player, enemy)

    if not player.is_alive():
        print("💀 Game Over! You have fallen in battle.")
        break
    else:
        print(f"🏆 You defeated {enemy.name}!\n")
        pause()

print("\n🎉 The adventure ends! 🎉")
