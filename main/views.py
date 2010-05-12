from SearchFiles import run, transform, similar as _similar
from django.shortcuts import render_to_response
import re

def index(request):
    # return the search page
    return render_to_response('index.html')

def search(request, page="1"):
    page = int(page)
    query = request.GET.get("query")
    results = run(query)
    count = len(results)
    results = results[page-1:(page-1)+25]
    # bold the query terms in the documents
    #for word in query.split():
    #    for result in results:
    #        regex = re.compile(word, re.IGNORECASE)
    #        #result['contents'] = regex.sub("<b>%s</b>" % word, result['contents'])
    if count < 1:
        count = None
    return render_to_response('index.html', {'results':enumerate(results), 'count':count, 'query':query })

def similar(request, page = "1"):
    page = int(page)
    query = request.GET.get("query")
    docno = request.GET.get("docno")
    print query
    print docno

    results = _similar(query, int(docno))
    count = len(results)
    results = results[page-1:(page-1) + 25]
    # bold the query terms in the documents
    #for word in query.split():
    #    for result in results:
    #        regex = re.compile(word, re.IGNORECASE)
    #        #result['contents'] = regex.sub("<b>%s</b>" % word, result['contents'])
    if count < 1:
        count = None
    return render_to_response('index.html', {'results':enumerate(results), 'count':count, 'query':query })

