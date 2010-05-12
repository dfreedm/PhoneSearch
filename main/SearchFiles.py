#!/usr/bin/env python
from lucene import QueryParser, IndexSearcher, StandardAnalyzer, FSDirectory, Hit,VERSION, initVM, CLASSPATH, IndexReader, MoreLikeThis
from md5 import md5
import re

def transform(hit):
    hit = Hit.cast_(hit).getDocument()
    contents = hit.get("contents").strip()
    contents = contents.replace("\n", "<br />")
    r1 = r"(\b(http|https)://([-A-Za-z0-9+&@#/%?=~_()|!:,.;]*[-A-Za-z0-9+&@#/%=~_()|]))"
    r2 = r"((^|\b)www\.([-A-Za-z0-9+&@#/%?=~_()|!:,.;]*[-A-Za-z0-9+&@#/%=~_()|]))"
    contents = re.sub(r2,r'<a rel="nofollow" target="_blank" href="http://\1">\1</a>',re.sub(r1,r'<a rel="nofollow" target="_blank" href="\1">\1</a>',contents))

    title = hit.get("contents")[:100] + "..."
    path = hit.get("path")
    unique = md5(hit.get("name")).hexdigest()
    return {"contents":contents, "title":title, "path":path, 'unique':unique }

def run(command):
    if command == '':
        return None
    STORE_DIR = "index"
    initVM(CLASSPATH)
    directory = FSDirectory.getDirectory(STORE_DIR, False)
    searcher = IndexSearcher(directory)
    analyzer = StandardAnalyzer()
    
    parser = QueryParser("contents", analyzer)
    parser.setDefaultOperator(QueryParser.Operator.AND)
    parser.setFuzzyMinSim(0.2)
    query = parser.parse(command)
    hits = map(transform, searcher.search(query))
    searcher.close()
    return hits

def similar(command, docno):
    STORE_DIR = "index"
    initVM(CLASSPATH)
    directory = FSDirectory.getDirectory(STORE_DIR, False)
    searcher = IndexSearcher(directory)
    analyzer = StandardAnalyzer()
    
    parser = QueryParser("contents", analyzer)
    parser.setDefaultOperator(QueryParser.Operator.AND)
    parser.setFuzzyMinSim(0.2)
    query = parser.parse(command)
    hits = searcher.search(query)
    document = hits.id(docno)

    ir = IndexReader.open(STORE_DIR)
    mlt = MoreLikeThis(ir)
    mlt.setFieldNames(['name', 'contents'])
    mlt.setMinWordLen(2)
    mlt.setBoost(True)
    query = mlt.like(document)
    hits = map(transform, searcher.search(query))
    searcher.close()
    return hits
