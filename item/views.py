from django.template import RequestContext
from django.shortcuts import render_to_response
from item.models import Item
from django.http import HttpResponse
from django.utils import simplejson
from django.core import serializers
from eav.models import Attribute


def inbox(request):
    if request.user.is_authenticated():
        return render_to_response('item/item_list.html', {},
             context_instance=RequestContext(request))
    else:
        return render_to_response('account/authentication.html', {},
            RequestContext(request))


def add_item(request):
    if request.method == 'POST':
        item = Item(name=request.POST["new_item"], created_by=request.user, details=request.POST["item_details"])
        item.save()
    result = {"name": item.name, "pk": item.pk}
    return HttpResponse(simplejson.dumps(result))


def add_attribute(request):
    if request.method == 'POST':
        # TODO: Pass in datatype
        Attribute.objects.get_or_create(name=request.POST["name"], datatype=Attribute.TYPE_TEXT)


def get_items(request):
    items = Item.objects.filter(created_by=request.user)
    results = serializers.serialize('json', items, fields=('name'))
    return HttpResponse(results)
