import pygame
from pygame.locals import *
import glob, os
from math import floor

import GIFImage
import load_mod_file

tile_size = (64,32)

def GridToScreen(c, r, cx, cy):
    return cx + c*tile_size[0]*0.5 + r*tile_size[0]*0.5, \
           cy - c*tile_size[1]*0.5 + r*tile_size[1]*0.5 

def ScreenToGrid(mx, my, cx, cy):
    '''Returns Column, Row pair. May return points outside the grid_bounds '''
    return (mx-cx)/tile_size[0] - (my-cy)/tile_size[1], \
           (mx-cx)/tile_size[0] + (my-cy)/tile_size[1]

def color_swap(surf, old, new):
    for x in xrange(surf.get_width()):
        for y in xrange(surf.get_height()):
            rgb = tuple(surf.get_at((x,y))[:3])
            if rgb == old:
                surf.set_at((x,y), new[:3]+(255,))
    return surf

class ImageHandler(object):
    def __init__(self):
        self.images = {}

    def load_dir(self, dire):
        for i in glob.glob(dire+'*.gif'):
            short = os.path.split(i)[1]
            if not short in self.images:
                #already there
                self.images[short] = GIFImage.GIFImage(i)
        for i in glob.glob(dire+'*.png'):
            short = os.path.split(i)[1]
            if not short in self.images:
                #already there
                img = pygame.image.load(i).convert_alpha()
                self.images[short] = img

    def set_flags(self):
        player_flag = 'player-team-flag.png'
        colors = [(255,0,0), (0,255,0), (0,0,255),
                  (255,255,0), (255,0,255), (0,255,255)]

        for i in xrange(6):
            new = self.images[player_flag].copy()
            self.images[player_flag+str(i)] = color_swap(new,
                                                         (127,127,127),
                                                         colors[i])

class MapEntity(object):
    def __init__(self, parent, image, pos=(0,0), name='', render_pos='real'):
        self.parent = parent
        self.image = image
        self.pos = (0,0)
        self.move(*pos)
        self.parent.entities.append(self)
        self.name = name
        self.render_pos = render_pos
        self.dead = False
        self.bound_to = None
    def kill(self):
        if self in self.parent.entities:
            self.parent.entities.remove(self)
            self.dead = True

    def get_real_pos(self):
        cx,cy = self.parent.engine.camera.get_shift_pos()
        tw,th = self.parent.tile_size
        sx, sy = self.pos

        if self.render_pos == 'bottom':
            return (int(cx + sx*tw*0.5 + sy*tw*0.5 + tw*0.5),
                    int(cy - sx*th*0.5 + sy*th*0.5 + th))
        elif self.render_pos == 'center':
            return (int(cx + sx*tw*0.5 + sy*tw*0.5 + tw*0.5),
                    int(cy - sx*th*0.5 + sy*th*0.5 + th*0.5))
        else: #real
            return (int(cx + sx*tw*0.5 + sy*tw*0.5),
                    int(cy - sx*th*0.5 + sy*th*0.5))

    def get_my_tile(self):
        return int(self.pos[0]), int(self.pos[1])

    def move(self, x, y):
        x = self.pos[0] + x
        y = self.pos[1] + y
        if self.parent.map_grid:
            if x < 0:
                x = 0
            if x >= len(self.parent.map_grid[0]):
                x = len(self.parent.map_grid[0])

            if y < 0:
                y = 0
            if y >= len(self.parent.map_grid):
                y = len(self.parent.map_grid)

        self.pos = (x,y)

    def render(self):
        if self.bound_to:
            x, y = self.bound_to.pos
            x -= 0.01
            self.pos = x,y
            if self.bound_to.dead:
                self.kill()
        image = self.parent.images.images[self.image]
        r = image.get_rect()
        x, y = self.get_real_pos()
        if self.render_pos == 'bottom':
            r.midbottom = x,y
        elif self.render_pos == 'center':
            r.midbottom = x,y
        else: # 'real'
            r.topleft = x,y
        
        try:
            image.render(self.parent.screen, r)
        except:
            self.parent.screen.blit(image, r)

class MapHighlight(MapEntity):
    def __init__(self, parent, image, pos=(0,0)):
        self.parent = parent
        self.image = image
        self.pos = (0,0)
        self.move(*pos)
        self.parent.highlights.append(self)
        self.render_pos = 'real'
        self.bound_to = None

    def kill(self):
        if self in self.parent.highlights:
            self.parent.highlights.remove(self)

class MapHandler(object):
    def __init__(self, engine):
        self.tiles = {}
        self.map_grid = []
        self.engine = engine
        self.screen = engine.screen
        self.images = engine.images
        self.entities = []

        self.highlights = []

        self.tile_size = tile_size

    def sort_entities(self, a, b):
        if a.pos[1] < b.pos[1]:
            return -1
        elif b.pos[1] < a.pos[1]:
            return 1
        elif a.pos[0] < b.pos[0]:
            return 1
        elif b.pos[0] < a.pos[0]:
            return -1
        return -1

    def make_entity(self, image, pos, name='', render_pos='bottom'):
        return MapEntity(self, image, map(int, pos), name, render_pos)

    def load_map_file(self, path):
        access = {"game":self.engine.client,
                  'gfx_engine':self.engine}
        succeed = load_mod_file.load(path, access)
        if succeed == False:
            self.engine.failed = True

    def add_highlight(self, image, pos):
        return MapHighlight(self, image, (pos[0], pos[1]))
    def clear_highlights(self):
        self.highlights = []

    def render(self):
        r = 0
        tw, th = self.tile_size
        for row in self.map_grid:
            c = 0
            for col in row:
                cx, cy = self.engine.camera.get_shift_pos()
                self.screen.blit(self.images.images[self.tiles[col]],
                                 (cx + c*tw*0.5 + r*tw*0.5,
                                  cy - c*th*0.5 + r*th*0.5))
                c += 1
            r += 1

        for i in self.highlights:
            i.render()

        self.entities.sort(self.sort_entities)
        for i in self.entities:
            i.render()

    def in_bounds(self, pos):
        xx, yy = pos
        if self.map_grid:
            if xx >= 0 and xx < len(self.map_grid[0]) and\
               yy >= 0 and yy < len(self.map_grid):
                return True
        return False

    def get_mouse_tile(self):
        mx, my = pygame.mouse.get_pos()
        cx, cy = self.engine.camera.get_shift_pos()
        tw = float(self.tile_size[0])
        th = float(self.tile_size[1])
        xx = int(floor((mx-cx)/tw - (my-cy-th*0.5)/th) ) if mx-cx else 0
        yy = int(floor((mx-cx)/tw + (my-cy-th*0.5)/th)) if my-cy else 0

        if self.in_bounds((xx,yy)):
            return xx, yy
        return None

    def get_entities_on_tile(self, x, y):
        n = []
        for i in self.entities:
            a, b = i.get_my_tile()
            if a==x and b==y:
                n.append(i)
        return n

class Camera(object):
    def __init__(self, engine):
        self.pos = (0,0)
        self.engine = engine

    def get_real_pos(self):
        if self.engine.mapd:
            tw,th = self.engine.mapd.tile_size
        else:
            tw, th = tile_size
        sx, sy = self.pos
        return (int(sx*tw*0.5 + sy*tw*0.5 + tw*0.5),
                int(-sx*th*0.5 + sy*th*0.5 + th*0.5))

    def get_shift_pos(self):
        px, py = self.get_real_pos()
        return (320-px,240-py)

    def move(self, x, y):
        x = self.pos[0] + x
        y = self.pos[1] + y
        if self.engine.mapd:
            if x < 0:
                x = 0
            if x >= len(self.engine.mapd.map_grid[0]):
                x = len(self.engine.mapd.map_grid[0])

            if y < 0:
                y = 0
            if y >= len(self.engine.mapd.map_grid):
                y = len(self.engine.mapd.map_grid)

        self.pos = (x,y)

    def set_pos(self, x, y):
        x = x
        y = y
        if self.engine.mapd:
            if x < 0:
                x = 0
            if x >= len(self.engine.mapd.map_grid[0]):
                x = len(self.engine.mapd.map_grid[0])

            if y < 0:
                y = 0
            if y >= len(self.engine.mapd.map_grid):
                y = len(self.engine.mapd.map_grid)

        self.pos = (x,y)

class GFXEngine(object):
    def __init__(self, screen, scenario, client=None):
        self.screen = screen
        self.scenario = scenario
        self.client = client
        self.failed = False
        self.load_images()
        self.mapd = None
        self.camera = Camera(self)
        self.load_map()

    def load_images(self):
        self.images = ImageHandler()
        self.images.load_dir('data/scenarios/%s/images/'%self.scenario)
        self.images.load_dir('data/images/')
        self.images.set_flags()

    def load_map(self):
        self.mapd = MapHandler(self)
        self.mapd.load_map_file('data/scenarios/%s/map.py'%self.scenario)

    def render(self):
        self.mapd.render()
