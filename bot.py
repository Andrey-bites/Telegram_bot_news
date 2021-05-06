import config
import logging
from aiogram import Bot, Dispatcher, executor, types
from sqliter3 import Sqlighter

# задаём уровень логов
logging.basicConfig(level=logging.INFO)

# инициализируем бота
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)

# инициализируем соединение с БД
db = Sqlighter('db.db')


# команда активации подписки
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if(not db.subscriber_exists(message.from_user.id)):
        # если юзера нет добавляем его
        db.add_subscriber(message.from_user.id)
    else:
        # если есть, обновляем статус подписки
        db.update_subscription(message.from_user.id, True)

    await message.answer('Вы успешно подписались на  рассылку \n Скоро выйдут новые обзоры и вы узнаете о них 1-ый')


@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    if(not db.subscriber_exists(message.from_user.id)):
        # если юзера нет добавляем его с неактивной подпиской (запоминаем)
        db.add_subscriber(message.from_user.id, False)
        await message.answer('Вы и так не подписаны')
    else:
        # если он уже есть то просто обноваляем ему статус подписки
        db.update_subscription(message.from_user.id, False)
        await message.answer('Вы успешно отписаны!!')


# запускаем лонг поллинг
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
