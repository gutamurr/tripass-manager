from aiogram import Bot, Dispatcher, executor, types
import logging
import sqlite3

from settings import API_KEY
import markups as mrk
import messages as msg

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_KEY, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

con = sqlite3.connect("database/passwords.db")
cur = con.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER,
            GooglePassword TEXT, MicrosoftPassword TEXT, DiscordPassword TEXT, GitHubPassword TEXT, SpotifyPassword)""")
con.commit()

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await bot.send_message(message.chat.id, msg.start_text, reply_markup=mrk.StartCommands)

    global people_id
    people_id = message.from_user.id
    cur.execute(f"SELECT id FROM users WHERE id = {people_id}")
    if cur.fetchone() is None:
        user_id = [message.from_user.id]
        cur.execute("INSERT INTO users (id) VALUES(?)", user_id)
        con.commit()
    else:
        pass

def AddPasswords(service, password, people_id):
            cur.execute(f"""UPDATE users SET {service} = "{password}" WHERE id = {people_id}""")
            con.commit()

@dp.callback_query_handler(text = ["SetPasswordToBD", "SendTheList", "ToBack"])
async def StartCommands(call: types.CallbackQuery):
    if call.data == "SetPasswordToBD":
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await call.message.answer(msg.setpassmenu_text, reply_markup=mrk.Back)

    elif call.data == "SendTheList":
        await bot.delete_message(call.from_user.id, call.message.message_id)
        people_id = call.message.from_user.id

        gpass = str(cur.execute(f'SELECT GooglePassword FROM users WHERE id = {people_id}').fetchone())
        mpass = str(cur.execute(f'SELECT MicrosoftPassword FROM users WHERE id = {people_id}').fetchone())
        dpass = str(cur.execute(f'SELECT DiscordPassword FROM users WHERE id = {people_id}').fetchone())
        ghpass = str(cur.execute(f'SELECT GitHubPassword FROM users WHERE id = {people_id}').fetchone())
        spass = str(cur.execute(f'SELECT SpotifyPassword FROM users WHERE id = {people_id}').fetchone())

        passlist = f"Your Google password: <b>{gpass}</b>,\nYour Microsoft password: <b>{mpass}</b>,\nYour Discord password: <b>{dpass}</b>,\nYour GitHub password: <b>{ghpass}</b>,\nYour Spotify password: <b>{spass}</b>"
        await call.message.answer(passlist, reply_markup=mrk.Back)

    elif call.data == "ToBack":
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await call.message.answer(msg.start_text, reply_markup=mrk.StartCommands)

@dp.message_handler(commands=['google'])
async def echo(message: types.Message):
    arguments = message.get_args()
    AddPasswords(service="GooglePassword", password=f"{arguments}", people_id=message.from_user.id)
    await message.reply("<b>Your password has been add to database.</b>", reply_markup=mrk.Back)

@dp.message_handler(commands=['microsoft'])
async def echo(message: types.Message):
    arguments = message.get_args()
    AddPasswords(service="MicrosoftPassword", password=f"{arguments}", people_id=message.from_user.id)
    await message.reply("<b>Your password has been add to database.</b>", reply_markup=mrk.Back)

@dp.message_handler(commands=['discord'])
async def echo(message: types.Message):
    arguments = message.get_args()
    AddPasswords(service="DiscordPassword", password=f"{arguments}", people_id=message.from_user.id)
    await message.reply("<b>Your password has been add to database.</b>", reply_markup=mrk.Back)

@dp.message_handler(commands=['github'])
async def echo(message: types.Message):
    arguments = message.get_args()
    AddPasswords(service="GitHubPassword", password=f"{arguments}", people_id=message.from_user.id)
    await message.reply("<b>Your password has been add to database.</b>", reply_markup=mrk.Back)

@dp.message_handler(commands=['spotify'])
async def echo(message: types.Message):
    arguments = message.get_args()
    AddPasswords(service="SpotifyPassword", password=f"{arguments}", people_id=message.from_user.id)
    await message.reply("<b>Your password has been add to database.</b>", reply_markup=mrk.Back)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)