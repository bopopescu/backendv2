from telebot import  types

keyboard_1 = types.InlineKeyboardMarkup(row_width= 3)
s1 = types.InlineKeyboardButton (text= "Рейтинг", callback_data="rating")
s2 = types.InlineKeyboardButton (text= "Личный кабинет", callback_data="login")

keyboard_1.add(s1, s2)

keyboard_2 = types.InlineKeyboardMarkup(row_width= 3)
s3 = types.InlineKeyboardButton (text= "Рейтинг", callback_data="rating")
s4 = types.InlineKeyboardButton (text= "Выйти", callback_data="logout")

keyboard_2.add(s3, s4)