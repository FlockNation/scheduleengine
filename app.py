from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

nfl_divisions = {
    "AFC East": ["Buffalo Bills", "Miami Dolphins", "New England Patriots", "New York Jets"],
    "AFC North": ["Baltimore Ravens", "Cincinnati Bengals", "Cleveland Browns", "Pittsburgh Steelers"],
    "AFC South": ["Houston Texans", "Indianapolis Colts", "Jacksonville Jaguars", "Tennessee Titans"],
    "AFC West": ["Denver Broncos", "Kansas City Chiefs", "Las Vegas Raiders", "Los Angeles Chargers"],
    "NFC East": ["Dallas Cowboys", "New York Giants", "Philadelphia Eagles", "Washington Commanders"],
    "NFC North": ["Chicago Bears", "Detroit Lions", "Green Bay Packers", "Minnesota Vikings"],
    "NFC South": ["Atlanta Falcons", "Carolina Panthers", "New Orleans Saints", "Tampa Bay Buccaneers"],
    "NFC West": ["Arizona Cardinals", "Los Angeles Rams", "San Francisco 49ers", "Seattle Seahawks"]
}

nfl_teams = [team for div in nfl_divisions.values() for team in div]

nba_divisions = {
    "Atlantic": ["Boston Celtics", "Brooklyn Nets", "New York Knicks", "Philadelphia 76ers", "Toronto Raptors"],
    "Central": ["Chicago Bulls", "Cleveland Cavaliers", "Detroit Pistons", "Indiana Pacers", "Milwaukee Bucks"],
    "Southeast": ["Atlanta Hawks", "Charlotte Hornets", "Miami Heat", "Orlando Magic", "Washington Wizards"],
    "Northwest": ["Denver Nuggets", "Minnesota Timberwolves", "Oklahoma City Thunder", "Portland Trail Blazers", "Utah Jazz"],
    "Pacific": ["Golden State Warriors", "Los Angeles Clippers", "Los Angeles Lakers", "Phoenix Suns", "Sacramento Kings"],
    "Southwest": ["Dallas Mavericks", "Houston Rockets", "Memphis Grizzlies", "New Orleans Pelicans", "San Antonio Spurs"]
}

nba_teams = [team for div in nba_divisions.values() for team in div]

mlb_divisions = {
    "AL East": ["Baltimore Orioles", "Boston Red Sox", "New York Yankees", "Tampa Bay Rays", "Toronto Blue Jays"],
    "AL Central": ["Chicago White Sox", "Cleveland Guardians", "Detroit Tigers", "Kansas City Royals", "Minnesota Twins"],
    "AL West": ["Houston Astros", "Los Angeles Angels", "Oakland Athletics", "Seattle Mariners", "Texas Rangers"],
    "NL East": ["Atlanta Braves", "Miami Marlins", "New York Mets", "Philadelphia Phillies", "Washington Nationals"],
    "NL Central": ["Chicago Cubs", "Cincinnati Reds", "Milwaukee Brewers", "Pittsburgh Pirates", "St. Louis Cardinals"],
    "NL West": ["Arizona Diamondbacks", "Colorado Rockies", "Los Angeles Dodgers", "San Diego Padres", "San Francisco Giants"]
}

mlb_teams = [team for div in mlb_divisions.values() for team in div]

nhl_divisions = {
    "Atlantic": ["Boston Bruins", "Buffalo Sabres", "Detroit Red Wings", "Florida Panthers", "Montreal Canadiens", "Ottawa Senators", "Tampa Bay Lightning", "Toronto Maple Leafs"],
    "Metropolitan": ["Carolina Hurricanes", "Columbus Blue Jackets", "New Jersey Devils", "New York Islanders", "New York Rangers", "Philadelphia Flyers", "Pittsburgh Penguins", "Washington Capitals"],
    "Central": ["Arizona Coyotes", "Chicago Blackhawks", "Colorado Avalanche", "Dallas Stars", "Minnesota Wild", "Nashville Predators", "St. Louis Blues", "Winnipeg Jets"],
    "Pacific": ["Anaheim Ducks", "Calgary Flames", "Edmonton Oilers", "Los Angeles Kings", "San Jose Sharks", "Seattle Kraken", "Vancouver Canucks", "Vegas Golden Knights"]
}

nhl_teams = [team for div in nhl_divisions.values() for team in div]

teams = {
    "NFL": nfl_teams,
    "NBA": nba_teams,
    "MLB": mlb_teams,
    "NHL": nhl_teams
}

def find_division(team, league):
    if league == "NFL":
        for div, tlist in nfl_divisions.items():
            if team in tlist:
                return div
    elif league == "NBA":
        for div, tlist in nba_divisions.items():
            if team in tlist:
                return div
    elif league == "MLB":
        for div, tlist in mlb_divisions.items():
            if team in tlist:
                return div
    elif league == "NHL":
        for div, tlist in nhl_divisions.items():
            if team in tlist:
                return div
    return None

def get_teams_in_division(league, division):
    if league == "NFL":
        return nfl_divisions.get(division, [])
    elif league == "NBA":
        return nba_divisions.get(division, [])
    elif league == "MLB":
        return mlb_divisions.get(division, [])
    elif league == "NHL":
        return nhl_divisions.get(division, [])
    return []

def get_conference_nfl(division):
    if division.startswith("AFC"):
        return "AFC"
    else:
        return "NFC"

def get_conference_nba(division):
    east = ["Atlantic", "Central", "Southeast"]
    if division in east:
        return "East"
    else:
        return "West"

def get_conference_mlb(division):
    if division.startswith("AL"):
        return "AL"
    else:
        return "NL"

def get_conference_nhl(division):
    if division in ["Atlantic", "Metropolitan"]:
        return "Eastern"
    else:
        return "Western"

def get_conference(league, division):
    if league == "NFL":
        return get_conference_nfl(division)
    elif league == "NBA":
        return get_conference_nba(division)
    elif league == "MLB":
        return get_conference_mlb(division)
    elif league == "NHL":
        return get_conference_nhl(division)
    return None

def generate_nfl_schedule(team):
    division = find_division(team, "NFL")
    division_teams = get_teams_in_division("NFL", division)
    conf = get_conference("NFL", division)

    division_opponents = [t for t in division_teams if t != team]
    division_games = []
    for opp in division_opponents:
        division_games.extend([f"{team} vs {opp}", f"{opp} vs {team}"])

    same_conf_divs = [d for d in nfl_divisions if get_conference("NFL", d) == conf and d != division]
    inter_division = random.choice(same_conf_divs)
    inter_div_teams = get_teams_in_division("NFL", inter_division)
    inter_div_games = []
    for opp in inter_div_teams:
        if len(inter_div_games) >= 4:
            break
        home_away = random.choice([f"{team} vs {opp}", f"{opp} vs {team}"])
        inter_div_games.append(home_away)

    other_conf_divs = [d for d in nfl_divisions if get_conference("NFL", d) != conf]
    other_conf_div = random.choice(other_conf_divs)
    other_conf_teams = get_teams_in_division("NFL", other_conf_div)
    other_conf_games = []
    for opp in other_conf_teams:
        if len(other_conf_games) >= 4:
            break
        home_away = random.choice([f"{team} vs {opp}", f"{opp} vs {team}"])
        other_conf_games.append(home_away)
      
    same_conf_teams = []
    for d in same_conf_divs:
        same_conf_teams.extend(get_teams_in_division("NFL", d))
    two_same_pos = random.sample(same_conf_teams, 2)
    two_same_pos_games = []
    for opp in two_same_pos:
        home_away = random.choice([f"{team} vs {opp}", f"{opp} vs {team}"])
        two_same_pos_games.append(home_away)

    remaining_divs = [d for d in other_conf_divs if d != other_conf_div]
    if remaining_divs:
        remaining_div = random.choice(remaining_divs)
        rem_div_teams = get_teams_in_division("NFL", remaining_div)
        if rem_div_teams:
            opp = random.choice(rem_div_teams)
            home_away = random.choice([f"{team} vs {opp}", f"{opp} vs {team}"])
            interconference_game = [home_away]
        else:
            interconference_game = []
    else:
        interconference_game = []

    all_games = division_games + inter_div_games + other_conf_games + two_same_pos_games + interconference_game
    if len(all_games) < 17:
        filler_pool = [t for t in nfl_teams if t != team and t not in division_opponents]
        while len(all_games) < 17:
            opp = random.choice(filler_pool)
            home_away = random.choice([f"{team} vs {opp}", f"{opp} vs {team}"])
            if home_away not in all_games:
                all_games.append(home_away)

    random.shuffle(all_games)
    return all_games

def generate_nba_schedule(team):
    division = find_division(team, "NBA")
    division_teams = get_teams_in_division("NBA", division)
    conf = get_conference("NBA", division)

    schedule = []

    division_opponents = [t for t in division_teams if t != team]
    for opp in division_opponents:
        schedule.extend([f"{team} vs {opp}"] * 4)

    conf_divs = [d for d in nba_divisions if get_conference("NBA", d) == conf and d != division]
    conf_teams = []
    for d in conf_divs:
        conf_teams.extend(get_teams_in_division("NBA", d))

    conf_opponents = [t for t in conf_teams if t != team]
    for opp in conf_opponents:
        schedule.extend([f"{team} vs {opp}"] * 3)

    other_conf_divs = [d for d in nba_divisions if get_conference("NBA", d) != conf]
    other_conf_teams = []
    for d in other_conf_divs:
        other_conf_teams.extend(get_teams_in_division("NBA", d))

    non_conf_opponents = [t for t in other_conf_teams if t != team]
    for opp in non_conf_opponents:
        schedule.append(f"{team} vs {opp}")

    random.shuffle(schedule)
    return schedule

def generate_mlb_schedule(team):
    division = find_division(team, "MLB")
    division_teams = get_teams_in_division("MLB", division)
    conf = get_conference("MLB", division)

    schedule = []

    def split_series_19():
        return [3,3,3,4,3,3]

    def split_series_6():
        return [3,3]

    for opp in division_teams:
        if opp == team:
            continue
        series_lengths = split_series_19()
        home_away_flag = True
        for length in series_lengths:
            for game_num in range(length):
                if home_away_flag:
                    game = f"{team} vs {opp}"
                else:
                    game = f"{opp} vs {team}"
                schedule.append(game)
            home_away_flag = not home_away_flag

    same_league_divisions = [d for d in mlb_divisions if get_conference("MLB", d) == conf and d != division]
    other_division_teams = []
    for d in same_league_divisions:
        other_division_teams.extend(get_teams_in_division("MLB", d))

    for opp in other_division_teams:
        series_lengths = split_series_6()
        home_away_flag = True
        for length in series_lengths:
            for _ in range(length):
                if home_away_flag:
                    game = f"{team} vs {opp}"
                else:
                    game = f"{opp} vs {team}"
                schedule.append(game)
            home_away_flag = not home_away_flag

    other_league_divisions = [d for d in mlb_divisions if get_conference("MLB", d) != conf]
    interleague_teams = []
    for d in other_league_divisions:
        interleague_teams.extend(get_teams_in_division("MLB", d))

    for opp in interleague_teams:
        home_away_flag = True
        series_length = 3
        for _ in range(series_length):
            if home_away_flag:
                game = f"{team} vs {opp}"
            else:
                game = f"{opp} vs {team}"
            schedule.append(game)

    random.shuffle(schedule)
    return schedule

def generate_nhl_schedule(team):
    division = find_division(team, "NHL")
    division_teams = get_teams_in_division("NHL", division)
    conf = get_conference("NHL", division)

    schedule = []

    division_opponents = [t for t in division_teams if t != team]
    for opp in division_opponents:
        schedule.extend([f"{team} vs {opp}"] * 6)

    conf_divs = [d for d in nhl_divisions if get_conference("NHL", d) == conf and d != division]
    conf_teams = []
    for d in conf_divs:
        conf_teams.extend(get_teams_in_division("NHL", d))

    conf_opponents = [t for t in conf_teams if t != team]
    for opp in conf_opponents:
        schedule.extend([f"{team} vs {opp}"] * 4)

    other_conf_divs = [d for d in nhl_divisions if get_conference("NHL", d) != conf]
    other_conf_teams = []
    for d in other_conf_divs:
        other_conf_teams.extend(get_teams_in_division("NHL", d))

    non_conf_opponents = [t for t in other_conf_teams if t != team]
    for opp in non_conf_opponents:
        schedule.append(f"{team} vs {opp}")

    random.shuffle(schedule)
    return schedule

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate_schedule", methods=["POST"])
def generate_schedule():
    data = request.json
    team = data.get("team")
    league = data.get("league")

    if league not in teams:
        return jsonify({"error": "Invalid league"}), 400
    if team not in teams[league]:
        return jsonify({"error": "Invalid team"}), 400

    if league == "NFL":
        schedule = generate_nfl_schedule(team)
    elif league == "NBA":
        schedule = generate_nba_schedule(team)
    elif league == "MLB":
        schedule = generate_mlb_schedule(team)
    elif league == "NHL":
        schedule = generate_nhl_schedule(team)
    else:
        schedule = []

    return jsonify({"schedule": schedule})

if __name__ == "__main__":
    app.run(debug=True)
