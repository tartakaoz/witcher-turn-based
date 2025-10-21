from character import Character
import random

class Enemy(Character):
    def __init__(self, name, health, attack_power):
        super().__init__(name, health, attack_power)
        self.special_power = False

    def special(self):
        if random.random() >= 0.75:
            print(f"{self.name} activates a special power! 👹")
            self.special_power = True
