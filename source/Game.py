import pygame
import sys

sys.path.append('../')
from threading import Thread
from source import *
from source import network
from source import camera
from source import button
from source.get_platforms import *
from source.player import Player

pygame.init()
pygame.font.init()

pygame.display.set_caption("CyB3r_F0rC3_2O77")
WIDTH, HEIGHT = 1280, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
cl = pygame.time.Clock()
FPS = 60



#sound1 = pygame.mixer.Sound('boom.wav')
#sound2 = pygame.mixer.Sound('one.ogg')


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
        self.init_buttons()
        self.init_joining_server()
        self.pause = False
        self.timestamp = 0

    def init_buttons(self):
        self.w_button, self.h_button = WIDTH // 3, HEIGHT // 15
        self.sounds_is_on = True
        self.pause = False
        self.buttons_game_pause = [
            button.Button(self.w_button, self.h_button, WIDTH // 2 - (self.w_button // 2), int(HEIGHT * 0.3), (5, 5, 5),
                          (15, 15, 15), (25, 25, 25), "Continue"),
            button.Button(self.w_button, self.h_button, WIDTH // 2 - (self.w_button // 2), int(HEIGHT * 0.4), (5, 5, 5),
                          (15, 15, 15), (25, 25, 25), "Return to menu")]
        self.buttons_game_not_pause = [
            button.Button(self.h_button, self.h_button, WIDTH // 2 - (self.h_button // 2), int(HEIGHT * 0.01),
                          (5, 5, 5), (15, 15, 15), (25, 25, 25), "II")]

        self.buttons_menu = [
            button.Button(self.w_button, self.h_button, WIDTH // 2 - (self.w_button // 2), int(HEIGHT * 0.2), (5, 5, 5),
                          (15, 15, 15), (25, 25, 25), "Join server"),
            button.Button(self.w_button, self.h_button, WIDTH // 2 - (self.w_button // 2), int(HEIGHT * 0.30625),
                          (5, 5, 5), (15, 15, 15), (25, 25, 25), "Authors"),
            button.Button(self.w_button, self.h_button, WIDTH // 2 - (self.w_button // 2), int(HEIGHT * 0.40625),
                          (5, 5, 5), (15, 15, 15), (25, 25, 25), "Training"),
            button.Button(self.w_button, self.h_button, WIDTH // 2 - (self.w_button // 2), int(HEIGHT * 0.5125),
                          (5, 5, 5), (15, 15, 15), (25, 25, 25), "Settings"),
            button.Button(self.w_button, self.h_button, WIDTH // 2 - (self.w_button // 2), int(HEIGHT * 0.6125),
                          (5, 5, 5), (15, 15, 15), (25, 25, 25), "Quit game")]
        self.bg_menu = pygame.image.load("../source/resources/bg_for_menu.png")
        self.buttons_authors = [
            button.Button(self.w_button, self.h_button, WIDTH // 2 - (self.w_button // 2), int(HEIGHT * 0.9), (5, 5, 5),
                          (15, 15, 15), (25, 25, 25), "Return to menu")]
        self.buttons_training = [
            button.Button(self.w_button, self.h_button, WIDTH // 2 - (self.w_button // 2), int(HEIGHT * 0.9), (5, 5, 5),
                          (15, 15, 15), (25, 25, 25), "Return to menu")]
        self.buttons_settings = [
            button.Button(self.w_button, self.h_button, WIDTH // 2 - (self.w_button // 2), int(HEIGHT * 0.9), (5, 5, 5),
                          (15, 15, 15), (25, 25, 25), "Return to menu"),
            button.Button(self.w_button, self.h_button, WIDTH // 2 - (self.w_button // 2), int(HEIGHT * 0.25),
                          (5, 5, 5), (15, 15, 15), (25, 25, 25), "Turn off sounds")]
        self.buttons_game_pause = [
            button.Button(self.w_button, self.h_button, WIDTH // 2 - (self.w_button // 2), int(HEIGHT * 0.3), (5, 5, 5),
                          (15, 15, 15), (25, 25, 25), "Continue"),
            button.Button(self.w_button, self.h_button, WIDTH // 2 - (self.w_button // 2), int(HEIGHT * 0.4), (5, 5, 5),
                          (15, 15, 15), (25, 25, 25), "Return to menu")]
        self.buttons_game_not_pause = [
            button.Button(self.h_button, self.h_button, WIDTH // 2 - (self.h_button // 2), int(HEIGHT * 0.01),
                          (5, 5, 5), (15, 15, 15), (25, 25, 25), "II")]
        self.magenta = (200, 0, 255)

    def init_joining_server(self):
        self.msg_text = str()
        self.ip = str()
        self.ip = ''
        self.sockIn = network.connect_InSocket(address='0.0.0.0', port=5556)

    def init_game(self):
        network.alive = True
        t1 = Thread(target=network.read_server_sock, args=(self.sockIn, self.messages))
        t1.start()
        self.platforms = get_platforms_surface()
        self.player = Player(100, 100)
        self.enemies = pygame.sprite.Group()

    @staticmethod
    def get_infinite_background():  # бесконечный background
        images['background'] = pygame.transform.scale(images['background'], (WIDTH, HEIGHT))
        img_rect = images['background'].get_rect()
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
            self.check_cursor_click_button(self.buttons_menu, event.pos)
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
                    if name_button == "Quit game":
                        self.running = False
                        network.alive = False
        else:
            self.check_cursor_on_button(self.buttons_menu, pygame.mouse.get_pos())

    def check_exit_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        return not self.running

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
            except (IndexError, ValueError):
                self.msg_text = 'IP указан неккоректно'
            else:
                network.sock_send(self.sockOut, '1')
                data, address = network.read_sock(self.sockIn)  # todo: если сервер не включен то виснет, исправить
                if data == '1':
                    self.msg_text = 'Подключение прошло успешно!'
                    self.init_game()
                    print(self.msg_text)
                    self.state = 3
                    self.music_is_off = True
                elif data == '2':
                    self.msg_text = 'Вы уже подключены к данному серверу'
                elif data == '3':
                    self.msg_text = 'Сервер уже заполнен!'
        self.ip = self.ip + event.unicode if event.unicode.isprintable() else self.ip
        print(self.ip)

    def render_ip_text(self, ip):
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
            data = self.messages[0][0].split()
            print(data)
            try:
                self.player.x, self.player.y, self.player.hp, self.player.direction, self.player.state = int(
                    float(data.pop(0))), int(float(data.pop(0))), int(
                    data.pop(0)), data.pop(0), data.pop(0)
                self.bullets = pygame.sprite.Group()
            except IndexError:
                pass
            for i in range(int(data.pop(0))):  # получение данных о пулях
                self.bullets.add(Bullet(screen, int(float(data.pop(0))), int(float(data.pop(0)))))
            n = int(data.pop(0))
            if len(self.enemies) == n:
                for sprite in self.enemies:
                    x, y, direction, state = int(float(data.pop(0))), int(float(data.pop(0))), data.pop(
                        0), data.pop(0)
                    sprite.update(x, y)
            else:  # получение данных о врагах
                for i in range(n):
                    x, y, direction, state = int(float(data.pop(0))), int(float(data.pop(0))), data.pop(
                        0), data.pop(0)
                    self.enemies.add(Player(x, y, state=state, direction=direction))
            self.messages.clear()
            print(self.enemies)

    def authors(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.check_cursor_click_button(self.buttons_authors, event.pos)
        if event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            for i in self.buttons_authors:
                if button.Button.check_cursor_release_button(i, x, y):
                    name_button = button.Button.get_name(i)
                    if name_button == "Return to menu":
                        self.state = 1
        else:
            self.check_cursor_on_button(self.buttons_authors, pygame.mouse.get_pos())

    def draw_authors(self):
        screen.blit(self.bg_menu, (0, 0))
        font = pygame.font.Font(None, 70)
        text = font.render("Authors:", 0, self.magenta)
        text_x = WIDTH // 2 - text.get_width() // 2
        screen.blit(text, (text_x, 150))
        text = font.render("Denis Bakushev", 0, self.magenta)
        text_x = WIDTH // 2 - text.get_width() // 2
        screen.blit(text, (text_x, 210))
        text = font.render("Froggling", 0, self.magenta)
        text_x = WIDTH // 2 - text.get_width() // 2
        screen.blit(text, (text_x, 270))
        text = font.render("Pavel Rudnik", 0, self.magenta)
        text_x = WIDTH // 2 - text.get_width() // 2
        screen.blit(text, (text_x, 330))
        self.draw_buttons(self.buttons_authors)

    def settings(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.check_cursor_click_button(self.buttons_settings, event.pos)
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
            self.check_cursor_on_button(self.buttons_settings, pygame.mouse.get_pos())

    def training(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.check_cursor_click_button(self.buttons_training, event.pos)
        if event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            for i in self.buttons_training:
                if button.Button.check_cursor_release_button(i, x, y):
                    name_button = button.Button.get_name(i)
                    if name_button == "Return to menu":
                        self.state = 1
        else:
            self.check_cursor_on_button(self.buttons_training, pygame.mouse.get_pos())

    def gameover(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
            self.state = 1
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 70)
        text = font.render("GAME OVER", 0, self.magenta)
        text_x = WIDTH // 2 - text.get_width() // 2
        screen.blit(text, (text_x, 150))

    def draw(self):
        self.camera.update(self.player)
        if self.timestamp <= 70:
            self.timestamp += cl.get_time()
        else:
            self.timestamp = 0
            self.player.change_image()
            for enemy in self.enemies:
                enemy.change_image()
        screen.blit(self.background, self.background.get_rect())
        screen.blit(self.platforms, self.camera.apply_rect(self.platforms.get_rect()))
        screen.blit(self.player.image, self.camera.apply(self.player))
        for bullet in self.bullets:
            bullet.move()
            screen.blit(bullet.image, bullet.rect)
        for enemy in self.enemies:
            try:
                screen.blit(enemy.image, self.camera.apply(enemy))
            except TypeError:
                pass
        if self.pause:
            bg_darkness = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA, 32)
            bg_darkness.fill((0, 0, 0))
            bg_darkness.set_alpha(150)
            screen.blit(bg_darkness, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
            self.draw_buttons(self.buttons_game_pause)
        else:
            self.draw_buttons(self.buttons_game_not_pause)

    def draw_buttons(self, buttons):
        for i in buttons:
            x, y, b_width, b_height, color, name_button = i.draw()
            pygame.draw.rect(screen, color, (x, y, b_width, b_height))
            font = pygame.font.Font(None, 70)
            text = font.render(button.Button.get_name(i), 0, self.magenta)
            text_x = x + b_width // 2 - text.get_width() // 2
            text_y = y + b_height // 2 - text.get_height() // 2
            screen.blit(text, (text_x, text_y))

    def check_cursor_on_button(self, buttons, xy):
        x, y = xy
        for i in buttons:
            if button.Button.check_cursor_on_button(i, x, y):
                continue

    def check_cursor_click_button(self, buttons, xy):
        x, y = xy
        for i in buttons:
            if button.Button.check_cursor_click_button(i, x, y):
                continue

    def run(self):
        self.music_is_off = True
        while self.running:
            if self.state == 1:  # отрисовка меню
                if self.music_is_off:
                    pygame.mixer.music.load('../source/resources/music/menu_music.mp3')
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play()
                    self.music_is_off = False
                for event in pygame.event.get():
                    self.menu(event)
                screen.blit(self.bg_menu, (0, 0))
                self.draw_buttons(self.buttons_menu)
            if self.state == 2:  # ввод IP
                pygame.mixer.music.pause()
                for event in pygame.event.get():
                    self.check_exit_event(event)
                    if event.type == pygame.KEYDOWN:
                        pygame.mixer.music.load('../source/resources/music/pechat_sound.mp3')
                        pygame.mixer.music.set_volume(1)
                        pygame.mixer.music.play()
                        self.enter_ip_address(event)
                self.render_ip_text(self.ip)
            if self.state == 3:  # Игра
                if self.music_is_off:
                    pygame.mixer.music.load('../source/resources/music/game_music.mp3')
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play()
                    self.music_is_off = False
                for event in pygame.event.get():
                    if self.check_exit_event(event):
                        network.sock_send(self.sockOut, '0')
                        break
                    if event.type == pygame.KEYDOWN:
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_ESCAPE]:
                            self.pause = not self.pause
                    if self.pause:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.check_cursor_click_button(self.buttons_game_pause, event.pos)
                        if event.type == pygame.MOUSEBUTTONUP:
                            x, y = event.pos
                            for i in self.buttons_game_pause:
                                if button.Button.check_cursor_release_button(i, x, y):
                                    name_button = button.Button.get_name(i)
                                    if name_button == "Return to menu":
                                        network.sock_send(self.sockOut, '0')
                                        self.state = 1
                                        self.music_is_off = True
                                    if name_button == "Continue":
                                        self.pause = False
                    else:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.check_cursor_click_button(self.buttons_game_not_pause, event.pos)
                        if event.type == pygame.MOUSEBUTTONUP:
                            x, y = event.pos
                            for i in self.buttons_game_not_pause:
                                if button.Button.check_cursor_release_button(i, x, y):
                                    name_button = button.Button.get_name(i)
                                    if name_button == "II":
                                        self.pause = True
                else:
                    if self.pause:
                        self.check_cursor_on_button(self.buttons_game_pause, pygame.mouse.get_pos())
                    else:
                        self.check_cursor_on_button(self.buttons_game_not_pause, pygame.mouse.get_pos())
                keys = pygame.key.get_pressed()
                self.parse_data()
                if not self.pause:
                    network.sock_send(self.sockOut, '2 ' + ''.join(map(str, keys)))
                try:
                    self.player.update(self.player.x, self.player.y)
                except ValueError:
                    continue
                if self.player.hp <= 0:
                    self.state = 7
                    network.sock_send(self.sockOut, '0')
                    network.close_sock(self.sockOut)
                self.draw()
            if self.state == 4:  # авторы
                for event in pygame.event.get():
                    self.check_exit_event(event)
                    self.authors(event)
                self.draw_authors()
            if self.state == 5:  # настройки
                for event in pygame.event.get():
                    self.check_exit_event(event)
                    self.settings(event)
                screen.blit(self.bg_menu, (0, 0))
                self.draw_buttons(self.buttons_settings)

            if self.state == 6:
                for event in pygame.event.get():
                    self.check_exit_event(event)
                    self.training(event)
                screen.blit(self.bg_menu, (0, 0))
                self.draw_buttons(self.buttons_training)

            if self.state == 7:  # Game over
                for event in pygame.event.get():
                    self.gameover(event)
            pygame.display.flip()
            cl.tick(FPS)
        try:
            network.alive = False
            network.close_sock(self.sockIn)
            network.close_sock(self.sockOut)
            pygame.quit()
        except AttributeError:
            pass
        finally:
            print('GoodBye')


game = Game()
game.run()
