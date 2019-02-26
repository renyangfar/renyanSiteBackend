from ssl import create_default_context

import elasticsearch

blog_index = 'test_site'


def get_es_client(is_authorization=True):
    try:
        if is_authorization:
            # context = create_default_context(cafile="root-ca.pem")
            # es_client = elasticsearch.Elasticsearch(['203.91.58.43', ], http_auth=('admin', 'antiy123654'),
            #                                         scheme='https',
            #                                         port=9200,
            #                                         ssl_context=context, )
            es_client = elasticsearch.Elasticsearch(['https://admin:antiy123654@203.91.58.43:9200'], verify_certs=False,
                                                    use_ssl=True)
            return es_client
        else:
            es_servers = [{
                "host": "127.0.0.1",
                "port": "9200"
            }]
            es_client = elasticsearch.Elasticsearch(hosts=es_servers)
            return es_client
    except Exception as err:
        print err
        return None


def get_query_dict(q_filter=None, q_must=None, q_must_not=None, q_should=None,
                   q_aggs=None, q_from=0, q_size=0, q_sort=None, q_highlight=None):
    q_filter = q_filter if q_filter else []
    q_must = q_must if q_must else []
    q_must_not = q_must_not if q_must_not else []
    q_should = q_should if q_should else []
    q_sort = q_sort if q_sort else []
    q_aggs = q_aggs if q_aggs else {}
    q_highlight = q_highlight if q_highlight else {}

    query_dict = {
        "query": {
            "bool": {
                "filter": q_filter,
                "must": q_must,
                "must_not": q_must_not,
                "should": q_should
            }
        },
        "aggs": q_aggs,
        "from": q_from,
        "size": q_size,
        "sort": q_sort,
        "highlight": q_highlight,
    }
    return query_dict
