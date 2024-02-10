from django.shortcuts import render
from base.constants.constants import rooms


# Create your views here.
def home(request):
    return render(request, "base/home.html", {"rooms": rooms})


def room(request, pk):
    room = None
    for i in rooms:
        if i["id"] == int(pk):
            room = i
    context = {"room": room}
    return render(request, "base/room.html", context)
