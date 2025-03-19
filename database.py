import asyncpg
import asyncio


class Database:
    def __init__(self, database: str) -> None:
        self.database = database

    async def __aenter__(self) -> "Database":
        self.connection = await asyncpg.connect(self.database)
        return self

    async def __aexit__(self, *exc) -> None:
        if self.connection:
            await self.connection.close()

    async def create_table(self) -> None:
        query = """
                CREATE TABLE IF NOT EXISTS users (
                    user_id BIGINT PRIMARY KEY,
                    recipient_id BIGINT
                )
                """
        await self.connection.execute(query)

    async def insert_data(self, params: tuple) -> None:
        query = """
                INSERT INTO users (user_id, recipient_id)
                VALUES ($1, $2)
                ON CONFLICT (user_id) DO UPDATE SET recipient_id = EXCLUDED.recipient_id
                """
        await self.connection.execute(query, *params)
