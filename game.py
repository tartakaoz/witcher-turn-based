from player import Player
from enemy import Enemy
from battle import battle
from utils import pause, line

# Create the player
player = Player("Geralt", 110, 25)

# Create a list of enemies
enemies = [
    Enemy("Drowner", 70, 10),
    Enemy("Imlerith", 110, 20),
    Enemy("Eredin", 130, 25)
]

print("\n" * 5)
print("⚔️  The Witcher Adventure Begins! ⚔️\n")
pause()

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
