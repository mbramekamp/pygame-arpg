from projectile import Projectile
from skills.active_skill import ActiveSkill


class ShurikenSkill(ActiveSkill):
    damage: int
    speed: float
    sound: str
    image: str
    size: tuple

    def __init__(self, name, cooldown, cost, damage, speed, sound, images, size):
        super().__init__(name, cooldown, cost, last_cast_time=0)
        self.damage = damage
        self.speed = speed
        self.sound = sound
        self.image = images
        self.size = size

    def cast(self, **kwargs):
        projectile = Projectile(
            kwargs["x"],
            kwargs["y"],
            kwargs["direction"],
            self.speed,
            self.damage,
            self.image,
            self.sound,
            self.size,
        )
        return projectile

    def level_up(self) -> None:
        super().level_up()
        self.damage = int(self.damage * self.level**1.15)
