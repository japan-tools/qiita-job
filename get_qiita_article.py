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
    for i in range(1, 9999):
        top = get_qiita_articles_by_page(i)
        if top:
            articles.extend(top)
        else:
            break
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
        df.drop(columns=["id", "rendered_body", "body", "coediting", "comments_count", "created_at", "group", "private", "reactions_count",
                         "stocks_count", "tags", "updated_at", "team_membership", "organization_url_name", "user", "page_views_count"], axis=1, inplace=True)
        df.sort_values(by="likes_count", axis=0, ascending=False, inplace=True)
        df = df[df["likes_count"] > 0]
        df = df.reindex(columns=['title', 'url', 'likes_count'])
        df.to_csv(file_name, encoding='utf-8', index=False)
    else:
        print("文章を取得できなかった！")


if __name__ == '__main__':
    day = dt.now().strftime('%Y%m%d')
    out_put_articels(f'./result_{day}.csv')
