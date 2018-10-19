import requests
from bs4 import BeautifulSoup

# Create your views here.
from rest_framework import permissions
from rest_framework.views import APIView


class URLs(APIView):

    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        response = requests.get(request.url)
        soup = BeautifulSoup(response.text, 'html')
        urls = [url.get('href') for url in soup.find_all('a') if url.get('href')]
        urls = [url for url in urls if url.startswith('http')]
