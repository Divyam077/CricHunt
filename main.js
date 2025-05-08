// CrickHunt Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Handle tournament selection and data loading
    const tournamentForm = document.getElementById('tournament-form');
    if (tournamentForm) {
        tournamentForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const tournamentId = document.getElementById('tournament-select').value;
            fetchTournamentStats(tournamentId);
        });
    }

    // Initialize any active tabs
    const tabLinks = document.querySelectorAll('.tab-link');
    if (tabLinks.length > 0) {
        tabLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Remove active class from all tabs
                tabLinks.forEach(l => l.classList.remove('active'));
                
                // Add active class to clicked tab
                this.classList.add('active');
                
                // Show the corresponding content
                const targetId = this.getAttribute('data-target');
                const tabContents = document.querySelectorAll('.tab-content');
                
                tabContents.forEach(content => {
                    content.style.display = 'none';
                });
                
                document.getElementById(targetId).style.display = 'block';
            });
        });
        
        // Activate first tab by default
        tabLinks[0].click();
    }
});

// Function to fetch tournament statistics
function fetchTournamentStats(tournamentId) {
    // Show loading indicators
    document.getElementById('bowlers-container').innerHTML = '<div class="loading">Loading bowler statistics...</div>';
    document.getElementById('batsmen-container').innerHTML = '<div class="loading">Loading batsman statistics...</div>';
    
    // Fetch data from the API
    fetch('/api/get_tournament_stats', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ tournament_id: tournamentId })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        displayBowlerStats(data.bowlers);
        displayBatsmanStats(data.batsmen);
        document.getElementById('tournament-title').textContent = data.tournament;
    })
    .catch(error => {
        console.error('Error fetching tournament data:', error);
        document.getElementById('bowlers-container').innerHTML = '<div class="error">Failed to load bowler statistics. Please try again.</div>';
        document.getElementById('batsmen-container').innerHTML = '<div class="error">Failed to load batsman statistics. Please try again.</div>';
    });
}

// Function to display bowler statistics
function displayBowlerStats(bowlers) {
    const container = document.getElementById('bowlers-container');
    
    if (!bowlers || bowlers.length === 0) {
        container.innerHTML = '<div class="no-data">No bowler data available</div>';
        return;
    }
    
    let html = `
        <table class="stats-table">
            <thead>
                <tr>
                    <th>Rank</th>
                    <th>Player</th>
                    <th>Team</th>
                    <th>Wickets</th>
                    <th>Matches</th>
                    <th>Average</th>
                    <th>Best Figures</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    bowlers.forEach(bowler => {
        html += `
            <tr>
                <td>${bowler.rank}</td>
                <td>${bowler.name}</td>
                <td>${bowler.team}</td>
                <td>${bowler.wickets}</td>
                <td>${bowler.matches}</td>
                <td>${bowler.average}</td>
                <td>${bowler.best_figures}</td>
            </tr>
        `;
    });
    
    html += `
            </tbody>
        </table>
    `;
    
    container.innerHTML = html;
}

// Function to display batsman statistics
function displayBatsmanStats(batsmen) {
    const container = document.getElementById('batsmen-container');
    
    if (!batsmen || batsmen.length === 0) {
        container.innerHTML = '<div class="no-data">No batsman data available</div>';
        return;
    }
    
    let html = `
        <table class="stats-table">
            <thead>
                <tr>
                    <th>Rank</th>
                    <th>Player</th>
                    <th>Team</th>
                    <th>Runs</th>
                    <th>Matches</th>
                    <th>Average</th>
                    <th>Highest Score</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    batsmen.forEach(batsman => {
        html += `
            <tr>
                <td>${batsman.rank}</td>
                <td>${batsman.name}</td>
                <td>${batsman.team}</td>
                <td>${batsman.runs}</td>
                <td>${batsman.matches}</td>
                <td>${batsman.average}</td>
                <td>${batsman.highest_score}</td>
            </tr>
        `;
    });
    
    html += `
            </tbody>
        </table>
    `;
    
    container.innerHTML = html;
} 