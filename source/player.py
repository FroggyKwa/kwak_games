JUMP_POWER = 2.3
GRAVITY = 0.5
MOVE_SPEED = 7


class Player:
    def __init__(self, x0, y0, socket):
        self.x = x0
        self.direction = 'right'
        self.y = y0
        self.x_velocity = 0
        self.y_velocity = 0
        self.ip = None
        self.sock = socket
        self.hp = 100
        self.onGround = True
        self.update(x0, y0)
        self.cur_shoot_time = 0

    def update(self, x, y):
        self.x = x
        self.y = y

    def change_velocity(self, direction=None):
        if not direction:
            self.x_velocity = 0
            if not self.onGround:
                self.y_velocity += GRAVITY if self.y_velocity <= 10 else 0
        if direction == 'up':
            if self.onGround:
                self.y_velocity = -JUMP_POWER
                self.onGround = False
        if direction == 'left':
            self.x_velocity = -MOVE_SPEED
        if direction == 'right':
            self.x_velocity = MOVE_SPEED

    def move(self):
        self.y = self.y + self.y_velocity
        self.x = self.x + self.x_velocity

    def get_damage(self, dmg):
        self.hp -= dmg if self.hp >= dmg else self.hp
