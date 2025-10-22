from character import Character
from utils import pause
import random

class Enemy(Character):
    def __init__(self, name, health, attack_power, energy):
        super().__init__(name, health, attack_power, energy)
        self.special_power = False
        self.enemy_dodge = False


    def attack(self, target):
      if self.energy>14:
        self.energy -= 15
        critic = random.random() / 2
        damage = round(self.attack_power * (critic + 1))
        target.health -= damage
        print(f"{self.name} attacks {target.name} for {damage} damage!")
      else:
         print("Insufficient energy for attack")


    def special(self):
        if random.random() >= 0.75:
            print(f"{self.name} activates a special power! 👹")
            self.special_power = True

    def dodge(self, target):
        if target.attack_power > 0:
           self.energy += 45
        self.enemy_dodge = True

