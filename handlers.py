import random
from aiogram.types import Message
from aiogram.dispatcher.filters import Text
from config import dp
import game

@dp.message_handler(commands=['start'])
async def on_start(message: Message):
    await message.answer(text=f'{message.from_user.full_name}, привет! Это игра в конфеты! Правила очень простые:\n'
                              f'Кто последний возьмет конфеты со стола, тот и побеждает!\n'
                              f'За один ход возможно брать не более 28ми конфет!\n'
                              f'Бот и игрок ходят по очереди. Кто ходит первый определит жребий.\n'
                              f'Для начала новой игры введи команду /new_game')


@dp.message_handler(commands=['new_game'])
async def start_new_game(message: Message):
    game.start_game()
    if game.games():
        toss = random.randint(0, 1)
        if toss == 1:
            await player_turn(message)
        else:
            await bot_turn(message)

async def player_turn(message: Message):
    await message.answer(f'{message.from_user.first_name}, твой ход!\n'
                         f'Сколько конфет берешь?')

async def bot_turn(message):
    total = game.get_total()
    if total <= 28:
        takebot = total
    else:
        takebot = random.randint(1, 28)
    game.take_candy(takebot)
    if await check_win(message, takebot, 'bot'):
        return
    await message.answer(f'Бот взял {takebot} конфет\n'
                         f'На столе осталось {game.get_total()} конфет.\n'
                         f'Ходит игрок!')
    # if await check_win(message, takebot, 'bot'):
    #     return
    await player_turn(message)

@dp.message_handler()
async def take(message: Message):
    if game.games():
        if message.text.isdigit():
            if (0 < int(message.text) < 29) and int(message.text) <= game.get_total():
                game.take_candy(int(message.text))
                if await check_win(message, int(message.text), 'player'):
                    return
                await message.answer(f'{message.from_user.first_name} взял {int(message.text)} конфет\n'
                                     f'На столе осталось {game.get_total()} конфет.\n'
                                     f'Ходит бот!')
                await bot_turn(message)
            else:
                await message.answer('Недопустимое количество взятых конфет. Введи число от 1 до 28.')
        else:
            pass

async def check_win(message, take: int, player: str):
    if game.get_total() <= 0:
        if player == 'player':
            await message.answer(f'{message.from_user.first_name} взял {take} конфет последним со стола!\n'
                                 f'{message.from_user.first_name} одержал победу!')

        else:
            await message.answer(f'Бот взял {take} конфет последим со стола!\n'
                                 f'Бот одержал победу!\n'
                                 f'{message.from_user.first_name}, не печалься, победишь в следующий раз!')
        game.start_game()
        return True
    else:
        return False