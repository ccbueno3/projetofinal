import pygame
import random

# Cores
BRANCO = (255, 255, 255)
LARANJA = (255, 165, 0)
PRETO = (0, 0, 0)
MARROM = (150, 75, 0)
VERDE = (39,71,57)

# Dimensões da janela do jogo
largura = 750
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
        self.image = pygame.Surface((largura_bloco, altura_bloco))
        self.image.fill(LARANJA)
        self.rect = self.image.get_rect()
        self.rect.x = x * largura_bloco
        self.rect.y = y * altura_bloco

    def update(self, dx=0, dy=0):
        if 0 <= self.rect.x + dx < largura - largura_bloco and dx != 0:
            self.rect.x += dx
        if 0 <= self.rect.y + dy < altura - altura_bloco and dy != 0:
            self.rect.y += dy

# Classe para representar os carros
class Carro(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidade):
        super().__init__()
        self.image = pygame.Surface((largura_bloco, altura_bloco))
        self.image.fill(PRETO)
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

class Tronco(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidade):
        super().__init__()
        self.image = pygame.Surface((largura_bloco*3, altura_bloco))
        self.image.fill(MARROM)
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
    def __init__(self, x, y, velocidade):
        super().__init__()
        if y == altura_rio[1] +1:
            self.image = pygame.Surface((largura_bloco*2, altura_bloco))
        else:
            self.image = pygame.Surface((largura_bloco*3, altura_bloco))
        self.image.fill(VERDE)
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

# Inicialização do Pygame
pygame.init()
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Foxxer")

# Grupo de sprites
sprites = pygame.sprite.Group()



# Criação dos carros
carros = pygame.sprite.Group()
for i in range(num_blocos_y // 2, num_blocos_y - 2):
    x = random.randint(0, num_blocos_x - 1)
    y = i + 1
    velocidade = random.choice([-1, 1]) * largura_bloco // 4
    carro = Carro(x, y, velocidade)
    sprites.add(carro)
    carros.add(carro)

altura_rio = range(num_blocos_y//2-1)

# Criação dos troncos
troncos = pygame.sprite.Group()
y_troncos = [altura_rio[0],altura_rio[2],altura_rio[3],altura_rio[4]]

for i in y_troncos:
    x_values = random.sample(range(0, num_blocos_x - 8),1)  # Amostra aleatória de 3 valores únicos
    y = i + 1
    velocidade = random.choice([-1, 1] ) * largura_bloco // 4
    for x in x_values:
        tronco = Tronco(x, y, velocidade)
        sprites.add(tronco)
        troncos.add(tronco)

#Criação dos  jacares
jacares = pygame.sprite.Group()
y_jacares = [altura_rio[1],altura_rio[5]]
for i in y_jacares:
    y = i + 1
    velocidade =  -largura_bloco // 4
    if i == y_jacares[1]:
        for x in range(0,11, 5):
            jacare = Jacare(x, y, velocidade)
            sprites.add(jacare)
            jacares.add(jacare)
    else:
        for x in range(0,13, 3):
            jacare = Jacare(x, y, velocidade)
            sprites.add(jacare)
            jacares.add(jacare)
    

# Criação do jogador
jogador = Player(num_blocos_x // 2, num_blocos_y - 1)  # Posição inicial do jogador (centro da linha inferior)
sprites.add(jogador)

# Fonte para exibir a pontuação
fonte = pygame.font.SysFont(None, 36)

# Variáveis de pontuação e reinício
pontuacao = 0
pontuacao_para_ganhar = 10

# Loop principal
rodando = True
clock = pygame.time.Clock()

while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    keys = pygame.key.get_pressed()
    dx = 0
    dy = 0
    if keys[pygame.K_LEFT]:
        dx = -largura_bloco
    elif keys[pygame.K_RIGHT]:
        dx = largura_bloco
    elif keys[pygame.K_UP]:
        dy = -altura_bloco
    elif keys[pygame.K_DOWN]:
        dy = altura_bloco

    jogador.update(dx, dy)

    sprites.update()

    # Verifica colisões
    if pygame.sprite.spritecollide(jogador, carros, False):
        rodando = False

    # Verifica se o jogador atingiu o topo
    if jogador.rect.y < altura_bloco:
        jogador.rect.y = num_blocos_y - 1
        if jogador.rect.y == num_blocos_y - 1:
            pontuacao += 1
            jogador.rect.x = largura // 2
            jogador.rect.y = altura - altura_bloco

    # Verifica se o jogador está colidindo com algum tronco/jacare
    troncos_colididos = pygame.sprite.spritecollide(jogador, troncos, False)
    if troncos_colididos:
        jogador.rect.x += troncos_colididos[0].velocidade
    
    jacares_colididos = pygame.sprite.spritecollide(jogador, jacares, False)
    if jacares_colididos:
        jogador.rect.x += jacares_colididos[0].velocidade

    if not jacares_colididos and not troncos_colididos:
    # Verifica se o jogador encostou na região azul
        if jogador.rect.colliderect(pygame.Rect(0, altura_bloco, largura, (num_blocos_y // 2 - 1) * altura_bloco)):
            rodando = False



    # Renderização do jogo
    tela.fill(BRANCO)
        
    # Preenchendo a área dos troncos com azul
    pygame.draw.rect(tela, (0, 0, 255), pygame.Rect(0, altura_bloco, largura, (num_blocos_y // 2 - 1) * altura_bloco))

    # Desenha os sprites 
    sprites.draw(tela)

    # Exibe a pontuação na tela
    texto_pontuacao = fonte.render("Pontuação: {}".format(pontuacao), True, PRETO)
    tela.blit(texto_pontuacao, (10, 10))

    pygame.display.flip()

    clock.tick(10)  # Ajuste a velocidade do jogo aqui

    # Verifica se o jogador ganhou o jogo
    if pontuacao >= pontuacao_para_ganhar:
        rodando = False

# Mensagem de vitória ou derrota
if pontuacao >= pontuacao_para_ganhar:
    print("Você ganhou!")
else:
    print("Você perdeu!")

# Finalização do Pygame
pygame.quit()
