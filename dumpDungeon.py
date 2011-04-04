from pyDungeon import *
import sys, numpy, pickle

if __name__=="__main__":
    dungeon = angDungeon(int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]))

    dungeon2 = dungeon.tolist()

    pickle.dump(dungeon2,open(sys.argv[1],'wb'),1)