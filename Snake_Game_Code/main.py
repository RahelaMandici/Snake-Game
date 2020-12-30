import sys
import json
import pygame
import random

WHITE = (255, 255, 255)
FUNDAL = (0, 0, 0)
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
    if snake_head.x > table_size[0] - snake_box_size:
        snake_head.x = 0
        return True
    if snake_head.x < 0:
        snake_head.x = table_size[0] - snake_box_size
        return True
    if snake_head.y > table_size[1] - snake_box_size:
        snake_head.y = 0
        return True
    if snake_head.y < 0:
        snake_head.y = table_size[1] - snake_box_size
        return True
    return False


def get_food():
    food_size = 10
    food_coord = [0, 0]
    food_coord[0] = int(random.randint(0, table_size[0] - snake_box_size) / 10) * 10
    food_coord[1] = int(random.randint(0, table_size[1] - snake_box_size) / 10) * 10
    food = pygame.Rect(food_coord[0], food_coord[1], food_size, food_size)
    return food


def main():
    global close_all, table_size, obstacles, snake_box_size
    pygame.init()
    pygame.display.set_caption('Snake Game')
    font = pygame.font.SysFont('Comic Sans MS', 30)
    clock = pygame.time.Clock()

    close_all = False
    snake_box_size = 10
    obstacles_box_size = 10
    direction = [0, 0]
    snake = list()
    no_food = True
    score = 0

    screen = pygame.display.set_mode((table_size[0], table_size[1] + 100))
    text_surface = font.render('Your Score: ' + str(score), False, WHITE)

    obstacles_rect = [pygame.Rect(obstacle[0], obstacle[1], obstacles_box_size, obstacles_box_size)
                      for obstacle in obstacles]

    snake.append(pygame.Rect(100, 100, snake_box_size, snake_box_size))

    while not close_all:
        verify_quit_game()
        screen.fill(FUNDAL)

        pygame.draw.line(screen, WHITE, (0, table_size[1]), (table_size[0], table_size[1]))
        screen.blit(text_surface, (table_size[0] / 2 - text_surface.get_width() / 2,
                                   table_size[1] + text_surface.get_height() / 2))

        get_moving_direction(direction)
        if direction[0] != 0 or direction[1] != 0:
            if len(snake) > 1:
                snake_tail = snake.pop(-1)
                snake_tail.x = snake[0].x + direction[0]
                snake_tail.y = snake[0].y + direction[1]

                snake.insert(0, snake_tail)
            else:
                snake[0].x += direction[0]
                snake[0].y += direction[1]

        verify_snake_out_of_table(snake[0])

        for snake_box in snake:
            pygame.draw.rect(screen, WHITE, snake_box)

        for obstacle_rect in obstacles_rect:
            pygame.draw.rect(screen, RED, obstacle_rect)

        while no_food:
            food = get_food()
            if len(food.collidelistall(obstacles_rect)) == 0 and len(food.collidelistall(snake)) == 0:
                no_food = False

        pygame.draw.rect(screen, (0, 255, 0), food)

        # verific daca se loveste de obstacole sau de el insusi
        if len(snake[0].collidelistall(obstacles_rect)) > 0:
            break
        danger_zone = snake.copy()
        danger_zone.pop(0)
        if len(snake[0].collidelistall(danger_zone)) > 0:
            break

        if snake[0].colliderect(food):
            pygame.draw.rect(screen, WHITE, food)
            snake_tail = snake[-1].copy()
            snake_tail.x = snake[-1].x - direction[0]
            snake_tail.y = snake[-1].y - direction[1]
            snake.append(snake_tail)
            score += 5
            text_surface = font.render('Your Score: ' + str(score), False, WHITE)
            no_food = True

        pygame.display.update()
        clock.tick(15)


main()
pygame.quit()
quit()
