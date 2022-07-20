import pygame
from random import randint, random

pygame.init()  # 초기화

# 화면 크기 설정
screen_width = 1080
screen_height = 720

screen = pygame.display.set_mode((screen_width, screen_height))

# 게임 이름 설정
pygame.display.set_caption('아케이드 게임')

# FPS
clock = pygame.time.Clock()

# 배경 이미지 불러오기
background = pygame.image.load("background.png")

# 캐릭터 불러오기
character = pygame.image.load("character.png")
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = screen_width / 2 - character_width / 2
character_y_pos = screen_height / 2 - character_height / 2

# 캐릭터 움직일 좌표
character_to_x_LEFT = 0
character_to_x_RIGHT = 0
character_to_y_DOWN = 0
character_to_y_UP = 0

# 캐릭터 이동속도
character_speed = 0.3

# 적 불러오기
enemy_image = pygame.image.load("enemy.png")
enemy_size = enemy_image.get_rect().size
enemy_width = enemy_size[0]
enemy_height = enemy_size[1]
no_enemy_zone = 250  # 화면 중앙 300 * 300 범위에 적이 스폰되지 않음
num_enemy = 150

# 레벨 초기화
level = 1
level_up = False # 레벨업 했는지 안 했는지 판별

# 적 초기화
enemies = []
for num in range(num_enemy):
    # 적 초기 위치
    enemy_pos_x_init = randint(0, screen_width)  # 적 초기 생성 x 좌표
    if (screen_width / 2 - no_enemy_zone / 2) <= enemy_pos_x_init <= (screen_width / 2 + no_enemy_zone / 2):
        enemy_pos_y_init = (randint(0, screen_height / 2 - no_enemy_zone / 2) +
                            randint(0, 1) * (screen_height / 2 + no_enemy_zone / 2))
    else:
        enemy_pos_y_init = randint(0, screen_height)

# 적 초기 위치에 따른 이동 방향, 속도
    if 0 <= enemy_pos_x_init < (screen_width / 2):
        enemy_to_x = random()
    elif (screen_width / 2) <= enemy_pos_x_init <= screen_width:
        enemy_to_x = -random()

    if 0 <= enemy_pos_y_init < (screen_height / 2):
        enemy_to_y = random()
    elif (screen_height / 2) <= enemy_pos_y_init <= screen_height:
        enemy_to_y = -random()

    enemies.append({
        'pos_x': enemy_pos_x_init,  # 적들의 x 좌표
        'pos_y': enemy_pos_y_init,  # 적들의 y 좌표
        'to_x': enemy_to_x,  # 적들의 x 속도
        'to_y': enemy_to_y  # 적들의 y 속도
    })

# 폰트 정의
game_font = pygame.font.Font(None, 40)

# 시작 시간 정보
start_ticks = pygame.time.get_ticks()  # 시작 시간

running = True
while running:
    dt = clock.tick(60)
    level_accel = 1.3 # 레벨에 따라 적들 속도 배

    # 이벤트 처리 (키보드, 마우스 등 입력에 대한)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x_LEFT -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x_RIGHT += character_speed
            elif event.key == pygame.K_UP:
                character_to_y_UP -= character_speed
            elif event.key == pygame.K_DOWN:
                character_to_y_DOWN += character_speed

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                character_to_x_LEFT = 0
            elif event.key == pygame.K_RIGHT:
                character_to_x_RIGHT = 0
            elif event.key == pygame.K_UP:
                character_to_y_UP = 0
            elif event.key == pygame.K_DOWN:
                character_to_y_DOWN = 0

    # 캐릭터, 적 좌표 업데이트
    character_x_pos += dt * (character_to_x_RIGHT + character_to_x_LEFT)
    character_y_pos += dt * (character_to_y_UP + character_to_y_DOWN)

    # 캐릭터 경계값 처리
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    if character_y_pos < 0:
        character_y_pos = 0
    elif character_y_pos > screen_height - character_height:
        character_y_pos = screen_height - character_height

    for enemy_idx, enemy_val in enumerate(enemies):
        enemy_x_pos = enemy_val['pos_x']
        enemy_y_pos = enemy_val['pos_y']

        if level_up:
            enemy_val['to_x'] *= level_accel
            enemy_val['to_y'] *= level_accel

        # 적이 배경 밖으로 이동하면 없앰
        if enemy_x_pos < -enemy_width:
            pass
        elif enemy_x_pos > screen_width:
            pass

        if enemy_y_pos < -enemy_height:
            pass
        elif enemy_y_pos > screen_height:
            pass

        enemy_val['pos_x'] += enemy_val['to_x']
        enemy_val['pos_y'] += enemy_val['to_y']

    level_up = False

    # 캐릭터 rect 값 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    # 적 rect 값 업데이트
    for enemy_idx, enemy_val in enumerate(enemies):
        enemy_x_pos = enemy_val['pos_x']
        enemy_y_pos = enemy_val['pos_y']

        enemy_rect = enemy_image.get_rect()
        enemy_rect.left = enemy_x_pos
        enemy_rect.top = enemy_y_pos

        if character_rect.colliderect(enemy_rect):
            print("충돌했어요")
            running = False

    # 레벨 집어넣기
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000  # 경과된 시간(s)

    if elapsed_time / 10 > level:
        level += 1
        level_up = True

    level_print = game_font.render(f"{level} Level", True, (255, 255, 255))
    timer = game_font.render(str(int(elapsed_time)), True, (255, 255, 255))

    # 화면에 그리기
    screen.blit(background, (0, 0))
    screen.blit(character, (character_x_pos, character_y_pos))

    for enemy_idx, enemy_val in enumerate(enemies):
        enemy_x_pos = enemy_val['pos_x']
        enemy_y_pos = enemy_val['pos_y']
        screen.blit(enemy_image, (enemy_x_pos, enemy_y_pos))

    screen.blit(level_print, (30, 10))
    screen.blit(timer, (1040, 10))

    pygame.display.update()  # 게임 화면 업데이트

pygame.time.delay(2000)  # 2초 대기

pygame.quit()  # pygame 종료
