import json

from flask import request

from modules.elasticSearch import get_es_client, get_query_dict
from . import blog

es_client = get_es_client()


@blog.route('/public/articles')
def index():
    try:
        req_data = request.form
        page, q_size = int(req_data.get('page', 0)), int(req_data.get('size', 15))
        q_from = page * q_size
        q_filter = {
            "term": {
                "isPublish": True
            }
        }
        q_sort = [
            {
                "updated.keyword": {
                    "order": "desc"
                }
            }
        ]
        query_dict = get_query_dict(q_filter=q_filter, q_sort=q_sort, q_from=q_from, q_size=q_size)
        print(json.dumps(query_dict))
        res = es_client.search(index='test_site', body=query_dict)
        res_hits = res['hits']['hits']
        data_list = [item['_source']  for item in res_hits]
        return json.dumps({"success": True, "data": data_list})
    except Exception as e:
        print(e)
        return json.dumps({"success": False, "data": e.message})
