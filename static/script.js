document.getElementById('leagueSelect').addEventListener('change', async function() {
    const league = this.value;
    const teamSelect = document.getElementById('teamSelect');

    if (!league) {
        teamSelect.innerHTML = '<option value="">Select Team</option>';
        return;
    }

    let teams = [];

    if (league === 'NFL') {
        teams = ["Buffalo Bills", "Miami Dolphins", "New England Patriots", "New York Jets",
                 "Baltimore Ravens", "Cincinnati Bengals", "Cleveland Browns", "Pittsburgh Steelers",
                 "Houston Texans", "Indianapolis Colts", "Jacksonville Jaguars", "Tennessee Titans",
                 "Denver Broncos", "Kansas City Chiefs", "Las Vegas Raiders", "Los Angeles Chargers",
                 "Dallas Cowboys", "New York Giants", "Philadelphia Eagles", "Washington Commanders",
                 "Chicago Bears", "Detroit Lions", "Green Bay Packers", "Minnesota Vikings",
                 "Atlanta Falcons", "Carolina Panthers", "New Orleans Saints", "Tampa Bay Buccaneers",
                 "Arizona Cardinals", "Los Angeles Rams", "San Francisco 49ers", "Seattle Seahawks"];
    } else if (league === 'NBA') {
        teams = ["Boston Celtics", "Brooklyn Nets", "New York Knicks", "Philadelphia 76ers", "Toronto Raptors",
                 "Chicago Bulls", "Cleveland Cavaliers", "Detroit Pistons", "Indiana Pacers", "Milwaukee Bucks",
                 "Atlanta Hawks", "Charlotte Hornets", "Miami Heat", "Orlando Magic", "Washington Wizards",
                 "Denver Nuggets", "Minnesota Timberwolves", "Oklahoma City Thunder", "Portland Trail Blazers", "Utah Jazz",
                 "Golden State Warriors", "Los Angeles Clippers", "Los Angeles Lakers", "Phoenix Suns", "Sacramento Kings",
                 "Dallas Mavericks", "Houston Rockets", "Memphis Grizzlies", "New Orleans Pelicans", "San Antonio Spurs"];
    } else if (league === 'MLB') {
        teams = ["Baltimore Orioles", "Boston Red Sox", "New York Yankees", "Tampa Bay Rays", "Toronto Blue Jays",
                 "Chicago White Sox", "Cleveland Guardians", "Detroit Tigers", "Kansas City Royals", "Minnesota Twins",
                 "Houston Astros", "Los Angeles Angels", "Oakland Athletics", "Seattle Mariners", "Texas Rangers",
                 "Atlanta Braves", "Miami Marlins", "New York Mets", "Philadelphia Phillies", "Washington Nationals",
                 "Chicago Cubs", "Cincinnati Reds", "Milwaukee Brewers", "Pittsburgh Pirates", "St. Louis Cardinals",
                 "Arizona Diamondbacks", "Colorado Rockies", "Los Angeles Dodgers", "San Diego Padres", "San Francisco Giants"];
    } else if (league === 'NHL') {
        teams = ["Boston Bruins", "Buffalo Sabres", "Detroit Red Wings", "Florida Panthers", "Montreal Canadiens", "Ottawa Senators", "Tampa Bay Lightning", "Toronto Maple Leafs",
                 "Carolina Hurricanes", "Columbus Blue Jackets", "New Jersey Devils", "New York Islanders", "New York Rangers", "Philadelphia Flyers", "Pittsburgh Penguins", "Washington Capitals",
                 "Arizona Coyotes", "Chicago Blackhawks", "Colorado Avalanche", "Dallas Stars", "Minnesota Wild", "Nashville Predators", "St. Louis Blues", "Winnipeg Jets",
                 "Anaheim Ducks", "Calgary Flames", "Edmonton Oilers", "Los Angeles Kings", "San Jose Sharks", "Seattle Kraken", "Vancouver Canucks", "Vegas Golden Knights"];
    }

    teamSelect.innerHTML = '<option value="">Select Team</option>';
    teams.forEach(team => {
        const option = document.createElement('option');
        option.value = team;
        option.textContent = team;
        teamSelect.appendChild(option);
    });
});

document.getElementById('teamSelect').addEventListener('change', async function() {
    const league = document.getElementById('leagueSelect').value;
    const team = this.value;
    const scheduleDiv = document.getElementById('schedule');

    if (!league || !team) {
        scheduleDiv.innerHTML = '';
        return;
    }

    const response = await fetch('/get_schedule', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ league, team })
    });

    const data = await response.json();

    if (data.error) {
        scheduleDiv.innerHTML = `<p>Error: ${data.error}</p>`;
        return;
    }

    let html = `<h3>Schedule for ${team} (${league})</h3><ul>`;
    data.schedule.forEach(game => {
        html += `<li>${game}</li>`;
    });
    html += '</ul>';

    scheduleDiv.innerHTML = html;
});
