from time import sleep
import json
from libkafka import Kafka
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="Print verbose messages", action="store_true")

kafka_group = parser.add_argument_group("Kafka")
kafka_group.add_argument("--kafka-host", help="Kafka host address", nargs="+", type=str, required=True)

args = parser.parse_args()

kafka = Kafka()
kafka.init_producer(bootstrap_servers=args.kafka_host)

urls = [
    {
        "website": "www.sahamyab.com",
        "tag": "ختور",
        "url": "https://www.sahamyab.com/hashtag/%D8%AE%D8%AA%D9%88%D8%B1",
    },
    {
        "website": "www.sahamyab.com",
        "tag": "دی",
        "url": "https://www.sahamyab.com/hashtag/%D8%AF%DB%8C",
    },
    {
        "website": "www.sahamyab.com",
        "tag": "خودرو",
        "url": "https://www.sahamyab.com/hashtag/%D8%AE%D9%88%D8%AF%D8%B1%D9%88",
    },
    {
        "website": "www.sahamyab.com",
        "tag": "خساپا",
        "url": "https://www.sahamyab.com/hashtag/%D8%AE%D8%B3%D8%A7%D9%BE%D8%A7",
    },
    {
        "website": "www.sahamyab.com",
        "tag": "خگستر",
        "url": "https://www.sahamyab.com/hashtag/%D8%AE%DA%AF%D8%B3%D8%AA%D8%B1",
    },
]

while True:
    for u in urls:
        kafka.log("crawler-urls", 1, [json.dumps(u)])
        print("Logging:", u)
    sleep(30)