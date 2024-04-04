from django.views import generic
from django.shortcuts import render
from core.settings import API_KEY, API_READ_ACCESS_TOKEN, BASE_URL
import requests


class FetchMoviesView(generic.TemplateView):
    template_name = "movies/movie_list.html"
    context_object_name = "response"

    def get(self, request, *args, **kwargs):

        headers = {
            "Authorization": f"Bearer {API_READ_ACCESS_TOKEN}",
            "accept": "application/json"
        }

        auth_url = f"{BASE_URL}authentication"
        response = requests.get(url=auth_url, headers=headers)
        context = {"response": response.text}
        return render(request, self.template_name, context)
