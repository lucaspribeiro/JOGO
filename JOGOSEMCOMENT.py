import pygame, random, time 

from pygame.locals import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

pygame.init()

pygame.mixer.music.set_volume(0.01)
background_music = pygame.mixer.music.load('fundoMusica.ogg')
pygame.mixer.music.play(-1)

collision_sound = pygame.mixer.Sound('colisaoMusica.wav')
pygame.mixer.music.set_volume(0.01)

obstacle = 0 

font = pygame.font.SysFont('arial', 30, True, False)
score = 0

screen = pygame.display.set_mode((640, 480))
 
pygame.display.set_caption('SALLES VERSO')

background_image = pygame.image.load('fundoCidade.png').convert()
background_image = pygame.transform.scale(background_image, (640, 480))

position_x = 300
position_y = 440

is_right = is_left = False

clock = pygame.time.Clock()

position_yobst = -100

aux = 0

vector_position_xobst = []
vector_position_yobst = []

for i in range(20):
    position_xobst = random.randint(0, 620)
    vector_position_xobst.append(position_xobst)

    aux = random.randint(-100, -50)
    position_yobst += aux 
    vector_position_yobst.append(position_yobst)

position_xbon = random.randint(0, 620)
position_ybon = 0

bonus_ativo = False
jogo_rodando = True

while jogo_rodando:

    clock.tick(30)

    text = f'Colisões:{score}'
    text_format = font.render(text, True, GREEN)

    for event in pygame.event.get():
        if event.type == QUIT:  
            pygame.quit()

        if event.type == pygame.KEYDOWN:   
            if event.key == pygame.K_a:
                is_left = True

            if event.key == pygame.K_d:
                is_right = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                is_left = False

            if event.key == pygame.K_d:
                is_right = False

    if is_right:
        position_x += 10

    if is_left:
        position_x -= 10

    screen.blit(background_image, (0,0))

    character = pygame.draw.rect(screen, WHITE, [position_x, position_y, 40, 40]) 
    
    if not bonus_ativo:
        bonus = pygame.draw.rect(screen, BLUE, [position_xbon, position_ybon, 20, 20])
        position_ybon += 10 

    for j in range(19):
        obstacle = pygame.draw.rect(screen, RED, [vector_position_xobst[j], vector_position_yobst[j], 20, 20])
        
        vector_position_yobst[j] += 10
        
        if character.colliderect(obstacle):
            vector_position_yobst[j] = -100

            if bonus_ativo:
                bonus_ativo = False                
                break
            
            if bonus_ativo == False:    
                collision_sound.play()
                vector_position_yobst[j] = 0
                jogo_rodando = False
                
                break
           
        
    if character.colliderect(bonus):
        bonus_ativo = True
        position_ybon = -100

    for k in range(20):
        if vector_position_yobst[k] > 640:
            vector_position_yobst[k] = random.randint(-100, -50)
            vector_position_xobst[k] = random.randint(20, 620)

    if position_ybon > 640:
        position_ybon = random.randint(-100, -20)
        position_xbon = random.randint(0, 620)

    screen.blit(text_format, (450,40))

    pygame.display.flip()
