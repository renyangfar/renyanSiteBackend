import json

from flask import request

from app.blog import es_client
from modules.elasticSearch import get_query_dict, blog_index


def handle_public_articles():
    try:
        req_data = request.args
        page, q_size, order = int(
            req_data.get('page', 0)), int(
            req_data.get('size', 10)), req_data.get(
            'order', 'updated')
        q_from = page * q_size
        q_filter = {
            "term": {
                "isPublish": True
            }
        }
        q_sort = [
            {
                order: {
                    "order": "desc"
                }
            }
        ]
        query_dict = get_query_dict(q_filter=q_filter, q_sort=q_sort, q_from=q_from, q_size=q_size)
        print(json.dumps(query_dict))
        res = es_client.search(index=blog_index, body=query_dict)
        res_hits = res['hits']['hits']
        data_list = []
        for item in res_hits:
            _source = item['_source']
            _source['_id'] = item['_id']
            _source['body'] = _source['body'][:180]
            data_list.append(_source)

        return json.dumps({"success": True, "data": data_list})
    except Exception as e:
        print("raise error: %s" % e.message)
        return json.dumps({"success": False, "data": e.message})
