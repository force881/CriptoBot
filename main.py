import logging
from aiogram import Bot,Dispatcher,executor,types
from aiogram.types import callback_game
from pycoingecko import CoinGeckoAPI
import config 
import markups as nav

logging.basicConfig(level = logging.INFO)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)
cg = CoinGeckoAPI()

@dp.message_handler(commands=['start'])
async def start(messege: types.Message):
    if messege.chat.type == 'private':
        await bot.send_message(messege.from_user.id, 'Выберете крипто валюту:', reply_markup=nav.crupto_list)


@dp.message_handler()
async def bot_message(message: types.Message):
    if message.chat.type == 'private':
        result = cg.get_price(ids=message.text, vs_currencies='usd')
        await bot.send_message(message.from_user.id, f"Криптовалюта: {message.text}\nСтоимость на данный момент: {result[message.text]['usd']} $",reply_markup=nav.crupto_list)


@dp.callback_query_handler(text_contains='cc_')
async def crupto(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    callback_data = call.data
    currency = str(callback_data[3:])
    result = cg.get_price(ids=currency, vs_currencies='usd')
    await bot.send_message(call.from_user.id, f"Криптовалюта: {currency}\nСтоимость на данный момент: {result[currency]['usd']} $",reply_markup=nav.crupto_list)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)