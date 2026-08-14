import asyncio
import time
from aiomax.fsm import FSMCursor
#import logging
from bot.adapters.max.keyboards import next_to_education_kb, tomorrow_kb
from bot.adapters.max.create_bot import logger
from core.content import (
    get_another_emp_training_info_text,
    get_cel_and_prinsipes_text,
    get_change_course_text,
    get_change_date_text,
    get_first_mess_another_empl,
    get_first_mess_lawyer,
    get_start_text,
    get_about_company_text,
    get_sales_training_intro_text,
    get_sales_training_info_text,
    get_course_intro_text,
    get_block1_intro_text,
    get_block1_section1_intro_text,
    get_block1_section1_questions,
    format_block1_section1_question,
    format_block1_section1_result,
    get_start_text_another_employer,
    get_text_change_department,
    get_text_change_status,
)
from services.redis_storage import save_cursor

#logging.basicConfig(level=logging.INFO)


async def flow_start(send, course_name:str, status_user:str):
    """
    Стартовый сценарий:
    отправить приветственное сообщение в зависимости от названия курса обучения,
    переданного в аргументе.
    """
    #state_name = cursor.get_state()
    print(f'{status_user=}')
    if course_name == "Обучение по продажам":
        text = get_start_text(status_user)
    
    elif course_name == "Обучение по продукту":
        #text = get_start_text_another_employer()
        text = get_start_text(status_user)
        
    if course_name == "Обучение для юриста":
        text = get_start_text(status_user)
    
    #if state_name == "another_employer":
    await send(text=text)
     

async def flow_start_change_kb(send):
    """
    Стартовый сценарий:
    выбрать курс обучения.
    """
    logger.info('Стартовал')
    text = get_text_change_status()
    logger.info(f'{text=}')
    #text = get_change_course_text()
    await send(text)


    
async def flow_start_new_empl_change_kb(send, incomplete_flag: bool = False):
    """
    Стартовый сценарий:
    выбрать курс обучения для тех, кто уже есть в JSON.
    """
    logger.info("Стартовал")
    text = get_text_change_department()
    if incomplete_flag:
        text = text[9:]
    #text = get_change_course_text()
    await send(text)


async def flow_about_company(send):
    """
    Сценарий '🏢 О компании'.
    """
    text = get_about_company_text()
    info = get_change_date_text()
    prinsipes_text = get_cel_and_prinsipes_text()
    
    await send(text)
    await asyncio.sleep(5)  # 30 секунд !!!!!!
    await send(prinsipes_text)
    await asyncio.sleep(5) # 15
    
    tom_kb = tomorrow_kb
       
    logger.info("Пытаюсь отправить info")
    await send(info, with_keyboard=tom_kb)
    

async def flow_sales_training_intro(send, user_name: str = "коллега"):
    """
    Сценарий '💼 Обучение по продажам' (ШАГ 1 + инфо).
    """
    try:
        logger.info("[flow_sales_training_intro] стартовал")
        intro = get_sales_training_intro_text(user_name)
        #info = get_change_date_text()
        info = get_sales_training_info_text()
        logger.info(f"{intro=}\n{info=}")
        logger.info("Пытаюсь отправить intro")
        await send(intro, with_keyboard="clear")
        await asyncio.sleep(5)  # 30 секунд 
        # Паузы, задержки и т.п. — в адаптере (MAX), чтобы не блокировать CORE.
        next_kb = next_to_education_kb
        logger.info("Пытаюсь отправить info")
        await send(info, with_keyboard=next_kb)
    except Exception as e:
        logger.error(f"[flow_sales_training_intro] произошла ошибка {e}")



async def flow_another_emp_training_intro(send, user_name: str = "коллега"):
    """
    Сценарий '💼 Обучение по продукту' (ШАГ 1 + инфо).
    """
    try:
        logger.info("[flow_another_emp_training_intro] стартовал")
        intro = get_first_mess_another_empl()
        #intro = get_sales_training_intro_text(user_name)
        #info = get_change_date_text()
        info = get_another_emp_training_info_text()
        logger.info(f"{intro=}\n{info=}")
        logger.info("Пытаюсь отправить intro")
        await send(intro, with_keyboard="clear")
        await asyncio.sleep(5)  # 30 секунд 
        # Паузы, задержки и т.п. — в адаптере (MAX), чтобы не блокировать CORE.
        next_kb = next_to_education_kb
        logger.info("Пытаюсь отправить info")
        await send(info, with_keyboard=next_kb)
    except Exception as e:
        logger.error(f"[flow_another_emp_training_intro] произошла ошибка {e}")
        

async def flow_lawyer_training_intro(send, user_name: str = "коллега", user_id: int = 0):
    """
    Сценарий '💼 Обучение для юриста' (ШАГ 1 + инфо).
    """
    try:
        logger.info("[flow_lawyer_training_intro] стартовал")
        intro = get_first_mess_lawyer()
        #intro = get_sales_training_intro_text(user_name)
        #info = get_change_date_text()
        info = get_sales_training_info_text()
        logger.info(f"{intro=}\n{info=}")
        logger.info("Пытаюсь отправить intro")
        await send(intro, with_keyboard="clear")
        await asyncio.sleep(5)  # 30 секунд 
        # Паузы, задержки и т.п. — в адаптере (MAX), чтобы не блокировать CORE.
        next_kb = next_to_education_kb
        logger.info("Пытаюсь отправить info")
        await save_cursor(user_id, extra_data={"payload": "next_education"})
        await send(info, with_keyboard=next_kb)
    except Exception as e:
        logger.error(f"[flow_lawyer_training_intro] произошла ошибка {e}")
    

