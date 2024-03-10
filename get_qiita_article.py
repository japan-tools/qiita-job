import os
import requests
import pandas as pd
from datetime import datetime as dt

URL = 'https://qiita.com/api/v2'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
    'Authorization' : os.environ['AUTHORIZATION']
}

def get_qiita_articles_by_page(page):
    '''
    第何ページ目の文章を取得
    @param page ページ目
    @return 文章リストを返す
    '''

    params = {
        'page': page,
        'per_page': 100,
        'query': 'likes_count:>0'
    }
    response = requests.get(f'{URL}/items', headers=HEADERS, params=params)
    if response.status_code == 200:
        article = response.json()
        return article
    return None


def get_qiita_articles():
    '''
    qiitaの文章を取得

    '''
    articles = []
    for i in range(1, 9999):
        article = get_qiita_articles_by_page(i)
        if article:
            articles.extend(article)
        else:
            break
    return articles


def out_put_articels(articles, file_name):
    '''
    qiitaの文章を出力
    '''
    if articles:
        df = pd.DataFrame(articles)
        df.drop(columns=['id', 'rendered_body', 'body', 'coediting', 'group', 'private', 'reactions_count',
                         'stocks_count', 'tags', 'updated_at', 'team_membership', 'organization_url_name', 'page_views_count'], axis=1, inplace=True)
        df.sort_values(by='likes_count', axis=0, ascending=False, inplace=True)
        df = df[df['likes_count'] > 0]
        df = df.reindex(columns=['title', 'url', 'likes_count', 'comments_count', 'tags' , 'created_at', 'user'])
        df.to_csv(file_name, encoding='utf-8', index=False)
    else:
        print('文章を取得できなかった！')


if __name__ == '__main__':
    date = dt.now().strftime('%Y%m%d')
    articles = get_qiita_articles()
    out_put_articels(articles, f'./archive/total_result.csv')
