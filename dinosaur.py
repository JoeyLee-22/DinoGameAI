class Dinosaur:
    X_POS = 80
    JUMP_VEL = 7.25
    score = 0

    def __init__(self, Y_POS, DUCKING, RUNNING, JUMPING):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = Y_POS
        
        self.Y_POS = Y_POS
        self.Y_POS_DUCK = Y_POS+30
        self.DUCKING = DUCKING
        self.RUNNING = RUNNING
        self.JUMPING = JUMPING

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput==0 and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput==1 and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False
        elif userInput==2 and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
            
        self.score += 0.25

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))
        
    def getY(self):
        return self.dino_rect.y
    
    def changeScore(self, num):
        self.score = num
    
    def getScore(self):
        return self.score