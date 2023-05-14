from aiogram import Bot, types, Dispatcher, executor
from aiogram.types import InlineKeyboardMarkup, \
    InlineKeyboardButton
import sqlite3
import datetime as dt
from Vk import search_group
import asyncio

from config import load_BOT
from app import app

TG_TOKEN = load_BOT(app.root_path)


def bd_record(id, id_first, id_last, group_id, now, group_name):
    conn = sqlite3.connect(app.config['DATABASE'])
    cur = conn.cursor()
    print(f"SELECT * FROM users WHERE id_group =={group_id};")
    cur.execute(f"SELECT * FROM users WHERE id_group =={group_id};")
    one_result = cur.fetchone()
    if one_result:
        return 'Вы уже подписаны на группу ' + group_name
    else:
        cur.execute("""INSERT INTO users(id, first, last, id_group, sub_date, name_group) VALUES (?,?,?,?,?,?);""",
                    (id, id_first, id_last, group_id, now, group_name))
        conn.commit()
    return 'Группа ' + group_name + ' добавлена в базу данных'


# xcv
def bd_read(id):
    conn = sqlite3.connect(app.config['DATABASE'])
    cur = conn.cursor()
    cur.execute(f"SELECT sub_date, name_group, id_group FROM users WHERE id == {id};")
    result = cur.fetchall()
    if result:
        return result
    else:
        return None


# bot init
PROXY_URL = "http://167.235.144.131:8080"

#bot = Bot(proxy=PROXY_URL, token=TG_TOKEN)
bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot)

btn_search = InlineKeyboardButton('Начать поиск!😁', callback_data='btn_search')
btn_help = InlineKeyboardButton('Помогите😥', callback_data='btn_help')
btn_group = InlineKeyboardButton('Мои подписки', callback_data='btn_group')
btn_all_user = InlineKeyboardButton('Все пользовтели', callback_data='btn_all_user')
btn_id_user = InlineKeyboardButton('Подписки пользователя', callback_data='btn_id_user')

# add inline buttons([help], [start searching]) to inline keyboard
keyboard_help_search = InlineKeyboardMarkup(resize_keyboard=True).add(btn_search, btn_group, btn_all_user, btn_id_user,
                                                                      btn_help)


# command processing(start)
@dp.message_handler(commands=['start'])
async def process_start(msg: types.Message):
    await msg.answer('Привет!👋\n'
                     'Я бот, который ищет по вашему запросу группы в социальной сети Вконтакте\n'
                     'и подписывается на их новости😎.Внимание база данных не обновляется на сайте, посколько'
                     'используется sqlite, а файловая система на heroku не постоянная',
                     reply_markup=keyboard_help_search)


# answer for button help
@dp.callback_query_handler(text='btn_help')
async def process_callback_btn_help(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id,
                           'Здраствуйте! ' + callback_query.from_user.first_name + ' ' \
                           + callback_query.from_user.last_name + ' это тестовый бот для поиска групп и новостей')
    await bot.send_message(callback_query.from_user.id, 'Выберите действие в меню', reply_markup=keyboard_help_search)


# answer for bd
@dp.callback_query_handler(text='btn_all_user')
async def process_callback_btn_all_user(callback_query: types.CallbackQuery):
    conn = sqlite3.connect(app.config['DATABASE'])
    cur = conn.cursor()
    cur.execute(f"SELECT DISTINCT id, first, last FROM users")
    result = cur.fetchall()
    if result:
        await bot.send_message(callback_query.from_user.id, 'Зарегистрированы следующие пользователи')
        for i in result:
            s = 'ID пользователя  ' + str(i[0]) + ' Имя: ' + i[1] + ' Фамилия: ' + i[2]
            await bot.send_message(callback_query.from_user.id, s)
        await bot.send_message(callback_query.from_user.id, "Продолжаем", reply_markup=keyboard_help_search)

    else:
        await bot.send_message(callback_query.from_user.id, 'База данных пуста')


# answer for id_user
@dp.callback_query_handler(text='btn_id_user')
async def process_callback_id_user(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'Введите id пользователя')

    @dp.message_handler()
    async def process_id(msg: types.Message):
        id = msg.text
        res = bd_read(id)
        if res is None:
            await bot.send_message(callback_query.from_user.id, 'Такого пользователя нет')
        else:
            await bot.send_message(callback_query.from_user.id, 'У вас следующие подписки')
            for i in res:
                date = dt.datetime.fromisoformat(i[0])
                s = 'Группа ' + i[1] + f" https://vk.com/public{i[2]}" + '\n дата подписки ' + str(date)
                await bot.send_message(callback_query.from_user.id, s)
            await bot.send_message(callback_query.from_user.id, "Продолжаем", reply_markup=keyboard_help_search)
            pass


# answer for button group
@dp.callback_query_handler(text='btn_group')
async def process_callback_btn_group(callback_query: types.CallbackQuery):
    id = callback_query.from_user.id
    res = bd_read(id)
    if res is None:
        await bot.send_message(callback_query.from_user.id, 'Вы не подписаны ни на одну группу ')
    else:
        await bot.send_message(callback_query.from_user.id, 'У вас следующие подписки')
        for i in res:
            date = dt.datetime.fromisoformat(i[0])
            s = 'Группа ' + i[1] + f" https://vk.com/public{i[2]}" + '\n дата подписки ' + str(date)
            await bot.send_message(callback_query.from_user.id, s)
        await bot.send_message(callback_query.from_user.id, "Продолжаем", reply_markup=keyboard_help_search)
        pass


# answer for button search
@dp.callback_query_handler(text='btn_search')
async def process_callback_btn_search(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'Давай начнем!😊\n'
                                                        'Введи любой запрос,\n'
                                                        'а я поищу похожие группы во Вконтакте🙃.')

    # search groups
    @dp.message_handler()
    async def process_search(msg: types.Message):
        groups = search_group(msg)
        # name_ids = json.load(open('name_ids.json'))
        # print(name_ids)
        all_id = []

        # add inline keyboard for founded groups
        keyboard_groups = InlineKeyboardMarkup(resize_keyboard=True)

        if len(groups) != 0:
            await msg.answer('Нашлось несколько групп для тебя😉.')
            for group in groups:
                group_name = group['name']
                id = group['id']
                # name_ids.update({id: group_name})
                all_id.append(str(id))
                await msg.answer(f"{group_name}\n"
                                 f"https://vk.com/public{id}")
                button_group = InlineKeyboardButton(group_name, callback_data=str(id))
                keyboard_groups.insert(button_group)
            # choose the groups
            await msg.answer('Выбери группу(-ы), на новости которой(-ых) ты хотел бы подписаться😉.',
                             reply_markup=keyboard_groups)

            @dp.callback_query_handler(text=all_id)
            async def process_callback_group(callback_query: types.CallbackQuery):
                usr_id = str(callback_query.from_user.id)
                id_first = callback_query.from_user.first_name
                id_last = callback_query.from_user.last_name
                group_id = int(callback_query['data'])
                name_group = ''.join([x['name'] for x in groups if x['id'] == group_id])
                now = dt.datetime.now().replace(second=0, microsecond=0).isoformat()
                await msg.answer(bd_record(usr_id, id_first, id_last, group_id, now, name_group))
                await msg.answer('продолжим', reply_markup=keyboard_help_search)

        # not find groups
        else:
            await msg.answer('Не могу найти ни одной группы с таким названием🤔...')
            await msg.answer('Выберите действие в меню', reply_markup=keyboard_help_search)


# main program
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    executor.start_polling(dp, skip_updates=True)
