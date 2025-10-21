import random

class Character:
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.attack_power = attack_power
    
    def attack(self, target):
        critic = random.random() / 2
        damage = round(self.attack_power * (critic + 1))
        target.health -= damage
        print(f"{self.name} attacks {target.name} for {damage} damage!")

    def is_alive(self):
        return self.health > 0
