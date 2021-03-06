# coding=utf-8
# !/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='10.10.133.160'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs',
                         type='direct')

result = channel.queue_declare(exclusive=True) # 当与消费者（consumer）断开连接的时候，这个队列应当被立即删除。exclusive标识符即可达到此目的。
queue_name = result.method.queue

severities = sys.argv[1:]
if not severities:
    print >> sys.stderr, "Usage: %s [info] [warning] [error]" % \
                         (sys.argv[0],)
    sys.exit(1)

for severity in severities:
    channel.queue_bind(exchange='direct_logs',
                       queue=queue_name,
                       routing_key=severity)

print ' [*] Waiting for logs. To exit press CTRL+C'


def callback(ch, method, properties, body):
    print " [x] %r:%r" % (method.routing_key, body,)


channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
