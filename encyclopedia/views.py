import random
from django.shortcuts import render, redirect

from . import util
from markdown import markdown

def index(request):
    data = {}

    if request.session.get('error', None) != None:
        data.update(request.session.get('error'))
        del request.session['error']

    data.update({"entries": util.list_entries()})
    return render(request, "encyclopedia/index.html", data)

def wikiPage(request, title):
    entry = util.get_entry(title)

    if entry == None:
        data = {
            "title": title,
            "danger_alert": "Your requested Wiki page does not exist."
        }
    else:
        data = {
            "title": title,
            "entry": markdown(entry)
        }

    return render(request, "encyclopedia/showPage.html", data)

def search(request):

    if request.method == "POST":
        userInput = request.POST.get("userInput","")
        titles = util.list_entries()

        if userInput == "":
            redirect("index")
        elif userInput in titles:
            return redirect("wikiPage", title=userInput)
        else:
            relevant_titles = [title for title in titles if userInput.lower() in title.lower()]

            data = {
                "userInput": userInput,
                "titles": relevant_titles
            }
            return render(request, "encyclopedia/search.html", data)

def createPage(request):
    if request.method == "GET":
        return render(request, "encyclopedia/createPage.html")
    else:
        title = request.POST.get("title", "")
        userInput = request.POST.get("userInput", "")

        if userInput == "" or title == "":
            return render(request, "encyclopedia/createPage.html", {
                "danger_alert": "Both title and content cannot be empty."
            })
        elif title in util.list_entries():
            return render(request, "encyclopedia/createPage.html", {
                "danger_alert": "Your title is already taken."
            })
        else: ## Svae file to disk and redirect to new page
            with open("entries/"+title+".md", "w") as output_file:
                output_file.write(userInput)

            return redirect("wikiPage", title=title)

def editPage(request, title):
    if request.method == "GET":
        if title in util.list_entries():
            entry = util.get_entry(title)

            data = {
                "title": title,
                "entry": entry
            }
            return render(request, "encyclopedia/editPage.html", data)
        else:
            return redirect("createPage")
    else:
        userInput = request.POST.get("userInput", "")

        with open("entries/"+title+".md", "w") as output_file:
            output_file.write(userInput)

        return redirect("wikiPage", title=title)

def randomPage(request):
    title = random.choice(util.list_entries())

    return redirect("wikiPage", title=title)
