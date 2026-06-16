from abc import ABC, abstractmethod

from classes.projectile import Projectile


class Skill(ABC):
    name: str
    cooldown: int
    cost: int
    level: int

    def __init__(self, name, cooldown, cost):
        self.name = name
        self.cooldown = cooldown
        self.cost = cost
        self.level = 1

    @abstractmethod
    def cast(self, **kwargs) -> None | Projectile:
        pass

    def level_up(self) -> None:
        self.level += 1
