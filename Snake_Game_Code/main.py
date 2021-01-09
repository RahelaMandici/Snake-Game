import sys
import json
import pygame
import random

WHITE = (255, 255, 255)
FUNDAL = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

game_over = False
high_score = 0
snake_box_size = 10
obstacles_box_size = 10


def verify_quit_game():
    """
    Checks if the X button has been pressed. If it has been pressed, close the game.
    :return:
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()


def get_moving_direction(direction):
    """
    It changes the direction of the snake, depending on the input received from the keyboard.
    :param direction: It is a list of two elements which represents the directions of the snake on the X axis and the Y
                    axis.At the beginning of the function, it has the current direction of the snake,
                    after the execution of the function it will have the updated direction of the snake.
    :return:
    """
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


def snake_advances(snake, direction):
    """
    It implements one step forward of the snake.
    :param snake: It is a list of pygame.Rect() objects that represents the squares that make up the snake.
                First of them is the head of the snake. This list is updated during the execution of the function.
    :param direction: It is a list of two elements which represent the directions of the snake on the X axis and the Y
                     axis.
    :return:
    """
    if direction[0] != 0 or direction[1] != 0:
        if len(snake) > 1:
            snake_tail = snake.pop(-1)
            snake_tail.x = snake[0].x + direction[0]
            snake_tail.y = snake[0].y + direction[1]

            snake.insert(0, snake_tail)
        else:
            snake[0].x += direction[0]
            snake[0].y += direction[1]


def verify_snake_out_of_table(snake_head):
    """
    Checks if the snake head is out of the table. If so, it modifies the position of it so that it comes out the other
    side of the table.
    :param snake_head: It is the first element from the snake's list. It is a pygame.Rect() object. During the execution
                        of the function, its position will be modified.
    :return:
    """
    if snake_head.x > table_size[0] - snake_box_size:
        snake_head.x = 0

    if snake_head.x < 0:
        snake_head.x = table_size[0] - snake_box_size

    if snake_head.y > table_size[1] - snake_box_size:
        snake_head.y = 0

    if snake_head.y < 0:
        snake_head.y = table_size[1] - snake_box_size


def get_food():
    """
    Generates a food rectangle on a random position.
    :return food: The food rectangle generated when performing this function.
    """
    food_size = 10
    food_coord = [0, 0]
    food_coord[0] = int(random.randint(0, table_size[0] - snake_box_size) / 10) * 10
    food_coord[1] = int(random.randint(0, table_size[1] - snake_box_size) / 10) * 10
    food = pygame.Rect(food_coord[0], food_coord[1], food_size, food_size)
    return food


def verify_snake_collision(snake):
    """
    Checks if there is collision between the snake head and an obstacle, or between the snake's head and snake's body.
    :param snake: It is a list of pygame.Rect() objects that represents the squares that make up the snake.
                First of them is the head of the snake.
    :return: True: if there is collision between the snake and his body or the obstacles;
             False: if there is no collision between the snake and his body or the obstacles;
    """
    if len(snake[0].collidelistall(obstacles_rect)) > 0:
        return True

    danger_zone = snake.copy()
    danger_zone.pop(0)
    if len(snake[0].collidelistall(danger_zone)) > 0:
        return True


def play():
    """
    This function implements the workflow of the game: draw the table with the obstacles, display the score and calls
    the functions for: food generating,
                    get moving directions of the snake,
                    advancing of the snake,
                    checking if the snake is on table,
                    checking if there is collision between the snake and himself or obstacles (if so, the game is over)
                    checking if there is collision between the snake head and food (if so, the score and the snake
                        length are updating)
    while the game is not over. When the game is over, it calls the function game_over_screen().
    :return:
    """
    global game_over
    direction = [0, 0]
    snake = list()
    no_food = True
    score = 0

    snake.append(pygame.Rect(100, 100, snake_box_size, snake_box_size))
    text_surface = font.render('Your Score: ' + str(score), False, WHITE)
    clock = pygame.time.Clock()

    while not game_over:
        verify_quit_game()
        screen.fill(FUNDAL)

        pygame.draw.line(screen, WHITE, (0, table_size[1]), (table_size[0], table_size[1]))
        screen.blit(text_surface, (table_size[0] / 2 - text_surface.get_width() / 2,
                                   table_size[1] + text_surface.get_height() / 2))
        for obstacle_rect in obstacles_rect:
            pygame.draw.rect(screen, RED, obstacle_rect)

        while no_food:
            food = get_food()
            if len(food.collidelistall(obstacles_rect)) == 0 and len(food.collidelistall(snake)) == 0:
                no_food = False

        pygame.draw.rect(screen, GREEN, food)

        get_moving_direction(direction)

        snake_advances(snake, direction)

        verify_snake_out_of_table(snake[0])

        for snake_box in snake:
            pygame.draw.rect(screen, WHITE, snake_box)

        if verify_snake_collision(snake):
            game_over = True
            game_over_screen(score)

        if snake[0].colliderect(food):
            pygame.draw.rect(screen, WHITE, food)
            snake_tail = snake[-1].copy()
            snake_tail.x = snake[-1].x - direction[0]
            snake_tail.y = snake[-1].y - direction[1]
            snake.append(snake_tail)
            score += 5
            text_surface = font.render('Your Score: ' + str(score), False, WHITE)
            no_food = True

        pygame.display.flip()
        clock.tick(15)


def game_over_screen(score):
    """
    Displays the score of the last game and buttons for play again and quit session. It memorises the high score of the
    current session. If the play again button is pressed, the play() function is called. If the quit session button is
    pressed, the quit_session_screen() function is called.
    :param score: The score of the last game.
    :return:
    """
    global game_over, high_score

    screen.fill(FUNDAL)
    text_surface = font.render('Your Score: ' + str(score), False, WHITE)
    screen.blit(text_surface, (table_size[0] / 2 - text_surface.get_width() / 2,
                               table_size[1] / 2 - text_surface.get_height()))
    if score > high_score:
        high_score = score

    play_again_text = font.render('Play again', False, WHITE)
    quit_session_text = font.render('Quit Session', False, WHITE)

    screen.blit(play_again_text, (table_size[0] / 2 - play_again_text.get_width() / 2,
                                  table_size[1] / 2 + play_again_text.get_height()))
    screen.blit(quit_session_text, (table_size[0] / 2 - quit_session_text.get_width() / 2,
                                    table_size[1] / 2 + play_again_text.get_height()
                                    + quit_session_text.get_height() + 50))

    button_play_again = pygame.Rect(table_size[0] / 2 - play_again_text.get_width() / 2,
                                    table_size[1] / 2 + play_again_text.get_height(), play_again_text.get_width(),
                                    play_again_text.get_height())

    button_quit_session = pygame.Rect(table_size[0] / 2 - quit_session_text.get_width() / 2,
                                      table_size[1] / 2 + play_again_text.get_height()
                                      + quit_session_text.get_height() + 50, quit_session_text.get_width(),
                                      quit_session_text.get_height())

    pygame.display.flip()
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button_play_again.collidepoint(event.pos):
                        game_over = False
                        play()
                    if button_quit_session.collidepoint(event.pos):
                        game_over = False
                        quit_session_screen()


def quit_session_screen():
    """
    Displays the high score of the current session and waits for the X button to be pressed.
    :return:
    """
    screen.fill(FUNDAL)
    text = font.render('High score: ' + str(high_score), False, WHITE)

    screen.blit(text, (table_size[0] / 2 - text.get_width() / 2, table_size[1] / 2))
    pygame.display.flip()
    while True:
        verify_quit_game()


def main():
    """
    Reads the dimensions of the table and the positions of the obstacles from the table.json file and calls the play()
    function to start a game.
    :return:
    """
    global obstacles_rect, screen, table_size, font

    with open(sys.argv[1]) as f_in:
        data = json.load(f_in)

    table_size = data["table_size"].copy()
    obstacles = data["obstacles"].copy()

    pygame.init()
    pygame.display.set_caption('Snake Game')
    font = pygame.font.SysFont('Comic Sans MS', 30)
    screen = pygame.display.set_mode((table_size[0], table_size[1] + 100))

    obstacles_rect = [pygame.Rect(obstacle[0], obstacle[1], obstacles_box_size, obstacles_box_size)
                      for obstacle in obstacles]

    play()


main()
