#!/usr/bin/env python
# coding=utf-8
import pika
import socket
import sys

host = "rmq03"          # <-- ИЗМЕНИТЕ на IP/имя узла, если скрипт не на брокере
vhost = "/"
username = "myuser"
password = "mypass"
port = 5672

# 1. Быстрая проверка: можем ли мы соединиться с портом?
print(f" [*] Проверка доступности {host}:{port}...")
try:
    sock = socket.create_connection((host, port), timeout=5)
    sock.close()
    print(" [OK] Порт 5672 доступен.")
except Exception as e:
    print(f" [ERROR] Не удалось соединиться с {host}:{port}: {e}")
    print("Это значит, что брокер не запущен, слушает другой интерфейс или порт закрыт фаерволом.")
    sys.exit(1)

# 2. Подключение через Pika
credentials = pika.PlainCredentials(username, password)
parameters = pika.ConnectionParameters(
    host=host,
    virtual_host=vhost,
    credentials=credentials,
    heartbeat=600,
    connection_attempts=5,
    retry_delay=2.0
)

try:
    print(f" [*] Подключение к RabbitMQ...")
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    print(" [OK] Соединение установлено.")
except pika.exceptions.AMQPConnectionError as e:
    print(f" [ERROR] Ошибка AMQP-подключения: {e}")
    print("Возможные причины: неверные логин/пароль, неверный vhost, брокер отверг соединение.")
    sys.exit(1)
except Exception as e:
    print(f" [ERROR] Другая ошибка: {e}")
    sys.exit(1)

# 3. Объявление очереди
try:
    channel.queue_declare(queue='hello', durable=True)
    print(" [OK] Очередь 'hello' объявлена.")
except Exception as e:
    print(f" [ERROR] Ошибка объявления очереди: {e}")
    print("Возможно, очередь уже создана с несовместимыми параметрами. Удалите её через rabbitmqctl.")
    connection.close()
    sys.exit(1)

def callback(ch, method, properties, body):
    print(f" [x] Received {body!r}")

channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

try:
    channel.start_consuming()
except KeyboardInterrupt:
    print("\n [*] Остановка по запросу пользователя.")
    connection.close()
