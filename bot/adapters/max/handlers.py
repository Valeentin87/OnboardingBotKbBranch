"""
Обработчики для MAX-бота.

Сейчас это слой-адаптер между core/ и конкретной библиотекой MAX (aiomax).
Пока нет реального Bot-объекта, описываем только функции и протокол.
"""

import asyncio
from datetime import datetime, timedelta
import json
import os
from pprint import pprint

from aiomax  import BotStartPayload, Message, Callback, Router, CommandContext, BotCommand
from aiomax.buttons import CallbackButton, KeyboardBuilder
from aiomax.fsm import FSMCursor, FSMStorage
from aiomax.filters import state
from aiomax import bot
#import logging


from bot.adapters.max.data_utils import format_progress_attempts, get_max_accuracy_item, load_user_data, save_reminder, save_user_data, validate_name_surname
from bot.adapters.max.test_utils import block_definition_func, get_block_2_test_1_quests, get_block_2_test_2_quests, get_block_2_test_3_quests, get_block_3_test_1_quests, get_block_3_test_2_quests, get_block_3_test_3_quests, get_block_3_test_4_quests, get_block_3_test_5_quests, get_block_3_test_6_quests, get_block_4_test_1_quests, get_block_4_test_2_quests, get_block_4_test_3_quests, get_block_4_test_4_quests, get_final_test_all_course_lawyer, get_final_test_block_1, get_final_test_block_1_lawyer, get_final_test_block_2, get_final_test_block_2_lawyer, get_final_test_block_3, get_final_test_block_3_lawyer, get_final_test_block_4, get_final_test_block_4_lawyer, get_final_test_block_5, get_final_test_block_5_lawyer, get_final_test_block_6, get_final_test_block_7, get_final_testing_data_module_0_kb, get_final_testing_data_module_1_kb, get_final_testing_data_module_2_kb, get_final_testing_data_module_3_kb, get_final_testing_data_module_4_kb, get_final_testing_data_module_5_kb, get_final_testing_data_module_6_kb, get_final_testing_data_module_7_kb, get_testing_data_1, get_testing_data_2, get_testing_data_3, get_testing_data_4, get_testing_data_5, get_testing_data_6, get_testing_data_module_0_test_1_kb, get_testing_data_module_0_test_2_kb, get_testing_data_module_0_test_3_kb, get_testing_data_module_0_test_4_kb, get_testing_data_module_0_test_5_kb, get_testing_data_module_1_test_1_kb, get_testing_data_module_1_test_2_kb, get_testing_data_module_1_test_3_kb, get_testing_data_module_1_test_4_kb, get_testing_data_module_1_test_5_kb, get_testing_data_module_1_test_6_kb, get_testing_data_module_2_test_1_kb, get_testing_data_module_2_test_2_kb, get_testing_data_module_2_test_3_kb, get_testing_data_module_2_test_4_kb, get_testing_data_module_2_test_5_kb, get_testing_data_module_3_test_1_kb, get_testing_data_module_3_test_2_kb, get_testing_data_module_3_test_3_kb, get_testing_data_module_3_test_4_kb, get_testing_data_module_3_test_5_kb, get_testing_data_module_4_test_1_kb, get_testing_data_module_4_test_2_kb, get_testing_data_module_4_test_3_kb, get_testing_data_module_4_test_4_kb, get_testing_data_module_5_test_1_kb, get_testing_data_module_5_test_2_kb, get_testing_data_module_5_test_3_kb, get_testing_data_module_5_test_4_kb, get_testing_data_module_6_test_1_kb, get_testing_data_module_6_test_2_kb, get_testing_data_module_6_test_3_kb, get_testing_data_module_6_test_4_kb, get_testing_data_module_7_test_1_kb, get_testing_data_module_7_test_2_kb, get_testing_data_module_7_test_3_kb, get_testing_data_module_7_test_4_kb
from bot.adapters.max.utils_FSM import AnotherEmployerStates, BranchKbStates, LawyerStates, OnboardingStates, TrainingStates, UserInfo
from bot.core.onboarding_flow import flow_about_company, flow_another_emp_training_intro, flow_branch_kb_training_intro, flow_lawyer_training_intro, flow_sales_training_intro, flow_start, flow_start_change_kb, flow_start_new_empl_change_kb
from bot.core.reg_managment_content import get_message_11_text, get_message_14_text, get_message_17_text, get_message_1_text, get_message_20_text, get_message_23_text, get_message_26_text, get_message_29_text, get_message_2_text, get_message_32_text, get_message_33_text, get_message_34_text, get_message_5_text, get_message_8_text, get_period_sender_text
from core.content import get_another_emp_intro_text, get_block1_intro_text, get_block1_intro_text_lawyer, get_block1_section1_intro_text, get_block1_section2_intro_text, get_block1_section_3_intro_text, get_block1_section_4_intro_text, get_block1_section_5_intro_text, get_block1_section_6_intro_text, get_block2_intro_text, get_block2_intro_text_lawyer, get_block2_section1_intro_text, get_block2_section_1_intro_text_lawyer, get_block2_section_2_intro_text, get_block2_section_2_intro_text_lawyer, get_block2_section_3_intro_text, get_block2_section_4_intro_text, get_block3_intro_text, get_block3_intro_text_lawyer, get_block3_section_1_intro_text, get_block3_section_2_intro_text, get_block3_section_3_intro_text, get_block3_section_4_intro_text, get_block3_section_5_intro_text, get_block3_section_6_intro_text, get_block4_intro_text, get_block4_intro_text_lawyer, get_block4_section_1_intro_text, get_block4_section_2_intro_text, get_block4_section_3_intro_text, get_block4_section_4_intro_text, get_block5_intro_text, get_block5_intro_text_lawyer, get_block5_intro_video1, get_block5_intro_video10, get_block5_intro_video11, get_block5_intro_video12, get_block5_intro_video13, get_block5_intro_video14, get_block5_intro_video15, get_block5_intro_video2, get_block5_intro_video3, get_block5_intro_video4, get_block5_intro_video5, get_block5_intro_video6, get_block5_intro_video7, get_block5_intro_video8, get_block5_intro_video9, get_block6_intro_text, get_block6_section_1_intro_text, get_block7_intro_text, get_change_course_text, get_course_intro_text, get_final_another_emp_text, get_final_intro_text, get_final_lawyer_text, get_first_day_congrats_text, get_first_mess_another_empl, get_module0_intro_text_kb_branch, get_module0_lesson1_intro_text_kb_branch, get_module0_lesson2_intro_text_kb_branch, get_module0_lesson3_intro_text_kb_branch, get_module0_lesson4_intro_text_kb_branch, get_module0_lesson5_intro_text_kb_branch, get_module1_intro_text_kb_branch, get_module1_lesson1_intro_text_kb_branch, get_module1_lesson2_intro_text_kb_branch, get_module1_lesson3_intro_text_kb_branch, get_module1_lesson4_intro_text_kb_branch, get_module1_lesson5_intro_text_kb_branch, get_module1_lesson6_intro_text_kb_branch, get_module2_intro_text_kb_branch, get_module2_lesson1_intro_text_kb_branch, get_module2_lesson2_intro_text_kb_branch, get_module2_lesson3_intro_text_kb_branch, get_module2_lesson4_intro_text_kb_branch, get_module2_lesson5_intro_text_kb_branch, get_module3_intro_text_kb_branch, get_module3_lesson1_intro_text_kb_branch, get_module3_lesson2_intro_text_kb_branch, get_module3_lesson3_intro_text_kb_branch, get_module3_lesson4_intro_text_kb_branch, get_module3_lesson5_intro_text_kb_branch, get_module4_intro_text_kb_branch, get_module4_lesson1_intro_text_kb_branch, get_module4_lesson2_intro_text_kb_branch, get_module4_lesson3_intro_text_kb_branch, get_module4_lesson4_intro_text_kb_branch, get_module5_intro_text_kb_branch, get_module5_lesson1_intro_text_kb_branch, get_module5_lesson2_intro_text_kb_branch, get_module5_lesson3_intro_text_kb_branch, get_module6_intro_text_kb_branch, get_module6_lesson1_intro_text_kb_branch, get_module6_lesson2_intro_text_kb_branch, get_module6_lesson3_intro_text_kb_branch, get_module6_lesson4_intro_text_kb_branch, get_module7_intro_text_kb_branch, get_module7_lesson1_intro_text_kb_branch, get_module7_lesson2_intro_text_kb_branch, get_module7_lesson3_intro_text_kb_branch, get_module7_lesson4_intro_text_kb_branch, get_reminder_text, get_start_text, get_text_change_department, get_text_change_status, get_text_for_add_educ, get_text_in_process, get_text_start_final_test_block_1, get_text_start_final_test_block_2, get_text_start_final_test_block_3, get_text_start_final_test_block_4, get_text_start_final_test_block_5, get_text_start_final_test_block_6, get_text_to_final_test_block_1, get_text_to_final_test_block_2, get_text_to_final_test_block_3, get_text_to_final_test_block_4, get_text_to_final_test_block_5, get_text_to_final_test_block_6, get_text_to_final_test_block_7, get_text_to_final_test_lawyer, get_text_to_test_after_lesson_kb, get_text_to_test_block_1_lawyer, get_to_final_intro_text_lawyer, get_tomorrow_reminder_text, get_training_step_3_text, go_to_test_1_text, kb_get_text_to_final_test_module_0, kb_get_text_to_final_test_module_1, kb_get_text_to_final_test_module_2, kb_get_text_to_final_test_module_3, kb_get_text_to_final_test_module_4, kb_get_text_to_final_test_module_5, kb_get_text_to_final_test_module_6, kb_get_text_to_final_test_module_7, kb_go_to_test_after_lesson, table_of_content_kb_branch, table_of_content_lawyer
from bot.adapters.max.keyboards import change_another_department_kb, change_course_kb, change_course_to_export_stat_kb, change_department_kb, change_status_kb, continue_studying_kb, education_kb, final_start_test_kb, final_test_kb, finish_studying_kb, main_menu_keyboard, main_one_kb, next_to_educ_to_part_kb, next_to_education_kb, regular_managment_kb, start_test_kb, test_abcd_keyboard, variants_questions_kb, yes_no_kb
#from services.claude_api import ClaudeService
from services.ExelStatisticGenerator import ExcelStatisticGenerator
from services.gigachat_api_last import GigaChatService
from services.debounce import debounce_button_max
from services.gamification import GamificationService
from services.rag_service import RAGService
from bot.adapters.max.create_bot import logger
from services.redis_storage import clear_cursor, del_value_from_redis, get_value_from_redis, load_cursor, remove_repeat_flag, save_cursor


#logging.basicConfig(level=logging.INFO)

REMINDERS_FILE = "data/reminders.json"
NAME_DATA_FILE = "data/name_surname.json"

COURSES_NAMES = {"Обучение по продажам": 'sales_training',
                 "Обучение по продукту": 'another_employee',
                 "Обучение для юриста": "lawyer",
                 "Регулярный менеджмент": "regular_managment",
                 "Обучение для конструкторов": "branch_kb"}


router = Router()


def get_current_course(cursor: FSMCursor):
    """Возвращает название курса обучения"""
    cursor_data = cursor.get_data()
    if cursor_data and 'current_course' in cursor_data:
        return cursor_data.get("current_course")
    else:
        return "Обучение по продажам"


@router.on_button_callback(lambda data: data.payload == "additional_education")
async def additional_education_handler(ctx: Callback, cursor: FSMCursor):
    """Обработчик нажатия на кнопку ДОПОЛНИТЕЛЬНОЕ ОБРАЗОВАНИЕ"""
    try:
        logger.info('Стартовал')
        await ctx.message.delete()
        text = get_text_for_add_educ()
        
        await ctx.message.send(text, keyboard=regular_managment_kb())
        
    except Exception as e:
        logger.error(f'Произошла ошибка {e}')


@router.on_button_callback(lambda data: data.payload == "sales_manager")
async def sales_manager_start_handl(ctx: Callback, cursor: FSMCursor, status_user: str = 'new_employer'):
    """Обработчик нажатия пользователем кнопки МЕНЕДЖЕР ПО ПРОДАЖАМ 
    при выборе курса обучения"""
    await ctx.message.delete()
    
    data = cursor.get_data()
    logger.info(f'{data=}\n{status_user=}')
    #status_user = data.get("status_user")
    if status_user == 'new_employer':
        cursor.change_data({"current_course": "Обучение по продажам"})
        await start_command(ctx, cursor, status_user)
    else:
        cursor.change_data({"current_course": "Обучение по продажам", "status_user": status_user})
        await start_command(ctx, cursor, status_user)
        
        
@router.on_button_callback(lambda data: data.payload == "another_employer")
async def another_employer_start_handl(ctx: Callback, cursor: FSMCursor, status_user: str = "new_employer"):
    """Обработчик нажатия пользователем кнопки ДРУГОЙ СОТРУДНИК 
    при выборе курса обучения"""
    logger.info('Стартовал')
    await ctx.message.delete()
    cursor_data = cursor.get_data()
    logger.info(f'{cursor_data=}')
    if not cursor_data:
        logger.warning('Возможно отсутствует cursor - обращаемся к Redis')
        cursor_redis_data = await load_cursor(ctx.user_id)
        logger.info(f'{cursor_redis_data=}')
        redis_data = cursor_redis_data.get("data", {})
        status_user = redis_data.get("status_user")
        cursor.change_data({"status_user": status_user, "current_course": "Обучение по продукту", "state_name": "another_employer" })
    else:
        status_user = cursor_data.get('status_user')
        logger.info(f'{status_user=}')
        cursor_data.update(current_course="Обучение по продукту")
        cursor.change_data(cursor_data)
        cursor.change_state(AnotherEmployerStates.user_type)
        extra_data = {"current_course": "Обучение по продукту", "state_name": "another_employer"}
        await save_cursor(ctx.user_id, extra_data=extra_data)
        
        
    
    
    await start_command(ctx, cursor, user_type = "another_employer", status_user = status_user)


@router.on_button_callback(lambda data: data.payload == "branch_kb")
async def branch_kb_start_handl(ctx: Callback, cursor: FSMCursor, status_user: str = "new_employer"):
    """Обработчик нажатия пользователем кнопки КОНСТРУКТОРСКИЙ ОТДЕЛ 
    при выборе курса обучения"""
    await ctx.message.delete()
        
    data = cursor.get_data()
    logger.info(f'{data=}\n{status_user=}')
    if data:
        await save_cursor(ctx.user_id, extra_data=data)
    #status_user = data.get("status_user")
    if status_user == 'new_employer':
        cursor.change_data({"current_course": "Обучение для конструкторов"})
        await start_command(ctx, cursor, "konstructor", status_user)
    else:
        cursor.change_data({"current_course": "Обучение для конструкторов", "status_user": status_user})
        await start_command(ctx, cursor, "konstructor", status_user)
   

async def lawyer_start_handl(ctx: Callback, cursor: FSMCursor, status_user: str = 'new_employer'):
    """Обработчик нажатия пользователем кнопки ЮРИДИЧЕСКИЙ ОТДЕЛ
    при выборе курса обучения"""
    await ctx.message.delete()
    
    data = cursor.get_data()
    logger.info(f'{data=}\n{status_user=}')
    if data:
        await save_cursor(ctx.user_id, extra_data=data)
    #status_user = data.get("status_user")
    if status_user == 'new_employer':
        cursor.change_data({"current_course": "Обучение для юриста"})
        await start_command(ctx, cursor, "lawyer", status_user)
    else:
        cursor.change_data({"current_course": "Обучение для юриста", "status_user": status_user})
        await start_command(ctx, cursor, "lawyer", status_user)
        

@router.on_button_callback(lambda data: data.payload == "change_course_name")
async def change_course_name_handl(ctx: Callback, cursor: FSMCursor):
    """Обработчик нажатия кнопки ВЫБРАТЬ ДРУГОЙ ОТДЕЛ"""
    await ctx.message.delete()
    cursor.change_data({"current_course" : None})
    cursor.clear_state()
    text = get_change_course_text()
    
    await ctx.send(text=text, keyboard=change_course_kb(), format='markdown')



@router.on_command('change_status')
async def change_status_command_handler(ctx: CommandContext, cursor: FSMCursor):
    """Обработчик команды change_status"""
    try:
        logger.info(f'[INFO][change_status_command_handler] Стартовал change_status_command_handler')
        text = get_text_change_status()
        kb = change_status_kb()
        await ctx.send(text, keyboard = kb)
    except Exception as e:
        logger.error(f'Произошла ошибка: {e}')


@router.on_button_callback(lambda data: data.payload in ["new_employer", "upper_qualification"])
async def change_status_handler(ctx: Callback, cursor: FSMCursor):
    """Обработчик нажатия на кнопку НОВЫЙ СОТРУДНИК или ПОВЫШЕНИЕ КВАЛИФИКАЦИИ"""
    try:
        logger.info('Стартовал')
        await ctx.message.delete()
        status_user = ctx.payload
        await save_cursor(ctx.user_id, extra_data = {"status_user": status_user})
        cursor_data = cursor.get_data()
        if not cursor_data:
            cursor_data = {}
        cursor_data.update(status_user = status_user)
        cursor.change_data(cursor_data)
        logger.info(f'{status_user=}\n{cursor_data=}')
        text = get_text_change_department()
        kb = change_department_kb()
        await ctx.send(text, keyboard = kb)
    except Exception as e:
        logger.error(f'Произошла ошибка: {e}')
                 

@router.on_bot_start()
@router.on_command('start')
async def start_command(ctx: CommandContext, cursor: FSMCursor, user_type:str = "manager", status_user: str = 'new_employer'):
    """Обработчик команды старт"""
    try:
        await save_cursor(ctx.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        text = get_text_change_status()
        kb = change_status_kb()
        
        logger.info(f'[INFO][start_command] Стартовал {status_user=}')
        user_data = load_user_data()
        user_id = str(ctx.user_id)
        logger.info(f'{user_id=}')
        await save_cursor(ctx.user_id, extra_data={"status_user": status_user})
        #cursor_data = cursor.get_data()
        logger.info(f'[INFO][start_command] {user_id=}')
        redis_data = await load_cursor(ctx.user_id)
        if user_id in user_data:
            first_name = user_data[user_id]["first_name"]
            second_name = user_data[user_id]["second_name"]
            logger.info(f'[INFO][start_command] Данные о пользователе уже есть в name_surname.json {user_id=}')

            #await ctx.send(f"Здравствуйте, {first_name} {second_name}!")
            
                
        else:
            # Если информации нет, запрашиваем имя и фамилию
            await ctx.send("Пожалуйста, введите ваше имя и фамилию в формате «Имя Фамилия»")
            await save_cursor(ctx.user_id, extra_data={"state_name": UserInfo.waiting_for_name_surname})
            cursor.change_state(UserInfo.waiting_for_name_surname)
            
            return
        
        logger.info(f'[INFO][start_command] Стартовал')
            
        # async def change_course_send(text: str):
        #     await ctx.send(text, keyboard=change_course_kb(), format='markdown')
            
        async def change_course_send(text: str):
            await ctx.send(text, keyboard=change_status_kb(), format='markdown')
            
        async def change_course_new_empl_send(text: str):
            await ctx.send(text, keyboard=change_department_kb(), format='markdown')
        
        async def send(text: str, cursor: FSMCursor = cursor):
            state = cursor.get_state() # изменил 12.07.26 !!!
            state_name = state.state if all([state, not isinstance(state, str)]) else state
            cursor_data = cursor.get_data()
            if not cursor_data:
                logger.warning('Возможно отсутствует cursor - обращаемся к Redis')
                logger.info('Пробуем получить state_name из Redis')
                state_name = await get_value_from_redis(ctx.user_id, 'state_name')
                logger.info('Пробуем получить status_user из Redis')
                status_user = await get_value_from_redis(ctx.user_id, 'status_user')
            else:
                status_user = cursor_data.get('status_user')          
            
            logger.info(f'{state_name=} {status_user=}')
            current_course = None
            if state_name == 'lawyer':
                current_course = "Обучение для юриста"
            elif state_name == "another_employer":
                current_course = "Обучение по продукту"
            elif state_name == 'konstructor':
                #logger.info('попали в условие state_name == "konstructor" ')
                current_course = "Обучение для конструкторов"
            else:
                current_course = "Обучение по продажам"
                
            #logger.info(f'Перед save_cursor {current_course=}')
            await save_cursor(ctx.user_id, extra_data={'state_name': state_name, 'status_user': status_user, 'current_course': current_course})
            
            if status_user == 'upper_qualification':
                text = get_start_text(status_user)
            if state_name == "another_employer":
                await ctx.send(text, keyboard=main_menu_keyboard(educ_button_name = "Обучение по продукту", status_user = status_user))
            elif state_name == 'lawyer':
                await ctx.send(text, keyboard=main_menu_keyboard(educ_button_name = "Обучение для юриста", status_user = status_user))
            elif state_name == 'konstructor':
                await ctx.send(text, keyboard=main_menu_keyboard(educ_button_name = "Обучение для конструкторов", status_user = status_user))
            else:
                await ctx.send(text, keyboard=main_menu_keyboard(educ_button_name = "Обучение по продажам", status_user = status_user))

                
        data = cursor.get_data()
        logger.info(f'{data=}')
        if data:
            current_status_user = data.get("status_user")
            if not current_status_user:
                data.setdefault("status_user", status_user)
                current_status_user = status_user
            
            logger.info(f'{current_status_user=}')
            
            cursor.change_data(data)
            
            if "current_course" in data and data.get("current_course") == "Обучение по продажам":
                course_name = data.get("current_course")
                logger.info(f'{course_name=}')
                await flow_start(send, course_name, current_status_user)
                return
            
            if "current_course" in data and data.get("current_course") == "Обучение по продукту":
                cursor.change_state(AnotherEmployerStates.user_type)
                await save_cursor(ctx.user_id, extra_data={'state_name': AnotherEmployerStates.user_type})
                course_name = data.get("current_course")
                await flow_start(send, course_name, status_user)
                return
            
            if "current_course" in data and data.get("current_course") == "Обучение для юриста":
                cursor.change_state(LawyerStates.user_type)
                await save_cursor(ctx.user_id, extra_data={'state_name': LawyerStates.user_type})
                course_name = data.get("current_course")
                logger.info(f'Перешли в состояние LawyerStates.user_type, ветка ЮРИСТ {course_name=}')
                await flow_start(send, course_name, status_user)
                return
            
            if "current_course" in data and data.get("current_course") == "Обучение для конструкторов":
                cursor.change_state(BranchKbStates.user_type)
                await save_cursor(ctx.user_id, extra_data={'state_name': BranchKbStates.user_type})
                course_name = data.get("current_course")
                logger.info(f'Перешли в состояние BranchKbStates.user_type, ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ {course_name=}')
                await flow_start(send, course_name, status_user)
                return
        
            logger.info(f"317 Проверяем наличие {user_id=} в progress.json")
            if user_id in ['51490094', '175082514', '20759321', '24297191', '228312484', '276950556', '49728997',
                            '85179182', '108241884', '152163122', '50076911', '219566997']:           
                await flow_start_new_empl_change_kb(change_course_new_empl_send, True)
                return
            else:
                await flow_start_change_kb(change_course_send)
                return 
        
        logger.info(f"326 Проверяем наличие {user_id=} в progress.json")
        data = {}
        data.setdefault("status_user", "new_employer")
        cursor.change_data(data)
        if user_id in ['51490094', '175082514', '20759321', '24297191', '228312484', '276950556', '49728997',
                        '85179182', '108241884', '152163122', '50076911', '219566997']:           
            await flow_start_new_empl_change_kb(change_course_new_empl_send, True)
            return 
        else:
            await flow_start_change_kb(change_course_send) 
          
    except Exception as e:
        logger.error(f'[ERROR][start_command] Произошла ошибка {e}')
    finally:
        await remove_repeat_flag(ctx.user_id)





@router.on_message(state(UserInfo.waiting_for_name_surname))
async def process_name_surname(message: Message, cursor: FSMCursor):
    
    try:
        logger.info('Стартовал')
        status_user = await get_value_from_redis(message.user_id, 'status_user')
        if not status_user:
            status_user = 'new_employer'
        current_course = await get_value_from_redis(message.user_id, 'current_course')
        if not current_course:
            current_course = 'Обучение по продажам'
        
        await save_cursor(message.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 4)    
        try:
            text = message.body.text.strip()
        except Exception:
            first_name = await get_value_from_redis(message.user_id, 'first_name')
            second_name = await get_value_from_redis(message.user_id, 'second_name')
            text = f'{first_name} {second_name}'

        if validate_name_surname(text):
            # Разделяем имя и фамилию
            try:
                first_name, second_name = text.split(' ', 1)
                await save_cursor(message.user_id, extra_data = dict(first_name = first_name, second_name = second_name))
            except ValueError:
                await message.send(
                "Неверный формат. Пожалуйста, введите имя и фамилию в формате «Имя Фамилия», "
                "используя только буквы и один пробел между ними."
            ) 

            # Сохраняем данные пользователя
            user_data = load_user_data()
            user_id = str(message.user_id)
            user_data[user_id] = {
                "first_name": first_name,
                "second_name": second_name
            }
            save_user_data(user_data)

            await message.send(f"Спасибо, {first_name}! Ваши данные сохранены.")
            cursor.clear_state()
            await save_cursor(message.user_id, state=dict(status_user = status_user, current_course = current_course, state_name = None))
            
            async def change_course_send(text: str):
                await message.send(text, keyboard=change_status_kb(), format="markdown")
            
            # async def send(text: str):
            #     await message.send(text, keyboard=main_menu_keyboard())

            await flow_start_change_kb(change_course_send)
        else:
            await message.send(
                "Неверный формат. Пожалуйста, введите имя и фамилию в формате «Имя Фамилия», "
                "используя только буквы и один пробел между ними."
            )
    except Exception as e:
        logger.error(f'Произошла ошибка: {e}')
    finally:
        await remove_repeat_flag(message.user_id)
                

@router.on_command('part2')
async def part2_command(ctx: CommandContext, cursor: FSMCursor):
    """Обработчик команды /part2 - для работы со вторым разделом"""
    try:
        logger.info(f'[INFO][part2_command] Стартовал')
        cursor.clear_state()
        await start_block_2_handler(ctx, cursor)
    except Exception as e:
        logger.error(f'[ERROR][part2_command] Произошла ошибка {e}')
        

@router.on_command('part3')
async def part3_command(ctx: CommandContext, cursor: FSMCursor):
    """Обработчик команды /part3 - для работы с третьим разделом"""
    try:
        logger.info(f'[INFO][part3_command] Стартовал')
        cursor.clear_state()
        await start_block_3_handler(ctx, cursor)
    except Exception as e:
        logger.error(f'[ERROR][part3_command] Произошла ошибка {e}')


@router.on_command('part4')
async def part4_command(ctx: CommandContext, cursor: FSMCursor):
    """Обработчик команды /part4 - для работы с четвёртым разделом"""
    try:
        logger.info(f'[INFO][part4_command] Стартовал')
        cursor.clear_state()
        await start_block_4_handler(ctx, cursor)
    except Exception as e:
        logger.error(f'[ERROR][part4_command] Произошла ошибка {e}')
        

@router.on_button_callback(lambda data: data.payload == 'raiting')
@router.on_command('rating')
async def raiting_command(ctx: CommandContext | Callback, cursor: FSMCursor):
    """Обработчик команды /raiting - для демонстрации рейтинга обучаемого"""
    try:
        logger.info(f'[INFO][raiting_command] Стартовал')
        cursor.clear_state()
        current_course = await get_value_from_redis(ctx.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        
        if isinstance(ctx, Callback):
            await ctx.message.delete()
        
        game = GamificationService(current_course)
              
        #course_name = "Обучение по продажам" if current_course != "Другой сотрудник" else "Другой сотрудник"
        course_name = current_course #if current_course != 'Обучение по продукту' else 'Другой сотрудник'
        logger.info(f'{course_name=}')
        if  course_name == 'Регулярный менеджмент':
            text_info = (
                '🏆 Рейтинг по курсу\n\n'
                'Для выбранного курса "Регулярный менеджмент" рейтинг не формируется, просьба перейти в "Главное меню".'
            )
            await ctx.send(text_info, keyboard = main_one_kb())
            return       
        # Получаем топ пользователей
        logger.info(f'[INFO][raiting_command] Получаем топ пользователей')
        leaderboard = game.get_all_users_progress(course_name)
        
        if not leaderboard:
            await ctx.send(
                "📊 **Рейтинг пока пуст**\n\n"
                "Пройдите обучение, чтобы попасть в рейтинг!",
                keyboard=main_menu_keyboard(current_course),
                format="markdown"
            )
            return
        
        logger.info(f'[INFO][raiting_command] Находим место текущего пользователя')
        # Находим место текущего пользователя
        user_rank = 0
        user_progress = None
        for i, user_data in enumerate(leaderboard, start=1):
            if user_data['user_id'] == ctx.user_id:
                user_rank = i
                user_progress = user_data
                break
        
        # Формируем текст рейтинга (топ-10)
        if course_name == "Другой сотрудник":
            course_name = "Обучение по продукту"
        rating_text = f"🏆 <b>Рейтинг по курсу</b>\n📚 {course_name}\n\n"
        
        # Показываем топ-10
        for i, user_data in enumerate(leaderboard[:10], start=1):
            logger.info(f'{user_data=}')
            # Эмодзи для топ-3
            medal = ""
            if i == 1:
                medal = "🥇 "
            elif i == 2:
                medal = "🥈 "
            elif i == 3:
                medal = "🥉 "
            
            # Отметка для текущего пользователя
            is_current_user = (user_data['user_id'] == ctx.user_id)
            user_marker = " ← Вы" if is_current_user else ""
            
            # Формируем кликабельный username
            username = user_data.get('username')
            user_id = user_data['user_id']
            logger.info(f"[INFO][raiting_command]  {user_id=}")
            
            if username:
                display_name = f'<a href="https://web.max.ru/?id={user_id}">{username}</a>'
            else:
                display_name = f"Пользователь #{user_id}"
                
            completed_lessons = user_data['lessons_completed']
            logger.info(f'{completed_lessons=}') 
            if current_course == 'Другой сотрудник':
                if int(completed_lessons) < 5:
                    completed_lessons = 0
                elif int(completed_lessons) < 10:
                    completed_lessons = 1
                elif int(completed_lessons) < 15:
                    completed_lessons = 2
                elif int(completed_lessons) < 20:
                    completed_lessons = 3
                elif int(completed_lessons) < 25:
                    completed_lessons = 4
                elif int(completed_lessons) < 30:
                    completed_lessons = 5
                elif int(completed_lessons) < 43:
                    completed_lessons = 6
                else:
                    completed_lessons = 7
            elif current_course == 'Обучение для конструкторов':
                if int(completed_lessons) < 13:
                    completed_lessons = 0
                elif int(completed_lessons) < 26:
                    completed_lessons = 1
                elif int(completed_lessons) < 37:
                    completed_lessons = 2
                elif int(completed_lessons) < 48:
                    completed_lessons = 3
                elif int(completed_lessons) < 57:
                    completed_lessons = 4
                elif int(completed_lessons) < 66:
                    completed_lessons = 5
                elif int(completed_lessons) < 75:
                    completed_lessons = 6
                elif int(completed_lessons) < 84:
                    completed_lessons = 7
                
                 
            elif current_course == 'Обучение для юриста':
                completed_lessons = int(int(completed_lessons) / 2)
                  
            
            
            rating_text += (
                f"{medal}<b>#{i}</b> {display_name} — "
                f"{user_data['accuracy_percent']:.1f}% "
                f"({completed_lessons} уроков){user_marker}\n"
            )
        
        # Если пользователь не в топ-10, показываем его место отдельно
        if user_rank > 10:
            username = user_progress.get('username')
            user_id = user_progress['user_id']
            logger.info(f"[INFO][raiting_command]  {user_id=}")
            completed_lessons = user_progress['lessons_completed']
            logger.info(f'{completed_lessons=}') 
            if current_course == 'Другой сотрудник':
                if int(completed_lessons) < 5:
                    completed_lessons = 0
                elif int(completed_lessons) < 10:
                    completed_lessons = 1
                elif int(completed_lessons) < 15:
                    completed_lessons = 2
                elif int(completed_lessons) < 20:
                    completed_lessons = 3
                elif int(completed_lessons) < 25:
                    completed_lessons = 4
                elif int(completed_lessons) < 30:
                    completed_lessons = 5
                elif int(completed_lessons) < 43:
                    completed_lessons = 6
                else:
                    completed_lessons = 7 
            
            
            if username:
                display_name = f'<a href="https://web.max.ru/?id={user_id}">{username}</a>'
            else:
                display_name = f"Пользователь #{user_id}"
            
            rating_text += f"\n...\n"
            rating_text += (
                f"<b>#{user_rank}</b> {display_name} — "
                f"{user_progress['accuracy_percent']:.1f}% "
                f"({completed_lessons} уроков) ← <b>Вы</b>\n"
            )
        
        # Если пользователь ещё не в рейтинге
        if user_rank == 0:
            rating_text += "\n_Вы ещё не начали обучение. Пройдите первый урок, чтобы попасть в рейтинг!_"
        
        await ctx.send(rating_text, format="html", keyboard=main_menu_keyboard(current_course))
        
    except Exception as e:
        logger.error(f'[ERROR][raiting_command] Произошла ошибка {e}')


FILE_PATH = 'data/statistics.xlsx'


def add_timestamp_to_filename(filename: str = FILE_PATH):
    # Получаем текущую дату и время
    now = datetime.now()
    
    # Форматируем дату и время в нужный вид: ДД_ММ_ГГГГ_time_ЧЧ_ММ
    timestamp = now.strftime("%d_%m_%Y_time_%H_%M")
    
    # Разделяем имя файла и расширение
    if '.' in filename:
        name, extension = filename.rsplit('.', 1)
        new_filename = f"{name}_{timestamp}.{extension}"
    else:
        # Если расширения нет
        new_filename = f"{filename}_{timestamp}"
    
    return new_filename



@router.on_button_callback(lambda data: data.payload == 'all_courses')
async def all_courses_stat_info_handler(ctx: CommandContext, cursor: FSMCursor):
    """Обработчик нажатия на кнопку ПО ВСЕМ КУРСАМ"""
    logger.info(f'Приступаем к формированию статистики прохождения обучения по всем курсам')
    
    game = GamificationService()
    
    data = game._load_data()
    data_to_exel = {}
    logger.info(f'Убираем лишнюю информацию из data - ключи lesson_results и значения по ним')
    
    users_data = {}
    for user, user_data in data.copy().items():
        #del user_data['lesson_results']
        users_data.setdefault(user, user_data)
    pprint(users_data)
    
    logger.info(f'Для каждого пользователя получаем результат прохождения обучения по курсам')
    for user_id, education_info in users_data.items():
        last_first_user_name = f"{education_info.get('user_info')['last_name']} {education_info.get('user_info')['first_name']}"
        if user_id not in data_to_exel:
            data_to_exel.setdefault((user_id, last_first_user_name))
        current_user_result = game.get_info_to_exel_for_user(user_id=int(user_id), education_info=education_info)
        data_to_exel[(user_id, last_first_user_name)] = current_user_result
    
    logger.info(f'{data_to_exel=}')
    pprint(data_to_exel)
    
    excel_gen = ExcelStatisticGenerator(data_to_exel)
    
    file_path = add_timestamp_to_filename()
    
    #excel_gen.generate_excel("data/statistics.xlsx")
    excel_gen.generate_excel(file_path)
    
    if not os.path.exists(file_path):
        await ctx.send(f"❌ Файл {file_path} не найден в папке data.")
        return
    
    try:
        # Открываем файл в бинарном режиме
        with open(file_path, 'rb') as file:
            # Отправляем документ в чат
            attachment = await ctx.bot.upload_file(
                file_path
            )
            await ctx.send('Статистика прохождения обучения', attachments=attachment)
        await ctx.send("Для продолжения нажмите ниже", keyboard=main_one_kb())
    except Exception as e:
        await ctx.send(f"❌ Произошла ошибка при отправке файла: {e}")

    
    
    #pprint(data_to_exel)

@router.on_button_callback(lambda data: data.payload.startswith('export_data'))
async def current_course_stat_info_handler(callback: Callback, cursor: FSMCursor):
    course = callback.payload.split('::')[1]
    logger.info(f'{course=}')
        
    course_name = next(key for key, value in COURSES_NAMES.items() if value == course)
    
    logger.info(f'{course_name=}')
    
    logger.info(f'Приступаем к формированию статистики прохождения обучения по курсу: {course_name}')
    
    game = GamificationService()
    
    data = game._load_data()
    data_to_exel = {}
    logger.info(f'Убираем лишнюю информацию из data - ключи lesson_results и значения по ним')
    
    users_data = {}
    for user, user_data in data.copy().items():
        #del user_data['lesson_results']
        users_data.setdefault(user, user_data)
    pprint(users_data)
    
    logger.info(f'Для каждого пользователя получаем результат прохождения обучения по курсам')
    for user_id, education_info in users_data.items():
        last_first_user_name = f"{education_info.get('user_info')['last_name']} {education_info.get('user_info')['first_name']}"
        if user_id not in data_to_exel:
            data_to_exel.setdefault((user_id, last_first_user_name))
        current_user_result = game.get_info_to_exel_for_user(user_id=int(user_id), education_info=education_info, course_name=course_name, all_courses_flag=False)
        data_to_exel[(user_id, last_first_user_name)] = current_user_result
    
    logger.info(f'{data_to_exel=}')
    pprint(data_to_exel)
    
    excel_gen = ExcelStatisticGenerator(data_to_exel)
    
    file_path = add_timestamp_to_filename()
    
    #excel_gen.generate_excel("data/statistics.xlsx")
    logger.info(f'{file_path=}')
    try:
        excel_gen.generate_excel(file_path)
    except Exception as e:
        logger.error(f'При генерации файла статистики произошла ошибка {e}')
    
    
    if not os.path.exists(file_path):
        await callback.send(f"❌ Файл {file_path} не найден в папке data.")
        return
    
    try:
        # Открываем файл в бинарном режиме
        with open(file_path, 'rb') as file:
            # Отправляем документ в чат
            attachment = await callback.bot.upload_file(
                file_path
            )
            await callback.send('Статистика прохождения обучения', attachments=attachment)
        await callback.send("Для продолжения нажмите ниже", keyboard=main_one_kb())
    except Exception as e:
        await callback.send(f"❌ Произошла ошибка при отправке файла: {e}")

    
        
        

@router.on_button_callback(lambda data: data.payload == 'my_progress')
@router.on_command("my_progress")
async def my_progress_handler(ctx: CommandContext | Callback, cursor: FSMCursor):
    """Реализация логики прогресса ученика"""
    try:
        logger.info(f'[INFO][my_progress_handler] Стартовал')
        await save_cursor(ctx.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        current_course = await get_value_from_redis(ctx.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        logger.info(f'{current_course=}')
              
        if isinstance(ctx, Callback):
            await ctx.message.delete()
        
        game = GamificationService(current_course)
            
        #course_name = current_course #if current_course != 'Обучение по продукту' else 'Другой сотрудник'
        
        # if current_course == 'Другой сотрудник':
        #     course_name = current_course
        progress = game.get_user_progress(ctx.user_id, current_course)
        logger.info(f'{current_course=}\n{progress=}')
        
        logger.info(
            'Реализуем логику отображения прогресса в зависимости от того, кто его запрашивает'
            'Для админов будет реализована логика формирования Exel файла'
            )
        
        user_id = str(ctx.user_id)
        user_data = load_user_data()
        logger.info(f'{user_data=}')
              
        if user_id in user_data:
            first_name = user_data[user_id]["first_name"]
            second_name = user_data[user_id]["second_name"]
            
        if isinstance(progress, tuple):
            logger.info(f'[INFO][my_progress_handler] {first_name} {second_name} еще не прошел до конца курс')
            
            completed_lesson = progress[1]['lessons_completed']
            logger.info(f'{completed_lesson=}')
            # if current_course == 'Другой сотрудник':
            #     if int(completed_lesson) < 5:
            #         completed_lesson = 0
            #     elif int(completed_lesson) < 10:
            #         completed_lesson = 1
            #     elif int(completed_lesson) < 15:
            #         completed_lesson = 2
            #     elif int(completed_lesson) < 20:
            #         completed_lesson = 3
            #     elif int(completed_lesson) < 25:
            #         completed_lesson = 4
            #     elif int(completed_lesson) < 30:
            #         completed_lesson = 5
            #     elif int(completed_lesson) < 43:
            #         completed_lesson = 6
            #     else:
            #         completed_lesson = 7
            
            text = (
                f"📊 <b>{first_name} {second_name}</b>\n\n"
                f"📚 <b>Курс:</b> {current_course}\n\n"
                f"✅ <b>Уроков пройдено:</b> {completed_lesson} / {progress[1]['total_lessons']}\n"
                f"📈 <b>Процент правильных ответов:</b> {progress[1]['accuracy_percent']:.1f}%\n\n"
                f"⚠️ Вы ещё ни разу не прошли курс до завершения ⚠️\n"
                f"<i>Продолжайте обучение для повышения результатов!</i>"
            )
        else:
            text = format_progress_attempts(progress)
        
        await ctx.send(text, format="html", keyboard=education_kb(True))
            
        
    except Exception as e:
        logger.error(f'[ERROR][my_progress_handler] Произошла ошибка {e}')
    finally:
        await remove_repeat_flag(ctx.user_id)
        


@router.on_button_callback(lambda data: data.payload == 'send_question')
@router.on_command("send_question")
async def answer_to_send_question(ctx: CommandContext | Callback, cursor: FSMCursor):
    """Активация AI-ассистента с базой знаний"""
    try:
        logger.info(f'[INFO][answer_to_send_question] Стартовал')
        state = cursor.get_state() # изменил 12.07.26 !!!!!
        state_name = state.state if all([state, not isinstance(state, str)]) else state
        cursor_data = cursor.get_data()
        logger.info(f'{state_name=} {cursor_data=}')
        current_course = await get_value_from_redis(ctx.user_id, 'current_course')
        logger.info(f'787 {current_course=}')
        branch_name = ''
        if not current_course:
            current_course = cursor_data.get('current_course')
        if current_course in ['Обучение по продажам', 'Другой сотрудник', 'Обучение по продукту']:
            branch_name = 'sales_training'
        elif current_course == 'Обучение для юриста':
            branch_name = 'lawyer'
        elif current_course == 'Регулярный менеджмент':
            branch_name = 'regular_managment'
        elif current_course == 'Другой сотрудник':
            branch_name = 'another_employer'
        elif current_course == 'Обучение для конструкторов':
            branch_name = 'branch_kb'
        if isinstance(ctx, Callback):
            await ctx.message.delete()
        # Проверяем загрузку базы знаний
        await save_cursor(ctx.user_id, extra_data={'branch_name': branch_name})
        rag = RAGService(branch_name=branch_name)
        stats = rag.get_stats()
        
        if not stats['is_loaded']:
            await ctx.send(
                "❌ База знаний не загружена. Обратитесь к администратору.",
                format='html',
                keyboard=education_kb(True)
            )
            return
        
        logger.info(f'882 {current_course=}')
        
        if current_course in ['Обучение по продажам', 'Другой сотрудник', 'Обучение по продукту']:
           
            await ctx.send(
                "🤖 <b>AI-ассистент компании</b>\n\n"
                f"📚 База знаний загружена ({stats['total_size']} символов)\n\n"
                "Задавайте вопросы о компании, продукции или процессах.\n"
                "Я буду отвечать на каждый ваш вопрос.\n\n"
                "<i>Например:</i>\n"
                "· О чем говорит ФЗ-123?\n"
                "· Что такое кремнезольная технология?\n"
                "· Какая гарантия на продукцию?\n\n"
                "Напишите ваш вопрос 👇\n\n"
                "Для выхода нажмите <b>🏠 Главное меню</b>",
                format='html',
                keyboard=education_kb(True, True)
            )
        elif current_course == 'Обучение для юриста':
            await ctx.send(
                "🤖 <b>AI-ассистент компании</b>\n\n"
                f"📚 База знаний загружена ({stats['total_size']} символов)\n\n"
                "Задавайте вопросы о компании, продукции или процессах.\n"
                "Я буду отвечать на каждый ваш вопрос.\n\n"
                "<i>Например:</i>\n"
                "· Где хранятся учредительные документы?\n"
                "· Какие шаблонные договоры?\n"
                "· Кто подписывает документы по ЭДО?\n\n"
                "Напишите ваш вопрос 👇\n\n"
                "Для выхода нажмите <b>🏠 Главное меню</b>",
                format='html',
                keyboard=education_kb(True, True)
            )
        elif current_course == 'Регулярный менеджмент':
            await ctx.send(
               '🤖 <b>AI-ассистент компании</b>\n\n'
                f'📚 База знаний загружена ({stats["total_size"]} символов)\n\n'
                'Задавайте вопросы о компании, продукции или процессах.\n'
                'Я буду отвечать на каждый ваш вопрос.\n\n'
                '<i>Например:</i>\n'
                '· Что такое "Ошибка" и "Проступок"?\n'
                '· Что такое парадигмы в контексте компании?\n'
                '· Что понимается под термином «препятствие»?\n\n'
                'Напишите ваш вопрос 👇\n\n'
                'Для выхода нажмите <b>🏠 Главное меню</b>',
                format='html',
                keyboard=education_kb(True, True) 
            )
        elif current_course == 'Обучение для конструкторов':
            await ctx.send(
                '🤖 <b>AI-ассистент компании</b>\n\n'
                f'📚 База знаний загружена ({stats["total_size"]} символов)\n\n'
                'Задавайте вопросы о компании, продукции или процессах.\n'
                'Я буду отвечать на каждый ваш вопрос.\n\n'
                '<i>Например:</i>\n'
                '· Как пользоваться Glass Builder?\n'
                '· Что значит СП 2.13130.2020?\n'
                '· Как закрывать задачу в Б24?\n\n'
                'Напишите ваш вопрос 👇\n\n'
                'Для выхода нажмите <b>🏠 Главное меню</b>',
                format='html',
                keyboard=education_kb(True, True) 
            )
            
        cursor.change_state(TrainingStates.asking_ai)
        await save_cursor(ctx.user_id, extra_data={'state_name': TrainingStates.asking_ai})
        
        
    except Exception as e:
        logger.error(f'[ERROR][answer_to_send_question] Произошла ошибка: {e}')


@router.on_button_callback(state(TrainingStates.asking_ai), lambda data: data.payload == 'main_menu_without_ai')
async def exit_ai_handler(callback: Callback, cursor: FSMCursor):
    """Выход из режима AI-ассистента"""
    try:
        logger.info(f'[INFO][exit_ai_handler] Стартовал')
        await save_cursor(callback.user_id, extra_data = {'exit_ai_flag': True}) 
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)    
        # if await debounce_button(message, state):
        #     return

        await callback.message.delete()
        current_course = get_current_course(cursor)
        cursor.clear_state()
        await callback.send(
            "✅ Вы вышли из режима AI-ассистента",
            keyboard=main_menu_keyboard(current_course)
        )
        return
    
    except Exception as e:
        logger.error(f'[ERROR][exit_ai_handler] Произошла ошибка: {e}')
    finally:
        await remove_repeat_flag(callback.user_id)
        

@router.on_message(state(TrainingStates.asking_ai))
async def process_ai_question_handler(message: Message, cursor: FSMCursor):
    """Обработка вопроса через RAG + Claude (непрерывный диалог)"""
       
    # Показываем процесс
    logger.info(f'[INFO][process_ai_question_handler] Стартовал')
    state = cursor.get_state() # изменил 12.07.26 !!!!!
    state_name = state.state if all([state, not isinstance(state, str)]) else state
    cursor_data = cursor.get_data()
    logger.info(f'{state_name=} {cursor_data=}' )
    current_course = await get_value_from_redis(message.user_id, 'current_course')
    if not current_course:
        current_course = cursor_data.get('current_course')
    if current_course in ['Обучение по продажам', 'Другой сотрудник', 'Обучение по продукту']:
        branch_name = 'sales_training'
    elif current_course == 'Обучение для юриста':
        branch_name = 'lawyer'
    elif current_course == 'Регулярный менеджмент':
        branch_name = 'regular_managment'
    elif current_course == 'Обучение для конструкторов':
        branch_name = 'branch_kb'
    thinking_msg = await message.send("🔍 Ищу информацию в базе знаний...")
    
    try:
        rag = RAGService(branch_name=branch_name)
        
        text = message.body.text
        logger.info(f'[INFO][process_ai_question_handler] {text=}')
        
        answer = await rag.answer_question(text)
        
        await thinking_msg.delete()
        
        # Форматируем ответ
        response_text = f"💡 **Ответ:**\n\n{answer}\n\n➡️ Задайте следующий вопрос или нажмите 🏠 **Главное меню**"
        
        
        await message.send(response_text, format='markdown', keyboard=education_kb(True, True))
        
        
    except Exception as e:
        await thinking_msg.delete()
        print(f"❌ Ошибка обработки вопроса: {e}")
        logger.error(f'[ERROR][process_ai_question_handler] Произошла ошибка: {e}')
        await message.send(
            "❌ Произошла ошибка. Попробуйте задать вопрос ещё раз или нажмите <b>🏠 Главное меню</b>",
            format="html",
            keyboard=education_kb(True, True)
            )
        # НЕ очищаем state - даём пользователю попробовать снова


@router.on_command("home")
@router.on_button_callback(lambda data: data.payload == 'main_menu')        
async def go_to_main_menu_handler(callback: Callback, cursor: FSMCursor):
    """Обработчик нажатия кнопки перехода в Главное меню"""
    try:
        await callback.message.delete()
    except Exception as e:
        logger.error(f'Ошибка при удалении сообщения: {e}')
    finally:    
        try:
            current_course = await get_value_from_redis(callback.user_id, 'current_course')
            if not current_course:
                current_course = get_current_course(cursor)
            logger.info(f'{current_course=}')
            cursor_data = cursor.get_data()
            logger.info(f'{cursor_data=}')
            if cursor_data:
                status_user = cursor_data.get("status_user") if cursor_data.get("status_user") else 'new_employer'
            else:
                status_user = await get_value_from_redis(callback.user_id, 'status_user')
                if not status_user:
                    status_user = 'new_employer'
            logger.info(f'{status_user=}')
            logger.info(f'{current_course=}')
            cursor.clear()
            cursor.change_data({"current_course": current_course, "status_user": status_user})
            
            await callback.send("Вернулись в главное меню, выберите одно из действий 👇", keyboard=main_menu_keyboard(current_course, status_user))
            return
        except Exception as e:
            logger.error(f'[go_to_main_menu_handler] произошла ошибка {e}')    

        
@router.on_command("export_stats")
async def export_stats(message: Message):
    """Экспорт статистики всех пользователей (только для админа)"""
    try:
        # ⚙️ ЗАМЕНИ на свой MAX ID
        logger.info(f'[INFO][export_stats] Стартовал')
        ADMIN_IDS = [51490094, 175082514, 20759321, 85179182] #[175082514]  # Твой ID
        
        user_id = message.user_id
        logger.info(f'Проверим id пользователя на принадлежность к ADMIN')
        
        if user_id not in ADMIN_IDS:
            logger.warning(f'Ваш max_id равен: {message.user_id}')
            await message.send("⛔ У вас нет доступа к этой команде")
            return
        
        game = GamificationService()
        
        all_courses_name = game.get_all_courses_name()
        logger.info(f'{all_courses_name=}')
               
        await message.send(
            text='Выберите название курса, по которому хотите получить статистику, либо нажмите <b>ПО ВСЕМ КУРСАМ</b> для выгрузки всей статистики:',
            keyboard=change_course_to_export_stat_kb(all_courses_name),
            format='html'
        )
        
        return
                
    except Exception as e:
        logger.error(f'[ERROR][export_stats] Произошла ошибка: {e}')
        

async def send(message: Message | Callback, out: str, with_keyboard: bool = False):
        try:
            logger.info("[send] стартовала функция отправки сообщения")
            if with_keyboard == "clear":
                if isinstance(message, Message):
                    logger.info("отвечаем на Message без клавиатуры")
                    await message.send(out)
                else:
                    logger.info("отвечаем на Callback без клавиатуры")
                    #await message.answer(out)
                    await message.send(out)
            elif callable(with_keyboard):
                logger.info("В качестве параметра для клавиатуры передана функция")
                kb = with_keyboard()
                if isinstance(message, Message):
                    logger.info("отвечаем на Message и прикрепляем клавиатуру")
                    await message.send(out, keyboard=kb)
                else:
                    logger.info("отвечаем на Callback и прикрепляем клавиатуру")
                    await message.send(out, keyboard=kb)
            else:
                kb = main_menu_keyboard()
                if isinstance(message, Message):
                    logger.info("отвечаем на Message и приклепляем главную клавиатуру")
                    await message.send(out, keyboard=kb)
                else:
                    logger.info("отвечаем на Callback и прикрепляем главную клавиатуру")
                    #await message.answer(out, keyboard=kb)
                    await message.send(out, keyboard=kb)
        except Exception as e:
            logger.error(f"[SEND] произошла ошибка {e}")

# ниже нужно раскомментировать
   
@router.on_button_callback(lambda data: data.payload == 'about_company')
async def about_company_handler(callback: Callback, cursor: FSMCursor):
    """Обработчик нажатия на кнопку 🏢 О компании """
    try:
        
        state = cursor.get_state() # изменил 12.07.26 !!!!!
        state_name = state.state if all([state, not isinstance(state, str)]) else state
        logger.info(f'{state_name=}')
        
        await flow_about_company(lambda t, with_keyboard="clear": send(callback, t, with_keyboard))
        
        cursor.change_state(OnboardingStates.waiting_for_start_date)
        await save_cursor(callback.user_id, extra_data={"state_name": OnboardingStates.waiting_for_start_date, "payload": "tomorrow", "second_payload": "change_date"})
        logger.info(f"[about_company_handler] состояние для пользователя {callback.user.user_id} поменяно на `waiting_for_start_date`")
        return
    except Exception as e:
        logger.error(f'Произошла ошибка {e}')

    
@router.on_button_callback(state(OnboardingStates.waiting_for_start_date), lambda data: data.payload == 'tomorrow')
async def start_tomorrow_handler(callback: Callback, cursor: FSMCursor):
    """Обработчик нажатия на кнопку `🚀 Выхожу завтра`"""
    try:
        logger.info('Стартовал')
        await save_cursor(callback.user_id, extra_data = {'tomorrow_flag': True})
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        cursor_data = cursor.get_data()
        logger.info(f'{cursor_data=}')
        
        # Пользователь выходит завтра - сразу присылаем напоминание   
        tomorrow = datetime.now() + timedelta(days=1)
        date_str = tomorrow.strftime("%d.%m")
        
        # if await debounce_button_max(callback, cursor=cursor):
        #     logger.info(f"[start_tomorrow_handler] Идет обработка нажмите позднее")
        #     return
        
        # Сохраняем напоминание и СРАЗУ помечаем как отправленное
        logger.info(f"[start_tomorrow_handler] Сохраняем напоминание и СРАЗУ помечаем как отправленное")
        os.makedirs("data", exist_ok=True)
        
        reminders = {}
        if os.path.exists(REMINDERS_FILE):
            with open(REMINDERS_FILE, 'r', encoding='utf-8') as f:
                reminders = json.load(f)
        
        # reminders[str(callback.user.user_id)] = {
        #     "start_date": date_str,
        #     "reminder_sent": True  # ← Сразу помечаем как отправленное
        # }
        
        reminders[str(callback.user_id)] = {
            "start_date": date_str,
            "reminder_sent": True  # ← Сразу помечаем как отправленное
        }
        
        with open(REMINDERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(reminders, f, ensure_ascii=False, indent=2)
        logger.info(f"[start_tomorrow_handler] Напоминание сохранено и СРАЗУ помечено как отправленное")
        
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = cursor_data.get("current_course")
        # Сразу отправляем напоминание
                
        if current_course == "Обучение по продукту":
            cursor.change_state(AnotherEmployerStates.user_type)
            pass # возможно нужна строка await save_cursor(callback.user_id, extra_data={"payload": ......"})
            #current_course = "Обучение по продукту"
        
        if current_course == "Обучение для юриста":
            cursor.change_state(LawyerStates.user_type)
            current_course = "Обучение для юриста"
            await save_cursor(callback.user_id, extra_data={"payload": "lawyer_educ"})
        
        if current_course == "Обучение для юриста":
            cursor.change_state(BranchKbStates.user_type)
            current_course = "Обучение для конструкторов"
            await save_cursor(callback.user_id, extra_data={"payload": "konstructor_educ"})
            
        text = get_tomorrow_reminder_text(date_str, current_course)
        
        await callback.send(text, keyboard=education_kb(current_cource = current_course))
        #cursor.clear()
    except Exception as e:
        logger.error(f"[start_tomorrow_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)
        
from services.debounce import debounce_button_max

@router.on_button_callback(state(OnboardingStates.waiting_for_start_date), lambda data: data.payload == 'change_date')
async def change_date_handler(callback: Callback, cursor: FSMCursor, without_cursor_flag: bool = False):
    """Обработчик нажатия на кнопку `🚀 Указать дату`"""
    try:
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[change_date_handler] Идет обработка нажмите позднее")
        #     return
        logger.info(f'Стартовал')
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)    
        if not without_cursor_flag:     
            await callback.send(
        "📝 Напишите дату вашего первого рабочего дня в формате ДД.ММ\n\n"
        "Например: 07.02"
        )
        else:
            await callback.send(
            "📝 Напишите дату вашего первого рабочего дня в формате ДД.ММ\n\n"
            "Например: 07.02, либо **Завтра**, если планируете выйти завтра"
            )
    except Exception as e:
        logger.error(f"[start_tomorrow_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)
        

@router.on_message(state(OnboardingStates.waiting_for_start_date))
async def input_date_handler(message: Message, cursor: FSMCursor):
    """Обработчик выбора пользователем даты выхода на работу"""
    try:
        # if await debounce_button_max(message, cursor):
        #     logger.info(f"[input_date_handler] Идет обработка нажмите позднее")
        #     return
              
        user_input = message.body.text
        
        if user_input.strip() == 'Завтра':
            await start_tomorrow_handler(message, cursor)
            return
        
        data = cursor.get_data()
        logger.info(f"[input_date_handler] {data=} {type(data)=}")
        if data and 'current_course' in data:
            current_course = data.get("current_course")
        else:
            current_course = await get_value_from_redis(message.user_id, 'current_course')
        logger.info(f"[input_date_handler] Вы ввели дату выхода на работу: {user_input}")
        day, month = map(int, user_input.split('.'))
        current_year = datetime.now().year
        start_date = datetime(current_year, month, day)
        
        if start_date < datetime.now():
            await message.send("⚠️ Выбранная Вами дата уже прошла.\nВведите актуальную дату...")
            logger.warning(f"Введенная дата уже прошла")
            return
            
        date_str = start_date.strftime("%d.%m")
        
        dt = datetime.strptime(f"{date_str}.{current_year}", "%d.%m.%Y")
        
        logger.info(f"[input_date_handler] {date_str=} {dt=}")
        
        cursor.change_data({"start_date": date_str, "parsed_date":dt, "current_course": current_course})
        await save_cursor(message.user_id, extra_data={"state_name": OnboardingStates.waiting_for_confirmation,
                                                       "payload": "yes", "second_payload": "no", "start_date": f'{start_date.day}.{start_date.month}'})
        
        months_ru = {
            1: "января", 2: "февраля", 3: "марта", 4: "апреля", 5: "мая", 6: "июня",
            7: "июля", 8: "августа", 9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
        }
        
        logger.info("Пытаемся отправить сообщение и клавиатуру")
        await message.send(
            f"✅ Правильно ли я понимаю, что ваш первый рабочий день — это {start_date.day} {months_ru[start_date.month]}?\n\n"
            "Нажмите «Да» для подтверждения или «Нет», чтобы указать другую дату.",
            keyboard=yes_no_kb()
        )
        
        cursor.change_state(OnboardingStates.waiting_for_confirmation)  # переходим в состояние подтверждения выбранной даты
    except Exception as e:
        logger.error(f"[input_date_handler] ошибка при вводе даты выхода на работу {e}")
        await message.send(
            "❌ Не удалось распознать дату. Используйте формат ДД.ММ (например, 07.02)"
        )  
    
from services.debounce import debounce_button_max


@router.on_button_callback(state(OnboardingStates.waiting_for_confirmation), lambda call: call.payload == 'yes')
async def confirm_date_handler(callback: Callback, cursor: FSMCursor):
    """Обработчик подтверждения выбора даты пользователем"""
    try:
        logger.info(f"[confirm_date_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'confirm_date_flag': True})    
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)    
        data = cursor.get_data()
        logger.info(f'{data=}')
        if data:
            start_date_str = data.get("start_date")
        else:
            start_date_str = await get_value_from_redis(callback.user_id, 'start_date')
        
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
            
                
        save_reminder(callback.user.user_id, start_date_str, REMINDERS_FILE)

        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[confirm_date_handler] Идет обработка нажмите позднее")
        #     return
        
        text = get_reminder_text(start_date_str)
        if current_course == "Обучение по продукту":
            #current_course = "Обучение по продукту"
            text = get_reminder_text(start_date_str, current_course)
            await callback.send(text, keyboard=main_menu_keyboard("Обучение по продукту"))
            state = cursor.get_state() # изменил 12.07.26 !!!!!
            state_name = state.state if all([state, not isinstance(state, str)]) else state
            logger.info(f'{state_name=}')
            cursor.change_state(AnotherEmployerStates.user_type)
            await save_cursor(callback.user_id, extra_data=dict(state_name = AnotherEmployerStates.user_type))
        else:
            await callback.send(text, keyboard=main_menu_keyboard(current_course))
            await save_cursor(callback.user_id, extra_data=dict(state_name = None))
            cursor.clear_state()
    
    except Exception as e:
        logger.error(f"[confirm_date_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)
    
    

@router.on_button_callback(state(OnboardingStates.waiting_for_confirmation), lambda call: call.payload == 'no')
async def not_confirm_date_handler(callback: Callback, cursor: FSMCursor):
    """Обработчик отклонения выбора даты пользователем"""
    try:
        logger.info(f'Стартовал')
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        await save_cursor(callback.user_id, extra_data = {'not_confirm_date_flag': True})    
        await callback.send("📝 Напишите правильную дату вашего первого рабочего дня в формате ДД.ММ\n\n"
        "Например: 10.02")
        cursor.change_state(OnboardingStates.waiting_for_start_date)
        await save_cursor(callback.user_id, extra_data=dict(state_name = OnboardingStates.waiting_for_start_date))
        
    except Exception as e:
        logger.error(f"[not_confirm_date_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)

     
        
from services.debounce import debounce_button_max
                      
@router.on_button_callback(state(TrainingStates.step_2_video), lambda data: data.payload.split('::')[1] == "not_first")
async def training_step_3_handler(callback: Callback, cursor: FSMCursor):
    """ШАГ 3 - Презентация компании (ссылка на материалы)"""
    try:
        logger.info("[training_step_3_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = dict(step_3_handler_flag = True))
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
            if not current_course:
                current_course == 'Обучение по продажам'
        
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
            
     
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_3_handler] Идет обработка нажмите позднее")
        #     return
        await callback.message.delete()
        
        text = get_training_step_3_text()
        
        logger.info(f'{text=}')
        
        await callback.send(text)

        await asyncio.sleep(3) # 15
        
        kb = KeyboardBuilder().add(CallbackButton(text="📚 Продолжить обучение", payload="next_education::not_first"))
            
        
        cursor.change_state(TrainingStates.course_intro)
        await save_cursor(callback.user_id, extra_data={'current_course': current_course, 'status_user': status_user, 'payload': 'next_education::not_first', 'state_name': TrainingStates.course_intro, })
        
        await callback.send(
            "📚 Вы можете продолжить обучение, нажав кнопку ниже 👇",
            keyboard=kb
        )
             
    except Exception as e:
        logger.error(f"[training_step_3_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)        
    


from services.debounce import debounce_button_max        


async def kb_branch_show_course_intro_handler(callback: Callback, cursor: FSMCursor, state_name = None):
    """Интро курса 'Обучение для конструкторов' - отправка ОГЛАВЛЕНИЯ"""
    try:
        logger.info("[kb_branch_show_course_intro_handler] Стартовал")
        await callback.message.delete()
        status_user = cursor.get_data().get('status_user') if cursor.get_data() else await get_value_from_redis(callback.user_id, 'status_user')
        if state_name != 'module_0':
            text = table_of_content_kb_branch()
            await callback.send(text)
            # 2) Через 15 секунд — содержание Блока №1
            await asyncio.sleep(2) # 15
            kb = KeyboardBuilder().add(CallbackButton(text="📚 Продолжить обучение", payload="next_education::not_first"))
            cursor.change_state(TrainingStates.konstructor['module_0'])
        
            await callback.send(
                "📚 Чтобы перейти к первому разделу и начать обучение, нажмите кнопку ниже 👇",
                keyboard=kb
                )
            await save_cursor(callback.user_id, state={"status_user": status_user, "state_name": TrainingStates.konstructor['module_0'], 'current_course': 'Обучение для конструкторов', "payload": "next_education::not_first" })
        else:
            text = get_module0_intro_text_kb_branch()
            await callback.send(text)  
            await asyncio.sleep(2) # 15
            kb = KeyboardBuilder().add(CallbackButton(text="📚 Продолжить обучение", payload="next_education::not_first"))      
            cursor.change_state(TrainingStates.konstructor['module_0_lesson_1'])
            await save_cursor(callback.user_id, state={"status_user": status_user, "state_name": TrainingStates.konstructor['module_0_lesson_1'], 'current_course': 'Обучение для конструкторов', "payload": "next_education::not_first" })
    except Exception as e:
        logger.error(f"[kb_branch_show_course_intro_handler] Произошла ошибка {e}") 


async def lawyer_show_course_intro_handler(callback: Callback, cursor: FSMCursor):
    """Интро курса 'Обучение для юриста' - отправка ОГЛАВЛЕНИЯ"""
    try:
        logger.info("[lawyer_show_course_intro_handler] Стартовал")
        await callback.message.delete()
        status_user = cursor.get_data().get('status_user') if cursor.get_data() else await get_value_from_redis(callback.user_id, 'status_user')
        text = table_of_content_lawyer()
        await callback.send(text)
        # 2) Через 15 секунд — содержание Блока №1
        await asyncio.sleep(2) # 15
        kb = KeyboardBuilder().add(CallbackButton(text="📚 Продолжить обучение", payload="next_education::not_first"))
        cursor.change_state(TrainingStates.lawyer['block_1'])
        
        await callback.send(
            "📚 Чтобы перейти к первому разделу и начать обучение, нажмите кнопку ниже 👇",
            keyboard=kb
        )
        await save_cursor(callback.user_id, state={"status_user": status_user, "state_name": TrainingStates.lawyer['block_1'], 'current_course': 'Обучение для юриста', "payload": "next_education::not_first" })
                
    except Exception as e:
        logger.error(f"[lawyer_show_course_intro_handler] Произошла ошибка {e}") 


@router.on_button_callback(state(TrainingStates.course_intro), lambda data: data.payload.split('::')[1] == "not_first")
async def show_course_intro_handler(callback: Callback, cursor: FSMCursor):
    """Интро курса 'Обучение по продажам' (между шагом 2 и 3)"""
    try:
        logger.info("[show_course_intro_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[show_course_intro_handler] Идет обработка нажмите позднее")
        #     return
        cursor_data = cursor.get_data()
        logger.info(f'{cursor_data=}')
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = cursor_data.get("current_course")
        if current_course == "Обучение по продажам":
            await callback.message.delete()
            text = get_course_intro_text()
            await callback.send(text)
            # 2) Через 15 секунд — содержание Блока №1
            await asyncio.sleep(2) # 15
            block1_intro = get_block1_intro_text()
       
        elif current_course in ["Другой сотрудник", "Обучение по продукту"]:
            block1_intro = get_another_emp_intro_text()
        elif current_course == "Обучение для юриста":
            await lawyer_show_course_intro_handler(callback, cursor)
            return
        elif current_course == "Обучение для конструкторов":
            state = cursor.get_state() # изменил 12.07.26 !!!!!
            state_name = state.state if all([state, not isinstance(state, str)]) else state
            logger.info(f'Из курсора: {state_name=}')
            if not state_name:
                state_name = await get_value_from_redis(callback.user_id, 'state_name')    
            module_0_intro = get_module0_intro_text_kb_branch()     
            await kb_branch_show_course_intro_handler(callback, cursor, state_name)
            return
        await callback.send(block1_intro)
        
        # 3) Ещё через 10 секунд — сообщение с кнопкой «Продолжить обучение»
        await asyncio.sleep(2) # 10
        
        kb = KeyboardBuilder().add(CallbackButton(text="📚 Продолжить обучение", payload="next_education::not_first"))
        cursor.change_state(TrainingStates.step_3_presentation)
        await save_cursor(callback.user_id, extra_data={"state_name": TrainingStates.step_3_presentation})
        
        await callback.send(
            "📚 Чтобы перейти к первому разделу и начать обучение, нажмите кнопку ниже 👇",
            keyboard=kb
        )
         
    except Exception as e:
        logger.error(f"[show_course_intro_handler] Произошла ошибка {e}") 


from services.debounce import debounce_button_max

@router.on_button_callback(state(TrainingStates.step_3_presentation), lambda data: data.payload.split('::')[1] == "not_first")
async def training_step_3_handler_first_step(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """ШАГ 4 - Раздел №1: База теории"""
    try:
        logger.info("[training_step_3_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = dict(first_step_flag = True))
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)    
        if continue_flag:
            intro_text = get_block1_intro_text()
            await callback.send(intro_text)
            await asyncio.sleep(2) # 10
        
        
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_3_handler] Идет обработка нажмите позднее")
        #     return      
        await callback.message.delete()
        intro_text = get_block1_section1_intro_text()
        await callback.send(intro_text, disable_link_preview=True)
        
        await asyncio.sleep(3) # 15
        
        # сообщение о тестировании с кнопкой
        test_text = go_to_test_1_text(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        cursor.change_state(TrainingStates.step_4_ready_for_test)
        await save_cursor(callback.user_id, extra_data={'state_name': TrainingStates.step_4_ready_for_test, 'payload': 'start_test', 'current_course': current_course})
    
    except Exception as e:
        logger.error(f"[training_step_3_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)   
        

from services.debounce import debounce_button_max

@router.on_button_callback(state(TrainingStates.step_4_ready_for_test), lambda data: data.payload == "start_test")
async def training_step_4_handler(callback: Callback, cursor: FSMCursor):
    """ШАГ 5 - Начало тестирования"""
    try:
        logger.info("[training_step_4_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'step_4_flag': True}) 
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}) 
        questions = get_testing_data_1()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[training_step_4_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
        logger.info(f'{callback=}')
        
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        else:
            await save_cursor(callback, extra_data=dict(questions=questions, current_question=0, answers=[]))
        
            
        logger.info(f'[training_step_4_handler] после добавления вопросов в state: {data=}')  
        
        # Отправляем первый вопрос
        cursor.change_data(data)
        await send_question(callback, cursor, "section_1")
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.step_5_testing))
        else:
            await save_cursor(callback, extra_data=dict(state_name = TrainingStates.step_5_testing))
        cursor.change_state(TrainingStates.step_5_testing)
    
    except Exception as e:
        logger.error(f"[training_step_4_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)  

        
async def send_question(message: Message | Callback, cursor: FSMCursor, lesson_id: str, course_name: str = "Обучение по продажам"):
    """Отправляет текущий вопрос с вариантами ответов"""
    try:
        logger.info("[send_question] Стартовал")
        await save_cursor(message.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2) 
        logger.info(f'[INFO][send_question]state={cursor.get_state()}')
        data:dict = cursor.get_data()
        if not data:
            logger.warning('Возможно сервер был перезапущен')
            data = dict()
        course_name = data.get('current_course') if data else await get_value_from_redis(message.user_id, 'current_course')
        if not course_name:
            course_name = "Обучение по продажам"
        questions = data.get("questions") if data else await get_value_from_redis(message.user_id, 'questions')
        current = data.get("current_question") if data else await get_value_from_redis(message.user_id, 'current')
        logger.info(f'[send_question] номер текущего вопроса: {current}')
        
        if current >= len(questions):
            # Все вопросы пройдены - показываем результаты
            logger.info("[send_question] все вопросы пройдены, показываем результаты")
            await show_results(message, cursor, lesson_id, course_name)
            return
        
        logger.info("[send_question] еще не все вопросы пройдены, продолжаем...")
        question_data = questions[current]
        if isinstance(message, (Callback, Message)):
            await save_cursor(message.user_id, extra_data = {"question_data": question_data})
        else:
            await save_cursor(message, extra_data = {"question_data": question_data})
        logger.info(f"[send_question] текущий вопрос: {question_data=}")
        
        # Текст вопроса
        text = f"📝 **{question_data['question']}**\n"
        
        # Текст вариантов ответов
        answers_text = "\n**Варианты ответов:**\n\n"
        for answer in question_data.get('options'):
            answers_text += f'{answer.strip()}\n'
        
        correct_answer = question_data.get('correct')
        logger.info("[INFO][send_question] обновляем информацию о правильном ответе в cursor")
        data.update(correct = correct_answer)
        if isinstance(message, (Callback, Message)):
            await save_cursor(message.user_id, extra_data = {"correct": correct_answer})
        else:
            await save_cursor(message, extra_data = {"correct": correct_answer})
        logger.info("[INFO][send_question] обновляем значение всего cursor")
        cursor.change_data(data)
        
        if isinstance(message, (Callback, Message)):
            kb = await variants_questions_kb(question_data, message.user_id)
        else:
            kb = await variants_questions_kb(question_data, message)
                
        if isinstance(message, Callback):
            await message.message.delete()
               
        await message.send(text + answers_text, keyboard=kb)
    
    except Exception as e:
        logger.error(f"[send_question] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(message.user_id) 
         

async def show_results(message: Message, cursor: FSMCursor, lesson_id: str, course_name: str):
    """Показывает результаты тестирования"""
    try:
        logger.info("[INFO][show_results] Стартовал")
        if isinstance(message, Callback):
            await message.message.delete()
        data: dict = cursor.get_data()
        if data:
            questions = data.get("questions")
            answers = data.get("answers")
        else:
            questions = await get_value_from_redis(message.user_id, "questions")
            answers = await get_value_from_redis(message.user_id, "answers")
        
        state = cursor.get_state() # изменил 12.07.26 !!!!!
        state_name = state.state if all([state, not isinstance(state, str)]) else state
        logger.info(f'Из курсора: {state_name=}')
        if not state_name:
            state_name = await get_value_from_redis(message.user_id, 'state_name')    
            
        logger.info(f"[INFO][show_results] {questions=}\n{answers=}\n{state_name=}")   
        
        # Подсчитываем правильные ответы
        correct_count = 0
        mistakes = []
        
        for i, question in enumerate(questions):
            logger.info(f"[INFO][show_results] Вопрос № {i}:\n{question}")
            if i < len(answers) and answers[i] == question["correct"]:
                logger.info(f"[INFO][show_results] ответ правильный")
                correct_count += 1
            else:
                user_ans = answers[i] if i < len(answers) else "Нет ответа"
                logger.info(f"[INFO][show_results] ответ не правильный (или нет ответа)")
                correct_ans = question["correct"]
                logger.info(f"[INFO][show_results] правильным должен был быть вариант ответа: {correct_ans}")
                
                # Находим полный текст ответа пользователя
                user_option = "Нет ответа"
                if user_ans != "Нет ответа":
                    user_option = [opt for opt in question["options"] if opt.startswith(user_ans)]
                    user_option = user_option[0] if user_option else user_ans
                logger.info(f"[INFO][show_results] полный текст ответа пользователя: {user_option}")
                
                # Находим полный текст правильного ответа
                correct_option = [opt for opt in question["options"] if opt.startswith(correct_ans)][0]
                logger.info(f"[INFO][show_results] полный текст правильного ответа: {correct_option}")
                
                mistakes.append({
                    "number": i + 1,
                    "question": question["question"],
                    "user_answer": user_option,
                    "correct_answer": correct_option
                })
                
                logger.info(f"[INFO][show_results] добавили информацию об ошибочном ответе пользователя")
        
        # Формируем сообщение с результатами
        result_text = f"📊 **Результаты тестирования**\n\n"
        result_text += f"✅ Правильных ответов: **{correct_count} из {len(questions)}**\n\n"
        
        if correct_count == len(questions):
            result_text += "🎉 **Отлично!** Вы ответили на все вопросы правильно! Так держать! 💪"
        else:
            result_text += "❌ **Неправильные ответы:**\n\n"
            for mistake in mistakes:
                result_text += f"**{mistake['question']}**\n\n"
                result_text += f"📝 **Ваш ответ**: {mistake['user_answer']}\n"
                result_text += f"🎯 **Правильный ответ**: {mistake['correct_answer']}\n\n"
                result_text += f"━━━━━━━━━━━━━━━━━━━━\n\n"
            
            result_text += "💡 **Обратите внимание на эти моменты и повторите материал!**"
        
        await send_message_safely(message, result_text)
        #await message.send(result_text)
        
        # ✅ Обновляем прогресс пользователя (НОВЫЙ КОД)
        from services.gamification import GamificationService
        game = GamificationService(course_name)
        user_data = load_user_data()
        user_id = str(message.user_id)
        first_name = user_data.get(user_id).get("first_name")
        last_name = user_data.get(user_id).get("second_name")
        
        await game.update_lesson_progress(
            user_id=message.user_id,
            course_name=course_name, # "Обучение по продажам"
            correct_count=correct_count,
            total_count=len(questions),
            lesson_id=lesson_id, #  "section_1"
            user_data={
                "username": f'{first_name} {last_name}',
                "first_name": first_name,
                "last_name": last_name
            }
        )
        
        # Через 15 секунд предлагаем продолжить
        await asyncio.sleep(2) # 15
        
        kb = KeyboardBuilder().add(CallbackButton(text="📚 Продолжить обучение", payload="next_education::not_first"))
        await save_cursor(message.user_id, extra_data = {'call_button': 'next_education::not_first'})    

        cursor_redis_data = await load_cursor(message.user_id)
        if 'state_name' in cursor_redis_data:
            del cursor_redis_data['state_name']
        if 'payload' in cursor_redis_data:
            del cursor_redis_data['payload']
        
        if state_name == 'step_5_testing':
            cursor.change_state(TrainingStates.step_6_next)
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.step_6_next, 'current_course': course_name})
        elif state_name == 'step_7_testing':
            cursor.change_state(TrainingStates.step_8_next)
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.step_8_next, 'current_course': course_name})
        elif state_name == 'step_8_testing':
            cursor.change_state(TrainingStates.step_9_next)
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.step_9_next, 'current_course': course_name})
        elif state_name == 'step_9_testing':
            cursor.change_state(TrainingStates.step_10_next)
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.step_10_next, 'current_course': course_name})
        elif state_name == 'step_10_testing':
            cursor.change_state(TrainingStates.step_11_next)
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.step_11_next, 'current_course': course_name})
        elif state_name == 'block_2_test_1_testing':
            cursor.change_state(TrainingStates.block_2_section_2_next)
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.block_2_section_2_next, 'current_course': course_name})
        elif state_name == 'block_2_test_2_testing':
            cursor.change_state(TrainingStates.block_2_section_3_next)
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.block_2_section_3_next, 'current_course': course_name})
        elif state_name == 'block_2_test_3_testing':
            cursor.change_state(TrainingStates.block_2_section_4_next)
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.block_2_section_4_next, 'current_course': course_name})
        elif state_name == 'block_3_test_1_testing':
            cursor.change_state(TrainingStates.block_3_section_1_next)
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.block_3_section_1_next, 'current_course': course_name})
        elif state_name == 'block_3_test_2_testing':
            cursor.change_state(TrainingStates.block_3_section_2_next)
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.block_3_section_2_next, 'current_course': course_name})
        elif state_name == 'block_3_test_3_testing':
            cursor.change_state(TrainingStates.block_3_section_3_next)
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.block_3_section_3_next, 'current_course': course_name})
        elif state_name == 'block_3_test_4_testing':
            cursor.change_state(TrainingStates.block_3_section_4_next)
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.block_3_section_4_next, 'current_course': course_name})
        elif state_name == 'block_3_test_5_testing':
            cursor.change_state(TrainingStates.block_3_section_5_next)
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.block_3_section_5_next, 'current_course': course_name})
        elif state_name == 'block_3_test_6_testing':
            cursor.change_state(TrainingStates.block3_final_test)
            await save_cursor(message.user_id, extra_data = {**cursor_redis_data, 'state_name': TrainingStates.block3_final_test, 'current_course': course_name, 'payload': 'ai_after_block3'})
        elif state_name == 'block_4_test_1_testing':
            cursor.change_state(TrainingStates.block_4_section_1_next)
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.block_4_section_1_next, 'current_course': course_name})
        elif state_name == 'block_4_test_2_testing':
            cursor.change_state(TrainingStates.block_4_section_2_next)
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.block_4_section_2_next, 'current_course': course_name})
        elif state_name == 'block_4_test_3_testing':
            cursor.change_state(TrainingStates.block_4_section_3_next)
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.block_4_section_3_next, 'current_course': course_name})
        elif state_name == 'block_4_test_4_testing':
            cursor.change_state(TrainingStates.block4_final_test)
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.block4_final_test, 'current_course': course_name, 'payload': 'ai_after_block4'})
        elif state_name == 'module_0_lesson_1_testing':
            cursor.change_state(TrainingStates.konstructor['module_0_lesson_2'])
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_0_lesson_2'], 'current_course': course_name})
        elif state_name == 'module_0_lesson_2_testing':
            cursor.change_state(TrainingStates.konstructor['module_0_lesson_3'])
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_0_lesson_3'], 'current_course': course_name})
        elif state_name == 'module_0_lesson_3_testing':
            cursor.change_state(TrainingStates.konstructor['module_0_lesson_4'])
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_0_lesson_4'], 'current_course': course_name})
        elif state_name == 'module_0_lesson_4_testing':
            cursor.change_state(TrainingStates.konstructor['module_0_lesson_5'])
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_0_lesson_5'], 'current_course': course_name})
        elif state_name == 'module_0_lesson_5_testing':
        #     cursor.change_state(TrainingStates.konstructor['module_0_lesson_6'])
        #     await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_0_lesson_6'], 'current_course': course_name})
        # elif state_name == 'module_0_lesson_6_testing':
            await game.increment_lesson_func(
                        user_id=user_id,
                        course_name=course_name, # "Обучение по продажам"
                        lesson_id='section_11', #  "section_1"
                        user_data={
                            "username": f'{first_name} {last_name}',
                            "first_name": first_name,
                            "last_name": last_name
                        }
                    )
            #cursor.change_state(TrainingStates.konstructor['module_0_final_testing'])  # ''' заглушка
            #await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_0_final_testing'], 'current_course': course_name, 'migration_state': 'module_0_final_testing'})
            #cursor.change_state(TrainingStates.konstructor['module_0_questions']) 
            #await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_0_questions'], 'current_course': course_name, 'migration_state': 'module_0_questions'})
        # заглушка - здесь надо проверить есть ли тест после ГЛОССАРИЙ ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ
        # здесь надо продумать переходы к финальным тестам после каждого модуля и переходы после тестирования к очередному модулю
        elif state_name == 'module_1_lesson_1_testing':
            cursor.change_state(TrainingStates.konstructor['module_1_lesson_2'])
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_1_lesson_2'], 'current_course': course_name})
        elif state_name == 'module_1_lesson_2_testing':
            cursor.change_state(TrainingStates.konstructor['module_1_lesson_3'])
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_1_lesson_3'], 'current_course': course_name})
        elif state_name == 'module_1_lesson_3_testing':
            cursor.change_state(TrainingStates.konstructor['module_1_lesson_4'])
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_1_lesson_4'], 'current_course': course_name})
        elif state_name == 'module_1_lesson_4_testing':
            cursor.change_state(TrainingStates.konstructor['module_1_lesson_5'])
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_1_lesson_5'], 'current_course': course_name})
        elif state_name == 'module_1_lesson_5_testing':
            cursor.change_state(TrainingStates.konstructor['module_1_lesson_6'])
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_1_lesson_6'], 'current_course': course_name})
        elif state_name == 'module_1_lesson_6_testing':
            cursor.change_state(TrainingStates.konstructor['module_1_final_testing'])
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_1_final_testing'], 'current_course': course_name, 'migration_state': 'module_1_final_testing'})
        elif state_name == 'module_2_lesson_1_testing':
            cursor.change_state(TrainingStates.konstructor['module_2_lesson_2'])
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_2_lesson_2'], 'current_course': course_name})
        elif state_name == 'module_2_lesson_2_testing':
            cursor.change_state(TrainingStates.konstructor['module_2_lesson_3'])
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_2_lesson_3'], 'current_course': course_name})
        elif state_name == 'module_2_lesson_3_testing':
            cursor.change_state(TrainingStates.konstructor['module_2_lesson_4'])
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_2_lesson_4'], 'current_course': course_name})
        elif state_name == 'module_2_lesson_4_testing':
            cursor.change_state(TrainingStates.konstructor['module_2_lesson_5'])
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_2_lesson_5'], 'current_course': course_name})
        elif state_name == 'module_2_lesson_5_testing':
            cursor.change_state(TrainingStates.konstructor['module_2_final_testing'])
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_2_final_testing'], 'current_course': course_name, 'migration_state': 'module_2_final_testing'})
        elif state_name == 'module_3_lesson_1_testing':
            cursor.change_state(TrainingStates.konstructor['module_3_lesson_2'])
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_3_lesson_2'], 'current_course': course_name})
        elif state_name == 'module_3_lesson_2_testing':
            cursor.change_state(TrainingStates.konstructor['module_3_lesson_3'])
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_3_lesson_3'], 'current_course': course_name})
        elif state_name == 'module_3_lesson_3_testing':
            cursor.change_state(TrainingStates.konstructor['module_3_lesson_4'])
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_3_lesson_4'], 'current_course': course_name})
        elif state_name == 'module_3_lesson_4_testing':
            cursor.change_state(TrainingStates.konstructor['module_3_lesson_5'])
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_3_lesson_5'], 'current_course': course_name})
        elif state_name == 'module_3_lesson_5_testing':
            cursor.change_state(TrainingStates.konstructor['module_3_final_testing'])
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_3_final_testing'], 'current_course': course_name, 'migration_state': 'module_3_final_testing'})
        elif state_name == 'module_4_lesson_1_testing':
            cursor.change_state(TrainingStates.konstructor['module_4_lesson_2'])
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_4_lesson_2'], 'current_course': course_name})
        elif state_name == 'module_4_lesson_2_testing':
            cursor.change_state(TrainingStates.konstructor['module_4_lesson_3'])
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_4_lesson_3'], 'current_course': course_name})
        elif state_name == 'module_4_lesson_3_testing':
            cursor.change_state(TrainingStates.konstructor['module_4_lesson_4'])
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_4_lesson_4'], 'current_course': course_name})
        elif state_name == 'module_4_lesson_4_testing':
            cursor.change_state(TrainingStates.konstructor['module_4_final_testing'])
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_4_final_testing'], 'current_course': course_name, 'migration_state': 'module_4_final_testing'})
        elif state_name == 'module_5_lesson_1_testing':
            cursor.change_state(TrainingStates.konstructor['module_5_lesson_2'])
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_5_lesson_2'], 'current_course': course_name})
        elif state_name == 'module_5_lesson_2_testing':
            cursor.change_state(TrainingStates.konstructor['module_5_lesson_3'])
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_5_lesson_3'], 'current_course': course_name})
        elif state_name == 'module_5_lesson_3_testing':
            cursor.change_state(TrainingStates.konstructor['module_5_lesson_4'])
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_5_lesson_4'], 'current_course': course_name})
        elif state_name == 'module_5_lesson_4_testing':
            cursor.change_state(TrainingStates.konstructor['module_5_final_testing'])
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_5_final_testing'], 'current_course': course_name, 'migration_state': 'module_5_final_testing'})
        elif state_name == 'module_6_lesson_1_testing':
            cursor.change_state(TrainingStates.konstructor['module_6_lesson_2'])
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_6_lesson_2'], 'current_course': course_name})
        elif state_name == 'module_6_lesson_2_testing':
            cursor.change_state(TrainingStates.konstructor['module_6_lesson_3'])
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_6_lesson_3'], 'current_course': course_name})
        elif state_name == 'module_6_lesson_3_testing':
            cursor.change_state(TrainingStates.konstructor['module_6_lesson_4'])
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_6_lesson_4'], 'current_course': course_name})
        elif state_name == 'module_6_lesson_4_testing':
            cursor.change_state(TrainingStates.konstructor['module_6_final_testing'])
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_6_final_testing'], 'current_course': course_name, 'migration_state': 'module_6_final_testing'})
        elif state_name == 'module_7_lesson_1_testing':
            cursor.change_state(TrainingStates.konstructor['module_7_lesson_2'])
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_7_lesson_2'], 'current_course': course_name})
        elif state_name == 'module_7_lesson_2_testing':
            cursor.change_state(TrainingStates.konstructor['module_7_lesson_3'])
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_7_lesson_3'], 'current_course': course_name})
        elif state_name == 'module_7_lesson_3_testing':
            cursor.change_state(TrainingStates.konstructor['module_7_lesson_4'])
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_7_lesson_4'], 'current_course': course_name})
        elif state_name == 'module_7_lesson_4_testing':
            cursor.change_state(TrainingStates.konstructor['module_7_final_testing'])
            await save_cursor(message.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_7_final_testing'], 'current_course': course_name, 'migration_state': 'module_7_final_testing'})
        
        
        logger.info(f"[INFO][show_results] state = {cursor.get_state()} type= {type(cursor.get_state())}")
        if state_name != 'step_11_testing' and cursor.get_state() != 'module_0_questions': 
            await message.send(
                    "📚 Вы можете продолжить обучение, нажав кнопку ниже 👇",
                    keyboard=kb
                )
        elif state_name == 'step_11_testing':
            await continue_after_section6_handler(message, cursor)

        # elif cursor.get_state() == 'block3_final_test':
        #     await continue_after_section17_handler(message, cursor)
                
            
         
    except Exception as e:
        logger.error(f"[show_results] Произошла ошибка {e}")   
        

@router.on_button_callback(state(TrainingStates.konstructor['module_7_lesson_4_testing']))
@router.on_button_callback(state(TrainingStates.konstructor['module_7_lesson_3_testing']))
@router.on_button_callback(state(TrainingStates.konstructor['module_7_lesson_2_testing']))
@router.on_button_callback(state(TrainingStates.konstructor['module_7_lesson_1_testing']))
@router.on_button_callback(state(TrainingStates.konstructor['module_6_lesson_4_testing']))
@router.on_button_callback(state(TrainingStates.konstructor['module_6_lesson_3_testing']))
@router.on_button_callback(state(TrainingStates.konstructor['module_6_lesson_2_testing']))
@router.on_button_callback(state(TrainingStates.konstructor['module_6_lesson_1_testing']))
@router.on_button_callback(state(TrainingStates.konstructor['module_5_lesson_4_testing']))
@router.on_button_callback(state(TrainingStates.konstructor['module_5_lesson_3_testing']))
@router.on_button_callback(state(TrainingStates.konstructor['module_5_lesson_2_testing']))
@router.on_button_callback(state(TrainingStates.konstructor['module_5_lesson_1_testing']))
@router.on_button_callback(state(TrainingStates.konstructor['module_4_lesson_4_testing']))
@router.on_button_callback(state(TrainingStates.konstructor['module_4_lesson_3_testing']))
@router.on_button_callback(state(TrainingStates.konstructor['module_4_lesson_2_testing']))
@router.on_button_callback(state(TrainingStates.konstructor['module_4_lesson_1_testing']))
@router.on_button_callback(state(TrainingStates.konstructor['module_3_lesson_5_testing']))
@router.on_button_callback(state(TrainingStates.konstructor['module_3_lesson_4_testing']))
@router.on_button_callback(state(TrainingStates.konstructor['module_3_lesson_3_testing']))
@router.on_button_callback(state(TrainingStates.konstructor['module_3_lesson_2_testing']))
@router.on_button_callback(state(TrainingStates.konstructor['module_3_lesson_1_testing']))
@router.on_button_callback(state(TrainingStates.konstructor['module_2_lesson_5_testing']))
@router.on_button_callback(state(TrainingStates.konstructor['module_2_lesson_4_testing']))
@router.on_button_callback(state(TrainingStates.konstructor['module_2_lesson_3_testing']))
@router.on_button_callback(state(TrainingStates.konstructor['module_2_lesson_2_testing']))
@router.on_button_callback(state(TrainingStates.konstructor['module_2_lesson_1_testing']))
@router.on_button_callback(state(TrainingStates.konstructor['module_1_lesson_6_testing']))
@router.on_button_callback(state(TrainingStates.konstructor['module_1_lesson_5_testing']))
@router.on_button_callback(state(TrainingStates.konstructor['module_1_lesson_4_testing']))
@router.on_button_callback(state(TrainingStates.konstructor['module_1_lesson_3_testing']))
@router.on_button_callback(state(TrainingStates.konstructor['module_1_lesson_2_testing']))
@router.on_button_callback(state(TrainingStates.konstructor['module_1_lesson_1_testing']))
@router.on_button_callback(state(TrainingStates.konstructor['module_0_lesson_5_testing']))        
@router.on_button_callback(state(TrainingStates.konstructor['module_0_lesson_4_testing']))        
@router.on_button_callback(state(TrainingStates.konstructor['module_0_lesson_3_testing']))
@router.on_button_callback(state(TrainingStates.konstructor['module_0_lesson_2_testing']))
@router.on_button_callback(state(TrainingStates.konstructor['module_0_lesson_1_testing']))
@router.on_button_callback(state(TrainingStates.block_4_test_4_testing))
@router.on_button_callback(state(TrainingStates.block_4_test_3_testing))
@router.on_button_callback(state(TrainingStates.block_4_test_2_testing))
@router.on_button_callback(state(TrainingStates.block_4_test_1_testing))
@router.on_button_callback(state(TrainingStates.block_3_test_1_testing))
@router.on_button_callback(state(TrainingStates.block_3_test_2_testing))
@router.on_button_callback(state(TrainingStates.block_3_test_3_testing))
@router.on_button_callback(state(TrainingStates.block_3_test_4_testing))
@router.on_button_callback(state(TrainingStates.block_3_test_5_testing))
@router.on_button_callback(state(TrainingStates.block_3_test_6_testing))
@router.on_button_callback(state(TrainingStates.block_2_test_3_testing))
@router.on_button_callback(state(TrainingStates.block_2_test_2_testing))
@router.on_button_callback(state(TrainingStates.block_2_test_1_testing))
@router.on_button_callback(state(TrainingStates.step_11_testing))
@router.on_button_callback(state(TrainingStates.step_10_testing))
@router.on_button_callback(state(TrainingStates.step_9_testing))
@router.on_button_callback(state(TrainingStates.step_8_testing))
@router.on_button_callback(state(TrainingStates.step_7_testing))
@router.on_button_callback(state(TrainingStates.step_5_testing))
async def process_answer_handler(callback: Callback, cursor: FSMCursor):
    """Обрабатывает ответ пользователя"""
    try:
        logger.info(f"[INFO][process_answer_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)    
        data:dict = cursor.get_data()
        logger.info(f"[INFO][process_answer_handler] {data=}")
        if data:
            logger.info(f'Курсор: ') 
            answers = data.get("answers", [])
            current = data.get("current_question")
            await save_cursor(callback.user_id, extra_data = dict(current_question = current + 1, answers = answers))
            correct = data.get("correct")
            logger.info(f'{answers=} {current=} {correct=}')
        else:
            logger.info(f'Redis: ') 
            answers = await get_value_from_redis(callback.user_id, 'answers')
            if not answers:
                answers = []
            current = await get_value_from_redis(callback.user_id, 'current_question')
            if not current:
                current = 0
            correct = await get_value_from_redis(callback.user_id, 'correct')
            logger.info(f'{answers=} {current=} {correct=}')
        
        call_answer = callback.payload
        logger.info(f"{call_answer=}")
        if not call_answer:
            call_answer = await get_value_from_redis(callback.user_id, 'call_answer')
            user_answer = call_answer.split('::')[1] if "correct" not in call_answer else call_answer.split('::')[1].split("_")[0]
            logger.info(f"[INFO][process_answer_handler] {user_answer=}\n{call_answer=}\n{correct=}")
            answers.append(user_answer)
            await save_cursor(callback.user_id, extra_data = dict(answers = answers))
            
        
        elif all([call_answer, '::' in callback.payload, call_answer != 'change_department::in_process']):
            user_answer = call_answer.split('::')[1] if "correct" not in call_answer else call_answer.split('::')[1].split("_")[0]
            logger.info(f"[INFO][final_process_answer_handler] {user_answer=}\n{call_answer=}\n{correct=}")        
            answers.append(user_answer)
            logger.info(f"[INFO][process_answer_handler] Сохраняем ответ пользователя и переходим к следующему вопросу")
            if data:
                data.update(answers=answers, current_question=current + 1)
                cursor.change_data(data) # !!!!!!!!!!
            else:
                extra_data = await load_cursor(callback.user_id)
                extra_data.update(answers=answers, current_question=current + 1)
                await save_cursor(callback.user_id, extra_data = {**extra_data})
                cursor.change_data(extra_data)
        
        state = cursor.get_state() # изменил 12.07.26 !!!!!
        state_name = state.state if all([state, not isinstance(state, str)]) else state
        logger.info(f'Из курсора: {state_name=}')
        if not state_name:
            state_name = await get_value_from_redis(callback.user_id, 'state_name')
               
        logger.info(f'[INFO][process_answer_handler] {state_name=}')
        if state_name == 'step_5_testing':
            await send_question(callback, cursor, 'section_1')
        elif state_name == 'step_7_testing':
            await send_question(callback, cursor, 'section_2')
        elif state_name == 'step_8_testing':
            await send_question(callback, cursor, 'section_3')
        elif state_name == 'step_9_testing':
            await send_question(callback, cursor, 'section_4')
        elif state_name == 'step_10_testing':
            await send_question(callback, cursor, 'section_5')
        elif state_name == 'step_11_testing':
            await send_question(callback, cursor, 'section_6')
        elif state_name == 'block_2_test_1_testing':
            await send_question(callback, cursor, 'section_7')
        elif state_name == 'block_2_test_2_testing':
            await send_question(callback, cursor, 'section_8')
        elif state_name == 'block_2_test_3_testing':
            await send_question(callback, cursor, 'section_9')
        elif state_name == 'block_3_test_1_testing':
            await send_question(callback, cursor, 'section_11')
        elif state_name == 'block_3_test_2_testing':
            await send_question(callback, cursor, 'section_12')
        elif state_name == 'block_3_test_3_testing':
            await send_question(callback, cursor, 'section_13')
        elif state_name == 'block_3_test_4_testing':
            await send_question(callback, cursor, 'section_14')
        elif state_name == 'block_3_test_5_testing':
            await send_question(callback, cursor, 'section_15')
        elif state_name == 'block_3_test_6_testing':
            await send_question(callback, cursor, 'section_16')
        elif state_name == 'block_4_test_1_testing':
            await send_question(callback, cursor, 'section_18')
        elif state_name == 'block_4_test_2_testing':
            await send_question(callback, cursor, 'section_19')
        elif state_name == 'block_4_test_3_testing':
            await send_question(callback, cursor, 'section_20')
        elif state_name == 'block_4_test_4_testing':
            await send_question(callback, cursor, 'section_21')
        elif state_name == 'module_0_lesson_1_testing':
            await send_question(callback, cursor, 'section_2')
        elif state_name == 'module_0_lesson_2_testing':
            await send_question(callback, cursor, 'section_4')
        elif state_name == 'module_0_lesson_3_testing':
            await send_question(callback, cursor, 'section_6')
        elif state_name == 'module_0_lesson_4_testing':
            await send_question(callback, cursor, 'section_8')
        elif state_name == 'module_0_lesson_5_testing':
            await send_question(callback, cursor, 'section_10')
        elif state_name == 'module_1_lesson_1_testing':
            await send_question(callback, cursor, 'section_14')
        elif state_name == 'module_1_lesson_2_testing':
            await send_question(callback, cursor, 'section_16')
        elif state_name == 'module_1_lesson_3_testing':
            await send_question(callback, cursor, 'section_18')
        elif state_name == 'module_1_lesson_4_testing':
            await send_question(callback, cursor, 'section_20')
        elif state_name == 'module_1_lesson_5_testing':
            await send_question(callback, cursor, 'section_22')
        elif state_name == 'module_1_lesson_6_testing':
            await send_question(callback, cursor, 'section_24')
        elif state_name == 'module_2_lesson_1_testing':
            await send_question(callback, cursor, 'section_27')
        elif state_name == 'module_2_lesson_2_testing':
            await send_question(callback, cursor, 'section_29')
        elif state_name == 'module_2_lesson_3_testing':
            await send_question(callback, cursor, 'section_31')
        elif state_name == 'module_2_lesson_4_testing':
            await send_question(callback, cursor, 'section_33')
        elif state_name == 'module_2_lesson_5_testing':
            await send_question(callback, cursor, 'section_35')
        elif state_name == 'module_3_lesson_1_testing':
            await send_question(callback, cursor, 'section_38')
        elif state_name == 'module_3_lesson_2_testing':
            await send_question(callback, cursor, 'section_40')
        elif state_name == 'module_3_lesson_3_testing':
            await send_question(callback, cursor, 'section_42')
        elif state_name == 'module_3_lesson_4_testing':
            await send_question(callback, cursor, 'section_44')
        elif state_name == 'module_3_lesson_5_testing':
            await send_question(callback, cursor, 'section_46')
        elif state_name == 'module_4_lesson_1_testing':
            await send_question(callback, cursor, 'section_49')
        elif state_name == 'module_4_lesson_2_testing':
            await send_question(callback, cursor, 'section_51')
        elif state_name == 'module_4_lesson_3_testing':
            await send_question(callback, cursor, 'section_53')
        elif state_name == 'module_4_lesson_4_testing':
            await send_question(callback, cursor, 'section_55')
        elif state_name == 'module_5_lesson_1_testing':
            await send_question(callback, cursor, 'section_58')
        elif state_name == 'module_5_lesson_2_testing':
            await send_question(callback, cursor, 'section_60')
        elif state_name == 'module_5_lesson_3_testing':
            await send_question(callback, cursor, 'section_62')
        elif state_name == 'module_5_lesson_4_testing':
            await send_question(callback, cursor, 'section_64')
        elif state_name == 'module_6_lesson_1_testing':
            await send_question(callback, cursor, 'section_67')
        elif state_name == 'module_6_lesson_2_testing':
            await send_question(callback, cursor, 'section_69')
        elif state_name == 'module_6_lesson_3_testing':
            await send_question(callback, cursor, 'section_71')
        elif state_name == 'module_6_lesson_4_testing':
            await send_question(callback, cursor, 'section_73')
        elif state_name == 'module_7_lesson_1_testing':
            await send_question(callback, cursor, 'section_76')
        elif state_name == 'module_7_lesson_2_testing':
            await send_question(callback, cursor, 'section_78')
        elif state_name == 'module_7_lesson_3_testing':
            await send_question(callback, cursor, 'section_80')
        elif state_name == 'module_7_lesson_4_testing':
            await send_question(callback, cursor, 'section_82')
    except Exception as e:
        logger.error(f"[ERROR][process_answer_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)       


@router.on_button_callback(state(TrainingStates.step_6_next), lambda data: data.payload.split('::')[1] == "not_first")
async def training_step_6_handler(callback: Callback, cursor: FSMCursor):
    """ШАГ 6 - Раздел №2: Продукция компании"""
    try:
        logger.info('Стартовал')
        await del_value_from_redis(callback.user_id, 'call_button')
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        await callback.message.delete()
        intro_text = get_block1_section2_intro_text()  
        await callback.send(intro_text, disable_link_preview=True)
        
        await asyncio.sleep(2) # 15
        
        test_text = go_to_test_1_text(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        await save_cursor(callback.user_id, extra_data={'state_name': TrainingStates.step_6_ready_for_test, 'payload': 'start_test', 'current_course': current_course})
        cursor.change_state(TrainingStates.step_6_ready_for_test)
        
        
    except Exception as e:
        logger.error(f"[ERROR][training_step_6_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)
        
            

# ========== РАЗДЕЛ №2 ==========

@router.on_button_callback(state(TrainingStates.step_6_ready_for_test), lambda data: data.payload == "start_test")
async def training_test_2_handler(callback: Callback, cursor: FSMCursor):
    """ШАГ 5 - Начало тестирования"""
    try:
        logger.info("[training_test_2_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2) 
        questions = get_testing_data_2()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[training_test_2_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
            
        await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        logger.info(f'[training_test_2_handler] после добавления вопросов в state: {data=}')  
        
        # Отправляем первый вопрос
        cursor.change_data(data)
        await send_question(callback, cursor, 'section_2')
        cursor.change_state(TrainingStates.step_7_testing)
        await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.step_7_testing))
        
    
    except Exception as e:
        logger.error(f"[training_test_2_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)        


from services.debounce import debounce_button_max


# ========== РАЗДЕЛ №3 ==========

@router.on_button_callback(state(TrainingStates.step_8_next), lambda data: data.payload.split('::')[1] == "not_first")
async def training_step_8_handler(callback: Callback, cursor: FSMCursor):
    """ШАГ 6 - Раздел №3: Кремнезольная технология"""
    try:
        logger.info('Стартовал')
        await del_value_from_redis(callback.user_id, 'call_button')
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)    
        await callback.message.delete()
        intro_text = get_block1_section_3_intro_text()  
        await callback.send(intro_text, disable_link_preview=True)
        
        await asyncio.sleep(2) # 15
        
        test_text = go_to_test_1_text(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        await save_cursor(callback.user_id, extra_data={'state_name': TrainingStates.step_8_ready_for_test, 'payload': 'start_test', 'current_course': current_course})
        cursor.change_state(TrainingStates.step_8_ready_for_test)
        
        
    except Exception as e:
        logger.error(f"[ERROR][training_step_8_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)   
        

@router.on_button_callback(state(TrainingStates.step_8_ready_for_test), lambda data: data.payload == "start_test")
async def training_test_3_handler(callback: Callback, cursor: FSMCursor):
    """ШАГ 6 - Начало тестирования"""
    try:
        logger.info("[training_test_3_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2) 
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        
        questions = get_testing_data_3()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[training_test_3_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
            
        await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        logger.info(f'[training_test_3_handler] после добавления вопросов в state: {data=}')  
        
        cursor.change_data(data)
        # Отправляем первый вопрос
        await send_question(callback, cursor, 'section_3')
        await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.step_8_testing))
        cursor.change_state(TrainingStates.step_8_testing)
    
    except Exception as e:
        logger.error(f"[training_test_3_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)       


# ========== РАЗДЕЛ №4 ==========

@router.on_button_callback(state(TrainingStates.step_9_next), lambda data: data.payload.split('::')[1] == "not_first")
async def training_step_9_handler(callback: Callback, cursor: FSMCursor):
    """ШАГ 7 - Раздел №4: Производственный процесс: как это делается"""
    try:
        logger.info('Стартовал')
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)    
        await callback.message.delete()
        intro_text = get_block1_section_4_intro_text()  
        await callback.send(intro_text, disable_link_preview=True)
        
        await asyncio.sleep(2) # 15
        
        test_text = go_to_test_1_text(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        await save_cursor(callback.user_id, extra_data={'state_name': TrainingStates.step_9_ready_for_test, 'payload': 'start_test', 'current_course': current_course})
        cursor.change_state(TrainingStates.step_9_ready_for_test)
        
        
    except Exception as e:
        logger.error(f"[ERROR][training_step_9_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)   
        

@router.on_button_callback(state(TrainingStates.step_9_ready_for_test), lambda data: data.payload == "start_test")
async def training_test_4_handler(callback: Callback, cursor: FSMCursor):
    """ШАГ 8 - Начало тестирования"""
    try:
        logger.info("[training_test_4_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2) 
        questions = get_testing_data_4()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[training_test_4_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
            
        await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        logger.info(f'[training_test_4_handler] после добавления вопросов в state: {data=}')  
        
        cursor.change_data(data)
        # Отправляем первый вопрос
        await send_question(callback, cursor, 'section_4')
        await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.step_9_testing))
        cursor.change_state(TrainingStates.step_9_testing)
    
    except Exception as e:
        logger.error(f"[training_test_4_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)       


# ========== РАЗДЕЛ №5 ==========

@router.on_button_callback(state(TrainingStates.step_10_next), lambda data: data.payload.split('::')[1] == "not_first")
async def training_step_10_handler(callback: Callback, cursor: FSMCursor):
    """ШАГ 9 - Раздел №5: Группировка продуктов по назначению и условиям"""
    try:
        logger.info('Стартовал')
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)    
        await callback.message.delete()
        intro_text = get_block1_section_5_intro_text()  
        await callback.send(intro_text, disable_link_preview=True)
        
        await asyncio.sleep(2) # 15
        
        test_text = go_to_test_1_text(5)
        await callback.send(test_text, format='markdown', keyboard=start_test_kb())
        
        await save_cursor(callback.user_id, extra_data={'state_name': TrainingStates.step_10_ready_for_test, 'payload': 'start_test', 'current_course': current_course})
        cursor.change_state(TrainingStates.step_10_ready_for_test)
        
        
    except Exception as e:
        logger.error(f"[ERROR][training_step_10_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)   
        

@router.on_button_callback(state(TrainingStates.step_10_ready_for_test), lambda data: data.payload == "start_test")
async def training_test_5_handler(callback: Callback, cursor: FSMCursor):
    """ШАГ 9 - Начало тестирования"""
    try:
        logger.info("[training_test_5_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2) 
        questions = get_testing_data_5()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[training_test_5_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
            
        await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        logger.info(f'[training_test_5_handler] после добавления вопросов в state: {data=}')  
        
        cursor.change_data(data)
        # Отправляем первый вопрос
        await send_question(callback, cursor, 'section_5')
        await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.step_10_testing))
        cursor.change_state(TrainingStates.step_10_testing)
    
    except Exception as e:
        logger.error(f"[training_test_5_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)         


# ========== РАЗДЕЛ №6 ==========

@router.on_button_callback(state(TrainingStates.step_11_next), lambda data: data.payload.split('::')[1] == "not_first")
async def training_step_11_handler(callback: Callback, cursor: FSMCursor):
    """ШАГ 9 - Раздел №6: Ценообразование: как формируется стоимость"""
    try:
        logger.info('Стартовал')
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)    
        await callback.message.delete()
        intro_text = get_block1_section_6_intro_text()  
        await callback.send(intro_text, disable_link_preview=True)
        
        await asyncio.sleep(2) # 15
        
        test_text = go_to_test_1_text(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        await save_cursor(callback.user_id, extra_data={'state_name': TrainingStates.step_11_ready_for_test, 'payload': 'start_test', 'current_course': current_course})
        cursor.change_state(TrainingStates.step_11_ready_for_test)
        
        
    except Exception as e:
        logger.error(f"[ERROR][training_step_11_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)   
        

@router.on_button_callback(state(TrainingStates.step_11_ready_for_test), lambda data: data.payload == "start_test")
async def training_test_6_handler(callback: Callback, cursor: FSMCursor):
    """ШАГ 9 - Начало тестирования"""
    try:
        logger.info("[training_test_6_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2) 
        questions = get_testing_data_6()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[training_test_6_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
            
        await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        logger.info(f'[training_test_6_handler] после добавления вопросов в state: {data=}')  
        
        cursor.change_data(data)
        # Отправляем первый вопрос
        await send_question(callback, cursor, 'section_6')
        await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.step_11_testing))
        cursor.change_state(TrainingStates.step_11_testing)
    
    except Exception as e:
        logger.error(f"[training_test_6_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)      
        
        
@router.on_button_callback(state(TrainingStates.step_11_testing), lambda data: data.payload.split('::')[1] == "not_first")
async def continue_after_section6_handler(callback: Callback, cursor: FSMCursor):
    """Завершение Блока №1 - Продукт. Переход к вопросам или финальному тесту"""
    try:
        logger.info(f"[continue_after_section6_handler] Стартовал")
        await callback.message.delete()
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        # Проверяем загрузку базы знаний
        rag = RAGService()
        stats = rag.get_stats()
        
        cursor_data = cursor.get_data()
                
        if not stats['is_loaded']:
            await callback.send(
                "❌ База знаний не загружена. Обратитесь к администратору.",
                keyboard=main_menu_keyboard(current_course)
            )
            cursor.clear()
            return
        
        text = get_text_to_final_test_block_1()
        if cursor_data.get("current_course") == ["Обучение по продукту"]:
            text = get_text_to_final_test_block_1(True)
        
        await callback.send(text, keyboard=final_start_test_kb())
        cursor.change_state(TrainingStates.block1_questions)
        await save_cursor(callback.user_id, extra_data = {'payload': 'to_final_test', 'state_name': TrainingStates.block1_questions, 'current_course': current_course})
    
    except Exception as e:
        logger.error(f"[continue_after_section6_handler] Произошла ошибка {e}")



@router.on_button_callback(state(TrainingStates.block1_questions), lambda data: data.payload == 'to_final_test')
async def start_block1_final_test_handler(callback: Callback, cursor: FSMCursor):
    """Переход к финальному тесту по Блоку №1 - ШАГ 10"""
    try:
        logger.info(f"[INFO][start_block1_final_test_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)    
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        text = get_text_start_final_test_block_1()
        
        if current_course in ["Другой сотрудник", "Обучение по продукту"]:
            text = get_text_start_final_test_block_1(True)
        
        data = cursor.get_data()
        if not data:
            data = dict()
            status_user = await get_value_from_redis(callback.user_id, 'status_user')
            if not status_user:
                status_user = 'new_employer'
        else:
            status_user = data.get('status_user', 'new_employer')

        logger.info(f'{current_course=} {status_user=}')
        data.update(current_question=0, current_course=current_course, status_user=status_user)
        cursor.change_data(data)
        await callback.send(text, keyboard=final_test_kb())
        cursor.change_state(TrainingStates.step_12_testing)
        await save_cursor(callback.user_id, extra_data = {**data, 'state_name': TrainingStates.step_12_testing, 'payload': 'start_final_test'})
           
    
    except Exception as e:
        logger.error(f"[ERROR][start_block1_final_test_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)
        

@router.on_message(state(TrainingStates.konstructor['module_7_questions']))
@router.on_message(state(TrainingStates.konstructor['module_6_questions']))
@router.on_message(state(TrainingStates.konstructor['module_5_questions']))
@router.on_message(state(TrainingStates.konstructor['module_4_questions']))
@router.on_message(state(TrainingStates.konstructor['module_3_questions']))
@router.on_message(state(TrainingStates.konstructor['module_2_questions']))
@router.on_message(state(TrainingStates.konstructor['module_1_questions']))        
@router.on_message(state(TrainingStates.konstructor['module_0_questions']))
@router.on_message(state(TrainingStates.lawyer['block1_questions']))
@router.on_message(state(TrainingStates.block1_questions))
async def answer_block1_question_handler(message: Message, cursor: FSMCursor, state_name: str = None):
    """Ответы на вопросы по Блоку 1 через RAG + Claude"""
    try:
        logger.info(f"[INFO][answer_block1_question_handler] Стартовал")
        cursor_redis_data = await load_cursor(message.user_id)
        del cursor_redis_data['state_name']
        await save_cursor(message.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)    
        # Показываем процесс
        thinking_msg = await message.send("🔍 Ищу информацию в базе знаний...")
        
        if not state_name:
            state = cursor.get_state() # изменил 12.07.26 !!!!!
            state_name = state.state if all([state, not isinstance(state, str)]) else state
            logger.info(f'Из курсора: {state_name=}')
        else:
            logger.info(f'Из аргумента обработчика:{state_name=}')
        
        if state_name in ['block1_questions_lawyer', 'block2_questions_lawyer', 'block3_questions_lawyer',
                          'block4_questions_lawyer']:
            rag = RAGService(branch_name = 'lawyer')
        elif state_name in ['module_0_questions', 'module_1_questions', 'module_2_questions', 'module_3_questions'
                            'module_4_questions', 'module_5_questions', 'module_6_questions', 'module_7_questions']:
            rag = RAGService(branch_name = 'branch_kb')
        else:
            rag = RAGService()
        
        answer = await rag.answer_question(message.body.text)
        
        await thinking_msg.delete() 
        
        # Форматируем ответ
        logger.info(f"[INFO][answer_block1_question_handler] Форматируем ответ") 
        response_text = (
            f"💡 **Ответ по Блоку №1:**\n\n"
            f"{answer}\n\n"
            "➡️ Задайте следующий вопрос или нажмите 📝 **Перейти к тестированию**"
        )
        if state_name in ['module_0_questions', 'module_1_questions', 'module_2_questions', 'module_3_questions'
                            'module_4_questions', 'module_5_questions', 'module_6_questions', 'module_7_questions']:
            module_number = ''
            if '0' in state_name:
                module_number = '0'
            elif '1' in state_name:
                module_number = '1'
            elif '2' in state_name:
                module_number = '2'
            elif '3' in state_name:
                module_number = '3'
            elif '4' in state_name:
                module_number = '4'
            elif '5' in state_name:
                module_number = '5'
            elif '6' in state_name:
                module_number = '6'
            elif '7' in state_name:
                module_number = '7'
            
            response_text = (
                        f"💡 **Ответ по Модулю № {module_number}:**\n\n"
                        f"{answer}\n\n"
                        "➡️ Задайте следующий вопрос или нажмите 📝 **Перейти к тестированию**"
                    )
            
        
        await message.send(response_text, keyboard=final_start_test_kb(), format='markdown')
        cursor.change_state(state_name)
        await save_cursor(message.user_id, extra_data = {**cursor_redis_data, 'state_name': state_name})
            
    except Exception as e:
        await thinking_msg.delete()
        logger.error(f"[ERROR][answer_block1_question_handler] Произошла ошибка {e}")   

        await message.send(
            "❌ Произошла ошибка при обработке вопроса.\n\n"
            "Попробуйте задать вопрос ещё раз или обратитесь к администратору.",
            keyboard=final_start_test_kb()
        )
    finally:
        await remove_repeat_flag(message.user_id) 


@router.on_message(state(TrainingStates.step_12_testing))
async def block1_final_testing_handler(message: Message, cursor: FSMCursor):
    """Ответы на вопросы по Блоку 1 через RAG + Claude"""
    try:
        logger.info(f"[INFO][block1_final_testing_handler] Стартовал")   
        
        await asyncio.sleep(2)
        course_name = await get_value_from_redis(message.user_id, 'current_course')
        if not course_name:
            course_name = get_current_course(cursor)
        logger.info(f'{course_name=}')
        
        await send_question_step_12(message, cursor, 'final_test', course_name)
        return
        
    except Exception as e:
        #await thinking_msg.delete()
        logger.error(f"[ERROR][block1_final_testing_handler] Произошла ошибка {e}")   

        await message.send(
            "❌ Произошла ошибка при обработке вопроса.\n\n"
            "Попробуйте задать вопрос ещё раз или обратитесь к администратору.",
            keyboard=final_start_test_kb()
        )
       
# ============================================================================
# ШАГ 17: ФИНАЛЬНОЕ ТЕСТИРОВАНИЕ ПО БЛОКУ №1 (10 закрытых + 5 открытых)
# ============================================================================


@router.on_button_callback(state(TrainingStates.step_12_testing), lambda data: data.payload == 'start_final_test')
async def start_testing_block1_handler(callback: Callback, cursor: FSMCursor):
    """ШАГ 12 - Запуск финального тестирования по Блоку 1"""
    try:
        logger.info(f"[INFO][start_testing_block1_handler] Стартовал")
        await del_value_from_redis(callback.user_id, 'payload')
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        # ЧАСТЬ 1: Закрытые вопросы (10 вопросов с вариантами A/B/C/D)
        closed_questions = get_final_test_block_1('close')
        logger.info(f"[INFO][start_testing_block1_handler] {closed_questions=}")
        
        # ЧАСТЬ 2: Открытые вопросы (5 вопросов с эталонными ответами)
        open_questions = get_final_test_block_1('open')
        logger.info(f"[INFO][start_testing_block1_handler] {open_questions=}")
        
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        logger.info(f'{current_course=}')
        
        data = cursor.get_data()
        logger.info(f'[start_testing_block1_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(
                closed_questions=closed_questions,
                open_questions=open_questions,
                current_question=0,
                closed_answers=[],  # Ответы на закрытые вопросы
                open_answers=[],    # Ответы на открытые вопросы
                test_stage="closed",  # Начинаем с закрытых вопросов
                migration_state = "step_12_testing",
                current_course = current_course
                )
            await save_cursor(callback.user_id, extra_data = dict(
                closed_questions=closed_questions,
                open_questions=open_questions,
                current_question=0,
                closed_answers=[],  # Ответы на закрытые вопросы
                open_answers=[],    # Ответы на открытые вопросы
                test_stage="closed",  # Начинаем с закрытых вопросов
                migration_state = "step_12_testing",
                current_course= current_course
            ))
            
        else:
            data = dict()
            data.update(
                closed_questions=closed_questions,
                open_questions=open_questions,
                current_question=0,
                closed_answers=[],  # Ответы на закрытые вопросы
                open_answers=[],    # Ответы на открытые вопросы
                test_stage="closed",  # Начинаем с закрытых вопросов
                migration_state = "step_12_testing",
                current_course= current_course
                )
            await save_cursor(callback.user_id, extra_data = dict(
                closed_questions=closed_questions,
                open_questions=open_questions,
                current_question=0,
                closed_answers=[],  # Ответы на закрытые вопросы
                open_answers=[],    # Ответы на открытые вопросы
                test_stage="closed",  # Начинаем с закрытых вопросов
                migration_state = "step_12_testing",
                current_course= current_course
            ))
            
        logger.info(f'[start_testing_block1_handler] после добавления вопросов в state: {data=}')  
        cursor.change_data(data)
        # Отправляем первый закрытый вопрос
        logger.info(f'[start_testing_block1_handler] Отправляем первый закрытый вопрос')
        course_name = get_current_course(cursor)
        logger.info(f'{course_name=}')
        if course_name not in  ["Другой сотрудник", "Обучение по продукту"]:
            await send_question_step_12(callback, cursor, "final_test", "Обучение по продажам")
        else:
            #await send_question_step_12(callback, cursor, 'final_test', 'Другой сотрудник') # !!!!!!
            await send_question_step_12(callback, cursor, 'final_test', 'Обучение по продукту')
        #cursor.change_data(data)  # !!!!!!!!!!
        cursor.change_state(TrainingStates.step_12_testing)
        await save_cursor(callback.user_id, extra_data = {'final_block_1_flag': True})
        

    except Exception as e:
        logger.error(f"[ERROR][start_testing_block1_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)       
         


@router.on_message(state(TrainingStates.check_answer_to_open_question))
async def check_valid_answer_of_question(message: Message, cursor: FSMCursor):
    """Проверка валидности введенного пользователем ответа на открытый вопрос"""
    try:
        logger.info("Стартовал")
        data = cursor.get_data()
        open_answers = data.get("open_answers", []) if data else await get_value_from_redis(message.user_id, "open_answers")
        current = data.get("current_question") if data else await get_value_from_redis(message.user_id, "current_question")
        migration_state = data.get("migration_state") if data else await get_value_from_redis(message.user_id, "migration_state")
        
        user_answer = message.body.text.strip()
        
        if len(user_answer) < 10:
            await message.send(
                "⚠️ Ответ слишком короткий. Пожалуйста, дайте более развёрнутый ответ."
            )
            return
        
        logger.info(f"[INFO][check_valid_answer_of_question] Сохраняем ответ пользователя и переходим к следующему вопросу")
        open_answers.append(user_answer)
        if data:
            data.update(open_answers=open_answers, current_question=current + 1)
        else:
            data = await load_cursor(message.user_id)
            data.update(open_answers=open_answers, current_question=current + 1)
        await save_cursor(message.user_id, extra_data=dict(open_answers=open_answers, current_question=current + 1))
        cursor.change_data(data)
        cursor.change_state(migration_state) # 'step_12_testing' или 'block_2_final_testing'
        
        if migration_state == 'step_12_testing': 
            await block1_final_testing_handler(message, cursor)
            return
        elif migration_state == 'block_2_final_testing': 
            await block2_final_testing_handler(message, cursor)
            return
        elif migration_state == 'block_3_final_testing': 
            await block3_final_testing_handler(message, cursor)
            return
        elif migration_state == 'block_4_final_testing': 
            await block4_final_testing_handler(message, cursor)
            return
        elif migration_state == 'block_5_final_testing': 
            await block5_final_testing_handler(message, cursor)
            return
        elif migration_state == 'block_6_final_testing': 
            await block6_final_testing_handler(message, cursor)
            return
        elif migration_state == 'block_7_final_testing': 
            await block7_final_testing_handler(message, cursor)
            return
        elif migration_state == 'module_0_final_testing':
            await kb_module_0_final_testing_handler(message, cursor)
            return
        elif migration_state == 'module_1_final_testing':
            await kb_module_1_final_testing_handler(message, cursor)
            return
        elif migration_state == 'module_2_final_testing':
            await kb_module_2_final_testing_handler(message, cursor)
            return
        elif migration_state == 'module_3_final_testing':
            await kb_module_3_final_testing_handler(message, cursor)
            return
        elif migration_state == 'module_4_final_testing':
            await kb_module_4_final_testing_handler(message, cursor)
            return
        elif migration_state == 'module_5_final_testing':
            await kb_module_5_final_testing_handler(message, cursor)
            return
        elif migration_state == 'module_6_final_testing':
            await kb_module_6_final_testing_handler(message, cursor)
            return
        elif migration_state == 'module_7_final_testing':
            await kb_module_7_final_testing_handler(message, cursor)
            return
            
               
        #await send_question_step_12(message, cursor, 'final_test', 'Обучение по продажам')
        
    except Exception as e:
        logger.error(f'[ERROR][check_valid_answer_of_question] Произошла ошибка {e}')


async def send_question_step_12(message: Message | Callback, cursor: FSMCursor, lesson_id: str, course_name: str = "Обучение по продажам"):
    """Отправка вопроса для step_12 (закрытые или открытые)"""
    try:
        logger.info("[send_question_step12] Стартовал")
        # send_question_flag = await get_value_from_redis(message.user_id, 'send_question_flag')
        # if send_question_flag:
        #     await del_value_from_redis(message.user_id, 'send_question_flag')
        #     return
        await save_cursor(message.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        data:dict = cursor.get_data()
        logger.info(f'{data=}')
        
        lawyer_finish_flag = data.get('lawyer_finish_flag')
        logger.info(f'{lawyer_finish_flag=}')
        
        course_name = get_current_course(cursor)
        logger.info(f'{course_name=}')
        if not course_name:
            course_name = "Обучение по продажам"
        
        if not data:
            logger.info(f'Возможно сервер был перезагружен, пробуем получить значение test_stage из redis_storage')
            # data = dict()
            # stage = data.get("test_stage", "closed")
            stage = await get_value_from_redis(message.user_id, 'test_stage')
            logger.info(f'Значение из redis_storage: {stage=}')
        else:
            stage = data.get("test_stage")
            logger.info(f'Значение из cursor: {stage=}')
            current = data.get("current_question")
            logger.info(f'{current=}')
            # await save_cursor(message.user_id, extra_data={'send_question_flag': True})
        
        if stage == "closed":
            # ЗАКРЫТЫЕ ВОПРОСЫ (с кнопками)
            closed_questions = data.get("closed_questions") if data else await get_value_from_redis(message.user_id, "closed_questions")
            current = data.get("current_question") if data else await get_value_from_redis(message.user_id, "current_question")
            logger.info(f'{current=}')
            logger.info(f"[send_question_step12] {closed_questions=}")
                        
            if current >= len(closed_questions):
                # Закрытые вопросы закончились → переходим к открытым
                logger.info("[send_question_step12] Закрытые вопросы закончились → переходим к открытым")
                if data:
                    data.update(test_stage="open", current_question=0)
                    await save_cursor(message.user_id, extra_data={"test_stage": "open", "current_question": 0})
                    cursor.change_data(data)
                else:
                    extra_data = await load_cursor(message.user_id)
                    logger.info(f'{extra_data=}')
                    extra_data.update(test_stage="open", current_question=0)
                    await save_cursor(message.user_id, extra_data = {**extra_data})
                    cursor.change_data(extra_data)
                
                # Сообщение о переходе к открытым вопросам
                if isinstance(message, Callback):
                    await message.message.delete()
                await message.send(
                "✅ **Часть 1 завершена!**\n\n"
                "Теперь переходим к **открытым вопросам**.\n\n"
                "Отвечайте своими словами, развёрнуто. Ваши ответы будут оценены автоматически."
                )
            
                await asyncio.sleep(2)
                await send_question_step_12(message, cursor, lesson_id, course_name)
                return   

            logger.info("[send_question_step12] еще не все вопросы пройдены, продолжаем...")
            question_data = closed_questions[current] #if not current else closed_questions[current - 1] 
            logger.info(f"[send_question_step12] текущий вопрос: {question_data=}")
        
            # Текст вопроса
            text = f"**Вопрос {'1' if not current else int(current) + 1}/{len(closed_questions)}**\n\n📝 **{question_data['question']}**\n"
            
            # Текст вариантов ответов
            answers_text = "\n**Варианты ответов:**\n\n"
            for answer in question_data.get('options'):
                answers_text += f'{answer}\n'
            
            correct_answer = question_data.get('correct')
            logger.info(f'{correct_answer=}')
            if data:
                logger.info("[INFO][send_question_step12] обновляем информацию о правильном ответе в cursor")
                data.update(correct = correct_answer, current_question = current)
                logger.info(f"[INFO][send_question_step12] обновляем значение всего cursor\nstate = {cursor.get_state()}")
                cursor.change_data(data)
            else:
                logger.info("[INFO][send_question_step12] обновляем информацию о правильном ответе в redis_storage")
                extra_data = await load_cursor(message.user_id)
                logger.info(f'{extra_data=}')
                extra_data.update(correct = correct_answer, current_question = current)
                cursor.change_data(extra_data)
                
            kb = await variants_questions_kb(question_data, message.user_id)
            
            if isinstance(message, Callback):
                await message.message.delete()
            await message.send(text + answers_text, keyboard=kb)
            return

        elif stage == "open":
            # ОТКРЫТЫЕ ВОПРОСЫ (текстовый ввод)
            open_questions = data.get("open_questions") if data else await get_value_from_redis(message.user_id, "open_questions")
            current = data.get("current_question") if data else await get_value_from_redis(message.user_id, "current_question")
            
            if current >= len(open_questions):
                logger.info(f"[INFO][send_question_step12] Все вопросы закончились → показываем результаты")
                # Все вопросы закончились → показываем результаты
                await show_results_step12(message, cursor, lesson_id, course_name)
                return
            
            # Отправляем открытый вопрос
            question_data = open_questions[current]
            await save_cursor(message.user_id, extra_data = {"question_data": question_data})
            state = cursor.get_state() 
            state_name = state.state if all([state, not isinstance(state, str)]) else state
            if not state_name:
                state_name = await get_value_from_redis(message.user_id, 'state_name')
            logger.info(f'{state_name=}\n{cursor.get_data()}')
            
            if state_name == 'block_7_final_testing' or lawyer_finish_flag:
                text = f"**Вопрос {21 + current}/30** (открытый вопрос)\n\n{question_data['question']}\n\n_Ответьте развёрнуто своими словами._"
            else:
                text = f"**Вопрос {11 + current}/15** (открытый вопрос)\n\n{question_data['question']}\n\n_Ответьте развёрнуто своими словами._"
        
            await message.send(text, format="markdown")
            cursor.change_state(TrainingStates.check_answer_to_open_question)
            await save_cursor(message.user_id, extra_data=dict(state_name = TrainingStates.check_answer_to_open_question))
            return
        
    except Exception as e:
        logger.error(f'[ERROR][send_question_step12] Произошла ошибка {e}')
    finally:
        await remove_repeat_flag(message.user_id) 
        
        
async def send_message_safely(message, text: str, max_length: int = 3700, format: str = "markdown"):
    """
    Безопасно отправляет сообщение, разбивая его на части, если оно превышает max_length.

    Args:
        message: объект сообщения для отправки (должен иметь метод send)
        text: текст для отправки
        max_length: максимальная длина одной части сообщения (по умолчанию 3700)
        format: формат сообщения для параметра format в send (по умолчанию "markdown")
    """
    if len(text) <= max_length:
        # Отправляем целиком, если длина в пределах лимита
        await message.send(text, format=format)
    else:
        # Разбиваем текст на части по max_length символов
        parts = [text[i:i + max_length] for i in range(0, len(text), max_length)]

        # Отправляем каждую часть последовательно
        for part in parts:
            await message.send(part, format=format)



async def show_results_step12(message: Message, cursor: FSMCursor, lesson_id: str, course_name: str):
    """Показ результатов финального теста step_12"""
    try:
        logger.info("[INFO][show_results_step12] Стартовал")
        #await save_cursor(message.user_id, extra_data={'current_course': course_name})
        if isinstance(message, Callback):
            await message.message.delete()
        data = cursor.get_data()
        closed_questions = data.get("closed_questions")
        open_questions = data.get("open_questions")
        closed_answers = data.get("closed_answers")
        open_answers = data.get("open_answers")
        if "migration_state" in data:
            migration_state = data.get("migration_state")
            logger.info(f"[INFO][show_results_step12] {closed_answers=} {open_answers=} {migration_state=}")
        else:
            logger.info(f"[INFO][show_results_step12] {closed_answers=} {open_answers=}")
        
        # Показываем сообщение о проверке
        checking_msg = await message.send("⏳ **Проверяю ваши ответы...**\n\nЭто может занять некоторое время.", format="markdown")
        
        # ==========================================
        # ЧАСТЬ 1: Проверка закрытых вопросов
        # ==========================================
        closed_correct = 0
        closed_mistakes = []
        
        for i, question in enumerate(closed_questions):
            logger.info(f"[INFO][show_results_step12] Вопрос № {i}:\n{question}")
            if i < len(closed_answers) and closed_answers[i] == question["correct"]:
                logger.info(f"[INFO][show_results_step12] ответ правильный")
                closed_correct += 1
            else:
                user_ans = closed_answers[i] if i < len(closed_answers) else "Нет ответа"
                logger.info(f"[INFO][show_results_step12] ответ не правильный (или нет ответа)")
                correct_ans = question["correct"]
                logger.info(f"[INFO][show_results_step12] правильным должен был быть вариант ответа: {correct_ans}")
                
                # Находим полный текст ответа пользователя
                user_option = "Нет ответа"
                if user_ans != "Нет ответа":
                    user_option = [opt for opt in question["options"] if opt.startswith(user_ans)]
                    user_option = user_option[0] if user_option else user_ans
                logger.info(f"[INFO][show_results_step12] полный текст ответа пользователя: {user_option}")
                
                # Находим полный текст правильного ответа
                correct_option = [opt for opt in question["options"] if opt.startswith(correct_ans)][0]
                logger.info(f"[INFO][show_results_step12] полный текст правильного ответа: {correct_option}")
                
                closed_mistakes.append({
                    "number": i + 1,
                    "question": question["question"],
                    "user_answer": user_option,
                    "correct_answer": correct_option
                })
                
                logger.info(f"[INFO][show_results_step12] добавили информацию об ошибочном ответе пользователя")
                
        # ==========================================
        # ЧАСТЬ 2: Проверка открытых вопросов через AI
        # ==========================================
        
        giga_service = GigaChatService()
        #claude = ClaudeService()
        open_scores = []
        open_mistakes = []
        giga_comments = []
        logger.info(f'[INFO][show_results_step12] Инициализировали список {open_mistakes=}')
        
        for i, question in enumerate(open_questions):
            if i >= len(open_answers):
                open_scores.append(0)
                open_mistakes.append({
                    "number": 11 + i,
                    "question": question["question"],
                    "user_answer": "Нет ответа",
                    "feedback": "Вы не ответили на вопрос.",
                    "score": 0
                })
                continue
            
            user_answer = open_answers[i]
            ideal_answer = question["ideal_answer"]
            
            # Оцениваем через GigaChat
            logger.info(f"[INFO][show_results_step12] Оцениваем через Claude AI")
            evaluation = await giga_service.evaluate_answer(
                user_answer=user_answer,
                ideal_answer=ideal_answer,
                question=question["question"]
            )
            
            logger.info(f'[INFO][show_results_step12] Инициализировали список {evaluation=}')
            
            score = evaluation.get("score", 0)
            feedback = evaluation.get("feedback", "Нет фидбека")
            passed = evaluation.get("passed", False)
            ideal_answer = evaluation.get("ideal_answer", "Не нашли правильного ответа")
                  
            open_scores.append(score)
            
            if not passed:  # Если оценка < 7.0
                open_mistakes.append({
                    "number": 11 + i,
                    "question": question["question"],
                    "user_answer": user_answer[:200] + "..." if len(user_answer) > 200 else user_answer,
                    "feedback": feedback,
                    "score": score,
                    "ideal_answer": ideal_answer
                })
            
            if 7.0 < score < 10.0:
                giga_comments.append({
                    "number": 11 + i,
                    "question": question["question"],
                    "user_answer": user_answer[:200] + "..." if len(user_answer) > 200 else user_answer,
                    "feedback": feedback,
                    "score": score,
                    "ideal_answer": ideal_answer
                })
                
                
    
        await checking_msg.delete()
        
        # ==========================================
        # РАСЧЁТ ДЛЯ ОТОБРАЖЕНИЯ РЕЗУЛЬТАТОВ
        # ==========================================
        logger.info(f"[INFO][show_results_step12] РАСЧЁТ ДЛЯ ОТОБРАЖЕНИЯ РЕЗУЛЬТАТОВ")
        open_correct = sum(1 for score in open_scores if score >= 7.0)
        total_correct = closed_correct + open_correct
        total_questions = len(closed_questions) + len(open_questions)
        
        # Процент для отображения
        accuracy_percent = (total_correct / total_questions) * 100 if total_questions > 0 else 0
        
        # ==========================================
        # ОБНОВЛЯЕМ ПРОГРЕСС (нормализация к 15 вопросам)
        # ==========================================
        logger.info(f"[INFO][show_results_step12] ОБНОВЛЯЕМ ПРОГРЕСС (нормализация к 15 вопросам)")
        # Закрытые: считаем как есть (из 10)
        closed_correct_for_progress = closed_correct
        
        # Открытые: нормализуем баллы к количеству вопросов (из 5)
        # Максимум баллов за открытые: 5 вопросов × 10 баллов = 50
        open_max_score = len(open_questions) * 10
        open_total_score = sum(open_scores)
        open_correct_equivalent = (open_total_score / open_max_score) * len(open_questions) if open_max_score > 0 else 0
        
        # Итого для статистики (из 15 вопросов)
        logger.info(f"[INFO][show_results_step12] Итого для статистики (из 15 вопросов)")
        total_correct_for_progress = closed_correct_for_progress + open_correct_equivalent
        total_questions_for_progress = len(closed_questions) + len(open_questions)  # 15
        
        game = GamificationService(course_name)
        user_data = load_user_data()
        user_id = str(message.user_id)
        
        
        
        first_name = user_data.get(user_id).get("first_name")
        last_name = user_data.get(user_id).get("second_name")
               
        await game.update_lesson_progress(
            user_id=message.user_id,
            course_name=course_name, #  "Обучение по продажам",
            correct_count=int(round(total_correct_for_progress)),  # Округляем
            total_count=total_questions_for_progress,               # 15
            lesson_id=lesson_id, #"final_test",
            user_data={
                "username": f'{first_name} {last_name}',
                "first_name": first_name,
                "last_name": last_name
            }
        )
        
        
        logger.info(f"Значение state_name курсора: {cursor.get_state()} ")
        full_completed_lessons, current_persent = game.get_full_completed_lessons(course_name = course_name, user_id = user_id)
        logger.info(f'{full_completed_lessons=}')
        
        
        
        if cursor.get_state() == 'block_7_final_testing':
            data = game._load_data()
            course_progress = data[user_id]['courses'][course_name]
            correct_answers = course_progress.get('correct_answers')
            total_answers = course_progress.get('total_answers')       
            game.record_course_completion_attempt(int(user_id), correct_answers=correct_answers, total_answers=total_answers)
        
        if cursor.get_state() == 'step_12_testing' and course_name != 'Обучение для юриста':
            data = game._load_data()
            course_progress = data[user_id]['courses'][course_name]
            correct_answers = course_progress.get('correct_answers')
            total_answers = course_progress.get('total_answers')       
            game.record_course_completion_attempt(int(user_id), correct_answers=correct_answers, total_answers=total_answers, course_name="Обучение по продукту")
            #game.record_course_completion_attempt(int(user_id), correct_answers=correct_answers, total_answers=total_answers, course_name="Другой сотрудник") # !!!!!!!!!!
        
        if all([cursor.get_state() == 'step_12_testing', course_name == 'Обучение для юриста', full_completed_lessons > 10]):
            data = game._load_data()
            course_progress = data[user_id]['courses'][course_name]
            correct_answers = course_progress.get('correct_answers')
            total_answers = course_progress.get('total_answers')       
            game.record_course_completion_attempt(int(user_id), correct_answers=correct_answers, total_answers=total_answers, course_name="Обучение для юриста")
            
        
        # ==========================================
        # ИТОГОВЫЙ ОТЧЁТ
        # ==========================================
        logger.info(f"[INFO][show_results_step12] ИТОГОВЫЙ ОТЧЁТ")
        
        logger.info(f"[INFO][show_results_step12] Получаем обновлённый прогресс пользователя")
        
        progress = ''
        
        current_course = await get_value_from_redis(message.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        # if current_course == 'Другой сотрудник':
        progress = game.get_user_progress(message.user_id, current_course)
                
        migration_header = ''
        cursor_data = cursor.get_data()
        if migration_state == 'step_12_testing':
            logger.info(f'{cursor_data=}')
            
            migration_header = '№1'
            if cursor_data.get("current_course") in ["Другой сотрудник", "Обучение по продукту"]:
                migration_header = ''
            elif cursor_data.get("current_course") == "Обучение для юриста" and full_completed_lessons > 0:
                migration_header = int(full_completed_lessons/2)
        elif migration_state == 'block_2_final_testing':
            migration_header = '№2'
        elif migration_state == 'block_3_final_testing':
            migration_header = '№3'
        elif migration_state == 'block_4_final_testing':
            migration_header = '№4'
        elif migration_state == 'block_5_final_testing':
            migration_header = '№5'
        elif migration_state == 'block_6_final_testing':
            migration_header = '№6'
        elif migration_state == 'block_7_final_testing':
            migration_header = '№7'
        elif migration_state == 'module_0_final_testing':
            migration_header = '№0'
        elif migration_state == 'module_1_final_testing':
            migration_header = '№1'
        elif migration_state == 'module_2_final_testing':
            migration_header = '№2'
        elif migration_state == 'module_3_final_testing':
            migration_header = '№3'
        elif migration_state == 'module_4_final_testing':
            migration_header = '№4'
        elif migration_state == 'module_5_final_testing':
            migration_header = '№5'
        elif migration_state == 'module_6_final_testing':
            migration_header = '№6'
        elif migration_state == 'module_7_final_testing':
            migration_header = '№7'
            
        part_name = 'Блоку'
        if current_course == 'Обучение для конструкторов':
            part_name = 'Модулю'
               
        result_text = f"📊 **Результаты финального теста по {part_name} {migration_header}**\n\n" if migration_header else f"📊 **Результаты финального теста по Блоку**\n\n"
        result_text += f"**Правильных ответов: {total_correct}/{total_questions}**\n\n"
        result_text += f"━━━━━━━━━━━━━━━━━━━━\n\n"
        if full_completed_lessons == 12 and cursor_data.get("current_course") == "Обучение для юриста":
            result_text += f"**Часть 1 (тестовые вопросы):** {closed_correct}/20\n"
            result_text += f"**Часть 2 (открытые вопросы):** {open_correct}/10\n"
        else:
            result_text += f"**Часть 1 (тестовые вопросы):** {closed_correct}/10\n"
            result_text += f"**Часть 2 (открытые вопросы):** {open_correct}/5\n"
        result_text += f"**Итоговый процент:** {accuracy_percent:.1f}%\n\n"
        
        if total_correct == total_questions:
            if giga_comments:
                logger.info('[INFO][show_results_step12] Были неточности в ответах на открытые вопросы')
                
                result_text += "**Не точные ответы в открытых вопросах:**\n\n"
                for comment in giga_comments:
                    result_text += f"⚠️ **Вопрос {comment['number']}:** {comment['question']}\n\n"
                    result_text += f"📝 **Ваш ответ**:\n{comment['user_answer']}\n\n"
                    result_text += f"🎯 **Правильный ответ**:\n{comment['ideal_answer']}\n\n"
                    result_text += f"📊 **Оценка**: {comment['score']}/10\n\n"
                    result_text += f"💬 **Фидбек**:\n{comment['feedback']}\n\n"
                    result_text += f"━━━━━━━━━━━━━━━━━━━━\n\n"
                
            part_name = 'Блока'
            if current_course == 'Обучение для конструкторов':
                part_name = 'Модуля'
            
            result_text += f"🎉 **Отлично!**\n\nВы успешно прошли финальный тест! Поздравляем с завершением {part_name} {migration_header}!"

        
        else:
            result_text += "📝 **Есть ошибки**\n\nОзнакомьтесь с правильными ответами ниже:\n\n"
            
            # Показываем ошибки в закрытых вопросах
            if closed_mistakes:
                result_text += "**Ошибки в тестовых вопросах:**\n\n"
                for mistake in closed_mistakes:
                    result_text += f"❌ **Вопрос {mistake['number']}:** {mistake['question']}\n"
                    result_text += f"**Ваш ответ**:\n{mistake['user_answer']}\n"
                    result_text += f"**Правильный ответ**:\n{mistake['correct_answer']}\n\n"
            
            # Показываем ошибки в открытых вопросах
            if giga_comments:
                logger.info('[INFO][show_results_step12] Были неточности в ответах на открытые вопросы')
                
                result_text += "**Не точные ответы в открытых вопросах:**\n\n"
                for comment in giga_comments:
                    result_text += f"⚠️ **Вопрос {comment['number']}:** {comment['question']}\n\n"
                    result_text += f"📝 **Ваш ответ**:\n{comment['user_answer']}\n\n"
                    result_text += f"🎯 **Правильный ответ**:\n{comment['ideal_answer']}\n\n"
                    result_text += f"📊 **Оценка**:{comment['score']}/10\n\n"
                    result_text += f"💬 **Фидбек**:\n{comment['feedback']}\n\n"
                    result_text += f"━━━━━━━━━━━━━━━━━━━━\n\n"
            
            if open_mistakes:
                result_text += "**Ошибки в открытых вопросах:**\n\n"
                for mistake in open_mistakes:
                    result_text += f"❌ **Вопрос {mistake['number']}:** {mistake['question']}\n\n"
                    result_text += f"📝 **Ваш ответ**:\n{mistake['user_answer']}\n\n"
                    result_text += f"🎯 **Правильный ответ**:\n{mistake['ideal_answer']}\n\n"
                    result_text += f"📊 **Оценка**:{mistake['score']}/10\n\n"
                    result_text += f"💬 **Фидбек**:\n{mistake['feedback']}\n\n"
                    result_text += f"━━━━━━━━━━━━━━━━━━━━\n\n"
            
            result_text += "\n**Рекомендуем изучить материалы ещё раз!**"
        
        await send_message_safely(message, result_text, format="markdown")
        
        #game = GamificationService()
        
        # Переход дальше (или завершение)
        await asyncio.sleep(2) # 15
        
        # ==========================================
        # ПОКАЗЫВАЕМ РЕЙТИНГ ПО ИТОГАМ ПРОЙДЕННОГО БЛОКА
        # ==========================================
        
        # Получаем обновлённый прогресс пользователя
        # if course_name == "Обучение для юриста" and cursor.get_state() == 'step_12_testing':
        #     logger.info(f'Состояние курсора: {cursor.get_state()}')
            
            
        #     return
            
        

        # elif current_course == 'Обучение по продажам':
        #     progress = game.get_user_progress(message.user_id, "Обучение по продажам")
        # elif current_course == 'Обучение для юриста':
        #     progress = game.get_user_progress(message.user_id, current_course)
        
        logger.info(f"[INFO][show_results_step12] {progress=}")
        
        # Получаем место пользователя в рейтинге
        logger.info(f"[INFO][show_results_step12] Получаем место пользователя в рейтинге")
        leaderboard = game.get_all_users_progress(course_name = current_course if not course_name else course_name)
        user_rank = 0
        for i, user_data in enumerate(leaderboard, start=1):
            logger.info(f"[INFO][show_results_step12] {i=} \n{user_data=}")
            if isinstance(user_data, tuple):
                if user_data[1]['user_id'] == message.user_id:
                    user_rank = i
                    break
            else:    
                if user_data['user_id'] == message.user_id:
                    user_rank = i
                    break
        
        # Формируем сообщение о рейтинге
        logger.info(f"[INFO][show_results_step12] Формируем сообщение о рейтинге")
        user_data = load_user_data()
        logger.info(f"[INFO][show_results_step12] {user_data=}")
        user_id = str(message.user_id)
        first_name = user_data.get(user_id).get("first_name")
        last_name = user_data.get(user_id).get("second_name")
        
        current_course = await get_value_from_redis(message.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        # Определяем количество пройденных уроков для пользователей на курсе ДРУГОЙ СОТРУДНИК
        complet_less = 0
        completed_lesson = 0
        current_persent = 0
        total_lessons = game.total_lessons_info.get(course_name)
        
        completed_dict = {'0': 0, '1': 5, '2': 10, '3': 15, '4': 20, '5': 25, '6': 30, '7': 45}
        
        logger.info(f'{progress=}')
                
        part_name = 'Блока'
        if current_course == 'Обучение для конструкторов':
            part_name = 'Модуля'
        
        max_progress = get_max_accuracy_item(progress)
            
        if isinstance(progress, list):
            #max_progress = get_max_accuracy_item(progress)
            logger.info(f'{max_progress=}')
            completed_lesson = max_progress['lessons_completed']
            logger.info(f'{completed_lesson=}')
            if current_course == 'Другой сотрудник':
                if int(completed_lesson) < 5:
                    completed_lesson = 0
                elif int(completed_lesson) < 10:
                    completed_lesson = 1
                elif int(completed_lesson) < 15:
                    completed_lesson = 2
                elif int(completed_lesson) < 20:
                    completed_lesson = 3
                elif int(completed_lesson) < 25:
                    completed_lesson = 4
                elif int(completed_lesson) < 30:
                    completed_lesson = 5
                elif int(completed_lesson) < 43:
                    completed_lesson = 6
                else:
                    completed_lesson = 7
                           
            
            
            first_phrase = f"🏆 **Ваш рейтинг по итогам {part_name} {migration_header}**\n\n" if migration_header else "🏆 **Ваш рейтинг по итогам Блока**\n\n"
            
            if current_course == 'Обучение для юриста':
                full_completed_lessons, current_persent = game.get_full_completed_lessons(course_name = current_course, user_id = user_id)
                completed_lesson = int(completed_lesson)
                first_phrase = f"🏆 **Ваш рейтинг по итогам Блока {int(full_completed_lessons/2)}**\n\n"
                if completed_lesson == 12:
                    first_phrase = f"🏆 **Ваш рейтинг по итогам курса**\n\n"
                        
            rating_text = (
                f"{first_phrase}"
                f"👤 **Ваше имя:** {first_name} {last_name}\n"
                # f"📚 **Курс:** {'Обучение по продажам' if current_course != 'Другой сотрудник' else current_course}\n\n"
                f"📚 **Курс:** {current_course}\n\n"
                # f"✅ **Уроков пройдено:** {completed_lesson} / {43 if current_course != 'Другой сотрудник' else 7}\n"   # f"✅ **Уроков пройдено:** {progress['lessons_completed']} / {progress['total_lessons']}\n"
                f"✅ **Уроков пройдено:** {full_completed_lessons} / {total_lessons}\n"
            )
            
            if full_completed_lessons != 12 and current_course == 'Обучение для юриста':
                rating_text += f"📈 **Процент правильных ответов:** {current_persent}%\n"
            elif full_completed_lessons != 10 and current_course == 'Регулярный менеджмент':
                rating_text += f"📈 **Процент правильных ответов:** {current_persent}%\n"
            else:
                rating_text += f"📈 **Процент правильных ответов:** {max_progress['accuracy_percent']:.1f}%\n"
        else:            
            logger.info(f'{max_progress=}')
            completed_lesson = progress[1]['lessons_completed']
            logger.info(f'{completed_lesson=}')
            
            first_phrase = f"🏆 **Ваш рейтинг по итогам {part_name} {migration_header}**\n\n" if migration_header else "🏆 **Ваш рейтинг по итогам Блока**\n\n"
            
            if current_course == 'Другой сотрудник':
                if int(completed_lesson) < 5:
                    completed_lesson = 0
                elif int(completed_lesson) < 10:
                    completed_lesson = 1
                elif int(completed_lesson) < 15:
                    completed_lesson = 2
                elif int(completed_lesson) < 20:
                    completed_lesson = 3
                elif int(completed_lesson) < 25:
                    completed_lesson = 4
                elif int(completed_lesson) < 30:
                    completed_lesson = 5
                elif int(completed_lesson) < 43:
                    completed_lesson = 6
                else:
                    completed_lesson = 7
            elif current_course == 'Обучение для юриста':
                completed_lesson = int(completed_lesson)
                full_completed_lessons, current_persent = game.get_full_completed_lessons(course_name = current_course, user_id = user_id)
                completed_lesson = int(completed_lesson)
                first_phrase = f"🏆 **Ваш рейтинг по итогам Блока {int(full_completed_lessons/2)}**\n\n"
                if completed_lesson == 12:
                    first_phrase = f"🏆 **Ваш рейтинг по итогам курса**\n\n"
            
            rating_text = (
                f"{first_phrase}"
                f"👤 **Ваше имя:** {first_name} {last_name}\n"
                # f"📚 **Курс:** {'Обучение по продажам' if current_course != 'Другой сотрудник' else current_course}\n\n"
                f"📚 **Курс:** {current_course}\n\n"
                # f"✅ **Уроков пройдено:** {completed_lesson} / {43 if current_course != 'Другой сотрудник' else 7}\n"   # f"✅ **Уроков пройдено:** {progress['lessons_completed']} / {progress['total_lessons']}\n"
                f"✅ **Уроков пройдено:** {full_completed_lessons} / {total_lessons}\n"
            )
            if full_completed_lessons != 12 and current_course == 'Обучение для юриста':
                rating_text += f"📈 **Процент правильных ответов:** {current_persent}%\n"
            elif full_completed_lessons != 10 and current_course == 'Регулярный менеджмент':
                rating_text += f"📈 **Процент правильных ответов:** {current_persent}%\n"
            else:
                rating_text += f"📈 **Процент правильных ответов:** {max_progress['accuracy_percent']:.1f}%\n"
        
        if user_rank > 0:
            rating_text += f"🥇 **Ваше место в рейтинге:** #{user_rank}\n"
        else:
            rating_text += f"📊 **Место в рейтинге:** не определено\n"
        
        rating_text += "\n_Продолжайте обучение для повышения результатов!_"
        
        await message.send(rating_text, format="markdown")
        
        # Пауза перед кнопкой продолжения
        await asyncio.sleep(2) # 5
        
        logger.info(f'Строка 2621: {migration_header=}')
        await del_value_from_redis(message.user_id, 'migration_state')
        await save_cursor(message.user_id, extra_data = {"migration_header": migration_header})
        
        status_user = 'new_employer'
        data = cursor.get_data()
        if not data:
            data = dict()
            status_user = await get_value_from_redis(message.user_id, 'status_user')
            if not status_user:
                status_user = 'new_employer'
        else:
            status_user = data.get('status_user', 'new_employer')
        
        if course_name in ['Обучение для юриста', 'Обучение для конструкторов']:
            block_intro = "Чтобы продолжить обучение, нажмите на кнопку 📚 Продолжить обучение"
            
            logger.info(f'{migration_header=} {type(migration_header)}')
            
            if migration_header == 6 and course_name == 'Обучение для юриста':
                block_intro = get_final_lawyer_text()
                await message.send(block_intro, format="markdown", keyboard=main_one_kb())
                cursor.clear_state()
                await clear_cursor(message.user_id)
                await save_cursor(message.user_id, extra_data={'status_user': status_user, 'current_course': 'Обучение для юриста', 'migration_header': migration_header})
                return
            await message.send(block_intro, format="markdown", keyboard=next_to_educ_to_part_kb())
            if migration_header == 1 and course_name == 'Обучение для юриста':
                await clear_cursor(message.user_id)
                await save_cursor(message.user_id, extra_data={'status_user': status_user, 'current_course': 'Обучение для юриста', "state_name": TrainingStates.lawyer['block_2_start'], 'migration_header': migration_header})
                #await save_cursor(message.user_id, extra_data = {"state_name": TrainingStates.lawyer['block_2_start']})
                cursor.change_state(TrainingStates.lawyer['block_2_start'])
                return
            elif migration_header == 2 and course_name == 'Обучение для юриста':
                await clear_cursor(message.user_id)
                await save_cursor(message.user_id, extra_data={'status_user': status_user, 'current_course': 'Обучение для юриста', "state_name": TrainingStates.lawyer['block_3_start'], 'migration_header': migration_header})
                #await save_cursor(message.user_id, extra_data = {"state_name": TrainingStates.lawyer['block_3_start']})
                cursor.change_state(TrainingStates.lawyer['block_3_start'])
            elif migration_header == 3 and course_name == 'Обучение для юриста':
                await clear_cursor(message.user_id)
                await save_cursor(message.user_id, extra_data={'status_user': status_user, 'current_course': 'Обучение для юриста', "state_name": TrainingStates.lawyer['block_4_start'], 'migration_header': migration_header})
                #await save_cursor(message.user_id, extra_data = {"state_name": TrainingStates.lawyer['block_4_start']})
                cursor.change_state(TrainingStates.lawyer['block_4_start'])
            elif migration_header == 4 and course_name == 'Обучение для юриста':
                await clear_cursor(message.user_id)
                await save_cursor(message.user_id, extra_data={'status_user': status_user, 'current_course': 'Обучение для юриста', "state_name": TrainingStates.lawyer['block_5_start'], 'migration_header': migration_header})
                #await save_cursor(message.user_id, extra_data = {"state_name": TrainingStates.lawyer['block_5_start']})
                cursor.change_state(TrainingStates.lawyer['block_5_start'])
            elif migration_header == 5 and course_name == 'Обучение для юриста':
                await clear_cursor(message.user_id)
                await save_cursor(message.user_id, extra_data={'status_user': status_user, 'current_course': 'Обучение для юриста', "state_name": TrainingStates.lawyer['final_test_start'], 'migration_header': migration_header})
                #await save_cursor(message.user_id, extra_data = {"state_name": TrainingStates.lawyer['final_test_start']})
                cursor.change_state(TrainingStates.lawyer['final_test_start'])
            elif migration_header == '№0' and course_name == 'Обучение для конструкторов':
                await clear_cursor(message.user_id)
                await save_cursor(message.user_id, extra_data={'status_user': status_user, 'current_course': 'Обучение для конструкторов', "state_name": TrainingStates.konstructor['kb_module_1_start'], 'migration_header': migration_header})
                #await save_cursor(message.user_id, extra_data = {"state_name": TrainingStates.lawyer['block_3_start']})
                cursor.change_state(TrainingStates.konstructor['kb_module_1_start'])
            elif migration_header == '№1' and course_name == 'Обучение для конструкторов':
                await clear_cursor(message.user_id)
                await save_cursor(message.user_id, extra_data={'status_user': status_user, 'current_course': 'Обучение для конструкторов', "state_name": TrainingStates.konstructor['kb_module_2_start'], 'migration_header': migration_header})
                #await save_cursor(message.user_id, extra_data = {"state_name": TrainingStates.lawyer['block_3_start']})
                cursor.change_state(TrainingStates.konstructor['kb_module_2_start'])
            elif migration_header == '№2' and course_name == 'Обучение для конструкторов':
                await clear_cursor(message.user_id)
                await save_cursor(message.user_id, extra_data={'status_user': status_user, 'current_course': 'Обучение для конструкторов', "state_name": TrainingStates.konstructor['kb_module_3_start'], 'migration_header': migration_header})
                #await save_cursor(message.user_id, extra_data = {"state_name": TrainingStates.lawyer['block_3_start']})
                cursor.change_state(TrainingStates.konstructor['kb_module_3_start'])
            elif migration_header == '№3' and course_name == 'Обучение для конструкторов':
                await clear_cursor(message.user_id)
                await save_cursor(message.user_id, extra_data={'status_user': status_user, 'current_course': 'Обучение для конструкторов', "state_name": TrainingStates.konstructor['kb_module_4_start'], 'migration_header': migration_header})
                #await save_cursor(message.user_id, extra_data = {"state_name": TrainingStates.lawyer['block_3_start']})
                cursor.change_state(TrainingStates.konstructor['kb_module_4_start'])
            elif migration_header == '№4' and course_name == 'Обучение для конструкторов':
                await clear_cursor(message.user_id)
                await save_cursor(message.user_id, extra_data={'status_user': status_user, 'current_course': 'Обучение для конструкторов', "state_name": TrainingStates.konstructor['kb_module_5_start'], 'migration_header': migration_header})
                #await save_cursor(message.user_id, extra_data = {"state_name": TrainingStates.lawyer['block_3_start']})
                cursor.change_state(TrainingStates.konstructor['kb_module_5_start'])
            elif migration_header == '№5' and course_name == 'Обучение для конструкторов':
                await clear_cursor(message.user_id)
                await save_cursor(message.user_id, extra_data={'status_user': status_user, 'current_course': 'Обучение для конструкторов', "state_name": TrainingStates.konstructor['kb_module_6_start'], 'migration_header': migration_header})
                #await save_cursor(message.user_id, extra_data = {"state_name": TrainingStates.lawyer['block_3_start']})
                cursor.change_state(TrainingStates.konstructor['kb_module_6_start'])
            elif migration_header == '№6' and course_name == 'Обучение для конструкторов':
                await clear_cursor(message.user_id)
                await save_cursor(message.user_id, extra_data={'status_user': status_user, 'current_course': 'Обучение для конструкторов', "state_name": TrainingStates.konstructor['kb_module_37_start'], 'migration_header': migration_header})
                #await save_cursor(message.user_id, extra_data = {"state_name": TrainingStates.lawyer['block_3_start']})
                cursor.change_state(TrainingStates.konstructor['kb_module_7_start'])
            return
        
        logger.info(f'Строка 3704')    
        
        if migration_header == "":
            block_intro = get_final_another_emp_text()
            #await message.send(block_intro, format="markdown", keyboard=education_kb(current_cource="Другой сотрудник", final_flag=True)) # !!!!!!!!!!!!!!!!!!!!
            cursor.clear_state()
            await clear_cursor(message.user_id)
            await save_cursor(message.user_id, extra_data={'status_user': status_user, 'current_course': 'Обучение по продукту'})
            await message.send(block_intro, format="markdown", keyboard=education_kb(current_cource="Обучение по продукту", final_flag=True))
            return       
        if migration_header == "№1":
            await clear_cursor(message.user_id)
            await save_cursor(message.user_id, extra_data={'status_user': status_user, 'current_course': course_name, "state_name": TrainingStates.block2_start, 'migration_header': migration_header, 'payload': 'next_educ_to_part_2'})
            block_intro = get_block2_intro_text()
            # await message.send(block_intro, format="markdown", keyboard=next_to_educ_to_part_kb())
            # return
        elif migration_header == "№2":
            await clear_cursor(message.user_id)
            await save_cursor(message.user_id, extra_data={'status_user': status_user, 'current_course': course_name, "state_name": TrainingStates.block_2_final_testing, 'migration_header': migration_header, 'payload': 'next_educ_to_part_2'})
            block_intro = get_block3_intro_text()
        elif migration_header == "№3":
            await clear_cursor(message.user_id)
            await save_cursor(message.user_id, extra_data={'status_user': status_user, 'current_course': course_name, "state_name": TrainingStates.block_3_final_testing, 'migration_header': migration_header, 'payload': 'next_educ_to_part_2'})
            block_intro = get_block4_intro_text()
        elif migration_header == "№4":
            await clear_cursor(message.user_id)
            await save_cursor(message.user_id, extra_data={'status_user': status_user, 'current_course': course_name, "state_name": TrainingStates.block_4_final_testing, 'migration_header': migration_header, 'payload': 'next_educ_to_part_2'})
            block_intro = get_block5_intro_text()
        elif migration_header == "№5":
            await clear_cursor(message.user_id)
            await save_cursor(message.user_id, extra_data={'status_user': status_user, 'current_course': course_name, "state_name": TrainingStates.block_5_final_testing, 'migration_header': migration_header, 'payload': 'next_educ_to_part_2'})
            block_intro = get_block6_intro_text()
        elif migration_header == "№6":
            await clear_cursor(message.user_id)
            await save_cursor(message.user_id, extra_data={'status_user': status_user, 'current_course': course_name, "state_name": TrainingStates.block_6_final_testing, 'migration_header': migration_header, 'payload': 'next_educ_to_part_2'})
            block_intro = get_block7_intro_text()
        elif migration_header == "№7":
            await clear_cursor(message.user_id)
            await save_cursor(message.user_id, extra_data={'status_user': status_user, 'current_course': course_name, "state_name": TrainingStates.block_7_final_testing, 'migration_header': migration_header, 'payload': 'next_educ_to_part_2'})
            block_intro = get_final_intro_text()
            await message.send(block_intro, format="markdown", keyboard=education_kb(final_flag=True))
            cursor.clear_state()
            return
        
        await message.send(block_intro, format="markdown", keyboard=next_to_educ_to_part_kb())
        
                   
    except Exception as e:
        logger.error(f'[ERROR][show_results_step12] Произошла ошибка {e}')
        
        
# ============================================================================
# БЛОК №2: КЛИЕНТ И ЦЕЛЕВАЯ АУДИТОРИЯ
# ============================================================================

# РАЗДЕЛ № 1 ------------------

@router.on_button_callback(state(TrainingStates.step_12_testing), lambda data: data.payload == "next_educ_to_part_2")
async def start_block_2_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Обработчик завершения обучения по 1 блоку и перехода к блоку № 2 при нажатии на кнопку ПРОДОЛЖИТЬ ОБУЧЕНИЕ"""
    try:
        logger.info(f'[INFO][start_block_2_handler] Стартовал')
        cursor_redis_data = await load_cursor(callback.user_id)
        if 'state_name' in cursor_redis_data:
            del cursor_redis_data['state_name']
        if 'payload' in cursor_redis_data:
            del cursor_redis_data['payload']
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)    
        cursor.change_state(TrainingStates.block2_start)
        if continue_flag:
            intro_text = get_block2_intro_text()
            await callback.send(intro_text)
            await asyncio.sleep(2) # 10        
        
        # if await debounce_button_max(callback, cursor):
        #     return
        
        intro_text = get_block2_section1_intro_text()
        
        await callback.send(intro_text, format='markdown', disable_link_preview=True)
        
        await asyncio.sleep(2) # 15
        
        test_text = go_to_test_1_text(10)
        await callback.send(test_text, format="markdown", keyboard=start_test_kb())
        
        await save_cursor(callback.user_id, extra_data={**cursor_redis_data, 'state_name': TrainingStates.block2_section1_ready, 'payload': 'start_test'})
        cursor.change_state(TrainingStates.block2_section1_ready)
        return
        
    except Exception as e:
        logger.error(f'[ERROR][start_block_2_handler] Произошла ошибка {e}')
    finally:
        await remove_repeat_flag(callback.user_id)  
        

@router.on_button_callback(state(TrainingStates.block2_section1_ready), lambda data: data.payload == "start_test")
async def training_block_2_test_1_handler(callback: Callback, cursor: FSMCursor):
    """БЛО№ № 2 Тест 1 - Начало тестирования"""
    try:
        logger.info("[INFO][training_block_2_test_1_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2) 
        questions = get_block_2_test_1_quests()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[training_block_2_test_1_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
            
        await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        logger.info(f'[training_block_2_test_1_handler] после добавления вопросов в state: {data=}')  
        cursor.change_data(data)
        # Отправляем первый вопрос
        await send_question(callback, cursor, 'section_7')
        await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.block_2_test_1_testing))
        cursor.change_state(TrainingStates.block_2_test_1_testing)
    
    except Exception as e:
        logger.error(f"[training_block_2_test_1_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)      
       


# ============================================================================
# БЛОК №2 - РАЗДЕЛ №2: Сложные клиенты и стратегические партнёры
# ============================================================================

@router.on_button_callback(state(TrainingStates.block_2_section_2_next), lambda data: data.payload.split('::')[1] == "not_first")
async def block_2_test_2_ready_for_test_handl(callback: Callback, cursor: FSMCursor):
    """БЛОК №2 - Раздел №2: Сложные клиенты и стратегические партнёры"""
    try:
        logger.info('Стартовал')
        cursor_redis_data = await load_cursor(callback.user_id)
        if 'state_name' in cursor_redis_data:
            del cursor_redis_data['state_name']
        if 'payload' in cursor_redis_data:
            del cursor_redis_data['payload']
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)    
        await callback.message.delete()
        intro_text = get_block2_section_2_intro_text()  
        await callback.send(intro_text, disable_link_preview=True)
        
        await asyncio.sleep(2) # 15
        
        test_text = go_to_test_1_text(10)
        await callback.send(test_text, keyboard=start_test_kb())
        
        await save_cursor(callback.user_id, extra_data={**cursor_redis_data, 'state_name': TrainingStates.block_2_test_2_ready_for_test, 'payload': 'start_test'})
        cursor.change_state(TrainingStates.block_2_test_2_ready_for_test)
        
        
    except Exception as e:
        logger.error(f"[ERROR][block_2_test_2_ready_for_test_handl] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)  


@router.on_button_callback(state(TrainingStates.block_2_test_2_ready_for_test), lambda data: data.payload == "start_test")
async def training_block_2_test_2_handler(callback: Callback, cursor: FSMCursor):
    """БЛО№ № 2 Тест 2 - Начало тестирования"""
    try:
        logger.info("[INFO][training_block_2_test_2_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):'5. ООО "Альфа-Крас" — Производство малярных работ'   
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2) 
        questions = get_block_2_test_2_quests()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[training_block_2_test_2_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
        await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        logger.info(f'[training_block_2_test_2_handler] после добавления вопросов в state: {data=}')  
        cursor.change_data(data)
        # Отправляем первый вопрос
        await send_question(callback, cursor, 'section_8')
        await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.block_2_test_2_testing))
        cursor.change_state(TrainingStates.block_2_test_2_testing)
    
    except Exception as e:
        logger.error(f"[training_block_2_test_2_handler] Произошла ошибка {e}")
        
        
# ============================================================================
# БЛОК №2 - РАЗДЕЛ №3: CHAMP: метод квалификации клиентов
# ============================================================================

@router.on_button_callback(state(TrainingStates.block_2_section_3_next), lambda data: data.payload.split('::')[1] == "not_first")
async def block_2_test_3_ready_for_test_handl(callback: Callback, cursor: FSMCursor):
    """БЛОК №2 - Раздел №3: CHAMP: метод квалификации клиентов"""
    try:
        cursor_redis_data = await load_cursor(callback.user_id)
        if 'state_name' in cursor_redis_data:
            del cursor_redis_data['state_name']
        if 'payload' in cursor_redis_data:
            del cursor_redis_data['payload']
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)    
        await callback.message.delete()
        intro_text = get_block2_section_3_intro_text()  
        await callback.send(intro_text, disable_link_preview=True)
        
        await asyncio.sleep(2) # 15
        
        test_text = go_to_test_1_text(10)
        await callback.send(test_text, keyboard=start_test_kb())
        
        await save_cursor(callback.user_id, extra_data={**cursor_redis_data, 'state_name': TrainingStates.block_2_test_3_ready_for_test, 'payload': 'start_test'})
        cursor.change_state(TrainingStates.block_2_test_3_ready_for_test)
        
        
    except Exception as e:
        logger.error(f"[ERROR][block_2_test_3_ready_for_test_handl] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)   
        

@router.on_button_callback(state(TrainingStates.block_2_test_3_ready_for_test), lambda data: data.payload == "start_test")
async def training_block_2_test_3_handler(callback: Callback, cursor: FSMCursor):
    """БЛО№ № 2 Тест 3 - Начало тестирования"""
    try:
        logger.info("[INFO][training_block_2_test_3_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2) 
        questions = get_block_2_test_3_quests()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[training_block_2_test_3_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
            
        await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))    
        logger.info(f'[training_block_2_test_3_handler] после добавления вопросов в state: {data=}')  
        cursor.change_data(data)
        # Отправляем первый вопрос
        await send_question(callback, cursor, 'section_8')
        await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.block_2_test_3_testing))
        cursor.change_state(TrainingStates.block_2_test_3_testing)
    
    except Exception as e:
        logger.error(f"[training_block_2_test_3_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)    

# ============================================================================
# БЛОК №2 - РАЗДЕЛ №4: Видео-инструкция по AI-Агенту для CHAMP
# ============================================================================


@router.on_button_callback(state(TrainingStates.block_2_section_4_next), lambda data: data.payload.split('::')[1] == "not_first")
async def block_2_go_to_final_test_handl(callback: Callback, cursor: FSMCursor):
    """БЛОК №2 - Раздел №4: Видео-инструкция по AI-Агенту для CHAMP предложение 
    для перехода к финальному тесту"""
    try:
        logger.info("Стартовал")
        cursor_redis_data = await load_cursor(callback.user_id)
        if 'state_name' in cursor_redis_data:
            del cursor_redis_data['state_name']
        if 'payload' in cursor_redis_data:
            del cursor_redis_data['payload']
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)    
        await callback.message.delete()
        intro_text = get_block2_section_4_intro_text()  
        await callback.send(intro_text, disable_link_preview=True)
        
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        
        await asyncio.sleep(2) # 15
        game = GamificationService(current_course)
        game.increment_lessons_completed(callback.user_id, increment_lesson=1)
        
        continue_text = "📚 Вы можете продолжить обучение, нажав кнопку ниже 👇"
    
        kb = next_to_educ_to_part_kb()
    
        await callback.send(continue_text, keyboard=kb)
        cursor.change_state(TrainingStates.block2_final_test)
                
        await save_cursor(callback.user_id, extra_data={**cursor_redis_data, 'state_name': TrainingStates.block2_final_test, 'payload': 'ai_after_block2'})
        
    except Exception as e:
        logger.error(f"[ERROR][block_2_go_to_final_test_handl] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)  
        


@router.on_button_callback(state(TrainingStates.block2_final_test), lambda data: data.payload == "next_educ_to_part_2")
async def continue_after_block2_handler(callback: Callback, cursor: FSMCursor):
    """Завершение Блока №2 - Клиент и ЦА. Переход к вопросам или финальному тесту"""
    try:
        logger.info(f"[continue_after_block2_handler] Стартовал")
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)    
        # Проверяем загрузку базы знаний
        rag = RAGService()
        stats = rag.get_stats()
        
        if not stats['is_loaded']:
            await callback.send(
                "❌ База знаний не загружена. Обратитесь к администратору.",
                keyboard=main_menu_keyboard(current_course)
            )
            cursor.clear()
            return
        
        text = get_text_to_final_test_block_2()
        
        #await callback.send(text)
        await callback.send(text, keyboard=final_start_test_kb())
        cursor.change_state(TrainingStates.block2_questions)
        await save_cursor(callback.user_id, extra_data = {'payload': 'to_final_test', 'state_name': TrainingStates.block2_questions, 'current_course': current_course})
        
        # await asyncio.sleep(2)
        # await start_block2_final_test_handler(callback, cursor)
        return
        
    
    except Exception as e:
        logger.error(f"[continue_after_block2_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)   
        

@router.on_button_callback(state(TrainingStates.block2_questions), lambda data: data.payload == 'to_final_test')
async def start_block2_final_test_handler(callback: Callback, cursor: FSMCursor):
    """Переход к финальному тесту по Блоку №2"""
    try:
        logger.info(f"[INFO][start_block2_final_test_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)    
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        text = get_text_start_final_test_block_2()
        
        data = cursor.get_data()
        if not data:
            data = dict()
            status_user = await get_value_from_redis(callback.user_id, 'status_user')
            if not status_user:
                status_user = 'new_employer'
        else:
            status_user = data.get('status_user', 'new_employer')
        logger.info(f'{current_course=} {status_user=}')
        data.update(current_question=0, current_course=current_course, status_user=status_user)
        cursor.change_data(data)
        await callback.send(text, keyboard=final_test_kb())
        cursor.change_state(TrainingStates.block_2_final_testing)
        await save_cursor(callback.user_id, extra_data = {**data, 'state_name': TrainingStates.block_2_final_testing, 'payload': 'start_final_test'})
           
    
    except Exception as e:
        logger.error(f"[ERROR][start_block2_final_test_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 
    

@router.on_message(state(TrainingStates.lawyer['block2_questions']))
@router.on_message(state(TrainingStates.block2_questions))
async def answer_block2_question_handler(message: Message, cursor: FSMCursor, state_name: str = None):
    """Ответы на вопросы по Блоку 2 через RAG + Claude"""
    try:
        logger.info(f"[INFO][answer_block2_question_handler] Стартовал")
        cursor_redis_data = await load_cursor(message.user_id)
        del cursor_redis_data['state_name']
        await save_cursor(message.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)  
        # Показываем процесс
        thinking_msg = await message.send("🔍 Ищу информацию в базе знаний...")
        
        if not state_name:
            state = cursor.get_state() # изменил 12.07.26 !!!!!
            state_name = state.state if all([state, not isinstance(state, str)]) else state
            logger.info(f'Из курсора:{state_name=}')
        else:
            logger.info(f'Из аргумента обработчика:{state_name=}')
        
        if state_name in ['block1_questions_lawyer', 'block2_questions_lawyer', 'block3_questions_lawyer',
                          'block4_questions_lawyer']:
            rag = RAGService(branch_name = 'lawyer')
        else:
            rag = RAGService()
        
        answer = await rag.answer_question(message.body.text)
        
        await thinking_msg.delete() 
        
        # Форматируем ответ
        logger.info(f"[INFO][answer_block2_question_handler] Форматируем ответ") 
        response_text = (
            f"💡 **Ответ по Блоку №2:**\n\n"
            f"{answer}\n\n"
            "➡️ Задайте следующий вопрос или нажмите 📝 **Перейти к тестированию**"
        )
        
        await message.send(response_text, keyboard=final_start_test_kb(), format='markdown')
        
        cursor.change_state(state_name)
        await save_cursor(message.user_id, extra_data = {**cursor_redis_data, 'state_name': state_name})
         
    
    except Exception as e:
        await thinking_msg.delete()
        logger.error(f"[ERROR][answer_block2_question_handler] Произошла ошибка {e}")   

        await message.send(
            "❌ Произошла ошибка при обработке вопроса.\n\n"
            "Попробуйте задать вопрос ещё раз или обратитесь к администратору.",
            keyboard=final_start_test_kb()
        )
    finally:
        await remove_repeat_flag(message.user_id) 


@router.on_message(state(TrainingStates.block_2_final_testing))
async def block2_final_testing_handler(message: Message, cursor: FSMCursor):
    """Ответы на вопросы по Блоку 2 через RAG + Claude"""
    try:
        logger.info(f"[INFO][answer_block2_question_handler] Стартовал")   
        
        await asyncio.sleep(2)
        course_name = await get_value_from_redis(message.user_id, 'current_course')
        if not course_name:
            course_name = get_current_course(cursor)
        logger.info(f'{course_name=}')
        await send_question_step_12(message, cursor, 'section_10', course_name)
        return
    
    except Exception as e:
        #await thinking_msg.delete()
        logger.error(f"[ERROR][answer_block2_question_handler] Произошла ошибка {e}")   

        await message.send(
            "❌ Произошла ошибка при обработке вопроса.\n\n"
            "Попробуйте задать вопрос ещё раз или обратитесь к администратору.",
            keyboard=final_start_test_kb()
        )

# ============================================================================
# ШАГ № __: ФИНАЛЬНОЕ ТЕСТИРОВАНИЕ ПО БЛОКУ № 2 (10 закрытых + 5 открытых)
# ============================================================================


@router.on_button_callback(state(TrainingStates.block_2_final_testing), lambda data: data.payload == 'start_final_test')
async def start_testing_block2_handler(callback: Callback, cursor: FSMCursor):
    """ШАГ № __ - Запуск финального тестирования по Блоку 2"""
    try:
        logger.info(f"[INFO][start_testing_block2_handler] Стартовал")
        await del_value_from_redis(callback.user_id, 'payload')
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        # ЧАСТЬ 1: Закрытые вопросы (10 вопросов с вариантами A/B/C/D)
        closed_questions = get_final_test_block_2('close')
        
        # ЧАСТЬ 2: Открытые вопросы (5 вопросов с эталонными ответами)
        open_questions = get_final_test_block_2('open')
        
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        logger.info(f'{current_course=}')
        
        data = cursor.get_data()
        logger.info(f'[start_testing_block2_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(
                closed_questions=closed_questions,
                open_questions=open_questions,
                current_question=0,
                closed_answers=[],  # Ответы на закрытые вопросы
                open_answers=[],    # Ответы на открытые вопросы
                test_stage="closed",  # Начинаем с закрытых вопросов
                migration_state = "block_2_final_testing",
                current_course = current_course
                )
            await save_cursor(callback.user_id, extra_data = dict(
              closed_questions=closed_questions,
                open_questions=open_questions,
                current_question=0,
                closed_answers=[],  # Ответы на закрытые вопросы
                open_answers=[],    # Ответы на открытые вопросы
                test_stage="closed",  # Начинаем с закрытых вопросов
                migration_state = "block_2_final_testing",
                current_course = current_course  
            ))
        else:
            data = dict()
            data.update(
                closed_questions=closed_questions,
                open_questions=open_questions,
                current_question=0,
                closed_answers=[],  # Ответы на закрытые вопросы
                open_answers=[],    # Ответы на открытые вопросы
                test_stage="closed",  # Начинаем с закрытых вопросов
                migration_state = "block_2_final_testing",
                current_course = current_course
                )
            await save_cursor(callback.user_id, extra_data = dict(
                closed_questions=closed_questions,
                open_questions=open_questions,
                current_question=0,
                closed_answers=[],  # Ответы на закрытые вопросы
                open_answers=[],    # Ответы на открытые вопросы
                test_stage="closed",  # Начинаем с закрытых вопросов
                migration_state = "block_2_final_testing",
                current_course = current_course  
            ))
            
        logger.info(f'[start_testing_block2_handler] после добавления вопросов в state: {data=}')  
        cursor.change_data(data)  # !!!!!!!!!!
        # Отправляем первый закрытый вопрос
        logger.info(f'[start_testing_block2_handler] Отправляем первый закрытый вопрос')
        await send_question_step_12(callback, cursor, "section_10")
       
        cursor.change_state(TrainingStates.block_2_final_testing)
        await save_cursor(callback.user_id, extra_data = {'final_block_2_flag': True, 'state_name': TrainingStates.block_2_final_testing})
        

    except Exception as e:
        logger.error(f"[ERROR][start_testing_block2_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)  




#####################################################
@router.on_button_callback(state(TrainingStates.konstructor['module_7_final_testing']))
@router.on_button_callback(state(TrainingStates.konstructor['module_6_final_testing']))
@router.on_button_callback(state(TrainingStates.konstructor['module_5_final_testing']))
@router.on_button_callback(state(TrainingStates.konstructor['module_4_final_testing']))
@router.on_button_callback(state(TrainingStates.konstructor['module_3_final_testing']))
@router.on_button_callback(state(TrainingStates.konstructor['module_2_final_testing']))
@router.on_button_callback(state(TrainingStates.konstructor['module_1_final_testing']))
@router.on_button_callback(state(TrainingStates.konstructor['module_0_final_testing']))
@router.on_button_callback(state(TrainingStates.block_7_final_testing))
@router.on_button_callback(state(TrainingStates.block_6_final_testing))
@router.on_button_callback(state(TrainingStates.block_5_final_testing))
@router.on_button_callback(state(TrainingStates.block_4_final_testing))
@router.on_button_callback(state(TrainingStates.block_3_final_testing))
@router.on_button_callback(state(TrainingStates.block_2_final_testing))
@router.on_button_callback(state(TrainingStates.step_12_testing))
async def final_process_answer_handler(callback: Callback, cursor: FSMCursor):
    """Обрабатывает ответ пользователя в финальном блоке тестирования"""
    try:
        logger.info(f"[INFO][final_process_answer_handler] Стартовал")   
        data:dict = cursor.get_data()
        logger.info(f"[INFO][final_process_answer_handler] {data=}")   
        if data:
            answers = data.get("open_answers", [])
            closed_answers = data.get("closed_answers", [])
            current = data.get("current_question")
            await save_cursor(callback.user_id, extra_data = dict(current_question = current + 1))
            correct = data.get("correct")
            current_course = data.get('current_course')
            migration_state = data.get('migration_state')
            if not migration_state and current_course == "Обучение для конструкторов":
                logger.info('Пытаемся получить значение migration_state из redis')
                migration_state = await get_value_from_redis(callback.user_id, 'migration_state')
            logger.info(f'Из курсора:\n{answers=}\n{closed_answers=}\n{current=}\n{correct=}\n{migration_state=}')
        else:
            answers = await get_value_from_redis(callback.user_id, 'open_answers')
            if not answers:
                answers = list()
            closed_answers = await get_value_from_redis(callback.user_id, 'closed_answers')
            if not closed_answers:
                closed_answers = list()
            current = await get_value_from_redis(callback.user_id, 'current_question')
            if not current:
                current = 0
            correct = await get_value_from_redis(callback.user_id, 'correct')
            migration_state = await get_value_from_redis(callback.user_id, 'migration_state')
            logger.info(f'Из redis_storage:\n{answers=}\n{closed_answers=}\n{current=}\n{correct=}\n{migration_state=}')
        
        
        call_answer = callback.payload
        if not call_answer:
            call_answer = await get_value_from_redis(callback.user_id, 'call_answer')
            user_answer = call_answer.split('::')[1] if "correct" not in call_answer else call_answer.split('::')[1].split("_")[0]
            closed_answers.append(user_answer)
            await save_cursor(callback.user_id, extra_data = dict(closed_answers = closed_answers, current_question=current + 1))
        logger.info(f"[INFO][final_process_answer_handler] {answers=}\n{current=}\n{call_answer=}")
        if all([call_answer, '::' in callback.payload, call_answer != 'change_department::in_process']):
            user_answer = call_answer.split('::')[1] if "correct" not in call_answer else call_answer.split('::')[1].split("_")[0]
            logger.info(f"[INFO][final_process_answer_handler] {user_answer=}\n{call_answer=}\n{correct=}")
            #answers.append(user_answer)
            closed_answers.append(user_answer)
            await save_cursor(callback.user_id, extra_data = dict(closed_answers = closed_answers))
            logger.info(f"[INFO][final_process_answer_handler] Сохраняем ответ пользователя и переходим к следующему вопросу")
            #data.update(open_answers=answers, current_question=current + 1)
            if data:
                data.update(closed_answers=closed_answers, current_question=current + 1)
                cursor.change_data(data)
            else:
                extra_data = await load_cursor(callback.user_id)
                extra_data.update(closed_answers=closed_answers, current_question=current + 1)
                await save_cursor(callback.user_id, extra_data = {**extra_data})
                cursor.change_data(extra_data)
            logger.info(f'[INFO][final_process_answer_handler] state={cursor.get_state()}')
            state_name = await get_value_from_redis(callback.user_id, 'state_name')
            logger.info(f'{state_name=}')
            if migration_state == 'step_12_testing':
                await send_question_step_12(callback, cursor, 'final_test')
            elif not migration_state and state_name == 'block1_questions_lawyer':
                await send_question_step_12(callback, cursor, 'final_test')
                return
            elif migration_state == 'block_2_final_testing':
                await send_question_step_12(callback, cursor, 'section_10')
                return
            elif migration_state == 'block_3_final_testing':
                await send_question_step_12(callback, cursor, 'section_17')
                return
            elif migration_state == 'block_4_final_testing':
                await send_question_step_12(callback, cursor, 'section_22')
                return
            elif migration_state == 'block_5_final_testing':
                await send_question_step_12(callback, cursor, 'section_39')
                return
            elif migration_state == 'block_6_final_testing':
                await send_question_step_12(callback, cursor, 'section_41')
                return
            elif migration_state == 'block_7_final_testing':
                await send_question_step_12(callback, cursor, 'section_42')
                return
            elif migration_state == 'module_0_final_testing':
                await send_question_step_12(callback, cursor, 'section_12')
                return
            elif migration_state == 'module_1_final_testing':
                await send_question_step_12(callback, cursor, 'section_25')
                return
            elif migration_state == 'module_2_final_testing':
                await send_question_step_12(callback, cursor, 'section_36')
                return
            elif migration_state == 'module_3_final_testing':
                await send_question_step_12(callback, cursor, 'section_47')
                return
            elif migration_state == 'module_4_final_testing':
                await send_question_step_12(callback, cursor, 'section_56')
                return
            elif migration_state == 'module_5_final_testing':
                await send_question_step_12(callback, cursor, 'section_65')
                return
            elif migration_state == 'module_6_final_testing':
                await send_question_step_12(callback, cursor, 'section_74')
                return
            elif migration_state == 'module_7_final_testing':
                await send_question_step_12(callback, cursor, 'section_83')
                return
        elif callback.payload == 'to_final_test':
            if migration_state == 'step_12_testing':
                await send_question_step_12(callback, cursor, 'final_test')
                return
            elif migration_state == 'block_2_final_testing':
                await send_question_step_12(callback, cursor, 'section_10')
                return
            elif migration_state == 'block_3_final_testing':
                await send_question_step_12(callback, cursor, 'section_17')
                return
            elif migration_state == 'block_4_final_testing':
                await send_question_step_12(callback, cursor, 'section_22')
                return
            elif migration_state == 'block_5_final_testing':
                await send_question_step_12(callback, cursor, 'section_39')
                return
            elif migration_state == 'block_6_final_testing':
                await send_question_step_12(callback, cursor, 'section_41')
                return
            elif migration_state == 'block_7_final_testing':
                await send_question_step_12(callback, cursor, 'section_42')
                return
            elif migration_state == 'module_0_final_testing':
                await send_question_step_12(callback, cursor, 'section_12')
                return
            elif migration_state == 'module_1_final_testing':
                await send_question_step_12(callback, cursor, 'section_25')
                return
            elif migration_state == 'module_2_final_testing':
                await send_question_step_12(callback, cursor, 'section_36')
                return
            elif migration_state == 'module_3_final_testing':
                await send_question_step_12(callback, cursor, 'section_47')
                return
            elif migration_state == 'module_4_final_testing':
                await send_question_step_12(callback, cursor, 'section_56')
                return
            elif migration_state == 'module_5_final_testing':
                await send_question_step_12(callback, cursor, 'section_65')
                return
            elif migration_state == 'module_6_final_testing':
                await send_question_step_12(callback, cursor, 'section_74')
                return
            elif migration_state == 'module_7_final_testing':
                await send_question_step_12(callback, cursor, 'section_83')
                return
     
    except Exception as e:
        logger.error(f"[ERROR][final_process_answer_handler] Произошла ошибка {e}")  


# ============================================================================
# БЛОК №3: Технология продаж: этапы, скрипты и работа с возражениями
# ============================================================================

# РАЗДЕЛ № 1 ------------------

@router.on_button_callback(state(TrainingStates.block_2_final_testing), lambda data: data.payload == "next_educ_to_part_2")
async def start_block_3_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Обработчик завершения обучения по 2 блоку и перехода к блоку № 3 при нажатии на кнопку ПРОДОЛЖИТЬ ОБУЧЕНИЕ"""
    try:
        logger.info(f'[INFO][start_block_3_handler] Стартовал')
        #cursor.change_state(TrainingStates.block3_section1_ready)
        cursor_redis_data = await load_cursor(callback.user_id)
        if 'state_name' in cursor_redis_data:
            del cursor_redis_data['state_name']
        if 'payload' in cursor_redis_data:
            del cursor_redis_data['payload']
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)  
        if continue_flag:
            intro_text = get_block3_intro_text()
            await callback.send(intro_text)
            await asyncio.sleep(2) # 10 
        
        await callback.message.delete()
        
        intro_text = get_block3_section_1_intro_text()  
        await callback.send(intro_text, disable_link_preview=True)
        
        await asyncio.sleep(2) # 15
        
        test_text = go_to_test_1_text(5)
        await callback.send(test_text, format="markdown", keyboard=start_test_kb())
        
        await save_cursor(callback.user_id, extra_data={**cursor_redis_data, 'state_name': TrainingStates.block_3_test_1_ready_for_test, 'payload': 'start_test'})
        cursor.change_state(TrainingStates.block_3_test_1_ready_for_test)
        
        
        # cursor.change_state(TrainingStates.block3_start)
        
        # if await debounce_button_max(callback, cursor):
        #     return
        
        # intro_text = get_block3_intro_text()
        
        # kb = next_to_educ_to_part_kb()
        # await callback.send(intro_text, format='markdown', disable_link_preview=True, keyboard=kb)
                       
        return
        
    except Exception as e:
        logger.error(f'[ERROR][start_block_2_handler] Произошла ошибка {e}')
    finally:
        await remove_repeat_flag(callback.user_id)  


# ============================================================================
# БЛОК №3 - РАЗДЕЛ №1: Воронка продаж: 8 этапов от лида до закрытия сделки
# ============================================================================


@router.on_button_callback(state(TrainingStates.block3_section1_ready), lambda data: data.payload == "next_educ_to_part_2")
async def go_to_block3_section1_handler(callback: Callback, cursor: FSMCursor):
    """Обработчик перехода к изучению раздела 1 блока 3"""
    try:
        logger.info(f'[INFO][go_to_block3_section1_handler] Стартовал')
        await callback.message.delete()
        
        intro_text = get_block3_section_1_intro_text()  
        await callback.send(intro_text, disable_link_preview=True)
        
        await asyncio.sleep(2) # 15
        
        test_text = go_to_test_1_text(5)
        await callback.send(test_text, format="markdown", keyboard=start_test_kb())
        
        await save_cursor(callback.user_id, extra_data={'state_name': TrainingStates.block_3_test_1_ready_for_test})
        cursor.change_state(TrainingStates.block_3_test_1_ready_for_test)
    
    except Exception as e:
        logger.error(f'[ERROR][go_to_block3_section1_handler] Произошла ошибка {e}')



@router.on_button_callback(state(TrainingStates.block_3_test_1_ready_for_test), lambda data: data.payload == "start_test")
async def training_block_3_test_1_handler(callback: Callback, cursor: FSMCursor):
    """БЛО№ № 3 Тест 1 - Начало тестирования"""
    try:
        logger.info("[INFO][training_block_3_test_1_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2) 
        questions = get_block_3_test_1_quests()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[training_block_3_test_1_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
            
        await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        logger.info(f'[training_block_3_test_1_handler] после добавления вопросов в state: {data=}')  
        cursor.change_data(data)
        # Отправляем первый вопрос
        await send_question(callback, cursor, 'section_8')
        await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.block_3_test_1_testing))
        cursor.change_state(TrainingStates.block_3_test_1_testing)
    
    except Exception as e:
        logger.error(f"[training_block_3_test_1_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 
        


# ============================================================================
# БЛОК №3 - РАЗДЕЛ №2: Работа с возражениями клиентов и конкуренты
# ============================================================================

@router.on_button_callback(state(TrainingStates.block_3_section_1_next), lambda data: data.payload.split('::')[1] == "not_first")
async def block_3_test_2_ready_for_test_handl(callback: Callback, cursor: FSMCursor):
    """БЛОК №3 - Раздел №2: Работа с возражениями клиентов и конкуренты"""
    try:
        logger.info('Стартовал')
        cursor_redis_data = await load_cursor(callback.user_id)
        if 'state_name' in cursor_redis_data:
            del cursor_redis_data['state_name']
        if 'payload' in cursor_redis_data:
            del cursor_redis_data['payload']
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2) 
        await callback.message.delete()
        intro_text = get_block3_section_2_intro_text()  
        await callback.send(intro_text, disable_link_preview=True)
        
        await asyncio.sleep(3) # 15
        
        test_text = go_to_test_1_text(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        await save_cursor(callback.user_id, extra_data={**cursor_redis_data, 'state_name': TrainingStates.block_3_test_2_ready_for_test, 'payload': 'start_test'})
        cursor.change_state(TrainingStates.block_3_test_2_ready_for_test)
        
        
    except Exception as e:
        logger.error(f"[ERROR][block_3_test_2_ready_for_test_handl] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)  
        

@router.on_button_callback(state(TrainingStates.block_3_test_2_ready_for_test), lambda data: data.payload == "start_test")
async def training_block_3_test_2_handler(callback: Callback, cursor: FSMCursor):
    """БЛО№ № 3 Тест 2 - Начало тестирования"""
    try:
        logger.info("[INFO][training_block_3_test_2_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2) 
        questions = get_block_3_test_2_quests()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[training_block_3_test_2_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
        
        await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))        
        logger.info(f'[training_block_3_test_2_handler] после добавления вопросов в state: ')  
        cursor.change_data(data)
        # Отправляем первый вопрос
        await send_question(callback, cursor, 'section_12')
        await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.block_3_test_2_testing))
        cursor.change_state(TrainingStates.block_3_test_2_testing)
    
    except Exception as e:
        logger.error(f"[training_block_3_test_2_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 



# ============================================================================
# БЛОК №3 - РАЗДЕЛ №3: Скрипты диалогов: как правильно начать разговор с клиентом
# ============================================================================

@router.on_button_callback(state(TrainingStates.block_3_section_2_next), lambda data: data.payload.split('::')[1] == "not_first")
async def block_3_test_3_ready_for_test_handl(callback: Callback, cursor: FSMCursor):
    """БЛОК №2 - Раздел №3: Скрипты диалогов: как правильно начать разговор с клиентом"""
    try:
        cursor_redis_data = await load_cursor(callback.user_id)
        if 'state_name' in cursor_redis_data:
            del cursor_redis_data['state_name']
        if 'payload' in cursor_redis_data:
            del cursor_redis_data['payload']
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2) 
        await callback.message.delete()
        intro_text = get_block3_section_3_intro_text()  
        await callback.send(intro_text, disable_link_preview=True)
        
        await asyncio.sleep(2) # 215
        
        test_text = go_to_test_1_text(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        await save_cursor(callback.user_id, extra_data={**cursor_redis_data, 'state_name': TrainingStates.block_3_test_3_ready_for_test, 'payload': 'start_test'})
        cursor.change_state(TrainingStates.block_3_test_3_ready_for_test)
        
        
    except Exception as e:
        logger.error(f"[ERROR][block_3_test_2_ready_for_test_handl] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)  


@router.on_button_callback(state(TrainingStates.block_3_test_3_ready_for_test), lambda data: data.payload == "start_test")
async def training_block_3_test_3_handler(callback: Callback, cursor: FSMCursor):
    """БЛО№ № 3 Тест 3 - Начало тестирования"""
    try:
        logger.info("[INFO][training_block_3_test_3_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2) 
        questions = get_block_3_test_3_quests()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[training_block_3_test_3_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
            
        logger.info(f'[training_block_3_test_3_handler] после добавления вопросов в state: {data=}')  
        cursor.change_data(data)
        # Отправляем первый вопрос
        await send_question(callback, cursor, 'section_13')
        await save_cursor(callback.user_id, extra_data={'state_name': TrainingStates.block_3_test_3_testing})
        cursor.change_state(TrainingStates.block_3_test_3_testing)
    
    except Exception as e:
        logger.error(f"[training_block_3_test_3_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)  

# ============================================================================
# БЛОК №3 - РАЗДЕЛ №4: Психотипы клиентов: как адаптировать стиль общения
# ============================================================================

@router.on_button_callback(state(TrainingStates.block_3_section_3_next), lambda data: data.payload.split('::')[1] == "not_first")
async def block_3_test_4_ready_for_test_handl(callback: Callback, cursor: FSMCursor):
    """БЛОК №3 - Раздел №4: Психотипы клиентов: как адаптировать стиль общения"""
    try:
        cursor_redis_data = await load_cursor(callback.user_id)
        if 'state_name' in cursor_redis_data:
            del cursor_redis_data['state_name']
        if 'payload' in cursor_redis_data:
            del cursor_redis_data['payload']
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2) 
        await callback.message.delete()
        intro_text = get_block3_section_4_intro_text()  
        await callback.send(intro_text, disable_link_preview=True)
        
        await asyncio.sleep(2) # 15
        
        test_text = go_to_test_1_text(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        await save_cursor(callback.user_id, extra_data={**cursor_redis_data, 'state_name': TrainingStates.block_3_test_4_ready_for_test, 'payload': 'start_test'})
        cursor.change_state(TrainingStates.block_3_test_4_ready_for_test)
        
        
    except Exception as e:
        logger.error(f"[ERROR][block_3_test_2_ready_for_test_handl] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)  


@router.on_button_callback(state(TrainingStates.block_3_test_4_ready_for_test), lambda data: data.payload == "start_test")
async def training_block_3_test_4_handler(callback: Callback, cursor: FSMCursor):
    """БЛО№ № 3 Тест 4 - Начало тестирования"""
    try:
        logger.info("[INFO][training_block_3_test_4_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2) 
        questions = get_block_3_test_4_quests()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[training_block_3_test_4_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
            
        await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))    
        logger.info(f'[training_block_3_test_4_handler] после добавления вопросов в state: {data=}')  
        cursor.change_data(data)
        # Отправляем первый вопрос
        await send_question(callback, cursor, 'section_14')
        await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.block_3_test_4_testing))
        cursor.change_state(TrainingStates.block_3_test_4_testing)
    
    except Exception as e:
        logger.error(f"[training_block_3_test_3_handler] Произошла ошибка {e}")
    finally:
            await remove_repeat_flag(callback.user_id)  
        
        
# ============================================================================
# БЛОК №3 - РАЗДЕЛ №5: Шпаргалка менеджера: продукты, проблемы, решения
# ============================================================================

@router.on_button_callback(state(TrainingStates.block_3_section_4_next), lambda data: data.payload.split('::')[1] == "not_first")
async def block_3_test_5_ready_for_test_handl(callback: Callback, cursor: FSMCursor):
    """БЛОК №3 - Раздел №5: Шпаргалка менеджера: продукты, проблемы, решения"""
    try:
        
        cursor_redis_data = await load_cursor(callback.user_id)
        if 'state_name' in cursor_redis_data:
            del cursor_redis_data['state_name']
        if 'payload' in cursor_redis_data:
            del cursor_redis_data['payload']
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2) 
        await callback.message.delete()
        intro_text = get_block3_section_5_intro_text()  
        await callback.send(intro_text, disable_link_preview=True)
        
        await asyncio.sleep(2) # 15
        
        test_text = go_to_test_1_text(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        await save_cursor(callback.user_id, extra_data={**cursor_redis_data, 'state_name': TrainingStates.block_3_test_5_ready_for_test, 'payload': 'start_test'})
        cursor.change_state(TrainingStates.block_3_test_5_ready_for_test)
        
        
    except Exception as e:
        logger.error(f"[ERROR][block_3_test_5_ready_for_test_handl] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)    
        

@router.on_button_callback(state(TrainingStates.block_3_test_5_ready_for_test), lambda data: data.payload == "start_test")
async def training_block_3_test_5_handler(callback: Callback, cursor: FSMCursor):
    """БЛО№ № 3 Тест 5 - Начало тестирования"""
    try:
        logger.info("[INFO][training_block_3_test_5_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2) 
        questions = get_block_3_test_5_quests()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[training_block_3_test_5_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
            
        await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))    
        logger.info(f'[training_block_3_test_5_handler] после добавления вопросов в state: {data=}')  
        cursor.change_data(data)
        # Отправляем первый вопрос
        await send_question(callback, cursor, 'section_15')
        await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.block_3_test_5_testing))
        cursor.change_state(TrainingStates.block_3_test_5_testing)
    
    except Exception as e:
        logger.error(f"[training_block_3_test_5_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)            
        

# ============================================================================
# БЛОК №3 - РАЗДЕЛ №6: Простой алгоритм работы для менеджера-стажёра
# ============================================================================

@router.on_button_callback(state(TrainingStates.block_3_section_5_next), lambda data: data.payload.split('::')[1] == "not_first")
async def block_3_test_6_ready_for_test_handl(callback: Callback, cursor: FSMCursor):
    """БЛОК №3 - Раздел №6: Простой алгоритм работы для менеджера-стажёра"""
    try:
        cursor_redis_data = await load_cursor(callback.user_id)
        if 'state_name' in cursor_redis_data:
            del cursor_redis_data['state_name']
        if 'payload' in cursor_redis_data:
            del cursor_redis_data['payload']
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2) 
        await callback.message.delete()
        intro_text = get_block3_section_6_intro_text()  
        await callback.send(intro_text, disable_link_preview=True)
        
        await asyncio.sleep(2) # 15
        
        test_text = go_to_test_1_text(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        await save_cursor(callback.user_id, extra_data={**cursor_redis_data, 'state_name': TrainingStates.block_3_test_6_ready_for_test, 'payload': 'start_test'})
        cursor.change_state(TrainingStates.block_3_test_6_ready_for_test)
        
        
    except Exception as e:
        logger.error(f"[ERROR][block_3_test_6_ready_for_test_handl] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)        
        

@router.on_button_callback(state(TrainingStates.block_3_test_6_ready_for_test), lambda data: data.payload == "start_test")
async def training_block_3_test_6_handler(callback: Callback, cursor: FSMCursor):
    """БЛО№ № 3 Тест 6 - Начало тестирования"""
    try:
        logger.info("[INFO][training_block_3_test_6_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2) 
        questions = get_block_3_test_6_quests()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[training_block_3_test_6_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
        
        await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))        
        logger.info(f'[training_block_3_test_6_handler] после добавления вопросов в state: {data=}')  
        cursor.change_data(data)
        # Отправляем первый вопрос
        await send_question(callback, cursor, 'section_17')
        await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.block_3_test_6_testing))
        cursor.change_state(TrainingStates.block_3_test_6_testing)
    
    except Exception as e:
        logger.error(f"[training_block_3_test_6_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)    
               

        
@router.on_button_callback(state(TrainingStates.block3_final_test), lambda data: data.payload.split('::')[1] == "not_first")
async def continue_after_section17_handler(callback: Callback, cursor: FSMCursor):
    """Завершение Блока №3 - Продукт. Переход к вопросам или финальному тесту"""
    try:
        logger.info(f"[continue_after_section17_handler] Стартовал")
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)    
        await callback.message.delete()
        # Проверяем загрузку базы знаний
        rag = RAGService()
        stats = rag.get_stats()
        
        if not stats['is_loaded']:
            await callback.send(
                "❌ База знаний не загружена. Обратитесь к администратору.",
                keyboard=main_menu_keyboard(current_course)
            )
            cursor.clear()
            return
        
        text = get_text_to_final_test_block_3()
        
        await callback.send(text, keyboard=final_start_test_kb())
        cursor.change_state(TrainingStates.block3_questions)
        await save_cursor(callback.user_id, extra_data = {'payload': 'to_final_test', 'state_name': TrainingStates.block3_questions, 'current_course': current_course})
    
    except Exception as e:
        logger.error(f"[continue_after_section17_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)  


@router.on_button_callback(state(TrainingStates.block3_final_test), lambda data: data.payload == "next_educ_to_part_2")
async def continue_after_block3_handler(callback: Callback, cursor: FSMCursor):
    """Завершение Блока №3. Переход к вопросам или финальному тесту"""
    try:
        logger.info(f"[continue_after_block3_handler] Стартовал")
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)    
        # Проверяем загрузку базы знаний
        rag = RAGService()
        stats = rag.get_stats()
        
        if not stats['is_loaded']:
            await callback.send(
                "❌ База знаний не загружена. Обратитесь к администратору.",
                keyboard=main_menu_keyboard(current_course)
            )
            cursor.clear()
            return
        
        text = get_text_to_final_test_block_3()
        
        await callback.send(text)
        #await callback.send(text, keyboard=final_start_test_kb())
        cursor.change_state(TrainingStates.block3_questions)
        await save_cursor(callback.user_id, extra_data = {'payload': 'to_final_test', 'state_name': TrainingStates.block3_questions, 'current_course': current_course})
        
        # await asyncio.sleep(5)
        # await start_block3_final_test_handler(callback, cursor)
        return
        
    
    except Exception as e:
        logger.error(f"[continue_after_block3_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 

        

@router.on_button_callback(state(TrainingStates.block3_questions), lambda data: data.payload == 'to_final_test')
async def start_block3_final_test_handler(callback: Callback, cursor: FSMCursor):
    """Переход к финальному тесту по Блоку №3"""
    try:
        logger.info(f"[INFO][start_block3_final_test_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)    
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        text = get_text_start_final_test_block_3()
        
        data = cursor.get_data()
        if not data:
            data = dict()
            status_user = await get_value_from_redis(callback.user_id, 'status_user')
            if not status_user:
                status_user = 'new_employer'
        else:
            status_user = data.get('status_user', 'new_employer')

        logger.info(f'{current_course=} {status_user=}')
        data.update(current_question=0, current_course=current_course, status_user=status_user)
        data.update(payload = 'start_final_test')
        cursor.change_data(data)
        await callback.send(text, keyboard=final_test_kb())
        cursor.change_state(TrainingStates.block_3_final_testing)
        await save_cursor(callback.user_id, extra_data = {**data, 'state_name': TrainingStates.block_3_final_testing, 'payload': 'start_final_test'})
           
    
    except Exception as e:
        logger.error(f"[ERROR][start_block23_final_test_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)


@router.on_message(state(TrainingStates.lawyer['block3_questions']))
@router.on_message(state(TrainingStates.block3_questions))
async def answer_block3_question_handler(message: Message, cursor: FSMCursor, state_name: str = None):
    """Ответы на вопросы по Блоку 3 через RAG + Claude"""
    try:
        logger.info(f"[INFO][answer_block3_question_handler] Стартовал")
        cursor_redis_data = await load_cursor(message.user_id)
        del cursor_redis_data['state_name']
        await save_cursor(message.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)    
        # Показываем процесс
        thinking_msg = await message.send("🔍 Ищу информацию в базе знаний...")
        
        if not state_name:
        
            state = cursor.get_state() # изменил 12.07.26 !!!!!
            state_name = state.state if all([state, not isinstance(state, str)]) else state
            logger.info(f'Из курсора: {state_name=}')        
               
        if state_name in ['block1_questions_lawyer', 'block2_questions_lawyer', 'block3_questions_lawyer',
                          'block4_questions_lawyer']:
            logger.info('Создаем RAG для ветки ЮРИСТ')
            rag = RAGService(branch_name = 'lawyer')
        else:
            rag = RAGService()
        
        answer = await rag.answer_question(message.body.text)
        
        await thinking_msg.delete() 
        
        # Форматируем ответ
        logger.info(f"[INFO][answer_block3_question_handler] Форматируем ответ") 
        response_text = (
            f"💡 **Ответ по Блоку №3:**\n\n"
            f"{answer}\n\n"
            "➡️ Задайте следующий вопрос или нажмите 📝 **Перейти к тестированию**"
        )
        
        await message.send(response_text, keyboard=final_start_test_kb(), format='markdown')
        
        cursor.change_state(state_name)
        await save_cursor(message.user_id, extra_data = {**cursor_redis_data, 'state_name': state_name})
    
    except Exception as e:
        await thinking_msg.delete()
        logger.error(f"[ERROR][answer_block3_question_handler] Произошла ошибка {e}")   

        await message.send(
            "❌ Произошла ошибка при обработке вопроса.\n\n"
            "Попробуйте задать вопрос ещё раз или обратитесь к администратору.",
            keyboard=final_start_test_kb()
        )
    finally:
        await remove_repeat_flag(message.user_id) 

        

@router.on_message(state(TrainingStates.block_3_final_testing))
async def block3_final_testing_handler(message: Message, cursor: FSMCursor):
    """Обработка ответов на открытые вопросы по Блоку 3 в финальном тесте через RAG + Claude"""
    try:
        logger.info(f"[INFO][block3_final_testing_handler] Стартовал")   
         
        await asyncio.sleep(2)
        await send_question_step_12(message, cursor, 'section_17')
        return 
        
    except Exception as e:
        #await thinking_msg.delete()
        logger.error(f"[ERROR][block3_final_testing_handler] Произошла ошибка {e}")   

        await message.send(
            "❌ Произошла ошибка при обработке вопроса.\n\n"
            "Попробуйте набрать свой ответ ещё раз или обратитесь к администратору.",
            keyboard=final_start_test_kb())
             
# ============================================================================
# ШАГ № __: ФИНАЛЬНОЕ ТЕСТИРОВАНИЕ ПО БЛОКУ № 3 (10 закрытых + 5 открытых)
# ============================================================================


@router.on_button_callback(state(TrainingStates.block_3_final_testing), lambda data: data.payload == 'start_final_test')
async def start_testing_block3_handler(callback: Callback, cursor: FSMCursor):
    """ШАГ № __ - Запуск финального тестирования по Блоку 3"""
    try:
        logger.info(f"[INFO][start_testing_block3_handler] Стартовал")
        await del_value_from_redis(callback.user_id, 'payload')
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        # ЧАСТЬ 1: Закрытые вопросы (10 вопросов с вариантами A/B/C/D)
        closed_questions = get_final_test_block_3('close')
        
        # ЧАСТЬ 2: Открытые вопросы (5 вопросов с эталонными ответами)
        open_questions = get_final_test_block_3('open')
        
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        logger.info(f'{current_course=}')
        
        data = cursor.get_data()
        logger.info(f'[start_testing_block3_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(
                closed_questions=closed_questions,
                open_questions=open_questions,
                current_question=0,
                closed_answers=[],  # Ответы на закрытые вопросы
                open_answers=[],    # Ответы на открытые вопросы
                test_stage="closed",  # Начинаем с закрытых вопросов
                migration_state = "block_3_final_testing",
                current_course = current_course
                )
            await save_cursor(callback.user_id, extra_data = dict(
                closed_questions=closed_questions,
                open_questions=open_questions,
                current_question=0,
                closed_answers=[],  # Ответы на закрытые вопросы
                open_answers=[],    # Ответы на открытые вопросы
                test_stage="closed",  # Начинаем с закрытых вопросов
                migration_state = "block_3_final_testing",
                current_course = current_course  
            ))
        else:
            data = dict()
            data.update(
                closed_questions=closed_questions,
                open_questions=open_questions,
                current_question=0,
                closed_answers=[],  # Ответы на закрытые вопросы
                open_answers=[],    # Ответы на открытые вопросы
                test_stage="closed",  # Начинаем с закрытых вопросов
                migration_state = "block_3_final_testing",
                current_course = current_course
                )
            await save_cursor(callback.user_id, extra_data = dict(
                closed_questions=closed_questions,
                open_questions=open_questions,
                current_question=0,
                closed_answers=[],  # Ответы на закрытые вопросы
                open_answers=[],    # Ответы на открытые вопросы
                test_stage="closed",  # Начинаем с закрытых вопросов
                migration_state = "block_3_final_testing",
                current_course = current_course  
            ))
            
        logger.info(f'[start_testing_block3_handler] после добавления вопросов в state: {data=}')  
        cursor.change_data(data)  # !!!!!!!!!!
        # Отправляем первый закрытый вопрос
        logger.info(f'[start_testing_block3_handler] Отправляем первый закрытый вопрос')
        await send_question_step_12(callback, cursor, "section_17")

        #cursor.change_state(TrainingStates.block_3_final_testing)
        await save_cursor(callback.user_id, extra_data = {'final_block_3_flag': True, 'state_name': TrainingStates.block_3_final_testing, 'payload': 'start_final_test'})
        

    except Exception as e:
        logger.error(f"[ERROR][start_testing_block3_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)  
        

# ============================================================================
# БЛОК №4: Технология продаж: этапы, скрипты и работа с возражениями - 
# РАЗДЕЛ №1: Теория по расчёту стоимости противопожарного стекла и стеклопакета
# ============================================================================

@router.on_button_callback(state(TrainingStates.block_3_final_testing), lambda data: data.payload == "next_educ_to_part_2")
async def start_block_4_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Обработчик завершения обучения по 3 блоку и перехода к блоку № 4 при нажатии на кнопку ПРОДОЛЖИТЬ ОБУЧЕНИЕ"""
    try:
        logger.info(f'[INFO][start_block_4_handler] Стартовал')
        cursor_redis_data = await load_cursor(callback.user_id)
        if 'state_name' in cursor_redis_data:
            del cursor_redis_data['state_name']
        if 'payload' in cursor_redis_data:
            del cursor_redis_data['payload']
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
          
        #cursor.change_state(TrainingStates.block3_section1_ready)
        if continue_flag:
            intro_text = get_block4_intro_text()
            await callback.send(intro_text)
            await asyncio.sleep(2) # 10 
        
        await callback.message.delete()
        
        intro_text = get_block4_section_1_intro_text()  
        await callback.send(intro_text, disable_link_preview=True)
        
        await asyncio.sleep(2) # 15
        
        test_text = go_to_test_1_text(10)
        await callback.send(test_text, format="markdown", keyboard=start_test_kb())
        
        await save_cursor(callback.user_id, extra_data={**cursor_redis_data, 'state_name': TrainingStates.block4_section1_ready, 'payload': 'start_test'})
        cursor.change_state(TrainingStates.block4_section1_ready)
               
        return
        
    except Exception as e:
        logger.error(f'[ERROR][start_block_4_handler] Произошла ошибка {e}')
    finally:
        await remove_repeat_flag(callback.user_id) 



@router.on_button_callback(state(TrainingStates.block4_section1_ready), lambda data: data.payload == "next_educ_to_part_2")
async def go_to_block4_section1_handler(callback: Callback, cursor: FSMCursor):
    """Обработчик перехода к изучению раздела 1 блока 4"""
    try:
        logger.info(f'[INFO][go_to_block4_section1_handler] Стартовал')
        cursor_redis_data = await load_cursor(callback.user_id)
        if 'state_name' in cursor_redis_data:
            del cursor_redis_data['state_name']
        if 'payload' in cursor_redis_data:
            del cursor_redis_data['payload']
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2) 
        await callback.message.delete()
        intro_text = get_block4_section_1_intro_text()  
        await callback.send(intro_text, disable_link_preview=True)
        
        await asyncio.sleep(2) # 15
        
        test_text = go_to_test_1_text(10)
        await callback.send(test_text, format="markdown", keyboard=start_test_kb())
        
        await save_cursor(callback.user_id, extra_data={**cursor_redis_data, 'state_name': TrainingStates.block_4_test_1_ready_for_test, 'payload': 'start_test'})
        cursor.change_state(TrainingStates.block_4_test_1_ready_for_test)
    
    except Exception as e:
        logger.error(f'[ERROR][go_to_block4_section1_handler] Произошла ошибка {e}')
    finally:
        await remove_repeat_flag(callback.user_id)  


@router.on_button_callback(state(TrainingStates.block_4_test_1_ready_for_test), lambda data: data.payload == "start_test")
async def training_block_4_test_1_handler(callback: Callback, cursor: FSMCursor):
    """БЛО№ № 4 Тест 1 - Начало тестирования"""
    try:
        logger.info("[INFO][training_block_4_test_1_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2) 
        questions = get_block_4_test_1_quests()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[training_block_4_test_1_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
        await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))        
        logger.info(f'[training_block_4_test_1_handler] после добавления вопросов в state: {data=}')  
        cursor.change_data(data)
        # Отправляем первый вопрос
        await send_question(callback, cursor, 'section_18')
        await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.block_4_test_1_testing))
        cursor.change_state(TrainingStates.block_4_test_1_testing)
    
    
    except Exception as e:
        logger.error(f"[training_block_4_test_1_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)


# ============================================================================
# БЛОК №4 - РАЗДЕЛ №2: Методичка по расчёту стоимости противопожарного стекла
# ============================================================================

@router.on_button_callback(state(TrainingStates.block_4_section_1_next), lambda data: data.payload.split('::')[1] == "not_first")
async def block_4_test_2_ready_for_test_handl(callback: Callback, cursor: FSMCursor):
    """БЛОК №4 - Раздел №2: Методичка по расчёту стоимости противопожарного стекла/стеклопакета"""
    try:
        cursor_redis_data = await load_cursor(callback.user_id)
        if 'state_name' in cursor_redis_data:
            del cursor_redis_data['state_name']
        if 'payload' in cursor_redis_data:
            del cursor_redis_data['payload']
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        await callback.message.delete()
        intro_text = get_block4_section_2_intro_text()  
        await callback.send(intro_text, disable_link_preview=True)
        
        await asyncio.sleep(2) # 15
        
        test_text = go_to_test_1_text(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        await save_cursor(callback.user_id, extra_data={**cursor_redis_data, 'state_name': TrainingStates.block_4_test_2_ready_for_test, 'payload': 'start_test'})
        cursor.change_state(TrainingStates.block_4_test_2_ready_for_test)
        
        
    except Exception as e:
        logger.error(f"[ERROR][block_4_test_2_ready_for_test_handl] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 
        

@router.on_button_callback(state(TrainingStates.block_4_test_2_ready_for_test), lambda data: data.payload == "start_test")
async def training_block_4_test_2_handler(callback: Callback, cursor: FSMCursor):
    """БЛО№ № 4 Тест 2 - Начало тестирования"""
    try:
        logger.info("[INFO][training_block_4_test_2_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2) 
        questions = get_block_4_test_2_quests()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[training_block_4_test_2_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
        await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))            
        logger.info(f'[training_block_4_test_2_handler] после добавления вопросов в state: {data=}')  
        cursor.change_data(data)
        # Отправляем первый вопрос
        await send_question(callback, cursor, 'section_19')
        await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.block_4_test_2_testing))
        cursor.change_state(TrainingStates.block_4_test_2_testing)
    
    except Exception as e:
        logger.error(f"[training_block_4_test_2_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)

# ============================================================================
# БЛОК №4 - РАЗДЕЛ №3: Инструкция по заполнению примечаний к работам для распределения стоимости
# ============================================================================

@router.on_button_callback(state(TrainingStates.block_4_section_2_next), lambda data: data.payload.split('::')[1] == "not_first")
async def block_4_test_3_ready_for_test_handl(callback: Callback, cursor: FSMCursor):
    """БЛОК №4 - Раздел №3: Инструкция по заполнению примечаний к работам для распределения стоимости"""
    try:
        cursor_redis_data = await load_cursor(callback.user_id)
        if 'state_name' in cursor_redis_data:
            del cursor_redis_data['state_name']
        if 'payload' in cursor_redis_data:
            del cursor_redis_data['payload']
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        await callback.message.delete()
        intro_text = get_block4_section_3_intro_text()  
        await callback.send(intro_text, disable_link_preview=True)
        
        await asyncio.sleep(2) # 15
        
        test_text = go_to_test_1_text(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        await save_cursor(callback.user_id, extra_data={**cursor_redis_data, 'state_name': TrainingStates.block_4_test_3_ready_for_test, 'payload': 'start_test'})
        cursor.change_state(TrainingStates.block_4_test_3_ready_for_test)
        
        
    except Exception as e:
        logger.error(f"[ERROR][block_4_test_2_ready_for_test_handl] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)  


@router.on_button_callback(state(TrainingStates.block_4_test_3_ready_for_test), lambda data: data.payload == "start_test")
async def training_block_4_test_3_handler(callback: Callback, cursor: FSMCursor):
    """БЛО№ № 4 Тест 3 - Начало тестирования"""
    try:
        logger.info("[INFO][training_block_4_test_3_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2) 
        questions = get_block_4_test_3_quests()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[training_block_4_test_3_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
        await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))                
        logger.info(f'[training_block_4_test_3_handler] после добавления вопросов в state: {data=}')  
        cursor.change_data(data)
        # Отправляем первый вопрос
        await send_question(callback, cursor, 'section_20')
        await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.block_4_test_3_testing))
        cursor.change_state(TrainingStates.block_4_test_3_testing)
    
    except Exception as e:
        logger.error(f"[training_block_4_test_3_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)
        

'5. ООО "Альфа-Крас" — Производство малярных работ'   
# ============================================================================
# БЛОК №4 - РАЗДЕЛ №4: Быстрый расчёт: ИИ-Агент
# ============================================================================

@router.on_button_callback(state(TrainingStates.block_4_section_3_next), lambda data: data.payload.split('::')[1] == "not_first")
async def block_4_test_4_ready_for_test_handl(callback: Callback, cursor: FSMCursor):
    """БЛОК №4 - Раздел №4: Быстрый расчёт: ИИ-Агент"""
    try:
        cursor_redis_data = await load_cursor(callback.user_id)
        if 'state_name' in cursor_redis_data:
            del cursor_redis_data['state_name']
        if 'payload' in cursor_redis_data:
            del cursor_redis_data['payload']
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        await callback.message.delete()
        intro_text = get_block4_section_4_intro_text()  
        await callback.send(intro_text, disable_link_preview=True)
        
        await asyncio.sleep(2) # 15
        
        test_text = go_to_test_1_text(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        await save_cursor(callback.user_id, extra_data={**cursor_redis_data, 'state_name': TrainingStates.block_4_test_4_ready_for_test, 'payload': 'start_test'})
        cursor.change_state(TrainingStates.block_4_test_4_ready_for_test)
        
        
    except Exception as e:
        logger.error(f"[ERROR][block_4_test_4_ready_for_test_handl] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)

        
@router.on_button_callback(state(TrainingStates.block_4_test_4_ready_for_test), lambda data: data.payload == "start_test")
async def training_block_4_test_4_handler(callback: Callback, cursor: FSMCursor):
    """БЛО№ № 4 Тест 4 - Начало тестирования"""
    try:
        logger.info("[INFO][training_block_4_test_4_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2) 
        questions = get_block_4_test_4_quests()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[training_block_4_test_4_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
        await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))                    
        logger.info(f'[training_block_4_test_4_handler] после добавления вопросов в state: {data=}')  
        cursor.change_data(data)
        # Отправляем первый вопрос
        await send_question(callback, cursor, 'section_21')  
        await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.block_4_test_4_testing))
        cursor.change_state(TrainingStates.block_4_test_4_testing)
    
    except Exception as e:
        logger.error(f"[training_block_4_test_4_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)


@router.on_button_callback(state(TrainingStates.block4_final_test), lambda data: data.payload.split('::')[1] == "not_first")
async def continue_after_section21_handler(callback: Callback, cursor: FSMCursor):
    """Завершение Блока №4. Переход к вопросам или финальному тесту"""
    try:
        logger.info(f"[continue_after_section21_handler] Стартовал")
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)  
        await callback.message.delete()
        # Проверяем загрузку базы знаний
        rag = RAGService()
        stats = rag.get_stats()
        
        if not stats['is_loaded']:
            await callback.send(
                "❌ База знаний не загружена. Обратитесь к администратору.",
                keyboard=main_menu_keyboard(current_course)
            )
            cursor.clear()
            return
        
        text = get_text_to_final_test_block_4()
        
        await callback.send(text, keyboard=final_start_test_kb())
        cursor.change_state(TrainingStates.block4_questions)
        await save_cursor(callback.user_id, extra_data = {'payload': 'to_final_test', 'state_name': TrainingStates.block3_questions, 'current_course': current_course})
    
    except Exception as e:
        logger.error(f"[continue_after_section21_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)         



@router.on_button_callback(state(TrainingStates.block4_final_test), lambda data: data.payload == "next_educ_to_part_2")
async def continue_after_block4_handler(callback: Callback, cursor: FSMCursor):
    """Завершение Блока №4. Переход к вопросам или финальному тесту"""
    try:
        logger.info(f"[continue_after_block4_handler] Стартовал")
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)    
        
        # Проверяем загрузку базы знаний
        rag = RAGService()
        stats = rag.get_stats()
        
        if not stats['is_loaded']:
            await callback.send(
                "❌ База знаний не загружена. Обратитесь к администратору.",
                keyboard=main_menu_keyboard(current_course)
            )
            cursor.clear()
            return
        
        text = get_text_to_final_test_block_4()
        
        await callback.send(text)
        #await callback.send(text, keyboard=final_start_test_kb())
        cursor.change_state(TrainingStates.block4_questions)
        await save_cursor(callback.user_id, extra_data = {'payload': 'to_final_test', 'state_name': TrainingStates.block4_questions, 'current_course': current_course})
        
        # await asyncio.sleep(2)
        # await start_block4_final_test_handler(callback, cursor)
        return
        
    
    except Exception as e:
        logger.error(f"[continue_after_block4_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)  
        
        
@router.on_button_callback(state(TrainingStates.block4_questions), lambda data: data.payload == 'to_final_test')
async def start_block4_final_test_handler(callback: Callback, cursor: FSMCursor):
    """Переход к финальному тесту по Блоку №4"""
    try:
        logger.info(f"[INFO][start_block4_final_test_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)    
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        text = get_text_start_final_test_block_4()
        
        data = cursor.get_data()
        if not data:
            data = dict()
            status_user = await get_value_from_redis(callback.user_id, 'status_user')
            if not status_user:
                status_user = 'new_employer'
        else:
            status_user = data.get('status_user', 'new_employer')
        data.update(current_question=0, current_course=current_course, status_user=status_user)
        data.update(payload = 'start_final_test')
        cursor.change_data(data)
        await callback.send(text, keyboard=final_test_kb())
        cursor.change_state(TrainingStates.block_4_final_testing)
        await save_cursor(callback.user_id, extra_data = {**data, 'state_name': TrainingStates.block_4_final_testing, 'payload': 'start_final_test'})
           
    
    except Exception as e:
        logger.error(f"[ERROR][start_block4_final_test_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)


@router.on_message(state(TrainingStates.lawyer['block4_questions']))
@router.on_message(state(TrainingStates.block4_questions))
async def answer_block4_question_handler(message: Message, cursor: FSMCursor, state_name: str = None):
    """Ответы на вопросы по Блоку 4 через RAG + Claude"""
    try:
        logger.info(f"[INFO][answer_block4_question_handler] Стартовал")
        cursor_redis_data = await load_cursor(message.user_id)
        del cursor_redis_data['state_name']
        await save_cursor(message.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)    
        # Показываем процесс
        thinking_msg = await message.send("🔍 Ищу информацию в базе знаний...")
        
        if not state_name:
            state = cursor.get_state() # изменил 12.07.26 !!!!!
            state_name = state.state if all([state, not isinstance(state, str)]) else state
            logger.info(f'Из курсора: {state_name=}')
        else:
            logger.info(f'Из аргумента обработчика:{state_name=}')
        
        if state_name in ['block1_questions_lawyer', 'block2_questions_lawyer', 'block3_questions_lawyer',
                          'block4_questions_lawyer']:
            rag = RAGService(branch_name = 'lawyer')
        else:
            rag = RAGService()
        
        answer = await rag.answer_question(message.body.text)
        
        await thinking_msg.delete() 
        
        # Форматируем ответ
        logger.info(f"[INFO][answer_block4_question_handler] Форматируем ответ") 
        response_text = (
            f"💡 **Ответ по Блоку №4:**\n\n"
            f"{answer}\n\n"
            "➡️ Задайте следующий вопрос или нажмите 📝 **Перейти к тестированию**"
        )
        
        await message.send(response_text, keyboard=final_start_test_kb(), format='markdown')
        cursor.change_state(state_name)
        await save_cursor(message.user_id, extra_data = {**cursor_redis_data, 'state_name': state_name})
    
    except Exception as e:
        await thinking_msg.delete()
        logger.error(f"[ERROR][answer_block4_question_handler] Произошла ошибка {e}")   

        await message.send(
            "❌ Произошла ошибка при обработке вопроса.\n\n"
            "Попробуйте задать вопрос ещё раз или обратитесь к администратору.",
            keyboard=final_start_test_kb()
        )
    finally:
        await remove_repeat_flag(message.user_id) 

       
@router.on_message(state(TrainingStates.block_4_final_testing))
async def block4_final_testing_handler(message: Message, cursor: FSMCursor):
    """Обработка ответов на открытые вопросы по Блоку 4 в финальном тесте через RAG + Claude"""
    try:
        logger.info(f"[INFO][block4_final_testing_handler] Стартовал")   
        
        await asyncio.sleep(2)
        await send_question_step_12(message, cursor, 'section_22')
        return
        
    except Exception as e:
        #await thinking_msg.delete()
        logger.error(f"[ERROR][block4_final_testing_handler] Произошла ошибка {e}")   

        await message.send(
            "❌ Произошла ошибка при обработке вопроса.\n\n"
            "Попробуйте набрать свой ответ ещё раз или обратитесь к администратору.",
            keyboard=final_start_test_kb())
        

# ============================================================================
# ШАГ № __: ФИНАЛЬНОЕ ТЕСТИРОВАНИЕ ПО БЛОКУ № 4 (10 закрытых + 5 открытых)
# ============================================================================


@router.on_button_callback(state(TrainingStates.block_4_final_testing), lambda data: data.payload == 'start_final_test')
async def start_testing_block4_handler(callback: Callback, cursor: FSMCursor):
    """ШАГ № __ - Запуск финального тестирования по Блоку 4"""
    try:
        logger.info(f"[INFO][start_testing_block4_handler] Стартовал")
        await del_value_from_redis(callback.user_id, 'payload')
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        # ЧАСТЬ 1: Закрытые вопросы (10 вопросов с вариантами A/B/C/D)
        closed_questions = get_final_test_block_4('close')
        
        # ЧАСТЬ 2: Открытые вопросы (5 вопросов с эталонными ответами)
        open_questions = get_final_test_block_4('open')
        
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        logger.info(f'{current_course=}')
        
        data = cursor.get_data()
        logger.info(f'[start_testing_block4_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(
                closed_questions=closed_questions,
                open_questions=open_questions,
                current_question=0,
                closed_answers=[],  # Ответы на закрытые вопросы
                open_answers=[],    # Ответы на открытые вопросы
                test_stage="closed",  # Начинаем с закрытых вопросов
                migration_state = "block_4_final_testing",
                current_course = current_course
                )
            await save_cursor(callback.user_id, extra_data = dict(
                closed_questions=closed_questions,
                open_questions=open_questions,
                current_question=0,
                closed_answers=[],  # Ответы на закрытые вопросы
                open_answers=[],    # Ответы на открытые вопросы
                test_stage="closed",  # Начинаем с закрытых вопросов
                migration_state = "block_4_final_testing",
                current_course = current_course  
            ))
        else:
            data = dict()
            data.update(
                closed_questions=closed_questions,
                open_questions=open_questions,
                current_question=0,
                closed_answers=[],  # Ответы на закрытые вопросы
                open_answers=[],    # Ответы на открытые вопросы
                test_stage="closed",  # Начинаем с закрытых вопросов
                migration_state = "block_4_final_testing"
                )
            await save_cursor(callback.user_id, extra_data = dict(
                closed_questions=closed_questions,
                open_questions=open_questions,
                current_question=0,
                closed_answers=[],  # Ответы на закрытые вопросы
                open_answers=[],    # Ответы на открытые вопросы
                test_stage="closed",  # Начинаем с закрытых вопросов
                migration_state = "block_4_final_testing",
                current_course = current_course  
            ))
            
        logger.info(f'[start_testing_block4_handler] после добавления вопросов в state: {data=}')  
        cursor.change_data(data)  # !!!!!!!!!!
        # Отправляем первый закрытый вопрос
        logger.info(f'[start_testing_block4_handler] Отправляем первый закрытый вопрос')
        await send_question_step_12(callback, cursor, "section_22")
        await save_cursor(callback.user_id, extra_data = {'final_block_4_flag': True, 'state_name': TrainingStates.block_3_final_testing, 'payload': 'start_final_test'})

        #cursor.change_state(TrainingStates.block_4_final_testing)
        

    except Exception as e:
        logger.error(f"[ERROR][start_testing_block4_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)           


# ============================================================================
# БЛОК №5: Работа с Битрикс 
# РАЗДЕЛ №1: 15 видео уроков
# ============================================================================

@router.on_button_callback(state(TrainingStates.block_4_final_testing), lambda data: data.payload == "next_educ_to_part_2")
async def start_block_5_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Обработчик завершения обучения по 4 блоку и перехода к блоку № 5 при нажатии на кнопку ПРОДОЛЖИТЬ ОБУЧЕНИЕ"""
    try:
        logger.info(f'[INFO][start_block_5_handler] Стартовал')
        cursor_redis_data = await load_cursor(callback.user_id)
        if 'state_name' in cursor_redis_data:
            del cursor_redis_data['state_name']
        if 'payload' in cursor_redis_data:
            del cursor_redis_data['payload']
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        
        if continue_flag:
            intro_text = get_block5_intro_text()
            await callback.send(intro_text)
            await asyncio.sleep(2) # 15
        
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        
        game = GamificationService(current_course)
        user_id = callback.user_id
                
        # if await debounce_button_max(callback, cursor):
        #     return
        await callback.message.delete()
        
          
        intro_text = get_block5_intro_video1()
        
        await callback.send(intro_text)
        
        game.mark_video_section_viewed(user_id, "video_section_1")
        await asyncio.sleep(2) # 15
        
        kb = KeyboardBuilder().add(CallbackButton(text="📚 Продолжить обучение", payload="next_education::not_first"))
                 
        await callback.send(
            "📚 Вы можете продолжить обучение, нажав кнопку ниже 👇",
            keyboard=kb
        )  

        await save_cursor(callback.user_id, extra_data={**cursor_redis_data, 'state_name': TrainingStates.block_5_video_2_viewer, 'payload': 'mark_video_section_viewed'})
        cursor.change_state(TrainingStates.block_5_video_2_viewer)
               
        return
        
    except Exception as e:
        logger.error(f'[ERROR][start_block_5_handler] Произошла ошибка {e}')
    finally:
        await remove_repeat_flag(callback.user_id)


@router.on_button_callback(state(TrainingStates.block_5_video_2_viewer), lambda data: data.payload.split('::')[1] == "not_first")
async def block_5_video_2_handler(callback: Callback, cursor: FSMCursor):
    """БЛОК № 5 - Переход  к просмотру видео № 2"""
    try:
        logger.info(f'[INFO][block_5_video_2_handler] Стартовал')
        cursor_redis_data = await load_cursor(callback.user_id)
        if 'state_name' in cursor_redis_data:
            del cursor_redis_data['state_name']

        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        
        game = GamificationService(current_course)
        user_id = callback.user_id      
        # if await debounce_button_max(callback, cursor):
        #     return
        await callback.message.delete()
        
          
        intro_text = get_block5_intro_video2()
        
        await callback.send(intro_text)
        
        game.mark_video_section_viewed(user_id, "video_section_2")
        await asyncio.sleep(2) # 15
        
        kb = KeyboardBuilder().add(CallbackButton(text="📚 Продолжить обучение", payload="next_education::not_first"))
                 
        await callback.send(
            "📚 Вы можете продолжить обучение, нажав кнопку ниже 👇",
            keyboard=kb
        )  

        await save_cursor(callback.user_id, extra_data={**cursor_redis_data, 'state_name': TrainingStates.block_5_video_3_viewer})
        cursor.change_state(TrainingStates.block_5_video_3_viewer)
               
        return
        
    except Exception as e:
        logger.error(f'[ERROR][block_5_video_2_handler] Произошла ошибка {e}')
    finally:
        await remove_repeat_flag(callback.user_id)
        
        
@router.on_button_callback(state(TrainingStates.block_5_video_3_viewer), lambda data: data.payload.split('::')[1] == "not_first")
async def block_5_video_3_handler(callback: Callback, cursor: FSMCursor):
    """БЛОК № 5 - Переход  к просмотру видео № 3"""
    try:
        logger.info(f'[INFO][block_5_video_3_handler] Стартовал')
        cursor_redis_data = await load_cursor(callback.user_id)
        if 'state_name' in cursor_redis_data:
            del cursor_redis_data['state_name']

        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        
        game = GamificationService(current_course)
        user_id = callback.user_id       
        # if await debounce_button_max(callback, cursor):
        #     return
        await callback.message.delete()
        
          
        intro_text = get_block5_intro_video3()
        
        await callback.send(intro_text)
        
        game.mark_video_section_viewed(user_id, "video_section_3")
        await asyncio.sleep(2) # 15
        
        kb = KeyboardBuilder().add(CallbackButton(text="📚 Продолжить обучение", payload="next_education::not_first"))
                 
        await callback.send(
            "📚 Вы можете продолжить обучение, нажав кнопку ниже 👇",
            keyboard=kb
        )  

        await save_cursor(callback.user_id, extra_data={**cursor_redis_data, 'state_name': TrainingStates.block_5_video_4_viewer})
        cursor.change_state(TrainingStates.block_5_video_4_viewer)
               
        return
        
    except Exception as e:
        logger.error(f'[ERROR][block_5_video_3_handler] Произошла ошибка {e}')
    finally:
        await remove_repeat_flag(callback.user_id)


@router.on_button_callback(state(TrainingStates.block_5_video_4_viewer), lambda data: data.payload.split('::')[1] == "not_first")
async def block_5_video_4_handler(callback: Callback, cursor: FSMCursor):
    """БЛОК № 5 - Переход  к просмотру видео № 4"""
    try:
        logger.info(f'[INFO][block_5_video_4_handler] Стартовал')
        cursor_redis_data = await load_cursor(callback.user_id)
        if 'state_name' in cursor_redis_data:
            del cursor_redis_data['state_name']

        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        
        game = GamificationService(current_course)
        user_id = callback.user_id
                
        # if await debounce_button_max(callback, cursor):
        #     return
        await callback.message.delete()
        
          
        intro_text = get_block5_intro_video4()
        
        await callback.send(intro_text)
        
        game.mark_video_section_viewed(user_id, "video_section_4")
        await asyncio.sleep(2) # 15
        
        kb = KeyboardBuilder().add(CallbackButton(text="📚 Продолжить обучение", payload="next_education::not_first"))
                 
        await callback.send(
            "📚 Вы можете продолжить обучение, нажав кнопку ниже 👇",
            keyboard=kb
        )  

        await save_cursor(callback.user_id, extra_data={**cursor_redis_data, 'state_name': TrainingStates.block_5_video_5_viewer})
        cursor.change_state(TrainingStates.block_5_video_5_viewer)
               
        return
        
    except Exception as e:
        logger.error(f'[ERROR][block_5_video_4_handler] Произошла ошибка {e}')
    finally:
        await remove_repeat_flag(callback.user_id)        
         
         
@router.on_button_callback(state(TrainingStates.block_5_video_5_viewer), lambda data: data.payload.split('::')[1] == "not_first")
async def block_5_video_5_handler(callback: Callback, cursor: FSMCursor):
    """БЛОК № 5 - Переход  к просмотру видео № 5"""
    try:
        logger.info(f'[INFO][block_5_video_5_handler] Стартовал')
        
        cursor_redis_data = await load_cursor(callback.user_id)
        if 'state_name' in cursor_redis_data:
            del cursor_redis_data['state_name']

        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        
        game = GamificationService(current_course)
        user_id = callback.user_id        
        # if await debounce_button_max(callback, cursor):
        #     return
        await callback.message.delete()
        
          
        intro_text = get_block5_intro_video5()
        
        await callback.send(intro_text)
        
        game.mark_video_section_viewed(user_id, "video_section_5")
        await asyncio.sleep(2) # 15
        
        kb = KeyboardBuilder().add(CallbackButton(text="📚 Продолжить обучение", payload="next_education::not_first"))
                 
        await callback.send(
            "📚 Вы можете продолжить обучение, нажав кнопку ниже 👇",
            keyboard=kb
        )  

        await save_cursor(callback.user_id, extra_data={**cursor_redis_data, 'state_name': TrainingStates.block_5_video_6_viewer})
        cursor.change_state(TrainingStates.block_5_video_6_viewer)
               
        return
        
    except Exception as e:
        logger.error(f'[ERROR][block_5_video_5_handler] Произошла ошибка {e}')
    finally:
        await remove_repeat_flag(callback.user_id)   
        

@router.on_button_callback(state(TrainingStates.block_5_video_6_viewer), lambda data: data.payload.split('::')[1] == "not_first")
async def block_5_video_6_handler(callback: Callback, cursor: FSMCursor):
    """БЛОК № 5 - Переход  к просмотру видео № 6"""
    try:
        logger.info(f'[INFO][block_5_video_6_handler] Стартовал')
        
        cursor_redis_data = await load_cursor(callback.user_id)
        if 'state_name' in cursor_redis_data:
            del cursor_redis_data['state_name']

        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        
        game = GamificationService(current_course)
        user_id = callback.user_id          
        # if await debounce_button_max(callback, cursor):
        #     return
        await callback.message.delete()
        
          
        intro_text = get_block5_intro_video6()
        
        await callback.send(intro_text)
        
        game.mark_video_section_viewed(user_id, "video_section_6")
        await asyncio.sleep(2) # 15
        
        kb = KeyboardBuilder().add(CallbackButton(text="📚 Продолжить обучение", payload="next_education::not_first"))
                 
        await callback.send(
            "📚 Вы можете продолжить обучение, нажав кнопку ниже 👇",
            keyboard=kb
        )  

        await save_cursor(callback.user_id, extra_data={**cursor_redis_data, 'state_name': TrainingStates.block_5_video_5_viewer})
        cursor.change_state(TrainingStates.block_5_video_7_viewer)
               
        return
        
    except Exception as e:
        logger.error(f'[ERROR][block_5_video_6_handler] Произошла ошибка {e}')
    finally:
        await remove_repeat_flag(callback.user_id)           
     
        
@router.on_button_callback(state(TrainingStates.block_5_video_7_viewer), lambda data: data.payload.split('::')[1] == "not_first")
async def block_5_video_7_handler(callback: Callback, cursor: FSMCursor):
    """БЛОК № 5 - Переход  к просмотру видео № 7"""
    try:
        logger.info(f'[INFO][block_5_video_7_handler] Стартовал')
        
        cursor_redis_data = await load_cursor(callback.user_id)
        if 'state_name' in cursor_redis_data:
            del cursor_redis_data['state_name']

        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        
        game = GamificationService(current_course)
        user_id = callback.user_id            
        # if await debounce_button_max(callback, cursor):
        #     return
        await callback.message.delete()
        
          
        intro_text = get_block5_intro_video7()
        
        await callback.send(intro_text)
        
        game.mark_video_section_viewed(user_id, "video_section_7")
        await asyncio.sleep(2) # 15
        
        kb = KeyboardBuilder().add(CallbackButton(text="📚 Продолжить обучение", payload="next_education::not_first"))
                 
        await callback.send(
            "📚 Вы можете продолжить обучение, нажав кнопку ниже 👇",
            keyboard=kb
        )  

        await save_cursor(callback.user_id, extra_data={**cursor_redis_data, 'state_name': TrainingStates.block_5_video_8_viewer})
        cursor.change_state(TrainingStates.block_5_video_8_viewer)
               
        return
        
    except Exception as e:
        logger.error(f'[ERROR][block_5_video_7_handler] Произошла ошибка {e}')
    finally:
        await remove_repeat_flag(callback.user_id)           


@router.on_button_callback(state(TrainingStates.block_5_video_8_viewer), lambda data: data.payload.split('::')[1] == "not_first")
async def block_5_video_8_handler(callback: Callback, cursor: FSMCursor):
    """БЛОК № 5 - Переход  к просмотру видео № 8"""
    try:
        logger.info(f'[INFO][block_5_video_8_handler] Стартовал')
        cursor_redis_data = await load_cursor(callback.user_id)
        if 'state_name' in cursor_redis_data:
            del cursor_redis_data['state_name']

        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        game = GamificationService(current_course)
        user_id = callback.user_id        
        # if await debounce_button_max(callback, cursor):
        #     return
        await callback.message.delete()
        
          
        intro_text = get_block5_intro_video8()
        
        await callback.send(intro_text)
        
        game.mark_video_section_viewed(user_id, "video_section_8")
        await asyncio.sleep(2) # 15
        
        kb = KeyboardBuilder().add(CallbackButton(text="📚 Продолжить обучение", payload="next_education::not_first"))
                 
        await callback.send(
            "📚 Вы можете продолжить обучение, нажав кнопку ниже 👇",
            keyboard=kb
        )  

        await save_cursor(callback.user_id, extra_data={**cursor_redis_data, 'state_name': TrainingStates.block_5_video_9_viewer})
        cursor.change_state(TrainingStates.block_5_video_9_viewer)
               
        return
        
    except Exception as e:
        logger.error(f'[ERROR][block_5_video_8_handler] Произошла ошибка {e}')
    finally:
        await remove_repeat_flag(callback.user_id) 
        

@router.on_button_callback(state(TrainingStates.block_5_video_9_viewer), lambda data: data.payload.split('::')[1] == "not_first")
async def block_5_video_9_handler(callback: Callback, cursor: FSMCursor):
    """БЛОК № 5 - Переход  к просмотру видео № 9"""
    try:
        logger.info(f'[INFO][block_5_video_9_handler] Стартовал')
        cursor_redis_data = await load_cursor(callback.user_id)
        if 'state_name' in cursor_redis_data:
            del cursor_redis_data['state_name']

        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        game = GamificationService(current_course)
        user_id = callback.user_id             
        # if await debounce_button_max(callback, cursor):
        #     return
        await callback.message.delete()
        
          
        intro_text = get_block5_intro_video9()
        
        await callback.send(intro_text)
        
        game.mark_video_section_viewed(user_id, "video_section_9")
        await asyncio.sleep(2) # 15
        
        kb = KeyboardBuilder().add(CallbackButton(text="📚 Продолжить обучение", payload="next_education::not_first"))
                 
        await callback.send(
            "📚 Вы можете продолжить обучение, нажав кнопку ниже 👇",
            keyboard=kb
        )  

        await save_cursor(callback.user_id, extra_data={**cursor_redis_data, 'state_name': TrainingStates.block_5_video_10_viewer})
        cursor.change_state(TrainingStates.block_5_video_10_viewer)
               
        return
        
    except Exception as e:
        logger.error(f'[ERROR][block_5_video_9_handler] Произошла ошибка {e}')
    finally:
        await remove_repeat_flag(callback.user_id)                


@router.on_button_callback(state(TrainingStates.block_5_video_10_viewer), lambda data: data.payload.split('::')[1] == "not_first")
async def block_5_video_10_handler(callback: Callback, cursor: FSMCursor):
    """БЛОК № 5 - Переход  к просмотру видео № 10"""
    try:
        logger.info(f'[INFO][block_5_video_10_handler] Стартовал')
        cursor_redis_data = await load_cursor(callback.user_id)
        if 'state_name' in cursor_redis_data:
            del cursor_redis_data['state_name']

        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        game = GamificationService(current_course)
        user_id = callback.user_id               
        # if await debounce_button_max(callback, cursor):
        #     return
        await callback.message.delete()
        
          
        intro_text = get_block5_intro_video10()
        
        await callback.send(intro_text)
        
        game.mark_video_section_viewed(user_id, "video_section_10")
        await asyncio.sleep(2) # 15
        
        kb = KeyboardBuilder().add(CallbackButton(text="📚 Продолжить обучение", payload="next_education::not_first"))
                 
        await callback.send(
            "📚 Вы можете продолжить обучение, нажав кнопку ниже 👇",
            keyboard=kb
        )  

        await save_cursor(callback.user_id, extra_data={**cursor_redis_data, 'state_name': TrainingStates.block_5_video_11_viewer})
        cursor.change_state(TrainingStates.block_5_video_11_viewer)
               
        return
        
    except Exception as e:
        logger.error(f'[ERROR][block_5_video_10_handler] Произошла ошибка {e}')
    finally:
        await remove_repeat_flag(callback.user_id)


@router.on_button_callback(state(TrainingStates.block_5_video_11_viewer), lambda data: data.payload.split('::')[1] == "not_first")
async def block_5_video_11_handler(callback: Callback, cursor: FSMCursor):
    """БЛОК № 5 - Переход  к просмотру видео № 11"""
    try:
        logger.info(f'[INFO][block_5_video_11_handler] Стартовал')
        cursor_redis_data = await load_cursor(callback.user_id)
        if 'state_name' in cursor_redis_data:
            del cursor_redis_data['state_name']

        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        game = GamificationService(current_course)
        user_id = callback.user_id          
        # if await debounce_button_max(callback, cursor):
        #     return
        await callback.message.delete()
        
          
        intro_text = get_block5_intro_video11()
        
        await callback.send(intro_text)
        
        game.mark_video_section_viewed(user_id, "video_section_11")
        await asyncio.sleep(2) # 15
        
        kb = KeyboardBuilder().add(CallbackButton(text="📚 Продолжить обучение", payload="next_education::not_first"))
                 
        await callback.send(
            "📚 Вы можете продолжить обучение, нажав кнопку ниже 👇",
            keyboard=kb
        )  

        await save_cursor(callback.user_id, extra_data={**cursor_redis_data, 'state_name': TrainingStates.block_5_video_12_viewer})
        cursor.change_state(TrainingStates.block_5_video_12_viewer)
               
        return
        
    except Exception as e:
        logger.error(f'[ERROR][block_5_video_11_handler] Произошла ошибка {e}')
    finally:
        await remove_repeat_flag(callback.user_id)         


@router.on_button_callback(state(TrainingStates.block_5_video_12_viewer), lambda data: data.payload.split('::')[1] == "not_first")
async def block_5_video_12_handler(callback: Callback, cursor: FSMCursor):
    """БЛОК № 5 - Переход  к просмотру видео № 12"""
    try:
        logger.info(f'[INFO][block_5_video_12_handler] Стартовал')
        cursor_redis_data = await load_cursor(callback.user_id)
        if 'state_name' in cursor_redis_data:
            del cursor_redis_data['state_name']

        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        game = GamificationService(current_course)
        user_id = callback.user_id          
        # if await debounce_button_max(callback, cursor):
        #     return
        await callback.message.delete()
        
          
        intro_text = get_block5_intro_video12()
        
        await callback.send(intro_text)
        
        game.mark_video_section_viewed(user_id, "video_section_12")
        await asyncio.sleep(2) # 15
        
        kb = KeyboardBuilder().add(CallbackButton(text="📚 Продолжить обучение", payload="next_education::not_first"))
                 
        await callback.send(
            "📚 Вы можете продолжить обучение, нажав кнопку ниже 👇",
            keyboard=kb
        )  

        await save_cursor(callback.user_id, extra_data={**cursor_redis_data, 'state_name': TrainingStates.block_5_video_13_viewer})
        cursor.change_state(TrainingStates.block_5_video_13_viewer)
               
        return
        
    except Exception as e:
        logger.error(f'[ERROR][block_5_video_12_handler] Произошла ошибка {e}')
    finally:
        await remove_repeat_flag(callback.user_id) 
        
        
@router.on_button_callback(state(TrainingStates.block_5_video_13_viewer), lambda data: data.payload.split('::')[1] == "not_first")
async def block_5_video_13_handler(callback: Callback, cursor: FSMCursor):
    """БЛОК № 5 - Переход  к просмотру видео № 13"""
    try:
        logger.info(f'[INFO][block_5_video_13_handler] Стартовал')
        cursor_redis_data = await load_cursor(callback.user_id)
        if 'state_name' in cursor_redis_data:
            del cursor_redis_data['state_name']

        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        game = GamificationService(current_course)
        user_id = callback.user_id              
        # if await debounce_button_max(callback, cursor):
        #     return
        await callback.message.delete()
        
          
        intro_text = get_block5_intro_video13()
        
        await callback.send(intro_text)
        
        game.mark_video_section_viewed(user_id, "video_section_13")
        await asyncio.sleep(2) # 15
        
        kb = KeyboardBuilder().add(CallbackButton(text="📚 Продолжить обучение", payload="next_education::not_first"))
                 
        await callback.send(
            "📚 Вы можете продолжить обучение, нажав кнопку ниже 👇",
            keyboard=kb
        )  

        await save_cursor(callback.user_id, extra_data={**cursor_redis_data, 'state_name': TrainingStates.block_5_video_14_viewer})
        cursor.change_state(TrainingStates.block_5_video_14_viewer)
               
        return
        
    except Exception as e:
        logger.error(f'[ERROR][block_5_video_13_handler] Произошла ошибка {e}')
    finally:
        await remove_repeat_flag(callback.user_id)   
        
        
@router.on_button_callback(state(TrainingStates.block_5_video_14_viewer), lambda data: data.payload.split('::')[1] == "not_first")
async def block_5_video_14_handler(callback: Callback, cursor: FSMCursor):
    """БЛОК № 5 - Переход  к просмотру видео № 14"""
    try:
        logger.info(f'[INFO][block_5_video_14_handler] Стартовал')
        cursor_redis_data = await load_cursor(callback.user_id)
        if 'state_name' in cursor_redis_data:
            del cursor_redis_data['state_name']

        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        
        game = GamificationService(current_course)
        user_id = callback.user_id          
        # if await debounce_button_max(callback, cursor):
        #     return
        await callback.message.delete()
        
          
        intro_text = get_block5_intro_video14()
        
        await callback.send(intro_text)
        
        game.mark_video_section_viewed(user_id, "video_section_14")
        await asyncio.sleep(2) # 15
        
        kb = KeyboardBuilder().add(CallbackButton(text="📚 Продолжить обучение", payload="next_education::not_first"))
                 
        await callback.send(
            "📚 Вы можете продолжить обучение, нажав кнопку ниже 👇",
            keyboard=kb
        )  

        await save_cursor(callback.user_id, extra_data={**cursor_redis_data, 'state_name': TrainingStates.block_5_video_15_viewer})
        cursor.change_state(TrainingStates.block_5_video_15_viewer)
               
        return
        
    except Exception as e:
        logger.error(f'[ERROR][block_5_video_14_handler] Произошла ошибка {e}')
    finally:
        await remove_repeat_flag(callback.user_id) 
        

@router.on_button_callback(state(TrainingStates.block_5_video_15_viewer), lambda data: data.payload.split('::')[1] == "not_first")
async def block_5_video_15_handler(callback: Callback, cursor: FSMCursor):
    """БЛОК № 5 - Переход  к просмотру видео № 15"""
    try:
        logger.info(f'[INFO][block_5_video_15_handler] Стартовал')
        cursor_redis_data = await load_cursor(callback.user_id)
        if 'state_name' in cursor_redis_data:
            del cursor_redis_data['state_name']

        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        
        game = GamificationService(current_course)
        user_id = callback.user_id           
        # if await debounce_button_max(callback, cursor):
        #     return
        await callback.message.delete()
        
          
        intro_text = get_block5_intro_video15()
        
        await callback.send(intro_text)
        
        game.mark_video_section_viewed(user_id, "video_section_15")
        await asyncio.sleep(2) # 15
        
        kb = KeyboardBuilder().add(CallbackButton(text="📚 Продолжить обучение", payload="next_education::not_first"))
                 
        await callback.send(
            "📚 Вы можете продолжить обучение, нажав кнопку ниже 👇",
            keyboard=kb
        )  

        await save_cursor(callback.user_id, extra_data={**cursor_redis_data, 'state_name': TrainingStates.block5_final_test})
        cursor.change_state(TrainingStates.block5_final_test)
               
        return
        
    except Exception as e:
        logger.error(f'[ERROR][block_5_video_15_handler] Произошла ошибка {e}')
    finally:
        await remove_repeat_flag(callback.user_id) 
        


@router.on_button_callback(state(TrainingStates.block5_final_test), lambda data: data.payload.split('::')[1] == "not_first")
async def continue_after_block5_handler(callback: Callback, cursor: FSMCursor):
    """Завершение Блока №5 - Клиент и ЦА. Переход к вопросам или финальному тесту"""
    try:
        logger.info(f"[continue_after_block5_handler] Стартовал")
        logger.info(f"[continue_after_block5_handler] Прибавляем к прогрессу прохождения курса 15 видео-уроков")
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)  
        game = GamificationService(current_course)
        user_id = callback.user_id
                      
        #lessons_completed = game.get_lessons_completed(user_id) if current_course != "Другой сотрудник" else game.get_lessons_completed(user_id, "Другой сотрудник") # !!!!!!!!!!!!!!!
        lessons_completed = game.get_lessons_completed(user_id) if current_course not in ["Другой сотрудник", "Обучение по продукту"] else game.get_lessons_completed(user_id, "Обучение по продукту")
        
        #lessons_completed = game.get_lessons_completed(user_id)
        if lessons_completed < 38:
            game.increment_lessons_completed(user_id, increment_lesson=15)    
        
        # Проверяем загрузку базы знаний
        rag = RAGService()
        stats = rag.get_stats()
        
        if not stats['is_loaded']:
            await callback.send(
                "❌ База знаний не загружена. Обратитесь к администратору.",
                keyboard=main_menu_keyboard(current_course)
            )
            cursor.clear()
            return
        
        text = get_text_to_final_test_block_5()
        
        #await callback.send(text)
        await callback.send(text, keyboard=final_start_test_kb())
        cursor.change_state(TrainingStates.block5_questions)
        await save_cursor(callback.user_id, extra_data = {'payload': 'to_final_test', 'state_name': TrainingStates.block5_questions, 'current_course': current_course})
        
        # await asyncio.sleep(2)
        # await start_block2_final_test_handler(callback, cursor)
        return
        
    
    except Exception as e:
        logger.error(f"[continue_after_block5_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 
        

@router.on_button_callback(state(TrainingStates.block5_questions), lambda data: data.payload == 'to_final_test')
async def start_block5_final_test_handler(callback: Callback, cursor: FSMCursor):
    """Переход к финальному тесту по Блоку №5"""
    try:
        logger.info(f"[INFO][start_block5_final_test_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)    
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        text = get_text_start_final_test_block_5()
        
        data = cursor.get_data()
        if not data:
            data = dict()
            status_user = await get_value_from_redis(callback.user_id, 'status_user')
            if not status_user:
                status_user = 'new_employer'
        else:
            status_user = data.get('status_user', 'new_employer')
        data.update(current_question=0, current_course=current_course, status_user=status_user)
        data.update(payload = 'start_final_test')
        cursor.change_data(data)
        await callback.send(text, keyboard=final_test_kb())
        cursor.change_state(TrainingStates.block_5_final_testing)
        await save_cursor(callback.user_id, extra_data = {**data, 'state_name': TrainingStates.block_5_final_testing, 'payload': 'start_final_test'})
           
    
    except Exception as e:
        logger.error(f"[ERROR][start_block5_final_test_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)
               

@router.on_message(state(TrainingStates.lawyer['final_test_questions']))
@router.on_message(state(TrainingStates.lawyer['block5_questions']))
@router.on_message(state(TrainingStates.block5_questions))
async def answer_block5_question_handler(message: Message, cursor: FSMCursor, state_name: str = None):
    """Ответы на вопросы по Блоку 5 через RAG + Claude"""
    try:
        logger.info(f"[INFO][answer_block5_question_handler] Стартовал")
        cursor_redis_data = await load_cursor(message.user_id)
        del cursor_redis_data['state_name']
        await save_cursor(message.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)    
        # Показываем процесс
        thinking_msg = await message.send("🔍 Ищу информацию в базе знаний...")
        
        if not state_name:
            state = cursor.get_state() # изменил 12.07.26 !!!!!
            state_name = state.state if all([state, not isinstance(state, str)]) else state
            logger.info(f'Из курсора: {state_name=}')
        else:
            logger.info(f'Из аргумента обработчика: {state_name=}')
        
        if state_name in ['block5_questions_lawyer', 'final_test_questions_lawyer']:
            rag = RAGService(branch_name = 'lawyer')
        else:
            rag = RAGService()
        
        answer = await rag.answer_question(message.body.text)
        
        await thinking_msg.delete() 
        
        # Форматируем ответ
        logger.info(f"[INFO][answer_block5_question_handler] Форматируем ответ") 
        response_text = (
            f"💡 **Ответ по {'Блоку №5' if state_name != 'final_test_questions_lawyer' else 'Курсу'}:**\n\n"
            f"{answer}\n\n"
            "➡️ Задайте следующий вопрос или нажмите 📝 **Перейти к тестированию**"
        )
        
        await message.send(response_text, keyboard=final_start_test_kb(), format='markdown')
        
        cursor.change_state(state_name)
        await save_cursor(message.user_id, extra_data = {**cursor_redis_data, 'state_name': state_name})
         
    
    except Exception as e:
        await thinking_msg.delete()
        logger.error(f"[ERROR][answer_block5_question_handler] Произошла ошибка {e}")   

        await message.send(
            "❌ Произошла ошибка при обработке вопроса.\n\n"
            "Попробуйте задать вопрос ещё раз или обратитесь к администратору.",
            keyboard=final_start_test_kb()
        )
    finally:
        await remove_repeat_flag(message.user_id) 
        

@router.on_message(state(TrainingStates.block_5_final_testing))
async def block5_final_testing_handler(message: Message, cursor: FSMCursor):
    """Ответы на вопросы по Блоку 5 через RAG + Claude"""
    try:
        logger.info(f"[INFO][answer_block5_question_handler] Стартовал")   
        
        #await thinking_msg.delete() 
        await asyncio.sleep(2)
        await send_question_step_12(message, cursor, 'section_39')
        return
            
    except Exception as e:
        #await thinking_msg.delete()
        logger.error(f"[ERROR][answer_block2_question_handler] Произошла ошибка {e}")   

        await message.send(
            "❌ Произошла ошибка при обработке вопроса.\n\n"
            "Попробуйте задать вопрос ещё раз или обратитесь к администратору.",
            keyboard=final_start_test_kb()
        )                                               


# ============================================================================
# ШАГ № __: ФИНАЛЬНОЕ ТЕСТИРОВАНИЕ ПО БЛОКУ № 5 (10 закрытых + 5 открытых)
# ============================================================================


@router.on_button_callback(state(TrainingStates.block_5_final_testing), lambda data: data.payload == 'start_final_test')
async def start_testing_block5_handler(callback: Callback, cursor: FSMCursor):
    """ШАГ № __ - Запуск финального тестирования по Блоку 5"""
    try:
        logger.info(f"[INFO][start_testing_block5_handler] Стартовал")
        await del_value_from_redis(callback.user_id, 'payload')
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        # ЧАСТЬ 1: Закрытые вопросы (10 вопросов с вариантами A/B/C/D)
        closed_questions = get_final_test_block_5('close')
        
        # ЧАСТЬ 2: Открытые вопросы (5 вопросов с эталонными ответами)
        open_questions = get_final_test_block_5('open')
        
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        logger.info(f'{current_course=}')
        
        data = cursor.get_data()
        logger.info(f'[start_testing_block5_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(
                closed_questions=closed_questions,
                open_questions=open_questions,
                current_question=0,
                closed_answers=[],  # Ответы на закрытые вопросы
                open_answers=[],    # Ответы на открытые вопросы
                test_stage="closed",  # Начинаем с закрытых вопросов
                migration_state = "block_5_final_testing",
                current_course = current_course
                )
            await save_cursor(callback.user_id, extra_data = dict(
                closed_questions=closed_questions,
                open_questions=open_questions,
                current_question=0,
                closed_answers=[],  # Ответы на закрытые вопросы
                open_answers=[],    # Ответы на открытые вопросы
                test_stage="closed",  # Начинаем с закрытых вопросов
                migration_state = "block_5_final_testing",
                current_course = current_course
            ))
        else:
            data = dict()
            data.update(
                closed_questions=closed_questions,
                open_questions=open_questions,
                current_question=0,
                closed_answers=[],  # Ответы на закрытые вопросы
                open_answers=[],    # Ответы на открытые вопросы
                test_stage="closed",  # Начинаем с закрытых вопросов
                migration_state = "block_5_final_testing",
                current_course = current_course
                )
            await save_cursor(callback.user_id, extra_data = dict(
                closed_questions=closed_questions,
                open_questions=open_questions,
                current_question=0,
                closed_answers=[],  # Ответы на закрытые вопросы
                open_answers=[],    # Ответы на открытые вопросы
                test_stage="closed",  # Начинаем с закрытых вопросов
                migration_state = "block_5_final_testing",
                current_course = current_course
            ))
            
        logger.info(f'[start_testing_block5_handler] после добавления вопросов в state: {data=}')  
        cursor.change_data(data)  # !!!!!!!!!!
        # Отправляем первый закрытый вопрос
        logger.info(f'[start_testing_block5_handler] Отправляем первый закрытый вопрос')
        await send_question_step_12(callback, cursor, "section_39")

        #cursor.change_state(TrainingStates.block_5_final_testing)
        await save_cursor(callback.user_id, extra_data = {'final_block_5_flag': True, 'state_name': TrainingStates.block_5_final_testing, 'payload': 'start_final_test'})
        

    except Exception as e:
        logger.error(f"[ERROR][start_testing_block5_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)  


# ============================================================================
# БЛОК №6: Power BI: инструмент для аналитики
# ============================================================================
'''
@router.on_button_callback(state(TrainingStates.block_5_final_testing), lambda data: data.payload == "next_educ_to_part_2")
async def start_block_6_handler(callback: Callback, cursor: FSMCursor):
    """Обработчик завершения обучения по 5 блоку и перехода к блоку № 6 при нажатии на кнопку ПРОДОЛЖИТЬ ОБУЧЕНИЕ"""
    try:
        logger.info(f'[INFO][start_block_6_handler] Стартовал')
        #cursor.change_state(TrainingStates.block4_start)
        
        # if await debounce_button_max(callback, cursor):
        #     return
        await callback.message.delete()
        
        intro_text = get_block6_intro_text()
        
        kb = next_to_educ_to_part_kb()
        await callback.send(intro_text, format='markdown', disable_link_preview=True, keyboard=kb)
        cursor.change_state(TrainingStates.block_6_section_1_next)
               
        return
        
    except Exception as e:
        logger.error(f'[ERROR][start_block_6_handler] Произошла ошибка {e}')
'''     

#@router.on_button_callback(state(TrainingStates.block_6_section_1_next), lambda data: data.payload == "next_educ_to_part_2")        
@router.on_button_callback(state(TrainingStates.block_5_final_testing), lambda data: data.payload == "next_educ_to_part_2")
async def start_block_6_section_1_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Обработчик единственного учебного раздела блока 6 и переход к завершению 
    обучения по 5 блоку и перехода к блоку № 6 при нажатии на кнопку ПРОДОЛЖИТЬ ОБУЧЕНИЕ"""
    try:
        logger.info(f'[INFO][start_block_6_section_1_handler] Стартовал')
        cursor_redis_data = await load_cursor(callback.user_id)
        if 'state_name' in cursor_redis_data:
            del cursor_redis_data['state_name']
        if 'payload' in cursor_redis_data:
            del cursor_redis_data['payload']
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        
        if continue_flag:
            intro_text = get_block6_intro_text()
            await callback.send(intro_text, disable_link_preview=True)
            await asyncio.sleep(2) # 10
        #cursor.change_state(TrainingStates.block4_start)
        
        # if await debounce_button_max(callback, cursor):
        #     return
        await callback.message.delete()
        intro_text = get_block6_section_1_intro_text()  
        #await callback.send(intro_text, disable_link_preview=True)
        
        await asyncio.sleep(2) # 15
        
        kb = next_to_educ_to_part_kb()
        await callback.send(intro_text, format='markdown', disable_link_preview=True, keyboard=kb)
        await save_cursor(callback.user_id, extra_data={**cursor_redis_data, 'state_name': TrainingStates.block_6_final_test, 'payload': 'ai_after_block6',})
        cursor.change_state(TrainingStates.block_6_final_test)
               
        return
        
    except Exception as e:
        logger.error(f'[ERROR][start_block_6_section_1_handler] Произошла ошибка {e}')
    finally:
        await remove_repeat_flag(callback.user_id) 
        

@router.on_button_callback(state(TrainingStates.block_6_final_test), lambda data: data.payload == "next_educ_to_part_2")
async def continue_after_block6_handler(callback: Callback, cursor: FSMCursor):
    """Завершение Блока №6 - Клиент и ЦА. Переход к вопросам или финальному тесту"""
    try:
        logger.info(f"[continue_after_block6_handler] Стартовал")
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)  
        game = GamificationService(current_course)
        user_id = callback.user_id
        
        #lessons_completed = game.get_lessons_completed(user_id) if current_course != "Другой сотрудник" else game.get_lessons_completed(user_id, "Другой сотрудник") # !!!!!!!!!!!!!!!!!!
        lessons_completed = game.get_lessons_completed(user_id) if current_course not in ["Другой сотрудник", "Обучение по продукту"] else game.get_lessons_completed(user_id, "Обучение по продукту")
        if lessons_completed < 41:
            game.increment_lessons_completed(user_id, increment_lesson=1)
        # Проверяем загрузку базы знаний
        rag = RAGService()
        stats = rag.get_stats()
        
        if not stats['is_loaded']:
            await callback.send(
                "❌ База знаний не загружена. Обратитесь к администратору.",
                keyboard=main_menu_keyboard(current_course)
            )
            cursor.clear()
            return
        
        text = get_text_to_final_test_block_6()
        
        #await callback.send(text)
        await callback.send(text, keyboard=final_start_test_kb())
        cursor.change_state(TrainingStates.block6_questions)
        await save_cursor(callback.user_id, extra_data = {'payload': 'to_final_test', 'state_name': TrainingStates.block6_questions, 'current_course': current_course})
        
        # await asyncio.sleep(2)
        # await start_block2_final_test_handler(callback, cursor)
        return
        
    
    except Exception as e:
        logger.error(f"[continue_after_block6_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 
        

@router.on_button_callback(state(TrainingStates.block6_questions), lambda data: data.payload == 'to_final_test')
async def start_block6_final_test_handler(callback: Callback, cursor: FSMCursor):
    """Переход к финальному тесту по Блоку №6"""
    try:
        logger.info(f"[INFO][start_block6_final_test_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)    
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        text = get_text_start_final_test_block_6()
        
        data = cursor.get_data()
        if not data:
            data = dict()
            status_user = await get_value_from_redis(callback.user_id, 'status_user')
            if not status_user:
                status_user = 'new_employer'
        else:
            status_user = data.get('status_user', 'new_employer')
        data.update(current_question=0, current_course=current_course, status_user=status_user)
        cursor.change_data(data)
        await callback.send(text, keyboard=final_test_kb())
        cursor.change_state(TrainingStates.block_6_final_testing)
        await save_cursor(callback.user_id, extra_data = {**data, 'state_name': TrainingStates.block_6_final_testing, 'payload': 'start_final_test'})
           
    
    except Exception as e:
        logger.error(f"[ERROR][start_block6_final_test_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)
        

@router.on_message(state(TrainingStates.block6_questions))
async def answer_block6_question_handler(message: Message, cursor: FSMCursor):
    """Ответы на вопросы по Блоку 6 через RAG + Claude"""
    try:
        logger.info(f"[INFO][answer_block6_question_handler] Стартовал")   
        # Показываем процесс
        cursor_redis_data = await load_cursor(message.user_id)
        del cursor_redis_data['state_name']
        await save_cursor(message.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)    
        thinking_msg = await message.send("🔍 Ищу информацию в базе знаний...")
        
        state = cursor.get_state() # изменил 12.07.26 !!!!!
        state_name = state.state if all([state, not isinstance(state, str)]) else state
        logger.info(f'{state_name=}')
        
        if state_name == 'block6_questions_lawyer':
            rag = RAGService(branch_name = 'lawyer')
        else:
            rag = RAGService()
            
        answer = await rag.answer_question(message.body.text)
        
        await thinking_msg.delete() 
        
        # Форматируем ответ
        logger.info(f"[INFO][answer_block6_question_handler] Форматируем ответ") 
        response_text = (
            f"💡 **Ответ по Блоку №6:**\n\n"
            f"{answer}\n\n"
            "➡️ Задайте следующий вопрос или нажмите 📝 **Перейти к тестированию**"
        )
        
        await message.send(response_text, keyboard=final_start_test_kb(), format='markdown')
        cursor.change_state(state_name)
        await save_cursor(message.user_id, extra_data = {**cursor_redis_data, 'state_name': state_name})       
    
    except Exception as e:
        await thinking_msg.delete()
        logger.error(f"[ERROR][answer_block6_question_handler] Произошла ошибка {e}")   

        await message.send(
            "❌ Произошла ошибка при обработке вопроса.\n\n"
            "Попробуйте задать вопрос ещё раз или обратитесь к администратору.",
            keyboard=final_start_test_kb()
        )
    finally:
        await remove_repeat_flag(message.user_id)
        

        
@router.on_message(state(TrainingStates.block_6_final_testing))
async def block6_final_testing_handler(message: Message, cursor: FSMCursor):
    """Ответы на вопросы по Блоку 6 через RAG + Claude"""
    try:
        logger.info(f"[INFO][block6_final_testing_handler] Стартовал")           #await thinking_msg.delete() 
        await asyncio.sleep(2)
        await send_question_step_12(message, cursor, 'section_41')
        return
        
    except Exception as e:
        #await thinking_msg.delete()
        logger.error(f"[ERROR][block6_final_testing_handler] Произошла ошибка {e}")   

        await message.send(
            "❌ Произошла ошибка при обработке вопроса.\n\n"
            "Попробуйте задать вопрос ещё раз или обратитесь к администратору.",
            keyboard=final_start_test_kb()
        )                         
        
# ============================================================================
# ШАГ № __: ФИНАЛЬНОЕ ТЕСТИРОВАНИЕ ПО БЛОКУ № 6 (10 закрытых + 5 открытых)
# ============================================================================


@router.on_button_callback(state(TrainingStates.block_6_final_testing), lambda data: data.payload == 'start_final_test')
async def start_testing_block6_handler(callback: Callback, cursor: FSMCursor):
    """ШАГ № __ - Запуск финального тестирования по Блоку 6"""
    try:
        logger.info(f"[INFO][start_testing_block6_handler] Стартовал")
        await del_value_from_redis(callback.user_id, 'payload')
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        # ЧАСТЬ 1: Закрытые вопросы (10 вопросов с вариантами A/B/C/D)
        closed_questions = get_final_test_block_6('close') 
        
        # ЧАСТЬ 2: Открытые вопросы (5 вопросов с эталонными ответами)
        open_questions = get_final_test_block_6('open')
        
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        logger.info(f'{current_course=}')
        
        data = cursor.get_data()
        logger.info(f'[start_testing_block6_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(
                closed_questions=closed_questions,
                open_questions=open_questions,
                current_question=0,
                closed_answers=[],  # Ответы на закрытые вопросы
                open_answers=[],    # Ответы на открытые вопросы
                test_stage="closed",  # Начинаем с закрытых вопросов
                migration_state = "block_6_final_testing",
                current_course = current_course
                )
            await save_cursor(callback.user_id, extra_data = dict(
                closed_questions=closed_questions,
                open_questions=open_questions,
                current_question=0,
                closed_answers=[],  # Ответы на закрытые вопросы
                open_answers=[],    # Ответы на открытые вопросы
                test_stage="closed",  # Начинаем с закрытых вопросов
                migration_state = "block_6_final_testing",
                current_course = current_course
            ))
        else:
            data = dict()
            data.update(
                closed_questions=closed_questions,
                open_questions=open_questions,
                current_question=0,
                closed_answers=[],  # Ответы на закрытые вопросы
                open_answers=[],    # Ответы на открытые вопросы
                test_stage="closed",  # Начинаем с закрытых вопросов
                migration_state = "block_6_final_testing",
                current_course = current_course
                )
            await save_cursor(callback.user_id, extra_data = dict(
                closed_questions=closed_questions,
                open_questions=open_questions,
                current_question=0,
                closed_answers=[],  # Ответы на закрытые вопросы
                open_answers=[],    # Ответы на открытые вопросы
                test_stage="closed",  # Начинаем с закрытых вопросов
                migration_state = "block_6_final_testing",
                current_course = current_course
            ))
            
        logger.info(f'[start_testing_block6_handler] после добавления вопросов в state: {data=}')  
        cursor.change_data(data)  # !!!!!!!!!!
        # Отправляем первый закрытый вопрос
        logger.info(f'[start_testing_block6_handler] Отправляем первый закрытый вопрос')
        await send_question_step_12(callback, cursor, "section_41")

        cursor.change_state(TrainingStates.block_6_final_testing)
        await save_cursor(callback.user_id, extra_data = {'final_block_6_flag': True, 'state_name': TrainingStates.block_6_final_testing, 'payload': 'start_final_test'})
        

    except Exception as e:
        logger.error(f"[ERROR][start_testing_block6_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 


# ============================================================================
# БЛОК №7: Финальный этап обучения
# ============================================================================

@router.on_button_callback(state(TrainingStates.block_6_final_testing), lambda data: data.payload == "next_educ_to_part_2")
async def start_block_7_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Обработчик завершения обучения по 6 блоку и перехода к блоку № 7 при нажатии на кнопку ПРОДОЛЖИТЬ ОБУЧЕНИЕ"""
    try:
        logger.info(f'[INFO][start_block_7_handler] Стартовал')
        cursor_redis_data = await load_cursor(callback.user_id)
        if 'state_name' in cursor_redis_data:
            del cursor_redis_data['state_name']
        if 'payload' in cursor_redis_data:
            del cursor_redis_data['payload']
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
            
        game = GamificationService(current_course)
        user_id = callback.user_id
        
               
        #lessons_completed = game.get_lessons_completed(user_id) if current_course != "Другой сотрудник" else game.get_lessons_completed(user_id, "Другой сотрудник") # !!!!!!!!!!!!!!!!!
        lessons_completed = game.get_lessons_completed(user_id) if current_course not in ["Другой сотрудник", "Обучение по продукту"] else game.get_lessons_completed(user_id, "Обучение по продукту")
        
        #lessons_completed = game.get_lessons_completed(user_id)
        if lessons_completed < 41:
            game.increment_lessons_completed(user_id, increment_lesson=1)
        #cursor.change_state(TrainingStates.block4_start)
        
        # if await debounce_button_max(callback, cursor):
        #     return
        await callback.message.delete()
        
        # intro_text = get_block7_intro_text()
        
        # await callback.send(intro_text)
        if continue_flag:
            intro_text = get_block7_intro_text()
            await callback.send(intro_text)
        await asyncio.sleep(2) # 15
        
        await save_cursor(callback.user_id, extra_data={**cursor_redis_data, 'state_name': TrainingStates.block7_questions, 'payload': 'start_test'})       
        await continue_after_block7_handler(callback, cursor)
        
    except Exception as e:
        logger.error(f'[ERROR][start_block_6_handler] Произошла ошибка {e}')
    finally:
        await remove_repeat_flag(callback.user_id)
        
        

async def continue_after_block7_handler(callback: Callback, cursor: FSMCursor):
    """Блока №7 - Финальный этап обучения. Переход к вопросам или финальному тесту"""
    try:
        logger.info(f"[continue_after_block7_handler] Стартовал")
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)  
        # Проверяем загрузку базы знаний
        rag = RAGService()
        stats = rag.get_stats()
        
        if not stats['is_loaded']:
            await callback.send(
                "❌ База знаний не загружена. Обратитесь к администратору.",
                keyboard=main_menu_keyboard(current_course)
            )
            cursor.clear()
            return
        
        text = get_text_to_final_test_block_7()
        
        #await callback.send(text)
        await callback.send(text, keyboard=final_test_kb())
        cursor.change_state(TrainingStates.block7_questions)
        await save_cursor(callback.user_id, extra_data = {'payload': 'to_final_test', 'state_name': TrainingStates.block7_questions, 'current_course': current_course})
        
    except Exception as e:
        logger.error(f"[continue_after_block7_handler] Произошла ошибка {e}")
        
'''
@router.on_button_callback(state(TrainingStates.block7_questions), lambda data: data.payload == 'to_final_test')
async def start_block7_final_test_handler(callback: Callback, cursor: FSMCursor):
    """Переход к финальному тесту по Блоку №7"""
    try:
        logger.info(f"[INFO][start_block7_final_test_handler] Стартовал")
        #text = get_text_start_final_test_block_6()
        
        data = cursor.get_data()
        data.update(current_question=0)
        cursor.change_data(data)
        #await callback.send(text, keyboard=final_test_kb())
        cursor.change_state(TrainingStates.block_7_final_testing)
           
    
    except Exception as e:
        logger.error(f"[ERROR][start_block7_final_test_handler] Произошла ошибка {e}")
'''        

@router.on_message(state(TrainingStates.block7_questions))
async def answer_block7_question_handler(message: Message, cursor: FSMCursor):
    """Ответы на вопросы по Блоку 7 через RAG + Claude"""
    try:
        logger.info(f"[INFO][answer_block7_question_handler] Стартовал")
        cursor_redis_data = await load_cursor(message.user_id)
        del cursor_redis_data['state_name']
        await save_cursor(message.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)     
        # Показываем процесс
        thinking_msg = await message.send("🔍 Ищу информацию в базе знаний...")
        
        state = cursor.get_state() # изменил 12.07.26 !!!!!
        state_name = state.state if all([state, not isinstance(state, str)]) else state
        logger.info(f'{state_name=}')
        
        rag = RAGService()
        answer = await rag.answer_question(message.body.text)
        
        await thinking_msg.delete() 
        
        # Форматируем ответ
        logger.info(f"[INFO][answer_block7_question_handler] Форматируем ответ") 
        response_text = (
            f"💡 **Ответ по Блоку №7:**\n\n"
            f"{answer}\n\n"
            "➡️ Задайте следующий вопрос или нажмите 🚀 **Начать тест**"
        )
              
        await message.send(response_text, keyboard=final_test_kb(), format='markdown')
        cursor.change_state(state_name)
        await save_cursor(message.user_id, extra_data = {**cursor_redis_data, 'state_name': state_name}) 
                
    
    except Exception as e:
        await thinking_msg.delete()
        logger.error(f"[ERROR][answer_block7_question_handler] Произошла ошибка {e}")   

        await message.send(
            "❌ Произошла ошибка при обработке вопроса.\n\n"
            "Попробуйте задать вопрос ещё раз или обратитесь к администратору.",
            keyboard=final_start_test_kb()
        )
    finally:
        await remove_repeat_flag(message.user_id)
        

@router.on_message(state(TrainingStates.block_7_final_testing))
async def block7_final_testing_handler(message: Message, cursor: FSMCursor):
    """Ответы на вопросы по Блоку 7 через RAG + Claude"""
    try:
        logger.info(f"[INFO][block7_final_testing_handler] Стартовал")   
        
        await asyncio.sleep(2)
        await send_question_step_12(message, cursor, 'section_42')
        return
        
    except Exception as e:
        #await thinking_msg.delete()
        logger.error(f"[ERROR][block7_final_testing_handler] Произошла ошибка {e}")   

        await message.send(
            "❌ Произошла ошибка при обработке вопроса.\n\n"
            "Попробуйте задать вопрос ещё раз или обратитесь к администратору.",
            keyboard=final_start_test_kb()
        )                                 


# ============================================================================
# ШАГ № __: ФИНАЛЬНОЕ ТЕСТИРОВАНИЕ ПО ВСЕМУ КУРСУ (20 закрытых + 10 открытых)
# ============================================================================


@router.on_button_callback(state(TrainingStates.block7_questions), lambda data: data.payload == 'start_final_test')
async def start_testing_block7_handler(callback: Callback, cursor: FSMCursor):
    """ШАГ № __ - Запуск финального тестирования по итогам обучения"""
    try:
        logger.info(f"[INFO][start_testing_block7_handler] Стартовал")
        await del_value_from_redis(callback.user_id, 'payload')
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        cursor.change_state(TrainingStates.block_7_final_testing)
        
        # ЧАСТЬ 1: Закрытые вопросы (10 вопросов с вариантами A/B/C/D)
        closed_questions = get_final_test_block_7('close') 
        
        # ЧАСТЬ 2: Открытые вопросы (5 вопросов с эталонными ответами)
        open_questions = get_final_test_block_7('open')
        
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        logger.info(f'{current_course=}')
        
        data = cursor.get_data()
        logger.info(f'[start_testing_block7_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(
                closed_questions=closed_questions,
                open_questions=open_questions,
                current_question=0,
                closed_answers=[],  # Ответы на закрытые вопросы
                open_answers=[],    # Ответы на открытые вопросы
                test_stage="closed",  # Начинаем с закрытых вопросов
                migration_state = "block_7_final_testing",
                current_course = current_course
                )
            await save_cursor(callback.user_id, extra_data = dict(
                closed_questions=closed_questions,
                open_questions=open_questions,
                current_question=0,
                closed_answers=[],  # Ответы на закрытые вопросы
                open_answers=[],    # Ответы на открытые вопросы
                test_stage="closed",  # Начинаем с закрытых вопросов
                migration_state = "block_7_final_testing",
                current_course = current_course
            ))
        else:
            data = dict()
            data.update(
                closed_questions=closed_questions,
                open_questions=open_questions,
                current_question=0,
                closed_answers=[],  # Ответы на закрытые вопросы
                open_answers=[],    # Ответы на открытые вопросы
                test_stage="closed",  # Начинаем с закрытых вопросов
                migration_state = "block_7_final_testing",
                current_course = current_course
                )
            await save_cursor(callback.user_id, extra_data = dict(
                closed_questions=closed_questions,
                open_questions=open_questions,
                current_question=0,
                closed_answers=[],  # Ответы на закрытые вопросы
                open_answers=[],    # Ответы на открытые вопросы
                test_stage="closed",  # Начинаем с закрытых вопросов
                migration_state = "block_7_final_testing",
                current_course = current_course
            ))
            
        logger.info(f'[start_testing_block7_handler] после добавления вопросов в state: {data=}')  
        cursor.change_data(data)  # !!!!!!!!!!
        # Отправляем первый закрытый вопрос
        logger.info(f'[start_testing_block7_handler] Отправляем первый закрытый вопрос')
        
        await send_question_step_12(callback, cursor, "section_42")
        
        cursor.change_state(TrainingStates.block_7_final_testing)
        await save_cursor(callback.user_id, extra_data = {'final_block_7_flag': True, 'state_name': TrainingStates.block_7_final_testing, 'payload': 'start_final_test'})
        

    except Exception as e:
        logger.error(f"[ERROR][start_testing_block7_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 

        
#################################################        
   

@router.on_button_callback(state(AnotherEmployerStates.user_type), lambda data: data.payload == 'another_emp')
async def another_employer_training_handler(callback: Callback, cursor: FSMCursor):
    """Обработчик нажатия на кнопку 📚 Обучение по продукту"""
    try:
        state = cursor.get_state() # изменил 12.07.26 !!!!!
        state_name = state.state if all([state, not isinstance(state, str)]) else state
        logger.info(f'{state_name=}')
        await callback.message.delete()
        #await callback.send(text)
        
        logger.info("Cтартовал обработчик нажатия кнопки 📚 Обучение по продукту")
        logger.info(f"[another_employer_training_handler] Определяем прогресс пользователя в обучении")
        
        current_course = get_current_course(cursor)
        game = GamificationService(current_course)
        user_id = callback.user_id
        
        cursor_data = cursor.get_data()
        status_user = cursor_data.get('status_user')
        logger.info(f'{status_user=}')

        
        current_course = get_current_course(cursor)
        logger.info(f'{current_course=}')
               
        #lessons_completed = game.get_lessons_completed(user_id) if current_course != "Другой сотрудник" else game.get_lessons_completed(user_id, "Другой сотрудник") # !!!!!!!!!!!!!!!
        lessons_completed = game.get_lessons_completed(user_id) if current_course not in ["Другой сотрудник", "Обучение по продукту"] else game.get_lessons_completed(user_id, "Обучение по продукту")
        #lessons_completed = game.get_lessons_completed(user_id)
        #lessons_completed = None
        
        if not lessons_completed:
            if status_user == 'upper_qualification':
                await show_course_intro_handler(callback, cursor)
                return
            await flow_another_emp_training_intro(
                lambda text, with_keyboard=None: send(callback, text, with_keyboard)
                )
            return
                
        return
    except Exception as e:
        logger.error(f'Произошла ошибка {e}')    
        

@router.on_button_callback(state(LawyerStates.user_type), lambda data: data.payload == 'lawyer_educ')
async def lawyer_training_handler(callback: Callback, cursor: FSMCursor):
    """Обработчик нажатия на кнопку 📚 Обучение для юриста"""
    try:
        state = cursor.get_state() # изменил 12.07.26 !!!!!
        state_name = state.state if all([state, not isinstance(state, str)]) else state
        logger.info(f'{state_name=}')
        await callback.message.delete()
        #await callback.send(text)
        
        logger.info("Cтартовал обработчик нажатия кнопки 📚 Обучение для юриста")
        logger.info(f"[lawyer_training_handler] Определяем прогресс пользователя в обучении")
        
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        logger.info(f'{current_course=}')
        game = GamificationService(current_course)
        user_id = callback.user_id
        
        cursor_data = cursor.get_data()
        status_user = cursor_data.get('status_user') if cursor_data else await get_value_from_redis(callback.user_id, 'status_user')
        logger.info(f'{status_user=}')

                   
        #lessons_completed = game.get_lessons_completed(user_id) if current_course != "Другой сотрудник" else game.get_lessons_completed(user_id, "Другой сотрудник")
        lessons_completed = game.get_lessons_completed(user_id, current_course)
        #lessons_completed = None
        
        if not lessons_completed:
            if status_user == 'upper_qualification':
                await show_course_intro_handler(callback, cursor)
                return
            #await save_cursor(callback.user_id, extra_data={'payload': 'next_education'})
            await flow_lawyer_training_intro(
                lambda text, with_keyboard=None: send(callback, text, with_keyboard),
                user_id = callback.user_id
                )
            return
                
        return
    except Exception as e:
        logger.error(f'Произошла ошибка {e}')    
        


@router.on_button_callback(lambda data: data.payload == 'education')
async def flow_sales_training_handler(callback: Callback, cursor: FSMCursor):
    """Обработчик нажатия на кнопку 📚 Обучение по продажам или ДРУГОГО НАЗВАНИЯ ОБУЧЕНИЯ"""
    try:
        logger.info('Стартовал')
        state = cursor.get_state() # изменил 12.07.26 !!!!!
        state_name = state.state if all([state, not isinstance(state, str)]) else state
        logger.info(f'{state_name=} {cursor=}')
        current_course = None
        
        
        cursor_data = cursor.get_data()
        if not cursor_data:
            logger.warning('Возможно сервер перезагрузили, определим state_name и status_user из Redis')
            state_name = await get_value_from_redis(callback.user_id, 'state_name')
            status_user = await get_value_from_redis(callback.user_id, 'status_user')
            current_course = await get_value_from_redis(callback.user_id, 'current_course')
            logger.info(f'{state_name=} {status_user=} {current_course=}')
        else:
            status_user = cursor_data.get('status_user')
            logger.info(f'{status_user=}')
        
        if not current_course:
            current_course = get_current_course(cursor)
        
        if current_course == 'Другой сотрудник':
            current_course = 'Обучение по продукту'
        
        game = GamificationService(current_course)
        user_id = callback.user_id

                       
        #lessons_completed = game.get_lessons_completed(user_id) if current_course != "Другой сотрудник" else game.get_lessons_completed(user_id, "Другой сотрудник")
        
        lessons_completed = game.get_lessons_completed(user_id, current_course)
        
        logger.info(f'{lessons_completed=}')
        
        full_completed_lessons, current_persent = game.get_full_completed_lessons(course_name = current_course, user_id = user_id)
        
        full_block = 1
                
        if not lessons_completed:
            if current_course == 'Обучение по продажам':
                if status_user == 'upper_qualification':
                    await show_course_intro_handler(callback, cursor)
                    return
                await flow_sales_training_intro(
                    lambda text, with_keyboard=None: send(callback, text, with_keyboard)
                    )
            elif current_course in ['Другой сотрудник', 'Обучение по продукту']:
                if status_user == 'upper_qualification':
                    await show_course_intro_handler(callback, cursor)
                    return
                await flow_another_emp_training_intro(
                    lambda text, with_keyboard=None: send(callback, text, with_keyboard)
                    )
            elif current_course == 'Обучение для юриста':
                if status_user == 'upper_qualification':
                    await show_course_intro_handler(callback, cursor)
                    return
                #await save_cursor(callback.user_id, extra_data={'payload': 'next_education'})
                await flow_lawyer_training_intro(
                    lambda text, with_keyboard=None: send(callback, text, with_keyboard),
                    user_id = callback.user_id
                    )
            elif current_course == 'Обучение для конструкторов':
                if status_user == 'upper_qualification':
                    await show_course_intro_handler(callback, cursor)
                    return
                await flow_branch_kb_training_intro(
                    lambda text, with_keyboard=None: send(callback, text, with_keyboard),
                    user_id = callback.user_id
                    )
            return
        
        elif lessons_completed < 7 and current_course in ['Другой сотрудник', 'Обучение по продукту']:
            logger.info(f"[flow_sales_training_handler] Обучение по курсу ДРУГОЙ СОТРУДНИК не завершено")
            data = game._load_data()
            logger.info(f'{data=}')
            full_block = lessons_completed
            
        elif lessons_completed < 12 and current_course == 'Обучение для юриста':
            logger.info(f"[flow_sales_training_handler] Обучение по курсу ОБУЧЕНИЕ ДЛЯ ЮРИСТА не завершено")
            data = game._load_data()
            logger.info(f'{data=}')
            
        
        elif lessons_completed < 7:
            logger.info(f"[flow_sales_training_handler] Обучение по блоку № 1 не завершено")
            full_block = 1
            
                                  
        elif lessons_completed < 12:
            logger.info(f"[flow_sales_training_handler] Обучение по блоку № 2 не завершено")
            full_block = 2
            
            
        elif lessons_completed < 19:
            logger.info(f"[flow_sales_training_handler] Обучение по блоку № 3 не завершено")
            full_block = 3
            
        elif lessons_completed < 24:
            logger.info(f"[flow_sales_training_handler] Обучение по блоку № 4 не завершено")
            full_block = 4
            
        elif lessons_completed < 40:
            logger.info(f"[flow_sales_training_handler] Обучение по блоку № 5 не завершено")
            full_block = 5
            
        elif lessons_completed < 42:
            logger.info(f"[flow_sales_training_handler] Обучение по блоку № 6 не завершено")
            full_block = 6
            
        elif lessons_completed < 43:
            logger.info(f"[flow_sales_training_handler] Обучение по блоку № 7 не завершено")
            full_block = 7
            
        await save_cursor(callback.user_id, extra_data={'full_block_id': full_block})
                     
        all_blocks_count = 7
        
        if current_course == "Обучение по продажам":
            text = (
                f"Вы уже приступили к обучению и в настоящий момент полностью прошли **{full_block - 1} из 7** блоков обучения\n"
                " Вы можете 📚 **Продолжить обучение** \n либо попытаться ⬆️ **Улучшить результат**, нажав на соответствующие  кнопки ниже 👇"
                ) 
        
        else:
            if current_course == 'Обучение для юриста':
                all_blocks_count = 5# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                            
                text = (
                    f"Вы уже приступили к обучению и в настоящий момент полностью прошли **{int(full_completed_lessons/2)} из {all_blocks_count}** этапов обучения\n"
                    " Вы можете 📚 **Продолжить обучение** \n либо попытаться ⬆️ **Улучшить результат**, нажав на соответствующие  кнопки ниже 👇"
                    )
            
                if lessons_completed == 10:
                    text = (
                        f"Вы уже приступили к обучению и в настоящий момент полностью прошли **{int(full_completed_lessons/2)} из {all_blocks_count}** этапов обучения\n"
                        "Вам осталось пройти **финальное тестирование** по программе обучения\n"
                        " Вы можете 📚 **Продолжить обучение** \n либо попытаться ⬆️ **Улучшить результат**, нажав на соответствующие  кнопки ниже 👇"
                        )
            else:
                text = (
                    f"Вы уже приступили к обучению и в настоящий момент полностью прошли **{lessons_completed} из {all_blocks_count}** этапов обучения\n"
                    " Вы можете 📚 **Продолжить обучение** \n либо попытаться ⬆️ **Улучшить результат**, нажав на соответствующие  кнопки ниже 👇"
                    )       
        
        
        
        if lessons_completed == 43 and current_course == 'Обучение по продажам':
            logger.info(f"[flow_sales_training_handler] Обучение ранее было завершено")
            full_block = 8
            text = (
            f"Вы ранее уже полностью прошли **все 7** блоков обучения\n"
            " Вы можете попытаться ⬆️ **Улучшить результат**, нажав на соответствующую  кнопку ниже 👇\n"
            "либо вернуться в 🏠 **Главное меню**"
            )
            await callback.message.delete()
            await callback.send(text, keyboard=finish_studying_kb())
            return
        
        elif lessons_completed == 7 and current_course in ['Другой сотрудник', 'Обучение по продукту']:
            logger.info(f"[flow_sales_training_handler] Обучение по курсу ДРУГОЙ СОТРУДНИК ранее было завершено")
            full_block = 7
            await save_cursor(callback.user_id, extra_data={'full_block_id': full_block})
            text = (
            f"Вы ранее уже полностью прошли курс обучения **ДРУГОЙ СОТРУДНИК**\n"
            " Вы можете попытаться ⬆️ **Улучшить результат**, нажав на соответствующую  кнопку ниже 👇\n"
            "либо вернуться в 🏠 **Главное меню**"
            )
            await callback.message.delete()
            await callback.send(text, keyboard=finish_studying_kb())
            return
        
        elif lessons_completed == 12 and current_course == 'Обучение для юриста':
            logger.info(f"[flow_sales_training_handler] Обучение по курсу ОБУЧЕНИЕ ДЛЯ ЮРИСТА ранее было завершено")
            full_block = 12
            text = (
            f"Вы ранее уже полностью прошли курс обучения **ОБУЧЕНИЕ ДЛЯ ЮРИСТА**\n"
            " Вы можете попытаться ⬆️ **Улучшить результат**, нажав на соответствующую  кнопку ниже 👇\n"
            "либо вернуться в 🏠 **Главное меню**"
            )
            await callback.message.delete()
            await callback.send(text, keyboard=finish_studying_kb())
            return
        
        await callback.message.delete()
        if current_course == "Обучение по продажам":
            await save_cursor(callback.user_id, extra_data = {'full_block_id': full_block})
            await callback.send(text, keyboard=continue_studying_kb(full_block))
        elif current_course in ["Другой сотрудник", "Обучение по продукту"]:
            await save_cursor(callback.user_id, extra_data = {'full_block_id': full_block})
            await callback.send(text, keyboard=continue_studying_kb(full_completed_lessons))
        elif current_course == "Обучение для юриста":
            await save_cursor(callback.user_id, extra_data = {'full_block_id': full_completed_lessons/2})
            await callback.send(text, keyboard=continue_studying_kb(int(full_completed_lessons/2)))
        
        return
    except Exception as e:
        logger.error(f'Произошла ошибка {e}')    
        
from services.debounce import debounce_button_max   


   
@router.on_button_callback(lambda data: data.payload == "next_education")
async def next_education_handler(callback: Callback, cursor: FSMCursor):
    """Обработчик нажатия на кнопку 📚 Продолжить обучение
    ШАГ 2 - Видео от директора"""
    try:
        logger.info(f"[next_education_handler] Стартовал")
        await del_value_from_redis(callback.user_id, 'payload')        
        await callback.message.delete()
        
        if await debounce_button_max(callback, cursor):
            logger.info(f"[next_education_handler] Идет обработка нажмите позднее")
            return
        
        text = get_first_day_congrats_text()
        await callback.send(text)

        await asyncio.sleep(5) # 15
        
        kb = KeyboardBuilder().add(CallbackButton(text="📚 Продолжить обучение", payload="next_education::not_first"))
            

        cursor.change_state(TrainingStates.step_2_video)
        await save_cursor(callback.user_id, extra_data={"payload": "next_education::not_first", "state_name": TrainingStates.step_2_video})
        
        await callback.send(
            "📚 Вы можете продолжить обучение, нажав кнопку ниже 👇",
            keyboard=kb
        )
                
    except Exception as e:
        logger.error(f"[next_education_handler] Произошла ошибка {e}")         
        

@router.on_button_callback(lambda data: data.payload.split('::')[0] == "continue_studying")
async def continue_studying_handler(callback: Callback, cursor: FSMCursor):
    """Обработчик нажатия на кнопку 📚 Продолжить обучение для реализации возможности
    продолжить с блока, следующего за полностью завершенным"""
    try:
        logger.info(f"[continue_studying_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        cursor_data = cursor.get_data()
        logger.info(f'{cursor_data=}')
        if not cursor_data:
            logger.info('Кажется сервер был перезагружен, попробуем взять current_course и full_block_id из Redis')
            current_course = await get_value_from_redis(callback.user_id, 'current_course')
            full_block_id = await get_value_from_redis(callback.user_id, 'full_block_id')
            full_block_id = str(int(full_block_id))
        else:
            current_course = get_current_course(cursor)
            logger.info(f'{current_course=}')
            full_block_id = callback.payload.split("::")[1]
            logger.info(f"[continue_studying_handler] {full_block_id=}")
        if current_course == "Обучение по продажам":
            if full_block_id == '1':
                cursor.change_state(TrainingStates.step_2_video)
                await training_step_3_handler(callback, cursor)
            elif full_block_id == '2':
                cursor.change_state(TrainingStates.step_12_testing)
                await start_block_2_handler(callback, cursor, True)
            elif full_block_id == '3':
                cursor.change_state(TrainingStates.block_2_final_testing)
                await start_block_3_handler(callback, cursor, True)
            elif full_block_id == '4':
                cursor.change_state(TrainingStates.block_3_final_testing)
                await start_block_4_handler(callback, cursor, True)
            elif full_block_id == '5':
                cursor.change_state(TrainingStates.block_4_final_testing)
                await start_block_5_handler(callback, cursor, True)
            elif full_block_id == '6':
                cursor.change_state(TrainingStates.block_5_final_testing)
                await start_block_6_section_1_handler(callback, cursor, True)
            elif full_block_id == '7':
                cursor.change_state(TrainingStates.block_6_final_testing)
                await start_block_7_handler(callback, cursor, True)
        elif current_course in ["Другой сотрудник", "Обучение по продукту"]:
            if current_course == 'Другой сотрудник':
                сursor_data = cursor.get_data()
                if cursor_data:
                    cursor_data['current_course'] = "Обучение по продукту"
                    cursor.change_data(cursor_data)
                    logger.info("Принудительно поменяли название курса на ОБУЧЕНИЕ ПО ПРОДУКТУ")
            if full_block_id == '1':
                cursor.change_state(TrainingStates.step_6_next)
                await training_step_6_handler(callback, cursor)
            elif full_block_id == '2':
                cursor.change_state(TrainingStates.step_8_next)
                await training_step_8_handler(callback, cursor)
            elif full_block_id == '3':
                cursor.change_state(TrainingStates.step_9_next)
                await training_step_9_handler(callback, cursor)
            elif full_block_id == '4':
                cursor.change_state(TrainingStates.step_10_next)
                await training_step_10_handler(callback, cursor)
            elif full_block_id == '5':
                cursor.change_state(TrainingStates.step_11_next)
                await training_step_11_handler(callback, cursor)
            elif full_block_id == '6':
                cursor.change_state(TrainingStates.step_11_next)
                await continue_after_section6_handler(callback, cursor)
        elif current_course == 'Обучение для юриста':
            if full_block_id == '1':
                cursor.change_state(TrainingStates.lawyer['block_2_start'])
                await lawyer_start_block_2_handler(callback, cursor)
            elif full_block_id == '2':
                cursor.change_state(TrainingStates.lawyer['block_3_start'])
                await lawyer_start_block_3_handler(callback, cursor)
            elif full_block_id == '3':
                cursor.change_state(TrainingStates.lawyer['block_4_start'])
                await lawyer_start_block_4_handler(callback, cursor)
            elif full_block_id == '4':
                cursor.change_state(TrainingStates.lawyer['block_5_start'])
                await lawyer_start_block_5_handler(callback, cursor)
            elif full_block_id == '5':
                cursor.change_state(TrainingStates.lawyer['final_test_start'])
                await lawyer_start_final_test_handler(callback, cursor)
        elif current_course == 'Регулярный менеджмент':
            if str(full_block_id) == '1':
                await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.regular_managment['message_5']})
                cursor.change_state(state(TrainingStates.regular_managment['message_5']))
            elif str(full_block_id) == '2':
                await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.regular_managment['message_8']})
                cursor.change_state(state(TrainingStates.regular_managment['message_8']))
            elif str(full_block_id) == '3':
                await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.regular_managment['message_11']})
                cursor.change_state(state(TrainingStates.regular_managment['message_11']))
            elif str(full_block_id) == '4':
                await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.regular_managment['message_14']})
                cursor.change_state(state(TrainingStates.regular_managment['message_14']))
            elif str(full_block_id) == '5':
                await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.regular_managment['message_17']})
                cursor.change_state(state(TrainingStates.regular_managment['message_17']))
            elif str(full_block_id) == '6':
                await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.regular_managment['message_20']})
                cursor.change_state(state(TrainingStates.regular_managment['message_20']))
            elif str(full_block_id) == '7':
                await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.regular_managment['message_23']})
                cursor.change_state(state(TrainingStates.regular_managment['message_23']))
            elif str(full_block_id) == '8':
                await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.regular_managment['message_26']})
                cursor.change_state(state(TrainingStates.regular_managment['message_26']))
            elif str(full_block_id) == '9':
                await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.regular_managment['message_29']})
                cursor.change_state(state(TrainingStates.regular_managment['message_29']))
            
            await regular_managment_message_2_handler(callback, cursor)
                
                
            
    except Exception as e:
        logger.error(f"[continue_studying_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)
          
            

@router.on_button_callback(lambda data: data.payload == "start_again")
async def high_result_handler(callback: Callback, cursor: FSMCursor):
    """Обработчик нажатия на кнопку "⬆️ Улучшить результат"""
    try:
        logger.info(f"[high_result_handler] Стартовал")
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        logger.info(f'{current_course=}')
        game = GamificationService(current_course)
        game.reset_user_course_progress(callback.user_id, current_course)
        if current_course == 'Обучение по продажам':
            await training_step_3_handler(callback, cursor, True)
        elif current_course in ['Другой сотрудник', 'Обучение по продукту']:
            await del_value_from_redis(callback.user_id, 'full_block_id_')
            await training_step_3_handler(callback, cursor, True)
        elif current_course == 'Обучение для юриста':
            await lawyer_training_step_3_handler(callback, cursor, True)
        elif current_course == 'Регулярный менеджмент':
            cursor.change_state(TrainingStates.regular_managment['message_2'])
            await regular_managment_message_2_handler(callback, cursor)
            
            
            
    except Exception as e:
        logger.error(f"[high_result_handler] Произошла ошибка {e}")  
        


@router.on_button_callback(lambda data: data.payload.startswith("change_department::"))
async def change_department_handler(callback: Callback, cursor: FSMCursor):
    """Обработчик нажатия на кнопки с названиями курсов обучения"""
    try:
        logger.info('Стартовал')
        await callback.message.delete()
        cursor_data = cursor.get_data()
        logger.info(f'{cursor_data=}')
        if not cursor_data:
            logger.warning('Возможно отсутствует cursor - обращаемся к Redis')
            cursor_redis_data = await load_cursor(callback.user_id)
            logger.info(f'{cursor_redis_data=}')
            redis_data = cursor_redis_data.get("data", {})
            status_user = redis_data.get("status_user")
        else:
            status_user = cursor_data.get('status_user')
        logger.info(f'{status_user=}')
        
        payload_data = callback.payload
        department_name = payload_data.split('::')[1]
        logger.info(f'{department_name=}')
        if department_name == 'in_process':
            text = get_text_in_process()
            kb = change_another_department_kb()
            await callback.send(text, keyboard = kb)
            return
        elif department_name == 'manager':
            cursor.clear_state()
            new_cursor = cursor.get_data() if cursor.get_data() else {}
            new_cursor.update(current_course="Обучение по продажам", status_user=status_user)
            cursor.change_data(new_cursor) #if new_cursor else cursor.change_data({"status_user": status_user})
            extra_data = new_cursor if new_cursor else {"status_user": status_user, "current_course":"Обучение по продажам"}
            await save_cursor(callback.user_id, extra_data=extra_data)
            logger.info(f'Курсор после изменения: {cursor.get_state()} \n{new_cursor}')
            status_user = new_cursor.get('status_user') if new_cursor else status_user
            logger.info(f'{status_user=}')
            if status_user == 'new_employer':
                await sales_manager_start_handl(callback, cursor)
            else:
                logger.info(f'{status_user=}')
                cursor.change_data({"current_course": "Обучение по продажам", "status_user": status_user})
                await save_cursor(callback.user_id, extra_data={"current_course": "Обучение по продажам", "status_user": status_user})
                await start_command(callback, cursor, status_user)
                #await sales_manager_start_handl(callback, cursor, status_user='upper_qualification')
            
        elif department_name == 'lawyer':
            logger.info('Ветка ЮРИСТ')
            cursor.clear_state()
            new_cursor = cursor.get_data() if cursor.get_data() else {}
            new_cursor.update(current_course="Обучение для юриста", status_user=status_user)
            cursor.change_data(new_cursor) #if new_cursor else cursor.change_data({"status_user": status_user, "current_course":"Обучение для юриста" })
            extra_data = new_cursor if new_cursor else {"status_user": status_user, "current_course":"Обучение для юриста" }
            await save_cursor(callback.user_id, extra_data=extra_data)
            logger.info(f'Курсор после изменения: {cursor.get_state()} \n{new_cursor}')
            status_user = new_cursor.get('status_user') if new_cursor else status_user
            logger.info(f'{status_user=}')
            if not status_user:
                logger.warning('была перезагрузка сервера, определим status_user из Redis')
                status_user = await get_value_from_redis(callback.user_id, 'status_user')
            if status_user == 'new_employer':
                await lawyer_start_handl(callback, cursor)
            else:
                logger.info(f'5636 {status_user=}')
                cursor.change_data({"current_course": "Обучение для юриста", "status_user": status_user})
                await save_cursor(callback.user_id, extra_data={"current_course": "Обучение для юриста", "status_user": status_user})
                await start_command(callback, cursor, status_user)
        elif department_name == 'konstructor':
            logger.info('Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ')
            cursor.clear_state()
            new_cursor = cursor.get_data() if cursor.get_data() else {}
            new_cursor.update(current_course="Обучение для конструкторов", status_user=status_user)
            cursor.change_data(new_cursor) #if new_cursor else cursor.change_data({"status_user": status_user, "current_course":"Обучение для конструкторов" })
            extra_data = new_cursor if new_cursor else {"status_user": status_user, "current_course":"Обучение для юриста" }
            await save_cursor(callback.user_id, extra_data=extra_data)
            logger.info(f'Курсор после изменения: {cursor.get_state()} \n{new_cursor}')
            status_user = new_cursor.get('status_user') if new_cursor else status_user
            logger.info(f'{status_user=}')
            if not status_user:
                logger.warning('была перезагрузка сервера, определим status_user из Redis')
                status_user = await get_value_from_redis(callback.user_id, 'status_user')
            if status_user == 'new_employer':
                await branch_kb_start_handl(callback, cursor)
            
                
            
        
    except Exception as e:
        logger.error(f"[change_department_handler] Произошла ошибка {e}")
        
        
@router.on_button_callback(lambda data: data.payload == 'another_department')
async def another_department_handler(callback: Callback, cursor: FSMCursor):
    """Обработчик нажатия на кнопку ВЫБРАТЬ ДРУГОЙ ОТДЕЛ"""
    try:
        await callback.message.delete()
        logger.info('Стартовал')
        text = get_text_change_department()
        kb = change_department_kb()
        await callback.send(text, keyboard = kb)
    except Exception as e:
        logger.error(f'Произошла ошибка: {e}')


# ========================  СПЕЦИФИЧЕСКИЕ ХЭНДЛЕРЫ ДЛЯ ВЕТКИ ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ =======================
@router.on_button_callback(state(TrainingStates.konstructor['module_0']), lambda data: data.payload.split('::')[1] == "not_first")
async def kb_module_0_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ - Модуль №0: «Онбординг и экосистема КБ»"""
    try:
        logger.info("[kb_module_0_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2) 
        if continue_flag:
            intro_text = get_module0_intro_text_kb_branch()
            await callback.send(intro_text)
            await asyncio.sleep(2) # 10
        
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
        
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_3_handler] Идет обработка нажмите позднее")
        #     return      
        await callback.message.delete()
        intro_text = get_module0_intro_text_kb_branch()
        await callback.send(intro_text)
        
        await asyncio.sleep(2) # 15
        
        kb = KeyboardBuilder().add(CallbackButton(text="📚 Продолжить обучение", payload="next_education::not_first"))
                
        cursor.change_state(TrainingStates.konstructor['module_0_lesson_1'])
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_0_lesson_1'], 'current_course': 'Обучение для конструкторов', 'payload': 'next_education::not_first', 'status_user': status_user})
        
        await callback.send(
            "📚 Вы можете продолжить обучение, нажав кнопку ниже 👇",
            keyboard=kb
        )
    
    except Exception as e:
        logger.error(f"[kb_module_0_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 
        

@router.on_button_callback(state(TrainingStates.konstructor['module_0_lesson_1']), lambda data: data.payload.split('::')[1] == "not_first")
async def kb_module_0_lesson_1_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ - Модуль №0 Урок №1: «Роль конструктора в цепочке заказа»"""
    try:
        logger.info("[kb_module_0_lesson_1_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
        
        await callback.message.delete()
        intro_text = get_module0_lesson1_intro_text_kb_branch()
        await callback.send(intro_text, disable_link_preview = True) 
        
        await asyncio.sleep(2) # 15
        
        course_name = await get_value_from_redis(callback.user_id, 'current_course')
        if not course_name:
            course_name = get_current_course(cursor)
        logger.info(f'{course_name=}')
        
        game = GamificationService(course_name)
        user_data = load_user_data()
        user_id = str(callback.user_id)
        first_name = user_data.get(user_id).get("first_name")
        last_name = user_data.get(user_id).get("second_name")
        
        await game.increment_lesson_func(
            user_id=user_id,
            course_name=course_name, # "Обучение по продажам"
            lesson_id='section_1', #  "section_1"
            user_data={
                "username": f'{first_name} {last_name}',
                "first_name": first_name,
                "last_name": last_name
            }
        )
                
        # сообщение о тестировании с кнопкой
        test_text = kb_go_to_test_after_lesson(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        cursor.change_state(TrainingStates.konstructor['module_0_lesson_1_questions'])
        await asyncio.sleep(2) # 2
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_0_lesson_1_questions'], 'payload': 'start_test', 'current_course': 'Обучение для конструкторов', 'status_user': status_user})
    except Exception as e:
        logger.error(f"[kb_module_0_lesson_1_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 
        
        
@router.on_button_callback(state(TrainingStates.konstructor['module_0_lesson_1_questions']), lambda data: data.payload == "start_test")
async def kb_module_0_lesson_1_test_handler(callback: Callback, cursor: FSMCursor):
    """ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ Начало тестирования МОДУЛЬ № 0 УРОК № 1 """
    try:
        logger.info("[kb_module_0_lesson_1_test_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}) 
        questions = get_testing_data_module_0_test_1_kb()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[kb_module_0_lesson_1_test_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
        logger.info(f'{callback=}')
        
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        else:
            await save_cursor(callback, extra_data=dict(questions=questions, current_question=0, answers=[]))
        
            
        logger.info(f'[kb_module_0_lesson_1_test_handler] после добавления вопросов в state: {data=}')  
        
        # Отправляем первый вопрос
        cursor.change_data(data)
        await send_question(callback, cursor, "section_2")
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.konstructor['module_0_lesson_1_testing']))
        else:
            await save_cursor(callback, extra_data=dict(state_name = TrainingStates.konstructor['module_0_lesson_1_testing']))
        cursor.change_state(TrainingStates.konstructor['module_0_lesson_1_testing'])
    
    except Exception as e:
        logger.error(f"[kb_module_0_lesson_1_test_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 
        

@router.on_button_callback(state(TrainingStates.konstructor['module_0_lesson_2']), lambda data: data.payload.split('::')[1] == "not_first")
async def kb_module_0_lesson_2_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ - Модуль №0 Урок №2: «Инструменты и рабочая среда»"""
    try:
        logger.info("[kb_module_0_lesson_2_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
        
        await callback.message.delete()
        intro_text = get_module0_lesson2_intro_text_kb_branch()
        await callback.send(intro_text, disable_link_preview = True) 
        
        await asyncio.sleep(2) # 15
        
        course_name = await get_value_from_redis(callback.user_id, 'current_course')
        if not course_name:
            course_name = get_current_course(cursor)
        logger.info(f'{course_name=}')
        
        game = GamificationService(course_name)
        user_data = load_user_data()
        user_id = str(callback.user_id)
        first_name = user_data.get(user_id).get("first_name")
        last_name = user_data.get(user_id).get("second_name")
        
        await game.increment_lesson_func(
            user_id=user_id,
            course_name=course_name, # "Обучение по продажам"
            lesson_id='section_3', #  "section_1"
            user_data={
                "username": f'{first_name} {last_name}',
                "first_name": first_name,
                "last_name": last_name
            }
        )
                
        # сообщение о тестировании с кнопкой
        test_text = kb_go_to_test_after_lesson(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        cursor.change_state(TrainingStates.konstructor['module_0_lesson_2_questions'])
        await asyncio.sleep(2) # 2
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_0_lesson_2_questions'], 'payload': 'start_test', 'current_course': 'Обучение для конструкторов', 'status_user': status_user})
    except Exception as e:
        logger.error(f"[kb_module_0_lesson_2_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 


@router.on_button_callback(state(TrainingStates.konstructor['module_0_lesson_2_questions']), lambda data: data.payload == "start_test")
async def kb_module_0_lesson_2_test_handler(callback: Callback, cursor: FSMCursor):
    """ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ Начало тестирования МОДУЛЬ № 0 УРОК № 2 """
    try:
        logger.info("[kb_module_0_lesson_2_test_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}) 
        questions = get_testing_data_module_0_test_2_kb()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[kb_module_0_lesson_2_test_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
        logger.info(f'{callback=}')
        
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        else:
            await save_cursor(callback, extra_data=dict(questions=questions, current_question=0, answers=[]))
        
            
        logger.info(f'[kb_module_0_lesson_2_test_handler] после добавления вопросов в state: {data=}')  
        
        # Отправляем первый вопрос
        cursor.change_data(data)
        await send_question(callback, cursor, "section_4")
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.konstructor['module_0_lesson_2_testing']))
        else:
            await save_cursor(callback, extra_data=dict(state_name = TrainingStates.konstructor['module_0_lesson_2_testing']))
        cursor.change_state(TrainingStates.konstructor['module_0_lesson_2_testing'])
    
    except Exception as e:
        logger.error(f"[kb_module_0_lesson_2_test_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)
        

@router.on_button_callback(state(TrainingStates.konstructor['module_0_lesson_3']), lambda data: data.payload.split('::')[1] == "not_first")
async def kb_module_0_lesson_3_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ - Модуль №0 Урок №3: «Типовой день конструктора»"""
    try:
        logger.info("[kb_module_0_lesson_3_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
        
        await callback.message.delete()
        intro_text = get_module0_lesson3_intro_text_kb_branch()
        await callback.send(intro_text, disable_link_preview = True) 
        
        await asyncio.sleep(2) # 15
        
        course_name = await get_value_from_redis(callback.user_id, 'current_course')
        if not course_name:
            course_name = get_current_course(cursor)
        logger.info(f'{course_name=}')
        
        game = GamificationService(course_name)
        user_data = load_user_data()
        user_id = str(callback.user_id)
        first_name = user_data.get(user_id).get("first_name")
        last_name = user_data.get(user_id).get("second_name")
        
        await game.increment_lesson_func(
            user_id=user_id,
            course_name=course_name, # "Обучение по продажам"
            lesson_id='section_5', #  "section_1"
            user_data={
                "username": f'{first_name} {last_name}',
                "first_name": first_name,
                "last_name": last_name
            }
        )
                
        # сообщение о тестировании с кнопкой
        test_text = kb_go_to_test_after_lesson(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        cursor.change_state(TrainingStates.konstructor['module_0_lesson_3_questions'])
        await asyncio.sleep(2) # 2
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_0_lesson_3_questions'], 'payload': 'start_test', 'current_course': 'Обучение для конструкторов', 'status_user': status_user})
    except Exception as e:
        logger.error(f"[kb_module_0_lesson_3_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 


@router.on_button_callback(state(TrainingStates.konstructor['module_0_lesson_3_questions']), lambda data: data.payload == "start_test")
async def kb_module_0_lesson_3_test_handler(callback: Callback, cursor: FSMCursor):
    """ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ Начало тестирования МОДУЛЬ № 0 УРОК № 3 """
    try:
        logger.info("[kb_module_0_lesson_3_test_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}) 
        questions = get_testing_data_module_0_test_3_kb()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[kb_module_0_lesson_3_test_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
        logger.info(f'{callback=}')
        
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        else:
            await save_cursor(callback, extra_data=dict(questions=questions, current_question=0, answers=[]))
        
            
        logger.info(f'[kb_module_0_lesson_3_test_handler] после добавления вопросов в state: {data=}')  
        
        # Отправляем первый вопрос
        cursor.change_data(data)
        await send_question(callback, cursor, "section_6")
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.konstructor['module_0_lesson_3_testing']))
        else:
            await save_cursor(callback, extra_data=dict(state_name = TrainingStates.konstructor['module_0_lesson_3_testing']))
        cursor.change_state(TrainingStates.konstructor['module_0_lesson_3_testing'])
    
    except Exception as e:
        logger.error(f"[kb_module_0_lesson_3_test_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)
        

@router.on_button_callback(state(TrainingStates.konstructor['module_0_lesson_4']), lambda data: data.payload.split('::')[1] == "not_first")
async def kb_module_0_lesson_4_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ - Модуль №0 Урок №4: «Типовой день конструктора»"""
    try:
        logger.info("[kb_module_0_lesson_4_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
        
        await callback.message.delete()
        intro_text = get_module0_lesson4_intro_text_kb_branch()
        await callback.send(intro_text, disable_link_preview = True) 
        
        await asyncio.sleep(2) # 15
        
        course_name = await get_value_from_redis(callback.user_id, 'current_course')
        if not course_name:
            course_name = get_current_course(cursor)
        logger.info(f'{course_name=}')
        
        game = GamificationService(course_name)
        user_data = load_user_data()
        user_id = str(callback.user_id)
        first_name = user_data.get(user_id).get("first_name")
        last_name = user_data.get(user_id).get("second_name")
        
        await game.increment_lesson_func(
            user_id=user_id,
            course_name=course_name, # "Обучение по продажам"
            lesson_id='section_7', #  "section_1"
            user_data={
                "username": f'{first_name} {last_name}',
                "first_name": first_name,
                "last_name": last_name
            }
        )
                
        # сообщение о тестировании с кнопкой
        test_text = kb_go_to_test_after_lesson(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        cursor.change_state(TrainingStates.konstructor['module_0_lesson_4_questions'])
        await asyncio.sleep(2) # 2
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_0_lesson_4_questions'], 'payload': 'start_test', 'current_course': 'Обучение для конструкторов', 'status_user': status_user})
    except Exception as e:
        logger.error(f"[kb_module_0_lesson_4_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 


@router.on_button_callback(state(TrainingStates.konstructor['module_0_lesson_4_questions']), lambda data: data.payload == "start_test")
async def kb_module_0_lesson_4_test_handler(callback: Callback, cursor: FSMCursor):
    """ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ Начало тестирования МОДУЛЬ № 0 УРОК № 4 """
    try:
        logger.info("[kb_module_0_lesson_4_test_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}) 
        questions = get_testing_data_module_0_test_4_kb()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[kb_module_0_lesson_4_test_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
        logger.info(f'{callback=}')
        
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        else:
            await save_cursor(callback, extra_data=dict(questions=questions, current_question=0, answers=[]))
        
            
        logger.info(f'[kb_module_0_lesson_4_test_handler] после добавления вопросов в state: {data=}')  
        
        # Отправляем первый вопрос
        cursor.change_data(data)
        await send_question(callback, cursor, "section_8")
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.konstructor['module_0_lesson_4_testing']))
        else:
            await save_cursor(callback, extra_data=dict(state_name = TrainingStates.konstructor['module_0_lesson_4_testing']))
        cursor.change_state(TrainingStates.konstructor['module_0_lesson_4_testing'])
    
    except Exception as e:
        logger.error(f"[kb_module_0_lesson_4_test_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)
        

@router.on_button_callback(state(TrainingStates.konstructor['module_0_lesson_5']), lambda data: data.payload.split('::')[1] == "not_first")
async def kb_module_0_lesson_5_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ - Модуль №0 Урок №5: Эффективное общение с клиентами и смежными участниками"""
    try:
        logger.info("[kb_module_0_lesson_5_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
        
        await callback.message.delete()
        intro_text = get_module0_lesson5_intro_text_kb_branch()
        await callback.send(intro_text, disable_link_preview = True) 
        
        await asyncio.sleep(2) # 15
        
        course_name = await get_value_from_redis(callback.user_id, 'current_course')
        if not course_name:
            course_name = get_current_course(cursor)
        logger.info(f'{course_name=}')
        
        game = GamificationService(course_name)
        user_data = load_user_data()
        user_id = str(callback.user_id)
        first_name = user_data.get(user_id).get("first_name")
        last_name = user_data.get(user_id).get("second_name")
        
        await game.increment_lesson_func(
            user_id=user_id,
            course_name=course_name, # "Обучение по продажам"
            lesson_id='section_9', #  "section_1"
            user_data={
                "username": f'{first_name} {last_name}',
                "first_name": first_name,
                "last_name": last_name
            }
        )
                
        # сообщение о тестировании с кнопкой
        test_text = kb_go_to_test_after_lesson(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        cursor.change_state(TrainingStates.konstructor['module_0_lesson_5_questions'])
        await asyncio.sleep(2) # 2
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_0_lesson_5_questions'], 'payload': 'start_test', 'current_course': 'Обучение для конструкторов', 'status_user': status_user})
    except Exception as e:
        logger.error(f"[kb_module_0_lesson_5_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 


@router.on_button_callback(state(TrainingStates.konstructor['module_0_lesson_5_questions']), lambda data: data.payload == "start_test")
async def kb_module_0_lesson_5_test_handler(callback: Callback, cursor: FSMCursor):
    """ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ Начало тестирования МОДУЛЬ № 0 УРОК № 5 """
    try:
        logger.info("[kb_module_0_lesson_5_test_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}) 
        questions = get_testing_data_module_0_test_5_kb()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[kb_module_0_lesson_5_test_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
        logger.info(f'{callback=}')
        
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        else:
            await save_cursor(callback, extra_data=dict(questions=questions, current_question=0, answers=[]))
        
            
        logger.info(f'[kb_module_0_lesson_5_test_handler] после добавления вопросов в state: {data=}')  
        
        # Отправляем первый вопрос
        cursor.change_data(data)
        await send_question(callback, cursor, "section_10")
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.konstructor['module_0_lesson_5_testing']))
        else:
            await save_cursor(callback, extra_data=dict(state_name = TrainingStates.konstructor['module_0_lesson_5_testing']))
        cursor.change_state(TrainingStates.konstructor['module_0_lesson_5_testing'])
    
    except Exception as e:
        logger.error(f"[kb_module_0_lesson_5_test_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)
        

@router.on_button_callback(state(TrainingStates.konstructor['module_0_lesson_5_testing']), lambda data: data.payload.split('::')[1] == "not_first")
async def continue_after_kb_module_0_handler(callback: Callback, cursor: FSMCursor):
    """Завершение Модуля №0 - КБ. Переход к вопросам или финальному тесту"""
    try:
        logger.info(f"[continue_after_kb_module_0_handler] Стартовал")
        await callback.message.delete()
        branch_name = ''
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        # Проверяем загрузку базы знаний
        rag = RAGService()
        
        if current_course == 'Обучение для конструкторов':
            branch_name = 'branch_kb'
        if isinstance(callback, Callback):
            await callback.message.delete()
        # Проверяем загрузку базы знаний
        await save_cursor(callback.user_id, extra_data={'branch_name': branch_name})
        rag = RAGService(branch_name=branch_name)
        stats = rag.get_stats()
                        
        if not stats['is_loaded']:
            await callback.send(
                "❌ База знаний не загружена. Обратитесь к администратору.",
                keyboard=main_menu_keyboard(current_course)
            )
            cursor.clear()
            return
        
        text = kb_get_text_to_final_test_module_0()
        logger.info('Должны отправить текст')        
        await callback.send(text=text, keyboard=final_start_test_kb())
        cursor.change_state(TrainingStates.konstructor['module_0_questions'])
        await save_cursor(callback.user_id, extra_data = {'payload': 'to_final_test', 'state_name': TrainingStates.konstructor['module_0_questions'], 'current_course': current_course})
        logger.info('Завершение работы метода')
        return 
        
    except Exception as e:
        logger.error(f"[continue_after_kb_module_0_handler] Произошла ошибка {e}")


@router.on_message(state(TrainingStates.konstructor['module_1_final_testing']))
async def kb_module_0_final_testing_handler(message: Message, cursor: FSMCursor):
    """Ответы на вопросы по модулю № 0 (KB) через RAG + Claude"""
    try:
        logger.info(f"[INFO][kb_module_0_final_testing_handler] Стартовал")           #await thinking_msg.delete() 
        await asyncio.sleep(2)
        await send_question_step_12(message, cursor, 'section_12')
        return
        
    except Exception as e:
        #await thinking_msg.delete()
        logger.error(f"[ERROR][kb_module_0_final_testing_handler] Произошла ошибка {e}")   

        await message.send(
            "❌ Произошла ошибка при обработке вопроса.\n\n"
            "Попробуйте задать вопрос ещё раз или обратитесь к администратору.",
            keyboard=final_start_test_kb()
        )
        
@router.on_message(state(TrainingStates.konstructor['module_1_final_testing']))
async def kb_module_1_final_testing_handler(message: Message, cursor: FSMCursor):
    """Ответы на вопросы по модулю № 1 (KB) через RAG + Claude"""
    try:
        logger.info(f"[INFO][kb_module_1_final_testing_handler] Стартовал")           #await thinking_msg.delete() 
        await asyncio.sleep(2)
        await send_question_step_12(message, cursor, 'section_25')
        return
        
    except Exception as e:
        #await thinking_msg.delete()
        logger.error(f"[ERROR][kb_module_1_final_testing_handler] Произошла ошибка {e}")   

        await message.send(
            "❌ Произошла ошибка при обработке вопроса.\n\n"
            "Попробуйте задать вопрос ещё раз или обратитесь к администратору.",
            keyboard=final_start_test_kb()
        )
        
@router.on_message(state(TrainingStates.konstructor['module_2_final_testing']))
async def kb_module_2_final_testing_handler(message: Message, cursor: FSMCursor):
    """Ответы на вопросы по модулю № 2 (KB) через RAG + Claude"""
    try:
        logger.info(f"[INFO][kb_module_2_final_testing_handler] Стартовал")           #await thinking_msg.delete() 
        await asyncio.sleep(2)
        await send_question_step_12(message, cursor, 'section_36')
        return
        
    except Exception as e:
        #await thinking_msg.delete()
        logger.error(f"[ERROR][kb_module_2_final_testing_handler] Произошла ошибка {e}")   

        await message.send(
            "❌ Произошла ошибка при обработке вопроса.\n\n"
            "Попробуйте задать вопрос ещё раз или обратитесь к администратору.",
            keyboard=final_start_test_kb()
        ) 


@router.on_message(state(TrainingStates.konstructor['module_3_final_testing']))
async def kb_module_3_final_testing_handler(message: Message, cursor: FSMCursor):
    """Ответы на вопросы по модулю № 3 (KB) через RAG + Claude"""
    try:
        logger.info(f"[INFO][kb_module_3_final_testing_handler] Стартовал")           #await thinking_msg.delete() 
        await asyncio.sleep(2)
        await send_question_step_12(message, cursor, 'section_47')
        return
        
    except Exception as e:
        #await thinking_msg.delete()
        logger.error(f"[ERROR][kb_module_3_final_testing_handler] Произошла ошибка {e}")   

        await message.send(
            "❌ Произошла ошибка при обработке вопроса.\n\n"
            "Попробуйте задать вопрос ещё раз или обратитесь к администратору.",
            keyboard=final_start_test_kb()
        )  
        
        
@router.on_message(state(TrainingStates.konstructor['module_4_final_testing']))
async def kb_module_4_final_testing_handler(message: Message, cursor: FSMCursor):
    """Ответы на вопросы по модулю № 4 (KB) через RAG + Claude"""
    try:
        logger.info(f"[INFO][kb_module_4_final_testing_handler] Стартовал")           #await thinking_msg.delete() 
        await asyncio.sleep(2)
        await send_question_step_12(message, cursor, 'section_56')
        return
        
    except Exception as e:
        #await thinking_msg.delete()
        logger.error(f"[ERROR][kb_module_4_final_testing_handler] Произошла ошибка {e}")   

        await message.send(
            "❌ Произошла ошибка при обработке вопроса.\n\n"
            "Попробуйте задать вопрос ещё раз или обратитесь к администратору.",
            keyboard=final_start_test_kb()
        )
        
@router.on_message(state(TrainingStates.konstructor['module_5_final_testing']))
async def kb_module_5_final_testing_handler(message: Message, cursor: FSMCursor):
    """Ответы на вопросы по модулю № 5 (KB) через RAG + Claude"""
    try:
        logger.info(f"[INFO][kb_module_5_final_testing_handler] Стартовал")           #await thinking_msg.delete() 
        await asyncio.sleep(2)
        await send_question_step_12(message, cursor, 'section_65')
        return
        
    except Exception as e:
        #await thinking_msg.delete()
        logger.error(f"[ERROR][kb_module_5_final_testing_handler] Произошла ошибка {e}")   

        await message.send(
            "❌ Произошла ошибка при обработке вопроса.\n\n"
            "Попробуйте задать вопрос ещё раз или обратитесь к администратору.",
            keyboard=final_start_test_kb()
        )
        
@router.on_message(state(TrainingStates.konstructor['module_6_final_testing']))
async def kb_module_6_final_testing_handler(message: Message, cursor: FSMCursor):
    """Ответы на вопросы по модулю № 6 (KB) через RAG + Claude"""
    try:
        logger.info(f"[INFO][kb_module_6_final_testing_handler] Стартовал")           #await thinking_msg.delete() 
        await asyncio.sleep(2)
        await send_question_step_12(message, cursor, 'section_74')
        return
        
    except Exception as e:
        #await thinking_msg.delete()
        logger.error(f"[ERROR][kb_module_6_final_testing_handler] Произошла ошибка {e}")   

        await message.send(
            "❌ Произошла ошибка при обработке вопроса.\n\n"
            "Попробуйте задать вопрос ещё раз или обратитесь к администратору.",
            keyboard=final_start_test_kb()
        )  
        

@router.on_message(state(TrainingStates.konstructor['module_7_final_testing']))
async def kb_module_7_final_testing_handler(message: Message, cursor: FSMCursor):
    """Ответы на вопросы по модулю № 7 (KB) через RAG + Claude"""
    try:
        logger.info(f"[INFO][kb_module_7_final_testing_handler] Стартовал")           #await thinking_msg.delete() 
        await asyncio.sleep(2)
        await send_question_step_12(message, cursor, 'section_83')
        return
        
    except Exception as e:
        #await thinking_msg.delete()
        logger.error(f"[ERROR][kb_module_7_final_testing_handler] Произошла ошибка {e}")   

        await message.send(
            "❌ Произошла ошибка при обработке вопроса.\n\n"
            "Попробуйте задать вопрос ещё раз или обратитесь к администратору.",
            keyboard=final_start_test_kb()
        )                            



@router.on_button_callback(state(TrainingStates.konstructor['module_0_questions']), lambda data: data.payload == "to_final_test")
async def kb_module_0_final_test_handler(callback: Callback, cursor: FSMCursor):
    '''Заглушка для прохождения финального теста по модулю № 0'''
    try:
        logger.info("[kb_module_0_final_test_handler] Стартовал")
        # ЧАСТЬ 1: Закрытые вопросы (10 вопросов с вариантами A/B/C/D)
        closed_questions = get_final_testing_data_module_0_kb('close')
        logger.info(f"[INFO][kb_module_0_final_test_handler] {closed_questions=}")
        
        # ЧАСТЬ 2: Открытые вопросы (5 вопросов с эталонными ответами)
        open_questions = get_final_testing_data_module_0_kb('open')
        logger.info(f"[INFO][kb_module_0_final_test_handler] {open_questions=}")
        
        data = cursor.get_data()
        logger.info(f'[kb_module_0_final_test_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
    
        if data and isinstance(data, dict):
                data.update(
                    closed_questions=closed_questions,
                    open_questions=open_questions,
                    current_question=0,
                    closed_answers=[],  # Ответы на закрытые вопросы
                    open_answers=[],    # Ответы на открытые вопросы
                    test_stage="closed",  # Начинаем с закрытых вопросов
                    migration_state = "module_0_final_testing",
                    current_course='Обучение для конструкторов'
                    )
                await save_cursor(callback.user_id, extra_data = dict(
                    closed_questions=closed_questions,
                    open_questions=open_questions,
                    current_question=0,
                    closed_answers=[],  # Ответы на закрытые вопросы
                    open_answers=[],    # Ответы на открытые вопросы
                    test_stage="closed",  # Начинаем с закрытых вопросов
                    migration_state = "module_0_final_testing",
                    current_course='Обучение для конструкторов'
                ))
        else:
            data = dict()
            data.update(
                closed_questions=closed_questions,
                open_questions=open_questions,
                current_question=0,
                closed_answers=[],  # Ответы на закрытые вопросы
                open_answers=[],    # Ответы на открытые вопросы
                test_stage="closed",  # Начинаем с закрытых вопросов
                migration_state = "module_0_final_testing",
                current_course='Обучение для конструкторов'
                )
            await save_cursor(callback.user_id, extra_data = dict(
                    closed_questions=closed_questions,
                    open_questions=open_questions,
                    current_question=0,
                    closed_answers=[],  # Ответы на закрытые вопросы
                    open_answers=[],    # Ответы на открытые вопросы
                    test_stage="closed",  # Начинаем с закрытых вопросов
                    migration_state = "module_0_final_testing",
                    current_course='Обучение для конструкторов'
                ))
            
        logger.info(f'[kb_module_0_final_test_handler] после добавления вопросов в state: {data=}')  
        cursor.change_data(data)
        # Отправляем первый закрытый вопрос
        logger.info(f'[kb_module_0_final_test_handler] Отправляем первый закрытый вопрос')
        current_course = cursor.get_data().get('current_course')
        if not current_course:
            current_course = await get_value_from_redis(callback.user_id, 'current_course')
        else:
            current_course = get_current_course(cursor)
        logger.info(f'{current_course=}')
        await send_question_step_12(callback, cursor, "module_0_final_test", "Обучение для конструкторов")

        cursor.change_state(TrainingStates.step_12_testing)
        

    except Exception as e:
        logger.error(f"[ERROR][kb_module_0_final_test_handler] Произошла ошибка {e}")
        

@router.on_button_callback(state(TrainingStates.konstructor['module_1_questions']), lambda data: data.payload == "to_final_test")
async def kb_module_1_final_test_handler(callback: Callback, cursor: FSMCursor):
    '''Заглушка для прохождения финального теста по модулю № 1'''
    try:
        logger.info("[kb_module_1_final_test_handler] Стартовал")
        # ЧАСТЬ 1: Закрытые вопросы (10 вопросов с вариантами A/B/C/D)
        closed_questions = get_final_testing_data_module_1_kb('close')
        logger.info(f"[INFO][kb_module_1_final_test_handler] {closed_questions=}")
        
        # ЧАСТЬ 2: Открытые вопросы (5 вопросов с эталонными ответами)
        open_questions = get_final_testing_data_module_1_kb('open')
        logger.info(f"[INFO][kb_module_1_final_test_handler] {open_questions=}")
        
        data = cursor.get_data()
        logger.info(f'[kb_module_1_final_test_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
    
        if data and isinstance(data, dict):
                data.update(
                    closed_questions=closed_questions,
                    open_questions=open_questions,
                    current_question=0,
                    closed_answers=[],  # Ответы на закрытые вопросы
                    open_answers=[],    # Ответы на открытые вопросы
                    test_stage="closed",  # Начинаем с закрытых вопросов
                    migration_state = "module_1_final_testing",
                    current_course='Обучение для конструкторов'
                    )
                await save_cursor(callback.user_id, extra_data = dict(
                    closed_questions=closed_questions,
                    open_questions=open_questions,
                    current_question=0,
                    closed_answers=[],  # Ответы на закрытые вопросы
                    open_answers=[],    # Ответы на открытые вопросы
                    test_stage="closed",  # Начинаем с закрытых вопросов
                    migration_state = "module_1_final_testing",
                    current_course='Обучение для конструкторов'
                ))
        else:
            data = dict()
            data.update(
                closed_questions=closed_questions,
                open_questions=open_questions,
                current_question=0,
                closed_answers=[],  # Ответы на закрытые вопросы
                open_answers=[],    # Ответы на открытые вопросы
                test_stage="closed",  # Начинаем с закрытых вопросов
                migration_state = "module_1_final_testing",
                current_course='Обучение для конструкторов'
                )
            await save_cursor(callback.user_id, extra_data = dict(
                    closed_questions=closed_questions,
                    open_questions=open_questions,
                    current_question=0,
                    closed_answers=[],  # Ответы на закрытые вопросы
                    open_answers=[],    # Ответы на открытые вопросы
                    test_stage="closed",  # Начинаем с закрытых вопросов
                    migration_state = "module_1_final_testing",
                    current_course='Обучение для конструкторов'
                ))
            
        logger.info(f'[kb_module_1_final_test_handler] после добавления вопросов в state: {data=}')  
        cursor.change_data(data)
        # Отправляем первый закрытый вопрос
        logger.info(f'[kb_module_1_final_test_handler] Отправляем первый закрытый вопрос')
        current_course = cursor.get_data().get('current_course')
        if not current_course:
            current_course = await get_value_from_redis(callback.user_id, 'current_course')
        else:
            current_course = get_current_course(cursor)
        logger.info(f'{current_course=}')
        await send_question_step_12(callback, cursor, "module_1_final_test", "Обучение для конструкторов")

        cursor.change_state(TrainingStates.step_12_testing)
        

    except Exception as e:
        logger.error(f"[ERROR][kb_module_1_final_test_handler] Произошла ошибка {e}") 
 

@router.on_button_callback(state(TrainingStates.konstructor['kb_module_1_start']), lambda data: data.payload == "next_educ_to_part_2")
async def kb_module_1_start_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ - Модуль №1 Стартовое сообщение с оглавлением»"""
    try:
        logger.info("[kb_module_1_start_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2) 
        if continue_flag:
            intro_text = get_module1_intro_text_kb_branch()
            await callback.send(intro_text)
            await asyncio.sleep(2) # 10
        
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
        
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_3_handler] Идет обработка нажмите позднее")
        #     return      
        await callback.message.delete()
        intro_text = get_module1_intro_text_kb_branch()
        await callback.send(intro_text)
        
        await asyncio.sleep(2) # 15
        
        kb = KeyboardBuilder().add(CallbackButton(text="📚 Продолжить обучение", payload="next_education::not_first"))
                
        cursor.change_state(TrainingStates.konstructor['module_0_lesson_1'])
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_1_lesson_1'], 'current_course': 'Обучение для конструкторов', 'payload': 'next_education::not_first', 'status_user': status_user})
        
        await callback.send(
            "📚 Вы можете продолжить обучение, нажав кнопку ниже 👇",
            keyboard=kb
        )
    
    except Exception as e:
        logger.error(f"[kb_module_0_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)
        

@router.on_button_callback(state(TrainingStates.konstructor['kb_module_2_start']), lambda data: data.payload == "next_educ_to_part_2")
async def kb_module_2_start_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ - Модуль №2 Стартовое сообщение с оглавлением»"""
    try:
        logger.info("[kb_module_2_start_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2) 
        if continue_flag:
            intro_text = get_module2_intro_text_kb_branch()
            await callback.send(intro_text)
            await asyncio.sleep(2) # 10
        
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
        
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_3_handler] Идет обработка нажмите позднее")
        #     return      
        await callback.message.delete()
        intro_text = get_module2_intro_text_kb_branch()
        await callback.send(intro_text)
        
        await asyncio.sleep(2) # 15
        
        kb = KeyboardBuilder().add(CallbackButton(text="📚 Продолжить обучение", payload="next_education::not_first"))
                
        cursor.change_state(TrainingStates.konstructor['module_2_lesson_1'])
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_2_lesson_1'], 'current_course': 'Обучение для конструкторов', 'payload': 'next_education::not_first', 'status_user': status_user})
        
        await callback.send(
            "📚 Вы можете продолжить обучение, нажав кнопку ниже 👇",
            keyboard=kb
        )
    
    except Exception as e:
        logger.error(f"[kb_module_2_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)  
        

@router.on_button_callback(state(TrainingStates.konstructor['kb_module_3_start']), lambda data: data.payload == "next_educ_to_part_2")
async def kb_module_3_start_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ - Модуль №3 Стартовое сообщение с оглавлением»"""
    try:
        logger.info("[kb_module_1_start_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2) 
        if continue_flag:
            intro_text = get_module3_intro_text_kb_branch()
            await callback.send(intro_text)
            await asyncio.sleep(2) # 10
        
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
        
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_3_handler] Идет обработка нажмите позднее")
        #     return      
        await callback.message.delete()
        intro_text = get_module3_intro_text_kb_branch()
        await callback.send(intro_text)
        
        await asyncio.sleep(2) # 15
        
        kb = KeyboardBuilder().add(CallbackButton(text="📚 Продолжить обучение", payload="next_education::not_first"))
                
        cursor.change_state(TrainingStates.konstructor['module_3_lesson_1'])
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_3_lesson_1'], 'current_course': 'Обучение для конструкторов', 'payload': 'next_education::not_first', 'status_user': status_user})
        
        await callback.send(
            "📚 Вы можете продолжить обучение, нажав кнопку ниже 👇",
            keyboard=kb
        )
    
    except Exception as e:
        logger.error(f"[kb_module_3_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 


@router.on_button_callback(state(TrainingStates.konstructor['kb_module_4_start']), lambda data: data.payload == "next_educ_to_part_2")
async def kb_module_4_start_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ - Модуль №4 Стартовое сообщение с оглавлением»"""
    try:
        logger.info("[kb_module_4_start_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2) 
        if continue_flag:
            intro_text = get_module4_intro_text_kb_branch()
            await callback.send(intro_text)
            await asyncio.sleep(2) # 10
        
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
        
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_3_handler] Идет обработка нажмите позднее")
        #     return      
        await callback.message.delete()
        intro_text = get_module4_intro_text_kb_branch()
        await callback.send(intro_text)
        
        await asyncio.sleep(2) # 15
        
        kb = KeyboardBuilder().add(CallbackButton(text="📚 Продолжить обучение", payload="next_education::not_first"))
                
        cursor.change_state(TrainingStates.konstructor['module_4_lesson_1'])
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_4_lesson_1'], 'current_course': 'Обучение для конструкторов', 'payload': 'next_education::not_first', 'status_user': status_user})
        
        await callback.send(
            "📚 Вы можете продолжить обучение, нажав кнопку ниже 👇",
            keyboard=kb
        )
    
    except Exception as e:
        logger.error(f"[kb_module_4_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 


@router.on_button_callback(state(TrainingStates.konstructor['kb_module_5_start']), lambda data: data.payload == "next_educ_to_part_2")
async def kb_module_5_start_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ - Модуль №5 Стартовое сообщение с оглавлением»"""
    try:
        logger.info("[kb_module_5_start_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2) 
        if continue_flag:
            intro_text = get_module5_intro_text_kb_branch()
            await callback.send(intro_text)
            await asyncio.sleep(2) # 10
        
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
        
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_3_handler] Идет обработка нажмите позднее")
        #     return      
        await callback.message.delete()
        intro_text = get_module5_intro_text_kb_branch()
        await callback.send(intro_text)
        
        await asyncio.sleep(2) # 15
        
        kb = KeyboardBuilder().add(CallbackButton(text="📚 Продолжить обучение", payload="next_education::not_first"))
                
        cursor.change_state(TrainingStates.konstructor['module_5_lesson_1'])
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_5_lesson_1'], 'current_course': 'Обучение для конструкторов', 'payload': 'next_education::not_first', 'status_user': status_user})
        
        await callback.send(
            "📚 Вы можете продолжить обучение, нажав кнопку ниже 👇",
            keyboard=kb
        )
    
    except Exception as e:
        logger.error(f"[kb_module_5_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 
        
        
@router.on_button_callback(state(TrainingStates.konstructor['kb_module_6_start']), lambda data: data.payload == "next_educ_to_part_2")
async def kb_module_6_start_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ - Модуль №6 Стартовое сообщение с оглавлением»"""
    try:
        logger.info("[kb_module_6_start_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2) 
        if continue_flag:
            intro_text = get_module6_intro_text_kb_branch()
            await callback.send(intro_text)
            await asyncio.sleep(2) # 10
        
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
        
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_3_handler] Идет обработка нажмите позднее")
        #     return      
        await callback.message.delete()
        intro_text = get_module6_intro_text_kb_branch()
        await callback.send(intro_text)
        
        await asyncio.sleep(2) # 15
        
        kb = KeyboardBuilder().add(CallbackButton(text="📚 Продолжить обучение", payload="next_education::not_first"))
                
        cursor.change_state(TrainingStates.konstructor['module_6_lesson_1'])
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_6_lesson_1'], 'current_course': 'Обучение для конструкторов', 'payload': 'next_education::not_first', 'status_user': status_user})
        
        await callback.send(
            "📚 Вы можете продолжить обучение, нажав кнопку ниже 👇",
            keyboard=kb
        )
    
    except Exception as e:
        logger.error(f"[kb_module_6_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 
        
        
@router.on_button_callback(state(TrainingStates.konstructor['kb_module_7_start']), lambda data: data.payload == "next_educ_to_part_2")
async def kb_module_7_start_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ - Модуль №7 Стартовое сообщение с оглавлением»"""
    try:
        logger.info("[kb_module_7_start_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2) 
        if continue_flag:
            intro_text = get_module7_intro_text_kb_branch()
            await callback.send(intro_text)
            await asyncio.sleep(2) # 10
        
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
        
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_3_handler] Идет обработка нажмите позднее")
        #     return      
        await callback.message.delete()
        intro_text = get_module7_intro_text_kb_branch()
        await callback.send(intro_text)
        
        await asyncio.sleep(2) # 15
        
        kb = KeyboardBuilder().add(CallbackButton(text="📚 Продолжить обучение", payload="next_education::not_first"))
                
        cursor.change_state(TrainingStates.konstructor['module_7_lesson_1'])
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_7_lesson_1'], 'current_course': 'Обучение для конструкторов', 'payload': 'next_education::not_first', 'status_user': status_user})
        
        await callback.send(
            "📚 Вы можете продолжить обучение, нажав кнопку ниже 👇",
            keyboard=kb
        )
    
    except Exception as e:
        logger.error(f"[kb_module_7_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 


@router.on_button_callback(state(TrainingStates.konstructor['module_1_lesson_1']), lambda data: data.payload.split('::')[1] == "not_first")
async def kb_module_1_lesson_1_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ - Модуль №1 Урок №1: Расчёт заявки и формирование КП»"""
    try:
        logger.info("[kb_module_1_lesson_1_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
        
        await callback.message.delete()
        intro_text = get_module1_lesson1_intro_text_kb_branch()
        await callback.send(intro_text, disable_link_preview = True) 
        
        await asyncio.sleep(2) # 15
        
        course_name = await get_value_from_redis(callback.user_id, 'current_course')
        if not course_name:
            course_name = get_current_course(cursor)
        logger.info(f'{course_name=}')
        
        game = GamificationService(course_name)
        user_data = load_user_data()
        user_id = str(callback.user_id)
        first_name = user_data.get(user_id).get("first_name")
        last_name = user_data.get(user_id).get("second_name")
        
        await game.increment_lesson_func(
            user_id=user_id,
            course_name=course_name, # "Обучение по продажам"
            lesson_id='section_13', #  "section_1"
            user_data={
                "username": f'{first_name} {last_name}',
                "first_name": first_name,
                "last_name": last_name
            }
        )
                
        # сообщение о тестировании с кнопкой
        test_text = kb_go_to_test_after_lesson(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        cursor.change_state(TrainingStates.konstructor['module_1_lesson_1_questions'])
        await asyncio.sleep(2) # 2
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_1_lesson_1_questions'], 'payload': 'start_test', 'current_course': 'Обучение для конструкторов', 'status_user': status_user})
    except Exception as e:
        logger.error(f"[kb_module_1_lesson_1_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 


@router.on_button_callback(state(TrainingStates.konstructor['module_1_lesson_1_questions']), lambda data: data.payload == "start_test")
async def kb_module_1_lesson_1_test_handler(callback: Callback, cursor: FSMCursor):
    """ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ Начало тестирования МОДУЛЬ № 1 УРОК № 1 """
    try:
        logger.info("[kb_module_1_lesson_1_test_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}) 
        questions = get_testing_data_module_1_test_1_kb()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[kb_module_1_lesson_1_test_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
        logger.info(f'{callback=}')
        
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        else:
            await save_cursor(callback, extra_data=dict(questions=questions, current_question=0, answers=[]))
        
            
        logger.info(f'[kb_module_1_lesson_1_test_handler] после добавления вопросов в state: {data=}')  
        
        # Отправляем первый вопрос
        cursor.change_data(data)
        await send_question(callback, cursor, "section_15")
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.konstructor['module_1_lesson_1_testing']))
        else:
            await save_cursor(callback, extra_data=dict(state_name = TrainingStates.konstructor['module_1_lesson_1_testing']))
        cursor.change_state(TrainingStates.konstructor['module_1_lesson_1_testing'])
    
    except Exception as e:
        logger.error(f"[kb_module_0_lesson_5_test_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)
        

@router.on_button_callback(state(TrainingStates.konstructor['module_1_lesson_2']), lambda data: data.payload.split('::')[1] == "not_first")
async def kb_module_1_lesson_2_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ - Модуль №1 Урок №2: Как определить тип изделия и условия применения"""
    try:
        logger.info("[kb_module_1_lesson_2_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
        
        await callback.message.delete()
        intro_text = get_module1_lesson2_intro_text_kb_branch()
        await callback.send(intro_text, disable_link_preview = True) 
        
        await asyncio.sleep(2) # 15
        
        course_name = await get_value_from_redis(callback.user_id, 'current_course')
        if not course_name:
            course_name = get_current_course(cursor)
        logger.info(f'{course_name=}')
        
        game = GamificationService(course_name)
        user_data = load_user_data()
        user_id = str(callback.user_id)
        first_name = user_data.get(user_id).get("first_name")
        last_name = user_data.get(user_id).get("second_name")
        
        await game.increment_lesson_func(
            user_id=user_id,
            course_name=course_name, # "Обучение по продажам"
            lesson_id='section_15', #  "section_1"
            user_data={
                "username": f'{first_name} {last_name}',
                "first_name": first_name,
                "last_name": last_name
            }
        )
                
        # сообщение о тестировании с кнопкой
        test_text = kb_go_to_test_after_lesson(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        cursor.change_state(TrainingStates.konstructor['module_1_lesson_2_questions'])
        await asyncio.sleep(2) # 2
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_1_lesson_2_questions'], 'payload': 'start_test', 'current_course': 'Обучение для конструкторов', 'status_user': status_user})
    except Exception as e:
        logger.error(f"[kb_module_1_lesson_2_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 


@router.on_button_callback(state(TrainingStates.konstructor['module_1_lesson_2_questions']), lambda data: data.payload == "start_test")
async def kb_module_1_lesson_2_test_handler(callback: Callback, cursor: FSMCursor):
    """ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ Начало тестирования МОДУЛЬ № 1 УРОК № 2 """
    try:
        logger.info("[kb_module_1_lesson_2_test_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}) 
        questions = get_testing_data_module_1_test_2_kb()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[kb_module_1_lesson_2_test_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
        logger.info(f'{callback=}')
        
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        else:
            await save_cursor(callback, extra_data=dict(questions=questions, current_question=0, answers=[]))
        
            
        logger.info(f'[kb_module_1_lesson_2_test_handler] после добавления вопросов в state: {data=}')  
        
        # Отправляем первый вопрос
        cursor.change_data(data)
        await send_question(callback, cursor, "section_17")
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.konstructor['module_1_lesson_2_testing']))
        else:
            await save_cursor(callback, extra_data=dict(state_name = TrainingStates.konstructor['module_1_lesson_2_testing']))
        cursor.change_state(TrainingStates.konstructor['module_1_lesson_2_testing'])
    
    except Exception as e:
        logger.error(f"[kb_module_1_lesson_2_test_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)


@router.on_button_callback(state(TrainingStates.konstructor['module_1_lesson_3']), lambda data: data.payload.split('::')[1] == "not_first")
async def kb_module_1_lesson_3_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ - Модуль №1 Урок №3: Как выбрать техническое решение: система, профиль, заполнение, фурнитура"""
    try:
        logger.info("[kb_module_1_lesson_3_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
        
        await callback.message.delete()
        intro_text = get_module1_lesson3_intro_text_kb_branch()
        await callback.send(intro_text, disable_link_preview = True) 
        
        await asyncio.sleep(2) # 15
        
        course_name = await get_value_from_redis(callback.user_id, 'current_course')
        if not course_name:
            course_name = get_current_course(cursor)
        logger.info(f'{course_name=}')
        
        game = GamificationService(course_name)
        user_data = load_user_data()
        user_id = str(callback.user_id)
        first_name = user_data.get(user_id).get("first_name")
        last_name = user_data.get(user_id).get("second_name")
        
        await game.increment_lesson_func(
            user_id=user_id,
            course_name=course_name, # "Обучение по продажам"
            lesson_id='section_17', #  "section_1"
            user_data={
                "username": f'{first_name} {last_name}',
                "first_name": first_name,
                "last_name": last_name
            }
        )
                
        # сообщение о тестировании с кнопкой
        test_text = kb_go_to_test_after_lesson(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        cursor.change_state(TrainingStates.konstructor['module_1_lesson_3_questions'])
        await asyncio.sleep(2) # 2
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_1_lesson_3_questions'], 'payload': 'start_test', 'current_course': 'Обучение для конструкторов', 'status_user': status_user})
    except Exception as e:
        logger.error(f"[kb_module_1_lesson_3_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 


@router.on_button_callback(state(TrainingStates.konstructor['module_1_lesson_3_questions']), lambda data: data.payload == "start_test")
async def kb_module_1_lesson_3_test_handler(callback: Callback, cursor: FSMCursor):
    """ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ Начало тестирования МОДУЛЬ № 1 УРОК № 3 """
    try:
        logger.info("[kb_module_1_lesson_3_test_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}) 
        questions = get_testing_data_module_1_test_3_kb()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[kb_module_1_lesson_3_test_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
        logger.info(f'{callback=}')
        
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        else:
            await save_cursor(callback, extra_data=dict(questions=questions, current_question=0, answers=[]))
        
            
        logger.info(f'[kb_module_1_lesson_3_test_handler] после добавления вопросов в state: {data=}')  
        
        # Отправляем первый вопрос
        cursor.change_data(data)
        await send_question(callback, cursor, "section_19")
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.konstructor['module_1_lesson_3_testing']))
        else:
            await save_cursor(callback, extra_data=dict(state_name = TrainingStates.konstructor['module_1_lesson_3_testing']))
        cursor.change_state(TrainingStates.konstructor['module_1_lesson_3_testing'])
    
    except Exception as e:
        logger.error(f"[kb_module_1_lesson_3_test_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)
        

@router.on_button_callback(state(TrainingStates.konstructor['module_1_lesson_4']), lambda data: data.payload.split('::')[1] == "not_first")
async def kb_module_1_lesson_4_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ - Модуль №1 Урок №4: Как проверить ограничения: сертификаты, размеры, огнестойкость"""
    try:
        logger.info("[kb_module_1_lesson_4_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
        
        await callback.message.delete()
        intro_text = get_module1_lesson4_intro_text_kb_branch()
        await callback.send(intro_text, disable_link_preview = True) 
        
        await asyncio.sleep(2) # 15
        
        course_name = await get_value_from_redis(callback.user_id, 'current_course')
        if not course_name:
            course_name = get_current_course(cursor)
        logger.info(f'{course_name=}')
        
        game = GamificationService(course_name)
        user_data = load_user_data()
        user_id = str(callback.user_id)
        first_name = user_data.get(user_id).get("first_name")
        last_name = user_data.get(user_id).get("second_name")
        
        await game.increment_lesson_func(
            user_id=user_id,
            course_name=course_name, # "Обучение по продажам"
            lesson_id='section_19', #  "section_1"
            user_data={
                "username": f'{first_name} {last_name}',
                "first_name": first_name,
                "last_name": last_name
            }
        )
                
        # сообщение о тестировании с кнопкой
        test_text = kb_go_to_test_after_lesson(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        cursor.change_state(TrainingStates.konstructor['module_1_lesson_4_questions'])
        await asyncio.sleep(2) # 2
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_1_lesson_4_questions'], 'payload': 'start_test', 'current_course': 'Обучение для конструкторов', 'status_user': status_user})
    except Exception as e:
        logger.error(f"[kb_module_1_lesson_4_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 


@router.on_button_callback(state(TrainingStates.konstructor['module_1_lesson_3_questions']), lambda data: data.payload == "start_test")
async def kb_module_1_lesson_4_test_handler(callback: Callback, cursor: FSMCursor):
    """ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ Начало тестирования МОДУЛЬ № 1 УРОК № 4 """
    try:
        logger.info("[kb_module_1_lesson_4_test_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}) 
        questions = get_testing_data_module_1_test_4_kb()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[kb_module_1_lesson_4_test_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
        logger.info(f'{callback=}')
        
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        else:
            await save_cursor(callback, extra_data=dict(questions=questions, current_question=0, answers=[]))
        
            
        logger.info(f'[kb_module_1_lesson_4_test_handler] после добавления вопросов в state: {data=}')  
        
        # Отправляем первый вопрос
        cursor.change_data(data)
        await send_question(callback, cursor, "section_21")
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.konstructor['module_1_lesson_4_testing']))
        else:
            await save_cursor(callback, extra_data=dict(state_name = TrainingStates.konstructor['module_1_lesson_4_testing']))
        cursor.change_state(TrainingStates.konstructor['module_1_lesson_4_testing'])
    
    except Exception as e:
        logger.error(f"[kb_module_1_lesson_4_test_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)
        
        
@router.on_button_callback(state(TrainingStates.konstructor['module_1_lesson_5']), lambda data: data.payload.split('::')[1] == "not_first")
async def kb_module_1_lesson_5_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ - Модуль №1 Урок №5: Как выполнить стандартный расчёт в ПрофСтрой / ПФ4"""
    try:
        logger.info("[kb_module_1_lesson_5_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
        
        await callback.message.delete()
        intro_text = get_module1_lesson5_intro_text_kb_branch()
        await callback.send(intro_text, disable_link_preview = True) 
        
        await asyncio.sleep(2) # 15
        
        course_name = await get_value_from_redis(callback.user_id, 'current_course')
        if not course_name:
            course_name = get_current_course(cursor)
        logger.info(f'{course_name=}')
        
        game = GamificationService(course_name)
        user_data = load_user_data()
        user_id = str(callback.user_id)
        first_name = user_data.get(user_id).get("first_name")
        last_name = user_data.get(user_id).get("second_name")
        
        await game.increment_lesson_func(
            user_id=user_id,
            course_name=course_name, # "Обучение по продажам"
            lesson_id='section_21', #  "section_1"
            user_data={
                "username": f'{first_name} {last_name}',
                "first_name": first_name,
                "last_name": last_name
            }
        )
                
        # сообщение о тестировании с кнопкой
        test_text = kb_go_to_test_after_lesson(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        cursor.change_state(TrainingStates.konstructor['module_1_lesson_5_questions'])
        await asyncio.sleep(2) # 2
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_1_lesson_5_questions'], 'payload': 'start_test', 'current_course': 'Обучение для конструкторов', 'status_user': status_user})
    except Exception as e:
        logger.error(f"[kb_module_1_lesson_5_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 


@router.on_button_callback(state(TrainingStates.konstructor['module_1_lesson_5_questions']), lambda data: data.payload == "start_test")
async def kb_module_1_lesson_5_test_handler(callback: Callback, cursor: FSMCursor):
    """ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ Начало тестирования МОДУЛЬ № 1 УРОК № 5 """
    try:
        logger.info("[kb_module_1_lesson_5_test_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}) 
        questions = get_testing_data_module_1_test_5_kb()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[kb_module_1_lesson_5_test_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
        logger.info(f'{callback=}')
        
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        else:
            await save_cursor(callback, extra_data=dict(questions=questions, current_question=0, answers=[]))
        
            
        logger.info(f'[kb_module_1_lesson_5_test_handler] после добавления вопросов в state: {data=}')  
        
        # Отправляем первый вопрос
        cursor.change_data(data)
        await send_question(callback, cursor, "section_23")
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.konstructor['module_1_lesson_5_testing']))
        else:
            await save_cursor(callback, extra_data=dict(state_name = TrainingStates.konstructor['module_1_lesson_5_testing']))
        cursor.change_state(TrainingStates.konstructor['module_1_lesson_5_testing'])
    
    except Exception as e:
        logger.error(f"[kb_module_1_lesson_5_test_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)          


@router.on_button_callback(state(TrainingStates.konstructor['module_1_lesson_6']), lambda data: data.payload.split('::')[1] == "not_first")
async def kb_module_1_lesson_6_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ - Модуль №1 Урок №6: Как считать нестандартное решение вручную и когда эскалировать"""
    try:
        logger.info("[kb_module_1_lesson_6_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
        
        await callback.message.delete()
        intro_text = get_module1_lesson6_intro_text_kb_branch()
        await callback.send(intro_text, disable_link_preview = True) 
        
        await asyncio.sleep(2) # 15
        
        course_name = await get_value_from_redis(callback.user_id, 'current_course')
        if not course_name:
            course_name = get_current_course(cursor)
        logger.info(f'{course_name=}')
        
        game = GamificationService(course_name)
        user_data = load_user_data()
        user_id = str(callback.user_id)
        first_name = user_data.get(user_id).get("first_name")
        last_name = user_data.get(user_id).get("second_name")
        
        await game.increment_lesson_func(
            user_id=user_id,
            course_name=course_name, # "Обучение по продажам"
            lesson_id='section_23', #  "section_1"
            user_data={
                "username": f'{first_name} {last_name}',
                "first_name": first_name,
                "last_name": last_name
            }
        )
                
        # сообщение о тестировании с кнопкой
        test_text = kb_go_to_test_after_lesson(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        cursor.change_state(TrainingStates.konstructor['module_1_lesson_6_questions'])
        await asyncio.sleep(2) # 2
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_1_lesson_6_questions'], 'payload': 'start_test', 'current_course': 'Обучение для конструкторов', 'status_user': status_user})
    except Exception as e:
        logger.error(f"[kb_module_1_lesson_6_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 


@router.on_button_callback(state(TrainingStates.konstructor['module_1_lesson_6_questions']), lambda data: data.payload == "start_test")
async def kb_module_1_lesson_6_test_handler(callback: Callback, cursor: FSMCursor):
    """ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ Начало тестирования МОДУЛЬ № 1 УРОК № 6 """
    try:
        logger.info("[kb_module_1_lesson_6_test_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}) 
        questions = get_testing_data_module_1_test_6_kb()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[kb_module_1_lesson_6_test_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
        logger.info(f'{callback=}')
        
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        else:
            await save_cursor(callback, extra_data=dict(questions=questions, current_question=0, answers=[]))
        
            
        logger.info(f'[kb_module_1_lesson_6_test_handler] после добавления вопросов в state: {data=}')  
        
        # Отправляем первый вопрос
        cursor.change_data(data)
        await send_question(callback, cursor, "section_25")
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.konstructor['module_1_lesson_6_testing']))
        else:
            await save_cursor(callback, extra_data=dict(state_name = TrainingStates.konstructor['module_1_lesson_6_testing']))
        cursor.change_state(TrainingStates.konstructor['module_1_lesson_6_testing'])
    
    except Exception as e:
        logger.error(f"[kb_module_1_lesson_6_test_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 


@router.on_button_callback(state(TrainingStates.konstructor['module_1_lesson_6_testing']), lambda data: data.payload.split('::')[1] == "not_first")
async def continue_after_kb_module_1_handler(callback: Callback, cursor: FSMCursor):
    """Завершение Модуля №01 - КБ. Переход к вопросам или финальному тесту"""
    try:
        logger.info(f"[continue_after_kb_module_1_handler] Стартовал")
        await callback.message.delete()
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        # Проверяем загрузку базы знаний
        rag = RAGService()
        stats = rag.get_stats()
        
        cursor_data = cursor.get_data()
                
        if not stats['is_loaded']:
            await callback.send(
                "❌ База знаний не загружена. Обратитесь к администратору.",
                keyboard=main_menu_keyboard(current_course)
            )
            cursor.clear()
            return
        
        text = kb_get_text_to_final_test_module_1()
                
        await callback.send(text, keyboard=final_start_test_kb())
        cursor.change_state(TrainingStates.konstructor['module_1_questions'])
        await save_cursor(callback.user_id, extra_data = {'payload': 'to_final_test', 'state_name': TrainingStates.konstructor['module_1_questions'], 'current_course': current_course})
    
    except Exception as e:
        logger.error(f"[continue_after_kb_module_1_handler] Произошла ошибка {e}")
        

@router.on_button_callback(state(TrainingStates.konstructor['module_2_lesson_1']), lambda data: data.payload.split('::')[1] == "not_first")
async def kb_module_2_lesson_1_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ - Модуль №2 Урок №1: Как отличить актуализацию от пересчёта"""
    try:
        logger.info("[kb_module_2_lesson_1_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
        
        await callback.message.delete()
        intro_text = get_module2_lesson1_intro_text_kb_branch()
        await callback.send(intro_text, disable_link_preview = True) 
        
        await asyncio.sleep(2) # 15
        
        course_name = await get_value_from_redis(callback.user_id, 'current_course')
        if not course_name:
            course_name = get_current_course(cursor)
        logger.info(f'{course_name=}')
        
        game = GamificationService(course_name)
        user_data = load_user_data()
        user_id = str(callback.user_id)
        first_name = user_data.get(user_id).get("first_name")
        last_name = user_data.get(user_id).get("second_name")
        
        await game.increment_lesson_func(
            user_id=user_id,
            course_name=course_name, # "Обучение по продажам"
            lesson_id='section_26', #  "section_1"
            user_data={
                "username": f'{first_name} {last_name}',
                "first_name": first_name,
                "last_name": last_name
            }
        )
                
        # сообщение о тестировании с кнопкой
        test_text = kb_go_to_test_after_lesson(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        cursor.change_state(TrainingStates.konstructor['module_2_lesson_1_questions'])
        await asyncio.sleep(2) # 2
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_2_lesson_1_questions'], 'payload': 'start_test', 'current_course': 'Обучение для конструкторов', 'status_user': status_user})
    except Exception as e:
        logger.error(f"[kb_module_1_lesson_6_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 


@router.on_button_callback(state(TrainingStates.konstructor['module_2_lesson_1_questions']), lambda data: data.payload == "start_test")
async def kb_module_2_lesson_1_test_handler(callback: Callback, cursor: FSMCursor):
    """ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ Начало тестирования МОДУЛЬ № 2 УРОК № 1 """
    try:
        logger.info("[kb_module_2_lesson_1_test_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}) 
        questions = get_testing_data_module_2_test_1_kb()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[kb_module_2_lesson_1_test_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
        logger.info(f'{callback=}')
        
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        else:
            await save_cursor(callback, extra_data=dict(questions=questions, current_question=0, answers=[]))
        
            
        logger.info(f'[kb_module_2_lesson_1_test_handler] после добавления вопросов в state: {data=}')  
        
        # Отправляем первый вопрос
        cursor.change_data(data)
        await send_question(callback, cursor, "section_28")
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.konstructor['module_2_lesson_1_testing']))
        else:
            await save_cursor(callback, extra_data=dict(state_name = TrainingStates.konstructor['module_2_lesson_1_testing']))
        cursor.change_state(TrainingStates.konstructor['module_2_lesson_1_testing'])
    
    except Exception as e:
        logger.error(f"[kb_module_2_lesson_1_test_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 
        

@router.on_button_callback(state(TrainingStates.konstructor['module_2_lesson_2']), lambda data: data.payload.split('::')[1] == "not_first")
async def kb_module_2_lesson_2_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ - Модуль №2 Урок №2: Как проверить старый расчёт и новые данные клиента"""
    try:
        logger.info("[kb_module_2_lesson_2_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
        
        await callback.message.delete()
        intro_text = get_module2_lesson2_intro_text_kb_branch()
        await callback.send(intro_text, disable_link_preview = True) 
        
        await asyncio.sleep(2) # 15
        
        course_name = await get_value_from_redis(callback.user_id, 'current_course')
        if not course_name:
            course_name = get_current_course(cursor)
        logger.info(f'{course_name=}')
        
        game = GamificationService(course_name)
        user_data = load_user_data()
        user_id = str(callback.user_id)
        first_name = user_data.get(user_id).get("first_name")
        last_name = user_data.get(user_id).get("second_name")
        
        await game.increment_lesson_func(
            user_id=user_id,
            course_name=course_name, # "Обучение по продажам"
            lesson_id='section_28', #  "section_1"
            user_data={
                "username": f'{first_name} {last_name}',
                "first_name": first_name,
                "last_name": last_name
            }
        )
                
        # сообщение о тестировании с кнопкой
        test_text = kb_go_to_test_after_lesson(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        cursor.change_state(TrainingStates.konstructor['module_2_lesson_2_questions'])
        await asyncio.sleep(2) # 2
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_2_lesson_2_questions'], 'payload': 'start_test', 'current_course': 'Обучение для конструкторов', 'status_user': status_user})
    except Exception as e:
        logger.error(f"[kb_module_2_lesson_2_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 


@router.on_button_callback(state(TrainingStates.konstructor['module_2_lesson_2_questions']), lambda data: data.payload == "start_test")
async def kb_module_2_lesson_2_test_handler(callback: Callback, cursor: FSMCursor):
    """ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ Начало тестирования МОДУЛЬ № 2 УРОК № 2 """
    try:
        logger.info("[kb_module_2_lesson_2_test_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}) 
        questions = get_testing_data_module_2_test_2_kb()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[kb_module_2_lesson_2_test_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
        logger.info(f'{callback=}')
        
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        else:
            await save_cursor(callback, extra_data=dict(questions=questions, current_question=0, answers=[]))
        
            
        logger.info(f'[kb_module_2_lesson_2_test_handler] после добавления вопросов в state: {data=}')  
        
        # Отправляем первый вопрос
        cursor.change_data(data)
        await send_question(callback, cursor, "section_30")
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.konstructor['module_2_lesson_2_testing']))
        else:
            await save_cursor(callback, extra_data=dict(state_name = TrainingStates.konstructor['module_2_lesson_2_testing']))
        cursor.change_state(TrainingStates.konstructor['module_2_lesson_2_testing'])
    
    except Exception as e:
        logger.error(f"[kb_module_2_lesson_2_test_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)


@router.on_button_callback(state(TrainingStates.konstructor['module_2_lesson_3']), lambda data: data.payload.split('::')[1] == "not_first")
async def kb_module_2_lesson_3_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ - Модуль №2 Урок №3: Как внести изменения и обновить стоимость"""
    try:
        logger.info("[kb_module_2_lesson_3_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
        
        await callback.message.delete()
        intro_text = get_module2_lesson3_intro_text_kb_branch()
        await callback.send(intro_text, disable_link_preview = True) 
        
        await asyncio.sleep(2) # 15
        
        course_name = await get_value_from_redis(callback.user_id, 'current_course')
        if not course_name:
            course_name = get_current_course(cursor)
        logger.info(f'{course_name=}')
        
        game = GamificationService(course_name)
        user_data = load_user_data()
        user_id = str(callback.user_id)
        first_name = user_data.get(user_id).get("first_name")
        last_name = user_data.get(user_id).get("second_name")
        
        await game.increment_lesson_func(
            user_id=user_id,
            course_name=course_name, # "Обучение по продажам"
            lesson_id='section_30', #  "section_1"
            user_data={
                "username": f'{first_name} {last_name}',
                "first_name": first_name,
                "last_name": last_name
            }
        )
                
        # сообщение о тестировании с кнопкой
        test_text = kb_go_to_test_after_lesson(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        cursor.change_state(TrainingStates.konstructor['module_2_lesson_3_questions'])
        await asyncio.sleep(2) # 2
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_2_lesson_3_questions'], 'payload': 'start_test', 'current_course': 'Обучение для конструкторов', 'status_user': status_user})
    except Exception as e:
        logger.error(f"[kb_module_2_lesson_3_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 


@router.on_button_callback(state(TrainingStates.konstructor['module_2_lesson_3_questions']), lambda data: data.payload == "start_test")
async def kb_module_2_lesson_3_test_handler(callback: Callback, cursor: FSMCursor):
    """ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ Начало тестирования МОДУЛЬ № 2 УРОК № 3 """
    try:
        logger.info("[kb_module_2_lesson_3_test_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}) 
        questions = get_testing_data_module_2_test_3_kb()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[kb_module_2_lesson_3_test_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
        logger.info(f'{callback=}')
        
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        else:
            await save_cursor(callback, extra_data=dict(questions=questions, current_question=0, answers=[]))
        
            
        logger.info(f'[kb_module_2_lesson_3_test_handler] после добавления вопросов в state: {data=}')  
        
        # Отправляем первый вопрос
        cursor.change_data(data)
        await send_question(callback, cursor, "section_32")
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.konstructor['module_2_lesson_3_testing']))
        else:
            await save_cursor(callback, extra_data=dict(state_name = TrainingStates.konstructor['module_2_lesson_3_testing']))
        cursor.change_state(TrainingStates.konstructor['module_2_lesson_3_testing'])
    
    except Exception as e:
        logger.error(f"[kb_module_2_lesson_3_test_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)
        

@router.on_button_callback(state(TrainingStates.konstructor['module_2_lesson_4']), lambda data: data.payload.split('::')[1] == "not_first")
async def kb_module_2_lesson_4_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ - Модуль №2 Урок №4: Как проверить ограничения после изменений"""
    try:
        logger.info("[kb_module_2_lesson_4_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
        
        await callback.message.delete()
        intro_text = get_module2_lesson4_intro_text_kb_branch()
        await callback.send(intro_text, disable_link_preview = True) 
        
        await asyncio.sleep(2) # 15
        
        course_name = await get_value_from_redis(callback.user_id, 'current_course')
        if not course_name:
            course_name = get_current_course(cursor)
        logger.info(f'{course_name=}')
        
        game = GamificationService(course_name)
        user_data = load_user_data()
        user_id = str(callback.user_id)
        first_name = user_data.get(user_id).get("first_name")
        last_name = user_data.get(user_id).get("second_name")
        
        await game.increment_lesson_func(
            user_id=user_id,
            course_name=course_name, # "Обучение по продажам"
            lesson_id='section_32', #  "section_1"
            user_data={
                "username": f'{first_name} {last_name}',
                "first_name": first_name,
                "last_name": last_name
            }
        )
                
        # сообщение о тестировании с кнопкой
        test_text = kb_go_to_test_after_lesson(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        cursor.change_state(TrainingStates.konstructor['module_2_lesson_4_questions'])
        await asyncio.sleep(2) # 2
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_2_lesson_4_questions'], 'payload': 'start_test', 'current_course': 'Обучение для конструкторов', 'status_user': status_user})
    except Exception as e:
        logger.error(f"[kb_module_2_lesson_4_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 


@router.on_button_callback(state(TrainingStates.konstructor['module_2_lesson_4_questions']), lambda data: data.payload == "start_test")
async def kb_module_2_lesson_4_test_handler(callback: Callback, cursor: FSMCursor):
    """ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ Начало тестирования МОДУЛЬ № 2 УРОК № 4 """
    try:
        logger.info("[kb_module_2_lesson_4_test_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}) 
        questions = get_testing_data_module_2_test_4_kb()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[kb_module_2_lesson_4_test_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
        logger.info(f'{callback=}')
        
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        else:
            await save_cursor(callback, extra_data=dict(questions=questions, current_question=0, answers=[]))
        
            
        logger.info(f'[kb_module_2_lesson_4_test_handler] после добавления вопросов в state: {data=}')  
        
        # Отправляем первый вопрос
        cursor.change_data(data)
        await send_question(callback, cursor, "section_34")
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.konstructor['module_2_lesson_4_testing']))
        else:
            await save_cursor(callback, extra_data=dict(state_name = TrainingStates.konstructor['module_2_lesson_4_testing']))
        cursor.change_state(TrainingStates.konstructor['module_2_lesson_4_testing'])
    
    except Exception as e:
        logger.error(f"[kb_module_2_lesson_4_test_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)
        

@router.on_button_callback(state(TrainingStates.konstructor['module_2_lesson_5']), lambda data: data.payload.split('::')[1] == "not_first")
async def kb_module_2_lesson_5_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ - Модуль №2 Урок №5: Как передать обновлённый результат менеджеру"""
    try:
        logger.info("[kb_module_2_lesson_5_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
        
        await callback.message.delete()
        intro_text = get_module2_lesson5_intro_text_kb_branch()
        await callback.send(intro_text, disable_link_preview = True) 
        
        await asyncio.sleep(2) # 15
        
        course_name = await get_value_from_redis(callback.user_id, 'current_course')
        if not course_name:
            course_name = get_current_course(cursor)
        logger.info(f'{course_name=}')
        
        game = GamificationService(course_name)
        user_data = load_user_data()
        user_id = str(callback.user_id)
        first_name = user_data.get(user_id).get("first_name")
        last_name = user_data.get(user_id).get("second_name")
        
        await game.increment_lesson_func(
            user_id=user_id,
            course_name=course_name, # "Обучение по продажам"
            lesson_id='section_34', #  "section_1"
            user_data={
                "username": f'{first_name} {last_name}',
                "first_name": first_name,
                "last_name": last_name
            }
        )
                
        # сообщение о тестировании с кнопкой
        test_text = kb_go_to_test_after_lesson(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        cursor.change_state(TrainingStates.konstructor['module_2_lesson_5_questions'])
        await asyncio.sleep(2) # 2
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_2_lesson_5_questions'], 'payload': 'start_test', 'current_course': 'Обучение для конструкторов', 'status_user': status_user})
    except Exception as e:
        logger.error(f"[kb_module_2_lesson_5_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 


@router.on_button_callback(state(TrainingStates.konstructor['module_2_lesson_5_questions']), lambda data: data.payload == "start_test")
async def kb_module_2_lesson_5_test_handler(callback: Callback, cursor: FSMCursor):
    """ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ Начало тестирования МОДУЛЬ № 2 УРОК № 5 """
    try:
        logger.info("[kb_module_2_lesson_5_test_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}) 
        questions = get_testing_data_module_2_test_5_kb()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[kb_module_2_lesson_5_test_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
        logger.info(f'{callback=}')
        
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        else:
            await save_cursor(callback, extra_data=dict(questions=questions, current_question=0, answers=[]))
        
            
        logger.info(f'[kb_module_2_lesson_5_test_handler] после добавления вопросов в state: {data=}')  
        
        # Отправляем первый вопрос
        cursor.change_data(data)
        await send_question(callback, cursor, "section_36")
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.konstructor['module_2_lesson_5_testing']))
        else:
            await save_cursor(callback, extra_data=dict(state_name = TrainingStates.konstructor['module_2_lesson_5_testing']))
        cursor.change_state(TrainingStates.konstructor['module_2_lesson_5_testing'])
    
    except Exception as e:
        logger.error(f"[kb_module_2_lesson_5_test_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)
        

@router.on_button_callback(state(TrainingStates.konstructor['module_2_lesson_5_testing']), lambda data: data.payload.split('::')[1] == "not_first")
async def continue_after_kb_module_2_handler(callback: Callback, cursor: FSMCursor):
    """Завершение Модуля №2 - КБ. Переход к вопросам или финальному тесту"""
    try:
        logger.info(f"[continue_after_kb_module_2_handler] Стартовал")
        await callback.message.delete()
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        # Проверяем загрузку базы знаний
        rag = RAGService()
        stats = rag.get_stats()
        
        cursor_data = cursor.get_data()
                
        if not stats['is_loaded']:
            await callback.send(
                "❌ База знаний не загружена. Обратитесь к администратору.",
                keyboard=main_menu_keyboard(current_course)
            )
            cursor.clear()
            return
        
        text = kb_get_text_to_final_test_module_2()
                
        await callback.send(text, keyboard=final_start_test_kb())
        cursor.change_state(TrainingStates.konstructor['module_0_questions'])
        await save_cursor(callback.user_id, extra_data = {'payload': 'to_final_test', 'state_name': TrainingStates.konstructor['module_2_questions'], 'current_course': current_course})
    
    except Exception as e:
        logger.error(f"[continue_after_kb_module_2_handler] Произошла ошибка {e}")


@router.on_button_callback(state(TrainingStates.konstructor['module_2_questions']), lambda data: data.payload == "to_final_test")
async def kb_module_2_final_test_handler(callback: Callback, cursor: FSMCursor):
    '''Заглушка для прохождения финального теста по модулю № 2'''
    try:
        logger.info("[kb_module_2_final_test_handler] Стартовал")
        # ЧАСТЬ 1: Закрытые вопросы (10 вопросов с вариантами A/B/C/D)
        closed_questions = get_final_testing_data_module_2_kb('close')
        logger.info(f"[INFO][kb_module_2_final_test_handler] {closed_questions=}")
        
        # ЧАСТЬ 2: Открытые вопросы (5 вопросов с эталонными ответами)
        open_questions = get_final_testing_data_module_2_kb('open')
        logger.info(f"[INFO][kb_module_2_final_test_handler] {open_questions=}")
        
        data = cursor.get_data()
        logger.info(f'[kb_module_2_final_test_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
    
        if data and isinstance(data, dict):
                data.update(
                    closed_questions=closed_questions,
                    open_questions=open_questions,
                    current_question=0,
                    closed_answers=[],  # Ответы на закрытые вопросы
                    open_answers=[],    # Ответы на открытые вопросы
                    test_stage="closed",  # Начинаем с закрытых вопросов
                    migration_state = "module_2_final_testing",
                    current_course='Обучение для конструкторов'
                    )
                await save_cursor(callback.user_id, extra_data = dict(
                    closed_questions=closed_questions,
                    open_questions=open_questions,
                    current_question=0,
                    closed_answers=[],  # Ответы на закрытые вопросы
                    open_answers=[],    # Ответы на открытые вопросы
                    test_stage="closed",  # Начинаем с закрытых вопросов
                    migration_state = "module_2_final_testing",
                    current_course='Обучение для конструкторов'
                ))
        else:
            data = dict()
            data.update(
                closed_questions=closed_questions,
                open_questions=open_questions,
                current_question=0,
                closed_answers=[],  # Ответы на закрытые вопросы
                open_answers=[],    # Ответы на открытые вопросы
                test_stage="closed",  # Начинаем с закрытых вопросов
                migration_state = "module_2_final_testing",
                current_course='Обучение для конструкторов'
                )
            await save_cursor(callback.user_id, extra_data = dict(
                    closed_questions=closed_questions,
                    open_questions=open_questions,
                    current_question=0,
                    closed_answers=[],  # Ответы на закрытые вопросы
                    open_answers=[],    # Ответы на открытые вопросы
                    test_stage="closed",  # Начинаем с закрытых вопросов
                    migration_state = "module_2_final_testing",
                    current_course='Обучение для конструкторов'
                ))
            
        logger.info(f'[kb_module_2_final_test_handler] после добавления вопросов в state: {data=}')  
        cursor.change_data(data)
        # Отправляем первый закрытый вопрос
        logger.info(f'[kb_module_2_final_test_handler] Отправляем первый закрытый вопрос')
        current_course = cursor.get_data().get('current_course')
        if not current_course:
            current_course = await get_value_from_redis(callback.user_id, 'current_course')
        else:
            current_course = get_current_course(cursor)
        logger.info(f'{current_course=}')
        await send_question_step_12(callback, cursor, "module_2_final_test", "Обучение для конструкторов")

        cursor.change_state(TrainingStates.step_12_testing)
        

    except Exception as e:
        logger.error(f"[ERROR][kb_module_2_final_test_handler] Произошла ошибка {e}") 


@router.on_button_callback(state(TrainingStates.konstructor['module_3_lesson_1']), lambda data: data.payload.split('::')[1] == "not_first")
async def kb_module_3_lesson_1_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ - Модуль №3 Урок №1: Как принять задачу на запуск и сверить её со спецификацией"""
    try:
        logger.info("[kb_module_3_lesson_1_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
        
        await callback.message.delete()
        intro_text = get_module3_lesson1_intro_text_kb_branch()
        await callback.send(intro_text, disable_link_preview = True) 
        
        await asyncio.sleep(2) # 15
        
        course_name = await get_value_from_redis(callback.user_id, 'current_course')
        if not course_name:
            course_name = get_current_course(cursor)
        logger.info(f'{course_name=}')
        
        game = GamificationService(course_name)
        user_data = load_user_data()
        user_id = str(callback.user_id)
        first_name = user_data.get(user_id).get("first_name")
        last_name = user_data.get(user_id).get("second_name")
        
        await game.increment_lesson_func(
            user_id=user_id,
            course_name=course_name, # "Обучение по продажам"
            lesson_id='section_37', #  "section_1"
            user_data={
                "username": f'{first_name} {last_name}',
                "first_name": first_name,
                "last_name": last_name
            }
        )
                
        # сообщение о тестировании с кнопкой
        test_text = kb_go_to_test_after_lesson(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        cursor.change_state(TrainingStates.konstructor['module_3_lesson_1_questions'])
        await asyncio.sleep(2) # 2
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_3_lesson_1_questions'], 'payload': 'start_test', 'current_course': 'Обучение для конструкторов', 'status_user': status_user})
    except Exception as e:
        logger.error(f"[kb_module_3_lesson_1_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 


@router.on_button_callback(state(TrainingStates.konstructor['module_3_lesson_1_questions']), lambda data: data.payload == "start_test")
async def kb_module_3_lesson_1_test_handler(callback: Callback, cursor: FSMCursor):
    """ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ Начало тестирования МОДУЛЬ № 3 УРОК № 1 """
    try:
        logger.info("[kb_module_3_lesson_1_test_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}) 
        questions = get_testing_data_module_3_test_1_kb()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[kb_module_3_lesson_1_test_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
        logger.info(f'{callback=}')
        
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        else:
            await save_cursor(callback, extra_data=dict(questions=questions, current_question=0, answers=[]))
        
            
        logger.info(f'[kb_module_3_lesson_1_test_handler] после добавления вопросов в state: {data=}')  
        
        # Отправляем первый вопрос
        cursor.change_data(data)
        await send_question(callback, cursor, "section_39")
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.konstructor['module_3_lesson_1_testing']))
        else:
            await save_cursor(callback, extra_data=dict(state_name = TrainingStates.konstructor['module_3_lesson_1_testing']))
        cursor.change_state(TrainingStates.konstructor['module_3_lesson_1_testing'])
    
    except Exception as e:
        logger.error(f"[kb_module_3_lesson_1_test_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)
        

@router.on_button_callback(state(TrainingStates.konstructor['module_3_lesson_2']), lambda data: data.payload.split('::')[1] == "not_first")
async def kb_module_3_lesson_2_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ - Модуль №3 Урок №2: Как проверить размеры, цвет, заполнение, фурнитуру и примечания"""
    try:
        logger.info("[kb_module_3_lesson_2_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
        
        await callback.message.delete()
        intro_text = get_module3_lesson2_intro_text_kb_branch()
        await callback.send(intro_text, disable_link_preview = True) 
        
        await asyncio.sleep(2) # 15
        
        course_name = await get_value_from_redis(callback.user_id, 'current_course')
        if not course_name:
            course_name = get_current_course(cursor)
        logger.info(f'{course_name=}')
        
        game = GamificationService(course_name)
        user_data = load_user_data()
        user_id = str(callback.user_id)
        first_name = user_data.get(user_id).get("first_name")
        last_name = user_data.get(user_id).get("second_name")
        
        await game.increment_lesson_func(
            user_id=user_id,
            course_name=course_name, # "Обучение по продажам"
            lesson_id='section_39', #  "section_1"
            user_data={
                "username": f'{first_name} {last_name}',
                "first_name": first_name,
                "last_name": last_name
            }
        )
                
        # сообщение о тестировании с кнопкой
        test_text = kb_go_to_test_after_lesson(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        cursor.change_state(TrainingStates.konstructor['module_3_lesson_2_questions'])
        await asyncio.sleep(2) # 2
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_3_lesson_2_questions'], 'payload': 'start_test', 'current_course': 'Обучение для конструкторов', 'status_user': status_user})
    except Exception as e:
        logger.error(f"[kb_module_3_lesson_2_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 


@router.on_button_callback(state(TrainingStates.konstructor['module_3_lesson_2_questions']), lambda data: data.payload == "start_test")
async def kb_module_3_lesson_2_test_handler(callback: Callback, cursor: FSMCursor):
    """ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ Начало тестирования МОДУЛЬ № 3 УРОК № 2 """
    try:
        logger.info("[kb_module_3_lesson_2_test_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}) 
        questions = get_testing_data_module_3_test_2_kb()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[kb_module_3_lesson_2_test_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
        logger.info(f'{callback=}')
        
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        else:
            await save_cursor(callback, extra_data=dict(questions=questions, current_question=0, answers=[]))
        
            
        logger.info(f'[kb_module_3_lesson_2_test_handler] после добавления вопросов в state: {data=}')  
        
        # Отправляем первый вопрос
        cursor.change_data(data)
        await send_question(callback, cursor, "section_41")
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.konstructor['module_3_lesson_2_testing']))
        else:
            await save_cursor(callback, extra_data=dict(state_name = TrainingStates.konstructor['module_3_lesson_2_testing']))
        cursor.change_state(TrainingStates.konstructor['module_3_lesson_2_testing'])
    
    except Exception as e:
        logger.error(f"[kb_module_3_lesson_2_test_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)
        

@router.on_button_callback(state(TrainingStates.konstructor['module_3_lesson_3']), lambda data: data.payload.split('::')[1] == "not_first")
async def kb_module_3_lesson_3_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ - Модуль №3 Урок №3: Как подготовить пакет документов для производства"""
    try:
        logger.info("[kb_module_3_lesson_3_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
        
        await callback.message.delete()
        intro_text = get_module3_lesson3_intro_text_kb_branch()
        await callback.send(intro_text, disable_link_preview = True) 
        
        await asyncio.sleep(2) # 15
        
        course_name = await get_value_from_redis(callback.user_id, 'current_course')
        if not course_name:
            course_name = get_current_course(cursor)
        logger.info(f'{course_name=}')
        
        game = GamificationService(course_name)
        user_data = load_user_data()
        user_id = str(callback.user_id)
        first_name = user_data.get(user_id).get("first_name")
        last_name = user_data.get(user_id).get("second_name")
        
        await game.increment_lesson_func(
            user_id=user_id,
            course_name=course_name, # "Обучение по продажам"
            lesson_id='section_41', #  "section_1"
            user_data={
                "username": f'{first_name} {last_name}',
                "first_name": first_name,
                "last_name": last_name
            }
        )
                
        # сообщение о тестировании с кнопкой
        test_text = kb_go_to_test_after_lesson(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        cursor.change_state(TrainingStates.konstructor['module_3_lesson_3_questions'])
        await asyncio.sleep(2) # 2
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_3_lesson_3_questions'], 'payload': 'start_test', 'current_course': 'Обучение для конструкторов', 'status_user': status_user})
    except Exception as e:
        logger.error(f"[kb_module_3_lesson_3_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 


@router.on_button_callback(state(TrainingStates.konstructor['module_3_lesson_3_questions']), lambda data: data.payload == "start_test")
async def kb_module_3_lesson_3_test_handler(callback: Callback, cursor: FSMCursor):
    """ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ Начало тестирования МОДУЛЬ № 3 УРОК № 3 """
    try:
        logger.info("[kb_module_3_lesson_3_test_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}) 
        questions = get_testing_data_module_3_test_3_kb()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[kb_module_3_lesson_2_test_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
        logger.info(f'{callback=}')
        
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        else:
            await save_cursor(callback, extra_data=dict(questions=questions, current_question=0, answers=[]))
        
            
        logger.info(f'[kb_module_3_lesson_3_test_handler] после добавления вопросов в state: {data=}')  
        
        # Отправляем первый вопрос
        cursor.change_data(data)
        await send_question(callback, cursor, "section_43")
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.konstructor['module_3_lesson_3_testing']))
        else:
            await save_cursor(callback, extra_data=dict(state_name = TrainingStates.konstructor['module_3_lesson_3_testing']))
        cursor.change_state(TrainingStates.konstructor['module_3_lesson_3_testing'])
    
    except Exception as e:
        logger.error(f"[kb_module_3_lesson_3_test_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)         
         

@router.on_button_callback(state(TrainingStates.konstructor['module_3_lesson_4']), lambda data: data.payload.split('::')[1] == "not_first")
async def kb_module_3_lesson_4_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ - Модуль №3 Урок №4: Как сформировать и передать архив запуска в Битрикс24"""
    try:
        logger.info("[kb_module_3_lesson_4_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
        
        await callback.message.delete()
        intro_text = get_module3_lesson4_intro_text_kb_branch()
        await callback.send(intro_text, disable_link_preview = True) 
        
        await asyncio.sleep(2) # 15
        
        course_name = await get_value_from_redis(callback.user_id, 'current_course')
        if not course_name:
            course_name = get_current_course(cursor)
        logger.info(f'{course_name=}')
        
        game = GamificationService(course_name)
        user_data = load_user_data()
        user_id = str(callback.user_id)
        first_name = user_data.get(user_id).get("first_name")
        last_name = user_data.get(user_id).get("second_name")
        
        await game.increment_lesson_func(
            user_id=user_id,
            course_name=course_name, # "Обучение по продажам"
            lesson_id='section_43', #  "section_1"
            user_data={
                "username": f'{first_name} {last_name}',
                "first_name": first_name,
                "last_name": last_name
            }
        )
                
        # сообщение о тестировании с кнопкой
        test_text = kb_go_to_test_after_lesson(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        cursor.change_state(TrainingStates.konstructor['module_3_lesson_4_questions'])
        await asyncio.sleep(2) # 2
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_3_lesson_4_questions'], 'payload': 'start_test', 'current_course': 'Обучение для конструкторов', 'status_user': status_user})
    except Exception as e:
        logger.error(f"[kb_module_3_lesson_4_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 


@router.on_button_callback(state(TrainingStates.konstructor['module_3_lesson_4_questions']), lambda data: data.payload == "start_test")
async def kb_module_3_lesson_4_test_handler(callback: Callback, cursor: FSMCursor):
    """ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ Начало тестирования МОДУЛЬ № 3 УРОК № 4 """
    try:
        logger.info("[kb_module_3_lesson_4_test_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}) 
        questions = get_testing_data_module_3_test_4_kb()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[kb_module_3_lesson_4_test_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
        logger.info(f'{callback=}')
        
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        else:
            await save_cursor(callback, extra_data=dict(questions=questions, current_question=0, answers=[]))
        
            
        logger.info(f'[kb_module_3_lesson_4_test_handler] после добавления вопросов в state: {data=}')  
        
        # Отправляем первый вопрос
        cursor.change_data(data)
        await send_question(callback, cursor, "section_45")
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.konstructor['module_3_lesson_4_testing']))
        else:
            await save_cursor(callback, extra_data=dict(state_name = TrainingStates.konstructor['module_3_lesson_4_testing']))
        cursor.change_state(TrainingStates.konstructor['module_3_lesson_4_testing'])
    
    except Exception as e:
        logger.error(f"[kb_module_3_lesson_4_test_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)
        

@router.on_button_callback(state(TrainingStates.konstructor['module_3_lesson_5']), lambda data: data.payload.split('::')[1] == "not_first")
async def kb_module_3_lesson_5_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ - Модуль №3 Урок №5: Как запускать нестандартные конструкции и нестандартную фурнитуру"""
    try:
        logger.info("[kb_module_3_lesson_5_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
        
        await callback.message.delete()
        intro_text = get_module3_lesson5_intro_text_kb_branch()
        await callback.send(intro_text, disable_link_preview = True) 
        
        await asyncio.sleep(2) # 15
        
        course_name = await get_value_from_redis(callback.user_id, 'current_course')
        if not course_name:
            course_name = get_current_course(cursor)
        logger.info(f'{course_name=}')
        
        game = GamificationService(course_name)
        user_data = load_user_data()
        user_id = str(callback.user_id)
        first_name = user_data.get(user_id).get("first_name")
        last_name = user_data.get(user_id).get("second_name")
        
        await game.increment_lesson_func(
            user_id=user_id,
            course_name=course_name, # "Обучение по продажам"
            lesson_id='section_45', #  "section_1"
            user_data={
                "username": f'{first_name} {last_name}',
                "first_name": first_name,
                "last_name": last_name
            }
        )
                
        # сообщение о тестировании с кнопкой
        test_text = kb_go_to_test_after_lesson(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        cursor.change_state(TrainingStates.konstructor['module_3_lesson_5_questions'])
        await asyncio.sleep(2) # 2
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_3_lesson_5_questions'], 'payload': 'start_test', 'current_course': 'Обучение для конструкторов', 'status_user': status_user})
    except Exception as e:
        logger.error(f"[kb_module_3_lesson_5_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 


@router.on_button_callback(state(TrainingStates.konstructor['module_3_lesson_5_questions']), lambda data: data.payload == "start_test")
async def kb_module_3_lesson_5_test_handler(callback: Callback, cursor: FSMCursor):
    """ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ Начало тестирования МОДУЛЬ № 3 УРОК № 5 """
    try:
        logger.info("[kb_module_3_lesson_5_test_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}) 
        questions = get_testing_data_module_3_test_5_kb()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[kb_module_3_lesson_5_test_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
        logger.info(f'{callback=}')
        
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        else:
            await save_cursor(callback, extra_data=dict(questions=questions, current_question=0, answers=[]))
        
            
        logger.info(f'[kb_module_3_lesson_5_test_handler] после добавления вопросов в state: {data=}')  
        
        # Отправляем первый вопрос
        cursor.change_data(data)
        await send_question(callback, cursor, "section_47")
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.konstructor['module_3_lesson_5_testing']))
        else:
            await save_cursor(callback, extra_data=dict(state_name = TrainingStates.konstructor['module_3_lesson_5_testing']))
        cursor.change_state(TrainingStates.konstructor['module_3_lesson_5_testing'])
    
    except Exception as e:
        logger.error(f"[kb_module_3_lesson_5_test_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)


@router.on_button_callback(state(TrainingStates.konstructor['module_3_lesson_5_testing']), lambda data: data.payload.split('::')[1] == "not_first")
async def continue_after_kb_module_3_handler(callback: Callback, cursor: FSMCursor):
    """Завершение Модуля №3 - КБ. Переход к вопросам или финальному тесту"""
    try:
        logger.info(f"[continue_after_kb_module_3_handler] Стартовал")
        await callback.message.delete()
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        # Проверяем загрузку базы знаний
        rag = RAGService()
        stats = rag.get_stats()
        
        cursor_data = cursor.get_data()
                
        if not stats['is_loaded']:
            await callback.send(
                "❌ База знаний не загружена. Обратитесь к администратору.",
                keyboard=main_menu_keyboard(current_course)
            )
            cursor.clear()
            return
        
        text = kb_get_text_to_final_test_module_3()
                
        await callback.send(text, keyboard=final_start_test_kb())
        cursor.change_state(TrainingStates.konstructor['module_3_questions'])
        await save_cursor(callback.user_id, extra_data = {'payload': 'to_final_test', 'state_name': TrainingStates.konstructor['module_3_questions'], 'current_course': current_course})
    
    except Exception as e:
        logger.error(f"[continue_after_kb_module_3_handler] Произошла ошибка {e}")
        

@router.on_button_callback(state(TrainingStates.konstructor['module_3_questions']), lambda data: data.payload == "to_final_test")
async def kb_module_3_final_test_handler(callback: Callback, cursor: FSMCursor):
    '''Заглушка для прохождения финального теста по модулю № 3'''
    try:
        logger.info("[kb_module_3_final_test_handler] Стартовал")
        # ЧАСТЬ 1: Закрытые вопросы (10 вопросов с вариантами A/B/C/D)
        closed_questions = get_final_testing_data_module_3_kb('close')
        logger.info(f"[INFO][kb_module_3_final_test_handler] {closed_questions=}")
        
        # ЧАСТЬ 2: Открытые вопросы (5 вопросов с эталонными ответами)
        open_questions = get_final_testing_data_module_3_kb('open')
        logger.info(f"[INFO][kb_module_3_final_test_handler] {open_questions=}")
        
        data = cursor.get_data()
        logger.info(f'[kb_module_3_final_test_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
    
        if data and isinstance(data, dict):
                data.update(
                    closed_questions=closed_questions,
                    open_questions=open_questions,
                    current_question=0,
                    closed_answers=[],  # Ответы на закрытые вопросы
                    open_answers=[],    # Ответы на открытые вопросы
                    test_stage="closed",  # Начинаем с закрытых вопросов
                    migration_state = "module_3_final_testing",
                    current_course='Обучение для конструкторов'
                    )
                await save_cursor(callback.user_id, extra_data = dict(
                    closed_questions=closed_questions,
                    open_questions=open_questions,
                    current_question=0,
                    closed_answers=[],  # Ответы на закрытые вопросы
                    open_answers=[],    # Ответы на открытые вопросы
                    test_stage="closed",  # Начинаем с закрытых вопросов
                    migration_state = "module_3_final_testing",
                    current_course='Обучение для конструкторов'
                ))
        else:
            data = dict()
            data.update(
                closed_questions=closed_questions,
                open_questions=open_questions,
                current_question=0,
                closed_answers=[],  # Ответы на закрытые вопросы
                open_answers=[],    # Ответы на открытые вопросы
                test_stage="closed",  # Начинаем с закрытых вопросов
                migration_state = "module_3_final_testing",
                current_course='Обучение для конструкторов'
                )
            await save_cursor(callback.user_id, extra_data = dict(
                    closed_questions=closed_questions,
                    open_questions=open_questions,
                    current_question=0,
                    closed_answers=[],  # Ответы на закрытые вопросы
                    open_answers=[],    # Ответы на открытые вопросы
                    test_stage="closed",  # Начинаем с закрытых вопросов
                    migration_state = "module_3_final_testing",
                    current_course='Обучение для конструкторов'
                ))
            
        logger.info(f'[kb_module_3_final_test_handler] после добавления вопросов в state: {data=}')  
        cursor.change_data(data)
        # Отправляем первый закрытый вопрос
        logger.info(f'[kb_module_3_final_test_handler] Отправляем первый закрытый вопрос')
        current_course = cursor.get_data().get('current_course')
        if not current_course:
            current_course = await get_value_from_redis(callback.user_id, 'current_course')
        else:
            current_course = get_current_course(cursor)
        logger.info(f'{current_course=}')
        await send_question_step_12(callback, cursor, "module_3_final_test", "Обучение для конструкторов")

        cursor.change_state(TrainingStates.step_12_testing)
        

    except Exception as e:
        logger.error(f"[ERROR][kb_module_3_final_test_handler] Произошла ошибка {e}") 


@router.on_button_callback(state(TrainingStates.konstructor['module_4_lesson_1']), lambda data: data.payload.split('::')[1] == "not_first")
async def kb_module_4_lesson_1_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ - Модуль №4 Урок №1: Урок №1. Как подготовить заявку на материал для снабжения"""
    try:
        logger.info("[kb_module_4_lesson_1_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
        
        await callback.message.delete()
        intro_text = get_module4_lesson1_intro_text_kb_branch()
        await callback.send(intro_text, disable_link_preview = True) 
        
        await asyncio.sleep(2) # 15
        
        course_name = await get_value_from_redis(callback.user_id, 'current_course')
        if not course_name:
            course_name = get_current_course(cursor)
        logger.info(f'{course_name=}')
        
        game = GamificationService(course_name)
        user_data = load_user_data()
        user_id = str(callback.user_id)
        first_name = user_data.get(user_id).get("first_name")
        last_name = user_data.get(user_id).get("second_name")
        
        await game.increment_lesson_func(
            user_id=user_id,
            course_name=course_name, # "Обучение по продажам"
            lesson_id='section_48', #  "section_1"
            user_data={
                "username": f'{first_name} {last_name}',
                "first_name": first_name,
                "last_name": last_name
            }
        )
                
        # сообщение о тестировании с кнопкой
        test_text = kb_go_to_test_after_lesson(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        cursor.change_state(TrainingStates.konstructor['module_4_lesson_1_questions'])
        await asyncio.sleep(2) # 2
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_4_lesson_1_questions'], 'payload': 'start_test', 'current_course': 'Обучение для конструкторов', 'status_user': status_user})
    except Exception as e:
        logger.error(f"[kb_module_4_lesson_1_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 


@router.on_button_callback(state(TrainingStates.konstructor['module_4_lesson_1_questions']), lambda data: data.payload == "start_test")
async def kb_module_4_lesson_1_test_handler(callback: Callback, cursor: FSMCursor):
    """ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ Начало тестирования МОДУЛЬ № 4 УРОК № 1 """
    try:
        logger.info("[kb_module_4_lesson_1_test_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}) 
        questions = get_testing_data_module_4_test_1_kb()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[kb_module_4_lesson_1_test_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
        logger.info(f'{callback=}')
        
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        else:
            await save_cursor(callback, extra_data=dict(questions=questions, current_question=0, answers=[]))
        
            
        logger.info(f'[kb_module_4_lesson_1_test_handler] после добавления вопросов в state: {data=}')  
        
        # Отправляем первый вопрос
        cursor.change_data(data)
        await send_question(callback, cursor, "section_50")
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.konstructor['module_4_lesson_1_testing']))
        else:
            await save_cursor(callback, extra_data=dict(state_name = TrainingStates.konstructor['module_4_lesson_1_testing']))
        cursor.change_state(TrainingStates.konstructor['module_4_lesson_1_testing'])
    
    except Exception as e:
        logger.error(f"[kb_module_4_lesson_1_test_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)
        

@router.on_button_callback(state(TrainingStates.konstructor['module_4_lesson_2']), lambda data: data.payload.split('::')[1] == "not_first")
async def kb_module_4_lesson_2_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ - Модуль №4 Урок №2: Как проверить цвет, фурнитуру и нестандартные комплектующие"""
    try:
        logger.info("[kb_module_4_lesson_2_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
        
        await callback.message.delete()
        intro_text = get_module4_lesson2_intro_text_kb_branch()
        await callback.send(intro_text, disable_link_preview = True) 
        
        await asyncio.sleep(2) # 15
        
        course_name = await get_value_from_redis(callback.user_id, 'current_course')
        if not course_name:
            course_name = get_current_course(cursor)
        logger.info(f'{course_name=}')
        
        game = GamificationService(course_name)
        user_data = load_user_data()
        user_id = str(callback.user_id)
        first_name = user_data.get(user_id).get("first_name")
        last_name = user_data.get(user_id).get("second_name")
        
        await game.increment_lesson_func(
            user_id=user_id,
            course_name=course_name, # "Обучение по продажам"
            lesson_id='section_50', #  "section_1"
            user_data={
                "username": f'{first_name} {last_name}',
                "first_name": first_name,
                "last_name": last_name
            }
        )
                
        # сообщение о тестировании с кнопкой
        test_text = kb_go_to_test_after_lesson(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        cursor.change_state(TrainingStates.konstructor['module_4_lesson_2_questions'])
        await asyncio.sleep(2) # 2
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_4_lesson_2_questions'], 'payload': 'start_test', 'current_course': 'Обучение для конструкторов', 'status_user': status_user})
    except Exception as e:
        logger.error(f"[kb_module_4_lesson_2_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 


@router.on_button_callback(state(TrainingStates.konstructor['module_4_lesson_2_questions']), lambda data: data.payload == "start_test")
async def kb_module_4_lesson_2_test_handler(callback: Callback, cursor: FSMCursor):
    """ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ Начало тестирования МОДУЛЬ № 4 УРОК № 2 """
    try:
        logger.info("[kb_module_4_lesson_2_test_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}) 
        questions = get_testing_data_module_4_test_2_kb()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[kb_module_4_lesson_2_test_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
        logger.info(f'{callback=}')
        
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        else:
            await save_cursor(callback, extra_data=dict(questions=questions, current_question=0, answers=[]))
        
            
        logger.info(f'[kb_module_4_lesson_1_test_handler] после добавления вопросов в state: {data=}')  
        
        # Отправляем первый вопрос
        cursor.change_data(data)
        await send_question(callback, cursor, "section_52")
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.konstructor['module_4_lesson_2_testing']))
        else:
            await save_cursor(callback, extra_data=dict(state_name = TrainingStates.konstructor['module_4_lesson_2_testing']))
        cursor.change_state(TrainingStates.konstructor['module_4_lesson_2_testing'])
    
    except Exception as e:
        logger.error(f"[kb_module_4_lesson_2_test_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)
        

@router.on_button_callback(state(TrainingStates.konstructor['module_4_lesson_3']), lambda data: data.payload.split('::')[1] == "not_first")
async def kb_module_4_lesson_3_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ - Модуль №4 Урок №3: Как запросить сроки / стоимость и передать информацию менеджеру"""
    try:
        logger.info("[kb_module_4_lesson_3_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
        
        await callback.message.delete()
        intro_text = get_module4_lesson3_intro_text_kb_branch()
        await callback.send(intro_text, disable_link_preview = True) 
        
        await asyncio.sleep(2) # 15
        
        course_name = await get_value_from_redis(callback.user_id, 'current_course')
        if not course_name:
            course_name = get_current_course(cursor)
        logger.info(f'{course_name=}')
        
        game = GamificationService(course_name)
        user_data = load_user_data()
        user_id = str(callback.user_id)
        first_name = user_data.get(user_id).get("first_name")
        last_name = user_data.get(user_id).get("second_name")
        
        await game.increment_lesson_func(
            user_id=user_id,
            course_name=course_name, # "Обучение по продажам"
            lesson_id='section_52', #  "section_1"
            user_data={
                "username": f'{first_name} {last_name}',
                "first_name": first_name,
                "last_name": last_name
            }
        )
                
        # сообщение о тестировании с кнопкой
        test_text = kb_go_to_test_after_lesson(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        cursor.change_state(TrainingStates.konstructor['module_4_lesson_3_questions'])
        await asyncio.sleep(2) # 2
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_4_lesson_3_questions'], 'payload': 'start_test', 'current_course': 'Обучение для конструкторов', 'status_user': status_user})
    except Exception as e:
        logger.error(f"[kb_module_4_lesson_3_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 


@router.on_button_callback(state(TrainingStates.konstructor['module_4_lesson_3_questions']), lambda data: data.payload == "start_test")
async def kb_module_4_lesson_3_test_handler(callback: Callback, cursor: FSMCursor):
    """ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ Начало тестирования МОДУЛЬ № 4 УРОК № 3 """
    try:
        logger.info("[kb_module_4_lesson_3_test_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}) 
        questions = get_testing_data_module_4_test_3_kb()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[kb_module_4_lesson_3_test_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
        logger.info(f'{callback=}')
        
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        else:
            await save_cursor(callback, extra_data=dict(questions=questions, current_question=0, answers=[]))
        
            
        logger.info(f'[kb_module_4_lesson_3_test_handler] после добавления вопросов в state: {data=}')  
        
        # Отправляем первый вопрос
        cursor.change_data(data)
        await send_question(callback, cursor, "section_54")
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.konstructor['module_4_lesson_3_testing']))
        else:
            await save_cursor(callback, extra_data=dict(state_name = TrainingStates.konstructor['module_4_lesson_3_testing']))
        cursor.change_state(TrainingStates.konstructor['module_4_lesson_3_testing'])
    
    except Exception as e:
        logger.error(f"[kb_module_4_lesson_3_test_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)
        

@router.on_button_callback(state(TrainingStates.konstructor['module_4_lesson_4']), lambda data: data.payload.split('::')[1] == "not_first")
async def kb_module_4_lesson_4_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ - Модуль №4 Урок №4: Что делать, если материал недоступен или сроки не подходят"""
    try:
        logger.info("[kb_module_4_lesson_4_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
        
        await callback.message.delete()
        intro_text = get_module4_lesson4_intro_text_kb_branch()
        await callback.send(intro_text, disable_link_preview = True) 
        
        await asyncio.sleep(2) # 15
        
        course_name = await get_value_from_redis(callback.user_id, 'current_course')
        if not course_name:
            course_name = get_current_course(cursor)
        logger.info(f'{course_name=}')
        
        game = GamificationService(course_name)
        user_data = load_user_data()
        user_id = str(callback.user_id)
        first_name = user_data.get(user_id).get("first_name")
        last_name = user_data.get(user_id).get("second_name")
        
        await game.increment_lesson_func(
            user_id=user_id,
            course_name=course_name, # "Обучение по продажам"
            lesson_id='section_55', #  "section_1"
            user_data={
                "username": f'{first_name} {last_name}',
                "first_name": first_name,
                "last_name": last_name
            }
        )
                
        # сообщение о тестировании с кнопкой
        test_text = kb_go_to_test_after_lesson(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        cursor.change_state(TrainingStates.konstructor['module_4_lesson_4_questions'])
        await asyncio.sleep(2) # 2
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_4_lesson_4_questions'], 'payload': 'start_test', 'current_course': 'Обучение для конструкторов', 'status_user': status_user})
    except Exception as e:
        logger.error(f"[kb_module_4_lesson_4_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 


@router.on_button_callback(state(TrainingStates.konstructor['module_4_lesson_4_questions']), lambda data: data.payload == "start_test")
async def kb_module_4_lesson_4_test_handler(callback: Callback, cursor: FSMCursor):
    """ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ Начало тестирования МОДУЛЬ № 4 УРОК № 4 """
    try:
        logger.info("[kb_module_4_lesson_4_test_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}) 
        questions = get_testing_data_module_4_test_4_kb()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[kb_module_4_lesson_4_test_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
        logger.info(f'{callback=}')
        
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        else:
            await save_cursor(callback, extra_data=dict(questions=questions, current_question=0, answers=[]))
        
            
        logger.info(f'[kb_module_4_lesson_4_test_handler] после добавления вопросов в state: {data=}')  
        
        # Отправляем первый вопрос
        cursor.change_data(data)
        await send_question(callback, cursor, "section_56")
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.konstructor['module_4_lesson_4_testing']))
        else:
            await save_cursor(callback, extra_data=dict(state_name = TrainingStates.konstructor['module_4_lesson_4_testing']))
        cursor.change_state(TrainingStates.konstructor['module_4_lesson_4_testing'])
    
    except Exception as e:
        logger.error(f"[kb_module_4_lesson_4_test_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)


@router.on_button_callback(state(TrainingStates.konstructor['module_4_lesson_4_testing']), lambda data: data.payload.split('::')[1] == "not_first")
async def continue_after_kb_module_4_handler(callback: Callback, cursor: FSMCursor):
    """Завершение Модуля №4 - КБ. Переход к вопросам или финальному тесту"""
    try:
        logger.info(f"[continue_after_kb_module_4_handler] Стартовал")
        await callback.message.delete()
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        # Проверяем загрузку базы знаний
        rag = RAGService()
        stats = rag.get_stats()
        
        cursor_data = cursor.get_data()
                
        if not stats['is_loaded']:
            await callback.send(
                "❌ База знаний не загружена. Обратитесь к администратору.",
                keyboard=main_menu_keyboard(current_course)
            )
            cursor.clear()
            return
        
        text = kb_get_text_to_final_test_module_4()
                
        await callback.send(text, keyboard=final_start_test_kb())
        cursor.change_state(TrainingStates.konstructor['module_4_questions'])
        await save_cursor(callback.user_id, extra_data = {'payload': 'to_final_test', 'state_name': TrainingStates.konstructor['module_4_questions'], 'current_course': current_course})
    
    except Exception as e:
        logger.error(f"[continue_after_kb_module_4_handler] Произошла ошибка {e}")
        

@router.on_button_callback(state(TrainingStates.konstructor['module_4_questions']), lambda data: data.payload == "to_final_test")
async def kb_module_4_final_test_handler(callback: Callback, cursor: FSMCursor):
    '''Заглушка для прохождения финального теста по модулю № 4'''
    try:
        logger.info("[kb_module_4_final_test_handler] Стартовал")
        # ЧАСТЬ 1: Закрытые вопросы (10 вопросов с вариантами A/B/C/D)
        closed_questions = get_final_testing_data_module_4_kb('close')
        logger.info(f"[INFO][kb_module_4_final_test_handler] {closed_questions=}")
        
        # ЧАСТЬ 2: Открытые вопросы (5 вопросов с эталонными ответами)
        open_questions = get_final_testing_data_module_4_kb('open')
        logger.info(f"[INFO][kb_module_4_final_test_handler] {open_questions=}")
        
        data = cursor.get_data()
        logger.info(f'[kb_module_4_final_test_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
    
        if data and isinstance(data, dict):
                data.update(
                    closed_questions=closed_questions,
                    open_questions=open_questions,
                    current_question=0,
                    closed_answers=[],  # Ответы на закрытые вопросы
                    open_answers=[],    # Ответы на открытые вопросы
                    test_stage="closed",  # Начинаем с закрытых вопросов
                    migration_state = "module_4_final_testing",
                    current_course='Обучение для конструкторов'
                    )
                await save_cursor(callback.user_id, extra_data = dict(
                    closed_questions=closed_questions,
                    open_questions=open_questions,
                    current_question=0,
                    closed_answers=[],  # Ответы на закрытые вопросы
                    open_answers=[],    # Ответы на открытые вопросы
                    test_stage="closed",  # Начинаем с закрытых вопросов
                    migration_state = "module_4_final_testing",
                    current_course='Обучение для конструкторов'
                ))
        else:
            data = dict()
            data.update(
                closed_questions=closed_questions,
                open_questions=open_questions,
                current_question=0,
                closed_answers=[],  # Ответы на закрытые вопросы
                open_answers=[],    # Ответы на открытые вопросы
                test_stage="closed",  # Начинаем с закрытых вопросов
                migration_state = "module_4_final_testing",
                current_course='Обучение для конструкторов'
                )
            await save_cursor(callback.user_id, extra_data = dict(
                    closed_questions=closed_questions,
                    open_questions=open_questions,
                    current_question=0,
                    closed_answers=[],  # Ответы на закрытые вопросы
                    open_answers=[],    # Ответы на открытые вопросы
                    test_stage="closed",  # Начинаем с закрытых вопросов
                    migration_state = "module_4_final_testing",
                    current_course='Обучение для конструкторов'
                ))
            
        logger.info(f'[kb_module_4_final_test_handler] после добавления вопросов в state: {data=}')  
        cursor.change_data(data)
        # Отправляем первый закрытый вопрос
        logger.info(f'[kb_module_4_final_test_handler] Отправляем первый закрытый вопрос')
        current_course = cursor.get_data().get('current_course')
        if not current_course:
            current_course = await get_value_from_redis(callback.user_id, 'current_course')
        else:
            current_course = get_current_course(cursor)
        logger.info(f'{current_course=}')
        await send_question_step_12(callback, cursor, "module_4_final_test", "Обучение для конструкторов")

        cursor.change_state(TrainingStates.step_12_testing)
        

    except Exception as e:
        logger.error(f"[ERROR][kb_module_4_final_test_handler] Произошла ошибка {e}") 
        

@router.on_button_callback(state(TrainingStates.konstructor['module_5_questions']), lambda data: data.payload == "to_final_test")
async def kb_module_5_final_test_handler(callback: Callback, cursor: FSMCursor):
    '''Заглушка для прохождения финального теста по модулю № 5'''
    try:
        logger.info("[kb_module_5_final_test_handler] Стартовал")
        # ЧАСТЬ 1: Закрытые вопросы (10 вопросов с вариантами A/B/C/D)
        closed_questions = get_final_testing_data_module_5_kb('close')
        logger.info(f"[INFO][kb_module_4_final_test_handler] {closed_questions=}")
        
        # ЧАСТЬ 2: Открытые вопросы (5 вопросов с эталонными ответами)
        open_questions = get_final_testing_data_module_5_kb('open')
        logger.info(f"[INFO][kb_module_5_final_test_handler] {open_questions=}")
        
        data = cursor.get_data()
        logger.info(f'[kb_module_5_final_test_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
    
        if data and isinstance(data, dict):
                data.update(
                    closed_questions=closed_questions,
                    open_questions=open_questions,
                    current_question=0,
                    closed_answers=[],  # Ответы на закрытые вопросы
                    open_answers=[],    # Ответы на открытые вопросы
                    test_stage="closed",  # Начинаем с закрытых вопросов
                    migration_state = "module_5_final_testing",
                    current_course='Обучение для конструкторов'
                    )
                await save_cursor(callback.user_id, extra_data = dict(
                    closed_questions=closed_questions,
                    open_questions=open_questions,
                    current_question=0,
                    closed_answers=[],  # Ответы на закрытые вопросы
                    open_answers=[],    # Ответы на открытые вопросы
                    test_stage="closed",  # Начинаем с закрытых вопросов
                    migration_state = "module_5_final_testing",
                    current_course='Обучение для конструкторов'
                ))
        else:
            data = dict()
            data.update(
                closed_questions=closed_questions,
                open_questions=open_questions,
                current_question=0,
                closed_answers=[],  # Ответы на закрытые вопросы
                open_answers=[],    # Ответы на открытые вопросы
                test_stage="closed",  # Начинаем с закрытых вопросов
                migration_state = "module_5_final_testing",
                current_course='Обучение для конструкторов'
                )
            await save_cursor(callback.user_id, extra_data = dict(
                    closed_questions=closed_questions,
                    open_questions=open_questions,
                    current_question=0,
                    closed_answers=[],  # Ответы на закрытые вопросы
                    open_answers=[],    # Ответы на открытые вопросы
                    test_stage="closed",  # Начинаем с закрытых вопросов
                    migration_state = "module_5_final_testing",
                    current_course='Обучение для конструкторов'
                ))
            
        logger.info(f'[kb_module_5_final_test_handler] после добавления вопросов в state: {data=}')  
        cursor.change_data(data)
        # Отправляем первый закрытый вопрос
        logger.info(f'[kb_module_5_final_test_handler] Отправляем первый закрытый вопрос')
        current_course = cursor.get_data().get('current_course')
        if not current_course:
            current_course = await get_value_from_redis(callback.user_id, 'current_course')
        else:
            current_course = get_current_course(cursor)
        logger.info(f'{current_course=}')
        await send_question_step_12(callback, cursor, "module_5_final_test", "Обучение для конструкторов")

        cursor.change_state(TrainingStates.step_12_testing)
        

    except Exception as e:
        logger.error(f"[ERROR][kb_module_5_final_test_handler] Произошла ошибка {e}")
        

@router.on_button_callback(state(TrainingStates.konstructor['module_6_questions']), lambda data: data.payload == "to_final_test")
async def kb_module_6_final_test_handler(callback: Callback, cursor: FSMCursor):
    '''Заглушка для прохождения финального теста по модулю № 6'''
    try:
        logger.info("[kb_module_6_final_test_handler] Стартовал")
        # ЧАСТЬ 1: Закрытые вопросы (10 вопросов с вариантами A/B/C/D)
        closed_questions = get_final_testing_data_module_6_kb('close')
        logger.info(f"[INFO][kb_module_4_final_test_handler] {closed_questions=}")
        
        # ЧАСТЬ 2: Открытые вопросы (5 вопросов с эталонными ответами)
        open_questions = get_final_testing_data_module_6_kb('open')
        logger.info(f"[INFO][kb_module_6_final_test_handler] {open_questions=}")
        
        data = cursor.get_data()
        logger.info(f'[kb_module_6_final_test_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
    
        if data and isinstance(data, dict):
                data.update(
                    closed_questions=closed_questions,
                    open_questions=open_questions,
                    current_question=0,
                    closed_answers=[],  # Ответы на закрытые вопросы
                    open_answers=[],    # Ответы на открытые вопросы
                    test_stage="closed",  # Начинаем с закрытых вопросов
                    migration_state = "module_6_final_testing",
                    current_course='Обучение для конструкторов'
                    )
                await save_cursor(callback.user_id, extra_data = dict(
                    closed_questions=closed_questions,
                    open_questions=open_questions,
                    current_question=0,
                    closed_answers=[],  # Ответы на закрытые вопросы
                    open_answers=[],    # Ответы на открытые вопросы
                    test_stage="closed",  # Начинаем с закрытых вопросов
                    migration_state = "module_6_final_testing",
                    current_course='Обучение для конструкторов'
                ))
        else:
            data = dict()
            data.update(
                closed_questions=closed_questions,
                open_questions=open_questions,
                current_question=0,
                closed_answers=[],  # Ответы на закрытые вопросы
                open_answers=[],    # Ответы на открытые вопросы
                test_stage="closed",  # Начинаем с закрытых вопросов
                migration_state = "module_6_final_testing",
                current_course='Обучение для конструкторов'
                )
            await save_cursor(callback.user_id, extra_data = dict(
                    closed_questions=closed_questions,
                    open_questions=open_questions,
                    current_question=0,
                    closed_answers=[],  # Ответы на закрытые вопросы
                    open_answers=[],    # Ответы на открытые вопросы
                    test_stage="closed",  # Начинаем с закрытых вопросов
                    migration_state = "module_6_final_testing",
                    current_course='Обучение для конструкторов'
                ))
            
        logger.info(f'[kb_module_6_final_test_handler] после добавления вопросов в state: {data=}')  
        cursor.change_data(data)
        # Отправляем первый закрытый вопрос
        logger.info(f'[kb_module_6_final_test_handler] Отправляем первый закрытый вопрос')
        current_course = cursor.get_data().get('current_course')
        if not current_course:
            current_course = await get_value_from_redis(callback.user_id, 'current_course')
        else:
            current_course = get_current_course(cursor)
        logger.info(f'{current_course=}')
        await send_question_step_12(callback, cursor, "module_6_final_test", "Обучение для конструкторов")

        cursor.change_state(TrainingStates.step_12_testing)
        

    except Exception as e:
        logger.error(f"[ERROR][kb_module_6_final_test_handler] Произошла ошибка {e}")
        

@router.on_button_callback(state(TrainingStates.konstructor['module_7_questions']), lambda data: data.payload == "to_final_test")
async def kb_module_7_final_test_handler(callback: Callback, cursor: FSMCursor):
    '''Заглушка для прохождения финального теста по модулю № 7'''
    try:
        logger.info("[kb_module_7_final_test_handler] Стартовал")
        # ЧАСТЬ 1: Закрытые вопросы (10 вопросов с вариантами A/B/C/D)
        closed_questions = get_final_testing_data_module_7_kb('close')
        logger.info(f"[INFO][kb_module_7_final_test_handler] {closed_questions=}")
        
        # ЧАСТЬ 2: Открытые вопросы (5 вопросов с эталонными ответами)
        open_questions = get_final_testing_data_module_7_kb('open')
        logger.info(f"[INFO][kb_module_7_final_test_handler] {open_questions=}")
        
        data = cursor.get_data()
        logger.info(f'[kb_module_7_final_test_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
    
        if data and isinstance(data, dict):
                data.update(
                    closed_questions=closed_questions,
                    open_questions=open_questions,
                    current_question=0,
                    closed_answers=[],  # Ответы на закрытые вопросы
                    open_answers=[],    # Ответы на открытые вопросы
                    test_stage="closed",  # Начинаем с закрытых вопросов
                    migration_state = "module_7_final_testing",
                    current_course='Обучение для конструкторов'
                    )
                await save_cursor(callback.user_id, extra_data = dict(
                    closed_questions=closed_questions,
                    open_questions=open_questions,
                    current_question=0,
                    closed_answers=[],  # Ответы на закрытые вопросы
                    open_answers=[],    # Ответы на открытые вопросы
                    test_stage="closed",  # Начинаем с закрытых вопросов
                    migration_state = "module_7_final_testing",
                    current_course='Обучение для конструкторов'
                ))
        else:
            data = dict()
            data.update(
                closed_questions=closed_questions,
                open_questions=open_questions,
                current_question=0,
                closed_answers=[],  # Ответы на закрытые вопросы
                open_answers=[],    # Ответы на открытые вопросы
                test_stage="closed",  # Начинаем с закрытых вопросов
                migration_state = "module_7_final_testing",
                current_course='Обучение для конструкторов'
                )
            await save_cursor(callback.user_id, extra_data = dict(
                    closed_questions=closed_questions,
                    open_questions=open_questions,
                    current_question=0,
                    closed_answers=[],  # Ответы на закрытые вопросы
                    open_answers=[],    # Ответы на открытые вопросы
                    test_stage="closed",  # Начинаем с закрытых вопросов
                    migration_state = "module_7_final_testing",
                    current_course='Обучение для конструкторов'
                ))
            
        logger.info(f'[kb_module_7_final_test_handler] после добавления вопросов в state: {data=}')  
        cursor.change_data(data)
        # Отправляем первый закрытый вопрос
        logger.info(f'[kb_module_7_final_test_handler] Отправляем первый закрытый вопрос')
        current_course = cursor.get_data().get('current_course')
        if not current_course:
            current_course = await get_value_from_redis(callback.user_id, 'current_course')
        else:
            current_course = get_current_course(cursor)
        logger.info(f'{current_course=}')
        await send_question_step_12(callback, cursor, "module_7_final_test", "Обучение для конструкторов")

        cursor.change_state(TrainingStates.step_12_testing)
        

    except Exception as e:
        logger.error(f"[ERROR][kb_module_7_final_test_handler] Произошла ошибка {e}")    


@router.on_button_callback(state(TrainingStates.konstructor['module_5_lesson_1']), lambda data: data.payload.split('::')[1] == "not_first")
async def kb_module_5_lesson_1_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ - Модуль №5 Урок №1: Как принять задачу на разработку КД и проверить исходные данные"""
    try:
        logger.info("[kb_module_5_lesson_1_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
        
        await callback.message.delete()
        intro_text = get_module5_lesson1_intro_text_kb_branch()
        await callback.send(intro_text, disable_link_preview = True) 
        
        await asyncio.sleep(2) # 15
        
        course_name = await get_value_from_redis(callback.user_id, 'current_course')
        if not course_name:
            course_name = get_current_course(cursor)
        logger.info(f'{course_name=}')
        
        game = GamificationService(course_name)
        user_data = load_user_data()
        user_id = str(callback.user_id)
        first_name = user_data.get(user_id).get("first_name")
        last_name = user_data.get(user_id).get("second_name")
        
        await game.increment_lesson_func(
            user_id=user_id,
            course_name=course_name, # "Обучение по продажам"
            lesson_id='section_57', #  "section_1"
            user_data={
                "username": f'{first_name} {last_name}',
                "first_name": first_name,
                "last_name": last_name
            }
        )
                
        # сообщение о тестировании с кнопкой
        test_text = kb_go_to_test_after_lesson(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        cursor.change_state(TrainingStates.konstructor['module_5_lesson_1_questions'])
        await asyncio.sleep(2) # 2
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_5_lesson_1_questions'], 'payload': 'start_test', 'current_course': 'Обучение для конструкторов', 'status_user': status_user})
    except Exception as e:
        logger.error(f"[kb_module_5_lesson_1_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 


@router.on_button_callback(state(TrainingStates.konstructor['module_5_lesson_1_questions']), lambda data: data.payload == "start_test")
async def kb_module_5_lesson_1_test_handler(callback: Callback, cursor: FSMCursor):
    """ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ Начало тестирования МОДУЛЬ № 5 УРОК № 1 """
    try:
        logger.info("[kb_module_5_lesson_1_test_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}) 
        questions = get_testing_data_module_5_test_1_kb()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[kb_module_5_lesson_1_test_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
        logger.info(f'{callback=}')
        
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        else:
            await save_cursor(callback, extra_data=dict(questions=questions, current_question=0, answers=[]))
        
            
        logger.info(f'[kb_module_5_lesson_1_test_handler] после добавления вопросов в state: {data=}')  
        
        # Отправляем первый вопрос
        cursor.change_data(data)
        await send_question(callback, cursor, "section_59")
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.konstructor['module_5_lesson_1_testing']))
        else:
            await save_cursor(callback, extra_data=dict(state_name = TrainingStates.konstructor['module_5_lesson_1_testing']))
        cursor.change_state(TrainingStates.konstructor['module_5_lesson_1_testing'])
    
    except Exception as e:
        logger.error(f"[kb_module_5_lesson_1_test_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)
        

@router.on_button_callback(state(TrainingStates.konstructor['module_5_lesson_2']), lambda data: data.payload.split('::')[1] == "not_first")
async def kb_module_5_lesson_2_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ - Модуль №5 Урок №2: Как подготовить чертежи, сечения и узлы в AutoCAD"""
    try:
        logger.info("[kb_module_5_lesson_2_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
        
        await callback.message.delete()
        intro_text = get_module5_lesson2_intro_text_kb_branch()
        await callback.send(intro_text, disable_link_preview = True) 
        
        await asyncio.sleep(2) # 15
        
        course_name = await get_value_from_redis(callback.user_id, 'current_course')
        if not course_name:
            course_name = get_current_course(cursor)
        logger.info(f'{course_name=}')
        
        game = GamificationService(course_name)
        user_data = load_user_data()
        user_id = str(callback.user_id)
        first_name = user_data.get(user_id).get("first_name")
        last_name = user_data.get(user_id).get("second_name")
        
        await game.increment_lesson_func(
            user_id=user_id,
            course_name=course_name, # "Обучение по продажам"
            lesson_id='section_59', #  "section_1"
            user_data={
                "username": f'{first_name} {last_name}',
                "first_name": first_name,
                "last_name": last_name
            }
        )
                
        # сообщение о тестировании с кнопкой
        test_text = kb_go_to_test_after_lesson(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        cursor.change_state(TrainingStates.konstructor['module_5_lesson_2_questions'])
        await asyncio.sleep(2) # 2
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_5_lesson_2_questions'], 'payload': 'start_test', 'current_course': 'Обучение для конструкторов', 'status_user': status_user})
    except Exception as e:
        logger.error(f"[kb_module_5_lesson_2_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 


@router.on_button_callback(state(TrainingStates.konstructor['module_5_lesson_2_questions']), lambda data: data.payload == "start_test")
async def kb_module_5_lesson_2_test_handler(callback: Callback, cursor: FSMCursor):
    """ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ Начало тестирования МОДУЛЬ № 5 УРОК № 2 """
    try:
        logger.info("[kb_module_5_lesson_2_test_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}) 
        questions = get_testing_data_module_5_test_2_kb()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[kb_module_5_lesson_2_test_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
        logger.info(f'{callback=}')
        
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        else:
            await save_cursor(callback, extra_data=dict(questions=questions, current_question=0, answers=[]))
        
            
        logger.info(f'[kb_module_5_lesson_2_test_handler] после добавления вопросов в state: {data=}')  
        
        # Отправляем первый вопрос
        cursor.change_data(data)
        await send_question(callback, cursor, "section_61")
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.konstructor['module_5_lesson_2_testing']))
        else:
            await save_cursor(callback, extra_data=dict(state_name = TrainingStates.konstructor['module_5_lesson_2_testing']))
        cursor.change_state(TrainingStates.konstructor['module_5_lesson_2_testing'])
    
    except Exception as e:
        logger.error(f"[kb_module_5_lesson_2_test_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)
        

@router.on_button_callback(state(TrainingStates.konstructor['module_5_lesson_3']), lambda data: data.payload.split('::')[1] == "not_first")
async def kb_module_5_lesson_3_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ - Модуль №5 Урок №3: Как оформить КМ / КМД и нестандартные чертежи"""
    try:
        logger.info("[kb_module_5_lesson_3_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
        
        await callback.message.delete()
        intro_text = get_module5_lesson3_intro_text_kb_branch()
        await callback.send(intro_text, disable_link_preview = True) 
        
        await asyncio.sleep(2) # 15
        
        course_name = await get_value_from_redis(callback.user_id, 'current_course')
        if not course_name:
            course_name = get_current_course(cursor)
        logger.info(f'{course_name=}')
        
        game = GamificationService(course_name)
        user_data = load_user_data()
        user_id = str(callback.user_id)
        first_name = user_data.get(user_id).get("first_name")
        last_name = user_data.get(user_id).get("second_name")
        
        await game.increment_lesson_func(
            user_id=user_id,
            course_name=course_name, # "Обучение по продажам"
            lesson_id='section_61', #  "section_1"
            user_data={
                "username": f'{first_name} {last_name}',
                "first_name": first_name,
                "last_name": last_name
            }
        )
                
        # сообщение о тестировании с кнопкой
        test_text = kb_go_to_test_after_lesson(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        cursor.change_state(TrainingStates.konstructor['module_5_lesson_3_questions'])
        await asyncio.sleep(2) # 2
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_5_lesson_3_questions'], 'payload': 'start_test', 'current_course': 'Обучение для конструкторов', 'status_user': status_user})
    except Exception as e:
        logger.error(f"[kb_module_5_lesson_3_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 


@router.on_button_callback(state(TrainingStates.konstructor['module_5_lesson_3_questions']), lambda data: data.payload == "start_test")
async def kb_module_5_lesson_3_test_handler(callback: Callback, cursor: FSMCursor):
    """ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ Начало тестирования МОДУЛЬ № 5 УРОК № 3 """
    try:
        logger.info("[kb_module_5_lesson_3_test_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}) 
        questions = get_testing_data_module_5_test_3_kb()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[kb_module_5_lesson_3_test_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
        logger.info(f'{callback=}')
        
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        else:
            await save_cursor(callback, extra_data=dict(questions=questions, current_question=0, answers=[]))
        
            
        logger.info(f'[kb_module_5_lesson_3_test_handler] после добавления вопросов в state: {data=}')  
        
        # Отправляем первый вопрос
        cursor.change_data(data)
        await send_question(callback, cursor, "section_63")
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.konstructor['module_5_lesson_3_testing']))
        else:
            await save_cursor(callback, extra_data=dict(state_name = TrainingStates.konstructor['module_5_lesson_3_testing']))
        cursor.change_state(TrainingStates.konstructor['module_5_lesson_3_testing'])
    
    except Exception as e:
        logger.error(f"[kb_module_5_lesson_3_test_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)
        

@router.on_button_callback(state(TrainingStates.konstructor['module_5_lesson_4']), lambda data: data.payload.split('::')[1] == "not_first")
async def kb_module_5_lesson_4_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ - Модуль №5 Урок №4: Как проверить комплект документации перед передачей"""
    try:
        logger.info("[kb_module_5_lesson_4_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
        
        await callback.message.delete()
        intro_text = get_module5_lesson3_intro_text_kb_branch()
        await callback.send(intro_text, disable_link_preview = True) 
        
        await asyncio.sleep(2) # 15
        
        course_name = await get_value_from_redis(callback.user_id, 'current_course')
        if not course_name:
            course_name = get_current_course(cursor)
        logger.info(f'{course_name=}')
        
        game = GamificationService(course_name)
        user_data = load_user_data()
        user_id = str(callback.user_id)
        first_name = user_data.get(user_id).get("first_name")
        last_name = user_data.get(user_id).get("second_name")
        
        await game.increment_lesson_func(
            user_id=user_id,
            course_name=course_name, # "Обучение по продажам"
            lesson_id='section_63', #  "section_1"
            user_data={
                "username": f'{first_name} {last_name}',
                "first_name": first_name,
                "last_name": last_name
            }
        )
                
        # сообщение о тестировании с кнопкой
        test_text = kb_go_to_test_after_lesson(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        cursor.change_state(TrainingStates.konstructor['module_5_lesson_4_questions'])
        await asyncio.sleep(2) # 2
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_5_lesson_4_questions'], 'payload': 'start_test', 'current_course': 'Обучение для конструкторов', 'status_user': status_user})
    except Exception as e:
        logger.error(f"[kb_module_5_lesson_4_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 


@router.on_button_callback(state(TrainingStates.konstructor['module_5_lesson_4_questions']), lambda data: data.payload == "start_test")
async def kb_module_5_lesson_4_test_handler(callback: Callback, cursor: FSMCursor):
    """ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ Начало тестирования МОДУЛЬ № 5 УРОК № 4 """
    try:
        logger.info("[kb_module_5_lesson_4_test_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}) 
        questions = get_testing_data_module_5_test_4_kb()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[kb_module_5_lesson_4_test_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
        logger.info(f'{callback=}')
        
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        else:
            await save_cursor(callback, extra_data=dict(questions=questions, current_question=0, answers=[]))
        
            
        logger.info(f'[kb_module_5_lesson_4_test_handler] после добавления вопросов в state: {data=}')  
        
        # Отправляем первый вопрос
        cursor.change_data(data)
        await send_question(callback, cursor, "section_65")
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.konstructor['module_5_lesson_4_testing']))
        else:
            await save_cursor(callback, extra_data=dict(state_name = TrainingStates.konstructor['module_5_lesson_4_testing']))
        cursor.change_state(TrainingStates.konstructor['module_5_lesson_4_testing'])
    
    except Exception as e:
        logger.error(f"[kb_module_5_lesson_4_test_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)
        

@router.on_button_callback(state(TrainingStates.konstructor['module_5_lesson_4_testing']), lambda data: data.payload.split('::')[1] == "not_first")
async def continue_after_kb_module_5_handler(callback: Callback, cursor: FSMCursor):
    """Завершение Модуля №5 - КБ. Переход к вопросам или финальному тесту"""
    try:
        logger.info(f"[continue_after_kb_module_5_handler] Стартовал")
        await callback.message.delete()
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        # Проверяем загрузку базы знаний
        rag = RAGService()
        stats = rag.get_stats()
        
        cursor_data = cursor.get_data()
                
        if not stats['is_loaded']:
            await callback.send(
                "❌ База знаний не загружена. Обратитесь к администратору.",
                keyboard=main_menu_keyboard(current_course)
            )
            cursor.clear()
            return
        
        text = kb_get_text_to_final_test_module_5()
                
        await callback.send(text, keyboard=final_start_test_kb())
        cursor.change_state(TrainingStates.konstructor['module_5_questions'])
        await save_cursor(callback.user_id, extra_data = {'payload': 'to_final_test', 'state_name': TrainingStates.konstructor['module_5_questions'], 'current_course': current_course})
    
    except Exception as e:
        logger.error(f"[continue_after_kb_module_5_handler] Произошла ошибка {e}")
        

async def kb_module_5_final_test_handler(callback: Callback, cursor: FSMCursor):
    '''Заглушка для прохождения финального теста по модулю № 5'''
    pass


@router.on_button_callback(state(TrainingStates.konstructor['module_6_lesson_1']), lambda data: data.payload.split('::')[1] == "not_first")
async def kb_module_6_lesson_1_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ - Модуль №6 Урок №1: Как определить потребность в монтажных материалах"""
    try:
        logger.info("[kb_module_6_lesson_1_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
        
        await callback.message.delete()
        intro_text = get_module6_lesson1_intro_text_kb_branch()
        await callback.send(intro_text, disable_link_preview = True) 
        
        await asyncio.sleep(2) # 15
        
        course_name = await get_value_from_redis(callback.user_id, 'current_course')
        if not course_name:
            course_name = get_current_course(cursor)
        logger.info(f'{course_name=}')
        
        game = GamificationService(course_name)
        user_data = load_user_data()
        user_id = str(callback.user_id)
        first_name = user_data.get(user_id).get("first_name")
        last_name = user_data.get(user_id).get("second_name")
        
        await game.increment_lesson_func(
            user_id=user_id,
            course_name=course_name, # "Обучение по продажам"
            lesson_id='section_66', #  "section_1"
            user_data={
                "username": f'{first_name} {last_name}',
                "first_name": first_name,
                "last_name": last_name
            }
        )
                
        # сообщение о тестировании с кнопкой
        test_text = kb_go_to_test_after_lesson(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        cursor.change_state(TrainingStates.konstructor['module_6_lesson_1_questions'])
        await asyncio.sleep(2) # 2
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_6_lesson_1_questions'], 'payload': 'start_test', 'current_course': 'Обучение для конструкторов', 'status_user': status_user})
    except Exception as e:
        logger.error(f"[kb_module_6_lesson_1_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 


@router.on_button_callback(state(TrainingStates.konstructor['module_6_lesson_1_questions']), lambda data: data.payload == "start_test")
async def kb_module_6_lesson_1_test_handler(callback: Callback, cursor: FSMCursor):
    """ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ Начало тестирования МОДУЛЬ № 6 УРОК № 1 """
    try:
        logger.info("[kb_module_6_lesson_1_test_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}) 
        questions = get_testing_data_module_6_test_1_kb()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[kb_module_6_lesson_1_test_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
        logger.info(f'{callback=}')
        
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        else:
            await save_cursor(callback, extra_data=dict(questions=questions, current_question=0, answers=[]))
        
            
        logger.info(f'[kb_module_6_lesson_1_test_handler] после добавления вопросов в state: {data=}')  
        
        # Отправляем первый вопрос
        cursor.change_data(data)
        await send_question(callback, cursor, "section_68")
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.konstructor['module_6_lesson_1_testing']))
        else:
            await save_cursor(callback, extra_data=dict(state_name = TrainingStates.konstructor['module_6_lesson_1_testing']))
        cursor.change_state(TrainingStates.konstructor['module_6_lesson_1_testing'])
    
    except Exception as e:
        logger.error(f"[kb_module_6_lesson_1_test_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)
        

@router.on_button_callback(state(TrainingStates.konstructor['module_6_lesson_2']), lambda data: data.payload.split('::')[1] == "not_first")
async def kb_module_6_lesson_2_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ - Модуль №6 Урок №2: Как подобрать крепёж, изоляцию, расходники и нащельники"""
    try:
        logger.info("[kb_module_6_lesson_2_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
        
        await callback.message.delete()
        intro_text = get_module6_lesson2_intro_text_kb_branch()
        await callback.send(intro_text, disable_link_preview = True) 
        
        await asyncio.sleep(2) # 15
        
        course_name = await get_value_from_redis(callback.user_id, 'current_course')
        if not course_name:
            course_name = get_current_course(cursor)
        logger.info(f'{course_name=}')
        
        game = GamificationService(course_name)
        user_data = load_user_data()
        user_id = str(callback.user_id)
        first_name = user_data.get(user_id).get("first_name")
        last_name = user_data.get(user_id).get("second_name")
        
        await game.increment_lesson_func(
            user_id=user_id,
            course_name=course_name, # "Обучение по продажам"
            lesson_id='section_68', #  "section_1"
            user_data={
                "username": f'{first_name} {last_name}',
                "first_name": first_name,
                "last_name": last_name
            }
        )
                
        # сообщение о тестировании с кнопкой
        test_text = kb_go_to_test_after_lesson(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        cursor.change_state(TrainingStates.konstructor['module_6_lesson_2_questions'])
        await asyncio.sleep(2) # 2
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_6_lesson_2_questions'], 'payload': 'start_test', 'current_course': 'Обучение для конструкторов', 'status_user': status_user})
    except Exception as e:
        logger.error(f"[kb_module_6_lesson_2_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 


@router.on_button_callback(state(TrainingStates.konstructor['module_6_lesson_2_questions']), lambda data: data.payload == "start_test")
async def kb_module_6_lesson_2_test_handler(callback: Callback, cursor: FSMCursor):
    """ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ Начало тестирования МОДУЛЬ № 6 УРОК № 2 """
    try:
        logger.info("[kb_module_6_lesson_2_test_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}) 
        questions = get_testing_data_module_6_test_2_kb()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[kb_module_6_lesson_2_test_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
        logger.info(f'{callback=}')
        
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        else:
            await save_cursor(callback, extra_data=dict(questions=questions, current_question=0, answers=[]))
        
            
        logger.info(f'[kb_module_6_lesson_2_test_handler] после добавления вопросов в state: {data=}')  
        
        # Отправляем первый вопрос
        cursor.change_data(data)
        await send_question(callback, cursor, "section_70")
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.konstructor['module_6_lesson_2_testing']))
        else:
            await save_cursor(callback, extra_data=dict(state_name = TrainingStates.konstructor['module_6_lesson_2_testing']))
        cursor.change_state(TrainingStates.konstructor['module_6_lesson_2_testing'])
    
    except Exception as e:
        logger.error(f"[kb_module_6_lesson_2_test_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)
        

@router.on_button_callback(state(TrainingStates.konstructor['module_6_lesson_3']), lambda data: data.payload.split('::')[1] == "not_first")
async def kb_module_6_lesson_3_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ - Модуль №6 Урок №3: Как рассчитать количество монтажных материалов"""
    try:
        logger.info("[kb_module_6_lesson_3_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
        
        await callback.message.delete()
        intro_text = get_module6_lesson3_intro_text_kb_branch()
        await callback.send(intro_text, disable_link_preview = True) 
        
        await asyncio.sleep(2) # 15
        
        course_name = await get_value_from_redis(callback.user_id, 'current_course')
        if not course_name:
            course_name = get_current_course(cursor)
        logger.info(f'{course_name=}')
        
        game = GamificationService(course_name)
        user_data = load_user_data()
        user_id = str(callback.user_id)
        first_name = user_data.get(user_id).get("first_name")
        last_name = user_data.get(user_id).get("second_name")
        
        await game.increment_lesson_func(
            user_id=user_id,
            course_name=course_name, # "Обучение по продажам"
            lesson_id='section_70', #  "section_1"
            user_data={
                "username": f'{first_name} {last_name}',
                "first_name": first_name,
                "last_name": last_name
            }
        )
                
        # сообщение о тестировании с кнопкой
        test_text = kb_go_to_test_after_lesson(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        cursor.change_state(TrainingStates.konstructor['module_6_lesson_3_questions'])
        await asyncio.sleep(2) # 2
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_6_lesson_3_questions'], 'payload': 'start_test', 'current_course': 'Обучение для конструкторов', 'status_user': status_user})
    except Exception as e:
        logger.error(f"[kb_module_6_lesson_3_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 


@router.on_button_callback(state(TrainingStates.konstructor['module_6_lesson_3_questions']), lambda data: data.payload == "start_test")
async def kb_module_6_lesson_3_test_handler(callback: Callback, cursor: FSMCursor):
    """ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ Начало тестирования МОДУЛЬ № 6 УРОК № 3 """
    try:
        logger.info("[kb_module_6_lesson_3_test_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}) 
        questions = get_testing_data_module_6_test_3_kb()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[kb_module_6_lesson_3_test_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
        logger.info(f'{callback=}')
        
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        else:
            await save_cursor(callback, extra_data=dict(questions=questions, current_question=0, answers=[]))
        
            
        logger.info(f'[kb_module_6_lesson_3_test_handler] после добавления вопросов в state: {data=}')  
        
        # Отправляем первый вопрос
        cursor.change_data(data)
        await send_question(callback, cursor, "section_72")
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.konstructor['module_6_lesson_3_testing']))
        else:
            await save_cursor(callback, extra_data=dict(state_name = TrainingStates.konstructor['module_6_lesson_3_testing']))
        cursor.change_state(TrainingStates.konstructor['module_6_lesson_3_testing'])
    
    except Exception as e:
        logger.error(f"[kb_module_6_lesson_3_test_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)
        

@router.on_button_callback(state(TrainingStates.konstructor['module_6_lesson_4']), lambda data: data.payload.split('::')[1] == "not_first")
async def kb_module_6_lesson_4_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ - Модуль №6 Урок №4: Как передать заявку в цех / ПТО / монтаж"""
    try:
        logger.info("[kb_module_6_lesson_4_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
        
        await callback.message.delete()
        intro_text = get_module6_lesson4_intro_text_kb_branch()
        await callback.send(intro_text, disable_link_preview = True) 
        
        await asyncio.sleep(2) # 15
        
        course_name = await get_value_from_redis(callback.user_id, 'current_course')
        if not course_name:
            course_name = get_current_course(cursor)
        logger.info(f'{course_name=}')
        
        game = GamificationService(course_name)
        user_data = load_user_data()
        user_id = str(callback.user_id)
        first_name = user_data.get(user_id).get("first_name")
        last_name = user_data.get(user_id).get("second_name")
        
        await game.increment_lesson_func(
            user_id=user_id,
            course_name=course_name, # "Обучение по продажам"
            lesson_id='section_72', #  "section_1"
            user_data={
                "username": f'{first_name} {last_name}',
                "first_name": first_name,
                "last_name": last_name
            }
        )
                
        # сообщение о тестировании с кнопкой
        test_text = kb_go_to_test_after_lesson(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        cursor.change_state(TrainingStates.konstructor['module_6_lesson_4_questions'])
        await asyncio.sleep(2) # 2
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_6_lesson_4_questions'], 'payload': 'start_test', 'current_course': 'Обучение для конструкторов', 'status_user': status_user})
    except Exception as e:
        logger.error(f"[kb_module_6_lesson_4_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 


@router.on_button_callback(state(TrainingStates.konstructor['module_6_lesson_4_questions']), lambda data: data.payload == "start_test")
async def kb_module_6_lesson_4_test_handler(callback: Callback, cursor: FSMCursor):
    """ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ Начало тестирования МОДУЛЬ № 6 УРОК № 4 """
    try:
        logger.info("[kb_module_6_lesson_4_test_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}) 
        questions = get_testing_data_module_6_test_4_kb()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[kb_module_6_lesson_4_test_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
        logger.info(f'{callback=}')
        
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        else:
            await save_cursor(callback, extra_data=dict(questions=questions, current_question=0, answers=[]))
        
            
        logger.info(f'[kb_module_6_lesson_4_test_handler] после добавления вопросов в state: {data=}')  
        
        # Отправляем первый вопрос
        cursor.change_data(data)
        await send_question(callback, cursor, "section_74")
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.konstructor['module_6_lesson_4_testing']))
        else:
            await save_cursor(callback, extra_data=dict(state_name = TrainingStates.konstructor['module_6_lesson_4_testing']))
        cursor.change_state(TrainingStates.konstructor['module_6_lesson_4_testing'])
    
    except Exception as e:
        logger.error(f"[kb_module_6_lesson_4_test_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)
        

@router.on_button_callback(state(TrainingStates.konstructor['module_6_lesson_4_testing']), lambda data: data.payload.split('::')[1] == "not_first")
async def continue_after_kb_module_6_handler(callback: Callback, cursor: FSMCursor):
    """Завершение Модуля №6 - КБ. Переход к вопросам или финальному тесту"""
    try:
        logger.info(f"[continue_after_kb_module_6_handler] Стартовал")
        await callback.message.delete()
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        # Проверяем загрузку базы знаний
        rag = RAGService()
        stats = rag.get_stats()
        
        cursor_data = cursor.get_data()
                
        if not stats['is_loaded']:
            await callback.send(
                "❌ База знаний не загружена. Обратитесь к администратору.",
                keyboard=main_menu_keyboard(current_course)
            )
            cursor.clear()
            return
        
        text = kb_get_text_to_final_test_module_6()
                
        await callback.send(text, keyboard=final_start_test_kb())
        cursor.change_state(TrainingStates.konstructor['module_6_questions'])
        await save_cursor(callback.user_id, extra_data = {'payload': 'to_final_test', 'state_name': TrainingStates.konstructor['module_6_questions'], 'current_course': current_course})
    
    except Exception as e:
        logger.error(f"[continue_after_kb_module_6_handler] Произошла ошибка {e}")
        

async def kb_module_6_final_test_handler(callback: Callback, cursor: FSMCursor):
    '''Заглушка для прохождения финального теста по модулю № 6'''
    pass


@router.on_button_callback(state(TrainingStates.konstructor['module_7_lesson_1']), lambda data: data.payload.split('::')[1] == "not_first")
async def kb_module_7_lesson_1_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ - Модуль №7 Урок №1: Как принять корректировку после запуска"""
    try:
        logger.info("[kb_module_7_lesson_1_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
        
        await callback.message.delete()
        intro_text = get_module7_lesson1_intro_text_kb_branch()
        await callback.send(intro_text, disable_link_preview = True) 
        
        await asyncio.sleep(2) # 15
        
        course_name = await get_value_from_redis(callback.user_id, 'current_course')
        if not course_name:
            course_name = get_current_course(cursor)
        logger.info(f'{course_name=}')
        
        game = GamificationService(course_name)
        user_data = load_user_data()
        user_id = str(callback.user_id)
        first_name = user_data.get(user_id).get("first_name")
        last_name = user_data.get(user_id).get("second_name")
        
        await game.increment_lesson_func(
            user_id=user_id,
            course_name=course_name, # "Обучение по продажам"
            lesson_id='section_75', #  "section_1"
            user_data={
                "username": f'{first_name} {last_name}',
                "first_name": first_name,
                "last_name": last_name
            }
        )
                
        # сообщение о тестировании с кнопкой
        test_text = kb_go_to_test_after_lesson(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        cursor.change_state(TrainingStates.konstructor['module_7_lesson_1_questions'])
        await asyncio.sleep(2) # 2
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_7_lesson_1_questions'], 'payload': 'start_test', 'current_course': 'Обучение для конструкторов', 'status_user': status_user})
    except Exception as e:
        logger.error(f"[kb_module_7_lesson_1_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 


@router.on_button_callback(state(TrainingStates.konstructor['module_7_lesson_1_questions']), lambda data: data.payload == "start_test")
async def kb_module_7_lesson_1_test_handler(callback: Callback, cursor: FSMCursor):
    """ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ Начало тестирования МОДУЛЬ № 7 УРОК № 1 """
    try:
        logger.info("[kb_module_7_lesson_1_test_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}) 
        questions = get_testing_data_module_7_test_1_kb()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[kb_module_7_lesson_1_test_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
        logger.info(f'{callback=}')
        
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        else:
            await save_cursor(callback, extra_data=dict(questions=questions, current_question=0, answers=[]))
        
            
        logger.info(f'[kb_module_7_lesson_1_test_handler] после добавления вопросов в state: {data=}')  
        
        # Отправляем первый вопрос
        cursor.change_data(data)
        await send_question(callback, cursor, "section_77")
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.konstructor['module_7_lesson_1_testing']))
        else:
            await save_cursor(callback, extra_data=dict(state_name = TrainingStates.konstructor['module_7_lesson_1_testing']))
        cursor.change_state(TrainingStates.konstructor['module_7_lesson_1_testing'])
    
    except Exception as e:
        logger.error(f"[kb_module_7_lesson_1_test_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)
        

@router.on_button_callback(state(TrainingStates.konstructor['module_7_lesson_2']), lambda data: data.payload.split('::')[1] == "not_first")
async def kb_module_7_lesson_2_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ - Модуль №7 Урок №2: Как понять, какие документы и файлы нужно обновить"""
    try:
        logger.info("[kb_module_7_lesson_2_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
        
        await callback.message.delete()
        intro_text = get_module7_lesson2_intro_text_kb_branch()
        await callback.send(intro_text, disable_link_preview = True) 
        
        await asyncio.sleep(2) # 15
        
        course_name = await get_value_from_redis(callback.user_id, 'current_course')
        if not course_name:
            course_name = get_current_course(cursor)
        logger.info(f'{course_name=}')
        
        game = GamificationService(course_name)
        user_data = load_user_data()
        user_id = str(callback.user_id)
        first_name = user_data.get(user_id).get("first_name")
        last_name = user_data.get(user_id).get("second_name")
        
        await game.increment_lesson_func(
            user_id=user_id,
            course_name=course_name, # "Обучение по продажам"
            lesson_id='section_77', #  "section_1"
            user_data={
                "username": f'{first_name} {last_name}',
                "first_name": first_name,
                "last_name": last_name
            }
        )
                
        # сообщение о тестировании с кнопкой
        test_text = kb_go_to_test_after_lesson(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        cursor.change_state(TrainingStates.konstructor['module_7_lesson_2_questions'])
        await asyncio.sleep(2) # 2
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_7_lesson_2_questions'], 'payload': 'start_test', 'current_course': 'Обучение для конструкторов', 'status_user': status_user})
    except Exception as e:
        logger.error(f"[kb_module_7_lesson_2_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 


@router.on_button_callback(state(TrainingStates.konstructor['module_7_lesson_2_questions']), lambda data: data.payload == "start_test")
async def kb_module_7_lesson_2_test_handler(callback: Callback, cursor: FSMCursor):
    """ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ Начало тестирования МОДУЛЬ № 7 УРОК № 2 """
    try:
        logger.info("[kb_module_7_lesson_2_test_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}) 
        questions = get_testing_data_module_7_test_2_kb()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[kb_module_7_lesson_2_test_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
        logger.info(f'{callback=}')
        
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        else:
            await save_cursor(callback, extra_data=dict(questions=questions, current_question=0, answers=[]))
        
            
        logger.info(f'[kb_module_7_lesson_2_test_handler] после добавления вопросов в state: {data=}')  
        
        # Отправляем первый вопрос
        cursor.change_data(data)
        await send_question(callback, cursor, "section_79")
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.konstructor['module_7_lesson_2_testing']))
        else:
            await save_cursor(callback, extra_data=dict(state_name = TrainingStates.konstructor['module_7_lesson_2_testing']))
        cursor.change_state(TrainingStates.konstructor['module_7_lesson_2_testing'])
    
    except Exception as e:
        logger.error(f"[kb_module_7_lesson_2_test_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)


@router.on_button_callback(state(TrainingStates.konstructor['module_7_lesson_3']), lambda data: data.payload.split('::')[1] == "not_first")
async def kb_module_7_lesson_3_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ - Модуль №7 Урок №3: Как заменить архив и уведомить производство / смежные отделы"""
    try:
        logger.info("[kb_module_7_lesson_3_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
        
        await callback.message.delete()
        intro_text = get_module7_lesson3_intro_text_kb_branch()
        await callback.send(intro_text, disable_link_preview = True) 
        
        await asyncio.sleep(2) # 15
        
        course_name = await get_value_from_redis(callback.user_id, 'current_course')
        if not course_name:
            course_name = get_current_course(cursor)
        logger.info(f'{course_name=}')
        
        game = GamificationService(course_name)
        user_data = load_user_data()
        user_id = str(callback.user_id)
        first_name = user_data.get(user_id).get("first_name")
        last_name = user_data.get(user_id).get("second_name")
        
        await game.increment_lesson_func(
            user_id=user_id,
            course_name=course_name, # "Обучение по продажам"
            lesson_id='section_79', #  "section_1"
            user_data={
                "username": f'{first_name} {last_name}',
                "first_name": first_name,
                "last_name": last_name
            }
        )
                
        # сообщение о тестировании с кнопкой
        test_text = kb_go_to_test_after_lesson(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        cursor.change_state(TrainingStates.konstructor['module_7_lesson_3_questions'])
        await asyncio.sleep(2) # 2
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_7_lesson_3_questions'], 'payload': 'start_test', 'current_course': 'Обучение для конструкторов', 'status_user': status_user})
    except Exception as e:
        logger.error(f"[kb_module_7_lesson_3_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 


@router.on_button_callback(state(TrainingStates.konstructor['module_7_lesson_3_questions']), lambda data: data.payload == "start_test")
async def kb_module_7_lesson_3_test_handler(callback: Callback, cursor: FSMCursor):
    """ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ Начало тестирования МОДУЛЬ № 7 УРОК № 3 """
    try:
        logger.info("[kb_module_7_lesson_3_test_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}) 
        questions = get_testing_data_module_7_test_3_kb()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[kb_module_7_lesson_3_test_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
        logger.info(f'{callback=}')
        
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        else:
            await save_cursor(callback, extra_data=dict(questions=questions, current_question=0, answers=[]))
        
            
        logger.info(f'[kb_module_7_lesson_3_test_handler] после добавления вопросов в state: {data=}')  
        
        # Отправляем первый вопрос
        cursor.change_data(data)
        await send_question(callback, cursor, "section_81")
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.konstructor['module_7_lesson_3_testing']))
        else:
            await save_cursor(callback, extra_data=dict(state_name = TrainingStates.konstructor['module_7_lesson_3_testing']))
        cursor.change_state(TrainingStates.konstructor['module_7_lesson_3_testing'])
    
    except Exception as e:
        logger.error(f"[kb_module_7_lesson_3_test_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)


@router.on_button_callback(state(TrainingStates.konstructor['module_7_lesson_4']), lambda data: data.payload.split('::')[1] == "not_first")
async def kb_module_7_lesson_4_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ - Модуль №7 Урок №4: Как проверить, что в работе актуальная версия"""
    try:
        logger.info("[kb_module_7_lesson_4_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        status_user = await get_value_from_redis(callback.user_id, 'status_user')
        if not status_user:
            if cursor.get_data():
                status_user = cursor.get_data().get('status_user')
        
        await callback.message.delete()
        intro_text = get_module7_lesson4_intro_text_kb_branch()
        await callback.send(intro_text, disable_link_preview = True) 
        
        await asyncio.sleep(2) # 15
        
        course_name = await get_value_from_redis(callback.user_id, 'current_course')
        if not course_name:
            course_name = get_current_course(cursor)
        logger.info(f'{course_name=}')
        
        game = GamificationService(course_name)
        user_data = load_user_data()
        user_id = str(callback.user_id)
        first_name = user_data.get(user_id).get("first_name")
        last_name = user_data.get(user_id).get("second_name")
        
        await game.increment_lesson_func(
            user_id=user_id,
            course_name=course_name, # "Обучение по продажам"
            lesson_id='section_81', #  "section_1"
            user_data={
                "username": f'{first_name} {last_name}',
                "first_name": first_name,
                "last_name": last_name
            }
        )
                
        # сообщение о тестировании с кнопкой
        test_text = kb_go_to_test_after_lesson(5)
        await callback.send(test_text, keyboard=start_test_kb())
        
        cursor.change_state(TrainingStates.konstructor['module_7_lesson_4_questions'])
        await asyncio.sleep(2) # 2
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.konstructor['module_7_lesson_4_questions'], 'payload': 'start_test', 'current_course': 'Обучение для конструкторов', 'status_user': status_user})
    except Exception as e:
        logger.error(f"[kb_module_7_lesson_4_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 


@router.on_button_callback(state(TrainingStates.konstructor['module_7_lesson_4_questions']), lambda data: data.payload == "start_test")
async def kb_module_7_lesson_4_test_handler(callback: Callback, cursor: FSMCursor):
    """ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ Начало тестирования МОДУЛЬ № 7 УРОК № 4 """
    try:
        logger.info("[kb_module_7_lesson_4_test_handler] Стартовал")
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_4_handler] Идет обработка нажмите позднее")
        #     return
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}) 
        questions = get_testing_data_module_7_test_4_kb()
        logger.info(f"Вопросы для тестирования получены:\nПервый вопрос: {questions[0]}")
        
        data = cursor.get_data()
        logger.info(f'[kb_module_7_lesson_4_test_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
        if data and isinstance(data, dict):
            data.update(questions=questions, current_question=0, answers=[])
        else:
            data = dict()
            data.update(questions=questions, current_question=0, answers=[])
        logger.info(f'{callback=}')
        
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(questions=questions, current_question=0, answers=[]))
        else:
            await save_cursor(callback, extra_data=dict(questions=questions, current_question=0, answers=[]))
        
            
        logger.info(f'[kb_module_7_lesson_4_test_handler] после добавления вопросов в state: {data=}')  
        
        # Отправляем первый вопрос
        cursor.change_data(data)
        await send_question(callback, cursor, "section_83")
        if isinstance(callback, Callback):
            await save_cursor(callback.user_id, extra_data=dict(state_name = TrainingStates.konstructor['module_7_lesson_4_testing']))
        else:
            await save_cursor(callback, extra_data=dict(state_name = TrainingStates.konstructor['module_7_lesson_4_testing']))
        cursor.change_state(TrainingStates.konstructor['module_7_lesson_4_testing'])
    
    except Exception as e:
        logger.error(f"[kb_module_7_lesson_4_test_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id)
        

@router.on_button_callback(state(TrainingStates.konstructor['module_7_lesson_4_testing']), lambda data: data.payload.split('::')[1] == "not_first")
async def continue_after_kb_module_7_handler(callback: Callback, cursor: FSMCursor):
    """Завершение Модуля №7 - КБ. Переход к вопросам или финальному тесту"""
    try:
        logger.info(f"[continue_after_kb_module_7_handler] Стартовал")
        await callback.message.delete()
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        if not current_course:
            current_course = get_current_course(cursor)
        # Проверяем загрузку базы знаний
        rag = RAGService()
        stats = rag.get_stats()
        
        cursor_data = cursor.get_data()
                
        if not stats['is_loaded']:
            await callback.send(
                "❌ База знаний не загружена. Обратитесь к администратору.",
                keyboard=main_menu_keyboard(current_course)
            )
            cursor.clear()
            return
        
        text = kb_get_text_to_final_test_module_7()
                
        await callback.send(text, keyboard=final_start_test_kb())
        cursor.change_state(TrainingStates.konstructor['module_7_questions'])
        await save_cursor(callback.user_id, extra_data = {'payload': 'to_final_test', 'state_name': TrainingStates.konstructor['module_7_questions'], 'current_course': current_course})
    
    except Exception as e:
        logger.error(f"[continue_after_kb_module_7_handler] Произошла ошибка {e}")
        

async def kb_module_7_final_test_handler(callback: Callback, cursor: FSMCursor):
    '''Заглушка для прохождения финального теста по модулю № 7'''
    pass

async def kb_course_final_test_handler(callback: Callback, cursor: FSMCursor):
    '''Заглушка для прохождения финального теста по курсу ОБУЧЕНИЕ ДЛЯ КОНСТРУКТОРОВ'''
    pass
                    
# ================== СПЕЦИФИЧЕСКИЕ ХЭНДЛЕРЫ ДЛЯ ВЕТКИ ЮРИДИЧЕСКИЙ ОТДЕЛ =================


@router.on_button_callback(state(TrainingStates.lawyer['block_1']), lambda data: data.payload.split('::')[1] == "not_first")
async def lawyer_training_step_3_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ЮРИСТ - Блок №1: Перечень компаний и юридических лиц"""
    try:
        logger.info("[lawyer_training_step_3_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2) 
        if continue_flag:
            intro_text = table_of_content_lawyer()
            await callback.send(intro_text)
            await asyncio.sleep(2) # 10
        
        
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_3_handler] Идет обработка нажмите позднее")
        #     return      
        await callback.message.delete()
        intro_text = get_block1_intro_text_lawyer()
        await callback.send(intro_text, disable_link_preview=True)
        
        await asyncio.sleep(2) # 15
        
        # сообщение о тестировании с кнопкой
        test_text = get_text_to_test_block_1_lawyer()
        await callback.send(test_text, keyboard=start_test_kb(True))
        
        cursor.change_state(TrainingStates.lawyer['block1_questions'])
        await asyncio.sleep(2) # 2
        await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.lawyer['block1_questions'], 'current_course': 'Обучение для юриста'})
    
    except Exception as e:
        logger.error(f"[training_step_3_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 
        

@router.on_button_callback(state(TrainingStates.lawyer['block2_section_2']), lambda data: data.payload.split('::')[1] == "not_first")
async def lawyer_part2_section2_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ЮРИСТ - Блок №2 Раздел №2: Отдел продаж"""
    try:
        logger.info("[lawyer_part2_section2_handler] Стартовал")
        await save_cursor(callback.user_id, extra_data = {'lawyer_block_2_part_2_flag': True})
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        
        if continue_flag:
            intro_text = get_block2_intro_text_lawyer()
            await callback.send(intro_text)
            await asyncio.sleep(2) # 10
        
        
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_3_handler] Идет обработка нажмите позднее")
        #     return      
        await callback.message.delete()
        intro_text = get_block2_section_2_intro_text_lawyer()
        await callback.send(intro_text, disable_link_preview=True)
        
        await asyncio.sleep(2) # 10
        
        # сообщение о тестировании с кнопкой
        test_text = get_text_to_test_block_1_lawyer()
        await callback.send(test_text, keyboard=start_test_kb(True))
        
        cursor.change_state(TrainingStates.lawyer['block2_questions'])
        await save_cursor(callback.user_id, extra_data={'state_name': TrainingStates.lawyer['block2_questions']})
    
    except Exception as e:
        logger.error(f"[lawyer_part2_section2_handler] Произошла ошибка {e}")
    finally:
        await remove_repeat_flag(callback.user_id) 
 


@router.on_button_callback(state(TrainingStates.lawyer['block1_questions']), lambda data: data.payload == "to_final_test")
async def lawyer_start_testing_block1_handler(callback: Callback, cursor: FSMCursor):
    """Ветка ЮРИСТ - Начало тестирования по Блоку № 1"""
    try:
        logger.info("[lawyer_start_testing_block1_handler] Стартовал")
        # ЧАСТЬ 1: Закрытые вопросы (10 вопросов с вариантами A/B/C/D)
        closed_questions = get_final_test_block_1_lawyer('close')
        logger.info(f"[INFO][lawyer_start_testing_block1_handler] {closed_questions=}")
        
        # ЧАСТЬ 2: Открытые вопросы (5 вопросов с эталонными ответами)
        open_questions = get_final_test_block_1_lawyer('open')
        logger.info(f"[INFO][lawyer_start_testing_block1_handler] {open_questions=}")
        
        data = cursor.get_data()
        logger.info(f'[lawyer_start_testing_block1_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
    
        if data and isinstance(data, dict):
                data.update(
                    closed_questions=closed_questions,
                    open_questions=open_questions,
                    current_question=0,
                    closed_answers=[],  # Ответы на закрытые вопросы
                    open_answers=[],    # Ответы на открытые вопросы
                    test_stage="closed",  # Начинаем с закрытых вопросов
                    migration_state = "step_12_testing",
                    current_course='Обучение для юриста'
                    )
                await save_cursor(callback.user_id, extra_data = dict(
                    closed_questions=closed_questions,
                    open_questions=open_questions,
                    current_question=0,
                    closed_answers=[],  # Ответы на закрытые вопросы
                    open_answers=[],    # Ответы на открытые вопросы
                    test_stage="closed",  # Начинаем с закрытых вопросов
                    migration_state = "step_12_testing",
                    current_course='Обучение для юриста'
                ))
        else:
            data = dict()
            data.update(
                closed_questions=closed_questions,
                open_questions=open_questions,
                current_question=0,
                closed_answers=[],  # Ответы на закрытые вопросы
                open_answers=[],    # Ответы на открытые вопросы
                test_stage="closed",  # Начинаем с закрытых вопросов
                migration_state = "step_12_testing",
                current_course='Обучение для юриста'
                )
            await save_cursor(callback.user_id, extra_data = dict(
                    closed_questions=closed_questions,
                    open_questions=open_questions,
                    current_question=0,
                    closed_answers=[],  # Ответы на закрытые вопросы
                    open_answers=[],    # Ответы на открытые вопросы
                    test_stage="closed",  # Начинаем с закрытых вопросов
                    migration_state = "step_12_testing",
                    current_course='Обучение для юриста'
                ))
            
        logger.info(f'[lawyer_start_testing_block1_handler] после добавления вопросов в state: {data=}')  
        cursor.change_data(data)
        # Отправляем первый закрытый вопрос
        logger.info(f'[lawyer_start_testing_block3_handler] Отправляем первый закрытый вопрос')
        current_course = cursor.get_data().get('current_course')
        if not current_course:
            current_course = await get_value_from_redis(callback.user_id, 'current_course')
        else:
            current_course = get_current_course(cursor)
        logger.info(f'{current_course=}')
        await send_question_step_12(callback, cursor, "final_test", "Обучение для юриста")

        cursor.change_state(TrainingStates.step_12_testing)
        

    except Exception as e:
        logger.error(f"[ERROR][start_testing_block1_handler] Произошла ошибка {e}") 
        

@router.on_button_callback(state(TrainingStates.lawyer['block2_questions']), lambda data: data.payload == "to_final_test")
async def lawyer_start_testing_block2_sect2_handler(callback: Callback, cursor: FSMCursor):
    """Ветка ЮРИСТ - Начало тестирования по Блоку № 2 Раздел № 2"""
    try:
        logger.info("[lawyer_start_testing_block2_sect2_handler] Стартовал")
        # ЧАСТЬ 1: Закрытые вопросы (10 вопросов с вариантами A/B/C/D)
        closed_questions = get_final_test_block_2_lawyer('close')
        logger.info(f"[INFO][lawyer_start_testing_block2_sect2_handler] {closed_questions=}")
        
        # ЧАСТЬ 2: Открытые вопросы (5 вопросов с эталонными ответами)
        open_questions = get_final_test_block_2_lawyer('open')
        logger.info(f"[INFO][lawyer_start_testing_block2_sect2_handler] {open_questions=}")
        
        data = cursor.get_data()
        logger.info(f'[lawyer_start_testing_block2_sect2_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
    
        if data and isinstance(data, dict):
                data.update(
                    closed_questions=closed_questions,
                    open_questions=open_questions,
                    current_question=0,
                    closed_answers=[],  # Ответы на закрытые вопросы
                    open_answers=[],    # Ответы на открытые вопросы
                    test_stage="closed",  # Начинаем с закрытых вопросов
                    migration_state = "step_12_testing",
                    current_course='Обучение для юриста'
                    )
                await save_cursor(callback.user_id, extra_data = dict(
                    closed_questions=closed_questions,
                    open_questions=open_questions,
                    current_question=0,
                    closed_answers=[],  # Ответы на закрытые вопросы
                    open_answers=[],    # Ответы на открытые вопросы
                    test_stage="closed",  # Начинаем с закрытых вопросов
                    migration_state = "step_12_testing",
                    current_course='Обучение для юриста'
                ))
        else:
            data = dict()
            data.update(
                closed_questions=closed_questions,
                open_questions=open_questions,
                current_question=0,
                closed_answers=[],  # Ответы на закрытые вопросы
                open_answers=[],    # Ответы на открытые вопросы
                test_stage="closed",  # Начинаем с закрытых вопросов
                migration_state = "step_12_testing",
                current_course='Обучение для юриста'
                )
            await save_cursor(callback.user_id, extra_data = dict(
                    closed_questions=closed_questions,
                    open_questions=open_questions,
                    current_question=0,
                    closed_answers=[],  # Ответы на закрытые вопросы
                    open_answers=[],    # Ответы на открытые вопросы
                    test_stage="closed",  # Начинаем с закрытых вопросов
                    migration_state = "step_12_testing",
                    current_course='Обучение для юриста'
                ))
            
        logger.info(f'[lawyer_start_testing_block2_sect2_handler] после добавления вопросов в state: {data=}')  
        cursor.change_data(data)
        # Отправляем первый закрытый вопрос
        logger.info(f'[lawyer_start_testing_block3_handler] Отправляем первый закрытый вопрос')
        current_course = cursor.get_data().get('current_course')
        if not current_course:
            current_course = await get_value_from_redis(callback.user_id, 'current_course')
        else:
            current_course = get_current_course(cursor)
        logger.info(f'{current_course=}')
        await send_question_step_12(callback, cursor, "final_test", "Обучение для юриста")

        cursor.change_state(TrainingStates.step_12_testing)
        

    except Exception as e:
        logger.error(f"[ERROR][lawyer_start_testing_block2_sect2_handler] Произошла ошибка {e}")
     

@router.on_button_callback(state(TrainingStates.lawyer['block3_questions']), lambda data: data.payload == "to_final_test")
async def lawyer_start_testing_block3_handler(callback: Callback, cursor: FSMCursor):
    """Ветка ЮРИСТ - Начало тестирования по Блоку № 3"""
    try:
        logger.info("[lawyer_start_testing_block3_handler] Стартовал")
        # ЧАСТЬ 1: Закрытые вопросы (10 вопросов с вариантами A/B/C/D)
        closed_questions = get_final_test_block_3_lawyer('close')
        logger.info(f"[INFO][lawyer_start_testing_block3_handler] {closed_questions=}")
        
        # ЧАСТЬ 2: Открытые вопросы (5 вопросов с эталонными ответами)
        open_questions = get_final_test_block_3_lawyer('open')
        logger.info(f"[INFO][lawyer_start_testing_block3_handler] {open_questions=}")
        
        data = cursor.get_data()
        logger.info(f'[lawyer_start_testing_block3_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
    
        if data and isinstance(data, dict):
                data.update(
                    closed_questions=closed_questions,
                    open_questions=open_questions,
                    current_question=0,
                    closed_answers=[],  # Ответы на закрытые вопросы
                    open_answers=[],    # Ответы на открытые вопросы
                    test_stage="closed",  # Начинаем с закрытых вопросов
                    migration_state = "step_12_testing",
                    current_course='Обучение для юриста'
                    )
                await save_cursor(callback.user_id, extra_data = dict(
                    closed_questions=closed_questions,
                    open_questions=open_questions,
                    current_question=0,
                    closed_answers=[],  # Ответы на закрытые вопросы
                    open_answers=[],    # Ответы на открытые вопросы
                    test_stage="closed",  # Начинаем с закрытых вопросов
                    migration_state = "step_12_testing",
                    current_course='Обучение для юриста'
                ))
        else:
            data = dict()
            data.update(
                closed_questions=closed_questions,
                open_questions=open_questions,
                current_question=0,
                closed_answers=[],  # Ответы на закрытые вопросы
                open_answers=[],    # Ответы на открытые вопросы
                test_stage="closed",  # Начинаем с закрытых вопросов
                migration_state = "step_12_testing",
                current_course='Обучение для юриста'
                )
            await save_cursor(callback.user_id, extra_data = dict(
                    closed_questions=closed_questions,
                    open_questions=open_questions,
                    current_question=0,
                    closed_answers=[],  # Ответы на закрытые вопросы
                    open_answers=[],    # Ответы на открытые вопросы
                    test_stage="closed",  # Начинаем с закрытых вопросов
                    migration_state = "step_12_testing",
                    current_course='Обучение для юриста'
                ))
            
        logger.info(f'[lawyer_start_testing_block3_handler] после добавления вопросов в state: {data=}')  
        cursor.change_data(data)
        # Отправляем первый закрытый вопрос
        logger.info(f'[lawyer_start_testing_block3_handler] Отправляем первый закрытый вопрос')
        current_course = cursor.get_data().get('current_course')
        if not current_course:
            current_course = await get_value_from_redis(callback.user_id, 'current_course')
        else:
            current_course = get_current_course(cursor)
        logger.info(f'{current_course=}')
        await send_question_step_12(callback, cursor, "final_test", "Обучение для юриста")

        cursor.change_state(TrainingStates.step_12_testing)
        

    except Exception as e:
        logger.error(f"[ERROR][lawyer_start_testing_block3_handler] Произошла ошибка {e}")  
    

@router.on_button_callback(state(TrainingStates.lawyer['block4_questions']), lambda data: data.payload == "to_final_test")
async def lawyer_start_testing_block4_handler(callback: Callback, cursor: FSMCursor):
    """Ветка ЮРИСТ - Начало тестирования по Блоку № 4"""
    try:
        logger.info("[lawyer_start_testing_block4_handler] Стартовал")
        # ЧАСТЬ 1: Закрытые вопросы (10 вопросов с вариантами A/B/C/D)
        closed_questions = get_final_test_block_4_lawyer('close')
        logger.info(f"[INFO][lawyer_start_testing_block4_handler] {closed_questions=}")
        
        # ЧАСТЬ 2: Открытые вопросы (5 вопросов с эталонными ответами)
        open_questions = get_final_test_block_4_lawyer('open')
        logger.info(f"[INFO][lawyer_start_testing_block4_handler] {open_questions=}")
        
        data = cursor.get_data()
        logger.info(f'[lawyer_start_testing_block4_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
    
        if data and isinstance(data, dict):
                data.update(
                    closed_questions=closed_questions,
                    open_questions=open_questions,
                    current_question=0,
                    closed_answers=[],  # Ответы на закрытые вопросы
                    open_answers=[],    # Ответы на открытые вопросы
                    test_stage="closed",  # Начинаем с закрытых вопросов
                    migration_state = "step_12_testing",
                    
                    )
                await save_cursor(callback.user_id, extra_data = dict(
                    closed_questions=closed_questions,
                    open_questions=open_questions,
                    current_question=0,
                    closed_answers=[],  # Ответы на закрытые вопросы
                    open_answers=[],    # Ответы на открытые вопросы
                    test_stage="closed",  # Начинаем с закрытых вопросов
                    migration_state = "step_12_testing",
                    current_course='Обучение для юриста'
                ))
        else:
            data = dict()
            data.update(
                closed_questions=closed_questions,
                open_questions=open_questions,
                current_question=0,
                closed_answers=[],  # Ответы на закрытые вопросы
                open_answers=[],    # Ответы на открытые вопросы
                test_stage="closed",  # Начинаем с закрытых вопросов
                migration_state = "step_12_testing",
                current_course='Обучение для юриста'
                )
            await save_cursor(callback.user_id, extra_data = dict(
                    closed_questions=closed_questions,
                    open_questions=open_questions,
                    current_question=0,
                    closed_answers=[],  # Ответы на закрытые вопросы
                    open_answers=[],    # Ответы на открытые вопросы
                    test_stage="closed",  # Начинаем с закрытых вопросов
                    migration_state = "step_12_testing",
                    current_course='Обучение для юриста'
                ))
            
        logger.info(f'[lawyer_start_testing_block4_handler] после добавления вопросов в state: {data=}')  
        cursor.change_data(data)
        # Отправляем первый закрытый вопрос
        logger.info(f'[lawyer_start_testing_block3_handler] Отправляем первый закрытый вопрос')
        current_course = cursor.get_data().get('current_course')
        if not current_course:
            current_course = await get_value_from_redis(callback.user_id, 'current_course')
        else:
            current_course = get_current_course(cursor)
        logger.info(f'{current_course=}')
        await send_question_step_12(callback, cursor, "final_test", "Обучение для юриста")

        cursor.change_state(TrainingStates.step_12_testing)
        

    except Exception as e:
        logger.error(f"[ERROR][lawyer_start_testing_block4_handler] Произошла ошибка {e}") 
        

@router.on_button_callback(state(TrainingStates.lawyer['block5_questions']), lambda data: data.payload == "to_final_test")
async def lawyer_start_testing_block5_handler(callback: Callback, cursor: FSMCursor):
    """Ветка ЮРИСТ - Начало тестирования по Блоку № 5"""
    try:
        logger.info("[lawyer_start_testing_block5_handler] Стартовал")
        # ЧАСТЬ 1: Закрытые вопросы (10 вопросов с вариантами A/B/C/D)
        closed_questions = get_final_test_block_5_lawyer('close')
        logger.info(f"[INFO][lawyer_start_testing_block5_handler] {closed_questions=}")
        
        # ЧАСТЬ 2: Открытые вопросы (5 вопросов с эталонными ответами)
        open_questions = get_final_test_block_5_lawyer('open')
        logger.info(f"[INFO][lawyer_start_testing_block5_handler] {open_questions=}")
        
        data = cursor.get_data()
        logger.info(f'[lawyer_start_testing_block5_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
    
        if data and isinstance(data, dict):
                data.update(
                    closed_questions=closed_questions,
                    open_questions=open_questions,
                    current_question=0,
                    closed_answers=[],  # Ответы на закрытые вопросы
                    open_answers=[],    # Ответы на открытые вопросы
                    test_stage="closed",  # Начинаем с закрытых вопросов
                    migration_state = "step_12_testing",
                    current_course='Обучение для юриста'
                    )
                await save_cursor(callback.user_id, extra_data = dict(
                    closed_questions=closed_questions,
                    open_questions=open_questions,
                    current_question=0,
                    closed_answers=[],  # Ответы на закрытые вопросы
                    open_answers=[],    # Ответы на открытые вопросы
                    test_stage="closed",  # Начинаем с закрытых вопросов
                    migration_state = "step_12_testing",
                    current_course='Обучение для юриста'
                ))
        else:
            data = dict()
            data.update(
                closed_questions=closed_questions,
                open_questions=open_questions,
                current_question=0,
                closed_answers=[],  # Ответы на закрытые вопросы
                open_answers=[],    # Ответы на открытые вопросы
                test_stage="closed",  # Начинаем с закрытых вопросов
                migration_state = "step_12_testing",
                current_course='Обучение для юриста'
                )
            await save_cursor(callback.user_id, extra_data = dict(
                    closed_questions=closed_questions,
                    open_questions=open_questions,
                    current_question=0,
                    closed_answers=[],  # Ответы на закрытые вопросы
                    open_answers=[],    # Ответы на открытые вопросы
                    test_stage="closed",  # Начинаем с закрытых вопросов
                    migration_state = "step_12_testing",
                    current_course='Обучение для юриста'
                ))
            
        logger.info(f'[lawyer_start_testing_block5_handler] после добавления вопросов в state: {data=}')  
        cursor.change_data(data)
        # Отправляем первый закрытый вопрос
        logger.info(f'[lawyer_start_testing_block3_handler] Отправляем первый закрытый вопрос')
        current_course = cursor.get_data().get('current_course')
        if not current_course:
            current_course = await get_value_from_redis(callback.user_id, 'current_course')
        else:
            current_course = get_current_course(cursor)
        logger.info(f'{current_course=}')
        await send_question_step_12(callback, cursor, "final_test", "Обучение для юриста")

        cursor.change_state(TrainingStates.step_12_testing)
        

    except Exception as e:
        logger.error(f"[ERROR][lawyer_start_testing_block5_handler] Произошла ошибка {e}")
        

@router.on_button_callback(state(TrainingStates.lawyer['final_test_questions']), lambda data: data.payload == "to_final_test")
async def lawyer_start_final_testing_handler(callback: Callback, cursor: FSMCursor):
    """Ветка ЮРИСТ - Начало финального тестирования по КУРСУ ЮРИСТ"""
    try:
        logger.info("[lawyer_start_final_testing_handler] Стартовал")
        # ЧАСТЬ 1: Закрытые вопросы (10 вопросов с вариантами A/B/C/D)
        closed_questions = get_final_test_all_course_lawyer('close')
        logger.info(f"[INFO][lawyer_start_final_testing_handler] {closed_questions=}")
        
        # ЧАСТЬ 2: Открытые вопросы (5 вопросов с эталонными ответами)
        open_questions = get_final_test_all_course_lawyer('open')
        logger.info(f"[INFO][lawyer_start_final_testing_handler] {open_questions=}")
        
        data = cursor.get_data()
        logger.info(f'[lawyer_start_final_testing_handler] до добавления вопросов в state: {data=}')
        # Сохраняем вопросы и начинаем с первого
    
        if data and isinstance(data, dict):
                data.update(
                    closed_questions=closed_questions,
                    open_questions=open_questions,
                    current_question=0,
                    closed_answers=[],  # Ответы на закрытые вопросы
                    open_answers=[],    # Ответы на открытые вопросы
                    test_stage="closed",  # Начинаем с закрытых вопросов
                    migration_state = "step_12_testing",
                    lawyer_finish_flag=True,
                    current_course='Обучение для юриста'
                    )
                await save_cursor(callback.user_id, extra_data = dict(
                    closed_questions=closed_questions,
                    open_questions=open_questions,
                    current_question=0,
                    closed_answers=[],  # Ответы на закрытые вопросы
                    open_answers=[],    # Ответы на открытые вопросы
                    test_stage="closed",  # Начинаем с закрытых вопросов
                    migration_state = "step_12_testing",
                    lawyer_finish_flag=True,
                    current_course='Обучение для юриста'
                ))
        else:
            data = dict()
            data.update(
                closed_questions=closed_questions,
                open_questions=open_questions,
                current_question=0,
                closed_answers=[],  # Ответы на закрытые вопросы
                open_answers=[],    # Ответы на открытые вопросы
                test_stage="closed",  # Начинаем с закрытых вопросов
                migration_state = "step_12_testing",
                lawyer_finish_flag=True,
                current_course='Обучение для юриста'
                )
            await save_cursor(callback.user_id, extra_data = dict(
                    closed_questions=closed_questions,
                    open_questions=open_questions,
                    current_question=0,
                    closed_answers=[],  # Ответы на закрытые вопросы
                    open_answers=[],    # Ответы на открытые вопросы
                    test_stage="closed",  # Начинаем с закрытых вопросов
                    migration_state = "step_12_testing",
                    lawyer_finish_flag=True,
                    current_course='Обучение для юриста'
                ))
            
        logger.info(f'[lawyer_start_testing_block4_handler] после добавления вопросов в state: {data=}')  
        cursor.change_data(data)
        # Отправляем первый закрытый вопрос
        logger.info(f'[lawyer_start_testing_block3_handler] Отправляем первый закрытый вопрос')
        current_course = cursor.get_data().get('current_course')
        if not current_course:
            current_course = await get_value_from_redis(callback.user_id, 'current_course')
        else:
            current_course = get_current_course(cursor)
        logger.info(f'{current_course=}')
        await send_question_step_12(callback, cursor, "final_test", "Обучение для юриста")

        cursor.change_state(TrainingStates.step_12_testing)
        

    except Exception as e:
        logger.error(f"[ERROR][lawyer_start_testing_block4_handler] Произошла ошибка {e}")    
        
        
@router.on_button_callback(lambda data: data.payload == "to_final_test")
async def lawyer_start_testing_without_cursor(callback: Callback, cursor: FSMCursor):
    """Ветка ЮРИСТ - обработка начала тестирования после перезагрузки сервера"""
    try:
        logger.info("[lawyer_start_testing_without_cursor] Стартовал")
        cursor_data = cursor.get_data()
        if not cursor_data:
            state_name = await get_value_from_redis(callback.user_id, 'state_name')
            current_course = await get_value_from_redis(callback.user_id, 'current_course')
            logger.info(f'{state_name=} {current_course=}')
            if current_course == 'Обучение по продажам':
                if state_name == TrainingStates.block1_questions:
                    await start_block1_final_test_handler(callback, cursor)
            if state_name == TrainingStates.lawyer['block1_questions']:
                await lawyer_start_testing_block1_handler(callback, cursor)
            elif state_name == TrainingStates.lawyer['block2_questions']:
                await lawyer_start_testing_block2_sect2_handler(callback, cursor)
            elif state_name == TrainingStates.lawyer['block3_questions']:
                await lawyer_start_testing_block3_handler(callback, cursor)
            elif state_name == TrainingStates.lawyer['block4_questions']:
                await lawyer_start_testing_block4_handler(callback, cursor)
            elif state_name == TrainingStates.lawyer['block5_questions']:
                await lawyer_start_testing_block5_handler(callback, cursor)
            elif state_name == TrainingStates.lawyer['final_test_questions']:
                await lawyer_start_final_testing_handler(callback, cursor)
            elif state_name == TrainingStates.konstructor['module_0_final_testing']:
                await kb_module_0_final_test_handler(callback, cursor)
            elif state_name == TrainingStates.konstructor['module_1_final_testing']:
                await kb_module_1_final_test_handler(callback, cursor)
            elif state_name == TrainingStates.konstructor['module_2_final_testing']:
                await kb_module_2_final_test_handler(callback, cursor)   
            elif state_name == TrainingStates.konstructor['module_3_final_testing']:
                await kb_module_3_final_test_handler(callback, cursor) 
            elif state_name == TrainingStates.konstructor['module_4_final_testing']:
                await kb_module_4_final_test_handler(callback, cursor) 
            elif state_name == TrainingStates.konstructor['module_5_final_testing']:
                await kb_module_5_final_test_handler(callback, cursor)
            elif state_name == TrainingStates.konstructor['module_6_final_testing']:
                await kb_module_6_final_test_handler(callback, cursor) 
            elif state_name == TrainingStates.konstructor['module_7_final_testing']:
                await kb_module_7_final_test_handler(callback, cursor) 
        else:
            return
    except Exception as e:
        logger.error(f"[ERROR][lawyer_start_testing_without_cursor] Произошла ошибка {e}")        
        

@router.on_button_callback(state(TrainingStates.lawyer['block_2_start']), lambda data: data.payload == "next_educ_to_part_2")
async def lawyer_start_block_2_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ЮРИСТ - Обработчик завершения обучения по 1 блоку и перехода к блоку № 2 при нажатии на кнопку ПРОДОЛЖИТЬ ОБУЧЕНИЕ"""
    try:
        logger.info("[lawyer_start_block_2_handler] Стартовал")
        await del_value_from_redis(callback.user_id, "migration_header")
        if continue_flag:
            intro_text = table_of_content_lawyer()
            await callback.send(intro_text)
            await asyncio.sleep(10) # 10
        
        
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_3_handler] Идет обработка нажмите позднее")
        #     return      
        await callback.message.delete()
        intro_text = get_block2_intro_text_lawyer()
        await callback.send(intro_text)
        
        await asyncio.sleep(2) # 15
               
        section_1_text = get_block2_section_1_intro_text_lawyer()
        await callback.send(section_1_text, disable_link_preview=True)
        
        await asyncio.sleep(2) # 15
        
        # сообщение о предложении перейти к 2 разделу блока № 2 с кнопкой
        continue_text = "📚 Для того, чтобы перейти к следующему разделу, нажмите кнопку ниже 👇"
        kb = KeyboardBuilder().add(CallbackButton(text="📚 Продолжить обучение", payload="next_education::not_first"))
        await callback.send(continue_text, keyboard=kb)
        
        cursor.change_state(TrainingStates.lawyer['block2_section_2'])
        await save_cursor(callback.user_id, extra_data={'state_name': TrainingStates.lawyer['block2_section_2'], 'payload': 'next_education::not_first'})
    
    except Exception as e:
        logger.error(f"[lawyer_start_block_2_handler] Произошла ошибка {e}")
        
        
@router.on_button_callback(state(TrainingStates.lawyer['block_3_start']), lambda data: data.payload == "next_educ_to_part_2")
async def lawyer_start_block_3_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ЮРИСТ - Обработчик завершения обучения по 2 блоку и перехода к блоку № 3 при нажатии на кнопку ПРОДОЛЖИТЬ ОБУЧЕНИЕ"""
    try:
        logger.info("[lawyer_start_block_3_handler] Стартовал")
        await del_value_from_redis(callback.user_id, "migration_header")
        if continue_flag:
            intro_text = table_of_content_lawyer()
            await callback.send(intro_text)
            await asyncio.sleep(2) # 10
        
        
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_3_handler] Идет обработка нажмите позднее")
        #     return      
        await callback.message.delete()
        intro_text = get_block3_intro_text_lawyer()
        await callback.send(intro_text, disable_link_preview=True)
        
                
        await asyncio.sleep(2) # 15
        
        # сообщение о тестировании с кнопкой
        test_text = get_text_to_test_block_1_lawyer()
        await callback.send(test_text, keyboard=start_test_kb(True))
        
        cursor.change_state(TrainingStates.lawyer['block3_questions'])
        await save_cursor(callback.user_id, extra_data={'state_name': TrainingStates.lawyer['block3_questions']})
        
    
    except Exception as e:
        logger.error(f"[lawyer_start_block_3_handler] Произошла ошибка {e}")               


        

@router.on_button_callback(state(TrainingStates.lawyer['block_4_start']), lambda data: data.payload == "next_educ_to_part_2")
async def lawyer_start_block_4_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ЮРИСТ - Обработчик завершения обучения по 3 блоку и перехода к блоку № 4 при нажатии на кнопку ПРОДОЛЖИТЬ ОБУЧЕНИЕ"""
    try:
        logger.info("[lawyer_start_block_4_handler] Стартовал")
        await del_value_from_redis(callback.user_id, "migration_header")
        if continue_flag:
            intro_text = table_of_content_lawyer()
            await callback.send(intro_text)
            await asyncio.sleep(2) #10
        
        
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_3_handler] Идет обработка нажмите позднее")
        #     return      
        await callback.message.delete()
        intro_text = get_block4_intro_text_lawyer()
        await callback.send(intro_text, disable_link_preview=True)
               
        await asyncio.sleep(2) # 15
        
        # сообщение о тестировании с кнопкой
        test_text = get_text_to_test_block_1_lawyer()
        await callback.send(test_text, keyboard=start_test_kb(True))
        
        cursor.change_state(TrainingStates.lawyer['block4_questions'])
        await save_cursor(callback.user_id, extra_data={'state_name': TrainingStates.lawyer['block4_questions']})
        return
    
    except Exception as e:
        logger.error(f"[lawyer_start_block_4_handler] Произошла ошибка {e}") 
        

@router.on_button_callback(state(TrainingStates.lawyer['block_5_start']), lambda data: data.payload == "next_educ_to_part_2")
async def lawyer_start_block_5_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ЮРИСТ - Обработчик завершения обучения по 4 блоку и перехода к блоку № 5 при нажатии на кнопку ПРОДОЛЖИТЬ ОБУЧЕНИЕ"""
    try:
        logger.info("[lawyer_start_block_5_handler] Стартовал")
        await del_value_from_redis(callback.user_id, "migration_header")
        if continue_flag:
            intro_text = table_of_content_lawyer()
            await callback.send(intro_text)
            await asyncio.sleep(2) # 10
        
        
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_3_handler] Идет обработка нажмите позднее")
        #     return      
        await callback.message.delete()
        intro_text = get_block5_intro_text_lawyer()
        await callback.send(intro_text, disable_link_preview=True)
               
        await asyncio.sleep(2) # 15
        
        # сообщение о тестировании с кнопкой
        test_text = get_text_to_test_block_1_lawyer()
        await callback.send(test_text, keyboard=start_test_kb(True))
        
        cursor.change_state(TrainingStates.lawyer['block5_questions'])
        await save_cursor(callback.user_id, extra_data={'state_name': TrainingStates.lawyer['block5_questions']})
        
    
    except Exception as e:
        logger.error(f"[lawyer_start_block_5_handler] Произошла ошибка {e}")     
        

@router.on_button_callback(state(TrainingStates.lawyer['final_test_start']), lambda data: data.payload == "next_educ_to_part_2")
async def lawyer_start_final_test_handler(callback: Callback, cursor: FSMCursor, continue_flag:bool=False):
    """Ветка ЮРИСТ - Обработчик завершения обучения по 5 блоку и перехода к финальному тесту при нажатии на кнопку ПРОДОЛЖИТЬ ОБУЧЕНИЕ"""
    try:
        logger.info("[lawyer_start_final_test_handler] Стартовал")
        await del_value_from_redis(callback.user_id, "migration_header")
        if continue_flag:
            intro_text = table_of_content_lawyer()
            await callback.send(intro_text)
            await asyncio.sleep(2) # 10
        
        
        # if await debounce_button_max(callback, cursor):
        #     logger.info(f"[training_step_3_handler] Идет обработка нажмите позднее")
        #     return      
        await callback.message.delete()
        intro_text = get_to_final_intro_text_lawyer()  
        
        await asyncio.sleep(2) # 2
        
        before_test_text = get_text_to_final_test_lawyer()
        await callback.send(intro_text, keyboard=start_test_kb(True))    
                
        cursor.change_state(TrainingStates.lawyer['final_test_questions'])
        await save_cursor(callback.user_id, extra_data={'state_name': TrainingStates.lawyer['final_test_questions']})
        
    
    except Exception as e:
        logger.error(f"[lawyer_start_final_test_handler] Произошла ошибка {e}") 
        


# ========================= РЕГУЛЯРНЫЙ МЕНЕДЖМЕНТ ==========================

@router.on_button_callback(lambda data: data.payload == "regular_managment")
async def regular_managment_start_handl(ctx: Callback, cursor: FSMCursor):
    """Обработчик нажатия пользователем кнопки РЕГУЛЯРНЫЙ МЕНЕДЖМЕНТ
    в разделе ДОПОЛНИТЕЛЬНОЕ ОБРАЗОВАНИЕ"""
    try:
        logger.info('Стартовал')
        await ctx.message.delete()
        state = cursor.get_state() # изменил 12.07.26 !!!!!
        state_name = state.state if all([state, not isinstance(state, str)]) else state
        logger.info(f'{state_name=}')
        logger.info(f"Определяем прогресс пользователя в обучении")
        current_course = "Регулярный менеджмент"
        await save_cursor(ctx.user_id, extra_data={'state_name': state_name, 'current_course': current_course})
        logger.info(f'{current_course=}')
        game = GamificationService(current_course)
        user_id = ctx.user_id

        cursor.change_data({"current_course": current_course})
        cursor_data = cursor.get_data()
        logger.info(f'{cursor_data=}')
        
        lessons_completed = game.get_lessons_completed(user_id, current_course)
        
        logger.info(f'{lessons_completed=}')
        await save_cursor(ctx.user_id, extra_data={'full_block_id': lessons_completed})
        
        if not lessons_completed:
            cursor.change_state(TrainingStates.regular_managment['message_1'])
            text_mess_1 = get_message_1_text()
            await ctx.send(text_mess_1)
            kb = KeyboardBuilder().add(CallbackButton(text="📚 Продолжить обучение", payload="next_education::regular_managment"))     
            await ctx.send(
                    "📚 Вы можете продолжить обучение, нажав кнопку ниже 👇",
                    keyboard=kb
                    )  
            cursor.change_state(TrainingStates.regular_managment['message_2'])
            await save_cursor(ctx.user_id, extra_data={'state_name': TrainingStates.regular_managment['message_2']})
        elif lessons_completed < 10:
            logger.info(f"Обучение по курсу РЕГУЛЯРНЫЙ МЕНЕДЖМЕНТ начато, но еще не завершено, пройдено {lessons_completed} из 10")
            text = (
                f"Вы уже приступили к обучению и в настоящий момент прошли **{lessons_completed} из 10** этапов обучения\n"
                " Вы можете 📚 **Продолжить обучение** \n либо попытаться ⬆️ **Улучшить результат**, нажав на соответствующие  кнопки ниже 👇"
                )
            #await save_cursor(ctx.user_id, extra_data = {'full_block_id': lessons_completed})
            await save_cursor(ctx.user_id, extra_data = {'payload': f"continue_studying::{lessons_completed}"})
            await ctx.send(text, keyboard=continue_studying_kb(lessons_completed))
            return
        elif lessons_completed == 10:
            logger.info(f"Обучение по курсу РЕГУЛЯРНЫЙ МЕНЕДЖМЕНТ ранее было завершено")
            text = (
            f"Вы ранее уже полностью прошли **все 10** этапов обучения\n"
            " Вы можете попытаться ⬆️ **Улучшить результат**, нажав на соответствующую  кнопку ниже 👇\n"
            "либо вернуться в 🏠 **Главное меню**"
            )
            await ctx.send(text, keyboard=finish_studying_kb())
            return 
            
                    
        
        
    except Exception as e:
        logger.error(f'Произошла ошибка: {e}')
        

@router.on_button_callback(state(TrainingStates.regular_managment['message_34']), lambda data: data.payload.split('::')[1] == 'regular_managment')
@router.on_button_callback(state(TrainingStates.regular_managment['message_33']), lambda data: data.payload.split('::')[1] == 'regular_managment')
@router.on_button_callback(state(TrainingStates.regular_managment['message_32']), lambda data: data.payload.split('::')[1] == 'regular_managment')
@router.on_button_callback(state(TrainingStates.regular_managment['message_29']), lambda data: data.payload.split('::')[1] == 'regular_managment')
@router.on_button_callback(state(TrainingStates.regular_managment['message_26']), lambda data: data.payload.split('::')[1] == 'regular_managment')
@router.on_button_callback(state(TrainingStates.regular_managment['message_23']), lambda data: data.payload.split('::')[1] == 'regular_managment')
@router.on_button_callback(state(TrainingStates.regular_managment['message_20']), lambda data: data.payload.split('::')[1] == 'regular_managment')
@router.on_button_callback(state(TrainingStates.regular_managment['message_17']), lambda data: data.payload.split('::')[1] == 'regular_managment')
@router.on_button_callback(state(TrainingStates.regular_managment['message_14']), lambda data: data.payload.split('::')[1] == 'regular_managment')
@router.on_button_callback(state(TrainingStates.regular_managment['message_11']), lambda data: data.payload.split('::')[1] == 'regular_managment')
@router.on_button_callback(state(TrainingStates.regular_managment['message_8']), lambda data: data.payload.split('::')[1] == 'regular_managment')
@router.on_button_callback(state(TrainingStates.regular_managment['message_5']), lambda data: data.payload.split('::')[1] == 'regular_managment')
@router.on_button_callback(state(TrainingStates.regular_managment['message_2']), lambda data: data.payload.split('::')[1] == 'regular_managment')
async def regular_managment_message_2_handler(callback: Callback, cursor: FSMCursor):
    """Логика работы при нажатии на кнопку ПРОДОЛЖИТЬ ОБУЧЕНИЕ из сообщения № 2
    ветки РЕГУЛЯРНЫЙ МЕНЕДЖМЕНТ"""
    try:
        logger.info('Стартовал')
        await save_cursor(callback.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        await callback.message.delete()
        
        cursor_data = cursor.get_data()
        logger.info(f'{cursor_data=}')
        if not cursor_data:
            logger.warning('Возможно сервер был перезагружен, берем значение state_name из redis_storage')
            state_name = await get_value_from_redis(callback.user_id, 'state_name')
        else:
            state = cursor.get_state()
            state_name = state.state if all([state, not isinstance(state, str)]) else state
        logger.info(f'{state_name=}')
        
        if not cursor_data:
            cursor_data = {}
        cursor_data.update(current_term = None, user_answers = {})
                
        # Пауза перед кнопкой продолжения
        await save_cursor(callback.user_id, extra_data = {'payload':'next_education::regular_managment', 'current_term': None, 'user_answers': {}})        
        kb = KeyboardBuilder().add(CallbackButton(text="📚 Продолжить обучение", payload="next_education::regular_managment"))
                    
        
        if state_name == 'message_2':
            text_mess = get_message_2_text()
            await save_cursor(callback.user_id, extra_data = {'current_block':'block_3'})        
            cursor_data.update(current_block='block_3')
        elif state_name == 'message_5':
            text_mess = get_message_5_text()
            await save_cursor(callback.user_id, extra_data = {'current_block':'block_6'})
            cursor_data.update(current_block='block_6')
        elif state_name == 'message_8':
            text_mess = get_message_8_text()
            await save_cursor(callback.user_id, extra_data = {'current_block':'block_9'})
            cursor_data.update(current_block='block_9')
        elif state_name == 'message_11':
            text_mess = get_message_11_text()
            await save_cursor(callback.user_id, extra_data = {'current_block':'block_12'})
            cursor_data.update(current_block='block_12')
        elif state_name == 'message_14':
            text_mess = get_message_14_text()
            await save_cursor(callback.user_id, extra_data = {'current_block':'block_15'})
            cursor_data.update(current_block='block_15')
        elif state_name == 'message_17':
            text_mess = get_message_17_text()
            await save_cursor(callback.user_id, extra_data = {'current_block':'block_18'})
            cursor_data.update(current_block='block_18')
        elif state_name == 'message_20':
            text_mess = get_message_20_text()
            await save_cursor(callback.user_id, extra_data = {'current_block':'block_21'})
            cursor_data.update(current_block='block_21')
        elif state_name == 'message_23':
            text_mess = get_message_23_text()
            await save_cursor(callback.user_id, extra_data = {'current_block':'block_24'})
            cursor_data.update(current_block='block_24')
        elif state_name == 'message_26':
            text_mess = get_message_26_text()
            await save_cursor(callback.user_id, extra_data = {'current_block':'block_27'})
            cursor_data.update(current_block='block_27')
        elif state_name == 'message_29':
            text_mess = get_message_29_text()
            await save_cursor(callback.user_id, extra_data = {'current_block':'block_30'})
            cursor_data.update(current_block='block_30')
        elif state_name == 'message_32':
            text_mess = get_message_32_text()
            await save_cursor(callback.user_id, extra_data = {'current_block':'block_33'})
            cursor_data.update(current_block='block_33')
            cursor.change_data(cursor_data)
            await callback.send(text_mess)
            await asyncio.sleep(2) # 5
            await callback.send(
                "📚 Вы можете продолжить обучение, нажав кнопку ниже 👇",
                keyboard=kb
            )
            await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.regular_managment['message_33']})
            cursor.change_state(TrainingStates.regular_managment['message_33']) 
            return
        elif state_name == 'message_33':
            text_mess = get_message_33_text()
            await save_cursor(callback.user_id, extra_data = {'current_block':'block_34'})
            cursor_data.update(current_block='block_34')
            cursor.change_data(cursor_data)
            await callback.send(text_mess)
            await asyncio.sleep(2) # 5
            await callback.send(
                "📚 Вы можете продолжить обучение, нажав кнопку ниже 👇",
                keyboard=kb
            )
            await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.regular_managment['message_34']})
            cursor.change_state(TrainingStates.regular_managment['message_34']) 
            return
        elif state_name == 'message_34':
            text_mess = get_message_34_text()
            await callback.send(text_mess, keyboard=education_kb(final_flag=True))
            await clear_cursor(callback.user_id)
            await save_cursor(callback.user_id, extra_data = {'state_name': None, 'current_course': 'Регулярный менеджмент'})
            cursor.clear_state() 
            return
            
        await callback.send(text_mess)
        await asyncio.sleep(5) # 30
        await callback.message.delete()
        to_period_sender_text = get_period_sender_text()
        await callback.send(to_period_sender_text)
        
        cursor.change_data(cursor_data)
        
        cursor.change_state(TrainingStates.regular_managment['waiting_response'])
        await send_next_term(callback, cursor)
        return
    except Exception as e:
        logger.error(f'Произошла ошибка: {e}')
    finally:
        await remove_repeat_flag(callback.user_id)
        

async def send_next_term(ctx: Message|Callback, cursor: FSMCursor):
    """Обеспечивает отправку очередного вопроса-термина в чат
    обучаемым"""
    try:
        logger.info('Стартовал')
        cursor_data = cursor.get_data()
        logger.info(f'{cursor_data=}')
        current_block = cursor_data.get('current_block') if all([cursor_data, 'current_block' in cursor_data]) else await get_value_from_redis(ctx.user_id, 'current_block')
        logger.info(f'{current_block=}')
        current_block_number = int(current_block.split('_')[1])
        current_term = cursor_data.get('current_term') if all([cursor_data, 'current_term' in cursor_data]) else await get_value_from_redis(ctx.user_id, 'current_term')
        current_term_number = cursor_data.get('current_term_number') if all([cursor_data, 'current_term_number' in cursor_data]) else await get_value_from_redis(ctx.user_id, 'current_term_number')
        current_answer = cursor_data.get('current_answer') if all([cursor_data, 'current_answer' in cursor_data]) else await get_value_from_redis(ctx.user_id, 'current_answer')
        logger.info(f'{current_block=} {current_block_number=}\n{current_term=}\n{current_answer=}\n{current_term_number=}')
        get_right_answers_func = block_definition_func(current_block_number)
        logger.info(f'Работаем с функцией {get_right_answers_func.__name__}')
        logger.info('Получаем очередной вопрос-термин, требуемый для отправки')
        if not current_term:
            logger.info(f'Отправка первого термина из блока вопросов № {current_block_number}')
            current_term = get_right_answers_func(current_term, 0)
            logger.info(f'{current_term=}')
            cursor_data.update(current_term = current_term, current_term_number = 1)
            await save_cursor(ctx.user_id, extra_data = {'current_term': current_term, 'current_term_number': 1})
        else:
            logger.info(f'Отправка очередного термина из блока вопросов № {current_block_number}')
            current_term = get_right_answers_func(current_term, current_term_number)
            logger.info(f'{current_term=}')
            cursor_data.update(current_term = current_term, current_term_number = current_term_number + 1)
            await save_cursor(ctx.user_id, extra_data = {'current_term': current_term, 'current_term_number': current_term_number + 1})
        await ctx.send(current_term)
        return
        
    except Exception as e:
        logger.error(f'Произошла ошибка {e}')



@router.on_message(state(TrainingStates.regular_managment['waiting_response']))
async def waiting_response_handler(message: Message, cursor: FSMCursor):
    """Обработчик ответов пользователем на вопросы-термины
    в ветке РЕГУЛЯРНЫЙ МЕНЕДЖМЕНТ"""
    try:
        logger.info('Стартовал')
        await save_cursor(message.user_id, extra_data = {'repeat_flag': True}, ttl_seconds = 2)
        
        cursor_data = cursor.get_data()
        if not cursor_data:
            cursor_data = {}
        logger.info(f'{cursor_data=}')
        current_term_number = cursor_data.get('current_term_number') if all([cursor_data, 'current_term_number' in cursor_data ]) else await get_value_from_redis(message.user_id, 'current_term_number')
        current_block = cursor_data.get('current_block') if all([cursor_data, 'current_block' in cursor_data ]) else await get_value_from_redis(message.user_id, 'current_block')
        current_block_number = int(current_block.split('_')[1])
        current_term = cursor_data.get('current_term') if cursor_data else await get_value_from_redis(message.user_id, 'current_term')
        user_answers = cursor_data.get("user_answers", {}) if cursor_data else await get_value_from_redis(message.user_id, 'user_answers')
        current_answer = message.body.text
        user_answers.update({f'{current_term}' : current_answer })
        logger.info(f'{user_answers=}')
        cursor_data.update(user_answers = user_answers)
        await save_cursor(message.user_id, extra_data = {'user_answers': user_answers})
        get_right_answers_func = block_definition_func(current_block_number)
        logger.info(f'{current_block=} {current_block_number=}\n{current_answer=}\n{current_term_number=}')
        try:
            next_term = get_right_answers_func(current_term, current_term_number)
            cursor_data.update(current_term = next_term)
            cursor.change_data(cursor_data)
            await save_cursor(message.user_id, extra_data = {'current_term': next_term})
            await send_next_term(message, cursor)
        except Exception as e:
            logger.warning(f'По-моему вышли за пределы диапазона ключей словаря: {e}')
            await check_answers_to_terms(message, cursor)
                
        
    except Exception as e:
        logger.error(f'Произошла ошибка {e}')
    finally:
        await remove_repeat_flag(message.user_id)
        

async def check_answers_to_terms(message: Message, cursor: FSMCursor):
    """Отвечает за реализацию проверки валидности ответа пользователем
    на термины из ветки РЕГУЛЯРНЫЙ МЕНЕДЖМЕНТ"""
    try:
        logger.info('Стартовал')
        cursor_data = cursor.get_data()
        logger.info(f'{cursor_data=}')
        if not cursor_data:
            cursor_data = {}
        course_name = cursor_data.get('current_course') if all([cursor_data, 'current_course' in cursor_data]) else await get_value_from_redis(message.user_id, 'current_course')
        user_answers = cursor_data.get('user_answers') if all([cursor_data, 'user_answers' in cursor_data]) else await get_value_from_redis(message.user_id, 'user_answers')
        current_block = cursor_data.get('current_block') if all([cursor_data, 'current_block' in cursor_data]) else await get_value_from_redis(message.user_id, 'current_block')
        current_block_number = int(current_block.split('_')[-1])
        right_answer_func = block_definition_func(current_block_number)
        
        # Показываем сообщение о проверке
        checking_msg = await message.send("⏳ **Проверяю ваши ответы...**\n\nЭто может занять некоторое время.", format="markdown")
        
        # ==========================================
        #  Проверка ответов на термины через AI
        # ==========================================
        giga_service = GigaChatService()
        term_scores = []
        term_mistakes = []
        giga_comments = []
        logger.info(f'[INFO][check_answers_to_terms] Инициализировали список {term_mistakes=}')
        for i, term in enumerate(user_answers.copy()):
            if i >= len(list(user_answers.keys())):
                term_scores.append(0)
                term_mistakes.append({
                    "number": 1 + i,
                    "term": term,
                    "user_answer": "Нет ответа",
                    "feedback": "Вы не ответили на вопрос.",
                    "score": 0
                })
                continue
            
            user_answer = user_answers.get(term)
            ideal_answer = right_answer_func(term)
            logger.info(f'{user_answer=}\n{ideal_answer=}')
            
            # Оцениваем через GigaChat
            logger.info(f"Оцениваем через Claude AI")
            
            evaluation = dict()
            
            try:
                evaluation = await giga_service.evaluate_answer(
                    user_answer=user_answer,
                    ideal_answer=ideal_answer,
                    question=term
                )
            except Exception as e:
                logger.error(f'При проверке правильности ответа на термин произошла ошибка: {e}')
                evaluation.setdefault('score', 1.0)
                evaluation.setdefault('feedback', "При оценке правильности ответа на вопрос произошла ошибка, приносим извинения, если Вы были правы!")
                evaluation.setdefault('passed', False)
            
            logger.info(f'Инициализировали список {evaluation=}')
            
            score = evaluation.get("score", 0)
            feedback = evaluation.get("feedback", "Нет фидбека")
            passed = evaluation.get("passed", False)
            ideal_answer = evaluation.get("ideal_answer", "Не нашли правильного ответа")
            
            term_scores.append(score)
            
            if not passed:  # Если оценка < 7.0
                term_mistakes.append({
                    "number": 1 + i,
                    "term": term,
                    "user_answer": user_answer[:200] + "..." if len(user_answer) > 200 else user_answer,
                    "feedback": feedback,
                    "score": score,
                    "ideal_answer": ideal_answer
                })
            
            if 6.0 < score < 10.0:
                giga_comments.append({
                    "number": 1 + i,
                    "term": term,
                    "user_answer": user_answer[:200] + "..." if len(user_answer) > 200 else user_answer,
                    "feedback": feedback,
                    "score": score,
                    "ideal_answer": ideal_answer
                })
            
        await checking_msg.delete()
        
        # ==========================================
        # РАСЧЁТ ДЛЯ ОТОБРАЖЕНИЯ РЕЗУЛЬТАТОВ
        # ==========================================
        logger.info(f"РАСЧЁТ ДЛЯ ОТОБРАЖЕНИЯ РЕЗУЛЬТАТОВ")
        logger.info(f'{term_scores=}')
        term_correct = sum(1 for score in term_scores if score >= 6.0)
        total_terms = len(list(user_answers.keys()))
        
        # Процент для отображения
        accuracy_percent = (term_correct / total_terms) * 100 if total_terms > 0 else 0
        
        logger.info(f'{term_correct=} {total_terms=} {accuracy_percent=}')
        
        # Максимум баллов за открытые: 1 вопросов - 10 баллов
        term_max_score = len(list(user_answers.keys())) * 10
        logger.info(f'{term_max_score=}')
        term_total_score = sum(term_scores)
        term_correct_equivalent = (term_total_score / term_max_score) * len(list(user_answers.keys())) if term_max_score > 0 else 0
        
        logger.info(f'{term_max_score=} {term_total_score=} {term_correct_equivalent=}')
        
        game = GamificationService(course_name)
        user_data = load_user_data()
        user_id = str(message.user_id)
        
                
        first_name = user_data.get(user_id).get("first_name")
        last_name = user_data.get(user_id).get("second_name")
        logger.info(f'{first_name=} {last_name=}')
               
        await game.update_lesson_progress(
            user_id=message.user_id,
            course_name=course_name, #  "Обучение по продажам",
            #correct_count=int(round(term_correct_equivalent)),  # Округляем
            correct_count=int(term_correct),  
            total_count=len(list(user_answers.keys())),           
            lesson_id=current_block, # Номер текущего блока вопросов,
            user_data={
                "username": f'{first_name} {last_name}',
                "first_name": first_name,
                "last_name": last_name
            }
        )
        
        logger.info(f"Значение state_name курсора: {cursor.get_state()} ")
        full_completed_lessons, current_persent = game.get_full_completed_lessons(course_name = course_name, user_id = user_id)
        logger.info(f'{full_completed_lessons=}')
        
        if full_completed_lessons == 10:
            data = game._load_data()
            course_progress = data[user_id]['courses'][course_name]
            correct_answers = course_progress.get('correct_answers')
            total_answers = course_progress.get('total_answers')
            game.record_course_completion_attempt(int(user_id), correct_answers=correct_answers, total_answers=total_answers, course_name="Регулярный менеджмент")
            
        
        # ==========================================
        # ИТОГОВЫЙ ОТЧЁТ
        # ==========================================
        logger.info(f"ИТОГОВЫЙ ОТЧЁТ")
        
        logger.info(f"Получаем обновлённый прогресс пользователя")
              
        progress = game.get_user_progress(message.user_id, course_name)
        
        if isinstance(progress, tuple):
            correct_answers = progress[1].get('correct_answers')
            total_answers = progress[1].get('total_answers')
        else:
            max_progress = get_max_accuracy_item(progress)
            logger.info(f'{max_progress=}')
            correct_answers = max_progress.get('correct_answers')
            total_answers = max_progress.get('total_answers')
        
        
        migration_header = ''
        if current_block_number == 3:
            migration_header = '№1'
        elif current_block_number == 6:
            migration_header = '№2'    
        elif current_block_number == 9:
            migration_header = '№3'
        elif current_block_number == 12:
            migration_header = '№4'
        elif current_block_number == 15:
            migration_header = '№5'
        elif current_block_number == 18:
            migration_header = '№6'
        elif current_block_number == 21:
            migration_header = '№7'
        elif current_block_number == 24:
            migration_header = '№8'
        elif current_block_number == 27:
            migration_header = '№9'
        elif current_block_number == 30:
            migration_header = '№10'
        
        await save_cursor(message.user_id, extra_data = {'migration_header': migration_header})
        
        if current_block != "block_32":
            data_by_lesson = game.get_result_by_lesson(message.user_id, "Регулярный менеджмент", current_block)
            logger.info(f'{data_by_lesson=}')
            correct_answers = data_by_lesson.get('correct_count')
            total_answers = data_by_lesson.get('total_count')
            
        
        
        result_text = f"📊 **Результаты проверки Ваших знаний по Блоку {migration_header}**\n\n"
        result_text += f"**Правильных ответов: {correct_answers}/{total_answers}**\n\n"
        result_text += f"━━━━━━━━━━━━━━━━━━━━\n\n"
        
        if correct_answers == total_answers:
            if giga_comments:
                logger.info('Были неточности в ответах на открытые вопросы')
                
                result_text += "**Не точные ответы в следующих вопросах:**\n\n"
                for comment in giga_comments:
                    result_text += f"⚠️ **Вопрос {comment['number']}:** {comment['term']}\n\n"  # question !!!
                    result_text += f"📝 **Ваш ответ**:\n{comment['user_answer']}\n\n"
                    result_text += f"🎯 **Правильный ответ**:\n{comment['ideal_answer']}\n\n"
                    result_text += f"📊 **Оценка**: {comment['score']}/10\n\n"
                    result_text += f"💬 **Фидбек**:\n{comment['feedback']}\n\n"
                    result_text += f"━━━━━━━━━━━━━━━━━━━━\n\n"
            
            result_text += f"🎉 **Отлично!**\n\nВы успешно прошли тест! Поздравляем с завершением Блока {migration_header}!"
        
        else:
            result_text += "📝 **Есть ошибки**\n\nОзнакомьтесь с правильными ответами ниже:\n\n"
            
            if giga_comments:
                logger.info('Были неточности в ответах на открытые вопросы')
                
                result_text += "**Не точные ответы в следующих вопросах:**\n\n"
                for comment in giga_comments:
                    result_text += f"⚠️ **Вопрос {comment['number']}:** {comment['term']}\n\n" # question !!!!
                    result_text += f"📝 **Ваш ответ**:\n{comment['user_answer']}\n\n"
                    result_text += f"🎯 **Правильный ответ**:\n{comment['ideal_answer']}\n\n"
                    result_text += f"📊 **Оценка**: {comment['score']}/10\n\n"
                    result_text += f"💬 **Фидбек**:\n{comment['feedback']}\n\n"
                    result_text += f"━━━━━━━━━━━━━━━━━━━━\n\n"
            
            if term_mistakes:
                result_text += "**Ошибки в следующих вопросах:**\n\n"
                for mistake in term_mistakes:
                    result_text += f"❌ **Вопрос {mistake['number']}:** {mistake['term']}\n\n"
                    result_text += f"📝 **Ваш ответ**:\n{mistake['user_answer']}\n\n"
                    result_text += f"🎯 **Правильный ответ**:\n{mistake['ideal_answer']}\n\n"
                    result_text += f"📊 **Оценка**: {mistake['score']}/10\n\n"
                    result_text += f"💬 **Фидбек**:\n{mistake['feedback']}\n\n"
                    result_text += f"━━━━━━━━━━━━━━━━━━━━\n\n"
            
            result_text += "\n**Рекомендуем изучить материалы ещё раз!**"
        
        await send_message_safely(message, result_text, format="markdown")
        
        await asyncio.sleep(3) # 15
        
        # ==========================================
        # ПОКАЗЫВАЕМ РЕЙТИНГ ПО ИТОГАМ ПРОЙДЕННОГО БЛОКА
        # ==========================================
        
               
        logger.info(f"[INFO][show_results_step12] {progress=}")
        
        # Формируем сообщение о рейтинге
        logger.info(f"Формируем сообщение о рейтинге")
        user_data = load_user_data()
        logger.info(f"{user_data=}")
        user_id = str(message.user_id)
        first_name = user_data.get(user_id).get("first_name")
        last_name = user_data.get(user_id).get("second_name")
        completed_lesson = 0
        
        if isinstance(progress, list):
            max_progress = get_max_accuracy_item(progress)
            logger.info(f'{max_progress=}')
            completed_lesson = max_progress['lessons_completed']
            logger.info(f'{completed_lesson=}')
            full_completed_lessons, current_persent = game.get_full_completed_lessons(course_name = course_name, user_id = user_id)
            completed_lesson = int(completed_lesson)
            first_phrase = f"🏆 **Ваш рейтинг по итогам Блока {int(full_completed_lessons)}**\n\n"
            if migration_header == 10:
                    first_phrase = f"🏆 **Ваш рейтинг по итогам курса**\n\n"
                    
            rating_text = (
                f"{first_phrase}"
                f"👤 **Ваше имя:** {first_name} {last_name}\n"
                f"📚 **Курс:** {course_name}\n\n"
                f"✅ **Уроков пройдено:** {full_completed_lessons} / 10\n"
            )
            if full_completed_lessons != 10 and course_name == 'Регулярный менеджмент':
                rating_text += f"📈 **Процент правильных ответов:** {current_persent}%\n"
            else:
                rating_text += f"📈 **Процент правильных ответов:** {max_progress['accuracy_percent']:.1f}%\n"
        else:
                      
            first_phrase = f"🏆 **Ваш рейтинг по итогам Блока {migration_header}**\n\n"
            
            completed_lesson = progress[1]['lessons_completed']
            logger.info(f'{completed_lesson=}')
            full_completed_lessons, current_persent = game.get_full_completed_lessons(course_name = course_name, user_id = user_id)
            completed_lesson = int(completed_lesson)
            
            if migration_header == 10:
                    first_phrase = f"🏆 **Ваш рейтинг по итогам курса**\n\n"
            
            rating_text = (
                f"{first_phrase}"
                f"👤 **Ваше имя:** {first_name} {last_name}\n"
                f"📚 **Курс:** {course_name}\n\n"
                f"✅ **Уроков пройдено:** {full_completed_lessons} / 10\n"
            )
            
            if full_completed_lessons != 10 and course_name == 'Регулярный менеджмент':
                rating_text += f"📈 **Процент правильных ответов:** {current_persent}%\n"
            else:
                rating_text += f"📈 **Процент правильных ответов:** {progress[1]['accuracy_percent']:.1f}%\n"
        
        rating_text += "\n_Продолжайте обучение для повышения результатов!_"
        
        await message.send(rating_text, format="markdown")
        
        # Пауза перед кнопкой продолжения
        await asyncio.sleep(2) # 5
        
        kb = KeyboardBuilder().add(CallbackButton(text="📚 Продолжить обучение", payload="next_education::regular_managment"))
                
        await message.send(
            "📚 Вы можете продолжить обучение, нажав кнопку ниже 👇",
            keyboard=kb
        )
        
        status_user = await get_value_from_redis(message.user_id, 'status_user')
        migration_header = await get_value_from_redis(message.user_id, 'migration_header')
        
        if current_block == 'block_3':
            await clear_cursor(message.user_id)
            await save_cursor(message.user_id, extra_data={'payload':'next_education::regular_managment', 'status_user': status_user, 'current_course': 'Регулярный менеджмент', "state_name": TrainingStates.regular_managment['message_5'], 'migration_header': migration_header, 'current_block': current_block})
            cursor.change_state(TrainingStates.regular_managment['message_5'])
        elif current_block == 'block_6':
            await clear_cursor(message.user_id)
            await save_cursor(message.user_id, extra_data={'payload':'next_education::regular_managment', 'status_user': status_user, 'current_course': 'Регулярный менеджмент', "state_name": TrainingStates.regular_managment['message_8'], 'migration_header': migration_header, 'current_block': current_block})
            cursor.change_state(TrainingStates.regular_managment['message_8'])
        elif current_block == 'block_9':
            await clear_cursor(message.user_id)
            await save_cursor(message.user_id, extra_data={'payload':'next_education::regular_managment', 'status_user': status_user, 'current_course': 'Регулярный менеджмент', "state_name": TrainingStates.regular_managment['message_11'], 'migration_header': migration_header, 'current_block': current_block})
            cursor.change_state(TrainingStates.regular_managment['message_11'])
        elif current_block == 'block_12':
            await clear_cursor(message.user_id)
            await save_cursor(message.user_id, extra_data={'payload':'next_education::regular_managment', 'status_user': status_user, 'current_course': 'Регулярный менеджмент', "state_name": TrainingStates.regular_managment['message_14'], 'migration_header': migration_header, 'current_block': current_block})
            cursor.change_state(TrainingStates.regular_managment['message_14'])
        elif current_block == 'block_15':
            await clear_cursor(message.user_id)
            await save_cursor(message.user_id, extra_data={'payload':'next_education::regular_managment', 'status_user': status_user, 'current_course': 'Регулярный менеджмент', "state_name": TrainingStates.regular_managment['message_17'], 'migration_header': migration_header, 'current_block': current_block})
            cursor.change_state(TrainingStates.regular_managment['message_17'])
        elif current_block == 'block_18':
            await clear_cursor(message.user_id)
            await save_cursor(message.user_id, extra_data={'payload':'next_education::regular_managment','status_user': status_user, 'current_course': 'Регулярный менеджмент', "state_name": TrainingStates.regular_managment['message_20'], 'migration_header': migration_header, 'current_block': current_block})
            cursor.change_state(TrainingStates.regular_managment['message_20'])
        elif current_block == 'block_21':
            await clear_cursor(message.user_id)
            await save_cursor(message.user_id, extra_data={'payload':'next_education::regular_managment', 'status_user': status_user, 'current_course': 'Регулярный менеджмент', "state_name": TrainingStates.regular_managment['message_23'], 'migration_header': migration_header, 'current_block': current_block})
            cursor.change_state(TrainingStates.regular_managment['message_23'])
        elif current_block == 'block_24':
            await clear_cursor(message.user_id)
            await save_cursor(message.user_id, extra_data={'payload':'next_education::regular_managment', 'status_user': status_user, 'current_course': 'Регулярный менеджмент', "state_name": TrainingStates.regular_managment['message_26'], 'migration_header': migration_header, 'current_block': current_block})
            cursor.change_state(TrainingStates.regular_managment['message_26'])
        elif current_block == 'block_27':
            await clear_cursor(message.user_id)
            await save_cursor(message.user_id, extra_data={'payload':'next_education::regular_managment', 'status_user': status_user, 'current_course': 'Регулярный менеджмент', "state_name": TrainingStates.regular_managment['message_29'], 'migration_header': migration_header, 'current_block': current_block})
            cursor.change_state(TrainingStates.regular_managment['message_29'])
        elif current_block == 'block_30':
            await clear_cursor(message.user_id)
            await save_cursor(message.user_id, extra_data={'payload':'next_education::regular_managment', 'status_user': status_user, 'current_course': 'Регулярный менеджмент', "state_name": TrainingStates.regular_managment['message_32'], 'migration_header': migration_header, 'current_block': current_block})
            cursor.change_state(TrainingStates.regular_managment['message_32'])             
                                  
    except Exception as e:
        logger.error(f'Произошла ошибка: {e}')
        
            
@router.on_button_callback()
async def final_process_answer_without_cursor(callback: Callback, cursor: FSMCursor):
    """Обработчик-индикатор перенаправления в условиях отсутствия курсора
    в обработчик ответа пользователя на вопрос тестирования (final_process_answer_handler)"""
    try:
        logger.info("Стартовал")
        repeat_flag = await get_value_from_redis(callback.user_id, 'repeat_flag')
        not_confirm_date_flag = await get_value_from_redis(callback.user_id, 'not_confirm_date_flag')
        confirm_date_flag = await get_value_from_redis(callback.user_id, 'confirm_date_flag')
        step_3_handler_flag = await get_value_from_redis(callback.user_id, 'step_3_handler_flag')
        first_step_flag = await get_value_from_redis(callback.user_id, 'first_step_flag')
        exit_ai_flag = await get_value_from_redis(callback.user_id, 'exit_ai_flag')
        step_4_flag = await get_value_from_redis(callback.user_id, 'step_4_flag')
        tomorrow_flag = await get_value_from_redis(callback.user_id, 'tomorrow_flag')
        lawyer_block_2_part_2_flag = await get_value_from_redis(callback.user_id, 'lawyer_block_2_part_2_flag')
        logger.info(f'{repeat_flag=} {not_confirm_date_flag=} {confirm_date_flag=} {step_3_handler_flag=}')
        call_data = callback.payload
        if call_data == 'yes':
            if not repeat_flag and not confirm_date_flag:
                await del_value_from_redis(callback.user_id, 'confirm_date_flag')
                await confirm_date_handler(callback, cursor)
            return
        elif call_data == 'no':
            if not repeat_flag and not not_confirm_date_flag:
                await del_value_from_redis(callback.user_id, 'not_confirm_date_flag')
                await not_confirm_date_handler(callback, cursor)
            return
            
        logger.info(f'{call_data=}')
        cursor_data = cursor.get_data()
        if not cursor_data:
            cursor_data = {}
        logger.info(f'{cursor_data=}')
        if callback.payload in ['main_menu', 'main_menu_without_ai'] and not repeat_flag:
            if callback.payload == 'main_menu_without_ai' and not exit_ai_flag:
                await del_value_from_redis(callback.user_id, 'exit_ai_flag')
                await go_to_main_menu_handler(callback, cursor)
            return
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        payload = await get_value_from_redis(callback.user_id, 'payload')
        second_payload = await get_value_from_redis(callback.user_id, 'second_payload')
        state_name = await get_value_from_redis(callback.user_id, 'state_name')
        not_repeat_flag = await get_value_from_redis(callback.user_id, 'not_repeat_flag')
        
        logger.info(f'{payload=} {state_name=} {second_payload=} {current_course=} {not_repeat_flag=}')
        if all([not_repeat_flag, state_name != 'start_final_test']):
            logger.info('выходим по return')
            return
        
        if all([cursor_data, state_name == 'block_2_final_testing', 'final_block_2_flag' not in cursor_data]):
            logger.info('выходим по return')
            return
        
        if all([cursor_data, state_name == 'block_3_final_testing', 'final_block_3_flag' not in cursor_data]):
            logger.info('выходим по return')
            return
        
        if all([cursor_data, state_name == 'block_4_final_testing', 'final_block_4_flag' not in cursor_data]):
            logger.info('выходим по return')
            return
        
        if all([cursor_data, state_name == 'block_5_final_testing', 'final_block_5_flag' not in cursor_data]):
            logger.info('выходим по return')
            return
        
        if all([cursor_data, state_name == 'block_6_final_testing', 'final_block_6_flag' not in cursor_data]):
            logger.info('выходим по return')
            return 
        
        if all([cursor_data, state_name == 'block_7_final_testing', 'final_block_7_flag' not in cursor_data]):
            logger.info('выходим по return')
            return                
        
        if all([cursor_data, state_name == 'step_12_testing', 'final_block_1_flag' not in cursor_data]):
            logger.info('выходим по return')
            return

        if second_payload  == 'change_date' and not repeat_flag:
            await del_value_from_redis(callback.user_id, 'second_payload')
            second_payload = await get_value_from_redis(callback.user_id, 'second_payload')
            logger.info(f'После удаления {second_payload=}')
            if not repeat_flag and not tomorrow_flag:
                await change_date_handler(callback, cursor, True)
                await del_value_from_redis(callback.user_id, 'tomorrow_flag')
            return
        elif second_payload == 'no' and not repeat_flag:
            await del_value_from_redis(callback.user_id, 'second_payload')
            await not_confirm_date_handler(callback, cursor)
            return
        
        if payload == 'next_education':
            await next_education_handler(callback, cursor)
            return
        elif payload == 'next_education::not_first':
            if state_name == TrainingStates.step_2_video and not repeat_flag:
                if not step_3_handler_flag:
                    await del_value_from_redis(callback.user_id, 'step_3_handler_flag')
                    await training_step_3_handler(callback, cursor)
                #await show_course_intro_handler(callback, cursor)
                return
            if state_name == TrainingStates.step_3_presentation:# or TrainingStates.course_intro:
                repeat_flag = await get_value_from_redis(callback.user_id, 'repeat_flag')
                logger.info(f'{repeat_flag=}')
                if not repeat_flag and not first_step_flag:
                    await del_value_from_redis(callback.user_id, 'first_step_flag')
                    await training_step_3_handler_first_step(callback, cursor)
                return
            elif state_name in [TrainingStates.lawyer['block_1'], TrainingStates.course_intro] and current_course == 'Обучение для юриста':
                repeat_flag = await get_value_from_redis(callback.user_id, 'repeat_flag')
                logger.info(f'{repeat_flag=}')
                if not repeat_flag:
                    await lawyer_training_step_3_handler(callback, cursor)
                return
            elif state_name == TrainingStates.lawyer['block2_section_2'] and not repeat_flag:
                if not lawyer_block_2_part_2_flag:
                    await lawyer_part2_section2_handler(callback, cursor)
                    await del_value_from_redis(callback.user_id, 'lawyer_block_2_part_2_flag')
                return
        elif payload == 'lawyer_educ':
            await del_value_from_redis(callback.user_id, 'payload')
            await lawyer_training_handler(callback, cursor)                                      
            return
        elif payload == 'tomorrow' and not repeat_flag:
            if not tomorrow_flag:
                await del_value_from_redis(callback.user_id, 'payload')
                await start_tomorrow_handler(callback, cursor)
                await del_value_from_redis(callback.user_id, 'tomorrow_flag')
            return
        elif payload == 'yes' and not repeat_flag:
            await del_value_from_redis(callback.user_id, 'payload')
            await confirm_date_handler(callback, cursor)
            return
            
        # для курса Обучение по продажам
        if current_course == 'Обучение по продажам':
            repeat_flag = await get_value_from_redis(callback.user_id, 'repeat_flag')
            logger.info(f'{repeat_flag=}')
            call_button = await get_value_from_redis(callback.user_id, 'call_button')
            
            
            if not repeat_flag and payload == 'mark_video_section_viewed':
                if state_name == TrainingStates.block_5_video_2_viewer:
                    await block_5_video_2_handler(callback, cursor)
                elif state_name == TrainingStates.block_5_video_3_viewer:
                    await block_5_video_3_handler(callback, cursor)
                elif state_name == TrainingStates.block_5_video_4_viewer:
                    await block_5_video_4_handler(callback, cursor)
                elif state_name == TrainingStates.block_5_video_5_viewer:
                    await block_5_video_5_handler(callback, cursor)
                elif state_name == TrainingStates.block_5_video_6_viewer:
                    await block_5_video_6_handler(callback, cursor)
                elif state_name == TrainingStates.block_5_video_7_viewer:
                    await block_5_video_7_handler(callback, cursor)
                elif state_name == TrainingStates.block_5_video_8_viewer:
                    await block_5_video_8_handler(callback, cursor)
                elif state_name == TrainingStates.block_5_video_9_viewer:
                    await block_5_video_9_handler(callback, cursor)
                elif state_name == TrainingStates.block_5_video_10_viewer:
                    await block_5_video_10_handler(callback, cursor)
                elif state_name == TrainingStates.block_5_video_11_viewer:
                    await block_5_video_11_handler(callback, cursor)
                elif state_name == TrainingStates.block_5_video_12_viewer:
                    await block_5_video_12_handler(callback, cursor)
                elif state_name == TrainingStates.block_5_video_13_viewer:
                    await block_5_video_13_handler(callback, cursor)
                elif state_name == TrainingStates.block_5_video_14_viewer:
                    await block_5_video_14_handler(callback, cursor)
                elif state_name == TrainingStates.block_5_video_15_viewer:
                    await block_5_video_15_handler(callback, cursor)
                elif state_name == TrainingStates.block5_final_test:
                    cursor.change_state(TrainingStates.block5_final_test)
                    await save_cursor(callback.user_id, extra_data = {'state_name': TrainingStates.block5_final_test, 'current_course': current_course, 'payload': 'ai_after_block5'})
                    await continue_after_block5_handler(callback, cursor)                
                return
                
            
                          
            if all([call_button == 'next_education::not_first',state_name != TrainingStates.step_12_testing,
                    payload not in ['start_test', 'ai_after_block2', 'ai_after_block3', 'ai_after_block4', 'ai_after_block5', 'ai_after_block6' 'to_final_test', 'start_final_test']]):
                if not repeat_flag:
                    if state_name == TrainingStates.step_6_next:
                        await training_step_6_handler(callback, cursor)
                    elif state_name == TrainingStates.step_8_next:
                        await training_step_8_handler(callback, cursor)
                    elif state_name == TrainingStates.step_9_next:
                        await training_step_9_handler(callback, cursor)
                    elif state_name == TrainingStates.step_10_next:
                        await training_step_10_handler(callback, cursor)
                    elif state_name == TrainingStates.step_11_next:
                        await training_step_11_handler(callback, cursor)
                    elif state_name == TrainingStates.block_2_section_2_next:
                        await block_2_test_2_ready_for_test_handl(callback, cursor)
                    elif state_name == TrainingStates.block_2_section_3_next:
                        await block_2_test_3_ready_for_test_handl(callback, cursor)
                    elif state_name == TrainingStates.block_2_section_4_next:
                        await block_2_go_to_final_test_handl(callback, cursor)
                    elif state_name == TrainingStates.block_3_section_1_next:
                        await block_3_test_2_ready_for_test_handl(callback, cursor)
                    elif state_name == TrainingStates.block_3_section_2_next:
                        await block_3_test_3_ready_for_test_handl(callback, cursor)
                    elif state_name == TrainingStates.block_3_section_3_next:
                        await block_3_test_4_ready_for_test_handl(callback, cursor)
                    elif state_name == TrainingStates.block_3_section_4_next:
                        await block_3_test_5_ready_for_test_handl(callback, cursor)
                    elif state_name == TrainingStates.block_3_section_5_next:
                        await block_3_test_6_ready_for_test_handl(callback, cursor)
                    elif state_name == TrainingStates.block4_section1_ready:
                        await go_to_block4_section1_handler(callback, cursor)
                    elif state_name == TrainingStates.block_4_section_1_next:
                        await block_4_test_2_ready_for_test_handl(callback, cursor)
                    elif state_name == TrainingStates.block_4_section_2_next:
                        await block_4_test_3_ready_for_test_handl(callback, cursor)
                    elif state_name == TrainingStates.block_4_section_3_next:
                        await block_4_test_4_ready_for_test_handl(callback, cursor)

                    
                return
            
            if payload == 'ai_after_block2':
                if not repeat_flag:
                    await continue_after_block2_handler(callback, cursor)
                return
            elif payload == 'ai_after_block3':
                if not repeat_flag:
                    await continue_after_block3_handler(callback, cursor)
                return
            elif payload == 'ai_after_block4':
                if not repeat_flag:
                    await continue_after_block4_handler(callback, cursor)
                return
            elif payload == 'ai_after_block5':
                if not repeat_flag:
                    await continue_after_block5_handler(callback, cursor)
                return
            elif payload == 'ai_after_block6':
                if not repeat_flag:
                    await continue_after_block6_handler(callback, cursor)
                return
            
            elif payload == 'start_test':
                cursor.change_state(state_name)
                if not repeat_flag:
                    if state_name == 'step_4_ready_for_test':
                        await training_step_4_handler(callback, cursor)
                        return
                    elif state_name == 'step_6_ready_for_test':
                        await training_test_2_handler(callback, cursor)
                        return
                    elif state_name == 'step_8_ready_for_test':
                        await training_test_3_handler(callback, cursor)
                        return
                    elif state_name == 'step_9_ready_for_test':
                        await training_test_4_handler(callback, cursor)
                        return
                    elif state_name == 'step_10_ready_for_test':
                        await training_test_5_handler(callback, cursor)
                        return
                    elif state_name == 'step_11_ready_for_test':
                        await training_test_6_handler(callback, cursor)
                        return
                    elif state_name == TrainingStates.block2_section1_ready:
                        await training_block_2_test_1_handler(callback, cursor)
                        return
                    elif state_name == TrainingStates.block_2_test_2_ready_for_test:
                        await training_block_2_test_2_handler(callback, cursor)
                        return
                    elif state_name == TrainingStates.block_2_test_3_ready_for_test:
                        await training_block_2_test_3_handler(callback, cursor)
                        return
                    elif state_name == TrainingStates.block_3_test_1_ready_for_test:
                        await training_block_3_test_1_handler(callback, cursor)
                        return
                    elif state_name == TrainingStates.block_3_test_2_ready_for_test:
                        await training_block_3_test_2_handler(callback, cursor)
                        return
                    elif state_name == TrainingStates.block_3_test_3_ready_for_test:
                        await training_block_3_test_3_handler(callback, cursor)
                        return
                    elif state_name == TrainingStates.block_3_test_4_ready_for_test:
                        await training_block_3_test_4_handler(callback, cursor)
                        return
                    elif state_name == TrainingStates.block_3_test_5_ready_for_test:
                        await training_block_3_test_5_handler(callback, cursor)
                        return
                    elif state_name == TrainingStates.block_3_test_6_ready_for_test:
                        await training_block_3_test_6_handler(callback, cursor)
                        return
                    elif state_name in [TrainingStates.block_4_test_1_ready_for_test, TrainingStates.block4_section1_ready]:
                        await training_block_4_test_1_handler(callback, cursor)
                        return
                    elif state_name == TrainingStates.block_4_test_2_ready_for_test:
                        await training_block_4_test_2_handler(callback, cursor)
                        return
                    elif state_name == TrainingStates.block_4_test_3_ready_for_test:
                        await training_block_4_test_3_handler(callback, cursor)
                        return
                    elif state_name == TrainingStates.block_4_test_4_ready_for_test:
                        await training_block_4_test_4_handler(callback, cursor)
                        return
                    elif state_name == TrainingStates.konstructor['module_0_lesson_1_questions']:
                        await kb_module_0_lesson_1_test_handler(callback, cursor)
                        return
            
                if state_name in ['step_5_testing', 'step_7_testing', 'step_8_testing', 'step_9_testing',
                        'step_10_testing', 'step_11_testing', 'block_2_test_1_testing', 'block_2_test_2_testing',
                        'block_2_final_testing', 'block_3_final_testing', 'block_4_final_testing',
                        'block_5_final_testing', 'block_6_final_testing', 'block_7_final_testing',
                        'block_2_test_3_testing', 'block_3_test_6_testing', 'block_3_test_5_testing',
                        'block_3_test_4_testing', 'block_3_test_3_testing', 'block_3_test_2_testing',
                        'block_3_test_1_testing', 'block_4_test_1_testing', 'block_4_test_2_testing',
                        'block_4_test_3_testing', 'block_4_test_4_testing']:
                    repeat_flag = await get_value_from_redis(callback.user_id, 'repeat_flag')
                    logger.info(f'{repeat_flag=}')
                    if not repeat_flag:
                        cursor.change_state(state_name)
                        await process_answer_handler(callback, cursor)
                    return
            elif payload == 'to_final_test':
                final_block_1_flag = await get_value_from_redis(callback.user_id, 'final_block_1_flag')
                final_block_2_flag = await get_value_from_redis(callback.user_id, 'final_block_2_flag')
                final_block_3_flag = await get_value_from_redis(callback.user_id, 'final_block_3_flag')
                final_block_4_flag = await get_value_from_redis(callback.user_id, 'final_block_4_flag')
                final_block_5_flag = await get_value_from_redis(callback.user_id, 'final_block_5_flag')
                final_block_6_flag = await get_value_from_redis(callback.user_id, 'final_block_6_flag')
                full_block_id = await get_value_from_redis(callback.user_id, 'full_block_id')
                final_block_7_flag = await get_value_from_redis(callback.user_id, 'final_block_7_flag')
                logger.info(f'{payload=} {final_block_1_flag=} {final_block_2_flag=} {final_block_3_flag=} {final_block_4_flag=} {final_block_5_flag=} {final_block_6_flag=} {final_block_7_flag=}')
                if not repeat_flag:
                    if not final_block_2_flag and state_name == TrainingStates.block2_questions:
                        await start_block2_final_test_handler(callback, cursor)
                    elif not final_block_3_flag and state_name == TrainingStates.block3_questions:
                        await start_block3_final_test_handler(callback, cursor)
                    elif not final_block_4_flag and state_name == TrainingStates.block4_questions:
                        await start_block4_final_test_handler(callback, cursor)
                    elif not final_block_5_flag and state_name == TrainingStates.block5_questions:
                        await start_block5_final_test_handler(callback, cursor)
                    elif not final_block_6_flag and state_name == TrainingStates.block6_questions:
                        await start_block6_final_test_handler(callback, cursor)
                    elif not final_block_7_flag and state_name == TrainingStates.block7_questions:
                        await start_testing_block7_handler(callback, cursor)
                    elif not final_block_1_flag:
                        await start_block1_final_test_handler(callback, cursor)
                    # elif full_block_id == 7:
                    #     await start_testing_block7_handler(callback, cursor)
                    
                return
                
            elif payload == 'start_final_test': #and state_name == TrainingStates.step_12_testing or TrainingStates.block2_questions:
                final_block_2_flag = await get_value_from_redis(callback.user_id, 'final_block_2_flag')
                final_block_3_flag = await get_value_from_redis(callback.user_id, 'final_block_3_flag')
                final_block_4_flag = await get_value_from_redis(callback.user_id, 'final_block_4_flag')
                final_block_5_flag = await get_value_from_redis(callback.user_id, 'final_block_5_flag')
                final_block_6_flag = await get_value_from_redis(callback.user_id, 'final_block_6_flag')
                final_block_7_flag = await get_value_from_redis(callback.user_id, 'final_block_7_flag')
                #send_question_flag = await get_value_from_redis(callback.user_id, 'send_question_flag')
                logger.info(
                    f'{payload=}'
                    f'{final_block_2_flag=}'
                    f'{final_block_3_flag=}'
                    f'{final_block_4_flag=}'
                    f'{final_block_5_flag=}'
                    f'{final_block_6_flag=}'
                    f'{final_block_7_flag=}'
                    )
                if not repeat_flag:
                    if not final_block_2_flag and state_name == TrainingStates.block_2_final_testing:
                        await start_testing_block2_handler(callback, cursor)
                    elif not final_block_3_flag and state_name == TrainingStates.block_3_final_testing:
                        await start_testing_block3_handler(callback, cursor)
                    elif not final_block_4_flag and state_name == TrainingStates.block_4_final_testing:
                        await start_testing_block4_handler(callback, cursor)
                    elif not final_block_5_flag and state_name == TrainingStates.block_5_final_testing:
                        await start_testing_block5_handler(callback, cursor)
                    elif not final_block_6_flag and state_name == TrainingStates.block_6_final_testing:
                        await start_testing_block6_handler(callback, cursor)
                    elif not final_block_7_flag and state_name == TrainingStates.block_7_final_testing:
                        await start_testing_block7_handler(callback, cursor)
                    else:
                        #if send_question_flag:
                        #    await del_value_from_redis(callback.user_id, 'send_question_flag')
                        #    return
                        await final_process_answer_handler(callback, cursor)
                return
            elif payload == 'next_educ_to_part_2':
                if not repeat_flag:
                    if state_name == TrainingStates.block2_start:
                        await start_block_2_handler(callback, cursor)
                    elif state_name == TrainingStates.block_2_final_testing:
                        await start_block_3_handler(callback, cursor)
                    elif state_name == TrainingStates.block_3_final_testing:
                        await start_block_4_handler(callback, cursor)
                    elif state_name == TrainingStates.block_4_final_testing:
                        await start_block_5_handler(callback, cursor)
                    elif state_name == TrainingStates.block_5_final_testing:
                        await start_block_6_section_1_handler(callback, cursor)
                    elif state_name == TrainingStates.block_6_final_testing:
                        await start_block_7_handler(callback, cursor)
                return
            
                
   
        # для курса Обучение по продукту
        if current_course == 'Обучение по продукту':
            repeat_flag = await get_value_from_redis(callback.user_id, 'repeat_flag')
            logger.info(f'{repeat_flag=}')
            call_button = await get_value_from_redis(callback.user_id, 'call_button')
            logger.info(f'Работаем с {current_course=} {state_name=}')
            if call_button == 'next_education::not_first':
                if not repeat_flag:
                    if state_name == TrainingStates.step_6_next:
                        await training_step_6_handler(callback, cursor)
                    elif state_name == TrainingStates.step_8_next:
                        await training_step_8_handler(callback, cursor)
                    elif state_name == TrainingStates.step_9_next:
                        await training_step_9_handler(callback, cursor)
                    elif state_name == TrainingStates.step_10_next:
                        await training_step_10_handler(callback, cursor)
                    elif state_name == TrainingStates.step_11_next:
                        await training_step_11_handler(callback, cursor)
                return
            if payload == 'start_test':
                cursor.change_state(state_name)
                if not repeat_flag:
                    if state_name == 'step_4_ready_for_test':
                        await training_step_4_handler(callback, cursor)
                        return
                    elif state_name == 'step_6_ready_for_test':
                        await training_test_2_handler(callback, cursor)
                        return
                    elif state_name == 'step_8_ready_for_test':
                        await training_test_3_handler(callback, cursor)
                        return
                    elif state_name == 'step_9_ready_for_test' and not step_4_flag:
                        await training_test_4_handler(callback, cursor)
                        await del_value_from_redis(callback.user_id, 'step_4_flag')
                        return
                    elif state_name == 'step_10_ready_for_test':
                        await training_test_5_handler(callback, cursor)
                        return
                    elif state_name == 'step_11_ready_for_test':
                        await training_test_6_handler(callback, cursor)
                        return
                    
                if state_name in ['step_5_testing', 'step_7_testing', 'step_8_testing', 'step_9_testing',
                        'step_10_testing', 'step_11_testing', 'block_2_test_1_testing', 'block_2_test_2_testing',
                        'block_2_final_testing', 'block_3_final_testing', 'block_4_final_testing',
                        'block_5_final_testing', 'block_6_final_testing', 'block_7_final_testing',
                        'block_2_test_3_testing', 'block_3_test_6_testing', 'block_3_test_5_testing',
                        'block_3_test_4_testing', 'block_3_test_3_testing', 'block_3_test_2_testing',
                        'block_3_test_1_testing', 'block_4_test_1_testing', 'block_4_test_2_testing',
                        'block_4_test_3_testing', 'block_4_test_4_testing']:
                    repeat_flag = await get_value_from_redis(callback.user_id, 'repeat_flag')
                    logger.info(f'{repeat_flag=}')
                    if not repeat_flag:
                        cursor.change_state(state_name)
                        await process_answer_handler(callback, cursor)
                    return
            elif payload == 'to_final_test':
                if not repeat_flag:
                    if not final_block_1_flag:
                        await start_block1_final_test_handler(callback, cursor)
                return
            elif payload == 'start_final_test' and state_name == TrainingStates.step_12_testing:
                final_block_1_flag = await get_value_from_redis(callback.user_id, 'final_block_1_flag')
                if not repeat_flag:
                    if not final_block_1_flag:
                        await start_testing_block1_handler(callback, cursor)
                    else:
                        await final_process_answer_handler(callback, cursor)
                return
                
        
        # для курса Регулярный менеджмент
        repeat_flag = await get_value_from_redis(callback.user_id, 'repeat_flag')
        logger.info(f'{repeat_flag=}')
        if current_course == 'Регулярный менеджмент':
            if payload == 'next_education::regular_managment' and not repeat_flag:
                logger.info('Нажата кнопка ПРОДОЛЖИТЬ ОБУЧЕНИЕ после окончания текущего блока и прохождения теста ВОПРОС-ОТВЕТ')
                cursor.change_state(state_name)
                await regular_managment_message_2_handler(callback, cursor)
                return 
            
            if state_name in [TrainingStates.regular_managment['message_2'], TrainingStates.regular_managment['message_5'],
                              TrainingStates.regular_managment['message_8'], TrainingStates.regular_managment['message_11'],
                              TrainingStates.regular_managment['message_14'], TrainingStates.regular_managment['message_17'],
                              TrainingStates.regular_managment['message_20'], TrainingStates.regular_managment['message_23'],
                              TrainingStates.regular_managment['message_26'], TrainingStates.regular_managment['message_29'],
                              TrainingStates.regular_managment['message_32'], TrainingStates.regular_managment['message_33'],
                              TrainingStates.regular_managment['message_34']]:
                if not repeat_flag:
                    await regular_managment_message_2_handler(callback, cursor)
                return
                         
        # для курса Обучение для конструкторов
        if current_course == 'Обучение для конструкторов' and not repeat_flag:                  
            logger.info(f'Работаем с {current_course=} {state_name=}')
            if state_name == TrainingStates.konstructor['module_0']:
                await kb_module_0_handler(callback, cursor)
            elif state_name == TrainingStates.konstructor['module_0_lesson_1']:
                await kb_module_0_lesson_1_handler(callback, cursor)
            elif state_name == TrainingStates.konstructor['module_0_lesson_2']:
                await kb_module_0_lesson_2_handler(callback, cursor)
            elif state_name == TrainingStates.konstructor['module_0_lesson_3']:
                await kb_module_0_lesson_3_handler(callback, cursor)
            elif state_name == TrainingStates.konstructor['module_0_lesson_4']:
                await kb_module_0_lesson_4_handler(callback, cursor)
            elif state_name == TrainingStates.konstructor['module_0_lesson_5']:
                await kb_module_0_lesson_5_handler(callback, cursor)
            elif state_name == TrainingStates.konstructor['module_1_lesson_1']:
                await kb_module_1_lesson_1_handler(callback, cursor)
            elif state_name == TrainingStates.konstructor['module_1_lesson_2']:
                await kb_module_1_lesson_2_handler(callback, cursor)
            elif state_name == TrainingStates.konstructor['module_1_lesson_3']:
                await kb_module_1_lesson_3_handler(callback, cursor)
            elif state_name == TrainingStates.konstructor['module_1_lesson_4']:
                await kb_module_1_lesson_4_handler(callback, cursor)
            elif state_name == TrainingStates.konstructor['module_1_lesson_5']:
                await kb_module_1_lesson_5_handler(callback, cursor)
            elif state_name == TrainingStates.konstructor['module_1_lesson_6']:
                await kb_module_1_lesson_6_handler(callback, cursor)
            elif state_name == TrainingStates.konstructor['module_2_lesson_1']:
                await kb_module_2_lesson_1_handler(callback, cursor)
            elif state_name == TrainingStates.konstructor['module_2_lesson_2']:
                await kb_module_2_lesson_2_handler(callback, cursor)
            elif state_name == TrainingStates.konstructor['module_2_lesson_3']:
                await kb_module_2_lesson_3_handler(callback, cursor)
            elif state_name == TrainingStates.konstructor['module_2_lesson_4']:
                await kb_module_2_lesson_4_handler(callback, cursor)
            elif state_name == TrainingStates.konstructor['module_2_lesson_5']:
                await kb_module_2_lesson_5_handler(callback, cursor)
            elif state_name == TrainingStates.konstructor['module_3_lesson_1']:
                await kb_module_3_lesson_1_handler(callback, cursor)
            elif state_name == TrainingStates.konstructor['module_3_lesson_2']:
                await kb_module_3_lesson_2_handler(callback, cursor)
            elif state_name == TrainingStates.konstructor['module_3_lesson_3']:
                await kb_module_3_lesson_3_handler(callback, cursor)
            elif state_name == TrainingStates.konstructor['module_3_lesson_4']:
                await kb_module_3_lesson_4_handler(callback, cursor)
            elif state_name == TrainingStates.konstructor['module_3_lesson_5']:
                await kb_module_3_lesson_5_handler(callback, cursor)
            elif state_name == TrainingStates.konstructor['module_4_lesson_1']:
                await kb_module_4_lesson_1_handler(callback, cursor)
            elif state_name == TrainingStates.konstructor['module_4_lesson_2']:
                await kb_module_4_lesson_2_handler(callback, cursor)
            elif state_name == TrainingStates.konstructor['module_4_lesson_3']:
                await kb_module_4_lesson_3_handler(callback, cursor)
            elif state_name == TrainingStates.konstructor['module_4_lesson_4']:
                await kb_module_4_lesson_4_handler(callback, cursor)
            elif state_name == TrainingStates.konstructor['module_5_lesson_1']:
                await kb_module_5_lesson_1_handler(callback, cursor)
            elif state_name == TrainingStates.konstructor['module_5_lesson_2']:
                await kb_module_5_lesson_2_handler(callback, cursor)
            elif state_name == TrainingStates.konstructor['module_5_lesson_3']:
                await kb_module_5_lesson_3_handler(callback, cursor)
            elif state_name == TrainingStates.konstructor['module_5_lesson_4']:
                await kb_module_5_lesson_4_handler(callback, cursor)
            elif state_name == TrainingStates.konstructor['module_6_lesson_1']:
                await kb_module_6_lesson_1_handler(callback, cursor)
            elif state_name == TrainingStates.konstructor['module_6_lesson_2']:
                await kb_module_6_lesson_2_handler(callback, cursor)
            elif state_name == TrainingStates.konstructor['module_6_lesson_3']:
                await kb_module_6_lesson_3_handler(callback, cursor)
            elif state_name == TrainingStates.konstructor['module_6_lesson_4']:
                await kb_module_6_lesson_4_handler(callback, cursor)
            elif state_name == TrainingStates.konstructor['module_7_lesson_1']:
                await kb_module_7_lesson_1_handler(callback, cursor)
            elif state_name == TrainingStates.konstructor['module_7_lesson_2']:
                await kb_module_7_lesson_2_handler(callback, cursor)
            elif state_name == TrainingStates.konstructor['module_7_lesson_3']:
                await kb_module_7_lesson_3_handler(callback, cursor)
            elif state_name == TrainingStates.konstructor['module_7_lesson_4']:
                await kb_module_7_lesson_4_handler(callback, cursor)
            return    
        
        logger.info("Проверяем на принадлежность к блоку ПРОДОЛЖЕНИЯ ОБУЧЕНИЯ")
        migration_header = await get_value_from_redis(callback.user_id, 'migration_header')
        current_course = await get_value_from_redis(callback.user_id, 'current_course')
        logger.info(f'{current_course=}\n{migration_header=}')
        if all([any([isinstance(migration_header, str), isinstance(migration_header, int)]), migration_header, current_course == 'Обучение для юриста']):
            logger.info(f'{migration_header=} определяем state_name чтобы правильно определить требуемф обработчик для продолжения обучения')
            state_name = await get_value_from_redis(callback.user_id, 'state_name')
            logger.info(f'{state_name=}')
            if state_name == TrainingStates.lawyer['block_2_start']:
                await lawyer_start_block_2_handler(callback, cursor)
            elif state_name == TrainingStates.lawyer['block_3_start']:
                await lawyer_start_block_3_handler(callback, cursor)
            elif state_name == TrainingStates.lawyer['block_4_start']:
                await lawyer_start_block_4_handler(callback, cursor)
            elif state_name == TrainingStates.lawyer['block_5_start']:
                await lawyer_start_block_5_handler(callback, cursor)
            elif state_name == TrainingStates.lawyer['final_test_start']:
                await lawyer_start_final_test_handler(callback, cursor)
            return
                   
                
            
        cursor_data = cursor.get_data()
        redis_data = await load_cursor(callback.user_id)
        pprint(redis_data)
        migration_state = await get_value_from_redis(callback.user_id, 'migration_state')
        logger.info(f'{migration_state=}')
        if not cursor_data:
            cursor.change_state(migration_state)
            await final_process_answer_handler(callback, cursor)
        
    except Exception as e:
        logger.error(f'Произошла ошибка: {e}')
    
        
@router.on_message()
async def answer_block_question_without_cursor(message: Message, cursor: FSMCursor):
    """Обработчик-индикатор отсутствия курсора при попытке задать вопрос и перенаправления
    на нужный обработчик"""
    try:
        logger.info("Стартовал")
        cursor_data = cursor.get_data()
        current_course = await get_value_from_redis(message.user_id, 'current_course')
        state_name = await get_value_from_redis(message.user_id, 'state_name')
        repeat_flag = await get_value_from_redis(message.user_id, 'repeat_flag')
        if not current_course:
            current_course = get_current_course(cursor)
        if not cursor_data:
            logger.warning('Возможно сервер был перезагружен, попробуем определить state_name и ответить на заданный вопрос')
            # state_name = await get_value_from_redis(message.user_id, 'state_name')
            second_payload = await get_value_from_redis(message.user_id, 'second_payload')
            logger.info(f'Из redis_storage: {current_course=} {state_name=} {second_payload=}')
            if state_name == TrainingStates.asking_ai: #and current_course == 'Обучение по продукту':
                await process_ai_question_handler(message, cursor)
                return
            elif state_name == 'block7_questions':
                await answer_block7_question_handler(message, cursor)
                return
            elif state_name == UserInfo.waiting_for_name_surname and not repeat_flag:
                await process_name_surname(message, cursor)
                return
        else:
            if current_course == 'Регулярный менеджмент':
                logger.info('Внутри регулярного менеджмента')
                if state_name in [TrainingStates.regular_managment['message_2'], TrainingStates.regular_managment['message_5'],
                                    TrainingStates.regular_managment['message_8'], TrainingStates.regular_managment['message_11'],
                                    TrainingStates.regular_managment['message_14'], TrainingStates.regular_managment['message_17'],
                                    TrainingStates.regular_managment['message_20'], TrainingStates.regular_managment['message_23'],
                                    TrainingStates.regular_managment['message_26'], TrainingStates.regular_managment['message_29'],
                                    TrainingStates.regular_managment['message_32'], TrainingStates.regular_managment['message_33'],
                                    TrainingStates.regular_managment['message_34']]:

                    logger.info(f'{repeat_flag=}')
                    if not repeat_flag:
                        await waiting_response_handler(message, cursor)
                    #cursor.change_state(state)
                    return       
            return
            # state = cursor.get_state() # изменил 12.07.26 !!!!!
            # state_name = state.state if all([state, not isinstance(state, str)]) else state
            # logger.info(f'Из курсора: {state_name=}')
        
        if all([state_name == OnboardingStates.waiting_for_start_date, not second_payload]):
            logger.info('Переход к обработчику указания даты выхода на работу')
            await input_date_handler(message, cursor)
        
        
        repeat_flag = await get_value_from_redis(message.user_id, 'repeat_flag')
        logger.info(f'{repeat_flag=}')
        # Обучение по продажам
        if not repeat_flag:
            if state_name == TrainingStates.block1_questions:
                await start_block1_final_test_handler(message, cursor)
            elif state_name == TrainingStates.block2_questions:
                await start_block2_final_test_handler(message, cursor)
            elif state_name == TrainingStates.block3_questions:
                await start_block3_final_test_handler(message, cursor)
            elif state_name == TrainingStates.block4_questions:
                await start_block4_final_test_handler(message, cursor)
            elif state_name == TrainingStates.block5_questions:
                await start_block5_final_test_handler(message, cursor)
            elif state_name == TrainingStates.block6_questions:
                await start_block6_final_test_handler(message, cursor)
            
        
        # обучение для юриста
        if state_name == TrainingStates.lawyer['block3_questions']:
            if not repeat_flag:
                logger.info('Отвечаем на вопросы по Блоку 3 через RAG + Claude')
                await answer_block3_question_handler(message, cursor, state_name)
        elif state_name == TrainingStates.lawyer['block2_questions']:
            if not repeat_flag:
                logger.info('Отвечаем на вопросы по Блоку 2 через RAG + Claude')
                await answer_block2_question_handler(message, cursor, state_name)
        elif state_name == TrainingStates.lawyer['block1_questions']:
            if not repeat_flag:
                logger.info('Отвечаем на вопросы по Блоку 1 через RAG + Claude')
                await answer_block1_question_handler(message, cursor, state_name)
        elif state_name == TrainingStates.lawyer['block4_questions']:
            if not repeat_flag:
                logger.info('Отвечаем на вопросы по Блоку 4 через RAG + Claude')
                await answer_block4_question_handler(message, cursor, state_name)
        elif state_name in [TrainingStates.lawyer['block5_questions'], TrainingStates.lawyer['final_test_questions']]:
            if not repeat_flag:
                logger.info('Отвечаем на вопросы по Блоку 5 через RAG + Claude')
                await answer_block5_question_handler(message, cursor, state_name)
        elif state_name == TrainingStates.check_answer_to_open_question:
            cursor.change_state(TrainingStates.check_answer_to_open_question)
            logger.info('Перенаправляем на обработчик проверки валидности введенного пользователем ответа на открытый вопрос')
            await check_valid_answer_of_question(message, cursor)
        elif not state_name:
            await process_ai_question_handler(message, cursor)
            
        # регулярный менеджмент
        
        if current_course == 'Регулярный менеджмент':
            if state_name in [TrainingStates.regular_managment['message_2'], TrainingStates.regular_managment['message_5'],
                                TrainingStates.regular_managment['message_8'], TrainingStates.regular_managment['message_11'],
                                TrainingStates.regular_managment['message_14'], TrainingStates.regular_managment['message_17'],
                                TrainingStates.regular_managment['message_20'], TrainingStates.regular_managment['message_23'],
                                TrainingStates.regular_managment['message_26'], TrainingStates.regular_managment['message_29'],
                                TrainingStates.regular_managment['message_32'], TrainingStates.regular_managment['message_33'],
                                TrainingStates.regular_managment['message_34']]:
                repeat_flag = await get_value_from_redis(message.user_id, 'repeat_flag')
                logger.info(f'{repeat_flag=}')
                if not repeat_flag:
                    await waiting_response_handler(message, cursor)
                return        
            
        return
        
    except Exception as e:
        logger.error(f'Произошла ошибка: {e}')        
    
        

        

 
        
