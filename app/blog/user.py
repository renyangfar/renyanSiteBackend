import json
import threading
import time

from flask import request
from flask_login import login_required, current_user

from blog import es_client
from modules.elasticSearch import get_query_dict, blog_index


def handle_user_articles():
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
        res = es_client.search(index=blog_index, body=query_dict)
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


def handle_articles_category():
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
        res = es_client.search(index=blog_index, body=query_dict)
        buckets = res['aggregations']["CATEGORY"]['buckets']
        category_list = [item['key'] for item in buckets]
        return json.dumps({"success": True, "data": category_list})
    except Exception as e:
        print(e)
        return json.dumps({"success": False, "data": e.message})


def handle_get_articles():
    try:
        req_data = request.args
        _id = req_data.get('_id', ' ')
        q_filter = {
            "term": {
                "_id": _id
            }
        }
        query_dict = get_query_dict(q_filter=q_filter, q_size=1)
        print(json.dumps(query_dict))
        res = es_client.search(index=blog_index, body=query_dict)
        data = res['hits']['hits']
        threading.Thread(target=update_browse_mount, args=(_id,)).start()
        return json.dumps({"success": True, "data": data})
    except Exception as e:
        print(e)
        return json.dumps({"success": False, "data": e.message})


def update_browse_mount(_id):
    try:
        es_client.update(index=blog_index, doc_type='doc', id=_id, body={
            "script": "ctx._source.browse_mount += 2"
        })
    except Exception as e:
        print(e)


@login_required
def handle_post_articles():
    try:
        req_data = request.form
        title, body, category, isPublish = req_data.get('title', ''), req_data.get('body', ''), \
                                           req_data.get('category', ''), req_data.get('isPublish', False)
        author = current_user.username
        browse_mount = 1
        created = updated = time.strftime('%Y-%m-%dT%H:%M:%S')
        insert_body = {'title': title, 'body': body, 'category': category, 'isPublish': isPublish, 'author': author,
                       'brower_mount': browse_mount, 'created': created, 'updated': updated}
        res = es_client.index(index=blog_index, doc_type='doc', body=insert_body)
        return json.dumps({"success": True, "data": res['_shards']})
    except Exception as e:
        print(e)
        return json.dumps({"success": False, "data": e.message})


@login_required
def handle_put_articles():
    try:
        req_data = request.form
        _id, title, body, category, isPublish = req_data.get('_id', ''), req_data.get('title', ''), \
                                                req_data.get('body', ''), req_data.get('category', ''), \
                                                req_data.get('isPublish', False)
        updated = time.strftime('%Y-%m-%dT%H:%M:%S')
        insert_body = {
            'doc': {'title': title, 'body': body, 'category': category, 'isPublish': isPublish, 'updated': updated}}
        res = es_client.update(index=blog_index, doc_type='doc', id=_id, body=insert_body)
        return json.dumps({"success": True, "data": res['_shards']})
    except Exception as e:
        print(e)
        return json.dumps({"success": False, "data": e.message})


@login_required
def handle_delete_articles():
    try:
        req_data = request.args
        _id = req_data.get('_id', ' ')
        res = es_client.delete(index=blog_index, doc_type='doc', id=_id)
        return json.dumps({"success": True, "data": res['_shards']})
    except Exception as e:
        print(e)
        return json.dumps({"success": False, "data": e.message})


def handle_article():
    if request.method == 'GET':
        return handle_get_articles()
    if request.method == 'POST':
        return handle_post_articles()
    if request.method == 'PUT':
        return handle_put_articles()
    if request.method == 'DELETE':
        return handle_delete_articles()
