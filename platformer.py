import pygame
from pygame import *


# This is the class for the individual boxes/pieces of stone 
class Box(pygame.sprite.Sprite):
    def __init__(self, x, y, size, image):
        super().__init__()
        self.box_size = size
        self.image = pygame.transform.scale(image, (size, size))
        self.rect = self.image.get_rect()
        # For Position
        self.rect.x = x
        self.rect.y = y

# Handle the many stones/boxes
class World(pygame.sprite.Group):
    def __init__(self, data, box_size):
        super().__init__()
        self.box_size = box_size
        self.load_images()
        self.create_world(data)

    # Loads in the stone images + Goal image
    def load_images(self):
        self.box_images = {
            1: pygame.image.load('Images/stone.png'),
            # Add more images 
        }

    # I wanted to associate certain boxes/platforms with their specific indexes in the for loop which the enumerate function was able to help with: https://www.geeksforgeeks.org/enumerate-in-python/ 
    def create_world(self, data):
        for row_count, row in enumerate(data):
            for col_count, box in enumerate(row):
                # Using the data/indicies from the big world data list, check if the indicie has a matching picture in the dictionary and if so save that image 
                # Using that saved image, create a new box at the correct position, then finally add it to world which can keep track of which boxes to draw still
                if box in self.box_images:
                    image = self.box_images[box]
                    new_box = Box(col_count * self.box_size, row_count * self.box_size, self.box_size, image)
                    self.add(new_box)
                    


class Player(pygame.sprite.Sprite):
    def __init__(self, posx, posy, gravity):
        super().__init__()
        # Initialize the important variables
        self.image = pygame.image.load(f'Images/plat.jpeg')
        self.rect = self.image.get_rect()
        self.gravity = gravity
        self.rect.x = posx
        self.rect.y = posy
        self.movex, self.movey = 0, 0
        self.on_ground = False
    # Change the position of the player and check for collisions and make sure gravity is applied
    def update(self, world):
        self.rect.x += self.movex
        self.rect.y += self.movey
        self.apply_gravity()
        self.check_collisions(world)
    
    def apply_gravity(self):
        if not self.on_ground:
            self.movey += self.gravity
            # max falling speed
            if self.movey > 10:  
                self.movey = 10

    def check_collisions(self, world):
        # Reset to check if the player is on the ground 
        self.on_ground = False
        # Check for collisions after moving
        hits = pygame.sprite.spritecollide(self, world, False)
        for hit in hits:
            if self.movey > 0:
                self.rect.bottom = hit.rect.top
                self.movey = 0
                self.on_ground = True

    # Changes the movement variables based on which keys are pressed 
    def control(self, x, y):
        self.movex += x
        self.movey += y

class Game:
    # Set up screen and make world data along with player and position
    def __init__(self):
        pygame.init()
        gravity = 0.5
        self.clock = pygame.time.Clock()
        self.screen_width = 1000
        self.screen_height = 1000
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Voice Game')
        self.background = pygame.image.load('Images/game_bckgrnd.jpeg')
        self.box_size = 50
        self.world_data = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
 			[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
			[1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1], 
 			[1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 1, 1, 1], 
 			[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 7, 0, 5, 0, 0, 0, 1], 
 			[1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1], 
 			[1, 7, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
 			[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
 			[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1], 
 			[1, 0, 1, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
 			[1, 0, 0, 1, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 1], 
 			[1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1], 
 			[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
 			[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 1, 0, 1], 
 			[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
 			[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1], 
 			[1, 0, 0, 0, 0, 0, 1, 1, 1, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1], 
 			[1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
 			[1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
 			[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        self.world = World(self.world_data, self.box_size)
        self.player = Player(100, 900, gravity)
        self.player_list = pygame.sprite.Group()
        self.player_list.add(self.player)

    def run(self):

        run = True
        while run:
            # Key Press events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.control(-5, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.player.control(5, 0)
                        # Dont let player double jump
                    elif event.key == pygame.K_UP and self.player.on_ground:
                        self.player.movey = -10
                        self.player.on_ground = False
                        # Move left/right midair
                elif event.type == pygame.KEYUP:
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                        self.player.control(-self.player.movex, 0)

            self.player.update(self.world)
            # Draw Screen
            self.screen.blit(self.background, (0, 0))
            self.world.draw(self.screen)
            self.player_list.draw(self.screen)
            pygame.display.update()
            self.clock.tick(30)
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()