import pygame
import requests
from io import BytesIO

class Imagehandler:
    
    def __init__(self, url: str, w: int, h: int):
        try:
            response = requests.get(url)
            untransformed_image = pygame.image.load(BytesIO(response.content))
            self.image = pygame.transform.scale(untransformed_image, (w, h))
        except:
            print("Image couldn't load")
            if "white" in url:
                self.image = pygame.transform.rotozoom(pygame.image.load("white_circle.png"), 0, 3)
            else:
                self.image = pygame.transform.rotozoom(pygame.image.load("black_circle.png"), 0, 3)