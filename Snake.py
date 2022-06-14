from ctypes.wintypes import RGB
import queue
from random import random
from turtle import width
from types import new_class
from typing import Deque
import pygame
import random


# presistant? across all of the game?
# what does presistant mean ?
# I used it in Snake Deque as a datatype , only there it's a pair 
# but the word pair is already prserved
class Cell:
    x , y = (0 , 0)


# resultion
WIDTH = 900
HEIGHT = 500
FRAME_RATE = 10


# display
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
WHITE = (255,255,255)
GREEN = (0,255,0)
GRAY = (200,200,200)
RED = (255 , 0 , 0)

SQUARE_LEN = 20

food = pygame.Rect(random.randint(0, WIDTH // SQUARE_LEN - 1 ) * SQUARE_LEN,
                   random.randint(0, HEIGHT // SQUARE_LEN - 1 ) * SQUARE_LEN,
                   SQUARE_LEN, SQUARE_LEN)

Snake = Deque()
dir = 0


def SnakeMovement():
    global dir , Snake
    KeyPressed = pygame.key.get_pressed()
    if KeyPressed[pygame.K_RIGHT] == True and (dir != 2 or len(Snake) == 1):
        dir = 0
    elif KeyPressed[pygame.K_UP] == True and (dir != 3 or len(Snake) == 1):
        dir = 1
    elif KeyPressed[pygame.K_LEFT] == True and (dir != 0 or len(Snake) == 1):
        dir = 2
    elif KeyPressed[pygame.K_DOWN] == True and (dir != 1 or len(Snake) == 1):
        dir = 3

    else: pass
         

    Last_Square = Cell()
    Last_Square.x = Snake[len(Snake) - 1].x
    Last_Square.y = Snake[len(Snake) - 1].y

    if Last_Square.x == WIDTH // SQUARE_LEN - 1  and dir == 0:
        Last_Square.x = 0
    elif Last_Square.x == 0 and dir == 2:
        Last_Square.x = WIDTH // SQUARE_LEN - 1
    elif Last_Square.y == HEIGHT // SQUARE_LEN - 1 and dir == 3:
        Last_Square.y = 0
    elif Last_Square.y == 0 and dir == 1:
        Last_Square.y = HEIGHT // SQUARE_LEN - 1
    else:
        if dir == 0:
            Last_Square.x += 1
        elif dir == 1:
            Last_Square.y -= 1
        elif dir == 2:
            Last_Square.x -= 1
        else:
            Last_Square.y += 1

    Snake.append(Last_Square)
    Snake.popleft()

    for i in range(0 , len(Snake)):
        ok = False
        for j in range(0 , len(Snake)):
            if i == j: continue
            if Snake[i].x == Snake[j].x and Snake[i].y == Snake[j].y:
                Lose()
                ok = True
                break
        if ok == True:
            break

def RandomColor():
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return (r , g , b)
    
def Lose():
    global Snake
    Snake.clear()
    Snake.append(Cell())
    Snake[0].x = 22
    Snake[0].y = 10

def OnSnake(x , y):
    global Snake
    for Square in Snake:
        if Square.x == x * SQUARE_LEN and Square.y == y * SQUARE_LEN:
            return True

    return False

def FoodHandel():
    global Snake , food
    head = Snake[len(Snake) - 1] 
    if head.x * SQUARE_LEN == food.x and head.y * SQUARE_LEN == food.y:
        food.x = random.randint(0, WIDTH // SQUARE_LEN - 1 ) * SQUARE_LEN  
        food.y = random.randint(0, HEIGHT // SQUARE_LEN - 1 ) * SQUARE_LEN
        while OnSnake(food.x , food.y) == True:
            food.x = random.randint(0, WIDTH // SQUARE_LEN - 1 ) * SQUARE_LEN  
            food.y = random.randint(0, HEIGHT // SQUARE_LEN - 1 ) * SQUARE_LEN

        C = Cell()
        C.x = Snake[0].x - 1
        C.y = Snake[0].y
        Snake.appendleft(C)




def RenderAndDraw():
    WINDOW.fill(WHITE)
    for x in range((HEIGHT // SQUARE_LEN) ):
        for y in range( WIDTH // SQUARE_LEN ):
            if x + y & 1:
                pygame.draw.rect(WINDOW , GRAY ,pygame.Rect(y * SQUARE_LEN, x * SQUARE_LEN, SQUARE_LEN, SQUARE_LEN))
            else:
               pygame.draw.rect(WINDOW , WHITE , pygame.Rect(y * SQUARE_LEN, x * SQUARE_LEN, SQUARE_LEN, SQUARE_LEN))


    cnt = 100 
    for Square in Snake:
        pygame.draw.rect(WINDOW , RGB(0 , cnt , 0) ,pygame.Rect(Square.x * SQUARE_LEN, Square.y * SQUARE_LEN, SQUARE_LEN, SQUARE_LEN))
        cnt += 5

    for Square in Snake:
        pass
        #print(Square.x , Square.y)


    pygame.draw.rect(WINDOW , RED , food)
    pygame.display.update()
    


#game loop
def Game():
    global Snake
    clock = pygame.time.Clock()
    running = True
    Snake.clear()
    Snake.append(Cell())
    Snake[0].x = 22
    Snake[0].y = 10
    while running:
        clock.tick(FRAME_RATE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        SnakeMovement()
        FoodHandel()
        RenderAndDraw()



Game()











