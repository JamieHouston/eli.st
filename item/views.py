from django.template import RequestContext
from django.shortcuts import render_to_response
from item.models import Item
from django.http import HttpResponse
from django.utils import simplejson
#import pdb


def inbox(request):
    if request.user.is_authenticated():
        #pdb.set_trace()
        items = Item.objects.filter(created_by=request.user)
        return render_to_response('item/item_list.html', {'items': items},
             context_instance=RequestContext(request))
    else:
        return render_to_response('account/authentication.html', {},
            RequestContext(request))


def add_item(request, new_item):
    #user = get_or_create_user(user_name)
    #list = get_or_create_list(user, list_name)
    #list.save()
    item = Item(name=new_item, created_by=request.user)
    item.save()
    result = {"name": item.name, "pk": item.pk}
    return HttpResponse(simplejson.dumps(result))
