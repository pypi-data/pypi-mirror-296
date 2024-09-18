import os
import logging
import zipfile
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram import Router
from aiogram.utils.token import TokenValidationError
from dotenv import load_dotenv
import asyncio
from pathlib import Path
import time
import shutil

# Загружаем токен из .env файла
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Включаем логирование с добавлением смайликов
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Проверяем токен на валидность
try:
    bot = Bot(token=TOKEN)
except TokenValidationError as e:
    logging.error(f"🔴 Неверный токен: {e}")
    exit()

# Создаем диспетчер с использованием памяти для хранения состояний
dp = Dispatcher(storage=MemoryStorage())

# Маршрутизатор
router = Router()

# Путь к Calibre (ebook-convert)
CALIBRE_CONVERT_COMMAND = 'ebook-convert'

# Создаем папку для хранения данных, если её нет
DATA_DIR = Path('data')
DATA_DIR.mkdir(exist_ok=True)

# Время в секундах: 1 час = 3600 секунд
FILE_LIFETIME = 3600


# Функция для проверки доступности Calibre
def check_calibre_available():
    calibre_path = shutil.which(CALIBRE_CONVERT_COMMAND)
    if calibre_path:
        logging.info(f"🟢 Calibre доступен по пути: {calibre_path}")
        return True
    else:
        logging.error(f"🔴 Calibre не найден! Убедитесь, что он установлен и доступен в системе.")
        return False


# Функция для асинхронного запуска команд через subprocess
async def run_command(cmd):
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()

    return stdout.decode(), stderr.decode(), process.returncode


# Хэндлер на команду /start
@router.message(Command(commands=["start"]))
async def start(message: Message):
    await message.answer("Привет! 👋😃 Отправь мне файл формата .fb2, и я сконвертирую его в .epub! 📚✨")


# Асинхронная функция для конвертации файла с помощью Calibre
async def convert_fb2_to_epub(fb2_file_path: Path, epub_file_path: Path):
    cmd = f"{CALIBRE_CONVERT_COMMAND} {fb2_file_path} {epub_file_path}"
    stdout, stderr, returncode = await run_command(cmd)

    if returncode != 0:
        logging.error(f"🔴 Ошибка при конвертации: {stderr}")
        raise Exception(f"Ошибка при конвертации: {stderr}")

    logging.info(f"🟢 Конвертация завершена: {stdout}")
    return epub_file_path


# Функция для извлечения изображения обложки из epub
async def extract_epub_thumbnail(epub_file_path: Path, thumbnail_path: Path):
    try:
        with zipfile.ZipFile(epub_file_path, 'r') as epub:
            # Ищем файл с обложкой в EPUB
            for file_info in epub.infolist():
                if 'cover' in file_info.filename and file_info.filename.endswith(('.jpg', '.jpeg', '.png')):
                    # Сохраняем обложку
                    with open(thumbnail_path, 'wb') as thumbnail_file:
                        thumbnail_file.write(epub.read(file_info.filename))
                    logging.info(f"🟢 Изображение обложки извлечено: {thumbnail_path}")
                    return thumbnail_path
        return None  # Если обложка не найдена
    except Exception as e:
        logging.error(f"🔴 Ошибка при извлечении обложки: {e}")
        return None


# Хэндлер для обработки присланных документов
@router.message(F.document)
async def handle_document(message: Message):
    document = message.document

    # Проверяем расширение файла
    if not document.file_name.endswith('.fb2'):
        await message.answer(
            "Ой, кажется ты отправил что-то не то! 😅📄\nОтправь мне файл в формате .fb2, и я сделаю из него шикарный .epub! 📚✨")
        return

    # Скачиваем файл
    file_info = await bot.get_file(document.file_id)

    file_name = document.file_name
    fb2_file_path = DATA_DIR / file_name  # Сохраняем файл в папку data
    epub_file_path = fb2_file_path.with_suffix('.epub')

    try:
        # Скачиваем файл асинхронно
        await bot.download_file(file_info.file_path, fb2_file_path.as_posix())

        # Сообщение пользователю о начале конвертации
        converting_message = await message.answer("Начинаем конвертацию... 🛠📚 Подожди немного! ⏳")

        # Конвертируем файл асинхронно
        await convert_fb2_to_epub(fb2_file_path, epub_file_path)

        thumbnail_path = DATA_DIR / (fb2_file_path.stem + '_thumbnail.jpg')
        thumbnail = await extract_epub_thumbnail(epub_file_path, thumbnail_path)

        thumb = None
        if thumbnail and thumbnail.exists():
            thumb = FSInputFile(thumbnail)

        await bot.send_document(
            chat_id=message.chat.id,
            reply_to_message_id=message.message_id,
            parse_mode='HTML',
            document=FSInputFile(
                path=epub_file_path.as_posix(),
                filename=epub_file_path.name),
            thumbnail=thumb)

        await message.answer("Конвертация завершена! 🎉📚 Готовый .epub файл у тебя! 🚀")

        # Удаляем сообщение о начале конвертации
        await converting_message.delete()

    except Exception as e:
        await message.answer(f"Ой-ой! Что-то пошло не так! 😓 Ошибка: {e}")
        logging.error(f"🔴 Ошибка: {e}")


# Хэндлер для обработки всех остальных сообщений
@router.message()
async def handle_all_messages(message: Message):
    await message.answer(
        "Эй, я жду .fb2 файл! 📄😎\nОтправь его, и я превратю его в .epub, как по волшебству! ✨\nДругие файлы мне не так интересны, но я верю, что у тебя найдется то, что нужно. 😉")


# Функция для периодической очистки старых файлов
async def cleanup_old_files():
    while True:
        now = time.time()
        for file_path in DATA_DIR.iterdir():
            if file_path.is_file() and (now - file_path.stat().st_mtime > FILE_LIFETIME):
                try:
                    file_path.unlink()
                    logging.info(f"🟢 Удален файл: {file_path}")
                except Exception as e:
                    logging.error(f"🔴 Ошибка при удалении файла {file_path}: {e}")
        await asyncio.sleep(60)  # Проверяем файлы каждые 60 секунд


# Запуск бота
async def main():
    dp.include_router(router)

    # Проверяем доступность Calibre перед запуском бота
    if not check_calibre_available():
        logging.error("🔴 Бот остановлен, так как Calibre недоступен.")
        return

    # Запускаем задачу для периодической очистки файлов
    asyncio.create_task(cleanup_old_files())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())