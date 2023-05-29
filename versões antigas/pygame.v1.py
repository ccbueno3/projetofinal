import pygame
import random

# Cores
BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)
PRETO = (0, 0, 0)

# Dimensões da janela do jogo
largura = 800
altura = 600

# Dimensões do grid
largura_bloco = 50
altura_bloco = 50
num_blocos_x = largura // largura_bloco
num_blocos_y = altura // altura_bloco

# Classe para representar o jogador
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):   
        super().__init__()
        self.image = pygame.Surface((largura_bloco, altura_bloco))
        self.image.fill(VERDE)
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



# Inicialização do Pygame
pygame.init()
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Frogger")

# Grupo de sprites
sprites = pygame.sprite.Group()

# Criação do jogador
jogador = Player(num_blocos_x // 2, num_blocos_y - 1)  # Posição inicial do jogador (centro da linha inferior)
sprites.add(jogador)

# Criação dos carros
carros = pygame.sprite.Group()
for i in range(num_blocos_y - 2):
    x = random.randint(0, num_blocos_x - 1)
    y = i + 1
    velocidade = random.choice([-1, 1]) * largura_bloco // 4
    carro = Carro(x, y, velocidade)
    sprites.add(carro)
    carros.add(carro)

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
          
            

    # Renderização do jogo
    tela.fill(BRANCO)
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
