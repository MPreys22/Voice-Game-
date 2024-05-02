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
    def __init__(self, data, box_size, box_array):
        super().__init__()
        self.box_size = box_size
        self.load_images()
        self.box_array = box_array
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
                    self.box_array.append(new_box)
                    


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load in different images for different animations to go through when moving 
        # self.images = [pygame.image.load(f'Images/hero{i}.jpeg').convert_alpha() for i in range(1, 5)]
        self.image = pygame.image.load(f'Images/plat.jpeg')
        self.rect = self.image.get_rect()
        self.movex, self.movey = 0, 0
        self.frame = 0
    # Change the position of the player and change which animation they are on
    def update(self):
        self.rect.x += self.movex
        self.rect.y += self.movey
        self.rect.bottom = self.rect.y + 360
        # If there is any movement, change which frame we are on
        # if self.movex != 0 or self.movey != 0:  
        #     self.frame = (self.frame + 1) % len(self.images)
        #     self.image = self.images[self.frame]

    # Changes the movement variables based on which keys are pressed 
    def control(self, x, y):
        self.movex += x
        self.movey += y

class Game:
    # Set up screen and make world data along with player and position
    def __init__(self):
        pygame.init()
        self.box_array = []
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
        self.world = World(self.world_data, self.box_size, self.box_array)
        self.player = Player()
        self.player.rect.x = 100  # Starting X position
        self.player.rect.y = 100  # Starting Y position
        self.player_list = pygame.sprite.Group()
        self.player_list.add(self.player)

    def run(self):
        gravity = 0.01
        player_velocity = 0

        run = True
        while run:
            # Draw Screen
            self.screen.blit(self.background, (0, 0))
            self.world.draw(self.screen)
            self.player_list.draw(self.screen)
            
            # Key Press events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        # Move Left
                        self.player.movex = -5
                    elif event.key == pygame.K_RIGHT:
                        # Move Right
                        self.player.movex = 10
                    elif event.key == pygame.K_UP:
                        # Move up
                        self.player.movey = -5
                        # player_velocity = -10
                elif event.type == pygame.KEYUP:
                    # Making sure that the player only moves when the key is held down and not pressed
                    if event.key == pygame.K_LEFT and self.player.movex < 0:
                        self.player.movex = 0
                    elif event.key == pygame.K_RIGHT and self.player.movex > 0:
                        self.player.movex = 0
                    if event.key == pygame.K_UP and self.player.movey < 0:
                        self.player.movey = 0  
            
            # Apply gravity
            player_velocity += gravity
            self.player.movey += player_velocity

            # Make sure the player does not fall off of the screen
            if self.player.rect.bottom > 1000:
                self.player.rect.bottom = 1000 
                player_velocity = 0

            if self.player.rect.collidelist(self.box_array) >= 0:
                box = self.player.rect.collidelist(self.box_array)
                self.player.rect.bottom = self.box_array[box].rect.y
                # self.player.rect.x = self.box_array[box].rect.x + self.box_array[box].box_size



            self.player.update()
            pygame.display.update()
            self.clock.tick(30)
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()