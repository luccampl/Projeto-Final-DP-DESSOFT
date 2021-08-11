import pygame
import random
from os import path
from sprites import Tecla
from config import IMG_DIR, BLACK, FPS, GAME, QUIT


def init_screen(screen):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    # Carrega o fundo da tela inicial
    background = pygame.image.load(path.join(IMG_DIR, 'tela_inicio_01.PNG')).convert()
    background_rect = background.get_rect()

    all_sprites = pygame.sprite.Group()
    texto = Tecla()
    all_sprites.add(texto)


    running = True
    while running:

        # Ajusta a velocidade do jogo.
        clock.tick(FPS)
        
        all_sprites.update()
        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():
            # Verifica se foi fechado.
            if event.type == pygame.QUIT:
                state = QUIT
                running = False

            if event.type == pygame.KEYUP:
                state = GAME
                running = False

        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        screen.blit(background, background_rect)

        all_sprites.draw(screen)

        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()

    return state
