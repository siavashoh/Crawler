import json
import sys
import requests


class ElasticSearch:
    def __init__(self, host: str, index: str) -> None:
        self._host = host
        self._index = index

        resp = requests.get(self._host_index())

        if resp.status_code == 404:
            self._create_index()

    def _host_index(self):
        return f"{self._host}/{self._index}"

    def _create_index(self):
        resp = requests.put(
            self._host_index(),
            json.dumps(self._mapping()),
            headers={"Content-Type": "application/json"},
        )

        if resp.status_code != 200:
            print(
                "Couldn't create the index:",
                self._index,
                resp.text,
                resp.status_code,
                file=sys.stderr,
                flush=True,
            )

    def create_bulk(self, data: dict) -> bool:
        query = []
        result = True
        for id in data:
            query.append(json.dumps({"create": {"_index": self._index, "_id": id}}))
            query.append(json.dumps(data[id]))
            if len(query) % 1000 == 0:
                resp = requests.post(
                    f"{self._host}/_bulk",
                    "\n".join(query) + "\n",
                    headers={"Content-Type": "application/json"},
                )
                query = []
                if resp.status_code == 200:
                    resp = json.loads(resp.text)
                    if not resp["errors"]:
                        continue
                    else:
                        result = False

        if len(query):
            resp = requests.post(
                f"{self._host}/_bulk",
                "\n".join(query) + "\n",
                headers={"Content-Type": "application/json"},
            )
            if resp.status_code == 200:
                resp = json.loads(resp.text)
                result = not resp["errors"]

        return result

    def _mapping(self):
        return {
            "mappings": {
                "properties": {
                    "id": {"type": "keyword"},
                    "content": {"type": "text"},
                    "create_at": {
                        "type": "date",
                        "format": "strict_date_optional_time||epoch_millis",
                    },
                    "username": {"type": "keyword"},
                    "userid": {"type": "keyword"},
                    "retweet": {
                        "type": "object",
                        "properties": {
                            "userid": {"type": "keyword"},
                            "username": {"type": "keyword"},
                            "content": {"type": "text"},
                        },
                    },
                }
            }
        }
