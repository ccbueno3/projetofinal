import pygame

pygame.init()

largura = 800
altura = 600
janela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo do Nome")

nome = ""
executando = True

while executando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN:  # Se o jogador pressionar Enter
                executando = False
            elif evento.key == pygame.K_BACKSPACE:  # Se o jogador pressionar Backspace
                nome = nome[:-1]
            else:
                nome += evento.unicode
    # Limpe a janela e desenhe o nome digitado até agora
    janela.fill((255, 255, 255))
    fonte = pygame.font.Font(None, 36)
    texto = fonte.render("Digite seu nome: " + nome, True, (0, 0, 0))
    janela.blit(texto, (10, 10))
    pygame.display.flip()
