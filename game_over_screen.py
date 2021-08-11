from assets import load_assets
import pygame
import random
from os import path
from config import IMG_DIR, BLACK, FPS, GAME, INIT, OVER, QUIT, WIDTH, HEIGHT, WHITE
from assets import SCORE_FONT, load_assets

def game_over_screen(screen, score):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()
    assets = load_assets()
    # Carrega o fundo da tela inicial
    background = pygame.image.load(path.join(IMG_DIR, 'game_over_screen_02.PNG')).convert()
    background_rect = background.get_rect()

    running = True
    while running:

        # Ajusta a velocidade do jogo.
        clock.tick(FPS)

        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():
            # Verifica se foi fechado.
            if event.type == pygame.QUIT:
                state = QUIT
                running = False

            if event.type == pygame.KEYUP:
                state = INIT
                running = False

        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        screen.blit(background, background_rect)

        # Desenhando o score
        text_surface = assets[SCORE_FONT].render("{:08d}".format(score), True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = ((WIDTH / 2)-10,  210)
        screen.blit(text_surface, text_rect)

        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()

    return state
