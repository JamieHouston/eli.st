from django.template import RequestContext
from django.shortcuts import render_to_response
from item.models import UserCommand, WhatCommand
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

def run_command(request):
    if request.method == 'POST':
        parser_commander = Commander()
        parser_commander.setup()

        command = request.POST['command_text']
        response_data = parser_commander.parse_command(command)
        user_command = UserCommand()
        user_command.original_data = command
        if "action" in response_data and response_data["action"] == "search":
            search_list = response_data["what"]["list"]
            if search_list == "all" or search_list == "all items":
                model_results = UserCommand.objects.all()
            else:
                model_results = UserCommand.objects.filter(what__list=search_list)
            results = [{"pk": user_command.pk, "item": user_command.humanify()} for user_command in model_results]
            if results:
                response_data["results"] = results
            return get_json_response(convert_context_to_json(response_data))
        else:
            user_command.convert_from(response_data)
            user_command.save()

        # TODO: Pull this into stringifier to make view data pretty.  NOT HERE!
        # if "when" in response_data:
        #     if "start_time" in response_data["when"]:
        #         t = response_data["when"]["start_time"]
        #         response_data["when"]["start_time"] = "{0}:{1}".format(str(t.hour).ljust(2,"0"),str(t.minute).ljust(2,"0"))
        #     if "start_date" in response_data["when"]:
        #         d = response_data["when"]["start_date"]
        #         response_data["when"]["start_date"] = d.strftime("%A %d %B %Y")
        #return get_json_response(convert_context_to_json(response_data))
            return get_json_response(convert_context_to_json({"command": user_command.humanify()}))

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
