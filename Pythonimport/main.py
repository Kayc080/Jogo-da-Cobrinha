import pygame
import random

# Iniciar o pygame
pygame.init()

pygame.display.set_caption("Jogo da cobrinha")
LARGURA, ALTURA = 1200, 800
tela = pygame.display.set_mode((LARGURA, ALTURA))

relogio = pygame.time.Clock()

# Criar cores RGB
preta = (0, 0, 0)
branca = (255, 255, 255)
vermelha = (255, 0, 0)
verde = (0, 255, 0)

tamanho_quadrado = 20

# FPS do jogo (velocidade inicial)
velocidade_jogo = 15


def mensagem_fim_jogo(pontos):
    """Exibe a tela de fim de jogo."""
    fonte = pygame.font.SysFont("Arial", 48)
    texto_fim = fonte.render("GAME OVER", True, vermelha)
    texto_pontos = fonte.render(f"Pontos: {pontos}", True, branca)
    texto_reiniciar = fonte.render("Pressione R para reiniciar ou Q para sair", True, branca)

    tela.fill(preta)
    tela.blit(texto_fim, (LARGURA // 2 - texto_fim.get_width() // 2, ALTURA // 3))
    tela.blit(texto_pontos, (LARGURA // 2 - texto_pontos.get_width() // 2, ALTURA // 3 + 60))
    tela.blit(texto_reiniciar, (LARGURA // 2 - texto_reiniciar.get_width() // 2, ALTURA // 3 + 120))
    pygame.display.update()


def jogo():
    """Lógica principal do jogo."""
    comida_x = round(random.randrange(0, LARGURA - tamanho_quadrado) / float(tamanho_quadrado)) * float(tamanho_quadrado)
    comida_y = round(random.randrange(0, ALTURA - tamanho_quadrado) / float(tamanho_quadrado)) * float(tamanho_quadrado)

    x = LARGURA / 2
    y = ALTURA / 2

    velocidade_x = 0
    velocidade_y = 0

    tamanho_cobra = 1
    segmentos_cobra = []

    fim_jogo = False
    sair = False

    global velocidade_jogo
    velocidade_jogo = 15  # Reiniciar a velocidade sempre que o jogo é reiniciado

    while not sair:
        while fim_jogo:
            mensagem_fim_jogo(tamanho_cobra - 1)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    sair = True
                    fim_jogo = False
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_r:  # Reiniciar o jogo
                        jogo()
                    if evento.key == pygame.K_q:  # Sair do jogo
                        sair = True
                        fim_jogo = False

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                sair = True
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN and velocidade_y == 0:
                    velocidade_x = 0
                    velocidade_y = tamanho_quadrado
                elif evento.key == pygame.K_UP and velocidade_y == 0:
                    velocidade_x = 0
                    velocidade_y = -tamanho_quadrado
                elif evento.key == pygame.K_RIGHT and velocidade_x == 0:
                    velocidade_x = tamanho_quadrado
                    velocidade_y = 0
                elif evento.key == pygame.K_LEFT and velocidade_x == 0:
                    velocidade_x = -tamanho_quadrado
                    velocidade_y = 0

        x += velocidade_x
        y += velocidade_y

        segmentos_cobra.append([x, y])
        if len(segmentos_cobra) > tamanho_cobra:
            del segmentos_cobra[0]

        # Verificar colisão com o próprio corpo
        for lista in segmentos_cobra[:-1]:
            if lista == [x, y]:
                fim_jogo = True

        # Verificar colisão com a parede
        if x < 0 or x >= LARGURA or y < 0 or y >= ALTURA:
            fim_jogo = True

        tela.fill(preta)

        for lista in segmentos_cobra:
            pygame.draw.rect(tela, verde, [lista[0], lista[1], tamanho_quadrado, tamanho_quadrado])

        pygame.draw.rect(tela, vermelha, [comida_x, comida_y, tamanho_quadrado, tamanho_quadrado])

        fonte = pygame.font.SysFont("Arial", 32)
        texto = fonte.render(f"Pontos: {tamanho_cobra - 1}", True, vermelha)
        tela.blit(texto, [2, 1])

        pygame.display.update()

        if x == comida_x and y == comida_y:
            tamanho_cobra += 1
            # Aumentar a velocidade do jogo conforme o tamanho da cobra
            velocidade_jogo += 0.5
            comida_x = round(random.randrange(0, LARGURA - tamanho_quadrado) / float(tamanho_quadrado)) * float(tamanho_quadrado)
            comida_y = round(random.randrange(0, ALTURA - tamanho_quadrado) / float(tamanho_quadrado)) * float(tamanho_quadrado)

        relogio.tick(velocidade_jogo)

    pygame.quit()


jogo()
