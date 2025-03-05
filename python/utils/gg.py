class GoodGame(Exception):
    pass

_goodgame_hp = 1
def GG(*args, **kwargs):
    global _goodgame_hp
    _goodgame_hp -= 1
    if _goodgame_hp <= 0:
        raise GoodGame(*args, **kwargs)

def set_hp(hp):
    global _goodgame_hp
    _goodgame_hp = int(hp)

def get_hp():
    return _goodgame_hp
