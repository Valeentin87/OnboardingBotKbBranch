import math
import re
import os
import sys
import unicodedata
import json
from typing import List, Dict, Any
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
from dotenv import load_dotenv
import logging

# Настройка логгера (если у тебя его нет в другом месте)
logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

class GigaChatService:
    def __init__(self):
        load_dotenv()
        AUTH_KEY = os.getenv('AUTHORIZATION_KEY')
        TYPE_SCOPE = os.getenv('TYPE_SCOPE')

        credentials = str(AUTH_KEY).strip()
        # Очистка ключа от лишних символов, если нужно
        credentials = ''.join(c for c in credentials if c.isalnum() or c in '-_=+/')
        
        self.credentials = credentials
        self.scope = TYPE_SCOPE
        self.model = 'GigaChat-2-Max'
        logger.info(f'[INFO][GigaChatService] Экземпляр класса успешно создан')

    @staticmethod
    def _split_into_chunks(text: str, chunk_size: int, overlap: int) -> List[str]:
        """
        Разбивает текст на чанки с перекрытием.
        Это тот самый метод, которого не хватало!
        """
        chunks = []
        start = 0
        
        if overlap >= chunk_size:
            overlap = max(0, chunk_size - 100)

        while start < len(text):
            end = start + chunk_size
            
            # Логика перекрытия только для чанков после первого
            if start > 0:
                start = max(start - overlap, 0)
                end = start + chunk_size

            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            else:
                break
            
            start = end
            
        return chunks

    @staticmethod
    async def _get_embeddings(giga: GigaChat, texts: List[str]):
        """Вспомогательный метод для вызова API эмбеддингов."""
        response = await giga.embeddings(texts=texts)
        return [item.embedding for item in response.data]

    @staticmethod
    async def _get_embeddings_safe(giga: GigaChat, texts: List[str]) -> List[List[float]]:
        """
        Безопасное получение эмбеддингов батчами.
        Защита от 413 на этапе получения векторов.
        """
        MAX_BATCH_CHARS = 12000 
        all_embs = []
        current_batch = []
        current_len = 0

        for text in texts:
            text_len = len(text)
            
            if current_len + text_len > MAX_BATCH_CHARS and current_batch:
                try:
                    batch_embs = await GigaChatService._get_embeddings(giga, current_batch)
                    all_embs.extend(batch_embs)
                except Exception as e:
                    logger.error(f"Ошибка в батче эмбеддингов: {e}")
                current_batch = []
                current_len = 0
            
            current_batch.append(text)
            current_len += text_len

        if current_batch:
            try:
                batch_embs = await GigaChatService._get_embeddings(giga, current_batch)
                all_embs.extend(batch_embs)
            except Exception as e:
                logger.error(f"Ошибка финального батча эмбеддингов: {e}")
                
        return all_embs

    @staticmethod
    def _cosine_similarity(a: List[float], b: List[float]) -> float:
        if len(a) != len(b):
            return 0.0

        dot_product = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(y * y for y in b))

        if norm_a == 0 or norm_b == 0:
            return 0.0

        return dot_product / (norm_a * norm_b)

    @staticmethod
    async def _retrieve_relevant_chunks(
        giga: GigaChat,
        question: str,
        chunks: List[str],
        top_k: int = 2,
        expand_neighbors: bool = False
    ) -> str:
        """Находит наиболее релевантные чанки по косинусному сходству."""
        if not chunks:
            return ""

        try:
            q_emb_resp = await giga.embeddings(texts=[question])
            q_emb = q_emb_resp.data[0].embedding
        except Exception as e:
            logger.error(f"Не удалось получить эмбеддинг вопроса: {e}")
            return "\n\n".join(chunks[:3])

        all_embs = await GigaChatService._get_embeddings_safe(giga, chunks)

        # Синхронизация длин на случай ошибок
        if len(all_embs) != len(chunks):
            min_len = min(len(all_embs), len(chunks))
            chunks = chunks[:min_len]
            all_embs = all_embs[:min_len]

        scores = []
        for idx, emb in enumerate(all_embs):
            score = GigaChatService._cosine_similarity(q_emb, emb)
            scores.append((idx, score))

        scores.sort(key=lambda x: x[1], reverse=True)
        top_indices = [idx for idx, _ in scores[:top_k]]

        # Добавляем соседей ТОЛЬКО если expand_neighbors=True
        if expand_neighbors and len(chunks) > 1:
            expanded_indices = set(top_indices)
            for idx in top_indices:
                if idx > 0: expanded_indices.add(idx - 1)
                if idx < len(chunks) - 1: expanded_indices.add(idx + 1)
            top_indices = sorted(expanded_indices)

        # Берем максимум 4 чанка для финального контекста, чтобы не раздуть промпт
        final_indices = top_indices[:4] 
        relevant_chunks = [chunks[i] for i in final_indices]
        
        return "\n\n".join(relevant_chunks)

    @staticmethod
    def _clean_text(text: str) -> str:
        if not text: return text
        text = unicodedata.normalize('NFKD', text)
        text = ''.join(char for char in text if not unicodedata.combining(char))
        for char in ['\xad', '\u00ad', '\u200b', '\u200c', '\u200d', '\ufeff', '\u2060']:
            text = text.replace(char, '')
        text = text.replace('\xa0', ' ').replace('\u202f', ' ').replace('\u2009', ' ')
        replacements = {'\u2013': '-', '\u2014': '-', '\u2018': "'", '\u2019': "'", '\u201c': '"', '\u201d': '"', '\u2026': '...', '\u2022': '*'}
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        safe = []
        for char in text:
            code = ord(char)
            if 32 <= code <= 126 or 0x0400 <= code <= 0x04FF or char in '\n\r\t ':
                safe.append(char)
        text = ''.join(safe)
        text = re.sub(r' +', ' ', text)
        text = re.sub(r'\n\n+', '\n\n', text)
        return text.strip()

    async def answer_with_context(self, question: str, knowledge_base: str) -> str:
        question = self._clean_text(question)
        knowledge_base = self._clean_text(knowledge_base)

        logger.info('Стартовал')

        # --- ОБЩИЙ SYSTEM PROMPT ---
        system_prompt = (
            "Ты AI-ассистент компании по производству противопожарных систем. "
            "Отвечай ТОЛЬКО на основе предоставленной базы знаний. Не выдумывай.\n\n"
            "ПРАВИЛА ФОРМАТИРОВАНИЯ (СТРОГО СОБЛЮДАТЬ):\n"
            "- Заголовки смысловых блоков выделяй **жирным** (двойные звездочки).\n"
            "- Перечисления оформляй маркированным списком с символом •.\n"
            "- Последовательность действий — нумерованным списком (1., 2., 3.).\n"
            "- Прямые цитаты бери дословно в кавычки.\n"
            "- Перед списком делай перевод строки.\n"
            "- Фразу 'Ознакомиться с материалами можно здесь:' всегда выделяй **жирным**.\n"
            "Если информации нет: ответь одной фразой — «Информации по данному вопросу в базе знаний нет»."
        )

        try:
            async with GigaChat(
                credentials=self.credentials,
                scope=self.scope,
                model=self.model,
                verify_ssl_certs=False
            ) as giga:
                
                context_to_send = ""
                mode_used = ""

                # === СТРАТЕГИЯ 1: БАЗА МАЛЕНЬКАЯ ===
                SMALL_KB_LIMIT = 15000 

                if len(knowledge_base) <= SMALL_KB_LIMIT:
                    mode_used = "FULL_SEND"
                    logger.info(f"База небольшая ({len(knowledge_base)} символов). Отправляем целиком.")
                    
                    context_to_send = (
                        "=== БАЗА ЗНАНИЙ КОМПАНИИ ===\n"
                        f"{knowledge_base}\n\n"
                        "=== ВОПРОС СОТРУДНИКА ===\n"
                        f"{question}\n\n"
                        "Проанализируй базу знаний и ответь на вопрос."
                    )

                # === СТРАТЕГИЯ 2: БАЗА БОЛЬШАЯ (RAG) ===
                else:
                    mode_used = "RAG_SAFE"
                    logger.info(f"База большая ({len(knowledge_base)} символов). Применяем RAG.")

                    chunk_size = 1500      
                    overlap = 150           
                    chunks = self._split_into_chunks(knowledge_base, chunk_size, overlap)
                    logger.info(f"Разбито на {len(chunks)} чанков.")

                    if not chunks:
                        return "❌ База знаний пуста."

                    raw_context = await self._retrieve_relevant_chunks(
                        giga=giga,
                        question=question,
                        chunks=chunks,
                        top_k=2,            
                        expand_neighbors=False 
                    )

                    MAX_CONTEXT_CHARS = 12000
                    if len(raw_context) > MAX_CONTEXT_CHARS:
                        logger.warning(f"⚠️ Контекст ({len(raw_context)}) превышает лимит {MAX_CONTEXT_CHARS}. Обрезаем.")
                        context_to_send = raw_context[:MAX_CONTEXT_CHARS]
                    else:
                        context_to_send = raw_context

                    # Упрощенный промпт без лишних заголовков для RAG
                    context_to_send = f"{context_to_send}\n\nВопрос сотрудника: {question}"

                logger.info(f"[METRICS] Режим: {mode_used}, Длина контекста: {len(context_to_send)}, System: {len(system_prompt)}")

                # Проверка размера перед отправкой
                estimated_size_kb = (len(system_prompt) + len(context_to_send)) * 1.4 / 1024
                if estimated_size_kb > 35:
                    logger.error(f"❌ Оценочный размер запроса ({estimated_size_kb:.2f} KB) слишком велик. Принудительная обрезка.")
                    max_user_len = 10000
                    context_to_send = context_to_send[-max_user_len:]

                response = await giga.achat(Chat(
                    model=self.model,
                    messages=[
                        Messages(role=MessagesRole.SYSTEM, content=system_prompt),
                        Messages(role=MessagesRole.USER, content=context_to_send),
                    ],
                    max_tokens=2048,
                    temperature=0.2,
                ))
                answer = response.choices[0].message.content.strip()

            logger.info('[INFO][GigaChatService][answer_with_context] Ответ получен')

            if len(answer) < 10 or "информации по данному вопросу" in answer.lower():
                return "❌ Информация по вашему вопросу не найдена в базе знаний."
            
            return answer

        except Exception as e:
            print(f"❌ Ошибка GigaChatService.answer_with_context: {e}")
            import traceback
            traceback.print_exc()
            return "❌ Произошла ошибка при обработке запроса."

    
    async def evaluate_answer(self, user_answer: str, ideal_answer: str, question: str = "") -> dict:
        """
        Оценивает ответ сотрудника по шкале 1-10 на основе эталонного ответа.
        Возвращает словарь: {'score': float, 'feedback': str, 'passed': bool, 'ideal_answer': str}
        """
        user_answer = self._clean_text(user_answer)
        ideal_answer = self._clean_text(ideal_answer)
        question = self._clean_text(question)

        # Формируем промпт для оценщика
        prompt = (
            "Ты эксперт по оценке ответов новых сотрудников компании по производству "
            "противопожарных систем.\n\n"
            f"Вопрос: {question}\n\n"
            f"Эталонный ответ: {ideal_answer}\n\n"
            f"Ответ сотрудника: {user_answer}\n\n"
            "Оцени ответ по шкале от 1 до 10:\n"
            "• 9-10: Отличный, все ключевые моменты раскрыты\n"
            "• 6-8: Хороший, основные моменты упомянуты\n"
            "• 4-5: Удовлетворительно, есть пробелы\n"
            "• 1-3: Слабый, многое упущено\n\n"
            'Верни СТРОГО в формате JSON без какого‑либо текста вокруг:\n'
            '{"score": число от 1 до 10, "feedback": "структурированный текст с поддержкой и указанием на пробелы"}\n\n'
            "ВАЖНО:\n"
            "- В feedback обязательно должны быть поддерживающие фразы ('ты на правильном пути', 'осталось немного' и т.п.).\n"
            "- Четко укажи, чего не хватило в ответе сотрудника и почему это важно.\n"
            "- Не используй осуждающий тон, но не скрывай фактические ошибки.\n"
            "- Если ответ идеален, все равно дай краткий фидбек с похвалой."
        )

        try:
            async with GigaChat(
                credentials=self.credentials,
                scope=self.scope,
                model=self.model,
                verify_ssl_certs=False,
            ) as giga:
                response = await giga.achat(Chat(
                    model=self.model,
                    messages=[Messages(role=MessagesRole.USER, content=prompt)],
                    max_tokens=1024,
                    temperature=0.3,
                ))

            result_text = response.choices[0].message.content.strip()
            logger.debug(f"[DEBUG][GigaChatService][evaluate_answer] Raw response: {result_text}")

            # Пытаемся извлечь JSON из ответа (модель может добавить вводный текст)
            json_match = re.search(r'\{[^}]+\}', result_text)
            
            if json_match:
                result_json = json.loads(json_match.group())
                score = float(result_json.get('score', 6.0))
                feedback = str(result_json.get('feedback', 'Ответ принят, замечаний нет.'))
            else:
                # Фоллбэк, если JSON не найден: пытаемся вытащить число и берем начало текста как фидбек
                numbers = re.findall(r'\b([1-9]|10)(?:\.\d+)?\b', result_text)
                score = float(numbers[0]) if numbers else 6.0
                feedback = result_text[:200] if result_text else "Не удалось получить детальный фидбек."

            # Нормализация оценки в диапазон 1.0 - 10.0
            score = max(1.0, min(10.0, score))
            passed = score >= 6.0  # Порог прохождения

            logger.info(f"[INFO][GigaChatService][evaluate_answer] Оценка: {score}, Пройдено: {passed}")
            
            return {
                'score': score,
                'feedback': feedback,
                'passed': passed,
                'ideal_answer': ideal_answer
            }

        except json.JSONDecodeError as je:
            logger.error(f"[ERROR][GigaChatService][evaluate_answer] Ошибка парсинга JSON: {je}")
            return {
                'score': 6.0,
                'feedback': 'Ошибка анализа ответа: не удалось распознать формат оценки.',
                'passed': True,
                'ideal_answer': ideal_answer
            }
        except Exception as e:
            print(f"❌ Ошибка GigaChatService.evaluate_answer: {e}")
            import traceback
            traceback.print_exc()
            logger.error(f'[ERROR][GigaChatService][evaluate_answer] Произошла ошибка {e}')
            return {
                'score': 6.0,
                'feedback': 'Оценка временно недоступна из‑за технической ошибки.',
                'passed': True,
                'ideal_answer': ideal_answer
            }

