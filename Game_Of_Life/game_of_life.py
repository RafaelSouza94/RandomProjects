#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import argparse
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation

ON = 255
OFF = 0
vals = [ON, OFF]

def main():
    
    parser = argparse.ArgumentParser(description = "Runs Conway's Game of Life simulation.")
    parser.add_argument( '-g', '--grid_size', dest = 'N', help = "Size of grid NxN.", required = False)
    parser.add_argument('-m', '--mov_file', dest = 'mov_file', help = "Name of .mov file to save.", required = False)
    parser.add_argument('-i', '--interval', dest = 'interval', help = "Interval of animation update in miliseconds.", required = False)
    parser.add_argument( '-l', '--glider', action = 'store_true', help = "Start simulation with a glider pattern.", required = False)
    parser.add_argument('-b', '--block', action = 'store_true', help = "Start simulation with a block pattern.", required = False)
    parser.add_argument('-o', '--gosper_gun', action = 'store_true', help = "Start simulation with a gosper gun pattern.", required = False)
    args = parser.parse_args()

    N = 100
    if args.N and int(args.N) > 8:
        N = int(args.N)
    update_interval = 50
    if args.interval:
        update_interval = int(args.interval)
    grid = np.array([])
    if args.glider:
        grid = np.zeros(N * N).reshape(N, N)
        add_glider(1, 1, grid)
    elif args.block:
        grid = np.zeros(N * N).reshape(N, N)
        add_block(1, 1, grid)
    elif args.gosper_gun:
        grid = np.zeros(N * N).reshape(N, N)
        add_gosper_gun(1, 1, grid)
    else:
        grid = random_grid(N)
        
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation = 'nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, ),
                                  frames = 10,
                                  interval = update_interval,
                                  save_count = 50)
    if args.mov_file:
        ani.save(args.movfile, fps = 30, extra_args=['-vcodec', 'libx264'])
    
    plt.show()

def random_grid(N):
    """returns a grid of NxN random values"""
    
    return np.random.choice(vals, N * N, p = [0.2, 0.8]).reshape(N, N)

def add_glider(i, j, grid):
    """adds a glider with top left cell at (i, j)"""
    
    glider = np.array([[0, 0, 255],
                      [255, 0, 255],
                      [0, 255, 255]])
    grid[i:i + 3, j:j + 3] = glider
    
def add_block(i, j, grid):
    
    block = np.array([[255, 255, 255], 
                      [255, 255, 255],
                      [255, 255, 255]])
    grid[i:i + 3, j:j + 3] = block
    
def add_gosper_gun(i, j, grid):
     
    gg = np.zeros(9 * 38).reshape(9, 38)
    values = [[4, 0], [5, 0], [4, 1], [5, 1], [4, 10], [5, 10], [6, 10], 
              [3, 11], [7, 11], [2, 12], [8, 12], [2, 13], [8, 13], [5, 14], 
              [3, 15], [7, 15], [4, 16], [5, 16], [6, 16], [5, 17], [2, 20], 
              [3, 20], [4, 20], [2, 21], [3, 21], [4, 21], [1, 22], [5, 22], 
              [0, 24], [1, 24], [5, 24], [6, 24], [2, 34], [3, 34], [2, 35], [3, 35]]
    
    for i in range(0, 9):
        for j in range(0, 35):
            if [i, j] in values:
                gg[i, j] = 255
    
    grid[i:i + 9, j:j + 38] = gg
    
def update(frame_num, img, grid, N):
    
    # copy grid since we require 8 neighbors for calculation and we go line by line
    new_grid = grid.copy()
    for i in range(N):
        for j in range(N):
            # compute the 8-neighbor sum using toroidal boundary conditions
            # x and y wrap around so that the simulation takes place on a toroidal surface
            total = int((grid[i, (j - 1) % N] + grid[i, (j + 1) % N] +
                         grid[(i - 1) % N, j] + grid[(i + 1) % N, j] + 
                         grid[(i - 1) % N, (j - 1) % N] + grid[(i - 1) % N, (j + 1) % N] +
                         grid[(i + 1) % N, (j - 1) % N] + grid[(i + 1) % N, (j + 1) % N]) / 255) 
            # apply Conway's rules
            if grid[i, j] == ON:
                if (total < 2) or (total > 3):
                    new_grid[i, j] = OFF
            else:
                if total == 3:
                    new_grid[i, j] = ON
    
    # update data
    img.set_data(new_grid)
    grid[:] = new_grid[:]
    return img, 
        

            
        
if __name__ == '__main__':
    main()
