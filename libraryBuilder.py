from pyDungeon import *
import sys, numpy, pickle, os, shutil

ROOMS = 50
SIZE = 64

if __name__=="__main__":

    if os.path.exists('DungeonLibrary'):
        shutil.rmtree('DungeonLibrary')
        
    os.mkdir('DungeonLibrary')
    for d in range(0,15):
        dstr = os.path.join('DungeonLibrary','L'+repr(d))
        os.mkdir(dstr)

        for k in range(0,5):
            print('Generating Dungeon '+repr(d)+':'+repr(k))
            dungeon = angDungeon(d, SIZE, SIZE, ROOMS)

            dungeon2 = dungeon.tolist()

            pickle.dump(dungeon2,open(os.path.join(dstr,repr(k)),'wb'),1)