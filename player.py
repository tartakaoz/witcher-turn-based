from character import Character

class Player(Character):
    def __init__(self, name, health, attack_power, energy):
        super().__init__(name, health, attack_power, energy)
        self.level = 1
        self.exp = 0

    # -------------------------------
    # ACTIONS (silent: return intent objects only)
    # -------------------------------
    def choose_attack(self):
        cost = 15
        if self.energy < cost:
            return {"type": "none", "reason": "not_enough_energy", "attempted": "attack", "cost": cost}

        self.energy -= cost
        damage = self.attack_power
        return {"type": "attack", "power": damage, "cost": cost}

    def choose_dodge(self):
        # no energy cost, just an intent
        return {"type": "dodge"}

    def choose_counter(self):
        cost = 25
        if self.energy < cost:
            return {"type": "none", "reason": "not_enough_energy", "attempted": "counter", "cost": cost}

        self.energy -= cost
        counter_damage = self.attack_power
        return {"type": "counter", "power": counter_damage, "cost": cost}

    def choose_heal(self):
        cost = 20
        if self.energy < cost:
            return {"type": "none", "reason": "not_enough_energy", "attempted": "heal", "cost": cost}

        self.energy -= cost
        heal_amount = 20
        return {"type": "heal", "amount": heal_amount, "cost": cost}

    # -------------------------------
    # SUPPORT FUNCTIONS
    # -------------------------------
    def gain_exp(self, amount):
        self.exp += amount
        # silent: let battle/resolve_turn print this if you want
        # return info so caller can decide whether to print
        leveled = False
        while self.exp >= self.level * 50:
            self.exp -= self.level * 50
            self.level_up()
            leveled = True
        return {"gained": amount, "leveled_up": leveled, "level": self.level}

    def level_up(self):
        self.level += 1
        self.max_health += 20
        self.max_energy += 10
        self.attack_power += 5
        # optional: heal a bit on level up (your old code did a partial heal)
        self.health = min(self.health + 25, self.max_health)
