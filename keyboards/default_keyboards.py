from telebot import types


start_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1, resize_keyboard=True).add(types.KeyboardButton('🟩 Пройти опрос 🟩'))

question1_btns = [types.KeyboardButton('Не интересует'), 
                    types.KeyboardButton('Когда давали задачи на уроках – решал, но самостоятельно никогда не интересовался'), 
                    types.KeyboardButton('Немного заинтересован, любопытно следить за новыми технологиями в IT-индустрии'),
                    types.KeyboardButton('Заинтересован. Проходил/прохожу курсы, читал/читаю книги и практикуюсь')
                ]
first_question_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1, resize_keyboard=True).add(*question1_btns)