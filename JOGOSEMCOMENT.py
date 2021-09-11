import pygame, random, time 

from pygame.locals import *

#  cores para serem usadas durante o jogo
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

#  tamanho da tela 
WIDTH = 640
HEIGHT = 480

#  velocidade do jogador no eixo x 
speed_player = 10

#  classe do jogador, obstáculo e das balas 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.image_run = [pygame.image.load('sprites/sprite_0.png'),
                          pygame.image.load('sprites/sprite_1.png'),
                          pygame.image.load('sprites/sprite_2.png')
                          ]

        self.image = pygame.image.load('sprites/sprite_0.png')
        self.rect = pygame.Rect(320, 345, 32*2, 32*2)
        self.current_image = 0
    
    def update(self, *args):
        
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.rect[0] -= speed_player
            
        if key[pygame.K_d]:
            self.rect[0] += speed_player
            
        self.current_image = (self.current_image + 1) % 3
        self.image = self.image_run[self.current_image]
        self.image = pygame.transform.scale(self.image, (32*2, 32*2))
           
        if self.rect.x < -10:
            self.rect.x = -10
        elif self.rect.x > 600:
            self.rect.x = 600


class Obstacle(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            
            self.image = pygame.image.load('sprites/sprite_3.png')
            self.image = pygame.transform.scale(self.image, (32, 32))
            self.rect = pygame.Rect(450, -100 , 32, 32)
            
            self.speed = 5

            self.rect.x = random.randint(32, 608)
            self.rect.y = random.randint(-100, -50)

        def update(self, *args):
            self.rect.y += self.speed

            if self.rect.bottom > 500:
                self.kill()

class Bullets(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            
            self.image = pygame.image.load('sprites/sprite_4.png')
            self.image = pygame.transform.scale(self.image, (10, 10))
            self.rect = self.image.get_rect()
            
            self.speed = 5
    
        def update(self, *args):
            self.rect.y -= self.speed

            if self.rect.top < 0:
                self.kill()


pygame.init() 

#  grupos das classes do jogo 
player_group = pygame.sprite.Group()
player = Player()
player_group.add(player)

obstacle_group = pygame.sprite.Group()
obstacle = Obstacle()
obstacle_group.add(obstacle)

bullets_group = pygame.sprite.Group()
bullets = Bullets()
bullets_group.add(bullets)

#  músicas
pygame.mixer.music.set_volume(0.1)
background_music = pygame.mixer.music.load('fundoMusica.ogg')
pygame.mixer.music.play(-1)

pygame.mixer.music.set_volume(0.1)
collision_sound = pygame.mixer.Sound('colisaoMusica.wav')
 
pygame.mixer.music.set_volume(0.1)
bonus_sound = pygame.mixer.Sound('bonusMusica.wav')

#  fonte da pontuação
font = pygame.font.SysFont('Corbel', 30, True, False)
score = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('SALLES VS WINDOWS')


background_image = pygame.image.load('fundoCidade.png')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))


game_loop = True

def draw():
    player_group.draw(screen)
    obstacle_group.draw(screen)

def update():
    player_group.update()
    obstacle_group.update()

# atualizar o fps dentro do loop 
clock = pygame.time.Clock()

# tempo para dar spawn em novos obstáculos dentro do loop
timer = 20

while game_loop:
    
    clock.tick(60)

    screen.blit(background_image, (0, 0))

    text = f'Pontuação:   {score}'
    text_format = font.render(text, True, WHITE)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bonus_sound.play()
                new_Bullet = Bullets()
                player_group.add(new_Bullet) 
                bullets_group.add(new_Bullet)
                new_Bullet.rect.center = player.rect.center

    timer += 1

    if timer > 30:
        timer = 0
        if random.random() < 0.7:
            newObstacle = Obstacle()
            obstacle_group.add(newObstacle)

    collisions = pygame.sprite.spritecollide(player, obstacle_group, False, pygame.sprite.collide_mask)

    hits = pygame.sprite.groupcollide(bullets_group, obstacle_group, True, True, pygame.sprite.collide_mask)

    if collisions:
        game_loop = False

    screen.blit(text_format, (450,40))

    update()  
    draw()
    pygame.display.flip()
