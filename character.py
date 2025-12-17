import random

class Character:
    def __init__(self, name, health, attack_power, energy):
        self.name = name
        self.max_health = health
        self.max_energy = energy
        self.health = health
        self.attack_power = attack_power
        self.energy = energy

    def is_alive(self):
        return self.health > 0
    
    def clamp_stats(self):
        self.health = max(0, min(self.health, self.max_health))
        self.energy = max(0, min(self.energy, self.max_energy))