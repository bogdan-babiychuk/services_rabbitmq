from celery import Celery
import logging
from src.services.email_service.send_mail import send_email
import random

celery_app = Celery(
    "tasks",
    broker="redis://notice_redis:6379",
    backend="redis://notice_redis:6379"  
)




@celery_app.task
def send_notification(to_email, subject):
    try:
        code = random.randint(1000, 9000)
        body = f"Ты зарегался:\nКод подтверждения:{code}"
        send_email(to_email, subject, body)
        return f"Письмо отправлено: {to_email}"
    except Exception as e:
        logging.exception(f"Ошибка при отправке письма на {to_email}: {e}")
        raise
