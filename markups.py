from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# START MESSAGE INLINE TEXT
OpenSource = InlineKeyboardButton(text="GitHub 🌐", url="https://github.com/gutamurr")
SetPassword = InlineKeyboardButton(text="Set Passwords 🔐", callback_data="SetPasswordToBD")
SendThePassList = InlineKeyboardButton(text="Send Passwords List 📃", callback_data="SendTheList")
StartCommands = InlineKeyboardMarkup(row_width=2).add(OpenSource, SetPassword, SendThePassList)

BackButton = InlineKeyboardButton(text="Back ↩", callback_data="ToBack")
Back = InlineKeyboardMarkup().add(BackButton)