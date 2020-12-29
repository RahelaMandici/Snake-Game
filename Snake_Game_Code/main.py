import sys
import json
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

with open(sys.argv[1]) as f_in:
    data = json.load(f_in)

table_size = data["table_size"].copy()
obstacles = data["obstacles"].copy()
close_all = False


def verify_quit_game():
    global close_all
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close_all = True


def get_moving_direction(direction):
    snake_step = 10

    keys_input = pygame.key.get_pressed()
    if keys_input[pygame.K_LEFT]:
        if direction[0] != snake_step:
            direction[0] = -snake_step
            direction[1] = 0
    if keys_input[pygame.K_RIGHT]:
        if direction[0] != -snake_step:
            direction[0] = snake_step
            direction[1] = 0
    if keys_input[pygame.K_UP]:
        if direction[1] != snake_step:
            direction[1] = -snake_step
            direction[0] = 0
    if keys_input[pygame.K_DOWN]:
        if direction[1] != -snake_step:
            direction[1] = snake_step
            direction[0] = 0


def verify_snake_out_of_table(snake_head):
    if snake_head.x > table_size[0] - 10:
        snake_head.x = 0
        return True
    if snake_head.x < 0:
        snake_head.x = table_size[0] - 10
        return True
    if snake_head.y > table_size[1] - 10:
        snake_head.y = 0
        return True
    if snake_head.y < 0:
        snake_head.y = table_size[1] - 10
        return True
    return False


def main():
    global close_all, table_size, obstacles
    pygame.init()
    clock = pygame.time.Clock()

    close_all = False
    snake_box_size = 10
    obstacles_box_size = 10
    direction = [0, 0]

    screen = pygame.display.set_mode((table_size[0], table_size[1]))
    snake_head = pygame.Rect(50, 50, snake_box_size, snake_box_size)
    obstacles_rect = [pygame.Rect(obstacle[0], obstacle[1], obstacles_box_size, obstacles_box_size)
                      for obstacle in obstacles]

    while not close_all:
        verify_quit_game()
        screen.fill(BLACK)

        get_moving_direction(direction)

        snake_head.x += direction[0]
        snake_head.y += direction[1]

        verify_snake_out_of_table(snake_head)

        pygame.draw.rect(screen, WHITE, snake_head)

        for obstacle_rect in obstacles_rect:
            pygame.draw.rect(screen, RED, obstacle_rect)

        # verific daca se loveste de obstacole
        if len(snake_head.collidelistall(obstacles_rect)) > 0:
            break

        pygame.display.update()
        clock.tick(6)


main()
pygame.quit()
quit()
