from django.shortcuts import render
from markdown2 import markdown
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from . import util
import difflib
import random


#Index function
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
# entry function, allow user to type entry title and redirected to the entry page
def entry_page(request, title):
    try:
        # get .md file
        md_content = util.get_entry(title)
        # convert .md to html
        html = markdown(md_content)
        return render(request, "encyclopedia/entry.html", {
            "title":title, "html":html
        })
    except TypeError:
        return render(request, "encyclopedia/error.html", {
            "error": "Sorry, entry does not exist!"
        })

# this function allow user to search for the title of the page and redirected to the page. It gets user's input from the form via post.
def search(request):
    # Check request method is post
    if request.method == "POST":
        # get user input
        us_input = request.POST.get("q")
        print(us_input)
        # get list of entries. This return a list of file names
        entries = util.list_entries()
        print(entries)
        for entry in entries:
            if entry.lower() != us_input.lower():
                continue
            elif entry.lower() == us_input.lower():
                print(f"condition is try {entry}")
                return HttpResponseRedirect(reverse("encyclopedia:entry_page", args=[us_input]))
        # create a new list with it's content in lowercase      
        entries = [entry.lower() for entry in entries]
        # find the closes match from the user input
        
        matches = difflib.get_close_matches(us_input.lower(), entries, cutoff=0.02)
        if not matches:
            return render(request, "encyclopedia/error.html", {
                "error": "Sorry, no entry matches your search"
            })
        
        
        print(f"these are matches:{matches} and this is input: {us_input}")
        return render(request, "encyclopedia/index.html", {
            "entries": matches
        })
    # if method is get just render an index page      
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
        })

# create page function
def create_page(request):
    # check request method is post
    if request.method == "POST":
        # retrieve user's input
        title = request.POST.get("title")
        content = request.POST.get("content")
        entries = util.list_entries()
        # turn all markdown file names into lower case
        entries = [entry.lower() for entry in entries]
        print(f"this is title:{title}, this is content:{content}")
        if title.lower() in entries:
            return render(request, "encyclopedia/error.html", {
                "error": "Sorry, there is another entry with similar title"
            })
        # save entry
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("encyclopedia:entry_page", args=[title]))
    return render(request, "encyclopedia/create_page.html")

# edit page function
def edit_page(request,title):
    # for POST method
    if request.method == "POST":
        content_new = request.POST.get("content")
        util.save_entry(title,content_new)
        return HttpResponseRedirect(reverse("encyclopedia:entry_page", args=[title]))
    
    # for GET method, get url
    title_path = request.get_full_path()
    # debug with print
    print(f"This is my path:{title_path}")
    # get content of the md file
    content = util.get_entry(title)
    # render a text area with contents of the md file
    return render(request, "encyclopedia/edit.html", {
        "content_md": content, "title": title
    })

# random page functionality
def random_page(request):
    entries = util.list_entries()
    entry = random.choice(entries)
    print(entry)
    return HttpResponseRedirect(reverse("encyclopedia:entry_page", args=[entry]))