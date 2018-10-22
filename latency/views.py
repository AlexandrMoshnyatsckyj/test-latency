from multiprocessing import Pool

import redis
import requests
from bs4 import BeautifulSoup

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class URLs(APIView):

    def post(self, request):
        response = requests.get(request.data['url'])
        soup = BeautifulSoup(response.text, 'html')
        urls = [url.get('href') for url in soup.find_all('a') if url.get('href')]
        urls = [url.split('?')[0] for url in urls if url.startswith('http')]

        infos = []
        conn = redis.StrictRedis(host='localhost', port=6379, db=0)

        def get_all_latency(url):
            infos.append(get_latency(url))

        def get_latency(url):
            try:
                info = conn.lrange(url, 0, -1)
            except:
                result = requests.get(url)
                info = {url: {result.status_code, result.elapsed.microseconds // 1000}}
                conn.lpush(info)
            return info

        with Pool(4) as pool:
            pool.map(get_all_latency, urls)
            pool.close()
            pool.join()

        return Response({'status': status.HTTP_200_OK, 'data': infos})
