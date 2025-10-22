from character import Character
from utils import pause
import random

class Player(Character):
    def __init__(self, name, health, attack_power, energy):
        super().__init__(name, health, attack_power, energy)
        self.level = 1
        self.exp = 0
        self.dodge_next = False
        self.counter_attack_next = False
        self.counter_damage = 0

    def attack(self, target):
      if self.energy>15:
        self.energy -= 15
        critic = random.random() / 2
        damage = round(self.attack_power * (critic + 1))
        if hasattr(target, "enemy_dodge") and target.enemy_dodge:
            print(f"{target.name} dodged your attack!")
            pause()
            return
        target.health -= damage
        print(f"{self.name} attacks {target.name} for {damage} damage!")
      else:
         print("Not enough energy")


    def dodge(self):
        if random.random() < 0.65:
            print("🥷 You prepare to dodge the next attack!")
            self.dodge_next = True
            self.energy += 45
        else:
            print("❌ Failed to dodge.")
            self.dodge_next = False
    
    def counter_attack(self):
        if random.random() < 0.45:
            print("😈 You prepare to counter the next attack!")
            self.energy += 20
            criticR = random.random() / 2
            self.counter_damage = round(self.attack_power * (criticR + 1))
            self.counter_attack_next = True
        else:
            print("❌ You failed to ready your counter.")
            self.counter_attack_next = False


    def gain_exp(self, amount):
        self.exp += amount
        print(f"{self.name} gained {amount} XP!")
        if self.exp >= self.level * 50:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.health += 20
        self.attack_power += 5
        self.exp = 0
        print(f"🎉 {self.name} leveled up to Level {self.level}!")
