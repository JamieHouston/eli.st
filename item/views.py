from django.template import RequestContext
from django.shortcuts import render_to_response
from item.models import Item
#import pdb


def inbox(request):
    if request.user.is_authenticated():
        #pdb.set_trace()
        items = Item.objects.filter(created_by=request.user)
        return render_to_response('item/item_list.html', {'items': items},
            RequestContext(request))
    else:
        return render_to_response('account/authentication.html', {},
            RequestContext(request))
