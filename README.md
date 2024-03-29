# Study Bud

    Study Bud is a platform like discord you can create rooms and talk about something you want to learn about.

## Table Of Content

- [Requirements.](#requiremnts)
- [What I Learned.](#-what-i-learned)
- [OverAll Growth](#-overall-growth)

## Requiremnts

- **_Python_** should be **installed** if not check the **_docs_**
- **pip install virtualenv**
- **virtualenv env**
- **env\scripts\activate**
- **env\scripts\deactivate**
- **pip install django**
- **django-admin startproject "your project name"**
- cd to the project folder and execute **python manage.py runserver 9000** this will run the server on **port 9000** default is **8000**
- python manage.py makemigration
- python manage.py migrate
- pyhton manage.py createsuperuser

## 📚 What I Learned

- _MVT_
- _Database & Admin Panel_
- _CRUD Operations_
- _Search Bar_
- _Flash Messages_
- _Login, Register Form_
- _Chat Room Messages CRUD_
- _How to store a page in sessions:_

```py
@login_required(login_url="login")
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponseRedirect("You are not allowed here!")

    `if request.method == "POST":
        referer = request.session.get("referer", "/")
        message.delete()
        return HttpResponseRedirect(referer)`

    # If the user want to delete a message we store the page where he came from
    # then we delete a message and we redirect him to the prev page
    # Store the referer URL in session
    `request.session["referer"] = request.META.get("HTTP_REFERER")`

    context = {"obj": message}
    return render(request, "base/delete.html", context)
```

- _Add static files and let django know about them_

## 📈 Overall Growth:

Each part of this project helped understand more about Django.
