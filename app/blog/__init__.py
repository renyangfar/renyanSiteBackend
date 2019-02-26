from flask import Blueprint

from modules.elasticSearch import get_es_client

blog = Blueprint('blog', __name__)
es_client = get_es_client()

from . import views