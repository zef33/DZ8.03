#!/usr/bin/env python
# coding=utf-8
import pika
import sys

host = "rmq03"
username = "myuser"
password = "mypass"
vhost = "/"

credentials = pika.PlainCredentials(username, password)
parameters = pika.ConnectionParameters(
    host=host,
    virtual_host=vhost,
    credentials=credentials,
    heartbeat=600,
    connection_attempts=5
)

try:
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # durable=True — очередь переживёт рестарт брокера
    channel.queue_declare(queue='hello', durable=True)

    # delivery_mode=2 — сообщение тоже станет persistent
    channel.basic_publish(
        exchange='',
        routing_key='hello',
        body='Hello Netology!',
        properties=pika.BasicProperties(delivery_mode=2)
    )
    print(" [x] Сообщение успешно отправлено")
    connection.close()
except Exception as e:
    print(f" [ERROR] {e}")
    sys.exit(1)
