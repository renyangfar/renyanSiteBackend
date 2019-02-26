import json

from flask import request

from modules.elasticSearch import get_es_client, get_query_dict
from . import blog

es_client = get_es_client()


@blog.route('/public/articles')
def public_articles():
    try:
        req_data = request.args
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
        data_list = [item['_source'] for item in res_hits]
        return json.dumps({"success": True, "data": data_list})
    except Exception as e:
        print(e)
        return json.dumps({"success": False, "data": e.message})


@blog.route('/user/articles')
def user_articles():
    try:
        req_data = request.args
        username, page, q_size, order, search_key = req_data.get('username', ''), int(req_data.get('page', 0)), int(
            req_data.get('size', 15)), req_data.get('order', 'created'), req_data.get('search_key', '')
        q_from = page * q_size
        q_filter = {
            "term": {
                "author.keyword": username
            }
        }
        q_sort = [
            {
                order: {
                    "order": "desc"
                }
            }
        ]
        q_should = []
        q_highlight = {}
        if search_key:
            q_should = [
                {
                    "match": {
                        "title": {
                            "query": search_key,
                            "boost": 5
                        }
                    }
                },
                {
                    "match": {
                        "body": {
                            "query": search_key,
                            "boost": 1
                        }
                    }
                }
            ]
            q_highlight = {
                "fields": {
                    "body": {}
                }
            }
            q_sort = []
        query_dict = get_query_dict(q_filter=q_filter, q_sort=q_sort, q_should=q_should, q_from=q_from, q_size=q_size,
                                    q_highlight=q_highlight)
        print(json.dumps(query_dict))
        res = es_client.search(index='test_site', body=query_dict)
        res_hits = res['hits']['hits']
        if not search_key:
            data_list = [item['_source'] for item in res_hits]
            for item in data_list:
                item['body'] = item['body'][:100]
        else:
            for item in res_hits:
                item['_source']['body'] = item['highlight']['body']
            data_list = [item['_source'] for item in res_hits]
        return json.dumps({"success": True, "data": data_list})
    except Exception as e:
        print(e)
        return json.dumps({"success": False, "data": e.message})


@blog.route('/user/articles/category')
def articles_category():
    try:
        req_data = request.args
        username = req_data.get('username', '')
        q_filter = {
            "term": {
                "author.keyword": username
            }
        }
        q_aggs = {
            "CATEGORY": {
                "terms": {
                    "field": "category.keyword",
                    "size": 10
                }
            }
        }
        query_dict = get_query_dict(q_filter=q_filter, q_aggs=q_aggs)
        print(json.dumps(query_dict))
        res = es_client.search(index='test_site', body=query_dict)
        buckets = res['aggregations']["CATEGORY"]['buckets']
        category_list = [item['key'] for item in buckets]
        return json.dumps({"success": True, "data": category_list})
    except Exception as e:
        print(e)
        return json.dumps({"success": False, "data": e.message})
