def NlpParsers():
    return {"ManualParser": [{"command": "Massage with xyz on January 1st, 2013 at 4PM", "result": {"action":"add", "what": {"item": "massage"}, "who": {"person": "xyz"}, "when": {"start_date": "2013-1-1", "start_time": "1600"}}}]}
