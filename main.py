import telebot
from bot_logic import gen_pass, gen_emodji, flip_coin
from telebot.types import BotCommand
import os
import random
import requests

bot = telebot.TeleBot("")

bot.set_my_commands([
    BotCommand("start", "Запуск бота"),
    BotCommand("hello", "Здоровается с вами"),
    BotCommand("bye", "Прощается с вами"),
    BotCommand("pass", "Cгенерирует пароль длиной от 1 до 15"),
    BotCommand("emodji", "Отправит любой эмоджи"),
    BotCommand("coin", "Игра в монетку"),
    BotCommand("heh", "Смеется заданное количество раз"),
    BotCommand("mem", "Отправит мем про программирование"),
    BotCommand("duck", "Отправит изображение с уткой"),
    BotCommand("fox", "Отправит изображение с лисой"),
    BotCommand("dog", "Отправит изображение с собакой"),
    BotCommand("cat", "Отправит изображение с кошкой"),
    BotCommand("games", "Тематический блок с рандомными играми"),
    BotCommand("animals", "Тематический блок с рандомными изрбражениями животных"),
    BotCommand("fun", "Тематический блок с веселыми командами"),
    BotCommand("utils", "Тематический блок с полезными командами")
    
])

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я твой Telegram бот.У меня есть такие команды как:/hello, /bye, /pass, /emodji , /coin, /heh, /mem и многие другие")

@bot.message_handler(commands=['hello'])
def send_hello(message):
    bot.reply_to(message, "Привет! Как дела?")
    
@bot.message_handler(commands=['bye'])
def send_bye(message):
    bot.reply_to(message, "Пока! Удачи!")

@bot.message_handler(commands=['pass'])
def ask_password_length(message):
    msg = bot.reply_to(message, "Укажите длину пароля (число от 1 до 15):")
    bot.register_next_step_handler(msg, process_password_length)
def process_password_length(message):
    try:
        length = int(message.text)
        if length < 1:
            length = 1
        elif length > 15:
            length = 15
        password = gen_pass(length)
        bot.reply_to(message, f"Вот твой сгенерированный пароль длиной {length} символов: {password}")
    except ValueError:
        bot.reply_to(message, "Пожалуйста, введите число от 1 до 15. Попробуйте снова командой /pass")

@bot.message_handler(commands=['emodji'])
def send_emodji(message):
    emodji = gen_emodji()
    bot.reply_to(message, f"Вот эмоджи': {emodji}")

@bot.message_handler(commands=['coin'])
def send_coin(message):
    coin = flip_coin()
    bot.reply_to(message, f"Монетка выпала так: {coin}")

@bot.message_handler(commands=['heh'])
def send_heh(message):
        count_heh = int(message.text.split()[1]) if len(message.text.split()) > 1 else 5
        bot.reply_to(message, "he" * count_heh)



@bot.message_handler(commands=['mem'])
def send_mem(message):
    s =os.listdir("images")
    s =random.choice(s)
    with open(f'images/{s}', 'rb') as f:  
        bot.send_photo(message.chat.id, f)  


def get_duck_image_url():    
        url = 'https://random-d.uk/api/random'
        res = requests.get(url)
        data = res.json()
        return data["url"]
@bot.message_handler(commands=['duck'])
def duck(message):
        image_url = get_duck_image_url()
        bot.reply_to(message, image_url)
def get_dog_image_url():    
        url = "https://random.dog/woof.json"
        res = requests.get(url)
        data = res.json()
        return data["url"]

@bot.message_handler(commands=['dog'])
def dog(message):
        image_url = get_dog_image_url()
        bot.reply_to(message, image_url)
def get_fox_image_url():    
        url = "https://randomfox.ca/floof/"
        res = requests.get(url)
        data = res.json()
        return data["image"]
    
    
@bot.message_handler(commands=['fox'])
def fox(message):
        image_url = get_fox_image_url()
        bot.reply_to(message, image_url)


def get_cat_image_url():    
        url = "https://api.thecatapi.com/v1/images/search"
        res = requests.get(url)
        data = res.json()
        return data[0]['url']
    
    
@bot.message_handler(commands=['cat'])
def cat(message):
        image_url = get_cat_image_url()
        bot.reply_to(message, image_url)

@bot.message_handler(commands=['animals'])
def random_animal(message):
    animal_commands = ['duck', 'fox', 'dog', 'cat']
    chosen_command = random.choice(animal_commands)

    if chosen_command == 'duck':
        duck(message)
    elif chosen_command == 'fox':
        fox(message)
    elif chosen_command == 'dog':
        dog(message)
    elif chosen_command == 'cat':
        cat(message)

@bot.message_handler(commands=['fun'])
def random_fun(message):
    fun_commands = ['heh',  'mem']
    chosen_command = random.choice(fun_commands)
    
    if chosen_command == 'heh':
        send_heh(message)
    
    elif chosen_command == 'mem':
        send_mem(message)

@bot.message_handler(commands=['games'])
def random_game(message):
    game_commands = ['coin' ]
    chosen_command = random.choice(game_commands)
    
    if chosen_command == 'coin':
        send_coin(message)
    

@bot.message_handler(commands=['utils'])
def random_util(message):
    util_commands = ['pass', 'emodji']
    chosen_command = random.choice(util_commands)
    
    if chosen_command == 'pass':
        ask_password_length(message)
    elif chosen_command == 'emodji':
        send_emodji(message)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
        bot.reply_to(message, message.text)


def recognize(image_path,labels_path):
  with open(labels_path, "r") as f:
    class_names = [line.strip() for line in f.readlines()]


  # Обрабатываем изображение
  image = Image.open(image_path).convert("RGB")
  image = ImageOps.fit(image, (224, 224), Image.Resampling.LANCZOS)
  image_array = np.asarray(image, dtype=np.float32)
  normalized_image = (image_array / 127.5) - 1
  data = np.expand_dims(normalized_image, axis=0)

  # Предсказание
  prediction = model.predict(data, verbose=0)
  index = np.argmax(prediction)
  class_name = class_names[index]
  confidence_score = float(prediction[0][index])

  # Вывод результатов
  result_class = class_name[2:].strip() if len(class_name) > 2 else class_name.strip()


  return (result_class, confidence_score)


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    if not message.photo:
        bot.reply_to(message, 'дай фото ')
    file_info = bot.get_file(message.photo[-1].file_id)
    file_name = file_info.file_path.split('/')[-1]
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)
    result = recognize(file_name, '/content/labels.txt')
    bot.reply_to(message, result)






bot.polling()
