import os

import redis
from rq import Worker, Queue, Connection

listen = ['default']

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
print(redis_url)

#conn = redis.from_url(redis_url)
conn = redis.Redis(host='localhost',port=6379,password="reallylongpasswordgoeshere")
print(conn)
conn.ping()

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()