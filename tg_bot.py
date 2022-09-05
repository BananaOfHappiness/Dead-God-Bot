from dotenv import load_dotenv, find_dotenv
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import parser

#Get Token
load_dotenv('/Users/egor/Documents/Python/TOKENS/.env')
bot = Bot(os.getenv('TOKEN'))

dp = Dispatcher(bot)

Item_Syn1 = ''
Item_Virtues1 = ''
Item_Judas_BR1 = ''
Item_Bugs1 = ''

Message_Data = []

@dp.message_handler(commands = ['start', 'help'])
async def help(message: types.message):
    await message.answer('Привет! Введи название предмета, а я покажу его описание! Чтобы внести вклад в проект напиши /git')

@dp.message_handler(commands = ['git'])
async def help(message: types.message):
    await message.answer('Ссылка на гит: https://github.com/BananaOfHappiness/Dead-God-Bot')

#Get Item Description
@dp.message_handler()
async def get_description(message: types.message):
    global Item_Syn1, Message_Data, Item_Virtues1, Item_Judas_BR1, Item_Bugs1
    Item_Name, Item_Desc, Item_Syn, Item_Virtues, Item_Judas_BR, Item_Bugs = parser.get_desc(message.text)
    Item_Syn1 = Item_Syn
    Item_Virtues1 = Item_Virtues
    Item_Judas_BR1 = Item_Judas_BR
    Item_Bugs1 = Item_Bugs
    if Item_Name != 'None, Pls try again':
        with open('downloads/'+ Item_Name +'.png', 'rb') as f:
            Image = f.read()
            if Item_Syn !='':
                Main_Menu.insert(Learn_More_Button)
            if Item_Virtues != '':
                Main_Menu.insert(Book_of_Virtues_Button)
            if Item_Judas_BR != '':
                Main_Menu.insert(Judas_BR_Button)
            if Item_Bugs != '':
                Main_Menu.insert(Bugs_Button)
            await bot.send_photo(message.from_user.id, Image, Item_Desc, reply_markup=Main_Menu)
            Main_Menu.inline_keyboard.clear()
            Item_Name = ''
            Item_Syn = ''
            Item_Virtues = ''
            Item_Judas_BR = ''
            Item_Bugs = ''
    else:
        await message.answer(Item_Desc)


# InLine Buttons
Main_Menu = InlineKeyboardMarkup(row_width=1)
Learn_More_Button = InlineKeyboardButton('Узнать больше', callback_data='Learn_More_Button')
Book_of_Virtues_Button = InlineKeyboardButton('Книга добродетелей', callback_data='Book_of_Virtues_Button')
Judas_BR_Button = InlineKeyboardButton('Право Первородства Иуды', callback_data='Judas_BR_Button')
Bugs_Button = InlineKeyboardButton('Баги', callback_data='Bugs_Button')

@dp.callback_query_handler(text='Learn_More_Button')
async def Learn_More(message: types.message):
    await bot.send_message(message.from_user.id, Item_Syn1.replace('item:[','').replace(']',''))

@dp.callback_query_handler(text='Book_of_Virtues_Button')
async def Book_of_Virtues(message: types.message):
    await bot.send_message(message.from_user.id, Item_Virtues1.replace('item:[','').replace(']',''))

@dp.callback_query_handler(text='Judas_BR_Button')
async def Learn_More(message: types.message):
    await bot.send_message(message.from_user.id, Item_Judas_BR1.replace('item:[','').replace(']',''))

@dp.callback_query_handler(text='Bugs_Button')
async def Learn_More(message: types.message):
    await bot.send_message(message.from_user.id, Item_Bugs1.replace('item:[','').replace(']',''))

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)