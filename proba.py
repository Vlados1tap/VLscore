import telebot
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.web_app_info import WebAppInfo

API_KEY = Bot('5888195540:AAG3rFeJiHwh4qogIwFndWKoONzkKbgFnlU')

dp = Dispatcher(API_KEY)

@dp.message_handler(commands=["start"])
async def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item4 = types.KeyboardButton("О  боте❓")
    item5 = types.KeyboardButton("Анализ расходов")
    item6 = types.KeyboardButton("Открыть веб приложение", web_app=WebAppInfo(url="https://github.com/Vlados1tap/xtmls/blob/main/UGA.py"))

    markup.add(item4, item5, item6)

    await message.answer("Привет, {0.first_name}.".format(message.from_user), reply_markup=markup)




@dp.message_handler(content_types=["text"])
async def states(message):
    if message.chat.type == "private":
        if message.text == "О боте❓":

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton("🔙 Назад")
            markup.add(back)
            await message.answer("--", reply_markup=markup)

        elif message.text == "Анализ расходов":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton("🔙 Назад")
            markup.add(back)
            await message.answer(message.chat.id,
                             "Анализ доступен по следующим категориям:",
                             reply_markup=markup)

        elif message.text == "🔙 Назад":

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item4 = types.KeyboardButton("О боте❓")
            item5 = types.KeyboardButton("Анализ расходов")
            markup.add(item4, item5)
            await message.answer(message.chat.id, "Вы перешли в главное меню!", reply_markup=markup)
        elif message.text == "Готово":

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton("🔙 Назад")
            markup.add(back)
            await message.answer(message.chat.id, "авфы", reply_markup=markup)

        elif message.text == "###":
            await message.answer(message.chat.id, "try again", parse_mode="html")


executor.start_polling(dp)
