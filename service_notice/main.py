import asyncio
import aio_pika
import json
import logging
from src.celery_repo.celery_config import celery_app

logging.basicConfig(level=logging.INFO)
# Функции обработки для разных очередей
async def handle_registration(message: aio_pika.IncomingMessage):
    async with message.process():
        data = json.loads(message.body)
        logging.info(f"Получено уведомление:\n{data}")
        
        # Отправляем задачу в фоновом режиме, не дожидаясь результата
        celery_app.send_task(
            "src.celery_repo.celery_config.send_notification",
            args=[data.get("email"), "Регистрация"]
        )

        # Программа продолжает выполнение
        logging.info("Задача отправлена в фоновом режиме, не дожидаемся результата.")

# async def handle_password_change(message: aio_pika.IncomingMessage):
#     async with message.process():
#         data = json.loads(message.body)
#         print(f"Обработано уведомление о смене пароля: {data}")
#         # Здесь вы можете вызвать свою логику для обработки уведомления о смене пароля

# async def handle_subscription(message: aio_pika.IncomingMessage):
#     async with message.process():
#         data = json.loads(message.body)
#         print(f"Обработано уведомление о подписке: {data}")
#         # Здесь вы можете вызвать свою логику для обработки уведомления о подписке

# Функция для подключения и обработки очередей
async def consume_queues():
    # Подключаемся к RabbitMQ
    count = 1
    while True:
        try:
            connection = await aio_pika.connect_robust(url="amqp://rabbitmq:5672/",
                                               login="guest",
                                               password="guest")
            break
        except Exception as e:
            count += 1
            logging.info(f"Попытка: №{count}")
            await asyncio.sleep(5)
    logging.info(f"МЫ подключились")
    async with connection:
        async with connection.channel() as channel:
            queue_register = await channel.declare_queue('register_queue', durable=True)
            # Создаем обработку сообщений для каждой очереди
            # await asyncio.gather(
            #     queue_register.consume(handle_registration),
            # )
            await queue_register.consume(callback=handle_registration)
            await asyncio.Future()
# Запуск функции
asyncio.run(consume_queues())



# async def handle_registration(message: aio_pika.IncomingMessage):
#     try:
#         data = json.loads(message.body)
#         # выполняем работу
#         celery_app.send_task(
#             "src.celery_repo.celery_config.send_notification",
#             args=[data.get("email"), "Регистрация"]
#         )
#         await message.ack()  # вручную подтверждаем обработку
#         logging.info("Успешно обработали сообщение и отправили ack.")
#     except Exception as e:
#         await message.nack(requeue=True)  # возвращаем сообщение в очередь
#         logging.error(f"Ошибка при обработке сообщения: {e}")
