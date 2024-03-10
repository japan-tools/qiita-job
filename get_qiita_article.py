import os
import util
import requests
from datetime import datetime as dt

URL = 'https://qiita.com/'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
    'Authorization': os.environ.get('AUTHORIZATION')
}


print(os.environ.get('AUTHORIZATION'))

def get_qiita_articles_by_page(page):
    '''
    第何ページ目の文章を取得
    @param page ページ目
    @return 文章リストを返す
    '''

    params = {
        'page': page,
        'per_page': 100,
        'query': 'stocks:>0'
    }
    response = requests.get(f'{URL}api/v2/items',
                            headers=HEADERS, params=params)
    if response.status_code == 200:
        article = response.json()
        return article
    return None


def get_qiita_articles():
    '''
    qiitaの文章を取得

    '''
    articles = []
    for i in range(1, 2):
        article = get_qiita_articles_by_page(i)
        if article:
            articles.extend(article)
        else:
            break
    return articles


def out_put_articels(datas, file_name):
    '''
    qiitaの文章を出力
    '''
    if datas:
        articles = [{
            'title': article.get('title'),
            'url': article.get('url'),
            'likes_count': article.get('likes_count'),
            'stocks_count': article.get('stocks_count'),
            'tags': ','.join([tag.get('name') for tag in article.get('tags')]),
            'created_at': article.get('created_at'),
            'user_id': article.get('user').get('id'),
            'user_name': article.get('user').get('name'),
            'user_url': f'{URL}{article.get("user").get("id")}'} for article in datas]
        util.sort_articles(articles, 'stocks_count')
        file_name = util.make_path(file_name)
        util.write_json_file(articles, file_name)
    else:
        print('文章を取得できなかった！')


def start():
    articles = get_qiita_articles()
    out_put_articels(articles, 'archive/total_result.json')
    out_put_articels(articles, 'total_result.json')


if __name__ == '__main__':
    start()
