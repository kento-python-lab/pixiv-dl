from pixivpy3 import *
from time import sleep
import os
import setting


# Pixiv API へログイン
api = PixivAPI()
api.login(setting.pixiv_id, setting.client_password)
aapi = AppPixivAPI()

# 絵師のページIDを入力する
id_search = int(input('取得したい絵師のページIDを入力してください。>>>'))

# 最大画像取得数
works = 300

illustrator_id = api.users_works(id_search, per_page=works)
total_works = illustrator_id.pagination.total

# 最大取得数が絵師の公開する画像の枚数以上の場合
# 最大画像取得数を合計枚数にセット
if works < total_works:
    total_works = works

illust = illustrator_id.response[0]

# タグの指定
target_tag = [str(input('取得タグを指定してください。>>>'))]

# 保存先パスの生成
saving_direcory_path = './Downloads/' + illust.user.name + '/'
if not os.path.exists(saving_direcory_path):
    os.mkdir(saving_direcory_path)
separator = '------------------------------------------------------------'

print('Illustrator: {}'.format(illust.user.name))
print('Works number: {}'.format(total_works))
print(separator)

# ダウンロードスタート


for work_no in range(0, total_works):
    try:
        illust = illustrator_id.response[work_no]

        if len(list(set(target_tag) & set(illust.tags))) == 0 and target_tag != []:
            continue

        print('Now: {0}/{1}'.format(work_no + 1, total_works))
        print('Title: {}'.format(illust.title))

        if os.path.exists(saving_direcory_path+str(illust.id)+'_p0.png') or os.path.exists(saving_direcory_path + str(illust.id) + '_p0.jpg'):
            # すでにダウンロード済みの場合スキップ
            print('Title:'+str(illust.title)+' has already downloaded.')
            print(separator)
            sleep(1)
            continue

        if illust.is_manga:
            work_info = api.works(illust.id)
            for page_no in range(0, work_info.response[0].page_count):
                page_info = work_info.response[0].metadata.pages[page_no]
                aapi.download(page_info.image_urls.large, saving_direcory_path)
                sleep(3)

        else:
            aapi.download(illust.image_urls.large, saving_direcory_path)
            sleep(3)

    except Exception:
        continue

    print(separator)

print('Download complete!　Thanks to {}!!'.format(illust.user.name))
