from character import Character
import random

class Enemy(Character):
    def __init__(self, name, health, attack_power, energy, max_focus):
        super().__init__(name, health, attack_power, energy)
        self.focus = 0
        self.max_focus = max_focus

    # -------------------------------
    # DECIDE ACTION EACH TURN
    # -------------------------------
    def choose_action(self):
        roll = random.random()

        if self.energy < 15:
            return self.rest()  # regain some energy instead

        if self.health <= self.max_health * 0.35:
            return self.choose_heal()
        return self.choose_attack()

    def choose_attack(self):
        self.energy -= 15
        damage = self.attack_power
        print(f"{self.name} winds up to attack for {damage} damage!")
        return {"type": "attack", "power": damage}

    def choose_dodge(self):
        print(f"{self.name} prepares to dodge! 💨")
        return {"type": "dodge"}

    def choose_heal(self):
        heal_amount = 20
        print(f"{self.name} prepares to heal for {heal_amount} HP.")
        return {"type": "heal", "amount": heal_amount}

    def rest(self):
        regain = 20
        self.energy += regain
        print(f"{self.name} is too tired and regains {regain} energy.")
        return {"type": "rest", "amount": regain}

    # -------------------------------
    # SUPPORT FUNCTION
    # -------------------------------
   
