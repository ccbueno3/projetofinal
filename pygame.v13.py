import pygame
import random

pygame.init()
pygame.mixer.init()


# Cores
BRANCO = (255, 255, 255)
LARANJA = (255, 165, 0)
PRETO = (0, 0, 0)
MARROM = (150, 75, 0)
VERDE = (39,71,57)
VERDE_CLARO = (0,255,0)
CINZA = (128,128,128)
VERMELHO = (255,0,0)

#imagens 

#logo
imagem_logo = pygame.image.load("imagens/logo_foxxer.png")
tamanho_x_logo = 700/2
tamanho_y_logo = 500/2
imagem_logo = pygame.transform.scale(imagem_logo, (tamanho_x_logo, tamanho_y_logo))

#fundo menu foxer 
imagem_menu = pygame.image.load("imagens/menu_foxxer.png")
imagem_menu = pygame.transform.scale(imagem_menu, (800, 700))

#configurações
imagem_configuracoes = pygame.image.load("imagens/mapa_final.png")
tamanho_x_configuracoes = 800
tamanho_y_configuracoes = 700
imagem_configuracoes = pygame.transform.scale(imagem_configuracoes, (tamanho_x_configuracoes, tamanho_y_configuracoes))

#imagem fundo
imagem_fundo = pygame.image.load("imagens/mapa_final.png")
imagem_fundo = pygame.transform.scale(imagem_fundo,(800,700))



def tela_inicio():
    pygame.init()
    largura = 800
    altura = 700
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Foxxer")
    iniciado = False
    texto_inicial = True

    while not iniciado:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and texto_inicial:
                    iniciado = True
                    jogo_principal()
                elif event.key == pygame.K_t:
                    if texto_inicial:
                        texto_inicial = False
                elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                elif event.key == pygame.K_BACKSPACE:
                    if not texto_inicial:
                        texto_inicial = True

        tela.fill(BRANCO)
        fonte_inicio = pygame.font.SysFont("Comic Sans", 36)

        if texto_inicial:
            tela.blit(imagem_menu,(0,0))
            tela.blit(imagem_logo,((largura - tamanho_x_logo)/2,0))
            texto_inicio = fonte_inicio.render("Pressione 'Enter' para iniciar", True, PRETO)
            texto_embaixo = fonte_inicio.render("Pressione 'T' para aprender a jogar", True, PRETO)
            tela.blit(texto_inicio, (largura // 2 - texto_inicio.get_width() // 2, altura *0.8 - texto_inicio.get_height() // 2))
            tela.blit(texto_embaixo, (largura // 2 - texto_embaixo.get_width() // 2, altura *0.9 - texto_embaixo.get_height() // 2))
        else:
            tela.blit(imagem_configuracoes,(0,0))
            informacoes = fonte_inicio.render("W - anda para cima", True, PRETO)
            tela.blit(informacoes, (largura // 2 - informacoes.get_width() // 2, 50))
            informacoes = fonte_inicio.render("A - anda para esquerda", True, PRETO)
            tela.blit(informacoes, (largura // 2 - informacoes.get_width() // 2,90))
            informacoes = fonte_inicio.render("S - anda para baixo", True, PRETO)
            tela.blit(informacoes, (largura // 2 - informacoes.get_width() // 2, 130))
            informacoes = fonte_inicio.render("D - anda para cima", True, PRETO)
            tela.blit(informacoes, (largura // 2 - informacoes.get_width() // 2, 170))
            informacoes = fonte_inicio.render("ESC - fecha o jogo", True, PRETO)
            tela.blit(informacoes, (largura // 2 - informacoes.get_width() // 2,210))
            informacoes = fonte_inicio.render("RETURN - volta para o menu", True, PRETO)
            tela.blit(informacoes, (largura // 2 - informacoes.get_width() // 2, 250))
            
                        
        pygame.display.flip()


def jogo_principal():
    # Dimensões da janela do jogo
    largura = 800
    altura = 700

    # Dimensões do grid
    largura_bloco = 50
    altura_bloco = 50
    num_blocos_x = largura// largura_bloco
    num_blocos_y = altura // altura_bloco

    # Classe para representar o jogador
    class Player(pygame.sprite.Sprite):
        def __init__(self, x, y):   
            super().__init__()
            self.image = pygame.image.load("imagens/Raposa3.png").convert_alpha()
            self.image = pygame.transform.scale(self.image,(50,50))
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect.x = x * largura_bloco
            self.rect.y = y * altura_bloco
            self.invulneravel = False
            self.ticks_invulneravel = 0

        def update(self, dx=0, dy=0):
            if self.invulneravel:
                self.ticks_invulneravel += 1
                if self.ticks_invulneravel >= 60:  #quantidade de tempo sem poder se mexer 
                    self.invulneravel = False
                    self.ticks_invulneravel = 0
                    self.image = pygame.image.load("imagens/Raposa3.png").convert_alpha()  
                    self.image = pygame.transform.scale(self.image,(50,50))
            if not self.invulneravel:
                colisoes = pygame.sprite.spritecollide(self, carros, False, pygame.sprite.collide_mask)
                colisoes2 = jogador.rect.colliderect(pygame.Rect(0, altura_bloco, largura, (num_blocos_y // 2 - 1) * altura_bloco))
                if colisoes or colisoes2:
                    self.invulneravel = True
                    self.image = pygame.image.load("imagens/Raposa_dormindo.png")

            if 0 <= self.rect.x + dx < largura - largura_bloco and dx != 0 and not self.invulneravel:
                self.rect.x += dx
            if 0 <= self.rect.y + dy < altura - altura_bloco and dy != 0 and not self.invulneravel:
                self.rect.y += dy

    # Classe para representar os carros
    class Carro(pygame.sprite.Sprite):
        def __init__(self, x, y, velocidade, tamanho, tipo):
            super().__init__()
            if tipo == 1:
                self.image = pygame.image.load("imagens/caminhao.png")
            elif tipo == 2:
                self.image = pygame.image.load("imagens/Moto.png")
            elif tipo == 3:
                self.image = pygame.image.load("imagens/carro_fogo.png")
            elif tipo == 4:
                self.image = pygame.image.load("imagens/Fusca.png")
            else:
                self.image = pygame.image.load("imagens/Savero.png")

            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect.x = x * largura_bloco
            self.rect.y = y * altura_bloco
            self.velocidade = velocidade

        def update(self):
            self.rect.x += self.velocidade
            if self.rect.left > largura:
                self.rect.right = 0
            if self.rect.right < 0:
                self.rect.left = largura

    class Lobo(pygame.sprite.Sprite):
        def __init__(self, x, y, velocidade):
            super().__init__()
            self.image = pygame.image.load("imagens/lobo.png")
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect.x = x * largura_bloco
            self.rect.y = y * altura_bloco
            self.velocidade = velocidade

        def update(self):
            if tempo_passado % 2 != 0:
                self.image = pygame.image.load("imagens/lobo.png")
            if tempo_passado % 2 == 0:
                self.image = pygame.image.load("imagens/lobo2.png")


            self.rect.x += self.velocidade
            if self.rect.left > largura:
                self.rect.right = 0
            if self.rect.right < 0:
                self.rect.left = largura

    class Tronco(pygame.sprite.Sprite):
        def __init__(self, x, y, velocidade, tamanho):
            super().__init__()
            #tronco tamanho 3 
            if tamanho == tamanho_tronco[3]:
                self.image = pygame.image.load("imagens/tronco3.png").convert_alpha()
            #tronco tamanho 7
            elif tamanho == tamanho_tronco[2]:
                self.image = pygame.image.load("imagens/tronco7.png").convert_alpha()
            #tronco tamanho 4
            elif tamanho == tamanho_tronco[1]:
                self.image = pygame.image.load("imagens/tronco4.png").convert_alpha()
            else:
                self.image = pygame.image.load("imagens/tronco5.png").convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.x = x * largura_bloco
            self.rect.y = y * altura_bloco
            self.velocidade = velocidade

        def update(self):
            self.rect.x += self.velocidade
            if self.rect.left > largura:
                self.rect.right = 0
            if self.rect.right < 0:
                self.rect.left = largura

                

    class Jacare(pygame.sprite.Sprite):
        def __init__(self, x, y, velocidade, jacare_afunda):
            super().__init__()
            if y == altura_rio[1] +1:
                self.image = pygame.image.load("imagens/jacare_base3.png")
            else:
                self.image = pygame.image.load("imagens/jacare_base2.png")
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect.x = x * largura_bloco
            self.rect.y = y * altura_bloco
            self.velocidade = velocidade
            self.ticks = 0  
            self.cor_atual = VERDE
            self.afunda = jacare_afunda

        def update(self):
            self.rect.x += self.velocidade
            if self.rect.left > largura:
                self.rect.right = 0
            if self.rect.right < 0:
                self.rect.left = largura

            self.ticks += 1
            if self.ticks >= 60 and self.afunda == True:

                if self.cor_atual == VERDE_CLARO:
                    if self.rect.y == (altura_rio[1]+ 1)*altura_bloco:
                        self.cor_atual = self.image = pygame.image.load("imagens/jacare_base3.png")
                    else:
                        self.cor_atual = self.image = pygame.image.load("imagens/jacare_base2.png")
                else:
                    if self.rect.y == (altura_rio[1]+1)*altura_bloco:
                        self.image = pygame.image.load("imagens/Jacare_atacando3.png")
                    else:
                        self.image = self.image = pygame.image.load("imagens/Jacare_atacando2.png")    
                    self.cor_atual = VERDE_CLARO
                self.ticks = 0

    # Inicialização do Pygame
    pygame.init()
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Foxxer")

    # Grupo de sprites
    sprites = pygame.sprite.Group()



    # Criação dos carros
    carros = pygame.sprite.Group()
    y_carros = range(num_blocos_y // 2, num_blocos_y - 2)

    for i in y_carros:
        x = random.randint(0, num_blocos_x - 1)
        y = i + 1
        velocidade = largura_bloco // 12
        #caminhão (1)
        if i == y_carros[0]:
            for x in range(0,15,6):
                carro = Carro(x, y, -velocidade, 2,1)
                sprites.add(carro)
                carros.add(carro)

        #moto (2)
        elif i == y_carros[1]:
            for x in range(0,6,3):
                carro = Carro(x, y, velocidade*3, 1,2)
                sprites.add(carro)
                carros.add(carro)
        
        #sedan (3)
        elif i == y_carros[2]:
            for x in range(0,15,5):
                carro = Carro(x,y,-velocidade,1 ,3)
                sprites.add(carro)
                carros.add(carro)

        #camionete (4)
        elif i == y_carros[3]:
            for x in range(0,15,6):
                carro = Carro(x,y,velocidade,1,  4)
                sprites.add(carro)
                carros.add(carro)

        #fusca (5)
        elif i == y_carros[4]:
            for x in range(0,15,5):
                carro = Carro(x,y,-velocidade,1 ,5)
                sprites.add(carro)
                carros.add(carro)

    altura_rio = range(num_blocos_y//2-1)

    # Criação dos troncos
    troncos = pygame.sprite.Group()
    y_troncos = [altura_rio[0],altura_rio[2],altura_rio[3],altura_rio[4]]
    tamanho_tronco = [5,4,7,3]
    for i in y_troncos:
        y = i + 1
        velocidade =  largura_bloco // 12
        #primeira fileira de troncos
        if i == y_troncos[3]:
            for x in range(0,13,6):
                tronco = Tronco(x, y, velocidade/4,tamanho_tronco[3])
                sprites.add(tronco)
                troncos.add(tronco)

        #segunda fileira de troncos
        elif i == y_troncos[2]:
            for x in range(0,12,10):
                tronco = Tronco(x, y, velocidade/1,tamanho_tronco[2])
                sprites.add(tronco)
                troncos.add(tronco)

        #terceira fileira de troncos
        elif i == y_troncos[1]:
            for x in range(0,10,9):
                tronco = Tronco(x, y, -velocidade/5,tamanho_tronco[1])
                sprites.add(tronco)
                troncos.add(tronco)
            #terceira fileira de troncos
        else:
            for x in range(0,18,9):
                tronco = Tronco(x, y, velocidade/1.3,tamanho_tronco[0])
                sprites.add(tronco)
                troncos.add(tronco)


    #Criação dos  jacares
    jacares = pygame.sprite.Group()
    y_jacares = [altura_rio[1],altura_rio[5]]
    for i in y_jacares:
        y = i + 1
        velocidade =  -largura_bloco // 20
        if i == y_jacares[1]:
            sorteia = [0,5,10]
            escolhido = random.choice(sorteia) 
            for x in range(0,11, 5):
                jacare_afunda = False
                if x == escolhido:
                    jacare_afunda = True
                jacare = Jacare(x, y, velocidade,jacare_afunda)
                sprites.add(jacare)
                jacares.add(jacare)
        else:
            sorteia = [0,4,8,12]
            escolhido = random.choice(sorteia) 
            for x in range(0,16, 4):
                jacare_afunda = False
                if x == escolhido:
                    jacare_afunda = True
                jacare = Jacare(x, y, velocidade,jacare_afunda)
                sprites.add(jacare)
                jacares.add(jacare)
        

    # Criação do jogador
    jogador = Player(num_blocos_x // 2, num_blocos_y-10)  # Posição inicial do jogador (centro da linha inferior)
    sprites.add(jogador)

    # Fonte para exibir a pontuação
    fonte = pygame.font.SysFont(None, 36)

    # Variáveis de pontuação e reinício
    pontuacao = 0
    pontuacao_para_ganhar = 5
    #vidas 
    vidas = 4

    lobos = pygame.sprite.Group()
    if pontuacao == 3:
        x = largura +largura_bloco
        y = num_blocos_y // 2 
        velocidade = -largura_bloco // 25
        lobo = Lobo(x, y, velocidade)
        sprites.add(lobo)
        lobos.add(lobo)

    # Loop principal
    rodando = True
    clock = pygame.time.Clock()

    #variavel para nao permitir que o jogador se mova segurando a tecla
    tecla_solta = True

    em_cima_jacare_verde_claro = False

    #cria uma variavel para o jogo nao gerar um lobo multiplas vezes 
    um_lobo = True



    while rodando:
        tempo_passado = int(pygame.time.get_ticks()/1000)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            elif event.type == pygame.KEYUP:  # Evento de tecla solta
                tecla_solta = True
                if event.key == pygame.K_ESCAPE:  # Verifica se a tecla Esc foi pressionada
                    rodando = False
        
        #gera o lobo
        if pontuacao == 3 and um_lobo:
            x = largura +largura_bloco
            y = num_blocos_y // 2 
            velocidade = -largura_bloco // 25 
            lobo = Lobo(x, y, velocidade)
            sprites.add(lobo)
            lobos.add(lobo) 
            um_lobo = False

        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0
        if keys[pygame.K_a]:
            dx = -largura_bloco
        elif keys[pygame.K_d]:
            dx = largura_bloco  
        elif keys[pygame.K_w]:
            dy = -altura_bloco
        elif keys[pygame.K_s]:
            dy = altura_bloco

        if dx != 0 or dy != 0:
            if tecla_solta:  # Move o jogador apenas se a tecla estiver solta
                jogador.update(dx, dy)
                tecla_solta = False  # Define a variável de controle como False


        sprites.update()

        # Verifica colisões
        if pygame.sprite.spritecollide(jogador, carros, False, pygame.sprite.collide_mask):
            vidas -=1
            jogador.rect.x = largura // 2
            jogador.rect.y = altura - altura_bloco

        if pygame.sprite.spritecollide(jogador,lobos,False, pygame.sprite.collide_mask):
            vidas -=1
            jogador.rect.x = largura // 2
            jogador.rect.y = altura - altura_bloco

        # Verifica se o jogador atingiu o topo
        if jogador.rect.y < altura_bloco:
            jogador.rect.y = num_blocos_y - 1
            if jogador.rect.y == num_blocos_y - 1:
                pontuacao += 1
                jogador.rect.x = largura // 2
                jogador.rect.y = altura - altura_bloco

        # Verifica se o jogador está colidindo com algum tronco/jacare
        troncos_colididos = pygame.sprite.spritecollide(jogador, troncos, False, pygame.sprite.collide_mask)
        if troncos_colididos:
            jogador.rect.x += troncos_colididos[0].velocidade
        
        
        jacares_colididos = pygame.sprite.spritecollide(jogador, jacares, False)
        if jacares_colididos:
            jogador.rect.x += jacares_colididos[0].velocidade
            if jacares_colididos[0].cor_atual == VERDE_CLARO:
                em_cima_jacare_verde_claro = True
            else:
                em_cima_jacare_verde_claro = False

        if not jacares_colididos and not troncos_colididos:
        # Verifica se o jogador encostou na região azul
            if jogador.rect.colliderect(pygame.Rect(0, altura_bloco, largura, (num_blocos_y // 2 - 1) * altura_bloco)):
                vidas -=1
                jogador.rect.x = largura // 2
                jogador.rect.y = altura - altura_bloco

        if em_cima_jacare_verde_claro:
            vidas -=1
            jogador.rect.x = largura // 2
            jogador.rect.y = altura - altura_bloco
            em_cima_jacare_verde_claro = False

        # Renderização do jogo
        tela.fill(BRANCO)
            
        # Preenchendo a área dos troncos com azul
        pygame.draw.rect(tela, (0, 0, 255), pygame.Rect(0, altura_bloco, largura, (num_blocos_y // 2 - 1) * altura_bloco))

        # Preenchendo a área por onde passam os carros com a cor preta
        pygame.draw.rect(tela, PRETO, pygame.Rect(0, (num_blocos_y // 2 + 1) * altura_bloco, largura, (num_blocos_y - 9) * altura_bloco))

        tela.blit(imagem_fundo,(0,0))
        # Desenha os sprites 
        sprites.draw(tela)

        # Exibe a pontuação na tela
        texto_pontuacao = fonte.render("Pontuação: {}".format(pontuacao), True, LARANJA)
        tela.blit(texto_pontuacao, (10, 10))

        texto_pontuacao = fonte.render("Vidas: {}".format(vidas), True, VERMELHO)
        tela.blit(texto_pontuacao, (largura-100, 10))

        texto_tempo = fonte.render("Tempo: {} segundos".format(tempo_passado),True, PRETO)
        tela.blit(texto_tempo,(0,660))

        
        pygame.display.flip()

        ticks_jogo = 30 + pontuacao*5
        clock.tick(ticks_jogo)  # Ajuste a velocidade do jogo aqui

        #exibe tempo na tela


        # Verifica se o jogador ganhou o jogo
        if pontuacao >= pontuacao_para_ganhar:
            rodando = False

        if vidas == 0:
            rodando = False

    # Mensagem de vitória ou derrota
    if pontuacao >= pontuacao_para_ganhar:
        print("Você ganhou!")
    else:
        print("Você perdeu!")

    # Finalização do Pygame
    pygame.quit()
  

tela_inicio()
