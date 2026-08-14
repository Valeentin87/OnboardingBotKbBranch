import asyncio
import json
import redis.asyncio as redis  # <-- Важно: импортируем именно asyncio модуль
from aiomax.fsm import FSMCursor
from bot.adapters.max.create_bot import logger
#from aiomax import Bot, Dispatcher

# --- КОНФИГУРАЦИЯ ---
TOKEN = "YOUR_BOT_TOKEN"
REDIS_URL = "redis://localhost"

# Глобальная переменная для клиента Redis
redis_client = None

async def init_redis():
    """Инициализирует соединение с Redis. Вызывается при старте бота."""
    global redis_client
  
    # from_url работает точно так же
    redis_client = await redis.from_url("redis://localhost", decode_responses=True)
    print("✅ Redis подключен!")

async def close_redis():
    """Закрывает соединение при остановке бота."""
    global redis_client
    if redis_client:
        await redis_client.close()
        redis_client = None
        print("❌ Redis отключен")

# --- ФУНКЦИИ РАБОТЫ С СОСТОЯНИЕМ (CURSOR) ---

async def save_cursor(
    user_id: int, 
    state: dict | None = None, 
    extra_data: dict | None = None,
    ttl_seconds: int | None = None
                    ) -> None:
    """
    Сохраняет курсор в Redis.
    
    Приоритет аргументов:
    1. Если передан `state`: полная перезапись данных (extra_data игнорируется).
    2. Если передан только `extra_data`: чтение текущего состояния -> обновление -> запись.
    
    TTL (время жизни):
    - По умолчанию: 7 дней (604800 сек).
    - Можно переопределить через параметр ttl_seconds (например, 2-3 сек для временных данных).
    """
    if not redis_client:
        raise RuntimeError("Redis не инициализирован!")

    key = f"bot:cursor:{user_id}"
    
    # Устанавливаем TTL: если передано явно — используем его, иначе 7 дней
    default_ttl = 7 * 24 * 60 * 60  # 7 дней в секундах
    final_ttl = ttl_seconds if ttl_seconds is not None else default_ttl

    redis_data = {}

    if state is not None:
        # ПОЛНАЯ ЗАМЕНА: используем переданный словарь как есть
        redis_data = state
    else:
        # ОБНОВЛЕНИЕ: читаем текущее состояние и накладываем изменения
        current_raw = await redis_client.get(key)
        logger.info(f'{current_raw=}')
        
        if current_raw:
            try:
                redis_data = json.loads(current_raw)
            except json.JSONDecodeError:
                logger.warning(f"Некорректный JSON для пользователя {user_id}. Начинаем с нуля.")
                redis_data = {}
        else:
            redis_data = {}
            
        # Применяем дополнительные данные, если они есть
        if extra_data:
            redis_data.update(**extra_data)

    # Сериализуем и сохраняем с нужным TTL
    await redis_client.setex(key, final_ttl, json.dumps(redis_data, ensure_ascii=False))
    
    logger.debug(f"Сохранен курсор для user_id={user_id}, TTL={final_ttl} сек")


async def remove_repeat_flag(user_id: int):
    key = f"bot:cursor:{user_id}"
    
    # 1. Читаем текущее значение
    logger.info(f'Стартовал')
    raw_data = await redis_client.get(key)
    if not raw_data:
        return  # Ключа нет, нечего удалять
    
    try:
        # 2. Превращаем JSON в словарь
        data = json.loads(raw_data)
        
        # 3. Удаляем конкретное поле, если оно есть
        if "repeat_flag" in data:
            del data["repeat_flag"]
            
            # 4. Пишем обратно с тем же TTL (или новым)
            # Важно: setex перезапишет TTL. Если нужно сохранить старый TTL, 
            # придется отдельно делать EXPIRE после SET, либо хранить TTL в коде.
            # Для простоты ставим стандартный TTL 7 дней:
            ttl = 7 * 24 * 60 * 60 
            await redis_client.setex(key, ttl, json.dumps(data, ensure_ascii=False))
            logger.info(f"Поле 'repeat_flag' удалено для user_id={user_id}")
            
    except json.JSONDecodeError:
        logger.error("Некорректный JSON в Redis, сброс ключа")
        await redis_client.delete(key)




async def load_cursor(user_id: int):
    """Загружает курсор из Redis. Возвращает None, если нет записи."""
    if not redis_client:
        return None
        
    key = f"bot:cursor:{user_id}"
    raw_data = await redis_client.get(key)
    print(f'{raw_data=}')
    
    if not raw_data:
        return None
    
    try:
        return json.loads(raw_data)
    except json.JSONDecodeError:
        return None

    
async def get_value_from_redis(user_id: int, key: str):
    """Возвращает значение по ключу key, переданному в аргументе из базы данных  Redis"""
    try:
        redis_data = await load_cursor(user_id)
        print(f'{redis_data=}')
        if redis_data:
            return_data = redis_data.get(key)
            print(f'Возвращаем из redis_storage значение {key} равное {return_data}') 
            return return_data
    except Exception as e:
        print(f'Произошла ошибка {e}')

        
async def del_value_from_redis(user_id: int, key: str):
    try:
        logger.info("Стартовал")
        redis_data: dict = await load_cursor(user_id) or {}
        removed_value = redis_data.pop(key, None)
        logger.info(f"Удалили ключ '{key}' со значением {removed_value}")
        await save_cursor(user_id, state=redis_data)  # <-- передаём полное состояние
    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")


async def clear_cursor(user_id: int) -> bool:
    """
    Очищает значение по ключу bot:cursor:{user_id}, ОСТАВЛЯЯ сам ключ в Redis.
    Записывает пустой JSON объект {} с TTL 7 дней.
    """
    if not redis_client:
        raise RuntimeError("Redis не инициализирован!")

    key = f"bot:cursor:{user_id}"
    ttl_seconds = 7 * 24 * 60 * 60  # 7 дней
    
    # setex перезапишет существующее значение на пустой словарь {}
    await redis_client.setex(key, ttl_seconds, json.dumps({}, ensure_ascii=False))
    
    logger.info(f"✅ Значение для пользователя {user_id} очищено (ключ сохранен).")
    return True



# --- ЛОГИКА БОТА ---

# dp = Dispatcher()
# bot = Bot(token=TOKEN)

# @dp.command("start")
# async def cmd_start(ctx):
#     user_id = ctx.from_user.id
#     # При старте можно сбросить состояние или оставить старое
#     # Здесь мы просто показываем приветствие. 
#     # Старое состояние подхватится автоматически при первом нажатии кнопки.
#     await ctx.reply(
#         "Привет! Нажми кнопку ниже, чтобы начать навигацию.",
#         keyboard=create_keyboard(0)
#     )

# def create_keyboard(current_cursor: int):
#     from aiomax.types import CallbackButton, KeyboardBuilder
#     kb = KeyboardBuilder()
    
#     # Кнопка "Вперед" кодирует действие, но реальное состояние мы берем из БД
#     # Это страховка: если БД недоступна, кнопка все равно имеет смысл
#     kb.add(CallbackButton(text="➡️ Дальше", callback_data=f"nav:next:{current_cursor}"))
    
#     if current_cursor > 0:
#         kb.add(CallbackButton(text="↩️ Назад", callback_data=f"nav:prev:{current_cursor}"))
        
#     return kb.build()

# @dp.callback_query(lambda c: c.data.startswith("nav:"))
# async def handle_navigation(callback):
#     user_id = callback.from_user.id
#     action, direction, current_cursor_str = callback.data.split(":")
#     current_cursor = int(current_cursor_str)
    
#     # 1. ПЫТАЕМСЯ ЗАГРУЗИТЬ РЕАЛЬНОЕ СОСТОЯНИЕ ИЗ БД
#     state = await load_cursor(user_id)
    
#     # Если в БД есть состояние, используем его. Иначе используем то, что пришло в кнопке (страховка)
#     effective_cursor = state["cursor"] if state else current_cursor
    
#     # 2. ВЫЧИСЛЯЕМ НОВОЕ СОСТОЯНИЕ
#     new_cursor = effective_cursor + 1 if direction == "next" else effective_cursor - 1
    
#     # Корректировка границ (чтобы не ушел в минус)
#     if new_cursor < 0:
#         new_cursor = 0
        
#     # 3. СОХРАНЯЕМ ОБНОВЛЕННОЕ СОСТОЯНИЕ В БД
#     await save_cursor(user_id, new_cursor)
    
#     # 4. РЕДАКТИРУЕМ СООБЩЕНИЕ (или отправляем новое, если редактирование не удалось)
#     try:
#         await callback.message.edit_text(
#             f"Вы на шаге: {new_cursor}.\n(Реальное состояние восстановлено из БД)",
#             keyboard=create_keyboard(new_cursor)
#         )
#     except Exception as e:
#         # Если сообщение удалено пользователем или истекло, просто отправляем новое
#         await callback.message.answer(
#             f"Шаг обновлен: {new_cursor}. (Предыдущее сообщение недоступно)",
#             keyboard=create_keyboard(new_cursor)
#         )
        
#     await callback.answer()

# # --- ТОЧКА ВХОДА ---
# async def main():
#     # 1. Сначала подключаем Redis
#     await init_redis()
    
#     try:
#         # 2. Запускаем бота
#         await bot.run(dp)
#     finally:
#         # 3. При остановке (Ctrl+C) корректно закрываем Redis
#         await close_redis()

# if __name__ == "__main__":
#     asyncio.run(main())
