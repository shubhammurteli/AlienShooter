import random
import pygame
pygame.init()

screen = pygame.display.set_mode((500, 480))

x = 50
y = 400

width = 64
height = 64
vel = 5

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load(
    'R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load(
    'L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

score = 0


class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.heigth = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        # tuple consits of ( x-cor, y-cor, width , height)
        self.hitBox = (self.x + 17, self.y + 11, 29, 57)

    def hit(self):
        self.x = 60
        self.walkCount = 0
        # Popup on Screen
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font.render("-2", 1, (255, 0, 0))
        screen.blit(text, (250 - (text.get_width()/2), 220))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 300
                    pygame.quit()

    def draw(self, screen):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if not(self.standing):
            if self.left:
                screen.blit(walkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                screen.blit(walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                screen.blit(walkRight[0], (self.x, self.y))
            elif self.left:
                screen.blit(walkLeft[0], (self.x, self.y))
            else:
                screen.blit(char, (self.x, self.y))
        self.hitBox = (self.x + 17, self.y + 11, 29, 57)
        # rect accepts the arguments(screen, color, rect position & size, border_radius)
        # pygame.draw.rect(screen, (255, 0, 0), self.hitBox, 2)


class Bullet(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)


class enemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load(
        'R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load(
        'L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkcount = 0
        self.vel = 3
        self.hitBox = (self.x + 20, self.y, 31, 57)
        self.health = 10
        self.visible = True

    def draw(self, screen):
        self.move()
        if self.visible:
            if self.walkcount + 1 >= 33:
                self.walkcount = 0

            if self.vel > 0:
                screen.blit(
                    self.walkRight[self.walkcount//3], (self.x, self.y))
                self.walkcount += 1
            else:
                screen.blit(self.walkLeft[self.walkcount//3], (self.x, self.y))
                self.walkcount += 1
            pygame.draw.rect(screen, (255, 0, 0),
                             (self.hitBox[0], self.hitBox[1] - 20, 50, 10))
            pygame.draw.rect(
                screen, (0, 128, 0), (self.hitBox[0], self.hitBox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitBox = (self.x + 17, self.y + 2, 31, 57)
            # pygame.draw.rect(screen, (255, 0, 0), self.hitBox, 2)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkcount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1

    # collision
    def hit(self):
        if self.health > 1:
            self.health -= 1
        else:
            self.visible = False
        print("hit")


clock = pygame.time.Clock()

# sound variables
bulletSound = pygame.mixer.Sound('bullet.mp3')
hitSound = pygame.mixer.Sound('hit.mp3')

# Background Sound
music = pygame.mixer.music.load('music.mp3')
# -1 for Continous loop
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

# Functions


def reDraw():
    screen.blit(bg, (0, 0))
    text = font.render("Score: " + str(score), 1, (0, 0, 255))
    screen.blit(text, (360, 10))
    man.draw(screen)
    goblin.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    pygame.display.update()


# main loop
man = player(200, 400, 64, 64)
goblin = enemy(100, 410, 64, 64, 450)

bullets = []
bulletRelease = 0
# syntax is pygame.font.SysFont(name_of_font, size_of_font, True for bold(optional), True for italic(optional))
font = pygame.font.SysFont('comicsans', 28, True)

run = True
while run:
    ran = random.randint(100, 410)
    # looping delay in ms i.e. Framerate

    while not(goblin.visible):
        goblin = enemy(ran, 410, 64, 64, 450)
    if goblin.visible == True:
        # Player and Enemies Collision Detection
        if man.hitBox[1] < goblin.hitBox[1] + goblin.hitBox[3] and man.hitBox[1] + man.hitBox[3] > goblin.hitBox[1]:
            # Bullet is inside the left side of hitbox and bullet is inside the right side of goblin hitbox
            if man.hitBox[0] > goblin.hitBox[0] and man.hitBox[0] < goblin.hitBox[0] + goblin.hitBox[2]:
                man.hit()
                score -= 2

    clock.tick(27)
    if bulletRelease > 0:
        bulletRelease += 1
    if bulletRelease > 3:
        bulletRelease = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        # Below the top of hitbox of goblin and above the bottom of hitbox of goblin
        if bullet.y - bullet.radius < goblin.hitBox[1] + goblin.hitBox[3] and bullet.y + bullet.radius > goblin.hitBox[1]:
            # Bullet is inside the left side of hitbox and bullet is inside the right side of goblin hitbox
            if bullet.x + bullet.radius > goblin.hitBox[0] and bullet.x - bullet.radius < goblin.hitBox[0] + goblin.hitBox[2]:
                goblin.hit()
                hitSound.play()
                hitSound.set_volume(0.2)
                score += 1
                bullets.pop(bullets.index(bullet))

        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()
    # Movement
    if keys[pygame.K_SPACE] and bulletRelease == 0:
        bulletSound.play()
        bulletSound.set_volume(0.2)
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5:
            bullets.append(Bullet(round(man.x + man.width // 2),
                                  round(man.y + man.width // 2), 4, (0, 0, 0), facing))
        bulletRelease = 1

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0
    if not(man.isJump):
        if keys[pygame.K_UP]:
            man.isJump = True
            man.left = False
            man.right - False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10

    # Jump movement
    reDraw()

pygame.quit()
