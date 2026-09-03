
import asyncio
import json
import logging
import os
import aiohttp
import requests
from dotenv import load_dotenv
from aiomax import Bot
from bot.adapters.max.create_bot import bot, logger

load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# КОНФИГУРАЦИЯ С ВАШИМИ ДАННЫМИ
BOT_TOKEN = os.getenv('MAX_BOT_TOKEN')
YANDEX_API_KEY = os.getenv('YANDEX_API_KEY').strip()
YANDEX_FOLDER_ID = os.getenv('YANDEX_FOLDER_ID').strip()

# bot = Bot(access_token=BOT_TOKEN)


async def download_file_by_url(url: str, destination: str):
    """Скачивание файла через внутреннюю авторизованную сессию бота aiomax."""
    logging.info(f"[Download] Безопасный запрос к CDN через bot.session...")
    session = getattr(bot, 'session', getattr(bot, 'client', None))

    if hasattr(session, 'get'):
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.read()
                logging.info(f"[Download] Файл успешно получен. Размер: {len(data)} байт.")
                with open(destination, "wb") as f:
                    f.write(data)
                return
            else:
                raise Exception(f"CDN вернул статус: {response.status}")
    raise Exception("Не удалось получить сессию бота для скачивания.")


async def convert_to_wav(source_path: str, dest_path: str) -> bool:
    """Конвертация аудио с детальным логированием веса файлов."""
    if not os.path.exists(source_path):
        logging.error(f"[🚨 ШАГ 2 - ОШИБКА] Исходный файл {source_path} не найден на диске!")
        return False
        
    in_size = os.path.getsize(source_path)
    logging.info(f"[🍏 ШАГ 2 - СКАЧАНО] Размер исходного файла: {in_size} байт.")
    
    try:
        process = await asyncio.create_subprocess_exec(
            "ffmpeg", "-y", "-i", source_path,
            "-c:a", "libopus",
            "-b:a", "16k",
            "-ar", "16000",
            "-ac", "1",
            dest_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            logging.error(f"[🚨 ШАГ 2 - FFmpeg Error] Код: {process.returncode}")
            logging.error(f"[FFmpeg Отладка]: {stderr.decode('utf-8', errors='ignore')}")
            return False
            
        if not os.path.exists(dest_path):
            logging.error("[🚨 ШАГ 2 - ОШИБКА] FFmpeg отработал, но выходной файл не создался!")
            return False
            
        out_size = os.path.getsize(dest_path)
        logging.info(f"[🍏 ШАГ 2 - КОНВЕРТАЦИЯ] Выходной файл успешно создан. Размер: {out_size} байт.")
        
        if out_size == 0:
            logging.error("[🚨 ШАГ 2 - КРИТИЧНО] FFmpeg создал пустой файл (0 байт)! Проверьте кодеки исходника.")
            return False
            
        return True
    except Exception as e:
        logging.error(f"[🚨 ШАГ 2 - ИСКЛЮЧЕНИЕ] {e}")
        return False


async def transcribe_voice_yandex(file_path: str) -> str:
    """Детальная пошаговая диагностика отправки в Yandex SpeechKit."""
    if not os.path.exists(file_path):
        logging.error(f"[🚨 ШАГ 3 - ОШИБКА] Файл {file_path} не найден на диске!")
        return ""
        
    file_size = os.path.getsize(file_path)
    logging.info(f"[🍏 ШАГ 3 - ПОДГОТОВКА] Файл готов к отправке. Размер: {file_size} байт.")
    
    # === ИНСПЕКЦИЯ КЛЮЧЕЙ НА СКРЫТЫЕ СИМВОЛЫ ===
    clean_key = YANDEX_API_KEY.strip().replace("\n", "").replace("\r", "")
    clean_folder = YANDEX_FOLDER_ID.strip().replace("\n", "").replace("\r", "")
    
    logging.info(f"[🔍 ИНСПЕКЦИЯ КЛЮЧА] Оригинальная длина ключа: {len(YANDEX_API_KEY)}, после очистки: {len(clean_key)}")
    logging.info(f"[🔍 ИНСПЕКЦИЯ КАТАЛОГА] Оригинальная длина ID: {len(YANDEX_FOLDER_ID)}, после очистки: {len(clean_folder)}")
    
    # 1. Мы убираем параметры из строки URL, передавая их в requests через словарь params.
    # Это на 100% страхует нас от обрезания строки символами амперсанда в Linux.
    url = "https://stt.api.cloud.yandex.net/speech/v1/stt:recognize"
    
    params = {
        "folderId": clean_folder,
        "lang": "ru-RU",
        "format": "oggopus"
    }
    
    headers = {
        "Authorization": f"Api-Key {clean_key}",
        "Content-Type": "audio/ogg; codecs=opus"
    }
    
    with open(file_path, "rb") as f:
        audio_data = f.read()
        
    logging.info(f"[🍏 ШАГ 3 - ОТПРАВКА] Отправка {len(audio_data)} байт аудио через requests.post...")
    
    try:
        # Выполняем синхронный запрос в изолированном потоке
        response = await asyncio.to_thread(
            requests.post,
            url,
            params=params,
            headers=headers,
            data=audio_data,
            timeout=15
        )
        
        logging.info(f"[🍏 ШАГ 4 - СЕРВЕР ЯНДЕКСА] Код ответа: {response.status_code}")
        logging.info(f"[🔍 ИНСПЕКЦИЯ СЕТИ] Заголовки ответа Яндекса: {dict(response.headers)}")
        
        if response.status_code == 200:
            result_json = response.json()
            return result_json.get("result", "").strip()
        else:
            logging.error(f"[🚨 ШАГ 4 - ОШИБКА API] Код {response.status_code}. Текст ответа: {response.text}")
            return ""
            
    except Exception as e:
        logging.error(f"[🚨 ШАГ 3 - КРИТИЧЕСКОЕ ИСКЛЮЧЕНИЕ] Ошибка: {e}")
        return ""
    

#@bot.on_message()
async def handle_message(update):
    message = update.message if hasattr(update, 'message') else update

    if not hasattr(message, 'body') or not message.body or not message.body.attachments:
        return

    audio_attachment = None
    for attachment in message.body.attachments:
        if type(attachment).__name__ == 'AudioAttachment':
            audio_attachment = attachment
            break

    if not audio_attachment:
        return

    logging.info(f"=== Обработка аудиосообщения ID: {message.id} ===")
    await message.send(f"🗣 **Распознаю Ваше голосовое сообщение...**")

    input_file = f"voice_input_{message.id}.ogg"
    converted_file = f"voice_ready_{message.id}.ogg"  # Сохраняем в эталонный .ogg контейнер

    try:
        file_url = getattr(audio_attachment, 'url', None)
        if not file_url:
            return

        # 1. Скачивание через сессию бота
        await download_file_by_url(file_url, input_file)

        # 2. Конвертация в эталонный OGG/Opus
        if await convert_to_wav(input_file, converted_file):
            # 3. Отправка в Яндекс
            text_result = await transcribe_voice_yandex(converted_file)
            logging.info(f"[Результат] Текст: '{text_result}'")

            if text_result:
                # await message.reply(f"🗣 **Текст сообщения:**\n\n{text_result}")
                return text_result

        await message.reply("❌ Не удалось распознать речь.")

    except Exception as e:
        logging.error(f"Критическая ошибка: {e}")
        await message.reply("❌ Ошибка при обработке аудиофайла.")
    finally:
        # Обязательная очистка временных файлов на диске
        for temp_file in [input_file, converted_file]:
            if os.path.exists(temp_file):
                os.remove(temp_file)


async def main():
    print("Бот MAX успешно запущен. Все цепочки авторизации настроены!")
    await bot.start_polling()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен.")






