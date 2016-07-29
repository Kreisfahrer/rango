import os
import json
import tango_with_django_project.settings as settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()

from rango.models import Category, Page


def populate():
    items = load_pages(settings.POPULATION_FILE_PATH)
    for item in items:
        current_category = add_cat(name=item['cat'], views=item['views'], likes=item['likes'])
        for page in item['pages']:
            add_page(cat = current_category, **page)

    # Print out what we have added to the user.
    print_entries()


def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views = views
    p.save()
    return p


def add_cat(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name, views=views, likes=likes)[0]
    return c


def load_pages(json_file_path):
    with open(json_file_path) as data:
        values = json.load(data)
        return values


def print_entries():
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print "- {0} - {1}".format(str(c), str(p))


# Start execution here!
if __name__ == '__main__':
    print "Starting Rango population script..."
    populate()
