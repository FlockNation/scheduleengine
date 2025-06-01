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
    div_map = {"NFL": nfl_divisions, "NBA": nba_divisions, "MLB": mlb_divisions, "NHL": nhl_divisions}
    for div, tlist in div_map[league].items():
        if team in tlist:
            return div
    return None

def get_teams_in_division(league, division):
    div_map = {"NFL": nfl_divisions, "NBA": nba_divisions, "MLB": mlb_divisions, "NHL": nhl_divisions}
    return div_map[league].get(division, [])

def get_conference(league, division):
    if league == "NFL":
        return "AFC" if division.startswith("AFC") else "NFC"
    if league == "NBA":
        return "East" if division in ["Atlantic", "Central", "Southeast"] else "West"
    if league == "MLB":
        return "AL" if division.startswith("AL") else "NL"
    if league == "NHL":
        return "Eastern" if division in ["Atlantic", "Metropolitan"] else "Western"
    return None

def generate_balanced_schedule(team, opponents, total_games, same_match_count=1):
    schedule = []
    count = 0
    for opp in opponents:
        for _ in range(same_match_count):
            if count % 2 == 0:
                schedule.append(f"{team} vs {opp}")
            else:
                schedule.append(f"{opp} vs {team}")
            count += 1
    while len(schedule) < total_games:
        opp = random.choice(opponents)
        matchup = f"{team} vs {opp}" if schedule.count(f"{team} vs {opp}") <= schedule.count(f"{opp} vs {team}") else f"{opp} vs {team}"
        schedule.append(matchup)
    return schedule

def generate_nfl_schedule(team):
    division = find_division(team, "NFL")
    division_teams = get_teams_in_division("NFL", division)
    conf = get_conference("NFL", division)

    division_opponents = [t for t in division_teams if t != team]
    division_games = generate_balanced_schedule(team, division_opponents, 6, 2)

    same_conf_divs = [d for d in nfl_divisions if get_conference("NFL", d) == conf and d != division]
    inter_conf_divs = [d for d in nfl_divisions if get_conference("NFL", d) != conf]

    same_conf_div = random.choice(same_conf_divs)
    inter_conf_div = random.choice(inter_conf_divs)

    same_conf_teams = get_teams_in_division("NFL", same_conf_div)
    inter_conf_teams = get_teams_in_division("NFL", inter_conf_div)

    same_conf_games = generate_balanced_schedule(team, same_conf_teams, 4, 1)
    inter_conf_games = generate_balanced_schedule(team, inter_conf_teams, 4, 1)

    scheduled_teams = set(division_opponents + same_conf_teams + inter_conf_teams)
    scheduled_teams.discard(team)

    remaining_teams = [t for t in nfl_teams if t != team and t not in scheduled_teams]
    extra_opponents = random.sample(remaining_teams, 3)
    extra_games = generate_balanced_schedule(team, extra_opponents, 3, 1)

    all_games = division_games + same_conf_games + inter_conf_games + extra_games
    random.shuffle(all_games)
    return all_games
    
def generate_nba_schedule(team):
    division = find_division(team, "NBA")
    division_teams = [t for t in get_teams_in_division("NBA", division) if t != team]
    conf = get_conference("NBA", division)

    conf_teams = [t for d in nba_divisions if get_conference("NBA", d) == conf and d != division for t in get_teams_in_division("NBA", d) if t != team]
    other_conf_teams = [t for d in nba_divisions if get_conference("NBA", d) != conf for t in get_teams_in_division("NBA", d)]

    schedule = []
    schedule += generate_balanced_schedule(team, division_teams, 16, 4)

    four_game_conf_opponents = random.sample(conf_teams, 6)
    three_game_conf_opponents = [t for t in conf_teams if t not in four_game_conf_opponents]

    schedule += generate_balanced_schedule(team, four_game_conf_opponents, 24, 4)
    schedule += generate_balanced_schedule(team, three_game_conf_opponents, 12, 3)
    schedule += generate_balanced_schedule(team, other_conf_teams, 30, 2)

    random.shuffle(schedule)
    return schedule

def generate_mlb_schedule(team):
    division = find_division(team, "MLB")
    division_teams = [t for t in get_teams_in_division("MLB", division) if t != team]
    conf = get_conference("MLB", division)
    same_league_teams = [t for d in mlb_divisions if get_conference("MLB", d) == conf and d != division for t in get_teams_in_division("MLB", d)]
    interleague_teams = [t for d in mlb_divisions if get_conference("MLB", d) != conf for t in get_teams_in_division("MLB", d)]

    schedule = []

    def add_series(opponents, series_count, games_per_series):
        chosen_teams = random.sample(opponents, min(series_count, len(opponents)))
        home_away_toggle = True
        for opp in chosen_teams:
            if home_away_toggle:
                for _ in range(games_per_series):
                    schedule.append(f"{team} vs {opp}")
            else:
                for _ in range(games_per_series):
                    schedule.append(f"{opp} vs {team}")
            home_away_toggle = not home_away_toggle

    total_3_game_series = 30
    total_4_game_series = 18

    division_series_teams = random.sample(division_teams, min(len(division_teams), 3))
    home_away_toggle = True
    for opp in division_series_teams:
        games_in_series = 3 if total_3_game_series > 0 else 4
        if games_in_series == 3:
            total_3_game_series -= 1
        else:
            total_4_game_series -= 1
        if home_away_toggle:
            for _ in range(games_in_series):
                schedule.append(f"{team} vs {opp}")
        else:
            for _ in range(games_in_series):
                schedule.append(f"{opp} vs {team}")
        home_away_toggle = not home_away_toggle

    remaining_3_game_series = total_3_game_series
    remaining_4_game_series = total_4_game_series

    all_opponents = same_league_teams + interleague_teams
    random.shuffle(all_opponents)
    opponents_index = 0

    while remaining_3_game_series > 0 or remaining_4_game_series > 0:
        if opponents_index >= len(all_opponents):
            opponents_index = 0
            random.shuffle(all_opponents)
        opp = all_opponents[opponents_index]
        opponents_index += 1

        if remaining_3_game_series > 0:
            games_in_series = 3
            remaining_3_game_series -= 1
        elif remaining_4_game_series > 0:
            games_in_series = 4
            remaining_4_game_series -= 1
        else:
            break

        if home_away_toggle:
            for _ in range(games_in_series):
                schedule.append(f"{team} vs {opp}")
        else:
            for _ in range(games_in_series):
                schedule.append(f"{opp} vs {team}")
        home_away_toggle = not home_away_toggle

    if len(schedule) > 162:
        schedule = schedule[:162]
    elif len(schedule) < 162:
        extra_needed = 162 - len(schedule)
        extra_games = []
        home_away_toggle = True
        while len(extra_games) < extra_needed:
            opp = random.choice(division_teams)
            if home_away_toggle:
                extra_games.append(f"{team} vs {opp}")
            else:
                extra_games.append(f"{opp} vs {team}")
            home_away_toggle = not home_away_toggle
        schedule += extra_games
        
    return schedule

def generate_nhl_schedule(team):
    division = find_division(team, "NHL")
    division_teams = [t for t in get_teams_in_division("NHL", division) if t != team]
    conf = get_conference("NHL", division)
    same_conf_teams = [t for d in nhl_divisions if get_conference("NHL", d) == conf and d != division for t in get_teams_in_division("NHL", d)]
    other_conf_teams = [t for d in nhl_divisions if get_conference("NHL", d) != conf for t in get_teams_in_division("NHL", d)]

    schedule = []

    def add_games(opponents, games_per_opponent):
        for opp in opponents:
            for i in range(games_per_opponent):
                if i % 2 == 0:
                    schedule.append(f"{team} vs {opp}")
                else:
                    schedule.append(f"{opp} vs {team}")

    four_game_opps = random.sample(division_teams, 3)
    three_game_opps = [t for t in division_teams if t not in four_game_opps]
    add_games(four_game_opps, 4)
    add_games(three_game_opps, 3)
    extra_same_conf = random.sample(same_conf_teams, 2)
    other_same_conf = [t for t in same_conf_teams if t not in extra_same_conf]
    add_games(extra_same_conf, 4)
    add_games(other_same_conf, 3)
    add_games(other_conf_teams, 2)

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
    print(f"Received request: league={league}, team={team}")
    if league not in teams:
        return jsonify({"error": f"Invalid league: {league}"}), 400
    if team not in teams[league]:
        return jsonify({"error": f"Invalid team: {team} for league {league}"}), 400
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
