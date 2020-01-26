class Button:
    def __init__(self, width, height, x, y, color1, color2, color3, name):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.state = 1
        self.h = 5
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        self.name = name

    def draw(self):
        if self.state == 1:
            return self.x, self.y, self.width, self.height, self.color1, self.name
        elif self.state == 2:
            return self.x - self.h, self.y - self.h, self.width + 2 * self.h, self.height + 2 * self.h, \
                   self.color2, self.name
        elif self.state == 3:
            return self.x + self.h, self.y + self.h, self.width - 2 * self.h, self.height - 2 * self.h, \
                   self.color3, self.name

    def check_cursor_on_button(self, x, y):
        if self.state == 1:
            if (self.x < x < self.x + self.width) and \
                    (self.y < y < self.y + self.height):
                self.state = 2
                return True
        if self.state == 2:
            if (self.x - self.h < x < self.x + self.h + self.width) and \
                    (self.y - self.h < y < self.y + self.height + self.h):
                self.state = 2
                return True
            else:
                self.state = 1
                return False

    def check_cursor_click_button(self, x, y):
        if (self.x - self.h < x < self.x + self.h + self.width) and \
                (self.y - self.h < y < self.y + self.height + self.h):
            self.state = 3
            return True

    def check_cursor_release_button(self, x, y):
        if (self.x + self.h < x < self.x + self.width - self.h) and \
                (self.y + self.h < y < self.y + self.height - self.h) and self.state == 3:
            self.state = 1
            return True
        else:
            self.state = 1
            return False

    def get_name(self):
        return self.name

    def change_name(self, new_name):
        self.name = new_name