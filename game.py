import pygame
import os
import random
import numpy as np
from pynput.keyboard import Controller
from dinosaur import Dinosaur
from obstacle import SmallCactus, LargeCactus, Bird
from neuralNetwork import NeuralNetwork

pygame.init()

SCREEN_HEIGHT = 525
SCREEN_WIDTH = 1200
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
Y_POS = SCREEN_HEIGHT-200

game_speed = 20
x_pos_bg = 0
y_pos_bg = Y_POS+70
points = 0
max_score = 0
obstacles = []
kb = Controller()

state = np.zeros(3)
training_inputs = []
training_outputs = []

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

def main(ai, generation_size, run_AI, generation):
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    
    players = []
    if run_AI and ai=='genetic':
        for _ in range(generation_size):
            players.append(Dinosaur(Y_POS, DUCKING, RUNNING, JUMPING))
    else:
        players.append(Dinosaur(Y_POS, DUCKING, RUNNING, JUMPING))
        
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = Y_POS+70
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 30)
    obstacles = []

    def score():
        global points, game_speed, max_score
        points += 0.25
        if ai!='nn':
            if int(points) % 50 == 0:
                game_speed += 1

        text = font.render(str(int(points)).zfill(5), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH-75, 35)
        SCREEN.blit(text, textRect)
        if int(points) > max_score:
            max_score = int(points)
        
        text = font.render("HI   " + str(max_score).zfill(5), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH-225, 35)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed
        
    def data(generation):
        text = font.render("Gen " + str(generation), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (600, SCREEN_HEIGHT-70)
        SCREEN.blit(text, textRect)
        
        if ai=='genetic':
            text = font.render(str(len(players)) + ' players left', True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (600, SCREEN_HEIGHT-30)
            SCREEN.blit(text, textRect)
    
    def getInput():
        global state, prev
        for player, nn in zip(players, NN):
            if run_AI:
                if len(obstacles)!=0 and player.getY() == Y_POS:
                    global state
                    prev = state
                    state = np.array([nn.getDist(obstacles, SCREEN_WIDTH), game_speed/100, nn.getHeight(y_pos_bg, obstacles)])
                    userInput = nn.predict(state)
                else:
                    userInput = 1
            else:
                userInput = pygame.key.get_pressed()
                if userInput[pygame.K_UP]:
                    userInput = 0
                elif userInput[pygame.K_DOWN]:
                    userInput = 2
                else:
                    userInput = 1

            player.draw(SCREEN)
            player.update(userInput)
    
    def checkCollision():
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            for i, player in enumerate(players):
                if player.dino_rect.colliderect(obstacle.rect):
                    if ai=='nn':
                        if player.getY() < Y_POS and not NN[0].check_state(prev_jump_state, training_inputs):
                            training_inputs.append(prev_jump_state)
                            training_outputs.append(np.array([0,1]))
                        elif not NN[0].check_state(prev_run_state, training_inputs):
                            training_inputs.append(prev_run_state)
                            training_outputs.append(np.array([1,0]))
                        NN[0].train(training_inputs, training_outputs, epochs=2000)
                    if ai=='genetic':
                        pass

                    scores[i] = player.getScore()
                    players.remove(player)
                    if len(players)==0:
                        print()
                        for num in scores:
                            print(num)
                        pygame.time.delay(250)
                        menu(ai, generation_size, generation+1, run_AI, 1)
    
    def getObstacle():
        global prev_jump_state, prev_run_state
        if len(obstacles) == 0:
            if run_AI:
                num = random.randint(0,1)
            else:
                num = random.randint(0,2)
                
            if num == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS, SCREEN_WIDTH, Y_POS, game_speed, obstacles))
            elif num == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS, SCREEN_WIDTH, Y_POS, game_speed, obstacles))
            elif num == 2:
                obstacles.append(Bird(BIRD, SCREEN_WIDTH, Y_POS, game_speed, obstacles))
        elif run_AI:
            if players[0].getY() < Y_POS:
                prev_jump_state = prev
            else:
                prev_run_state = prev
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        SCREEN.fill((255, 255, 255))
        
        getInput()
        checkCollision()
        getObstacle()

        background()
        score()
        if run_AI: data(generation+1)
        
        clock.tick(40)
        pygame.display.update()

def menu(ai, generation_size, generation, run_AI, death_count):
    global points
    run = True
    while run:
        SCREEN.fill((255, 255, 255))
        if run_AI:            
            kb.press('a')
            SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
            pygame.display.update()
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type != pygame.QUIT:
                        main(ai, generation_size, run_AI, generation)
        else:
            font = pygame.font.Font('freesansbold.ttf', 30)

            if death_count == 0:
                text = font.render("Press any Key to Start", True, (0, 0, 0))
            elif death_count > 0:
                text = font.render("Press any Key to Restart", True, (0, 0, 0))
                score = font.render("Your Score: " + str(int(points)), True, (0, 0, 0))
                scoreRect = score.get_rect()
                scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
                SCREEN.blit(score, scoreRect)
            textRect = text.get_rect()
            textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            SCREEN.blit(text, textRect)
            SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    main(ai, generation_size, run_AI, generation)

def start(generation_size=2, run_AI=False, ai=''):
    global NN
    NN = []
    if run_AI:
        print('\nRunning AI')
        if ai=='nn':
            NN.append(NeuralNetwork(dimensions=[3,12,2], learningRate=1e-2))
        elif ai=='genetic':
            global scores
            scores = np.empty(generation_size)
            for _ in range(generation_size):
                NN.append(NeuralNetwork(dimensions=[3,12,2]))
    else:
        NN.append(0)
    menu(ai, generation_size, 0, run_AI, 0)