const teams = {
  NFL: ["All Teams", "Arizona Cardinals", "Atlanta Falcons", "Baltimore Ravens", "Buffalo Bills", "Carolina Panthers", "Chicago Bears", "Cincinnati Bengals", "Cleveland Browns", "Dallas Cowboys", "Denver Broncos", "Detroit Lions", "Green Bay Packers", "Houston Texans", "Indianapolis Colts", "Jacksonville Jaguars", "Kansas City Chiefs", "Las Vegas Raiders", "Los Angeles Chargers", "Los Angeles Rams", "Miami Dolphins", "Minnesota Vikings", "New England Patriots", "New Orleans Saints", "New York Giants", "New York Jets", "Philadelphia Eagles", "Pittsburgh Steelers", "San Francisco 49ers", "Seattle Seahawks", "Tampa Bay Buccaneers", "Tennessee Titans", "Washington Commanders"],
  NBA: ["All Teams", "Atlanta Hawks", "Boston Celtics", "Brooklyn Nets", "Charlotte Hornets", "Chicago Bulls", "Cleveland Cavaliers", "Dallas Mavericks", "Denver Nuggets", "Detroit Pistons", "Golden State Warriors", "Houston Rockets", "Indiana Pacers", "Los Angeles Clippers", "Los Angeles Lakers", "Memphis Grizzlies", "Miami Heat", "Milwaukee Bucks", "Minnesota Timberwolves", "New Orleans Pelicans", "New York Knicks", "Oklahoma City Thunder", "Orlando Magic", "Philadelphia 76ers", "Phoenix Suns", "Portland Trail Blazers", "Sacramento Kings", "San Antonio Spurs", "Toronto Raptors", "Utah Jazz", "Washington Wizards"],
  MLB: ["All Teams", "Arizona Diamondbacks", "Atlanta Braves", "Baltimore Orioles", "Boston Red Sox", "Chicago White Sox", "Chicago Cubs", "Cincinnati Reds", "Cleveland Guardians", "Colorado Rockies", "Detroit Tigers", "Houston Astros", "Kansas City Royals", "Los Angeles Angels", "Los Angeles Dodgers", "Miami Marlins", "Milwaukee Brewers", "Minnesota Twins", "New York Yankees", "New York Mets", "Oakland Athletics", "Philadelphia Phillies", "Pittsburgh Pirates", "San Diego Padres", "San Francisco Giants", "Seattle Mariners", "St. Louis Cardinals", "Tampa Bay Rays", "Texas Rangers", "Toronto Blue Jays", "Washington Nationals"],
  NHL: ["All Teams", "Anaheim Ducks", "Arizona Coyotes", "Boston Bruins", "Buffalo Sabres", "Calgary Flames", "Carolina Hurricanes", "Chicago Blackhawks", "Colorado Avalanche", "Columbus Blue Jackets", "Dallas Stars", "Detroit Red Wings", "Edmonton Oilers", "Florida Panthers", "Los Angeles Kings", "Minnesota Wild", "Montreal Canadiens", "Nashville Predators", "New Jersey Devils", "New York Islanders", "New York Rangers", "Ottawa Senators", "Philadelphia Flyers", "Pittsburgh Penguins", "San Jose Sharks", "Seattle Kraken", "St. Louis Blues", "Tampa Bay Lightning", "Toronto Maple Leafs", "Vancouver Canucks", "Vegas Golden Knights", "Washington Capitals", "Winnipeg Jets"],
  Formulas: ["Formulas"]
};

let currentLeague = "";

const leagueButtons = document.querySelectorAll(".league-buttons button");
const dropdownContainer = document.getElementById("dropdown-container");
const teamSelect = document.getElementById("team-select");
const scheduleDisplay = document.getElementById("schedule-display");

leagueButtons.forEach(button => {
  button.addEventListener("click", () => {
    currentLeague = button.getAttribute("data-league");
    if (currentLeague === "Formulas") {
      dropdownContainer.style.display = "none";
      scheduleDisplay.innerHTML = `
        <h2>League Schedule Formulas & Logic</h2>
        <section>
          <h3>NFL Schedule</h3>
          <p>The NFL schedule consists of 17 regular season games per team:</p>
          <ul>
            <li>6 games against division opponents (each team plays the other 3 teams twice, home and away)</li>
            <li>4 games against teams from another division within the same conference (rotates yearly)</li>
            <li>4 games against teams from a division in the other conference (rotates yearly)</li>
            <li>2 games against conference teams that finished in the same place in their divisions the previous season</li>
            <li>1 game against a non-conference opponent based on the previous season's standings</li>
          </ul>
        </section>
        <section>
          <h3>NBA Schedule</h3>
          <p>The NBA schedule includes 82 games per team:</p>
          <ul>
            <li>16 games against division opponents (4 games against each of 4 division teams)</li>
            <li>36 games against other conference teams outside division (3 or 4 games per team)</li>
            <li>30 games against teams from the other conference (2 games per team)</li>
          </ul>
          <p>This ensures a balanced schedule emphasizing divisional and conference rivalries.</p>
        </section>
        <section>
          <h3>MLB Schedule</h3>
          <p>MLB teams play 162 games per season:</p>
          <ul>
            <li>19 games against each division opponent (total 76 games)</li>
            <li>66 games against other teams in the same league but outside the division</li>
            <li>20 interleague games against teams from the other league</li>
          </ul>
          <p>The exact distribution varies slightly due to scheduling constraints and interleague play.</p>
        </section>
        <section>
          <h3>NHL Schedule</h3>
          <p>The NHL schedule has 82 games per team:</p>
          <ul>
            <li>24 games against division opponents (3 or 4 games per team)</li>
            <li>26 games against other teams in the same conference but outside division (2 games per team)</li>
            <li>32 games against teams from the other conference (1 or 2 games per team)</li>
          </ul>
          <p>Scheduling focuses on divisional rivalry while ensuring balanced competition across conferences.</p>
        </section>
      `;
    } else {
      populateTeams(currentLeague);
      dropdownContainer.style.display = "block";
      scheduleDisplay.innerHTML = `<p>Please select a specific team to see schedule.</p>`;
    }
  });
});

teamSelect.addEventListener("change", () => {
  const selectedTeam = teamSelect.value;
  if (selectedTeam === "All Teams") {
    scheduleDisplay.innerHTML = `<p>Please select a specific team to see schedule.</p>`;
    return;
  }
  fetchAndDisplaySchedule(currentLeague, selectedTeam);
});

function populateTeams(league) {
  teamSelect.innerHTML = "";
  teams[league].forEach(team => {
    const option = document.createElement("option");
    option.value = team;
    option.textContent = team;
    teamSelect.appendChild(option);
  });
  teamSelect.value = "All Teams";
}

async function fetchAndDisplaySchedule(league, team) {
  scheduleDisplay.innerHTML = `<p>Loading schedule for ${team}...</p>`;
  try {
    const response = await fetch("/generate_schedule", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ league, team }),
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch schedule: ${response.status}`);
    }

    const data = await response.json();
    renderSchedule(team, data.schedule);
  } catch (err) {
    console.error(err);
    scheduleDisplay.innerHTML = `<p>Error loading schedule for ${team}.</p>`;
  }
}

function renderSchedule(team, schedule) {
  let html = `<h2>${team} Schedule</h2>`;
  if (!schedule || schedule.length === 0) {
    html += "<p>No schedule available.</p>";
  } else {
    html += "<div>";
    schedule.forEach(game => {
      html += `<div class="game-item">${game}</div>`;
    });
    html += "</div>";
  }
  scheduleDisplay.innerHTML = html;
}
