import aiosqlite
import config

async def connect():

    db = await aiosqlite.connect(config.DATABASE)

    await db.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        xp INTEGER,
        level INTEGER,
        money INTEGER
    )
    """)

    await db.execute("""
    CREATE TABLE IF NOT EXISTS warnings(
        user_id INTEGER,
        reason TEXT
    )
    """)

    await db.commit()

    return db