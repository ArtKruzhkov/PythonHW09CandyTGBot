total = 150
new_game = False
def get_total():
    global total
    return total

def take_candy(take: int):
    global total
    total = total - take


def games():
    global new_game
    return new_game


def start_game():
    global new_game
    global total
    if new_game:
        new_game = False
    else:
        total = 150
        new_game = True