from bs4 import BeautifulSoup as BS

class Sahamyab(BS):
    _check_list = { }

    def __init__(self, markup="", features=None, builder=None,
                parse_only=None, from_encoding=None, exclude_encodings=None,
                element_classes=None, **kwargs):
        super(Sahamyab, self).__init__(markup, features, builder, parse_only, from_encoding, exclude_encodings, element_classes, **kwargs)

    def tweets(self):
        result = { }
        elems = self._tweets()
        if len(elems) == 0:
            return result;

        for elem in elems:
            if elem.select_one(".boxMainAdvertise") is not None:
                continue
            info, id = self._tweet_data(elem)
            if not id in self._check_list:
                result[id] = info

        return result

    def _tweets(self) -> list:
        return self.select("virtual-scroller app-twit-input-show article")

    def _tweet_data(self, elem) -> dict:
        id = self._tweet_id(elem)
        return {
            "id": id,
            "content": self._tweet_content(elem),
            "create_at": self._tweet_created_at(elem),
            "username": self._tweet_username(elem),
            "userid": self._tweet_userid(elem),
            "retweet": self._retweet(elem)
        }, id

    def _tweet_id(self, elem):
        el = elem.select_one(".twitsContents")
        if el is not None:
            return el.attrs["id"].replace("postId", "")
        return el

    def _tweet_content(self, elem):
        el = elem.select_one(".twitsContents")
        if el is not None:
            return el.text
        return el

    def _tweet_created_at(self, elem):
        el = elem.select_one("app-timeago div[data-timeago]")
        if el is not None:
            return el.attrs["data-timeago"]
        return el

    def _tweet_username(self, elem):
        el = elem.select_one(".lastNameUser")
        if el is not None:
            return el.text
        return el

    def _tweet_userid(self, elem):
        el = elem.select_one(".UserName")
        if el is not None:
            return el.text
        return el

    def _retweet(self, elem):
        retel = elem.select_one(".retweetBox")
        if retel is None:
            return retel
        return {
            "userid": self._tweet_userid(retel),
            "username": self._tweet_username(retel),
            "content": self._tweet_content(retel)
        }