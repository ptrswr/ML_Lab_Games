import pygame
import math
import sys
from datetime import datetime

# Inicjalizacja Pygame
pygame.init()

# Ustawienia ekranu
WIDTH, HEIGHT = 1000, 800
CENTER = (WIDTH / 2, HEIGHT / 2)
RADIUS = 300

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Analog Clock")
clock = pygame.time.Clock()

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


# Funkcja zamieniająca współrzędne biegunowe na kartezjańskie
def polar_to_cartesian_coordinates(r, theta, center=CENTER):
    theta_rad = math.radians(theta)
    x = r * math.cos(theta_rad) + center[0]
    y = r * math.sin(theta_rad) + center[1]
    return x, y


# Funkcja rysująca tekst na ekranie
def draw_text(text, size, position, font_name="Arial"):
    font = pygame.font.SysFont(font_name, size, True, False)
    text = font.render(text, True, WHITE)
    text_rect = text.get_rect(center=position)
    screen.blit(text, text_rect)


# Funkcja rysująca wskazówki zegara
def draw_clock_hand(angle, length, color, width):
    end_pos = polar_to_cartesian_coordinates(length, angle)
    pygame.draw.line(screen, color, CENTER, end_pos, width)


# Funkcja rysująca cyfry na tarczy zegara
def draw_clock_numbers():
    for i in range(1, 13):
        angle = i * 30 - 90
        pos = polar_to_cartesian_coordinates(RADIUS - 60, angle)
        draw_text(str(i), 60, pos, "Comic Sans MS")


# Funkcja rysująca kreski godzinowe i minutowe
def draw_ticks():
    for i in range(60):
        angle = i * 6 - 90
        if i % 5 == 0:
            # Kreski godzinowe
            start_pos = polar_to_cartesian_coordinates(RADIUS - 20, angle)
            end_pos = polar_to_cartesian_coordinates(RADIUS - 5, angle)
            pygame.draw.line(screen, WHITE, start_pos, end_pos, 8)
        else:
            # Kreski minutowe
            start_pos = polar_to_cartesian_coordinates(RADIUS - 15, angle)
            end_pos = polar_to_cartesian_coordinates(RADIUS - 5, angle)
            pygame.draw.line(screen, WHITE, start_pos, end_pos, 5)


# Funkcja rysująca datę i czas cyfrowy
def draw_digital_time(now):
    date_str = now.strftime("%A, %d %B %Y")
    time_str = now.strftime("%H:%M:%S")

    date_pos = (WIDTH / 2, HEIGHT - 50)
    draw_text(f"{date_str} | {time_str}", 30, date_pos, "Courier New")


def draw_clock(now):
    # Kolor ekranu
    screen.fill(BLACK)
    # Rysowanie tarczy zegara
    pygame.draw.circle(screen, WHITE, CENTER, RADIUS, 8)
    # Rysowanie cyfr na tarczy zegara
    draw_clock_numbers()
    # Rysowanie kresek minutowych i godzinowych
    draw_ticks()
    # Rysowanie wskazówek zegara
    draw_hands(now)
    # Rysowanie czasu cyfrowego
    draw_digital_time(now)


def draw_hands(now):
    hour = now.hour % 12
    minute = now.minute
    second = now.second
    # Obliczanie kątów wskazówek
    hour_angle = (hour * 30 + (minute / 2)) - 90
    minute_angle = (minute * 6) - 90
    second_angle = (second * 6) - 90

    # Rysowanie wskazówek
    draw_clock_hand(hour_angle, 140, WHITE, 12)  # wskazówka godzinowa
    draw_clock_hand(minute_angle, 200, WHITE, 7)  # wskazówka minutowa
    draw_clock_hand(second_angle, 230, RED, 4)  # wskazówka sekundowa


# Główna pętla programu
def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Pobieranie aktualnego czasu
        now = datetime.now()

        # Rysowanie layoutu zegara
        draw_clock(now)

        # Odświeżanie ekranu
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
