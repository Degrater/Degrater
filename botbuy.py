from typing import Dict, Tuple

from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher.filters.builtin import CommandStart

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup


bot = Bot(token='', parse_mode='HTML')
dp = Dispatcher(bot)

CHANNEL_ID = ''
CONTACTS = "<b>Пункт выдачи, производство и офис:</b>\n" \
           "г. Москва, наб. Новикова-Прибоя, д.14, к.1\n" \
           "<b>Телефон:</b> +7 (499) 199-61-61\n" \
           "<b>Режим работы:</b> 9:00 - 18:00"


# PS: желательно использовать сторонее хранилище, а не глобальную переменную.
order = {}

""" Кнопки """

"  ReplyKeyboardMarkup  "


def start_markup() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=3)
    buttons = ["Услуги", "Онлайн-заказ", "Прайс-лист", "Продукция", 'Контакты']
    for button in buttons:
        markup.insert(button)
    return markup


"  InlineKeyboardMarkup  "

menu_cd = CallbackData('menu', 'data', 'action')


class Buttons:
    """
    Класс со всеми Inline кнопками.
    """
    goods_menu = {
        "Конверты": 'convert', "Листовки": 'flyer', "Плакаты": 'posters', "Буклеты": 'booklets', "Этикетки": 'labels',
        "Бланки": 'forms', "Наклейки": 'stickers', "Календари": 'calendars', "Папки": 'f', "Брошюры": 'b',
        "Коробки": 'boxes', "Блокноты": 'n'
    }

    # не смотри, сразу с 220 строке иди. Тут присуствуют сокращения из-за ограничения в 64 символа у CallbackData

    all_buttons = {
        'convert': [['Количество сторон ?', 2, 'menu', 'convert_second', 'Количество сторон: '],
                    ["1+0 (любой пантон)", "4+0 "]],
        'convert_second': [['Выберите размер ?', 2, 'convert', 'convert_third', 'Размер: '],
                           ["С6 (144х162 мм.)", "Е65 (110х220 мм.) без окна", "Е65 (110х220 мм.) с окном",
                            "С65 (114х229 мм.) без окна", "С65 (114х229 мм.) с окном", "С5 (162х229 мм,) без окна",
                            "С5 (162х229 мм,) с окном ", "С4 (229х324 мм.) без окна", "С4 (229х324 мм.) с окном"]],
        'convert_third': [['Выберите количество ?', 3, 'convert_second', 'convert_total', 'Количество: '],
                          ["200", "300", "500", "1000", "2000"]],
        'convert_total': [['<b>Ваш заказ:</b>\n\n', 1, 'convert_third', 'apply_order', 'Заказ'], ['Подтвердить заказ']],


        'flyer': [['Выберите размер ?', 2, 'menu', 'flyer_second', 'Размер: '], ["A4", "A3"]],
        'flyer_second': [['Материал ?', 1, 'flyer', 'flyer_third', 'Материал: '], ["Глян. мелованная бумага"]],
        'flyer_third': [['Количество сторон ?', 1, 'flyer_second', 'flyer_fourth', 'Количество сторон: '],
                        ["4+0 (односторонняя печать)", "4+4 (двухсторонняя печать)"]],
        'flyer_fourth': [['Выберите количество ?', 3, 'flyer_third', 'flyer_total', 'Количество: '],
                         ["200", "300", "500", "1000", "2000"]],
        'flyer_total': [['<b>Ваш заказ:</b>\n\n', 1, 'flyer_fourth', 'apply_order', 'Заказ'], ['Подтвердить заказ']],


        'posters': [['Выберите размер ?', 3, 'menu', 'posters_second', 'Размер: '], ["A3", "A2", "A1"]],
        'posters_second': [['Материал ?', 1, 'posters', 'posters_third', 'Материал: '],
                           ["Глян. мелованная бумага", "Мат. мелованная бумага"]],
        'posters_third': [['Плотность ?', 2, 'posters_second', 'posters_fourth', 'Плотность: '],
                          ["115г", "150г", "200г", "300г"]],
        'posters_fourth': [['Количество сторон ?', 1, 'posters_third', 'posters_fifth', 'Количество сторон: '],
                           ["4+0 (односторонняя печать)"]],
        'posters_fifth': [['Выберите количество ?', 3, 'posters_fourth', 'posters_total', 'Количество: '],
                          ["200", "300", "500", "1000", "2000"]],
        'posters_total': [['<b>Ваш заказ:</b>\n\n', 1, 'posters_fifth', 'apply_order', 'Заказ'], ['Подтвердить заказ']],


        'booklets': [['Выберите размер ?', 2, 'menu', 'booklets_second', 'Размер: '], ["A4", "A3"]],
        'booklets_second': [['Материал ?', 1, 'booklets', 'booklets_third', 'Материал: '], ["Глян. мелованная бумага"]],
        'booklets_third': [['Операция ?', 2, 'booklets_second', 'booklets_fourth', 'Операция: '],
                           ["Евробуклет", "Гармошка", "Книжка"]],
        'booklets_fourth': [['Выберите количество ?', 3, 'booklets_third', 'booklets_total', 'Количество: '],
                            ["200", "300", "500", "1000", "2000"]],
        'booklets_total': [['<b>Ваш заказ:</b>\n\n', 1, 'booklets_fourth', 'apply_order', 'Заказ'], ['Подтвердить заказ']],


        'labels': [['Выберите размер ?', 2, 'menu', 'labels_second', 'Размер: '],
                   ["275x106 мм.", "285x75 мм.", "170х50 мм.", "205х70 мм.", "130х80 мм.", "120х165 мм.",
                    "220х210 мм.", "135х135 мм."]],
        'labels_second': [['Материал ?', 1, 'labels', 'labels_third', 'Материал: '], ["Sinarlux", "Этикеточная бумага"]],
        'labels_third': [['Плотность ?', 1, 'labels_second', 'labels_fourth', 'Плотность: '], ["80г"]],
        'labels_fourth': [['Количество сторон ?', 1, 'labels_third', 'labels_fifth', 'Количество сторон: '],
                          ["4+0 (односторонняя печать)"]],
        'labels_fifth': [['Выберите количество ?', 3, 'labels_fourth', 'labels_total', 'Количество: '],
                         ["200", "300", "500", "1000", "2000"]],
        'labels_total': [['<b>Ваш заказ:</b>\n\n', 1, 'labels_fifth', 'apply_order', 'Заказ'], ['Подтвердить заказ']],


        'forms': [['Выберите размер ?', 1, 'menu',  'forms_second', 'Размер: '], ['21х30 см. (так же A4)']],
        'forms_second': [['Материал ?', 1, 'forms', 'forms_third', 'Материал: '], ["Офсетная бумага"]],
        'forms_third': [['Плотность ?', 1, 'forms_second', 'forms_fourth', 'Плотность: '], ["80г"]],
        'forms_fourth': [['Количество сторон ?', 1, 'forms_third', 'forms_fifth', 'Количество сторон: '],
                         ["4+0 (односторонняя печать)"]],
        'forms_fifth': [['Выберите количество ?', 3, 'forms_fourth', 'forms_total', 'Количество: '],
                        ["200", "300", "500", "1000", "2000"]],
        'forms_total': [['<b>Ваш заказ:</b>\n\n', 1, 'forms_fifth', 'apply_order', 'Заказ'], ['Подтвердить заказ']],


        'stickers': [['Выберите размер ?', 1, 'menu',  'st_se', 'Размер: '],
                     ['Размер 7х10 см. (так же А7)', 'Размер 10х15 см. (так же А6)', "Размер 15х20 см. (так же А5)",
                      "Размер 21х30 см. (так же А4)", "Размер 30х42 см. (так же А3)", "Размер 42х60 см. (так же А2)"]],
        'st_se': [['Материал ?', 1, 'stickers', 'stickers_third', 'Материал: '], ["Самоклеющаяся бумага"]],
        'stickers_third': [['Цветность ?', 1, 'st_se', 'st_fo', 'Цветность: '],
                           ["4+0"]],
        'st_fo': [['Выберите количество ?', 3, 'stickers_third', 'stickers_total', 'Количество: '],
                  ["200", "300", "500", "1000", "2000"]],
        'stickers_total': [['<b>Ваш заказ:</b>\n\n', 1, 'st_fo', 'apply_order', 'Заказ'], ['Подтвердить заказ']],


        'calendars': [['Выберите размер ?', 1, 'menu',  'c_s', 'Размер: '],
                      ["Блок 12 листов (4+0) + Обложка (4+0)", "Блок 6 листов (4+4) + Обложка (4+0)"]],
        'c_s': [['Ламинирование', 1, 'calendars', 'calendars_third', 'Ламинирование: '],
                ["Без ламинации обложки", "С ламинацией обложки"]],
        'calendars_third': [['Лакирование', 1, 'c_s', 'c_f',  'Лакирование: '],
                            ["Без УФ лака", "УФ лак на обложке (выбор.) 1+0"]],
        'c_f': [['Выберите количество ?', 3, 'calendars_third', 'calendars_total', 'Количество: '],
                ["200", "300", "500", "1000", "2000"]],
        'calendars_total': [['<b>Ваш заказ:</b>\n\n', 1, 'c_f', 'apply_order', 'Заказ'],
                            ['Подтвердить заказ']],


        'f': [['Выберите размер ?', 1, 'menu',  'folders_second', 'Размер: '], ['A4']],
        'folders_second': [['Материал ?', 1, 'f', 'f_t', 'Материал: '],
                           ["Картон одностор. (цветность 4+0)", "Картон двустор. (цветность 4+4)"]],
        'f_t': [['Плотность ?', 1, 'folders_second', 'folders_fourth', 'Плотность: '], ["300г"]],
        'folders_fourth': [['Операция ?', 1, 'f_t', 'folders_fifth', 'Операция: '],
                           ["C ламинацией", "Без ламинации"]],
        'folders_fifth': [['Выберите количество ?', 3, 'folders_fourth', 'folders_total', 'Количество: '],
                          ["200", "300", "500", "1000", "2000"]],
        'folders_total': [['<b>Ваш заказ:</b>\n\n', 1, 'folders_fifth', 'apply_order', 'Заказ'], ['Подтвердить заказ']],


        'b': [['Выберите :', 1, 'menu', 'b_s', 'Выбор: '], []],
        'b_s': [['Выберите размер ?', 1, 'b', 'b_t', 'Размер: '],
                ["A5 (книж. ориентация)", "A4 (книж. ориентация)", "A5 (альбом. ориентация)", "A4 (книж. ориентация)"]],
        'b_t': [["Блок : Укажите количество полос в блоке (без учета обложки):", 2, 'b_s', 'brochures_fourth', 'Блок: '],
                ["8", "16", "24", "32"]],
        'brochures_fourth': [['Материал ?', 1, 'b_t', 'brochures_fifth', 'Материал: '],
                             ["Глян. мелованная бумага", "Мат. мелованная бумага", "Офсетная бумага"]],
        'brochures_fifth': [['Плотность ?', 2, 'brochures_fourth', 'b_si', 'Плотность: '],
                            ["115г", "130", "150г", "170г"]],
        'b_si': [['Количество сторон ?', 1, 'brochures_fifth', 'brochures_seventh', 'Количество сторон: '],
                 ["Полноцветная печать", "Одноцветная печать"]],
        'brochures_seventh': [['Материал обложки ?', 1, 'b_si', 'b_e', 'Материал обложки: '],
                              ["Глян. мелованная бумага", "Мат. мелованная бумага", "Офсетная бумага"]],
        'b_e': [['Плотность обложки ?', 3, 'brochures_seventh', 'brochures_ninth', 'Плотность обложки: '],
                ["115г", "130г", "150г", "170г", "200г", "250г"]],
        'brochures_ninth': [['Количество сторон обложки ?', 1, 'b_e', 'brochures_tenth', 'Количество сторон обложки: '],
                            ["Полноцветная печать", "Одноцветная печать"]],
        'brochures_tenth': [['Тираж ?', 3, 'brochures_ninth', 'brochures_total', 'Тираж: '],
                            ["200", "300", "500", "1000", "2000"]],
        'brochures_total': [['<b>Ваш заказ:</b>\n\n', 1, 'brochures_tenth', 'apply_order', 'Заказ'],
                            ['Подтвердить заказ']],


        'b_2_s': [['Выберите размер ?', 1, 'b', 'b_2_t', 'Размер: '], ["A4 (книж. ориентация)", "A4 (альбом. ориентация)"]],
        'b_2_t': [['Блок : Количество полос ?', 3, 'b_2_s', 'brochures_catalog_fourth', 'Блок : Количество полос: '],
                  ["32", "48", "64"]],
        'brochures_catalog_fourth': [['Блок : Материал ?', 1, 'b_2_t', 'b_2_f', 'Блок : Материал : '],
                                     ["Глян. мелованная бумага", "Мат. мелованная бумага", "Офсетная бумага"]],
        'b_2_f': [['Блок : Плотность ?', 2, 'brochures_catalog_fourth', 'b_2_si', 'Блок : Плотность: '],
                  ["115г", "130г", "150г", "170г"]],
        'b_2_si': [['Блок : Количество сторон ?', 1, 'b_2_f', 'b_2_se',  'Блок : Количество сторон: '],
                   ["Полноцветная печать", "Одноцветная печать"]],
        'b_2_se': [["Материал обложки ?", 1, 'b_2_si', 'b_2_e', "Материал обложки: "],
                   ["Глян. мелованная бумага", "Мат. мелованная бумага", "Офсетная бумага"]],
        'b_2_e': [['Плотность обложки ?', 2, 'b_2_se', 'brochures_2_ninth', 'Плотность обложки: '],
                  ["115г", "130г", "150г", "170г"]],
        'brochures_2_ninth': [['Количество сторон обложка ?', 1, 'b_2_e', 'brochures_2_tenth', 'Количество сторон обложка: '],
                              ["Полноцветная печать", "Одноцветная печать"]],
        'brochures_2_tenth': [['Тираж ?', 3, 'brochures_2_ninth', 'brochures_2_total', 'Тираж: '],
                              ["200", "300", "500", "1000", "2000"]],
        'brochures_2_total': [['<b>Ваш заказ:</b>\n\n', 1, 'brochures_2_tenth', 'apply_order', 'Заказ'],
                              ['Подтвердить заказ']],


        'boxes': [['Выберите размер ?', 1, 'menu', 'boxes_second', 'Размер: '],
                  ["50x30x30", "107x31x31", "160x125x40", "197x70x27", "197x70x55", "325x245x29"]],
        'boxes_second': [['Материал ?', 1, 'boxes', 'boxes_third', 'Материал: '], ["Картон(односторонний)"]],
        'boxes_third': [['Плотность ?', 1, 'boxes_second', 'boxes_fourth', 'Плотность: '], ["300г"]],
        'boxes_fourth': [['Тираж ?', 3, 'boxes_third', 'boxes_total', 'Тираж: '], ["200", "300", "500", "1000", "2000"]],
        'boxes_total': [['<b>Ваш заказ:</b>\n\n', 1, 'boxes_fourth', 'apply_order', 'Заказ'], ['Подтвердить заказ']],


        'n': [[0, 1, 2, 3, 'Выбор: '], []],
        'not_1_s': [['Материал обложки ?', 1, 'n', 'not_1_third', 'Материал обложки: '], ["Матовая бумага"]],
        'not_1_third': [['Плотность обложки ?', 3, 'not_1_s', 'notepads_1_fourth', 'Плотность обложки: '], ["300г"]],
        'notepads_1_fourth': [['Количество сторон обложки ?', 1, 'not_1_third', 'notepads_1_fifth', 'Количество сторон обложки: '],
                              ["4+0 (односторонняя печать)"]],
        'notepads_1_fifth': [["Блок : Материал ?", 1, 'notepads_1_fourth', 'notepads_1_sixth', 'Блок : Материал: '],
                             ["Офсетная бумага"]],
        'notepads_1_sixth': [["Блок : Плотность ?", 1, 'notepads_1_fifth', 'notepads_1_seventh', 'Блок : Плотность: '],
                             ["80г"]],
        'notepads_1_seventh': [["Блок : Количество сторон ?", 1, 'notepads_1_sixth', 'notepads_1_eighth', 'Блок : Количество сторон: '],
                               ["1+0 (любой пантон)", "1+1 (любой пантон)", "4+0 (CMYK)", "4+4 (CMYK)"]],
        'notepads_1_eighth': [['Тираж ?', 3, 'notepads_1_seventh', 'notepads_1_total', 'Тираж: '],
                              ["200", "300", "500", "1000", "2000"]],
        'notepads_1_total': [['<b>Ваш заказ:</b>\n\n', 1, 'notepads_1_eighth', 'apply_order', 'Заказ'], ['Подтвердить заказ']],


        'notepads_2_second': [['Выберите размер ?', 1, 'n', 'notepads_2_third', 'Размер: '],
                              ["5 см. или 500 листов", "9 см. или 900 листов"]],
        'notepads_2_third': [["Материал ?", 1, 'notepads_2_second', 'notepads_2_fourth', 'Материал: '],
                             ["Офсетная бумага"]],
        'notepads_2_fourth': [["Плотность ?", 1, 'notepads_2_third', 'notepads_2_fifth', 'Плотность: '], ["80г"]],
        'notepads_2_fifth': [["Количество сторон ?", 1, 'notepads_2_fourth', 'notepads_2_sixth', 'Количество сторон: '],
                             ["1+0 (любой пантон)", "4+0"]],
        'notepads_2_sixth': [['Тираж ?', 3, 'notepads_2_fifth', 'notepads_2_total', 'Тираж: '],
                             ["200", "300", "500", "1000", "2000"]],
        'notepads_2_total':  [['<b>Ваш заказ:</b>\n\n', 1, 'notepads_2_sixth', 'apply_order', 'Заказ'], ['Подтвердить заказ']],
    }


class CallbackFactory(Buttons):
    def __init__(self, action: str = ''):
        self.action = action
        self.menu_goods = Buttons.goods_menu
        self.all_buttons = Buttons.all_buttons
        self.value = self.all_buttons.get(self.action)

    def goods_markup(self) -> InlineKeyboardMarkup:
        """
        Генерирует кнопки товаров.
        :return:
        """
        markup = InlineKeyboardMarkup(row_width=3)
        for button, action in self.goods_menu.items():
            markup.insert(InlineKeyboardButton(button, callback_data=menu_cd.new(data=button, action=action)))
        return markup

    @classmethod
    def confirm_markup(cls) -> InlineKeyboardMarkup:
        """
        Генерирует кнопку после подтверждения заказаю.
        :return:
        """
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton('Главное меню', callback_data=menu_cd.new(data='Главное меню', action='main_menu'))
        )
        return markup

    def generator(self) -> Tuple[str, InlineKeyboardMarkup]:
        """
        Генерирует все кнопки для товаров. Для работы получает callback и по нему забирает значение из словаря
        со всем кнопками. Из первого списка получает необходимое для текущей клавиатуры. Из второго сами кнопки.
        PS: это медленный и хреновый способ. Надо бы это хранить в стороннем хранилище.
        :return:
        """
        if self.action == 'n' or self.action == 'b':
            keyboard = {'n': {"Блокноты А5 (блок 50 листов)": 'not_1_s', "Кубарики (90х90 мм.)": 'notepads_2_second'},
                        'b': {"Брошюра(скреплен. скоба)": 'b_s',
                              "Каталог(скреплен. термоклей)": 'b_2_s'}}
            markup = InlineKeyboardMarkup(row_width=1)
            for button, action in keyboard.get(self.action).items():
                markup.insert(InlineKeyboardButton(button, callback_data=menu_cd.new(data=button, action=action)))
            markup.add(InlineKeyboardButton('Назад', callback_data=menu_cd.new(data='Назад', action='menu')))
            return 'Выберите :', markup
        else:
            data = dict(zip(["text", "row_width", "previous", "next"], [elem for elem in self.value[0]]))
            markup = InlineKeyboardMarkup(row_width=data['row_width'])
            for button in self.value[1]:
                markup.insert(InlineKeyboardButton(button, callback_data=menu_cd.new(data=button, action=data['next'])))
            markup.add(InlineKeyboardButton('Назад', callback_data=menu_cd.new(data='Назад', action=data['previous'])))
            return data['text'], markup

    def back_button(self):
        """
        Кнопка назад.
        :return:
        """
        if 'menu' in self.action:
            return 'Выберите продукцию :', self.goods_markup()
        else:
            return self.generator()


"""  Бот  """


@dp.message_handler(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Добро Пожаловать! \nБот типографии https://moroz.pro/", reply_markup=start_markup())


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def menu_handler(message: types.Message):
    """
    Обработчик для кнопок меню.
    :param message:
    :return:
    """
    message_to_reply = {"Услуги": 'https://moroz.pro/vseuslugi/', "Контакты": CONTACTS,
                        "Прайс-лист": 'https://moroz.pro/prajs-list/', "Продукция": 'https://moroz.pro/producti0n/',
                        "Онлайн-заказ": 'Выберите продукцию :'}
    text = message_to_reply.get(message.text)
    if text:
        if text == 'Выберите продукцию :':
            await message.reply(text, reply_markup=CallbackFactory().goods_markup())
        else:
            await message.reply(text)


@dp.callback_query_handler(menu_cd.filter(data='Назад'))
async def back_button(query: types.CallbackQuery, callback_data: Dict[str, str]):
    """
    Обработчик кнопки назад.
    :param query:
    :param callback_data:
    :return:
    """
    text, markup = CallbackFactory(callback_data['action']).back_button()
    await query.message.edit_text(text, reply_markup=markup)


@dp.callback_query_handler(menu_cd.filter(action='main_menu'))
async def back_to_main_menu(query: types.CallbackQuery, callback_data: Dict[str, str]):
    """
    Обработчик кнопки "Главное меню" после подтверждения заказа.
    :param query:
    :param callback_data:
    :return:
    """
    await query.message.chat.delete_message(query.message.message_id)
    await cmd_start(query.message)


@dp.callback_query_handler(menu_cd.filter(action=[callback for callback in Buttons.goods_menu.values()]))
async def main_menu_goods(query: types.CallbackQuery, callback_data: Dict[str, str]):
    """
    Обработчик кнопок в меню товаров.
    :param query:
    :param callback_data:
    :return:
    """
    mention = query.message.chat.get_mention()
    order[mention] = {}
    order[mention]['Продукция: '] = callback_data['data']

    text, markup = CallbackFactory(callback_data['action']).generator()
    await query.message.edit_text(text, reply_markup=markup)


@dp.callback_query_handler(menu_cd.filter(action=[key for key in Buttons.all_buttons.keys()]))
async def handler_for_all_button(query: types.CallbackQuery, callback_data: Dict[str, str]):
    """
    Обработчик для всех кнопок.
    :param query:
    :param callback_data:
    :return:
    """
    key = Buttons.all_buttons.get(callback_data['action'])[0][2]
    description = Buttons.all_buttons.get(key)[0][4]
    mention = query.message.chat.get_mention()
    order[mention][description] = callback_data['data']

    text, markup = CallbackFactory(callback_data['action']).generator()
    if 'total' in callback_data['action']:
        for elem in order.values():
            for key, value in elem.items():
                text += f"<b>{key}</b>" + value + '\n'
        await query.message.edit_text(text, reply_markup=markup)
    else:
        await query.message.edit_text(text, reply_markup=markup)


@dp.callback_query_handler(menu_cd.filter(action='apply_order'))
async def total(query: types.CallbackQuery, callback_data: Dict[str, str]):
    """
    Обработчик подтверждения заказа.
    :param query:
    :param callback_data:
    :return:
    """
    text_for_channel, text_order = '', ''
    for user, data in order.items():
        text_for_channel += f'Заказ от пользователя:\n{user}\n\n'
        text_order += 'Ваш заказ:\n\n'
        for key, value in data.items():
            text_for_channel += f"<b>{key}</b>" + value + '\n'
            text_order += f"<b>{key}</b>" + value + '\n'
    await bot.send_message(CHANNEL_ID, text_for_channel)
    confirm = text_order + '\nПодтвержден!'
    await query.message.edit_text(confirm, reply_markup=CallbackFactory.confirm_markup())


if __name__ == "__main__":
    executor.start_polling(dp)