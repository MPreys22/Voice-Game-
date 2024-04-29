import pygame
from pygame import *

class Box(pygame.sprite.Sprite):
    def __init__(self, x, y, size, image):
        super().__init__()
        self.image = pygame.transform.scale(image, (size, size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class World(pygame.sprite.Group):
    def __init__(self, data, box_size):
        super().__init__()
        self.box_size = box_size
        self.load_images()
        self.create_world(data)

    def load_images(self):
        self.box_images = {
            1: pygame.image.load('Images/stone.png'),
            # Add more images
        }

    def create_world(self, data):
        # I wanted to associate certain boxes/platforms with their specific indexes in the for loop which the enumerate function was able to help with: https://www.geeksforgeeks.org/enumerate-in-python/ 
        for row_count, row in enumerate(data):
            for col_count, box in enumerate(row):
                # Using the data/indicies from the big world data list, check if the indicie has a matching picture in the dictionary and if so save that image 
                # Using that saved image, create a new box at the correct position, then finally add it to world which can keep track of which boxes to draw still
                if box in self.box_images:
                    image = self.box_images[box]
                    new_box = Box(col_count * self.box_size, row_count * self.box_size, self.box_size, image)
                    self.add(new_box)

class Game:
    def __init__(self):
        pygame.init()
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


    def run(self):
        run = True
        while run:
            self.screen.blit(self.background, (0, 0))
            self.world.draw(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            pygame.display.update()
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
