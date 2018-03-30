import pickle as pkl
import struct

from index import decode_vb_array

id_url = {}
term_position = {}


def find_docs(term, index):
    pos = term_position.get(term, None)
    if pos is None:
        return set()
    else:
        index.seek(pos)
        vb_len = struct.unpack('I', index.read(4))[0]
        vb = map(ord, index.read(vb_len))
        return set(decode_vb_array(vb))


def search(terms, index):
    docs = find_docs(terms[0], index)
    for term in terms[1:]:
        docs = docs.intersection(find_docs(term, index))
    return sorted(docs)


if __name__ == '__main__':
    with open('id_url', 'rb') as f:
        id_url = pkl.load(f)
    with open('term_position', 'rb') as f:
        term_position = pkl.load(f)

    with open('index', 'rb') as index:
        while True:
            try:
                query = raw_input()
                print query
                query = query.decode("utf-8")
                docs = search(query.strip().lower().replace(' ', '').split('&'), index)
                print len(docs)
                for id in docs:
                    print id_url[id]
            except EOFError:
                break
