from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View
from datetime import datetime
import json


# Create your views here.
class ComingSoon(View):
    def get(self, request, *args, **kwargs):
        return redirect('/news/')


class NewsFromJSON(View):
    def get(self, request, news_id, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH) as f:
            json_file = json.load(f)
            for i in json_file:
                for key, value in i.items():
                    if i["link"] == news_id:
                        context = i
        return render(request, 'news/news.html', context=context)


class MainMenu(View):
    def get(self, request, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH, encoding="utf-8") as f:
            json_file = json.load(f)
        news_dict = sorted(json_file, key=lambda x: x["created"], reverse=True)
        for i in news_dict:
            i["created"] = i["created"][:10]
        if "q" in request.GET:
            q = request.GET["q"]
            news_dict = [i for i in news_dict if q in i["title"]]
        return render(request, 'news/menu.html', context={"data": news_dict})


class CreateNews(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'news/create.html', context={})

    def post(self, request, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH, encoding="utf-8") as f:
            json_file = json.load(f)
        news_id = 1
        numbers = set([n["link"] for n in json_file])
        while news_id in numbers:
            news_id += 1
        news_to_add = {
            "created": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "text": request.POST["text"],
            "title": request.POST["title"],
            "link": news_id
        }
        json_file.append(news_to_add)
        with open(settings.NEWS_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(json_file, f)
        return redirect("/news/")
