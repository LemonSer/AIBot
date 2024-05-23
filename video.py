import requests
from aiogram import Bot, Dispatcher, types, executor

API_TOKEN = '7138631637:AAEnYvqdaFaAFz7ehzjnzEyo6RqK978pCAE'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message: types.Message):
  await message.reply('Привет, я нейроконсультант, который может помочь тебе подготовиться к ДНД. Напиши, что за враг напал на вашу команду и его локацию...')

async def get_response(message_text):
  prompt = {
    "modelUri": "gpt://b1go1t8vie998tqjdjhu/yandexgpt-lite",
    "completionOptions": {
      "stream": False,
      "temperature": 0.5,
      "maxTokens": "2000"
    },
    "messages": [
      {
        "role": "system",
        "text": "Ты - мастер подземелий проводящий сессию для игроков в колличестве 3 человек. Имитируй встречу с врагом, с которым столкнуться игроки на указанной локации, опиши способности и возможные атаки врага. Твоя задача - описать способности и атаки врага с цифрами урона и возможный исход встречи игроков с ним.  Сгенерируй битву игроков и врага."
  },
      {
        "role": "user",
        "text": message_text
      }
    ]
  }

  url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
  headers = {
    "Content-Type": "application/json",
    "Authorization": "API-Key AQVN0pDgU51dizMQvGEQnOj4ce4BPJyMBxzdRm9P"
  }

  response = requests.post(url, headers=headers, json=prompt)
  result = response.json()
  return result['result']['alternatives'][0]['message']['text']

@dp.message_handler()
async def analize_message(message: types.Message):
  response_text = await get_response((message.text))
  await message.answer(response_text)

if __name__ == '__main__':
  executor.start_polling(dp, skip_updates= True)
