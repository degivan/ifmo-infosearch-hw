import pickle as pkl
import struct
from collections import defaultdict

from doc2words import extract_words

import docreader


def code_to_byte(id):
    result = bytearray()
    while id > 127:
        result.append(id & 127)
        id >>= 7
    result.append((id & 127) + 128)
    return result


def decode_vb(coded_id):
    x = 0
    for i, code in enumerate(coded_id):
        if code < 128:
            x += (1 << 7 * i) * code
        elif code <= 255:
            x += (1 << 7 * i) * (code - 128)
            break
    return x


def decode_vb_array(vb):
    coded_ids = []
    prev = -1
    for i, s in enumerate(vb):
        if s > 127 <= 255:
            coded_ids.append(vb[(prev + 1):(i + 1)])
            prev = i
    diffs = [decode_vb(coded_id) for coded_id in coded_ids]
    res = [diffs[0]]
    for diff in diffs[1:]:
        res.append(res[-1] + diff)
    return res


def code_varbyte(docids):
    res = bytearray()
    for id in docids:
        res += code_to_byte(id)
    res = struct.pack('I',  len(res)) + res
    return res


if __name__ == '__main__':
    reader = docreader.DocumentStreamReader(docreader.parse_command_line().files)
    mdict = defaultdict(lambda: [])
    urls = []

    for doc in reader:
        urls.append(doc.url)
        for word in extract_words(doc.text):
            mdict[word].append(len(urls))
    for term in mdict.keys():
        docids = mdict[term]
        for i in reversed(range(1, len(docids))):
            docids[i] = docids[i] - docids[i - 1]
        docids = filter(lambda x: x != 0, docids)
        mdict[term] = docids

    for word in mdict.keys():
        mdict[word] = code_varbyte(mdict[word])

    id_url = {}
    term_position = {}
    with open('index', 'wb') as f:
        for term, coded_ids in mdict.iteritems():
            term_position[term] = f.tell()
            f.write(coded_ids)
    with open('term_position', 'wb') as f:
        pkl.dump(term_position, f)
    with open('id_url', 'wb') as f:
        for i, url in enumerate(urls):
            id_url[(i + 1)] = url
        pkl.dump(id_url, f)
