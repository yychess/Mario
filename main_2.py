import os
import sys
import pygame

pygame.init()
screen = None
FPS = 50
clock = pygame.time.Clock()


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def start_screen():
    intro_text = ["Перемещение героя", "",
                  "Герой двигается",
                  "Карта на месте"]

    fon = pygame.transform.scale(load_image('fon.jpg'), size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mar.png')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.type = tile_type
        self.x = pos_x
        self.y = pos_y


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.x = pos_x
        self.y = pos_y


player = None

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


def game_screen(file_name):
    player, level_x, level_y = generate_level(load_level(file_name))

    while True:
        for event in pygame.event.get():
            screen.fill("black")
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    for tile in tiles_group:
                        if tile.x + 1 == player.x and tile.y == player.y and tile.type == 'empty':
                            player.rect.x -= tile_width
                            player.x -= 1
                            break
                if keys[pygame.K_RIGHT]:
                    for tile in tiles_group:
                        if tile.x - 1 == player.x and tile.y == player.y and tile.type == 'empty':
                            player.rect.x += tile_width
                            player.x += 1
                            break
                if keys[pygame.K_UP]:
                    for tile in tiles_group:
                        if tile.y + 1 == player.y and tile.x == player.x and tile.type == 'empty':
                            player.rect.y -= tile_height
                            player.y -= 1
                            break
                if keys[pygame.K_DOWN]:
                    for tile in tiles_group:
                        if tile.y - 1 == player.y and tile.x == player.x and tile.type == 'empty':
                            player.rect.y += tile_height
                            player.y += 1
                            break
            if event.type == time:
                all_sprites.draw(screen)
                player_group.draw(screen)
                pygame.display.flip()


if __name__ == '__main__':
    fail_name = input()
    fullname = "/".join(['data', fail_name])
    if not os.path.isfile(fullname):
        print(f"Файл с уровнем '{fullname}' не найден")
        sys.exit()

    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Перемещение героя')

    time = pygame.USEREVENT + 1
    pygame.time.set_timer(time, 20)

    start_screen()
    game_screen(fail_name)
