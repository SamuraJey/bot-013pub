import random
from datetime import datetime, date
import requests
import vk_api
from num2words import num2words
from vk_api.longpoll import VkLongPoll, VkEventType

# Различные словари для ответов бота
goodbye = ["пока", "пока-пока", "возвращайся скорее", "прощай", "до скорых встреч", "асталависта", "до свидания",
           "до новых встреч"]

hello = ["приветствую", "здравствуй", "привет", "привет-привет", "проходи не задерживайся", "хай", "давно не виделись",
         "ты смотри кто к нам колеса катит, Привет"]

who_are_you = ['кто ты?', "что ты?", "кто твой создатель?", 'кто ты', "что ты", "кто твой создатель",
               "ты робот?", "ты бот?"]

n_help = ["помощь", "что ты умеешь?", "команды", "список команд", "что ты умеешь",
          "в чем твоя польза?", "в чём твоя польза?", "в чем твоя польза", "в чём твоя польза"]


# функция написания сообщения пользователю для прикрепления фотографий используется attachment по умолчанию равный False
def write_msg(user_id, message, attachment=False):
    if not attachment:
        vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.randint(0, 2 ** 32)})
    else:
        vk.method('messages.send', {'user_id': user_id, 'message': message, 'attachment': attachment,
                                    'random_id': random.randint(0, 2 ** 32)})


# API-ключ для группы
token = "APIKEY"

# Авторизуемся как сообщество
vk = vk_api.VkApi(token=token)

# Работа с сообщениями
longpoll = VkLongPoll(vk)

# переменные для работы генератора паролей
pas_use = []
low_let = 'abcdefghijkmnpqrstuvwxyz'
high_let = 'ABCDEFGHJKLMNPQRSTUVWXYZ'
nums = '0123456789'


# Функция открывающая файл с цитатами и возвращающая случайную
def quotes():
    text = []
    with open('data/text/quotes.txt',
              encoding="utf-8") as f:
        text = f.read().splitlines()
        return random.choice(text)


# Функция открывающая файл с анекдотами и возвращающий случайный
def anekdot():
    jokes = []
    with open('data/text/jokes.txt',
              encoding="utf-8") as f:
        jokes = f.read().splitlines()
        return random.choice(jokes)


# Функция открывающая директорию с фотографиями и возвращающая случайную
def photo():
    upload = vk_api.VkUpload(vk)
    photo = upload.photo_messages('data/img/lolcats' + str(random.randint(1, 80)) + '.jpg')
    owner_id = photo[0]['owner_id']
    photo_id = photo[0]['id']
    access_key = photo[0]['access_key']
    attachment = 'photo' + str(owner_id) + '_' + str(photo_id) + '_' + str(access_key)
    return attachment


# Функция Генерирующая пароли
def generate_password(m):
    end = False
    while end is False:
        let_right = 'abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'
        pas = []
        pas.append(random.choice(low_let))
        let_right = let_right.replace(pas[0], '')
        pas.append(random.choice(high_let))
        let_right = let_right.replace(pas[1], '')
        pas.append(random.choice(nums))
        let_right = let_right.replace(pas[2], '')
        for i in range(m - 3):
            new_lett = random.choice(let_right)
            let_right = let_right.replace(new_lett, '')
            pas.append(new_lett)
        random.shuffle(pas)
        pas = ''.join(pas)
        if pas not in pas_use:
            end = True
    return pas


def get_passwords(n, m):
    passwords = []
    for i in range(n):
        passwords.append(generate_password(m))
        pas_use.append(passwords[i])
    pas_use.clear()
    # тут меняется только эта строчка, чтоб возвращалась именно строка
    return ', '.join(passwords)


# Функция работающая с API OWM и возвращающая строку с погодой в указанном городе
def get_weather(city):
    url = 'http://api.openweathermap.org/data/2.5/weather?q=' + \
          city + '&units=metric&lang=ru&appid=6183cc27ea7a57941943927547658652'
    response = requests.get(url)
    if response.status_code == 200:
        dict_weather = response.json()
        temp = str(dict_weather['main']['temp'])
        if dict_weather['main']['temp'] > 0:
            temp = '+' + str(dict_weather['main']['temp'])
        line = city.capitalize() + '\nСейчас ' + temp + ', ' + dict_weather['weather'][0]['description']
    elif response.status_code == 404:
        line = 'Город не найден'
    return line


# Функция возвращает текущее время по которому работает бот
def get_time():
    today = datetime.today()
    wd = date.weekday(today)
    days = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]
    months = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября",
              "ноября", "декабря"]
    return f"Сегодня {days[wd]}, {today.day} {months[today.month - 1]} {today.year} года. " \
           f"Время {today.hour}:{today.minute}"


# Списки для работы функций шифровки/дешифровки шифра цезаря
llst = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н',
        'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы',
        'ь', 'э', 'ю', 'я']
blst = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н',
        'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы',
        'Ь', 'Э', 'Ю', 'Я']


# Функция шифровки по алгоритму цезаря
def encrypt_caesar(msg, shift):
    ret = ""
    shift = int(shift)
    for x in msg:
        if x in llst:
            ind = llst.index(x) % len(llst)
            ret += llst[(ind + shift) % len(llst)]
        elif x in blst:
            ind = blst.index(x) % len(llst)
            ret += blst[(ind + shift) % len(llst)]
        else:
            ret += x
    return ret


# Функция шифровки по алгоритму цезаря
def decrypt_caesar(msg, shift):
    ret = ""
    shift = int(shift)
    for x in msg:
        if x in llst:
            ind = llst.index(x)
            ret += llst[ind - shift]
        elif x in blst:
            ind = blst.index(x)
            ret += blst[ind - shift]
        else:
            ret += x
    return ret


# print("Бот запущен")

# флаги для работы условий
weather = False
password_quan = False
password = False
caesar = False
num_to_words = False
solving = False

# Основной цикл
for event in longpoll.listen():

    # Если пришло новое сообщение
    if event.type == VkEventType.MESSAGE_NEW:

        # Если оно имеет метку для меня(то есть бота)
        if event.to_me:

            # Сообщение от пользователя
            request = event.text.lower()
            # Каменная логика ответа
            if request in hello:
                write_msg(event.user_id, str(random.choice(hello)).capitalize())

            elif request in goodbye:
                write_msg(event.user_id, str(random.choice(goodbye)).capitalize())

            elif request == 'время' or request == "сколько времени?":
                write_msg(event.user_id, get_time())

            # активируем навык "генератор паролей"
            elif request == 'генератор паролей':
                write_msg(event.user_id, 'Введите длину пароля (Минимум 3)')
                # флаг "password" нужен для того, чтобы следующее сообщение воспринималось именно как длина пароля
                # следующие навки реализованы по такому же принципу
                password = True
            # если "password" true, значит пользователь активировал навык генерации паролей и сейчас ввел длину пароля
            elif password:
                # проверяем правильно ли пользователь все ввел
                if request.isdigit():
                    password_m = int(request)
                else:
                    # если данные не подходят  деактивируем навык
                    write_msg(event.user_id, 'Что-то не то...')
                    password = False
                    continue
                write_msg(event.user_id, 'Введите количество паролей (Минимум 1)')
                password_quan = True
                password = False
            # если "password_quan" true, значит активирован навык генерации паролей и сейчас вводится кол-во паролей
            elif password_quan:
                if request.isdigit():
                    password_n = int(request)
                else:
                    write_msg(event.user_id, 'Что-то не то...')
                    password_quan = False
                    continue
                # вызываем метод "get_passwords", в котором заранее настроили возвращение строки с паролями
                write_msg(event.user_id, 'Готово: ' + get_passwords(password_n, password_m))
                # меняем флаг на false, теперь навык не активирован
                password_quan = False
            # Реакция на сообщение с запросом помощи / списком комманд
            elif request in n_help:
                write_msg(event.user_id, 'Список команд: \n генератор паролей - позволяет сгенерировать ' +
                          'один или несколько паролей \n время - скажу тебе дату и время по которым я' +
                          ' работаю и живет мой создатель \n цезарь - позволит тебе расшифровать ' +
                          'или зашифровать сообщение шифром цезаря \n погода - позволит тебе узнать ' +
                          'текущую погоду в указанном тобой городе ' +
                          '(только не ошибайся в названии городов) \n число словами - напишет тебе как' +
                          ' пишется введенное тобой число русскими словами \n коты - отправит тебе' +
                          ' картинку с котом или кошкой, наслаждайся \n цитаты - ' +
                          'случайная цитата из фильма, всего 100 штук \n анекдоты - ' +
                          'пришлет тебе какой то анекдот')

            elif request == "цитаты":
                write_msg(event.user_id, f'Твоя цитата: \n {quotes()}')

            elif request == "цезарь":
                write_msg(event.user_id, 'Вы хотите зашифровать или расшифровать код?')
                caesar = True
                caesar_en = False
                caesar_de = False
            elif caesar:
                if request == "расшифровать":
                    write_msg(
                        event.user_id,
                        "Введите одно слово для расшифровки, только кириллица. И сдвиг шифра через пробел, " +
                        "только целое число")
                    caesar_de = True
                elif caesar_de:
                    message = request.split()
                    write_msg(event.user_id, f"Результат дешифровки: {decrypt_caesar(message[0], message[1])}")
                    caesar_de = False
                elif request == "зашифровать":
                    write_msg(event.user_id,
                              "Введите одно слово для шифровки, только кириллица. " +
                              "И сдвиг шифра через пробел только целое числа")
                    caesar_en = True
                elif caesar_en:
                    message = request.split()
                    write_msg(event.user_id, f"Результат шифровки: {encrypt_caesar(message[0], message[1])}")
                    caesar_en = False
                else:
                    write_msg(event.user_id, 'Не понял вашего ответа...')
                    caesar = not caesar
            # используется библеотека num2words для того что бы перевести число в слова
            elif request == "число словами":
                write_msg(event.user_id, 'Введите какое число вы хотите написать словами')
                num_to_words = True
            elif num_to_words:
                print(request)
                write_msg(event.user_id, num2words(int(request), lang='ru'))
                num_to_words = False
                # Навык коты
            elif request == 'коты':
                write_msg(event.user_id, "Твой котан:", photo())
                # навык анедоты
            elif request == 'анекдоты':
                write_msg(event.user_id, f'Твоя шутка: \n {anekdot()}')
                # навык отвечающий на вопрос "кто ты?" и т.п.
            elif request in who_are_you:
                write_msg(event.user_id, "Я процедурный Бот-013, мой создатель Сергей написал меня на " +
                          "Python используя кучу if'ов и elif'ов")

            # активируем навык "погода"
            elif request == 'погода':
                write_msg(event.user_id, 'Введите название города для которого хотите узнать погоду')
                # флаг "weather" нужен для того, чтобы следующее соо юзера воспринималось именно как город
                weather = True
            # если "weather" true, значит пользователь активировал навык погоды и сейчас ввел город
            elif weather:
                # передаем в метод "get_weather" город и возвращаем юзеру погоду
                write_msg(event.user_id, get_weather(request))
                # деактивируем навык изменением флага
                weather = not weather
                # самый последний случай если ничего из вышеперечисленного не подходит, сообщаем юзеру что не поняли его
            else:
                write_msg(event.user_id, "Не понял вашего ответа...")
