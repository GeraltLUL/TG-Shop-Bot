from pyqiwip2p import QiwiP2P
from aiogram.dispatcher.filters import Text
from aiogram.utils.callback_data import CallbackData
from aiogram import Bot, Dispatcher, executor, types
from Database import Database
import sqlite3
import io

#import database
#from database import dbase

#QIWI
SECRET_KEY = 'eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6Im83dHZtbS0wMCIsInVzZXJfaWQiOiI3OTg4NDc1OTU2MCIsInNlY3JldCI6IjY0NmJmN2JhOTY3OTY0ZDAxMDRlN2FmZjk3MjZhNDAxZmMxMzBmMDViMjJlODljNTFiZjM0ZTZlZTk2NjhkZTAifX0='

#Telegram
API_KEY = "5298929887:AAGop7JfGoLAdJY3zRKRRHOJgBMS1xwKbyQ"

p2p = QiwiP2P(auth_key=SECRET_KEY)
bot = Bot(token=API_KEY)
dp = Dispatcher(bot)

db_products = 'products.db'
db_users = 'users.db'

dbase_prod = Database(sqlite3.connect(db_products))
dbase_user = Database(sqlite3.connect(db_users))

products = []

# При старте бота
@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}!\n"
                         f"Ты попал в магазин книг!\n"
                         f"Приветственное сообщение 1\n"
                         f"Приветственное сообщение 2")

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    ##keyboard.one_time_keyboard = True

    buttons = ["Отзывы", "Ответы на вопросы", "Ассортимент товаров", "Розыгрыши и видео"]
    keyboard.add(*buttons)
    await message.answer("Выберите кнопку", reply_markup=keyboard)

@dp.message_handler(Text(equals="Отзывы"))
async def reviews(message: types.Message):
    await message.reply("Тут будут отзывы!")

@dp.message_handler(Text(equals="Ответы на вопросы"))
async def question_and_answers(message: types.Message):
    await message.reply("Тут будут ответы на вопросы!")

@dp.message_handler(Text(equals="Розыгрыши и видео"))
async def videos(message: types.Message):
    await message.reply("Тут будут розыгрыши и видео!")


@dp.message_handler(Text(equals="Ассортимент товаров"))
async def products_range(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    buttons = dbase_prod.get_categorys()
    buttons.add("Назад")
    keyboard.add(*buttons)

    await message.answer("Выберите категорию", reply_markup=keyboard)

@dp.message_handler(Text(equals="Назад"))
async def back_button(message: types.Message):
    await cmd_start(message)

@dp.message_handler(Text(equals="Русская классика"))
async def category_1(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    global products

    products = dbase_prod.get_items_names()
    for i in products:
        if Text(i[5]).equals == Text(message.text).equals:
            keyboard.add(types.InlineKeyboardButton(text=f"{i[1]}", callback_data=f"getdata_{i[0]}"))

    await message.answer("Выберите товар", reply_markup=keyboard)

@dp.message_handler(Text(equals="Образование"))
async def category_2(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    global products

    products = dbase_prod.get_items_names()
    for i in products:
        if Text(i[5]).equals == Text(message.text).equals:
            keyboard.add(types.InlineKeyboardButton(text=f"{i[1]}", callback_data=f"getdata_{i[0]}"))

    await message.answer("Выберите товар", reply_markup=keyboard)

@dp.message_handler(Text(equals="Художественная литература"))
async def category_2(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    global products

    products = dbase_prod.get_items_names()
    for i in products:
        if Text(i[5]).equals == Text(message.text).equals:
            keyboard.add(types.InlineKeyboardButton(text=f"{i[1]}", callback_data=f"getdata_{i[0]}"))

    await message.answer("Выберите товар", reply_markup=keyboard)


#@dp.message_handler(Text(equals="Ассортимент товаров"))
#async def products_range(message: types.Message):
#    keyboard = types.InlineKeyboardMarkup()
#    global products
#
#    products = dbase.all_items_names()
#
#    for i in products:
#        keyboard.add(types.InlineKeyboardButton(text=f"{i[1]}", callback_data=f"getdata_{i[0]}"))
#
#    await message.answer("Выберите товар", reply_markup=keyboard)




@dp.callback_query_handler(Text(startswith="getdata"))
async def send_data(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()

    data = int(call.data.split("_")[1])
    description = products[data-1][2]
    bill = p2p.bill(amount=products[data-1][4], lifetime=5, comment='')
    imgPath = products[data-1][3]
    pic = types.InputFile(f"./img/{imgPath}")
    keyboard.add(types.InlineKeyboardButton(text="Купить", url=bill.json['payUrl']))

    await bot.send_photo(call.from_user.id, pic)
    await call.message.answer(description, reply_markup=keyboard)
#    await call.message.answer(bill.json['payUrl'])

    await call.answer()


if __name__ == '__main__':
    ##sum = 0.00 # сумма платежа в рублях
    ##time = 60 # время жизни счета в минутах
    ##comment = 'TEST' # комментарий
    #create_db()
    ##database.create_db()  # Создание бд и подключение к ней
    #input_data()  # Расскоментить для ввода данных из файла input.txt

    dbase_prod.create_db(db_products, "sq_db_items.sql")
    #dbase_prod.input_data("input.txt")

    executor.start_polling(dp)

    ##bill = p2p.bill(amount=sum, lifetime=time, comment=comment)
    ##print(bill.json['payUrl'])