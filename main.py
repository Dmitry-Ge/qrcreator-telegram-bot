import os
import logging
import qrcode
import qrcode.image.svg
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types.input_file import FSInputFile


# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Бот и диспетчер
TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Меню кнопок
menu_buttons = [
    KeyboardButton(text='Создать QR-код(png)'),
    KeyboardButton(text='Создать QR-код(svg)')
]

# Клавиатура
keyboard = ReplyKeyboardMarkup(
    keyboard=[menu_buttons],
    resize_keyboard=True
)

# Группы состояний
class CreateQRCode(StatesGroup):
    waiting_for_text_png = State()
    waiting_for_text_svg = State()

# Команда старта
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет! Это бот для создания и скачивания QR-кодов.", reply_markup=keyboard)

# Команды помощи
@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Вы можете создавать и скачивать QR-коды. Просто выберите соответствующую команду.", reply_markup=keyboard)

# Начало процесса создания QR-кода
@dp.message(F.text.lower().in_(['создать qr-код(png)']))
async def process_create_qr(message: Message, state: FSMContext):
    await message.answer("Введите текст для QR-кода:", reply_markup=None)
    await state.set_state(CreateQRCode.waiting_for_text_png)

@dp.message(F.text.lower().in_(['создать qr-код(svg)']))
async def process_create_qr(message: Message, state: FSMContext):
    await message.answer("Введите текст для QR-кода:", reply_markup=None)
    await state.set_state(CreateQRCode.waiting_for_text_svg)

# Обработка введённого текста и создание QR-кода
# Обработка введённого текста и создание QR-кода
@dp.message(CreateQRCode.waiting_for_text_png)
async def handle_qr_text(message: Message, state: FSMContext):
    text = message.text
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=12,
        border=2,
    )
    qr.add_data(text)
    qr.make(fit=True)

    uniq_filename = f"qr_code_{message.from_user.id}.png"
    qr.make_image(fill_color="black", back_color="white").save(uniq_filename)

    # img = qr.make_image(fill_color="black", back_color="white")
    # img.save("qr_code.png")

    logging.info(uniq_filename)
    await bot.send_photo(chat_id=message.chat.id, photo=FSInputFile(uniq_filename))
    await state.clear()

    # delete old file
    os.remove(uniq_filename)

    await message.answer("QR-код успешно создан и отправлен.", reply_markup=keyboard)


@dp.message(CreateQRCode.waiting_for_text_svg)
async def handle_qr_text(message: Message, state: FSMContext):
    text = message.text
    qr = qrcode.QRCode(
        image_factory=qrcode.image.svg.SvgPathImage,
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=12,
        border=2
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    uniq_filename = f"qr_code_{message.from_user.id}.svg"
    img.save(uniq_filename)
    # qr.make_image(fill_color="black", back_color="white").save(uniq_filename)

    # img = qr.make_image(fill_color="black", back_color="white")
    # img.save("qr_code.png")

    logging.info(uniq_filename)
    await bot.send_document(chat_id=message.chat.id, document=FSInputFile(uniq_filename))
    await state.clear()

    # delete old file
    os.remove(uniq_filename)

    await message.answer("QR-код успешно создан и отправлен.", reply_markup=keyboard)

# default handler
@dp.message()
async def default_text_handler(message: Message):
    await message.reply("Выберите какой именно QR нужен", reply_markup=keyboard)


# Запуск бота
if __name__ == "__main__":
    # add timeout for long polling
    timeout = 30
    # dp.run_polling(bot)
    dp.run_polling(bot, timeout=timeout)
