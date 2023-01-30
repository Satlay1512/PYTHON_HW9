from aiogram.types import Message
from aiogram.dispatcher.filters import Text
from config import dp
import text
import game
import random

@dp.message_handler(commands=['start'])
async def  on_start(message: Message):
    await message.answer(text=f'{message.from_user.first_name},{text.greating}')
    
@dp.message_handler(commands=['new_game'])
async def start_new_game(message: Message):
    game.new_game()
    if game.check_game():
        toss = random.choice([True,False])
        if toss:
            await player_turn(message)
        else:
            await bot_turn(message)

async def player_turn(message):
    await message.answer(f'{message.from_user.first_name},' 
    f' твой ход! Сколько возмешь конфет?')

@dp.message_handler()
async def take(message: Message):
    name = message.from_user.first_name
    if game.check_game():
         if message.text.isdigit():
            take = int(message.text)
            if (0 < take < 29) and take <= game.get_total():
                game.take_candies(take)
                if await check_win(message, 'player'):
                    return
                await message.answer(f'{name} взял {take} кoнфет и на столе осталось'
                f'{game.get_total()}. Ходит бот ....')
                await bot_turn(message)
            else:
                await message.answer('Попробуй еще раз взять, только небольше 29')
         else:
            pass

async def bot_turn(message):
    total = game.get_total()
    if total <= 28:
        take = total
    else:
        take = random.randint(1, 28)
    game.take_candies(take)
    await message.answer(f'Бот взял {take} конфет и их осталось {game.get_total()}')
    if await check_win(message, 'Бот'):
        return
    await player_turn(message)
        
async def check_win(message, player: str):
    if game.get_total() <= 0:
        if player == 'player':
            await message.answer(f'{message.from_user.first_name} ты молодец! Тебе удалось одержал победу над бездушной машиной')

        else:
            await message.answer(f'БОТ одержал победу!!! {message.from_user.first_name} если бы ты сильней старался, то все было бы наоборот!')
        game.new_game()
        return True
    else:
        return False
            














    