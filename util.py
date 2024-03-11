import os
import json


def merge_data(current_data, before_data):
    '''
    データをマージする
    param:current_data 現在のデータ
    param:before_data 過去のデータ
    '''
    tmp_obj = {}
    if current_data and before_data:
        concat_data = before_data + current_data
        for data in concat_data:
            tmp_obj[data.get('href')] = data.copy()
        merge_datas = [tmp_obj.get(title) for title in tmp_obj]
        return merge_datas
    elif current_data:
        return current_data
    else:
        return before_data


def sort_articles(articles, sort_name1, sort_name2):
    '''
    ソートする
    '''
    return sorted(articles, key=lambda x: (x[sort_name1], x[sort_name2]), reverse=True)


def make_path(path):
    '''
    パスを作成する
    '''
    paths = path.split('/')
    if len(paths) > 1 and not os.path.exists('/'.join(paths[:-1])):
        os.makedirs('/'.join(paths[:-1]))
    return path


def write_json_file(data, path):
    '''
    jsonファイル作成
    '''
    jsonstr = json.dumps(data, ensure_ascii=False)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(jsonstr)
