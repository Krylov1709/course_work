from pprint import pprint
from urllib import response
import requests
import datetime
import json
from tqdm import tqdm

class VK:

    def __init__(self, token, user_id, version='5.131'):
        self.token = token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def users_info(self):
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.id}
        response = requests.get(url, params={**self.params, **params})
        return response.json()
   
    def photos_info(self):
        '''Вызываем список фотографий в профиле и сохраняем в список максимальный размер, количество лайков и дату фотографии'''
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.id, 
                  'album_id': 'profile',
                  'extended': 1}
        response = requests.get(url, params={**self.params, **params}).json()
        photo_dict = {}
        photos_list = []
        for photo in tqdm(response['response']['items']):
            photo_dict =  {'likes': photo['likes']['count'], 
                           'url': photo['sizes'][-1]['url'], 
                           'date': datetime.datetime.fromtimestamp(photo['date']),
                           'size': photo['sizes'][-1]['type']}
            photos_list.append(photo_dict)
        return photos_list
   
class Yandex:
    
    def __init__(self, token: str):
        self.token = token
        self.headers = {'Content-Type': 'application/json', 
                        'Authorization': f'OAuth {self.token}'}
        
    def create_folder(self, path):
        '''Создаем папку на яндекс диске'''
        url = f'https://cloud-api.yandex.net/v1/disk/resources?path={path}'
        return requests.put(url, headers=self.headers)
         
    def load_file(self, path):
        '''Записываем файл в указанную папку на яндекс диске и создаем файл с информацией о сохраненных файлах'''
        self.create_folder(path)
        size = []
        file_name = []
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        for photo in tqdm(vk.photos_info()):
            url_photo = photo['url']
            size.append(photo['size'])
            if f'{photo["likes"]}.jpg' in file_name:
                file_name_photo = photo['date'].strftime(f'{photo["likes"]}_%Y_%m_%d_%H_%M_%S.jpg')
                file_name.append(file_name_photo)
            else:
                file_name_photo = f'{photo["likes"]}.jpg'
                file_name.append(file_name_photo)          
            params = {'path': f'{path}/{file_name_photo}',
                      'url': url_photo}
            response = requests.post(url, params=params, headers=self.headers)
        copy_result = [dict(file_name = file_name, size = size) for file_name, size in zip(file_name, size)]
        return copy_result
    
def copy_result(copy_result):
    file = json.dumps(list(copy_result))
    file = json.loads(str(file))
    with open("copy_result.json", "w", encoding = 'utf-8') as write_file:
        json.dump(file, write_file, indent = 0)
        print('Запись выполнена')

ya_access_token = ''
vk_access_token = ''
user_id = input('Введите ID пользователя: ')
vk = VK(vk_access_token, user_id)
ya = Yandex(ya_access_token)
name_album_yandex = input('Введите названия альбома на Яндекс Диске: ')
# pprint(vk.users_info())
# pprint(vk.photos_info())
# ya.load_file("Мой альбом")
copy_result(ya.load_file(name_album_yandex))

