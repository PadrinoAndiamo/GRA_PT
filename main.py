import pygame
from sys import exit

def display_score():
    if not collision:  # Aktualizuj wynik tylko jeśli nie doszło do kolizji
        current_time = int(pygame.time.get_ticks() / 1000) - start_time
        score_surf = test_font.render(f'Score: {current_time}', False, (64, 64, 64))
        score_rect = score_surf.get_rect(center=(400, 50))
        screen.blit(score_surf, score_rect)

# anime2 --> przeciwnik

# anime_heroe2 --> nasza postać

pygame.init()
screen = pygame.display.set_mode((700, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()  # "Clock"
test_font = pygame.font.Font('font/Font_2/04B_30__.TTF', 50)
game_active = True
start_time = 0
collision = False  # Dodana zmienna do śledzenia kolizji

sky_surf = pygame.image.load('graphic/sky_2.jpg').convert()  # ścieżkę do pliku obrazu z niebem
ground_surf = pygame.image.load('graphic/ground.jpg').convert()

score_surf = test_font.render('Jump', False, (0, 128, 0))  # Zmieniłem kolor napisu na ciemnozielony
score_rect = score_surf.get_rect(center=(400, 50))
anime_surf = pygame.image.load('graphic/pixel_anime2.png').convert_alpha() # anime przeciwnik
anime_rect = anime_surf.get_rect(bottomright=(620, 350))

player_surf = pygame.image.load('graphic/pixel_anime_hero2.jpg').convert_alpha() # nasza postać
player_rect = player_surf.get_rect(midbottom=(80, 370))
player_gravity = 0

# Prędkość przeciwnika
anime_speed = 5

# Czas do zwiększenia prędkości
speed_up_time = 5000  # Przykład: zwiększ prędkość co 5 sekund
speed_up_timer = 0

# intro screen
player_stand = pygame.image.load('graphic/pixel_anime_hero.jpg').convert_alpha()
player_stand_rect = player_stand.get_rect(center=(350, 250))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if not collision:  # Dodaj warunek, aby skok był możliwy tylko jeśli nie doszło do kolizji
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                        player_gravity = -20
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                        player_gravity = -20

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                anime_rect.left = 700
                start_time = int(pygame.time.get_ticks() / 1000)
                collision = False  # Zresetuj zmienną kolizji po wznowieniu gry

    if game_active:
        screen.blit(sky_surf, (0, 0))  # pozycja tła
        screen.blit(ground_surf, (0, 350))  # pozycja ziemi

        # Aktualizuj prędkość przeciwnika co określony czas
        current_time = pygame.time.get_ticks()
        if current_time - speed_up_timer >= speed_up_time:
            anime_speed += 1
            speed_up_timer = current_time

        anime_rect.x -= anime_speed
        if anime_rect.right <= 0:
            anime_rect.left = 700
        screen.blit(anime_surf, anime_rect)

        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 370:
            player_rect.bottom = 370
            player_gravity = 0

        screen.blit(player_surf, player_rect)

        # Collision
        if anime_rect.colliderect(player_rect):
            game_active = False
            collision = True  # Ustaw zmienną kolizji na True

    else:
        screen.fill((1, 0, 0))  # Zmieniłem kolor tła na czarny
        screen.blit(player_stand, player_stand_rect)

    display_score()

    if player_rect.colliderect(anime_rect):
        print('collision')

    mouse_pos = pygame.mouse.get_pos()
    if player_rect.collidepoint(mouse_pos):
        print(pygame.mouse.get_pressed())

    pygame.display.update()
    clock.tick(60)
