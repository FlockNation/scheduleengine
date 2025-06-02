const teams = {
  NFL: ["All Teams", "Arizona Cardinals", "Atlanta Falcons", "Baltimore Ravens", "Buffalo Bills", "Carolina Panthers", "Chicago Bears", "Cincinnati Bengals", "Cleveland Browns", "Dallas Cowboys", "Denver Broncos", "Detroit Lions", "Green Bay Packers", "Houston Texans", "Indianapolis Colts", "Jacksonville Jaguars", "Kansas City Chiefs", "Las Vegas Raiders", "Los Angeles Chargers", "Los Angeles Rams", "Miami Dolphins", "Minnesota Vikings", "New England Patriots", "New Orleans Saints", "New York Giants", "New York Jets", "Philadelphia Eagles", "Pittsburgh Steelers", "San Francisco 49ers", "Seattle Seahawks", "Tampa Bay Buccaneers", "Tennessee Titans", "Washington Commanders"],
  NBA: ["All Teams", "Atlanta Hawks", "Boston Celtics", "Brooklyn Nets", "Charlotte Hornets", "Chicago Bulls", "Cleveland Cavaliers", "Dallas Mavericks", "Denver Nuggets", "Detroit Pistons", "Golden State Warriors", "Houston Rockets", "Indiana Pacers", "Los Angeles Clippers", "Los Angeles Lakers", "Memphis Grizzlies", "Miami Heat", "Milwaukee Bucks", "Minnesota Timberwolves", "New Orleans Pelicans", "New York Knicks", "Oklahoma City Thunder", "Orlando Magic", "Philadelphia 76ers", "Phoenix Suns", "Portland Trail Blazers", "Sacramento Kings", "San Antonio Spurs", "Toronto Raptors", "Utah Jazz", "Washington Wizards"],
  MLB: ["All Teams", "Arizona Diamondbacks", "Atlanta Braves", "Baltimore Orioles", "Boston Red Sox", "Chicago White Sox", "Chicago Cubs", "Cincinnati Reds", "Cleveland Guardians", "Colorado Rockies", "Detroit Tigers", "Houston Astros", "Kansas City Royals", "Los Angeles Angels", "Los Angeles Dodgers", "Miami Marlins", "Milwaukee Brewers", "Minnesota Twins", "New York Yankees", "New York Mets", "Oakland Athletics", "Philadelphia Phillies", "Pittsburgh Pirates", "San Diego Padres", "San Francisco Giants", "Seattle Mariners", "St. Louis Cardinals", "Tampa Bay Rays", "Texas Rangers", "Toronto Blue Jays", "Washington Nationals"],
  NHL: ["All Teams", "Anaheim Ducks", "Arizona Coyotes", "Boston Bruins", "Buffalo Sabres", "Calgary Flames", "Carolina Hurricanes", "Chicago Blackhawks", "Colorado Avalanche", "Columbus Blue Jackets", "Dallas Stars", "Detroit Red Wings", "Edmonton Oilers", "Florida Panthers", "Los Angeles Kings", "Minnesota Wild", "Montreal Canadiens", "Nashville Predators", "New Jersey Devils", "New York Islanders", "New York Rangers", "Ottawa Senators", "Philadelphia Flyers", "Pittsburgh Penguins", "San Jose Sharks", "Seattle Kraken", "St. Louis Blues", "Tampa Bay Lightning", "Toronto Maple Leafs", "Vancouver Canucks", "Vegas Golden Knights", "Washington Capitals", "Winnipeg Jets"]
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
        <h2>Schedule Formulas</h2>
        <ul style="text-align: left; max-width: 600px; margin: 0 auto;">
          <li><strong>NFL:</strong> 17 games total:
            <ul>
              <li>6 division games (2 vs each rival)</li>
              <li>4 vs another division in same conference</li>
              <li>4 vs division in opposite conference</li>
              <li>2 same-conference teams from remaining divisions (based on standings)</li>
              <li>1 interconference "17th" game</li>
            </ul>
          </li>
          <li><strong>NBA:</strong> 82 games total:
            <ul>
              <li>4 games vs 4 division opponents (16)</li>
              <li>3 or 4 games vs other conference teams (42)</li>
              <li>2 games vs each team in the other conference (30)</li>
            </ul>
          </li>
          <li><strong>MLB:</strong> 162 games:
            <ul>
              <li>13 games vs division rivals</li>
              <li>6-7 games vs same-league non-division teams</li>
              <li>Interleague: 1 series vs all teams in 1 division, rivals, and rotating matchups</li>
            </ul>
          </li>
          <li><strong>NHL:</strong> 82 games:
            <ul>
              <li>3-4 games vs division opponents (26)</li>
              <li>2-3 games vs same-conference, non-division teams (24)</li>
              <li>2 games vs each team in other conference (32)</li>
            </ul>
          </li>
        </ul>
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
