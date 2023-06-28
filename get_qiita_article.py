import requests
import pandas as pd
from datetime import datetime as dt


def get_qiita_articles_by_page(page):
    """
    第何ページ目の文章を取得
    @param page ページ目
    @return 文章リストを返す
    """
    url = 'https://qiita.com/api/v2/items'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
    }
    params = {
        'page': page,
        'per_page': 100,
        'query': 'likes_count:=0'
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        article = response.json()
        return article
    return None


def get_qiita_articles():
    """
    qiitaの文章を取得

    """
    articles = []
    for i in range(1, 1001):
        top = get_qiita_articles_by_page(i)
        if top:
            articles.extend(top)
    return articles


def out_put_articels(file_name):
    """
    qiitaの文章を出力
    """
    articles = get_qiita_articles()
    # for index, article in enumerate(articles, start=1):
    #     print(f'{index}. {article.get("title")} - {article.get("likes_count")} likes')
    if articles:
        df = pd.DataFrame(articles)
        df.to_csv(file_name, encoding='utf-8')
    else:
        print("文章を取得できなかった！")


if __name__ == '__main__':
    day = dt.now().strftime('%Y%m%d')
    out_put_articels(f'./result_{day}.csv')
