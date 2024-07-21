import requests
import json

class Download:
    def __init__(self, yturl: str):
        """
        Inisialisasi objek Download dengan URL video YouTube.

        :param yturl: URL dari video YouTube.
        """
        self.video_id = yturl.split('/')[-1]
        error_templates = {
            'title': None, 'id': self.video_id, 'size': None,
            'duration': None, 'channelTitle': None, 'source': 'Undefined'
        }

        try: 
            response = requests.get(f'https://ssi.mp3juice.blog/search.php?q={self.video_id}')
            response.raise_for_status()
            self.video_data = response.json()['items'][0]

            if self.video_data['id'] != self.video_id:
                self.video_data = error_templates
        except (IndexError, requests.RequestException):
            self.video_data = error_templates

        self.video_data['data'] = dict()

    def mp3(self, token: str='Bad Request') -> dict:
        """
        Mengonversi video YouTube ke format MP3.

        :param token: Token untuk konversi.
        :return: Data video dengan URL MP3.
        """
        data = {
            'id': self.video_id,
            'token': token,
            'ref': 'https://ssi.mp3juice.blog/',
            'title': self.video_data.get('title', 'Unknown Title')
        }

        while True:
            try:
                response = requests.post('https://api.canehill.info/convert', data=data)
                response.raise_for_status()
                cv = response.json()

                if cv['status'] == 'ok':
                    self.video_data['data']['url'] = cv['link']
                    break
                elif cv['status'] == 'fail':
                    self.video_data['data']['url'] = None
                    break
                elif cv['status'] == 'processing':
                    continue
                else:
                    self.video_data['data']['url'] = None
                    break
            except requests.RequestException:
                self.video_data['data']['url'] = None
                break

        self.video_data['data']['type'] = 'mp3'
        return self.video_data

    def mp4(self) -> dict:
        """
        Mengonversi video YouTube ke format MP4.

        :return: Data video dengan URL MP4.
        """
        try:
            response = requests.get(f'https://aa.sounddownmp3.com/download-ytjarmp4.php?id={self.video_id}')
            response.raise_for_status()
            api = response.json()

            if api.get('success'):
                self.video_data['data']['url'] = api['link']
            else:
                self.video_data['data']['url'] = None
        except (requests.exceptions.JSONDecodeError, requests.RequestException):
            self.video_data['data']['url'] = None
    
        self.video_data['data']['type'] = 'mp4'
        return self.video_data


def search(query: str) -> dict:
    """
    Mencari video berdasarkan query.

    :param query: Kata kunci pencarian.
    :return: Hasil pencarian dalam bentuk JSON.
    """
    try:
        response = requests.get(f'https://ssi.mp3juice.blog/search.php?q={query}')
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return {}
