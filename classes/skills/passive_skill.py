from abc import ABC, abstractmethod

from classes.skills.skill import Skill


class PassiveSkill(Skill, ABC):
    def __init__(self, name, cooldown, cost):
        super().__init__(name, cooldown, cost)

    @abstractmethod
    def cast(self, **kwargs) -> None:
        pass

    @abstractmethod
    def unassign(self, **kwargs) -> None:
        pass
