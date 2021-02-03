import argparse
import json
import re
import requests


def parsing(scoreboard_data, team_rankings_data):
    response = []
    for k in scoreboard_data["results"].keys():
        if not scoreboard_data["results"][k]:
            pass
        else:
            for k1 in scoreboard_data["results"][k]["data"].keys():
                d1 = scoreboard_data["results"][k]["data"]
                d2 = team_rankings_data["results"]["data"]
                res_dict = {}
                res_dict["event_id"] = d1[k1]["event_id"]
                res_dict["event_data"] = d1[k1]["event_date"].split()[0]
                res_dict["event_time"] = d1[k1]["event_date"].split()[1]
                res_dict["away_team_id"] = d1[k1]["away_team_id"]
                res_dict["away_nick_name"] = d1[k1]["away_nick_name"]
                res_dict["away_city"] = d1[k1]["away_city"]
                for index in range(len(d2)):
                    for _ in d2[index].keys():
                        if d2[index]["team_id"] == d1[k1]["away_team_id"]:
                            res_dict["away_rank"] = d2[index]["rank"]
                            res_dict["away_rank_points"] = str(
                                round(float(d2[index]["adjusted_points"]), 2)
                            )
                res_dict["home_team_id"] = d1[k1]["home_team_id"]
                res_dict["home_nick_name"] = d1[k1]["home_nick_name"]
                res_dict["home_city"] = d1[k1]["home_city"]
                for index in range(len(d2)):
                    for _ in d2[index].keys():
                        if d2[index]["team_id"] == d1[k1]["home_team_id"]:
                            res_dict["home_rank"] = d2[index]["rank"]
                            res_dict["home_rank_points"] = str(
                                round(float(d2[index]["adjusted_points"]), 2)
                            )

                response.append(res_dict)

    return json.dumps(response)


parser = argparse.ArgumentParser()
parser.add_argument("start_date", help="Start date format YYYY-MM-DD")
parser.add_argument("end_date", help="End date format YYYY-MM-DD")
args = parser.parse_args()
date_format = "([12]\\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\\d|3[01]))"


if (
    re.match(date_format, args.start_date) is None
    or re.match(date_format, args.end_date) is None
):
    print("Please check the date format (YYYY-MM-DD)")
elif int(args.end_date.split("-")[-1]) - int(args.start_date.split("-")[-1]) < 0:
    print("End_date must be greater than start_date")
elif int(args.end_date.split("-")[-1]) - int(args.start_date.split("-")[-1]) > 7:
    print(
        "Date range must a maximum of 7 days for sports other than MMA, Boxing and AutoRacing \
and a maximum of 1 month for MMA, Boxing and AutoRacing"
    )
else:
    team_rankings = requests.request(
        "get",
        "https://delivery.chalk247.com/team_rankings/NFL.json?api_key=74db8efa2a6db279393b433d97c2bc843f8e32b0",
    )

    scoreboard = requests.request(
        "get",
        "https://delivery.chalk247.com/scoreboard/NFL/"
        + args.start_date
        + "/"
        + args.end_date
        + ".json?api_key=74db8efa2a6db279393b433d97c2bc843f8e32b0",
    )

    team_rankings_data = json.loads(team_rankings.text)
    scoreboard_data = json.loads(scoreboard.text)
    print(parsing(scoreboard_data, team_rankings_data))
