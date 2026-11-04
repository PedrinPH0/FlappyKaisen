import pygame
import random

#Variaveis do Jogo
largura = 360
altura = 640
rodando = True
relogio = pygame.time.Clock()


#Classe Itadori
itadori_x = largura/8
itadori_y = altura/2
itadori_largura = 32
itadori_altura = 48

class Itadori(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self, itadori_x, itadori_y, itadori_largura, itadori_altura)
        self.img = img

#Classe do Cano
cano_x = largura
cano_y = 0
cano_largura = 64
cano_altura = 512

class Cano(pygame.Rect):
    def __init__(self,img): 
        pygame.Rect.__init__(self, cano_x, cano_y, cano_largura, cano_altura)
        self.img = img
        self.passed = False


#Imagens
fukuma = pygame.image.load('fukuma.jpg')
fukuma = pygame.transform.scale(fukuma, (360, 640))
itadori = pygame.image.load('itadori_normal3.png')
itadori = pygame.transform.scale(itadori, (itadori_largura, itadori_altura))
itadori_pulando = pygame.image.load('itadori_pulando2.png')
itadori_pulando = pygame.transform.scale(itadori_pulando, (itadori_largura, itadori_altura))
cano_inferior_imagem = pygame.image.load('cano_inferior.png')
cano_inferior_imagem = pygame.transform.scale(cano_inferior_imagem, (cano_largura, cano_altura))
cano_superior_imagem = pygame.image.load('cano_superior.png')
cano_superior_imagem = pygame.transform.scale(cano_superior_imagem, (cano_largura, cano_altura))

#Logica Gamer
itadori = Itadori(itadori)
itadori_pulando = Itadori(itadori_pulando)
canos = []
velocidade_x = -2
velocidade_y = 0
gravidade = 0.4
pontuacao = 0
game_over = False

def criar_canos():
    aleatorio_cano_y = cano_y - cano_altura/4 - random.random()*(cano_altura/2)


    espaço_safe = altura/4

    cano_superior = Cano(cano_superior_imagem)
    cano_superior.y = aleatorio_cano_y
    canos.append(cano_superior)

    cano_inferior = Cano(cano_inferior_imagem)
    cano_inferior.y = cano_superior.y + cano_altura + espaço_safe
    canos.append(cano_inferior)

    print(len(canos))

def movimento():
    global velocidade_y, pontuacao, game_over
    velocidade_y += gravidade
    itadori.y += velocidade_y
    itadori.y = max(itadori.y, 0)

    if itadori.y > altura:
        game_over = True
        pygame.mixer.music.stop()
        specialz.play()
        return


    for cano in canos:
        cano.x += velocidade_x

        if not cano.passed and itadori.x > cano.x + cano_largura:
            pontuacao += 0.5
            cano.passed = True

        if itadori.colliderect(cano):
            game_over = True
            pygame.mixer.music.stop()
            specialz.play()
            return

    while len(canos) > 0 and canos[0].x + cano_largura < 0:
        canos.pop(0)


def desenhar():
    tela.blit(fukuma, (0,0))
    tela.blit(itadori.img, itadori)

    for cano in canos:
        tela.blit(cano.img, cano)

    texto_str = str(int(pontuacao))
    if game_over:
        texto_str = 'Game Over: ' + texto_str

    texto_font = pygame.font.SysFont('Jujutsu Kaisen.ttf', 45)
    font = pygame.font.Font('fontes/jjk.ttf', 45)
    texto_render = font.render(texto_str, True, 'white')
    tela.blit(texto_render, (5, 0))

def acao(event):
    global pular
    if event.type == pygame.KEYDOWN:
        pular = False
        if event.key == pygame.K_SPACE:
            pular = True

pygame.init()
pygame.mixer.init()

criador_canos = pygame.USEREVENT + 0
pygame.time.set_timer(criador_canos, 1500)

#Musicas
pygame.mixer.music.load('kakai.mp3')
pygame.mixer.music.play(-1)
specialz = pygame.mixer.Sound('specialz.mp3')
opening2 = pygame.mixer.Sound('opening2.mp3')

tela = pygame.display.set_mode((largura, altura))

pygame.display.set_caption('Flappy Kaisen')

while rodando: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        
        if event.type == criador_canos and not game_over:
            criar_canos()

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_UP):
                velocidade_y = -6

                if game_over:
                    itadori.y = itadori_y
                    canos.clear()
                    pontuacao = 0
                    game_over = False
                    specialz.stop()
                    pygame.mixer.music.play(-1)


              
                    

    if not game_over:
        movimento()
        desenhar()

        
        pygame.display.update()
        relogio.tick(60)

