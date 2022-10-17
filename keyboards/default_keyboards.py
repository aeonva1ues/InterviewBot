from telebot import types

hide_keyboard = types.ReplyKeyboardRemove()
start_keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)\
    .add(types.KeyboardButton('🟩 Пройти опрос 🟩'))

question1_btns = [
    types.KeyboardButton('Не интересует'), 
    types.KeyboardButton(
        (
            'Когда давали задачи на уроках – решал, '
            'но самостоятельно никогда не интересовался'
        )
    ),
    types.KeyboardButton(
        (
            'Немного заинтересован, '
            'любопытно следить за новыми технологиями в IT-индустрии'
        )
        ),
    types.KeyboardButton(
        (
            'Заинтересован. '
            'Проходил/прохожу курсы, читал/читаю книги и практикуюсь'
        )
        )
                ]
first_question_keyboard = types.ReplyKeyboardMarkup(row_width=1,
                                                    resize_keyboard=True)\
                                                        .add(*question1_btns)

question21_btns = [
    types.KeyboardButton('Нет, только слышал название'),
    types.KeyboardButton('Перечислил несколько, но практиковался не на всех'),
    types.KeyboardButton('Да')
        ]
second_more_question_keyboard = types.ReplyKeyboardMarkup(
    row_width=1, resize_keyboard=True).add(*question21_btns)


question3_btns = [
    types.KeyboardButton('Никак, их нет'),
    types.KeyboardButton('Очень слабые знания, не дотягиваю до базы'),
    types.KeyboardButton('Понимаю основы, так называемую базу'),
    types.KeyboardButton('Могу решать сложные задачи с уроков/олимпиад'),
    types.KeyboardButton(
        (
            'Могу уверенно писать код для решения задач конкретного '
            'направления (backend, frontend, data science и др.)'
        )
    )
    ]
third_question_keyboard = types.ReplyKeyboardMarkup(
    row_width=1, resize_keyboard=True).add(*question3_btns)


question4_btns = [
    types.KeyboardButton(
        ('Ничего не понимаю в этом. Информация из учебников '
            '/ от учителя доходит до меня с трудом')
    ),
    types.KeyboardButton(
        'Частичное понимание имею, но на уроках это скучно для меня'
    ),
    types.KeyboardButton(
        'Понимаю темы, которые мы изучаем. На уроках мне интересно'
    ),
    types.KeyboardButton(
        ('Я заинтересован, однако часто разочаровываюсь от того, '
            'как мы изучаем это на уроках')
    ),
    types.KeyboardButton(
        'Мне интересны другие языки программирования. В школе мы их не изучали'
    ),
    types.KeyboardButton(
        ('Мне интересна другая подача информации. Например, из книг, '
            'написанных программистами или из курсов')
    ),
    types.KeyboardButton(
        'Мне интересны задачи для практики совершенно другого плана'
        ),
    ]
fourth_question_keyboard = types.ReplyKeyboardMarkup(
    row_width=1, resize_keyboard=True).add(*question4_btns)


question5_btns = [
    types.KeyboardButton('Да'),
    types.KeyboardButton('Рассматриваю этот вариант'),
    types.KeyboardButton('Нет')
]
fifth_question_keyboard = types.ReplyKeyboardMarkup(
    row_width=1, resize_keyboard=True).add(*question5_btns)
