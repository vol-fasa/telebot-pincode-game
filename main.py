import telebot
import random

class GameState:
    Greeting = 0
    FirstStep = 1
    Gaming = 2
    Finish = 3

bot = telebot.TeleBot('1245580645:AAEthpcxS9D8BzLKVlPAgRktLd5xi3jdE8U')

d = {}

def pinCode2(N):
  r = []
  digits = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
  for i in range(0, N):
    idx = random.randint(0, len(digits) - 1)
    r.append(digits[idx])
    digits.remove(digits[idx])
  return r


def pincodeToArray(info):
    array = []
    for i in info:
      i = int(i)
      array.append(i)
    return array


def calcEquals(text, massiv):
  d = 0
  b = 0
  array = pincodeToArray(text)
  for i in range(len(array)):
    if array[i] == massiv[i]:
      d = d + 1
    elif massiv[i] in array:
      b = b + 1
  return d, b


@bot.message_handler(commands=['start'])
def start_message(message):
  global d
  d[message.chat.id] = {'state': GameState.FirstStep, 'count': 1, 'pincode': None, 'length': 0}

  print(d[message.chat.id]['state'])
  bot.send_message(message.chat.id, 'В этой игре я загадываю пин-код, а ты должен(а) его отгадать. Я буду говорить сколько цифр присутствуют в коде и стоят на своих местах, и сколько цифр присутствуют в коде, но стоят не на своих местах.  ')
  bot.send_message(message.chat.id, 'Если вы вдруг захотите выйти из игры тогда скажите Стоп')
  bot.send_message(message.chat.id, 'Пришли мне сколько цифр должно быть в пинкоде (от 1 до 9)?')


@bot.message_handler(content_types=['sticker'])
def start_message(message):
  bot.send_sticker(message.chat.id, message.sticker.file_id)


@bot.message_handler(content_types=['text'])
def send_text(message):
  global d

  if d.get(message.chat.id) == None:
    bot.send_message(message.chat.id, 'Для начала игры пришли мне команду /start ')
    return

  if message.text.lower() == 'стоп':
    bot.send_message(message.chat.id, 'Хорошо, игра закончилась.')
    d[message.chat.id]['state'] = GameState.Greeting
    return

  if d[message.chat.id]['state'] == GameState.FirstStep:
    flag = message.text.isdigit()
    num = -1
    if flag:
      num = int(message.text)


    if flag and 1 <= num <= 9:
      d[message.chat.id]['pincode'] = pinCode2(num)
      d[message.chat.id]['state'] = GameState.Gaming
      d[message.chat.id]['length'] = num
      bot.send_message(message.chat.id,'Пожалуйста, пришлите мне пинкод.')

    else:
      bot.send_message(message.chat.id, 'Ты прислал мне не то. Пожалуйста, пришли мне сколько цифр должно быть в пинкоде (от 1 до 9)!')
      print(d)

  elif d[message.chat.id]['state'] == GameState.Gaming:

    if len(message.text) != d[message.chat.id]['length'] or not message.text.isdigit():
      bot.send_message(message.chat.id, 'Ты прислал что-то не то ')

    else:
      result = calcEquals(message.text, d[message.chat.id]['pincode'])

      if result[0] == d[message.chat.id]['length'] :
        d[message.chat.id]['state'] = GameState.Greeting
        bot.send_message(message.chat.id, 'Вы отгадали пинкод')
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIFel77Z6yJpkzkt6ImPLkJJlykZ5l5AAJNAANZu_wlKIGgbd0bgvcaBA')
        bot.send_message(message.chat.id, 'Пинкод был отгадан за {} попытки. Чтобы сыграть снова скажи /start'.format(d[message.chat.id]['count']))

      elif len(message.text) == d[message.chat.id]['length'] and message.text.isdigit():
        d[message.chat.id]['count'] = d[message.chat.id]['count']+1
        bot.send_message(
          message.chat.id,
          '\[ *{}* ] цифр верны и стоят на своих местах\n\[ *{}* ] цифр верны, но не на своем месте'.format(result[0], result[1]),
          None, None, None, 'Markdown'
        )

bot.polling()

