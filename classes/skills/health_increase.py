from passive_skill import PassiveSkill


class HealthIncrease(PassiveSkill):
    amount: float
    original_health: float | None

    def __init__(self, name, cooldown, cost, amount):
        super().__init__(name, cooldown, cost)

        self.amount = amount
        self.original_health = None

    def cast(self, **kwargs):
        self.original_health = kwargs["player"].health

        kwargs["player"].health *= self.amount

    def unassign(self, **kwargs):

        if self.original_health is not None:
            kwargs["player"].health = self.original_health
