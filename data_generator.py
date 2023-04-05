import time
import random
from kafka import KafkaProducer


KAFKA_SERVER = 'localhost:9092'
REMOTE_MACHINES_COUNT = 3
KAFKA_TOPICS = []
for i in range(REMOTE_MACHINES_COUNT):
    KAFKA_TOPICS.append('remote-' + str(i+1))


def generate_text():
    words = ['apple', 'banana', 'cherry', 'date', 'elderberry', 'fig', 'grape', 'honeydew', 'orange', 'pear']
    text = ' '.join(random.choices(words, k=random.randint(5, 10)))
    return text


if __name__ == '__main__':
    kafka_producer = KafkaProducer(bootstrap_servers=[KAFKA_SERVER])

    while True:
        text = generate_text()
        topic = random.choice(KAFKA_TOPICS)
        print('--> Topic: ', topic, ' -- ', text)
        kafka_producer.send(topic, text.encode())
        time.sleep(1)
