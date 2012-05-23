from django.template import RequestContext
from django.shortcuts import render_to_response
from item.models import UserCommand
from django.http import HttpResponse
from django.utils import simplejson
from django.core import serializers
#from utils.nlp import Parser
from commander.CommandParser import Commander
import json
import pdb


def get_friendly_message(item):
    response = [item.name]
    for item_attribute in item.get_attributes():
        response.push(item_attribute)
    return response.join(' ')


def inbox(request):
    if request.user.is_authenticated():
        return render_to_response('item/item_list.html', {},
             context_instance=RequestContext(request))
    else:
        return render_to_response('account/authentication.html', {},
            RequestContext(request))


# def add_item(request):
#     if request.method == 'POST':
#         parser = Parser()
#         chunks = parser.get_natural_command(text_input)
#         item.name, item.value = chunks
#         item = Item(name=request.POST["new_item"], created_by=request.user, details=request.POST["item_details"])

#         item.save()

#         attribute_name = request.POST["item_attribute"]
#         attribute_value = request.POST["attribute_value"]

#         item.add_attribute(attribute_name, attribute_value)

#         result = {"name": item.name, "pk": item.pk, "alert": "Added " + get_friendly_message(item)}
#         return HttpResponse(simplejson.dumps(result))


# def add_attribute(request):
#     if request.method == 'POST':
#         attribute_type = request.POST["attribute_type"]
#         name = request.POST["new_attribute"]

#         attribute, created = Attribute.objects.get_or_create(name=name, datatype=attribute_type)

#         result = {"name": attribute.name, "pk": attribute.pk}
#         return HttpResponse(simplejson.dumps(result))


# def get_items(request):
#     items = Item.objects.filter(created_by=request.user)
#     results = serializers.serialize('json', items, fields=('name', 'pk'))
#     return HttpResponse(results)


# def get_attributes(request):
#     items = Attribute.objects.all()
#     results = serializers.serialize('json', items, fields=('name', 'pk'))
#     return HttpResponse(results)


# def get_item(request, item_pk):
#     item = Item.objects.get(pk=item_pk)
#     items = item.itemattribute_set.all()
#     results = serializers.serialize('json', items)
#     return HttpResponse(results)


def run_command(request):
    if request.method == 'POST':
        parser_commander = Commander()
        parser_commander.setup()

        command = request.POST['command_text']
        #pdb.set_trace()
        response_data = parser_commander.parse_command(command)
        user_command = UserCommand()
        #user_command.user = request.user
        user_command.original_data = command
        #pdb.set_trace()
        if "action" in response_data and response_data["action"] == "search":
            model_results = WhatCommand.objects.filter(list=response_data["what"]["list"])
            results = [{"pk": what_command.pk, "item": what_command.item} for what_command in model_results]
            if results:
                response_data["results"] = results
        user_command.convert_from(response_data)
        user_command.save()

        # TODO: Pull this into stringifier to make view data pretty.  NOT HERE!
        if "when" in response_data:
            if "start_time" in response_data["when"]:
                t = response_data["when"]["start_time"]
                response_data["when"]["start_time"] = "{0}:{1}".format(str(t.hour).ljust(2,"0"),str(t.minute).ljust(2,"0"))
            if "start_date" in response_data["when"]:
                d = response_data["when"]["start_date"]
                response_data["when"]["start_date"] = d.strftime("%A %d %B %Y")
        return get_json_response(convert_context_to_json(response_data))
    else:
        return render_to_response('item/command_parser.html', {},
             context_instance=RequestContext(request))


def get_json_response(content, **httpresponse_kwargs):
    "Construct an `HttpResponse` object."
    return HttpResponse(content,
                             content_type='application/json',
                             **httpresponse_kwargs)


def convert_context_to_json(context):
    "Convert the context dictionary into a JSON object"
    # Note: This is *EXTREMELY* naive; in reality, you'll need
    # to do much more complex handling to ensure that arbitrary
    # objects -- such as Django model instances or querysets
    # -- can be serialized as JSON.
    return json.dumps(context)
