import pygame
import time
import os

from src.player import Player


GFX_DIR = os.path.join(os.path.dirname(__file__), 'gfx')


class Game:

    def __init__(self, gui=True):
        self.surface = None
        self.gui = gui

        if gui:
            pygame.init()
            self.surface = pygame.display.set_mode((640, 480))
            self.red_image = pygame.image.load(os.path.join(GFX_DIR, 'player-red.png')).convert_alpha()
            self.blue_image = pygame.image.load(os.path.join(GFX_DIR, 'player-blue.png')).convert_alpha()
            self.player = Player(self.blue_image, x=640, y=480)
            self.bot = Player(self.red_image, angle=180)
            self.sprites = pygame.sprite.RenderPlain(self.player, self.bot)

    def run(self):
        tick = time.clock()
        running = True

        while running:
            if self.gui:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                    self.handle_arrow_keys(event, self.player.input_state)
                    self.handle_wsad_keys(event, self.bot.input_state)

                if time.clock() - tick > 1 / 60:
                    tick = time.clock()
                    self.on_render()

        pygame.quit()

    def handle_wsad_keys(self, event, input_state):
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_w:
                input_state.up = True

            elif event.key == pygame.K_s:
                input_state.down = True

            elif event.key == pygame.K_a:
                input_state.left = True

            elif event.key == pygame.K_d:
                input_state.right = True

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_w:
                input_state.up = False

            elif event.key == pygame.K_s:
                input_state.down = False

            elif event.key == pygame.K_a:
                input_state.left = False

            elif event.key == pygame.K_d:
                input_state.right = False

    def handle_arrow_keys(self, event, input_state):
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                input_state.up = True

            elif event.key == pygame.K_DOWN:
                input_state.down = True

            elif event.key == pygame.K_LEFT:
                input_state.left = True

            elif event.key == pygame.K_RIGHT:
                input_state.right = True

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_UP:
                input_state.up = False

            elif event.key == pygame.K_DOWN:
                input_state.down = False

            elif event.key == pygame.K_LEFT:
                input_state.left = False

            elif event.key == pygame.K_RIGHT:
                input_state.right = False

    def on_render(self):
        self.surface.fill((253, 246, 227))

        self.sprites.update()
        self.sprites.draw(self.surface)

        pygame.display.flip()
