import random

class Character:
    def __init__(self, name, health, attack_power, energy):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.energy = energy

    def is_alive(self):
        return self.health > 0
