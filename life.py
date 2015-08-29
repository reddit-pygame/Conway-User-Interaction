#! /usr/bin/env python

"""
A barebones implementation of Conway's Game of Life.
"""

import os
import sys

import pygame as pg


CAPTION = "Conway"
SCREEN_SIZE = (792, 492)
BACKGROUND_COLOR = pg.Color("darkslategray")

BIRTH = {3} # Neighbors an empty cell needs to be born.
SURVIVE = {2, 3} # Neighbors a living cell needs to survive.

# Seed for a 'Gosper Glider Gun' in set form.
SEED = {(22, 3), (17, 5), (16, 8), (2, 6),(35, 3), (16, 4), (36, 4), (14, 3),
        (25, 7), (22, 4), (21, 4), (18, 6), (1, 6), (25, 1), (36, 3), (13, 9),
        (2, 5), (35, 4), (14, 9), (17, 7), (11, 7), (17, 6), (13, 3), (11, 5),
        (25, 6), (23, 2), (21, 3), (1, 5), (15, 6), (12, 4), (21, 5), (25, 2),
        (22, 5), (23, 6), (11, 6), (12, 8)}
        
# Convenient constant for looking at adjacent neighbors.
ADJACENTS = {(-1, 1), (0, 1), (1, 1), (-1, 0),
             (1, 0), (-1, -1), (0,-1), (1,-1)}

             
class App(object):
    """
    Manages control flow for entire program.
    """
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.fps = 30
        self.clock = pg.time.Clock()
        self.done = False
        self.size = (12, 12)
        self.cell_w = self.screen_rect.w//self.size[0]
        self.cell_h = self.screen_rect.h//self.size[1]
        self.birth, self.survive = BIRTH.copy(), SURVIVE.copy()
        self.living = SEED.copy()
        self.wrapping = True
        self.generating = False

    def event_loop(self):
        """
        Start and stop generation by pressing spacebar.
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.generating = not self.generating

    def update(self):
        """
        If generating is True, calculate the next generation of living cells.
        """
        if self.generating:
            self.living = get_next_gen(self.living, self.birth, self.survive,
                                       self.wrapping, self.cell_w, self.cell_h)

    def render(self):
        """
        Clear the screen and render all living cells.
        """
        self.screen.fill(BACKGROUND_COLOR)
        for x,y in self.living:
            rect = pg.Rect((x*self.size[0], y*self.size[1]), self.size)
            self.screen.fill(pg.Color("tomato"), rect.inflate(-2,-2))
        pg.display.update()

    def main_loop(self):
        """
        Spin.
        """
        while not self.done:
            self.event_loop()
            self.update()
            self.render()
            self.clock.tick(self.fps)


def get_next_gen(current, birth=BIRTH, survive=SURVIVE, *wrap_args):
    """
    Given a set of cells, calculates the next generation of cells.
    Rules default to Conway but different rule sets can be passed.
    """
    neighbors = count_neighbors(current, *wrap_args)
    next_generation = set()
    for neighbor in neighbors:
        if neighbors[neighbor] in birth and neighbor not in current:
            next_generation.add(neighbor)
        elif neighbors[neighbor] in survive and neighbor in current:
            next_generation.add(neighbor)
    return next_generation
    

def count_neighbors(current, wrap=False, width=None, height=None):
    """
    Count the number of neighbors around all current cells.
    If wrap is True, the calculation will include wrap around.
    The width and height of the field (in cells) must be passed
    if wrap is True.
    Returns a dictionary with coordinates of the cell to the
    number of neighbors.
    """
    neighbors = {}
    for x,y in current:
        for i,j in ADJACENTS:
            if wrap:
                check = ((x+i)%width, (y+j)%height)
            else:
                check = (x+i, y+j)
            neighbors[check] = neighbors.get(check, 0)+1
    return neighbors
    
    
def main():
    """
    Set up our environment; create an App instance; and start our main loop.
    """
    os.environ["SDL_VIDEO_CENTERED"] = "True"
    pg.init()
    pg.display.set_caption(CAPTION)
    pg.display.set_mode(SCREEN_SIZE)
    App().main_loop()
    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
