# coding=utf-8
# !/usr/bin/env python

import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='10.10.133.160'))
channel = connection.channel()
# 持久化队列
channel.queue_declare(queue='task_queue', durable=True)
print '[*] waiting for message. To exit press CTRL+C'


def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)
    time.sleep(body.count('.'))
    print " [x] Done"
    # 消息确认
    ch.basic_ack(delivery_tag=method.delivery_tag)


# 同一时刻，不要发送超过1条消息给一个工作者
channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='task_queue')

channel.start_consuming()
