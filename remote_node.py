import os
import json
import time
from kafka import KafkaConsumer
import redis

KAFKA_TOPIC = os.environ['KAFKA_TOPIC']
KAFKA_SERVER = os.environ['KAFKA_SERVER']
KAFKA_CONSUMER_GROUP = os.environ['KAFKA_CONSUMER_GROUP']
REDIS_SERVER = os.environ['REDIS_SERVER']
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')
REDIS_PUBSUB_CHANNEL = os.environ.get('REDIS_PUBSUB_CHANNEL', 'word_count_updates')
FETCH_INTERVAL = os.environ.get('FETCH_INTERVAL', '1')


def word_count(text_data):
    counts = dict()
    words = text_data.split()
    for w in words:
        if w in counts:
            counts[w] += 1
        else:
            counts[w] = 1
    return counts


def update_word_count(token, count):
    redis_conn.hincrby('word_count', token, count)
    print('')

    #redis_conn.publish(REDIS_PUBSUB_CHANNEL, json.dumps({'word': token, 'count': int(redis_conn.get(word))}))


if __name__ == '__main__':
    kafka_consumer = KafkaConsumer(KAFKA_TOPIC, bootstrap_servers=[KAFKA_SERVER], group_id=KAFKA_CONSUMER_GROUP,
                                   auto_offset_reset='earliest')
    redis_conn = redis.Redis(host=REDIS_SERVER, port=REDIS_PORT)

    while True:
        for message in kafka_consumer:
            text = message.value.decode()
            print('--> consumed text: ', text)
            words_count = word_count(text)
            for word in words_count.keys():
                update_word_count(word, words_count[word])
        time.sleep(int(FETCH_INTERVAL))
