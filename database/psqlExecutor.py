from datetime import datetime
import psycopg2
import argparse


# Значения бд по умолчанию
db_properties = {'database': 'test_db_tg', 
                    'user': "postgres", 
                    'password': '12345', 
                    'host': 'localhost', 
                    'port': '5432'}
# Свойства базы данных берутся из файла "db_properties.txt"
try:
    with open('database/db_properties.txt', 'r', encoding='utf-8') as properties:
        content = properties.read()
except FileNotFoundError:
    # Если файл с свойствами был не найден, то продолжить с значениями по умолчанию
    content = ''

if content:
    arg_lines = content.split('\n')
    if len(arg_lines) >= 5: 
        for arg_line in arg_lines:
            key, value = arg_line.split(':')
            if key.strip() == 'database':
                db_properties['database'] = value.strip()
            if key.strip() == 'user':
                db_properties['user'] = value.strip()
            if key.strip() == 'password':
                db_properties['password'] = value.strip()
            if key.strip() == 'host':
                db_properties['host'] = value.strip()
            if key.strip() == 'port':
                db_properties['port'] = value.strip()
    else:
        print('''Вероятно, содержимое файла db_properties.txt было изменено и было удалено обязательное поле
        \nКод будет выполнен с настройками по умолчанию.''')


def connect_db(sql_query_func):
    # Функция-декоратор. Осуществляет подключение к базе данных с последующим исполнением запроса из 
    # декорируемой функции
    global db_properties
    def do_sql_func(sql_query):
        con = psycopg2.connect(database=db_properties['database'], 
                            user=db_properties['user'], 
                            password=db_properties['password'], 
                            host=db_properties['host'], 
                            port=db_properties['port'])
        cur = con.cursor() 
        cur.execute(sql_query_func(sql_query))
        try:
            res = cur.fetchall()
        except (Exception, psycopg2.Error) as error:
            res = None
        finally:
            con.commit() 
            con.close()
            return res
     
    return do_sql_func


# =====================================================
# Все доступные функции для работы с БД
@connect_db
def create_table(table_name):
    # Структура таблицы заранее определена. 
    # Намеренно нарушено первое правило нормализации. Нет необходимости выносить ответы пользователя в отдельную таблицу,
    # поскольку в дальнейшем это лишь усложнит работу.
    assert __name__ == '__main__', 'Создание таблицы возможно только с помощью консольного запуска с аргументом'
    print('Запрос на создание таблицы сделан успешно. Проверьте базу данных.')
    return f'''CREATE TABLE {table_name}  
                (id SERIAL PRIMARY KEY,
                user_tg_id CHAR(150) NOT NULL,
                answer1 CHAR(150) NOT NULL,
                answer2 CHAR(150) NOT NULL,
                answer21 CHAR(150),
                answer3 CHAR(150) NOT NULL,
                answer4 CHAR(150) NOT NULL,
                answer41 TEXT,
                answer5 CHAR(150) NOT NULL,
                completion_date TIMESTAMP WITHOUT TIME ZONE NOT NULL);'''

@connect_db
def insert_into(values: dict):
    assert len(values) == 10, 'Некорректно указаны аргументы SQL запроса'
    print('Запрос на создание записи отправлен успешно. Проверьте базу данных.')
    return f"INSERT INTO {values['table_name']} (user_tg_id, answer1, answer2, answer21, answer3, answer4, answer41, answer5, completion_date) VALUES ('{values['tg_id']}', '{values['a1']}', '{values['a2']}', '{values['a21']}', '{values['a3']}', '{values['a4']}', '{values['a41']}', '{values['a5']}', '{values['date']}') RETURNING id;"

@connect_db
def search_user(values: dict):
    # Ищет пользователя по его ид
    return f"SELECT * FROM {values['table_name']} WHERE user_tg_id = '{values['user_id']}'"
# =====================================================


if __name__ == '__main__':
    # Если запущен через консоль с аргументом --newtable, то создаст новую таблицу
    parser = argparse.ArgumentParser()
    parser.add_argument("--newtable")
    args = parser.parse_args()
    if args.newtable:
        create_table(args.newtable)
        with open('database/db_properties.txt', 'r', encoding='utf-8') as properties:
            content = properties.read().split('\n')
            content = [f'{x}\n' for x in content]
        for i in range(len(content)):
            if content[i].startswith('active_table'):
                content[i] = f'active_table: {args.newtable}'
                with open('database/db_properties.txt', 'w', encoding='utf-8') as properties:
                    properties.writelines(content)
    else:
        print('''Используйте: "python psqlExecutor.py --tablename NAME" для создания таблицы.\n
        Остальные функции доступны при импорте.
        ''')