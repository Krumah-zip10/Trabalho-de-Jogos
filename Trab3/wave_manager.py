import random
from enemy import Enemy


def random_border_position(width, height, margin=32):
    side = random.choice(['left', 'right', 'top', 'bottom'])
    if side == 'left':
        return (0, random.randint(0, height - margin))
    elif side == 'right':
        return (width - margin, random.randint(0, height - margin))
    elif side == 'top':
        return (random.randint(0, width - margin), 0)
    else:
        return (random.randint(0, width - margin), height - margin)


class WaveManager:

    def __init__(self, handler, target, width, height,
                 base_enemies=3, increment=2):
        self.handler = handler
        self.target = target
        self.width = width
        self.height = height
        self.base_enemies = base_enemies
        self.increment = increment

        self.wave = 0
        self.alive_count = 0
        self.new_enemies = []

        handler.subscribe('enemy_killed', self.on_enemy_killed)
        self.start_next_wave()

    def start_next_wave(self):
        self.wave += 1
        count = self.base_enemies + self.increment * (self.wave - 1)
        self.alive_count = count
        for _ in range(count):
            pos = random_border_position(self.width, self.height)
            self.new_enemies.append(Enemy(pos, self.target, self.handler))

    def on_enemy_killed(self, enemy):
        self.alive_count -= 1
        if self.alive_count <= 0:
            self.start_next_wave()

    def collect_new_enemies(self):
        pending = self.new_enemies
        self.new_enemies = []
        return pending