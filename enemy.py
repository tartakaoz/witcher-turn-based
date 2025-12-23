from character import Character
import random

class Enemy(Character):
    def __init__(self, name, health, attack_power, energy, max_focus, heal_cooldown=2):
        super().__init__(name, health, attack_power, energy)
        self.focus = 0
        self.max_focus = max_focus
        self.heal_cooldown = heal_cooldown  # your “heals left in a row” idea

    def choose_action(self):
        if self.energy < 15:
            return self.rest()

        # heal when low AND has heal charges left
        if self.health <= self.max_health * 0.35 and self.heal_cooldown > 0:
            # (optional) add randomness so it doesn't always heal:
            # if random.random() < 0.75:
            return self.choose_heal()

        if self.focus >= self.max_focus and self.energy >= 25:
            return self.heavy_attack()

        return self.choose_attack()

    def heavy_attack(self):
        dmg = self.attack_power + 15
        return {
            "type": "heavy_attack",
            "power": dmg,
            "energy_cost": 25,

        }

    def choose_attack(self):
        dmg = self.attack_power
        return {
            "type": "attack",
            "power": dmg,
            "energy_cost": 15,

        }

    def choose_dodge(self):
        return {
            "type": "dodge",
            "energy_cost": 0,

        }

    def choose_heal(self):
        heal_amount = 20
        return {
            "type": "heal",
            "amount": heal_amount,
            "energy_cost": 0,

        }

    def rest(self):
        regain = 20
        return {
            "type": "rest",
            "amount": regain,
            "energy_cost": 0,

        }
