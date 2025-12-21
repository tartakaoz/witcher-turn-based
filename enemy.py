from character import Character
import random

class Enemy(Character):
    def __init__(self, name, health, attack_power, energy, max_focus, heals_left=2, max_heals_left=2):
        super().__init__(name, health, attack_power, energy)
        self.focus = 0
        self.max_focus = max_focus

        # This is NOT a cooldown; it's heal charges
        self.heals_left = heals_left
        self.max_heals_left = max_heals_left

    def _recover_heal_charge(self, amount=1):
        self.heals_left = min(self.max_heals_left, self.heals_left + amount)

    def choose_action(self):
        # If exhausted, rest first
        if self.energy < 15:
            return self.rest()

        low_hp = self.health <= self.max_health * 0.35

        # Heal sometimes even when not low (unpredictable),
        # but more likely when low.
        if self.heals_left > 0:
            if low_hp:
                # strong bias to heal when low
                if random.random() < 0.75:
                    return self.choose_heal()
            else:
                # occasional "fake-out" heal above low HP
                if random.random() < 0.10:
                    return self.choose_heal()

        # Heavy attack if focused
        if self.focus >= self.max_focus and self.energy >= 25:
            return self.heavy_attack()

        return self.choose_attack()

    def heavy_attack(self):
        self.energy -= 25
        self._recover_heal_charge(1)   # doing something else recovers heals
        self.focus = max(0, self.focus - 2)
        damage = self.attack_power + 15
        print(f"{self.name} winds up to a heavy attack for {damage} damage! ☠️")
        return {"type": "heavy_attack", "power": damage}

    def choose_attack(self):
        self.energy -= 15
        self._recover_heal_charge(1)   # doing something else recovers heals
        damage = self.attack_power
        print(f"{self.name} winds up to attack for {damage} damage!")
        return {"type": "attack", "power": damage}

    def choose_dodge(self):
        self._recover_heal_charge(1)   # also recovers heals
        print(f"{self.name} prepares to dodge! 💨")
        return {"type": "dodge"}

    def choose_heal(self):
        heal_amount = 20
        self.heals_left = max(0, self.heals_left - 1)  # spend a heal
        self.focus = min(self.max_focus, self.focus + 1)
        print(f"{self.name} prepares to heal for {heal_amount} HP.")
        return {"type": "heal", "amount": heal_amount}

    def rest(self):
        regain = 20
        self._recover_heal_charge(1)   # rest also recovers heals
        self.focus = min(self.max_focus, self.focus + 1)
        self.energy = min(self.max_energy, self.energy + regain)
        print(f"{self.name} is too tired and regains {regain} energy.")
        return {"type": "rest", "amount": regain}
