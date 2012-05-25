from datetime import date, timedelta


def CommonParsers():

    today = date.today()
    friday = today - timedelta(days=today.weekday()) + timedelta(days=4)
    return {
        "AddToList":
        [
            {
                "command": "Add brocoli to grocery",
                "result":
                    {"action":"add", "what": {"item": "brocoli", "list": "grocery"}}},
            {
                "command": "add brocoli to the grocery list",
                "result":
                    {"action":"add", "what": {"item": "brocoli", "list": "grocery"}}}
        ],
        "NaturalDate":
        [
            {
                "command": "Visit grandma on friday",
                "result": {
                    "action": "add",
                    "when":
                        {"start_date": friday}
                },
                "result_command": "visit grandma"
            }
        ],
        "RecurrenceFinder":
        [
            {
                "command": "Plan dinners every other Friday",
                "result": {
                    "action": "add",
                    "when":
                        {"recurrence":
                            {"frequency": "2",
                            "day": "friday"}
                        }
                }

            }
        ]
    }
