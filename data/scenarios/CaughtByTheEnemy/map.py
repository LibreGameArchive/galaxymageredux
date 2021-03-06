
mapd = gfx_engine.mapd

mapd.tiles = {0:'floor-dungeon-blue.png',
              1:'floor-dungeon-blue.png', #need tile under walls too!
              2:'floor-dungeon-blue.png',
              3:'floor-dungeon-blue.png'}

mapd.map_grid = [[0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
            [0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,2,0,1],
            [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,1],
            [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1],
            [0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1]]

for y in xrange(20):
    for x in xrange(20):
        if mapd.map_grid[y][x] == 1:
            mapd.make_entity('wall-dungeon-blue.png',
                             (x,y),
                             'blocking') #for the pathing
        if mapd.map_grid[y][x] == 2:
            mapd.make_entity('wall-bars-gate.png',
                             (x,y),
                             'Gate') #for the pathing

mapd.engine.camera.set_pos(2.5, 1.5)
