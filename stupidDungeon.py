import pickle, subprocess

def getDungeon(depth,width=64,height=64,rooms=50,py3x="C:\python31\python.exe"):
    subprocess.call([py3x,'dumpDungeon.py','tempDungeon.pkl',repr(depth),repr(width),repr(height),repr(rooms)])
    dungeon = pickle.load(open('tempDungeon.pkl','rb'))
    return dungeon

if __name__=="__main__":
    print(getDungeon(1,rooms=35))