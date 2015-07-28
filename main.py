__author__ = 'Kevin'

from elasticsearch import Elasticsearch

host = (['***'])

es = Elasticsearch(host)

result = es.search(
    index='routes_stage2',
    doc_type='route',
    body={"query":{"filtered":{"filter": {"geo_shape": {"geometry": {"relation": "intersects","shape": {"type": "envelope", "coordinates": [[2.06, 51.09],[5.59, 49.73]]}}}}}}}
)

print result