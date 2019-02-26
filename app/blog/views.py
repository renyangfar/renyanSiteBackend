from app.blog.public import handle_public_articles
from app.blog.user import handle_user_articles, handle_articles_category, handle_article
from . import blog


@blog.route('/public/articles_list')
def public_articles():
    return handle_public_articles()


@blog.route('/user/articles_list')
def user_articles():
    return handle_user_articles()


@blog.route('/user/articles/category')
def articles_category():
    return handle_articles_category()


@blog.route('/user/article', methods=['GET', 'POST', 'DELETE', 'PUT'])
def articles_detail():
        return handle_article()



