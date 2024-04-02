from urllib.request import Request

from django.shortcuts import render
from django.views import View

from events.partials import svd
from users import models as user_models
from events import models as event_models


class BaseView(View):
    def get(self, request: Request):
        avatar = None
        try:
            user = user_models.User.objects.get(id=request.user.pk)
            avatar = user.avatar.url
        except Exception as e:
            pass
        rec = svd.SvdRec(request.user.pk)
        events_main = event_models.Event.objects.all()[:8]
        context = {
            "user_avatar": avatar,
            "events": events_main,
            "users_count": user_models.User.objects.count(),
            "events_count": event_models.Event.objects.count(),
            "rating_events": rec.get_recommendation_qs(),
        }
        return render(request, "main.html", context=context)
