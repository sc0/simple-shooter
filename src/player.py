import pygame


class InputState:
    def __init__(self):
        self.up = False
        self.down = False
        self.left = False
        self.right = False


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x=0, y=0, going_up=True, damage=100):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.going_up = going_up
        self.damage = damage

    def __repr__(self):
        return 'Bullet (going_up: {}, x: {}, y: {})'.format(self.going_up, self.rect.x, self.rect.y)

    def __lt__(self, other):
        return self.rect.y < other.rect.y

    def update(self, player, bot):
        if self.going_up:
            self.rect.y -= 7
        else:
            self.rect.y += 7

        if self.rect.y < 0 or self.rect.y > 480:
            self.kill()

        if self.rect.colliderect(player.rect):
            player.health -= self.damage
            self.kill()

        if self.rect.colliderect(bot.rect):
            bot.health -= self.damage
            self.kill()


class Player(pygame.sprite.Sprite):

    def __init__(self, image, x=0, y=0, angle=0):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image
        self.input_state = InputState()

        self.angle = angle

        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 100

    def update(self):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        if self.health < 1:
            self.kill()

        if self.input_state.left:
            self.rect.x -= 5
        if self.input_state.right:
            self.rect.x += 5
        if self.input_state.up:
            self.rect.y -= 5
        if self.input_state.down:
            self.rect.y += 5

        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > 640 - self.rect.width:
            self.rect.x = 640 - self.rect.width

        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > 480 - self.rect.height:
            self.rect.y = 480 - self.rect.height
