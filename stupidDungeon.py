import pickle, subprocess

def getDungeon(depth,width=64,height=64,rooms=50,py3x="C:\python31\python.exe"):
    '''uses pyDungeon and a version of python with numpy to generate a new random dungeon

depth - dungeon depth
        0-2 will have rectangular rooms (no actual difference between levels)
        3+ will have cave-like rooms, with rooms generally getting larger with larger depths

width - width of the dungeon, defaults to 64

height - height of the dungeon, defaults to 64

rooms - number of rooms the algorithm will attempt to place in the dungeon.
        Note that some rooms will fail to be placed,
        defaults to 50

py3x - path to python with numpy installed, defaults to "C:\python31\python.exe"'''

    subprocess.call([py3x,'dumpDungeon.py','tempDungeon.pkl',repr(depth),repr(width),repr(height),repr(rooms)])
    dungeon = pickle.load(open('tempDungeon.pkl','rb'))
    return dungeon

if __name__=="__main__":
    print(getDungeon(1,rooms=35))