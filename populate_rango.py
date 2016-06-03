import os
import json
import tango_with_django_project.settings as settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()

from rango.models import Category, Page


def populate():
    pages = load_pages(settings.POPULATION_FILE_PATH)
    for page in pages:
        add_page(**page)

    # Print out what we have added to the user.
    print_entries()


def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views = views
    p.save()
    return p


def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    return c


def load_pages(json_file_path):
    with open(json_file_path) as data:
        values = json.load(data)
        for value in values:
            value['cat'] = Category.objects.get_or_create(name=value['cat'])[0]
        return values


def print_entries():
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print "- {0} - {1}".format(str(c), str(p))


# Start execution here!
if __name__ == '__main__':
    print "Starting Rango population script..."
    populate()
