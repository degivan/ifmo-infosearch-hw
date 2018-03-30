#!/usr/bin/env python

"""
This is just a draft for homework 'near-duplicates'
Use MinshinglesCounter to make result closer to checker
"""

import sys
import re
import mmh3
from docreader import DocumentStreamReader


class MinshinglesCounter:
    SPLIT_RGX = re.compile(r'\w+', re.U)

    def __init__(self, window=5, n=20):
        self.window = window
        self.n = n

    def count(self, text):
        words = MinshinglesCounter._extract_words(text)
        shs = self._count_shingles(words)
        mshs = self._select_minshingles(shs)

        if len(mshs) == self.n:
            return mshs

        if len(shs) >= self.n:
            return sorted(shs)[0:self.n]

        return None

    def _select_minshingles(self, shs):
        buckets = [None] * self.n
        for x in shs:
            bkt = x % self.n
            buckets[bkt] = x if buckets[bkt] is None else min(buckets[bkt], x)

        return filter(lambda a: a is not None, buckets)

    def _count_shingles(self, words):
        shingles = []
        for i in xrange(len(words) - self.window):
            h = mmh3.hash(' '.join(words[i:i + self.window]).encode('utf-8'))
            shingles.append(h)
        return sorted(shingles)

    @staticmethod
    def _extract_words(text):
        words = re.findall(MinshinglesCounter.SPLIT_RGX, text)
        return words


def main():
    mhc = MinshinglesCounter()

    signatures = []
    for path in sys.argv[1:]:
        for doc in DocumentStreamReader(path):
            signatures.append((doc.url, mhc.count(doc.text)))
    size = len(signatures)
    for i in range(size):
        for j in range(i + 1, size):
            sig1 = signatures[i]
            sig2 = signatures[j]
            if sig1[1] is None or sig2[1] is None:
                continue
            shset1 = set(sig1[1])
            shset2 = set(sig2[1])
            jaccard = len(shset1 & shset2) / float(len(shset1 | shset2))
            if jaccard > 0.75:
                print ' '.join([sig1[0], sig2[0], str(jaccard)])


if __name__ == '__main__':
    main()
