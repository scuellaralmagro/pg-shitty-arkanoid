import pygame as pg
import os

## WINDOW SPECS

WINDOW_WIDTH, WINDOW_HEIGHT = 400, 650
WINDOW = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pg.display.set_caption('Shitty Arkanoid')
pg.mixer.init()

BACKGROUND_COLOR = (0, 0, 0)

## GAME VARIABLES

FPS = 120
BAR_WIDTH, BAR_HEIGHT = 80, 20
BALL_RADIUS = 10
BAR_SPEED = 5
BALL_SPEED = 4
BRICK_WIDTH, BRICK_HEIGHT = 40, 20
BRICK_WALL_X_START, BRICK_WALL_X_FINISH = 0, 400
BRICK_WALL_Y_START, BRICK_WALL_Y_FINISH = 0, 300

## SOUNDS

boop = pg.mixer.Sound(os.path.join('assets', 'boop.wav'))
game_start = pg.mixer.Sound(os.path.join('assets', 'game_start.wav'))

## FUNCTIONS

def create_wall(brick_width, brick_height, wall_x_start, wall_x_finish, wall_y_start, wall_y_finish):
    bricks = []

    for y in range(wall_y_start, wall_y_finish, brick_height):
        for x in range(wall_x_start, wall_x_finish, brick_width):
            brick = Brick(position = (x, y), size = (brick_width, brick_height))
            bricks.append(brick)

    return bricks

## CLASSES

class Bar:
    def __init__(self, position, size, velocity) -> None:
        self.position = position
        self.size = size
        self.velocity = velocity
        self.image = pg.transform.scale(pg.image.load(os.path.join('assets', 'bar1.png')), size)

    def draw(self, WINDOW):
        WINDOW.blit(self.image, self.position)
    def update(self):
        keys_pressed = pg.key.get_pressed()
        if keys_pressed[pg.K_a] and self.position[0] > 0:
            self.position[0] -= self.velocity[0]
        elif keys_pressed[pg.K_d] and self.position[0] < WINDOW_WIDTH - self.size[0]:
            self.position[0] += self.velocity[0]

class Ball:
    def __init__(self, position, size, velocity) -> None:
        self.position = position
        self.size = size
        self.velocity = velocity
        self.image = pg.transform.scale(pg.image.load(os.path.join('assets', 'ball1.png')), size)
        self.attached = True
        self.rect = pg.Rect(position, size)         # ONLY FOR COLLISION DETECTION PURPOSES.
    
    def draw(self, WINDOW):
        WINDOW.blit(self.image, self.position)
    def update(self, bar, sound):

        # KEEPS BALL ON THE BAR WHEN ATTACHED IS TRUE.

        if self.attached == True:
            self.position[0] = bar.position[0] + bar.size[0] / 2 - self.size[0]/2
            self.position[1] = bar.position[1] - self.size[1]

            keys = pg.key.get_pressed()
            if keys[pg.K_SPACE]:
                self.attached = False
                sound.play()
        
        # BALL MOVEMENT SYSTEM.

        else:                                               
            self.position[0] += self.velocity[0]
            self.position[1] += self.velocity[1]
            
            # WALL COLLISION DETECTION / X-AXIS.
            
            if self.position[0] - self.size[0] < 0:
                self.velocity[0] *= -1
            elif self.position[0] + self.size[0] > WINDOW_WIDTH:
                self.velocity[0] *= -1

            # WALL COLLISION DETECTION / Y-AXIS.

            if self.position[1] - self.size[1] < 0:         
                self.velocity[1] *= -1
            elif self.position[1] + self.size[1] > WINDOW_HEIGHT:
                self.attached = True
            
            # BAR COLLISION DETECTION.

            if self.position[0] + self.size[0] > bar.position[0] and self.position[0] - self.size[0] < bar.position[0] + bar.size[0]:
                if self.position[1] + self.size[1] > bar.position[1]:
                    self.position[1] = bar.position[1] - self.size[1]
                    offset = self.position[0] - (bar.position[0] + bar.size[0] / 2)     # ALTERS X-AXIS SPEED DEPENDING ON WHERE THE BALL HITS ON THE BAR.
                    self.velocity[0] = offset * 0.2
                    self.velocity[1] *= -1

        # UPDATES RECT COORDINATES TO GO ALONG WITH BALL OBJECT.            
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

    def force_collision(self):
        self.velocity[0] *= -1
        self.velocity[1] *= -1

class Brick:
    def __init__(self, position, size) -> None:
        self.position = position
        self.size = size
        self.image = pg.transform.scale(pg.image.load(os.path.join('assets', 'tile0.png')), size)
        self.rect = pg.Rect(position, size)
        self.alive = True

    def draw(self, WINDOW):
        WINDOW.blit(self.image, self.position)
    def kill(self):
        self.alive = False

## DRIVER CODE

def main():

    # OBJECT INSTANTIATION

    bar = Bar(position=[160, 575], size = [BAR_WIDTH, BAR_HEIGHT], velocity = [BAR_SPEED, 0])
    ball = Ball(position = [(bar.position[0] + bar.size[0] / 2), (bar.position[1] + BALL_RADIUS)],
                size = [BALL_RADIUS, BALL_RADIUS], velocity = [BALL_SPEED, BALL_SPEED])
    bricks = create_wall(BRICK_WIDTH, BRICK_HEIGHT, BRICK_WALL_X_START, BRICK_WALL_X_FINISH, BRICK_WALL_Y_START, BRICK_WALL_Y_FINISH)

    # FPS & CLOCK STUFF

    clock = pg.time.Clock()
    run = True

    # OTHER VARIABLES

    lives = 5       # Not implemented yet.
    score = 0       # Not implemented yet.

    # EVENT LOOP

    while run:
        clock.tick(FPS)                     # Limits clock tick to FPS constant.
        for event in pg.event.get():
            if event.type == pg.QUIT:       # Exits game if user closes window.
                run = False
        
        # MOVEMENT & COLLISIONS:

        bar.update()
        ball.update(bar, sound = game_start)
        for brick in bricks:
            if ball.rect.colliderect(brick.rect) and brick.alive == True:
                brick.kill()
                ball.force_collision()
                boop.play()
                score += 1


        # RENDERING:

        ball.draw(WINDOW)
        bar.draw(WINDOW)
        for brick in bricks:
            if brick.alive == True:
                brick.draw(WINDOW)
            else:
                pass

        pg.display.flip()
        WINDOW.fill(BACKGROUND_COLOR)

        ## DEBUG CODE HERE:



    pg.quit()

if __name__ == '__main__':
    main()