import os
import util
import json
import requests
from datetime import datetime as dt

URL = 'https://qiita.com/api/v2/items'

HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {os.environ.get("QIITA_AUTH")}'
}


def get_qiita_articles_by_page(page):
    '''
    第何ページ目の文章を取得
    @param page ページ目
    @return 文章リストを返す
    '''

    params = {
        'page': page,
        'per_page': 100
    }
    response = requests.get(URL, headers=HEADERS, params=params)
    if response.status_code == 200:
        articles = response.json()
        articles = [article for article in articles if article.get(
            'likes_count') > 0 or article.get('stocks_count') > 0]
        return articles
    return None


def get_qiita_articles():
    '''
    qiitaの文章を取得
    '''
    articles = []
    for i in range(1, 999):
        article = get_qiita_articles_by_page(i)
        if article:
            articles.extend(article)
        else:
            break
    if articles:
        articles = [{
            'title': article.get('title'),
            'url': article.get('url'),
            'likes_count': article.get('likes_count'),
            'stocks_count': article.get('stocks_count'),
            'tags': ','.join([tag.get('name') for tag in article.get('tags')]),
            'created_at': str(dt.fromisoformat(article.get('created_at'))).replace('+09:00', ''),
            'user_id': article.get('user').get('id'),
            'user_name': article.get('user').get('name'),
            'user_url': f'{URL[-12:]}{article.get("user").get("id")}'} for article in articles]
        # likes_count,stocks_count降順でソートする
        articles = util.sort_articles(articles, 'likes_count', 'stocks_count')
    return articles


def out_put_articels(articles, file_name):
    '''
    qiitaの文章を出力
    '''
    if articles:
        file_name = util.make_path(file_name)
        util.write_json_file(articles, file_name)


def update_post(url, article_id, post_content):
    '''
    記事を更新する
    '''
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {os.environ.get("QIITA_AUTH")}'
    }
    url = f'{url}/{article_id}'
    res = requests.patch(url, headers=headers, json=post_content)
    if res.status_code >= 400:
        res.raise_for_status()
    return res


def start():
    articles = get_qiita_articles()
    out_put_articels(articles, 'archive/total_result.json')
    body = '## はじめ\n ### この記事ではGithubActionとQiita Apiを利用して定期的に自動でQiitaの記事を取得し、いいねとストックで順位を付けて、この記事を更新する。\n ## Github Open ソース \n  https://github.com/japan-tools/qiita-job \n ## いいね数とストック数ランキング記事一覧 \n'
    articles = [article for article in articles if article.get(
        'likes_count') > 50 or article.get('stocks_count') > 50]
    for article in articles:
        article_title = article.get('title')
        article_url = article.get('url')
        article_likes_count = article.get('likes_count')
        article_stocks_count = article.get('stocks_count')
        article_tags = article.get('tags')
        article_created_at = article.get('created_at')
        body += f"## [{article_title}]({article_url}) \n - いいね数: {article_likes_count} \n - ストック数: {article_stocks_count} \n - タグ: {article_tags} \n - 投稿日: {article_created_at} \n"
    post_content = {
        'body': body,
        "coediting": False,
        "private": False,
        "tags": [
            {
                "name": "qiita",
                "versions": []
            },
            {
                "name": "QiitaAPI",
                "versions": []
            },
            {
                "name": "GitHub",
                "versions": []
            },
            {
                "name": "GithubActions",
                "versions": []
            },
            {
                "name": "記事まとめ",
                "versions": []
            }
        ],
        "title": "GithubActionでQiita記事のいいね数とストック数ランキング更新",
        "slide": False
    }
    update_post(URL, 'b22a79d04eae4a401067', post_content)


if __name__ == '__main__':
    start()
