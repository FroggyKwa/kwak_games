import traceback

import pygame
from source import *
from source import network
from source import camera
from source import button
from source import instances
from threading import Thread
from source.get_platforms import *

pygame.init()
pygame.font.init()

pygame.display.set_caption("CyB3r_F0rC3_2O77")
WIDTH, HEIGHT = 1280, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
cl = pygame.time.Clock()
FPS = 60


class Game:

    def __init__(self):
        self.sound = sounds
        self.images = images
        self.background = self.get_infinite_background()
        self.size = (WIDTH, HEIGHT)
        self.state = 1
        self.messages = list()
        self.camera = camera.Camera(1280, 800, (1280, 800))
        self.running = True
        self.init_menu()
        self.init_joining_server()

    def init_menu(self):
        self.sounds_is_on = True
        self.buttons_menu = [button.Button(400, 60, WIDTH // 2 - 200, 160, (5, 5, 5), (15, 15, 15), (25, 25, 25), "Join server"),
                        button.Button(400, 60, WIDTH // 2 - 200, 245, (5, 5, 5), (15, 15, 15), (25, 25, 25), "Authors"),
                        button.Button(400, 60, WIDTH // 2 - 200, 325, (5, 5, 5), (15, 15, 15), (25, 25, 25), "Training"),
                        button.Button(400, 60, WIDTH // 2 - 200, 410, (5, 5, 5), (15, 15, 15), (25, 25, 25), "Settings")]
        self.bg_menu = pygame.image.load("../source/resources/bg_for_menu.png")
        self.buttons_authors = [
            button.Button(400, 60, WIDTH // 2 - 200, 720, (5, 5, 5), (15, 15, 15), (25, 25, 25), "Return to menu")]
        self.buttons_training = [
            button.Button(400, 60, WIDTH // 2 - 200, 720, (5, 5, 5), (15, 15, 15), (25, 25, 25), "Return to menu")]
        self.buttons_settings = [
            button.Button(400, 60, WIDTH // 2 - 200, 720, (5, 5, 5), (15, 15, 15), (25, 25, 25), "Return to menu"),
            button.Button(400, 60, WIDTH // 2 - 200, 180, (5, 5, 5), (15, 15, 15), (25, 25, 25), "Turn off sounds")]
        self.magenta = (200, 0, 255)

    def init_joining_server(self):
        self.msg_text = str()
        self.ip = str()
        self.ip = ''
        self.sockIn = network.connect_InSocket(address='0.0.0.0', port=5556)

    def init_game(self):
        t1 = Thread(target=network.read_server_sock, args=(self.sockIn, self.messages, self.running))
        t1.start()
        self.platforms = get_platforms()
        self.player = instances.Player(screen)
        self.bullets = list()  # todo:мусор
        self.enemies = list()  # todo:мусор

    @staticmethod
    def get_infinite_background():  # бесконечный background
        images['background'] = pygame.transform.scale(images['background'], (WIDTH, HEIGHT))
        img_rect = images['background'].get_rect()
        print(img_rect)
        n_rows = round(HEIGHT / img_rect.height) + 1
        n_cols = round(WIDTH / img_rect.width) + 1
        temp_surface = pygame.Surface((n_cols * img_rect.width, n_rows * img_rect.height))
        for y in range(n_rows):
            for x in range(n_cols):
                img_rect.topleft = (x * img_rect.width,
                                    y * img_rect.height)
                temp_surface.blit(images['background'], img_rect)
        return temp_surface

    def menu(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for i in self.buttons_menu:
                if button.Button.check_cursor_click_button(i, x, y):
                    continue
        if event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            for i in self.buttons_menu:
                if button.Button.check_cursor_release_button(i, x, y):
                    name_button = button.Button.get_name(i)
                    if name_button == "Join server":
                        self.state = 2
                    if name_button == "Authors":
                        self.state = 4
                    if name_button == "Training":
                        self.state = 6
                    if name_button == "Settings":
                        self.state = 5
        else:
            x, y = pygame.mouse.get_pos()
            for i in self.buttons_menu:
                if button.Button.check_cursor_on_button(i, x, y):
                    continue
        screen.blit(self.bg_menu, (0, 0))
        for i in self.buttons_menu:
            x, y, b_width, b_height, color, name_button = i.draw()
            pygame.draw.rect(screen, color, (x, y, b_width, b_height))
            font = pygame.font.Font(None, 70)
            text = font.render(button.Button.get_name(i), 0, self.magenta)
            text_x = x + b_width // 2 - text.get_width() // 2
            text_y = y + b_height // 2 - text.get_height() // 2
            screen.blit(text, (text_x, text_y))

    def check_exit_event(self, event):
        if event == pygame.QUIT:
            self.running = False

    def enter_ip_address(self, event):
        if event.key == 8:  # backspace
            self.ip = self.ip[:-1]
        if event.key == 27:  # escape
            self.state = 1
        if event.key == 13:  # enter
            try:
                self.sockOut = network.connect_OutSocket(address=self.ip.split(':')[0], port=int(self.ip.split(':')[1]))
            except network.socket.gaierror:
                self.msg_text = 'Сервер отключен или не сущесвует'
                print(traceback.format_exc())
            except (IndexError, ValueError):
                self.msg_text = 'IP указан неккоректно'
                print(traceback.format_exc())
            else:
                network.sock_send(self.sockOut, '1')
                data, address = network.read_sock(self.sockIn)  # todo: если сервер не включен то виснет, исправить
                if data == '1':
                    self.msg_text = 'Подключение прошло успешно!'
                    self.init_game()
                    print(self.msg_text)
                    self.state = 3
                elif data == '2':
                    self.msg_text = 'Вы уже подключены к данному серверу'
                elif data == '3':
                    self.msg_text = 'Сервер уже заполнен!'
        self.ip = self.ip + event.unicode if event.unicode.isprintable() else self.ip
        print(event.unicode, event.key, event.mod)
        print(self.ip)

    def render_text(self, ip):
        font = pygame.font.Font(None, 70)
        phr = font.render(ip, 0, (100, 255, 100))
        phr_w = phr.get_width() if phr.get_width() > 600 else 600
        phr_h = phr.get_height()
        phr_x = WIDTH // 2 - phr_w // 2
        phr_y = HEIGHT // 2 - phr_h // 2

        text = font.render("Введите IP сервера (x.x.x.x:y):", 0, (100, 255, 100))
        text_x = WIDTH // 2 - text.get_width() // 2
        text_y = HEIGHT // 2 - text.get_height() // 2 - phr.get_height() - 30

        msg = font.render(self.msg_text, 0, (100, 255, 100))
        msg_x = WIDTH // 2 - msg.get_width() // 2
        msg_y = HEIGHT // 2 - msg.get_height() // 2 + phr.get_height() + 30

        screen.fill((0, 0, 0))
        screen.blit(text, (text_x, text_y))
        screen.blit(phr, (phr_x, phr_y))
        screen.blit(msg, (msg_x, msg_y))
        pygame.draw.rect(screen, (0, 255, 0), (phr_x - 10, phr_y - 10,
                                               phr_w + 20, phr_h + 20), 1)

    def parse_data(self):
        if self.messages:
            print(self.messages)
            print(self.messages[0][0])
            data = self.messages[0][0].split()
            print(data)
            self.x, self.y, self.hp, self.d = int(float(data.pop(0))), int(float(data.pop(0))), int(
                data.pop(0)), data.pop(0)  # todo:мусор
            for i in range(int(data.pop(0))):  # todo:мусор
                self.bullets.append((int(float(data.pop(0))), int(float(data.pop(0)))))
            for i in range(int(data.pop(0))):  # todo:мусор
                self.enemies.append((int(data.pop(0)), int(data.pop(0)), data.pop(0)))
            self.messages.clear()

    def authors(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for i in self.buttons_authors:
                if button.Button.check_cursor_click_button(i, x, y):
                    continue
        if event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            for i in self.buttons_authors:
                if button.Button.check_cursor_release_button(i, x, y):
                    name_button = button.Button.get_name(i)
                    if name_button == "Return to menu":
                        self.state = 1
        else:
            x, y = pygame.mouse.get_pos()
            for i in self.buttons_authors:
                if button.Button.check_cursor_on_button(i, x, y):
                    continue
        screen.blit(self.bg_menu, (0, 0))
        font = pygame.font.Font(None, 70)
        text = font.render("Authors:", 0, self.magenta)
        text_x = WIDTH // 2 - text.get_width() // 2
        screen.blit(text, (text_x, 150))
        text = font.render("Denis Bakushev", 0, self.magenta)
        text_x = WIDTH // 2 - text.get_width() // 2
        screen.blit(text, (text_x, 210))
        text = font.render("Froggling Golovankov", 0, self.magenta)
        text_x = WIDTH // 2 - text.get_width() // 2
        screen.blit(text, (text_x, 270))
        text = font.render("Pavel Rudnik", 0, self.magenta)
        text_x = WIDTH // 2 - text.get_width() // 2
        screen.blit(text, (text_x, 330))
        for i in self.buttons_authors:
            x, y, b_WIDTH, b_HEIGHT, color, name_button = i.draw()
            pygame.draw.rect(screen, color, (x, y, b_WIDTH, b_HEIGHT))
            font = pygame.font.Font(None, 70)
            text = font.render(button.Button.get_name(i), 0, self.magenta)
            text_x = x + b_WIDTH // 2 - text.get_width() // 2
            text_y = y + b_HEIGHT // 2 - text.get_width() // 2
            screen.blit(text, (text_x, text_y))

    def settings(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for i in self.buttons_settings:
                if button.Button.check_cursor_click_button(i, x, y):
                    continue
        if event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            for i in self.buttons_settings:
                if button.Button.check_cursor_release_button(i, x, y):
                    name_button = button.Button.get_name(i)
                    if name_button == "Return to menu":
                        self.state = 1
                    if name_button == "Turn off sounds":
                        self.sounds_is_on = False
                        button.Button.change_name(i, "Turn on sounds")
                    if name_button == "Turn on sounds":
                        self.sounds_is_on = True
                        button.Button.change_name(i, "Turn off sounds")
        else:
            x, y = pygame.mouse.get_pos()
            for i in self.buttons_settings:
                if button.Button.check_cursor_on_button(i, x, y):
                    continue
        screen.blit(self.bg_menu, (0, 0))
        for i in self.buttons_settings:
            x, y, b_width, b_height, color, name_button = i.draw()
            pygame.draw.rect(screen, color, (x, y, b_width, b_height))
            font = pygame.font.Font(None, 70)
            text = font.render(button.Button.get_name(i), 0, self.magenta)
            text_x = x + b_width // 2 - text.get_width() // 2
            text_y = y + b_height // 2 - text.get_height() // 2
            screen.blit(text, (text_x, text_y))

    def training(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for i in self.buttons_training:
                if button.Button.check_cursor_click_button(i, x, y):
                    continue
        if event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            for i in self.buttons_training:
                if button.Button.check_cursor_release_button(i, x, y):
                    name_button = button.Button.get_name(i)
                    if name_button == "Return to menu":
                        self.state = 1
        else:
            x, y = pygame.mouse.get_pos()
            for i in self.buttons_training:
                if button.Button.check_cursor_on_button(i, x, y):
                    continue

        screen.blit(self.bg_menu, (0, 0))
        for i in self.buttons_training:
            x, y, b_width, b_height, color, name_button = i.draw()
            pygame.draw.rect(screen, color, (x, y, b_width, b_height))
            font = pygame.font.Font(None, 70)
            text = font.render(button.Button.get_name(i), 0, self.magenta)
            text_x = x + b_width // 2 - text.get_width() // 2
            text_y = y + b_height // 2 - text.get_height() // 2
            screen.blit(text, (text_x, text_y))

    def draw(self):
        self.camera.update(self.player)
        screen.blit(self.background, self.background.get_rect())
        screen.blit(self.platforms, self.camera.apply_rect(self.platforms.get_rect()))
        screen.blit(self.player.image, self.camera.apply(self.player))
        for i in self.bullets:  # todo:мусор
            bullet = pygame.Surface((10, 5))
            bullet.fill((100, 100, 100))
            screen.blit(bullet, (i[0], i[1]))
        for i in self.enemies:  # todo:мусор
            enemy = pygame.Surface((30, 50))
            enemy.fill((255, 0, 0))
            try:
                screen.blit((i[0], i[1]), enemy)
            except TypeError:
                print('something went wrong')
                print(i)

    def run(self):
        while self.running:
            if self.state == 1:  # отрисовка меню
                for event in pygame.event.get():
                    self.check_exit_event(event)
                    self.menu(event)
            if self.state == 2:  # ввод IP
                for event in pygame.event.get():
                    self.check_exit_event(event)
                    if event.type == pygame.KEYDOWN:
                        self.enter_ip_address(event)
                    self.render_text(self.ip)
            if self.state == 3:  # Игра
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        network.sock_send(self.sockOut, '0')
                        break
                keys = pygame.key.get_pressed()
                self.parse_data()
                network.sock_send(self.sockOut, '2 ' + ''.join(map(str, keys)))
                try:
                    self.player.update(self.x, self.y)
                except ValueError:
                    continue
                self.draw()
            if self.state == 4:  # авторы
                for event in pygame.event.get():
                    self.check_exit_event(event)
                    self.authors(event)
            if self.state == 5:  # настройки
                for event in pygame.event.get():
                    self.check_exit_event(event)
                    self.settings(event)
            if self.state == 6:
                for event in pygame.event.get():
                    self.check_exit_event(event)
                    self.training(event)
            pygame.display.flip()
            cl.tick(FPS)
        self.t1.join()
        network.close_sock(self.sockIn)
        network.close_sock(self.sockOut)
        pygame.quit()


game = Game()
game.run()
