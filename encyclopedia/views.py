from django.shortcuts import render
from markdown2 import markdown
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from . import util
import difflib
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
        return render(request, "encyclopedia/error.html")

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
        matches = difflib.get_close_matches(us_input.lower(), entries, cutoff=0.02)
        print(f"these are matches:{matches} and this is input: {us_input}")
        return render(request, "encyclopedia/index.html", {
            "entries": matches
        })
            
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
        })
