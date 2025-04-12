from email import message
from email.mime.text import MIMEText
import logging
from math import log
import smtplib
from abc import ABC, abstractmethod


class SendEmailNotification(ABC):

    @abstractmethod
    def send_email(self, to_email, subject, body):
        pass
    


class SendMailNotification(SendEmailNotification):

    def send_email(self, to_email, subject, body):
        sender = "babiychuk.bogdan@mail.ru"
        password = "e64ncCh5V95FfQwzge3e"  # Пароль приложения
        
        try:
            with smtplib.SMTP_SSL('smtp.mail.ru', 465) as server:
                # server.starttls()
                server.login(sender, password)
                
                msg = MIMEText(body, _charset="utf-8")
                msg["From"] = sender
                msg["To"] = to_email
                msg["Subject"] = subject
                
                server.send_message(msg)
                logging.info("Письмо успешно отправлено")
        except Exception as e:
            logging.error(f"Ошибка: {e}")

class SendGmailNotification(SendEmailNotification):
    def send_email(self, to_email, subject, body):
        sender = "bogdan.babiychuk.2k@gmail.com"
        password = "zaumpnslallvqvon"  # Пароль приложения
        
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender, password)
                
                msg = MIMEText(body, _charset="utf-8")
                msg["From"] = sender
                msg["To"] = to_email
                msg["Subject"] = subject
                
                server.send_message(msg)
                logging.info("Письмо успешно отправлено")
        except Exception as e:
            logging.error(f"Ошибка: {e}")

class SendYandexNotification(SendEmailNotification):
    pass


def send_email(to_email:str, subject:str, body:str):
    domen = to_email.split("@")[-1]
    try:
        match domen:
            case "mail.ru":
                logging.info(f"Отправляем сообщение: {body}")
                SendMailNotification().send_email(to_email, subject, body)
            case "yandex.ru":
                SendYandexNotification().send_email(to_email, subject, body)
            case "gmail.com":
                logging.info(f"Отправляем сообщение: {body}")
                SendGmailNotification().send_email(to_email, subject, body)
            case _:
                raise ValueError(f"Неизвестный почтовый домен: {domen}")
    except Exception as _e:
        logging.error(f"Ошибка при отправке письма\n{_e}")
