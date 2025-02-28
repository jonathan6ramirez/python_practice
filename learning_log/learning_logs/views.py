from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Entry
from .forms import TopicForm, EntryForm


# Util Functions
def _check_topic_owner(request, topic):
    """Checks to see if the user is the owner of the topic and raises throws a 404 if the user isnt."""

    if topic.owner != request.user:
        raise Http404


# Create your views here.
# Views are the pages that get sent to the browser whenever
# a user 'requests' a certain webpage.
def index(request):
    """The home page for Learning Log."""
    return render(request, "learning_logs/index.html")


@login_required
def topics(request):
    """Show all topics."""
    topics = Topic.objects.filter(owner=request.user).order_by("date_added")
    context = {"topics": topics}

    return render(request, "learning_logs/topics.html", context)


@login_required
def topic(request, topic_id):
    """Show a single topic and all its entries."""
    topic = Topic.objects.get(id=topic_id)

    # Make sure the topic belongs to the current user.
    _check_topic_owner(request, topic)

    entries = topic.entry_set.order_by("-date_added")
    context = {"topic": topic, "entries": entries}

    return render(request, "learning_logs/topic.html", context)


@login_required
def new_topic(request):
    """Add a new topic."""
    if request.method != "POST":
        # No data submitted; create a blank form.
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect("learning_logs:topics")

    # Display a blank or invalid form.
    context = {"form": form}
    return render(request, "learning_logs/new_topic.html", context)


def new_entry(request, topic_id):
    """Add a new entry."""
    topic = Topic.objects.get(id=topic_id)

    # Check that the user owns the topic.
    _check_topic_owner(request, topic)

    if request.method != "POST":
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect("learning_logs:topic", topic_id=topic_id)

    # Display a blank or invalid form.
    context = {"topic": topic, "form": form}
    return render(request, "learning_logs/new_entry.html", context)


def edit_entry(request, entry_id):
    """Edit and existing entry."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    # Check that the current user is the owner
    _check_topic_owner(request, topic)

    if request.method != "POST":
        # Initital request; pre-fill form with the current entry.
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("learning_logs:topic", topic_id=topic.id)

    context = {"entry": entry, "topic": topic, "form": form}
    return render(request, "learning_logs/edit_entry.html", context)
