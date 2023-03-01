import pygame


def modo_exemplo_grafico():
    pygame.init()

    pygame.display.set_caption("Exemplo básico dos gráficos")
    largura_da_janela = 800
    altura_da_janela = 600
    janela = pygame.display.set_mode((largura_da_janela, altura_da_janela))

    imagem_logo_gekitai = pygame.image.load("assets/logo.png")
    retangulo_da_imagem = imagem_logo_gekitai.get_rect()

    pos_x_da_imagem = 0
    pos_y_da_imagem = 0
    velocidade_do_eixo_x_para_imagem = 2
    velocidade_do_eixo_y_para_imagem = 2

    relogio = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        pos_x_da_imagem += velocidade_do_eixo_x_para_imagem
        pos_y_da_imagem += velocidade_do_eixo_y_para_imagem

        if (
            pos_x_da_imagem < 0
            or pos_x_da_imagem + retangulo_da_imagem.width > largura_da_janela
        ):
            velocidade_do_eixo_x_para_imagem *= -1
        if (
            pos_y_da_imagem < 0
            or pos_y_da_imagem + retangulo_da_imagem.height > altura_da_janela
        ):
            velocidade_do_eixo_y_para_imagem *= -1

        janela.fill((0, 0, 0))
        janela.blit(imagem_logo_gekitai, (pos_x_da_imagem, pos_y_da_imagem))
        pygame.display.update()

        relogio.tick(60)
