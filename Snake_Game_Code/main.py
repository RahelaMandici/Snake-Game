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


def main():
    global close_all
    pygame.init()
    clock = pygame.time.Clock()

    close_all = False
    snake_box_size = 10
    obstacles_box_size = 10

    screen = pygame.display.set_mode((table_size[0], table_size[1]))
    snake_head = pygame.Rect(50, 50, snake_box_size, snake_box_size)
    obstacles_rect = [pygame.Rect(obstacle[0], obstacle[1], obstacles_box_size, obstacles_box_size)
                      for obstacle in obstacles]

    while not close_all:
        verify_quit_game()
        screen.fill(BLACK)

        pygame.draw.rect(screen, WHITE, snake_head)

        for obstacle_rect in obstacles_rect:
            pygame.draw.rect(screen, RED, obstacle_rect)

        pygame.display.update()
        clock.tick(6)


main()
pygame.quit()
quit()
