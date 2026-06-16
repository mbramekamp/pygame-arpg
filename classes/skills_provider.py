from multiprocessing import Value
from random import random

from skills.fireball_skill import FireballSkill
from skills.health_increase import HealthIncrease
from skills.icebolt_skill import IceBoltSkill
from skills.rockthrow_skill import RockThrowSkill
from skills.shuriken_skill import ShurikenSkill
from skills.skill import Skill


class SkillProvider:
    skills_list: list[Skill]

    def __init__(self):

        self.skills_list = []

        # ACTIVE SKILLS

        fireball = FireballSkill(
            "Fireball",
            5,
            10,
            20,
            5,
            "./sounds/bubble pop.mp3",
            "./images/FireBall.png",
            (25, 25),
        )

        icebolt = IceBoltSkill(
            "IceBolt",
            5,
            10,
            20,
            5,
            "./sounds/bubble pop.mp3",
            "./images/FireBall.png",
            (25, 25),
        )
        rockthrow = RockThrowSkill(
            "Rockthrow",
            5,
            10,
            20,
            5,
            "./sounds/bubble pop.mp3",
            "./images/FireBall.png",
            (25, 25),
        )
        shuriken = ShurikenSkill(
            "Shuriken",
            5,
            10,
            20,
            5,
            "./sounds/bubble pop.mp3",
            "./images/FireBall.png",
            (10, 10),
        )

        # PASSIVE SKILLS

        health_increase = HealthIncrease("Health Increase", 0, 0, 5)

        # add them to the list

        self.skills_list.append(fireball)
        self.skills_list.append(icebolt)
        self.skills_list.append(rockthrow)
        self.skills_list.append(shuriken)
        self.skills_list.append(health_increase)

    def get_random_choices(self):
        if len(self.skills_list) < 3:
            raise ValueError("Not enough Skills in pool")
        result = random.sample(self.skills_list, 3)
        return result
