from character import Character
import random

class Enemy(Character):
    def __init__(self, name, health, attack_power, energy):
        super().__init__(name, health, attack_power, energy)
        self.special_power = False

    # -------------------------------
    # DECIDE ACTION EACH TURN
    # -------------------------------
    def choose_action(self):
        roll = random.random()

        if self.energy < 10:
            return self.rest()  # regain some energy instead

        if roll < 0.6:
            return self.choose_attack()
        elif roll < 0.8:
            return self.choose_heal()
        else:
            return self.choose_dodge()

    def choose_attack(self):
        self.energy -= 15
        damage = self.roll_damage()
        print(f"{self.name} winds up to attack for {damage} damage!")
        return {"type": "attack", "power": damage}

    def choose_dodge(self):
        print(f"{self.name} prepares to dodge! 💨")
        return {"type": "dodge"}

    def choose_heal(self):
        heal_amount = random.randint(20, 35)
        print(f"{self.name} prepares to heal for {heal_amount} HP.")
        return {"type": "heal", "amount": heal_amount}

    def rest(self):
        regain = random.randint(10, 25)
        self.energy += regain
        print(f"{self.name} is too tired and regains {regain} energy.")
        return {"type": "rest", "amount": regain}

    # -------------------------------
    # SUPPORT FUNCTION
    # -------------------------------
    def roll_damage(self):
        critic = random.random() / 2
        return round(self.attack_power * (1 + critic))
