from datetime import datetime
import json
import os

import aio_pika
import pytz

RABBIT_HOST = os.getenv("RABBIT_HOST", "localhost")
RABBIT_PORT = os.getenv("RABBIT_PORT", "5672")
RABBIT_USER = os.getenv("RABBIT_USER", "guest")
RABBIT_PASS = os.getenv("RABBIT_PASS", "guest")
DATE_FORMAT = "%Y-%m-%d %H:%M:%S %z"


async def publish_ingest_completed(catalog_type: str, start_date: datetime) -> None:
    connection = await aio_pika.connect_robust(
        f"amqp://{RABBIT_USER}:{RABBIT_PASS}@{RABBIT_HOST}:{RABBIT_PORT}",
    )

    async with connection:
        channel = await connection.channel()
        exchange = await channel.declare_exchange(
            name="harvests", type=aio_pika.ExchangeType.TOPIC
        )

        await exchange.publish(
            aio_pika.Message(
                body=json.dumps(
                    {
                        "start": start_date.strftime(DATE_FORMAT),
                        "end": datetime.now(pytz.timezone("Europe/Oslo")).strftime(
                            DATE_FORMAT
                        ),
                    }
                ).encode()
            ),
            routing_key=f"{catalog_type}.ingested",
        )
