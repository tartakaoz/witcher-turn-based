from character import Character
import random

class Player(Character):
    def __init__(self, name, health, attack_power, energy):
        super().__init__(name, health, attack_power, energy)
        self.level = 1
        self.exp = 0

    # -------------------------------
    # ACTIONS (return intent objects)
    # -------------------------------
    def choose_attack(self):
        if self.energy < 15:
            print("Not enough energy to attack!")
            return {"type": "none"}

        self.energy -= 15
        damage = self.roll_damage()
        print(f"{self.name} prepares to strike for {damage} damage!")
        return {"type": "attack", "power": damage}

    def choose_dodge(self):
        print("🥷 You prepare to dodge the next attack!")
        return {"type": "dodge"}
    
    def choose_counter(self):
      if self.energy < 25:
        print("Not enough energy to prepare a counterattack!")
        return {"type": "none"}
      
      self.energy -= 25
      print("😈 You prepare to counter the next attack!")
      counter_damage = self.roll_damage()
      return {"type": "counter", "power": counter_damage}


    def choose_heal(self):
        if self.energy < 20:
            print("Not enough energy to heal!")
            return {"type": "none"}

        self.energy -= 20
        heal_amount = random.randint(25, 40)
        print(f"{self.name} prepares to heal for {heal_amount} HP.")
        return {"type": "heal", "amount": heal_amount}

    # -------------------------------
    # SUPPORT FUNCTIONS
    # -------------------------------
    def roll_damage(self):
        critic = random.random() / 2
        return round(self.attack_power * (1 + critic))

    def gain_exp(self, amount):
        self.exp += amount
        print(f"{self.name} gained {amount} XP!")
        if self.exp >= self.level * 50:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.health = min(self.health + 25, self.max_health)
        self.max_energy += 10
        self.max_health += 20
        self.attack_power += 5
        self.exp = 0
        print(f"🎉 {self.name} leveled up to Level {self.level}!")
