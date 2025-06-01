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
    populateTeams(currentLeague);
    dropdownContainer.style.display = "block";
    if (teamSelect.value === "All Teams") {
      scheduleDisplay.innerHTML = `<p>Please select a specific team to see schedule.</p>`;
    } else {
      fetchAndDisplaySchedule(currentLeague, teamSelect.value);
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
  console.log("Fetching schedule for", league, team);
  scheduleDisplay.innerHTML = `<p>Loading schedule...</p>`;
  try {
    const response = await fetch("/generate_schedule", { 
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ league, team }),
    });
    console.log("Response status:", response.status);
    if (!response.ok) throw new Error("Network response was not ok");
    const data = await response.json();
    console.log("Received data:", data);
    renderSchedule(team, data.schedule);
  } catch (error) {
    console.error(error);
    scheduleDisplay.innerHTML = `<p>Error loading schedule.</p>`;
  }
}

function renderSchedule(team, schedule) {
  let html = `<h2>${team === "All Teams" ? currentLeague + " League Schedule" : team + " Schedule"}</h2>`;
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
