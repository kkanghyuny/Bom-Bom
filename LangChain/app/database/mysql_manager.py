import aiomysql
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
from app.config import settings

logger = logging.getLogger(__name__)

class MySQLManager:
    def __init__(self):
        """데이터베이스 매니저 초기화"""
        self.pool = None
        self.config = {
            "host": settings.mysql.host,
            "port": settings.mysql.port,
            "db": settings.mysql.database,
            "user": settings.mysql.user,
            "password": settings.mysql.password,
            "charset": settings.mysql.charset,
            "autocommit": True
        }

    async def initialize(self):
        """비동기 풀 초기화"""
        if not self.pool:
            self.pool = await aiomysql.create_pool(**self.config)
            logger.info("MySQL connection pool established")

    async def close(self):
        """연결 종료"""
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
            logger.info("MySQL connection pool closed")

    async def get_conversation_status(self, conversation_id: int) -> Optional[Dict]:
        """대화 상태 조회"""
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                try:
                    await cursor.execute("""
                        SELECT c.*, COUNT(m.id) as message_count
                        FROM Conversation c
                        LEFT JOIN Memory m ON c.conversation_id = m.conversation_id
                        WHERE c.conversation_id = %s
                        GROUP BY c.conversation_id
                    """, (conversation_id,))
                    result = await cursor.fetchone()
                    return dict(result) if result else None
                except Exception as e:
                    logger.error(f"Failed to get conversation status: {str(e)}")
                    return None

    async def get_conversation_memories(self, conversation_id: int) -> List[Dict]:
        """대화 메모리 조회"""
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                try:
                    await cursor.execute("""
                        SELECT *
                        FROM Memory
                        WHERE conversation_id = %s
                        ORDER BY id ASC
                    """, (conversation_id,))
                    results = await cursor.fetchall()
                    
                    # JSON 필드 파싱
                    for result in results:
                        if result.get('keywords'):
                            result['keywords'] = json.loads(result['keywords'])
                        if result.get('response_plan'):
                            result['response_plan'] = json.loads(result['response_plan'])
                    
                    return [dict(row) for row in results]
                except Exception as e:
                    logger.error(f"Failed to get conversation memories: {str(e)}")
                    return []

    async def start_conversation(self, memory_id: int, senior_id: int = 1) -> Optional[int]:
        """새로운 대화 세션 시작"""
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                try:
                    await cursor.execute("""
                        INSERT INTO Conversation (memory_id, senior_id, start_date)
                        VALUES (%s, %s, CURDATE())
                    """, (memory_id, senior_id))
                    return cursor.lastrowid
                except Exception as e:
                    logger.error(f"Failed to start conversation: {str(e)}")
                    return None

    async def save_memory(self, data: Dict) -> Optional[int]:
        """메모리 저장"""
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                try:
                    # JSON 필드 직렬화
                    keywords = json.dumps(data.get('keywords', []))
                    response_plan = json.dumps(data.get('response_plan', []))
                    
                    await cursor.execute("""
                        INSERT INTO Memory (
                            memory_id, conversation_id, speaker, content, 
                            summary, positivity_score, keywords, response_plan
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        data['memory_id'],
                        data['conversation_id'],
                        data['speaker'],
                        data['content'],
                        data.get('summary'),
                        data.get('positivity_score', 50),
                        keywords,
                        response_plan
                    ))
                    return cursor.lastrowid
                except Exception as e:
                    logger.error(f"Failed to save memory: {str(e)}")
                    return None

    async def end_conversation(self, conversation_id: int) -> bool:
        """대화 세션 종료"""
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                try:
                    # 평균 점수 계산 및 종료 시간 업데이트
                    await cursor.execute("""
                        UPDATE Conversation c
                        SET end_time = CURTIME(),
                            avg_score = (
                                SELECT AVG(positivity_score)
                                FROM Memory
                                WHERE conversation_id = %s
                            )
                        WHERE conversation_id = %s
                    """, (conversation_id, conversation_id))
                    return True
                except Exception as e:
                    logger.error(f"Failed to end conversation: {str(e)}")
                    return False