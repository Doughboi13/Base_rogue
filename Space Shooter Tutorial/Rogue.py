import pygame
from sprites import *
from config import *
import sys
pygame.font.init()

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        '''self.font = pygame.font.Font("Arial", 32)'''
        self.running = True

        self.character_spritesheet = Spritesheet("C:/Users/jdoughty/Documents/Python/Space invaders/Space Shooter Tutorial/img/character.png")
        self.terrain_spritesheet = Spritesheet("C:/Users/jdoughty/Documents/Python/Space invaders/Space Shooter Tutorial/img/terrain.png")
        self.enemy_spritesheet = Spritesheet("C:/Users/jdoughty/Documents/Python/Space invaders/Space Shooter Tutorial/img/enemy.png")
        self.intro_background = pygame.image.load("C:/Users/jdoughty/Documents/Python/Space invaders/Space Shooter Tutorial/img/introbackground.png")
        self.go_background = pygame.image.load("C:/Users/jdoughty/Documents/Python/Space invaders/Space Shooter Tutorial/img/gameover.png")
        self.attack_spritesheet = Spritesheet("C:/Users/jdoughty/Documents/Python/Space invaders/Space Shooter Tutorial/img/attack.png")
        title_font = pygame.font.SysFont("comicsans", 32)

    def createTilemap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "B":
                    Block(self, j, i)
                if column == "E":
                    Enemy(self, j, i)
                if column == "P":
                    self.player = Player(self, j, i)

    def new(self):

        #New Game
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.createTilemap()

    def events(self):
        # game loop events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.player.facing == "up":
                        Attack(self, self.player.rect.x, self.player.rect.y - TILESIZE)
                    if self.player.facing == "down":
                        Attack(self, self.player.rect.x, self.player.rect.y + TILESIZE)
                    if self.player.facing == "left":
                        Attack(self, self.player.rect.x - TILESIZE, self.player.rect.y)
                    if self.player.facing == "right":
                        Attack(self, self.player.rect.x + TILESIZE, self.player.rect.y)

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        #Game Loop
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def game_over(self):
        font = pygame.font.SysFont("comicsans", 32)
        text = font.render("Game Over", True, WHITE)
        text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))

        restart_button = Button(10, WIN_HEIGHT - 60, 120, 50, WHITE, BLACK, "Restart")

        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()

            self.screen.blit(self.go_background, (0,0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def intro_screen(self):
        intro = True
        title_font = pygame.font.SysFont("comicsans", 32)
        title = title_font.render("Game action", True, BLACK)
        title_rect = title.get_rect(x=255, y=10)

        play_button = Button(275, 275, 100, 50, WHITE, BLACK, "Play")


        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False

            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()

pygame.quit()
