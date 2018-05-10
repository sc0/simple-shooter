import pygame
import time
import os
import curses

import src.config as cfg
from src.player import Player, Bullet


class Game:

    def __init__(self, gui=True):
        self.surface = None
        self.gui = gui
        self.file = None
        self.screen = curses.initscr()
        curses.curs_set(0)

        if gui:
            pygame.init()
            self.surface = pygame.display.set_mode((640, 480))
            self.red_image = pygame.image.load(os.path.join(cfg.GFX_DIR, 'player-red.png')).convert_alpha()
            self.blue_image = pygame.image.load(os.path.join(cfg.GFX_DIR, 'player-blue.png')).convert_alpha()
            self.bullet_image = pygame.image.load(os.path.join(cfg.GFX_DIR, 'bullet.png')).convert_alpha()
            self.player = Player(self.blue_image, x=640, y=480)
            self.bot = Player(self.red_image, angle=180)
            self.bullets = pygame.sprite.RenderPlain()
            self.sprites = pygame.sprite.RenderPlain(self.player, self.bot)
            self.game_time = 0

    def run(self):
        tick = time.clock()
        running = True

        while running:
            if self.gui:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                    self.handle_arrow_keys(event, self.player)
                    self.handle_wsad_keys(event, self.bot)

                if time.clock() - tick > 1 / 60:
                    tick = time.clock()
                    self.game_time += 1
                    self.on_render()
                    if self.game_time % 5 == 0:
                        self.raport()
                    self.save_game_state('game.sav')

                if not self.player.alive() or not self.bot.alive():
                    self.raport()
                    running = False

        self.file.close()
        pygame.quit()

    def handle_wsad_keys(self, event, player):
        input_state = player.input_state

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_w:
                input_state.up = True

            elif event.key == pygame.K_s:
                input_state.down = True

            elif event.key == pygame.K_a:
                input_state.left = True

            elif event.key == pygame.K_d:
                input_state.right = True

            elif event.key == pygame.K_e:
                bullet = Bullet(self.bullet_image,
                                x=player.rect.x + 22, # wyśrodkowanie w poziomie
                                y=player.rect.y + (-20 if player.angle == 0 else 60), # podniesienie ponad gracza
                                going_up=player.angle == 0, damage=cfg.BULLET_DAMAGE)
                self.bullets.add(bullet)

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_w:
                input_state.up = False

            elif event.key == pygame.K_s:
                input_state.down = False

            elif event.key == pygame.K_a:
                input_state.left = False

            elif event.key == pygame.K_d:
                input_state.right = False

    def handle_arrow_keys(self, event, player):
        input_state = player.input_state

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                input_state.up = True

            elif event.key == pygame.K_DOWN:
                input_state.down = True

            elif event.key == pygame.K_LEFT:
                input_state.left = True

            elif event.key == pygame.K_RIGHT:
                input_state.right = True

            elif event.key == pygame.K_SPACE:
                # input_state.shoot = True
                bullet = Bullet(self.bullet_image,
                                x=player.rect.x + 22,  # wyśrodkowanie w poziomie
                                y=player.rect.y + (-20 if player.angle == 0 else 60),  # podniesienie ponad gracza
                                going_up=player.angle == 0, damage=cfg.BULLET_DAMAGE)
                self.bullets.add(bullet)

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_UP:
                input_state.up = False

            elif event.key == pygame.K_DOWN:
                input_state.down = False

            elif event.key == pygame.K_LEFT:
                input_state.left = False

            elif event.key == pygame.K_RIGHT:
                input_state.right = False

            # elif event.key == pygame.K_SPACE:
                # input_state.shoot = False

    def on_render(self):
        self.surface.fill((253, 246, 227))

        self.sprites.update()
        self.bullets.update(self.player, self.bot)

        self.sprites.draw(self.surface)
        self.bullets.draw(self.surface)

        pygame.display.flip()

    def get_game_state(self):
        state = [
            self.player.rect.x,
            self.player.rect.y,
            self.player.health,
            self.bot.rect.x,
            self.bot.rect.y,
            self.bot.health,
            len(self.bullets),
        ]

        bullets_going_up = []
        bullets_going_down = []

        for bullet in iter(self.bullets):
            if bullet.going_up:
                bullets_going_up.append(bullet)

            if not bullet.going_up:
                bullets_going_down.append(bullet)

        sorted(bullets_going_up)
        sorted(bullets_going_down)

        for bullet in bullets_going_up:
            state.append(bullet.rect.x)
            state.append(bullet.rect.y)

        for bullet in bullets_going_down:
            state.append(bullet.rect.x)
            state.append(bullet.rect.y)

        return state

    def save_game_state(self, filename):
        if not self.file:
            self.file = open(filename, 'w+')

        state = self.get_game_state()

        for item in state:
            self.file.write('%s ' % str(item))

        self.file.write('\n')

    def count_fitness(self, player, opponent):
        return cfg.DMG_TAKEN_MULTIPLIER * (100-player.health) + \
               cfg.GAME_TIME_MULTIPLIER * self.game_time + \
               cfg.DMG_GIVEN_MULTIPLIER * (100-opponent.health)

    def raport(self):
        self.screen.clear()
        self.screen.addstr(0, 0, 'Game time: ' + str(self.game_time))

        self.screen.addstr(2, 0, 'Red health: ' + str(self.bot.health) + (' (alive)' if self.bot.alive() else ' (dead)'))
        self.screen.addstr(3, 0, 'Blue health: ' + str(self.player.health) + (' (alive)' if self.player.alive() else ' (dead)'))

        self.screen.addstr(2, 25, 'fitness: ' + str(self.count_fitness(self.bot, self.player)))
        self.screen.addstr(3, 25, 'fitness: ' + str(self.count_fitness(self.player, self.bot)))

        self.screen.addstr(5, 0, 'Bullet damage: ' + str(cfg.BULLET_DAMAGE))
        self.screen.addstr(5, 20, 'DMG taken multiplier: ' + str(-5))
        self.screen.addstr(5, 50, 'DMG given multiplier: ' + str(10))
        self.screen.addstr(5, 80, 'Game time multiplier: ' + str(2))
        self.screen.addstr(6, 0, 'Bullets on screen: ' + str(len(self.bullets)))

        self.screen.refresh()
        # print(self.get_game_state())

