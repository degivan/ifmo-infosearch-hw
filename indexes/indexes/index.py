from collections import defaultdict

from indexes.docwork import docreader
from indexes.docwork.doc2words import extract_words

mdict = defaultdict(lambda : [])
urls = []


def code_to_byte(id):
    res = []
    # todo


def varbyte(docids):
    for i in range(1, len(docids)):
        docids[i] = docids[i] - docids[i - 1]
    docids.remove(0)

    res = []
    for id in docids:
        res += code_to_byte(id)

    return res


if __name__ == '__main__':
    reader = docreader.DocumentStreamReader(docreader.parse_command_line().files)

    for doc in reader:
        urls.append(doc.url)
        for word in extract_words(doc.text):
            mdict[word].append(len(urls))

    for word in mdict.keys():
        mdict[word] = varbyte(mdict[word])
    # todo
