from abc import ABC, abstractmethod

from classes.projectile import Projectile
from classes.skills.skill import Skill


class ActiveSkill(Skill, ABC):
    last_cast_time: int

    def __init__(self, name, cooldown, cost, last_cast_time):
        super().__init__(name, cooldown, cost)
        self.last_cast_time = last_cast_time

    @abstractmethod
    def cast(self, **kwargs) -> Projectile:
        pass

    def can_cast(self, game_time) -> bool:
        # print(f"game_time: {game_time}, last_cast: {self.last_cast_time}, cooldown: {self.cooldown}")
        if game_time - self.last_cast_time >= self.cooldown:
            return True

        return False

    def level_up(self) -> None:
        return super().level_up()
