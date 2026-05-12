import asyncio
from app.core.database import AsyncSessionLocal
from app.core_config import KAFKA_BOOTSTRAP_SERVERS
from app.repositories.profile_repository import ProfileRepository
from common.kafka.consumer import build_consumer


async def consume_user_registered():
    consumer = build_consumer(
        topic="user.registered",
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id="user-service-profile-group",
    )
    await consumer.start()
    try:
        async for message in consumer:
            event = message.value
            async with AsyncSessionLocal() as db:
                await ProfileRepository.upsert_from_registered_event(
                    db=db,
                    user_id=int(event["user_id"]),
                    email=event["email"],
                )
            await consumer.commit()
    finally:
        await consumer.stop()
