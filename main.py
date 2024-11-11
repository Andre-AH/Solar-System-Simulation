import pygame
import math

pygame.init()


WIDTH, HEIGHT = 1420, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sistema Solar")
FONTE = pygame.font.SysFont("comicsans", 16)
FONTE2 = pygame.font.SysFont("comicsans", 40)


class Planeta:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    ESCALA = 220 / AU
    TIMESTEP = 3600*24  # 1 DIA

    def __init__(self, x, y, raio, cor, massa):
        self.x = x
        self.y = y
        self.raio = raio
        self.cor = cor
        self.massa = massa

        self.orbita = []
        self.sol = False
        self.distancia_sol = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win, fator):
        x = self.x * self.ESCALA * fator + WIDTH / 2
        y = self.y * self.ESCALA * fator + HEIGHT / 2

        if len(self.orbita) > 2:
            Lpontos = []
            for ponto in self.orbita:
                x, y = ponto
                x = x * self.ESCALA * fator + WIDTH / 2
                y = y * self.ESCALA * fator + HEIGHT / 2
                Lpontos.append((x, y))
            pygame.draw.lines(win, self.cor, False, Lpontos, 1)

        pygame.draw.circle(win, self.cor, (x, y), self.raio * fator)

        if not self.sol:
            distancia_texto = FONTE.render(
                f"{round((self.distancia_sol/1000)*6.68459e-9, 4) } UA", 1, (255, 255, 255))
            win.blit(distancia_texto, (x-distancia_texto.get_width() /
                     2, y-distancia_texto.get_height()/2))

    def atracao(self, other, k):
        other_x, other_y = other.x, other.y
        distancia_x = other_x - self.x
        distancia_y = other_y - self.y
        distancia = math.sqrt(distancia_x ** 2 + distancia_y ** 2)

        if other.sol:
            self.distancia_sol = distancia

        forca = k * self.G * self.massa * other.massa / distancia**2
        teta = math.atan2(distancia_y, distancia_x)
        forca_x = math.cos(teta) * forca
        forca_y = math.sin(teta) * forca
        return forca_x, forca_y

    def atualizar_posicao(self, planetas, gravidade, k):
        total_fx = total_fy = 0
        for planeta in planetas:
            if self == planeta:
                continue
            if gravidade:
                fx, fy = self.atracao(planeta, k)
                total_fx += fx
                total_fy += fy
            else:
                total_fx = 0
                total_fy = 0

        self.x_vel += total_fx / self.massa * self.TIMESTEP
        self.y_vel += total_fy / self.massa * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbita.append((self.x, self.y))


def main():
    run = True
    gravidade = True
    clock = pygame.time.Clock()

    fator = 1

    sol = Planeta(0, 0, 70, (255, 255, 100), 1.98892 * 10**30)
    sol.sol = True

    terra = Planeta(-1*Planeta.AU, 0, 16, (0, 150, 255), 5.9742 * 10**24)
    terra.y_vel = 29.783*1000

    marte = Planeta(-1.524*Planeta.AU, 0, 8.5, (220, 50, 0), 6.39 * 10**23)
    marte.y_vel = 24.077*1000

    mercurio = Planeta(0.387*Planeta.AU, 0, 6.4, (100, 90, 70), 3.3 * 10**23)
    mercurio.y_vel = -47.4*1000

    venus = Planeta(0.723*Planeta.AU, 0, 15.2,
                    (255, 250, 200), 4.8685 * 10**24)
    venus.y_vel = -35.02*1000

    jupiter = Planeta(5.2*Planeta.AU, 0, 50, (255, 151, 41),
                      317.8 * 5.9742 * 10**24)
    jupiter.y_vel = -13074.737

    saturno = Planeta(9.57*Planeta.AU, 0, 42,
                      (255, 250, 100), 317.8 * 5.9742 * 10**24)
    saturno.y_vel = -9679.475

    urano = Planeta(19.17*Planeta.AU, 0, 20,
                    (211, 249, 250), 317.8 * 5.9742 * 10**24)
    urano.y_vel = -6790.524

    neptuno = Planeta(30.18*Planeta.AU, 0, 19,
                      (72, 120, 254), 317.8 * 5.9742 * 10**24)
    neptuno.y_vel = -5420.506

    LPlanetas = [sol, mercurio, venus, terra,
                 marte, jupiter, saturno, urano, neptuno]

    data = 0
    n = 1
    k = 1
    while run:

        clock.tick(15*n)
        data += 1
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if gravidade == True:
                        gravidade = False
                    else:
                        gravidade = True

                if event.key == pygame.K_RIGHT:
                    n += 1
                if event.key == pygame.K_LEFT:
                    n -= 1
                if event.key == pygame.K_UP:
                    k += 0.1
                if event.key == pygame.K_DOWN:
                    k -= 0.1
                if event.key == pygame.K_a:
                    fator += 0.1
                if event.key == pygame.K_s:
                    fator -= 0.1

        for planeta in LPlanetas:
            planeta.atualizar_posicao(LPlanetas, gravidade, k)
            planeta.draw(WIN, fator)
            data_texto = FONTE2.render(f"Dia {data}", 1, (255, 255, 255))
            WIN.blit(data_texto, (50, 50))
            info_texto = FONTE2.render(
                "'ESPAÇO' -> Gravidade ON/OFF", 1, (255, 255, 255))
            WIN.blit(info_texto, (950, 50))
            velocidade_texto = FONTE2.render(
                f"Velocidade {n}X ", 1, (255, 255, 255))
            WIN.blit(velocidade_texto, (1050, 100))
            gravidade_texto = FONTE2.render(
                f"Gravidade {round(k, 1)}X ", 1, (255, 255, 255))
            WIN.blit(gravidade_texto, (1050, 150))
            zoom_texto = FONTE2.render(
                f"Zoom {round(fator, 1)}X ", 1, (255, 255, 255))
            WIN.blit(zoom_texto, (1050, 200))

        pygame.display.update()
    pygame.quit()


main()
