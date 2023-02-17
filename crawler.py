import json
from sys import argv
import time
import argparse
from chrome import Chrome
from libkafka import Kafka
from parsers import Sahamyab
from elastic_search import ElasticSearch

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="Print verbose messages", action="store_true")

es_group = parser.add_argument_group("Elasticsearch")
es_group.add_argument("--es-host", help="Elasticsearch address [http://host:port]", type=str, required=True)
es_group.add_argument("--es-index", help="Elasticsearch index", type=str, required=True)

kafka_group = parser.add_argument_group("Kafka")
kafka_group.add_argument("--kafka-host", help="Kafka host address", nargs="+", type=str, required=True)

args = parser.parse_args()

es = ElasticSearch(args.es_host, args.es_index)

kafka = Kafka()
kafka.init_consumer("crawler-urls", bootstrap_servers=args.kafka_host, group_id="crawler-urls", max_poll_records=1)


while True:
    data = None
    log = kafka.get_log(blocking_mode=True)

    if log == None or len(log) == 0:
        if args.verbose:
            print("Empty log [skipped]", flush=True)
            continue

    if log[0] == "1":
        data = json.loads(log[1])

    if data is None:
        if args.verbose:
            print("Invalid log:", log)
        continue

    driver = None
    browser = Chrome(data["url"], 768)

    if args.verbose:
        print("Processing:", data["url"], flush=True)

    if data["website"] == "www.sahamyab.com":
        driver = Sahamyab(browser.page_source, "html.parser")

    while True:
        tweets = driver.tweets()

        if args.verbose:
            print("%i tweets fetched..." %(len(tweets)), flush=True)

        if not es.create_bulk(tweets):
            if args.verbose:
                print("Reached to a tweet that is already in our database, discontinuing...", flush=True)
            break

        browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(5)