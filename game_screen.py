import pygame
from config import FPS, OVER, WHITE, WIDTH, HEIGHT, BLACK, YELLOW, RED, QUIT, INIT
from assets import load_assets, DESTROY_SOUND, BOOM_SOUND, BACKGROUND, SCORE_FONT
from sprites import Ship, Meteor, Bullet, Explosion, Heart


def game_screen(window):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    assets = load_assets()

    # Criando um grupo 
    all_sprites = pygame.sprite.Group()
    all_meteors = pygame.sprite.Group()
    all_bullets = pygame.sprite.Group()
    all_hearts = pygame.sprite.Group()
    groups = {}
    groups['all_sprites'] = all_sprites
    groups['all_meteors'] = all_meteors
    groups['all_bullets'] = all_bullets
    groups['all_hearts'] = all_hearts

    # Criando o jogador
    player = Ship(groups, assets)
    all_sprites.add(player)
    
    # Criando os meteoros
    for i in range(8):
        meteor = Meteor(assets)
        all_sprites.add(meteor)
        all_meteors.add(meteor)

    DONE = 0
    PLAYING = 1
    EXPLODING = 2
    state = PLAYING

    keys_down = {}
    score = 0
    lives = 3

    # ===== Loop principal =====
    pygame.mixer.music.play(loops=-1)

    next_state = OVER

    while state != DONE:
        clock.tick(FPS)

        # ----- Trata eventos
        for event in pygame.event.get():
            # ----- Verifica consequências
            if event.type == pygame.QUIT:
                state = DONE
                next_state = QUIT
            # Só verifica o teclado se está no estado de jogo
            if state == PLAYING:
                # Verifica se apertou alguma tecla.
                if event.type == pygame.KEYDOWN:
                    # Dependendo da tecla, altera a velocidade.
                    keys_down[event.key] = True
                    if event.key == pygame.K_LEFT:
                        player.speedx -= 8
                    if event.key == pygame.K_RIGHT:
                        player.speedx += 8
                    if event.key == pygame.K_UP:
                        player.speedy -= 8
                    if event.key == pygame.K_DOWN:
                        player.speedy += 8
                    if event.key == pygame.K_SPACE:
                        player.shoot()
                # Verifica se soltou alguma tecla.
                if event.type == pygame.KEYUP:
                    # Dependendo da tecla, altera a velocidade.
                    if event.key in keys_down and keys_down[event.key]:
                        if event.key == pygame.K_LEFT:
                            player.speedx += 8
                        if event.key == pygame.K_RIGHT:
                            player.speedx -= 8
                        if event.key == pygame.K_UP:
                            player.speedy += 8
                        if event.key == pygame.K_DOWN:
                            player.speedy -= 8

        # ----- Atualiza estado do jogo
        # Atualizando a posição dos meteoros
        all_sprites.update()

        if state == PLAYING:
            # Verifica se houve colisão entre tiro e meteoro
            hits = pygame.sprite.groupcollide(all_meteors, all_bullets, True, True, pygame.sprite.collide_mask)
            for meteor in hits: # As chaves são os elementos do primeiro grupo (meteoros) que colidiram com alguma bala
                # O meteoro e destruido e precisa ser recriado
                assets[DESTROY_SOUND].play()
                m = Meteor(assets)
                all_sprites.add(m)
                all_meteors.add(m)

                # No lugar do meteoro antigo, adicionar uma explosão.
                explosao = Explosion(meteor.rect.center, assets)
                all_sprites.add(explosao)

                # Ganhou pontos!
                score += 100
                if score % 1000 == 0:
                    lives += 1
                    heart = Heart(assets)
                    all_sprites.add(heart)
                    all_hearts.add(heart)
                    



                # Cria um meteoro a mais a cada 500 pontos
                if score % 500 == 0:
                    meteor = Meteor(assets)
                    all_sprites.add(meteor)
                    all_meteors.add(meteor)

            # Verifica se há colisão entre o player e o coracao
            hits = pygame.sprite.spritecollide(player, all_hearts, True, pygame.sprite.collide_mask)
            if len(hits) > 0:
                heart.kill()
                lives += 1
                
            # Verifica se houve colisão entre nave e meteoro
            hits = pygame.sprite.spritecollide(player, all_meteors, True, pygame.sprite.collide_mask)
            if len(hits) > 0:
                # Toca o som da colisão
                assets[BOOM_SOUND].play()
                player.kill()
                lives -= 1

                explosao = Explosion(player.rect.center, assets)
                all_sprites.add(explosao)

                state = EXPLODING
                keys_down = {}
                explosion_tick = pygame.time.get_ticks()
                explosion_duration = explosao.frame_ticks * len(explosao.explosion_anim) + 400

        elif state == EXPLODING:
            now = pygame.time.get_ticks()
            if now - explosion_tick > explosion_duration:
                if lives == 0:
                    state = DONE
                else:
                    state = PLAYING
                    player = Ship(groups, assets)
                    all_sprites.add(player)

        # ----- Gera saídas
        window.fill(BLACK)  # Preenche com a cor branca
        window.blit(assets[BACKGROUND], (0, 0))
        # Desenhando meteoros
        all_sprites.draw(window)

        # Desenhando o score
        text_surface = assets[SCORE_FONT].render("{:08d}".format(score), True, YELLOW)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (WIDTH / 2,  10)
        window.blit(text_surface, text_rect)

        # Desenhando as vidas
        text_surface = assets[SCORE_FONT].render(chr(9829) * lives, True, RED)
        text_rect = text_surface.get_rect()
        text_rect.bottomleft = (10, HEIGHT - 10)
        window.blit(text_surface, text_rect)

        pygame.display.update()  # Mostra o novo frame para o jogador

    return next_state, score