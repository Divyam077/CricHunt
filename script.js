document.addEventListener('DOMContentLoaded', function() {
    const player1Input = document.getElementById('player1');
    const player2Input = document.getElementById('player2');
    const tournamentSelect = document.getElementById('tournament');
    const playerTypeSelect = document.getElementById('playerType');
    const comparisonResult = document.getElementById('comparisonResult');
    
    // Initialize autocomplete for both player inputs
    initializeAutocomplete(player1Input);
    initializeAutocomplete(player2Input);
    
    // Function to initialize autocomplete for a player input
    function initializeAutocomplete(input) {
        input.addEventListener('input', function() {
            const query = this.value;
            if (query.length < 2) return;
            
            fetch(`/search_players/?query=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    const results = data.results;
                    const datalist = document.createElement('datalist');
                    datalist.id = `${input.id}List`;
                    
                    results.forEach(player => {
                        const option = document.createElement('option');
                        option.value = player.name;
                        option.dataset.id = player.id;
                        option.dataset.team = player.team;
                        option.dataset.role = player.role;
                        datalist.appendChild(option);
                    });
                    
                    // Remove existing datalist if any
                    const existingDatalist = document.getElementById(`${input.id}List`);
                    if (existingDatalist) {
                        existingDatalist.remove();
                    }
                    
                    input.setAttribute('list', `${input.id}List`);
                    document.body.appendChild(datalist);
                })
                .catch(error => console.error('Error:', error));
        });
    }
    
    // Function to compare players
    function comparePlayers() {
        const player1Id = document.querySelector(`option[value="${player1Input.value}"]`)?.dataset.id;
        const player2Id = document.querySelector(`option[value="${player2Input.value}"]`)?.dataset.id;
        const tournamentId = tournamentSelect.value;
        
        if (!player1Id || !player2Id) {
            comparisonResult.innerHTML = '<p>Please select valid players</p>';
            return;
        }
        
        fetch(`/player_comparison/?player1=${player1Id}&player2=${player2Id}&tournament=${tournamentId}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    comparisonResult.innerHTML = `<p>Error: ${data.error}</p>`;
                    return;
                }
                
                const player1 = data.player1;
                const player2 = data.player2;
                
                let html = `
                    <div class="comparison-container">
                        <div class="player-stats">
                            <h3>${player1.name} (${player1.team})</h3>
                            <p>Role: ${player1.role}</p>
                            ${player1.stats ? `
                                <h4>Overall Stats</h4>
                                <p>Matches: ${player1.stats.matches}</p>
                                <p>Runs: ${player1.stats.runs}</p>
                                <p>Wickets: ${player1.stats.wickets}</p>
                                <p>Average: ${player1.stats.average}</p>
                                <p>Strike Rate: ${player1.stats.strike_rate}</p>
                                <p>Economy: ${player1.stats.economy}</p>
                            ` : ''}
                            ${player1.tournament_stats ? `
                                <h4>Tournament Stats</h4>
                                <p>Matches: ${player1.tournament_stats.matches}</p>
                                <p>Runs: ${player1.tournament_stats.runs}</p>
                                <p>Wickets: ${player1.tournament_stats.wickets}</p>
                                <p>Average: ${player1.tournament_stats.average}</p>
                                <p>Strike Rate: ${player1.tournament_stats.strike_rate}</p>
                                <p>Economy: ${player1.tournament_stats.economy}</p>
                            ` : ''}
                        </div>
                        <div class="player-stats">
                            <h3>${player2.name} (${player2.team})</h3>
                            <p>Role: ${player2.role}</p>
                            ${player2.stats ? `
                                <h4>Overall Stats</h4>
                                <p>Matches: ${player2.stats.matches}</p>
                                <p>Runs: ${player2.stats.runs}</p>
                                <p>Wickets: ${player2.stats.wickets}</p>
                                <p>Average: ${player2.stats.average}</p>
                                <p>Strike Rate: ${player2.stats.strike_rate}</p>
                                <p>Economy: ${player2.stats.economy}</p>
                            ` : ''}
                            ${player2.tournament_stats ? `
                                <h4>Tournament Stats</h4>
                                <p>Matches: ${player2.tournament_stats.matches}</p>
                                <p>Runs: ${player2.tournament_stats.runs}</p>
                                <p>Wickets: ${player2.tournament_stats.wickets}</p>
                                <p>Average: ${player2.tournament_stats.average}</p>
                                <p>Strike Rate: ${player2.tournament_stats.strike_rate}</p>
                                <p>Economy: ${player2.tournament_stats.economy}</p>
                            ` : ''}
                        </div>
                    </div>
                `;
                
                comparisonResult.innerHTML = html;
            })
            .catch(error => {
                console.error('Error:', error);
                comparisonResult.innerHTML = '<p>An error occurred while comparing players</p>';
            });
    }
    
    // Function to load tournament players
    function loadTournamentPlayers() {
        const tournamentId = tournamentSelect.value;
        const playerType = playerTypeSelect.value;
        
        fetch(`/get_tournament_players/?tournament=${tournamentId}&type=${playerType}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error('Error:', data.error);
                    return;
                }
                
                const players = data.players;
                const playerList = document.getElementById('playerList');
                playerList.innerHTML = '';
                
                players.forEach(player => {
                    const playerDiv = document.createElement('div');
                    playerDiv.className = 'player-card';
                    playerDiv.innerHTML = `
                        <h3>${player.name} (${player.team})</h3>
                        <p>Matches: ${player.matches}</p>
                        <p>Runs: ${player.runs}</p>
                        <p>Wickets: ${player.wickets}</p>
                        <p>Average: ${player.average}</p>
                        <p>Strike Rate: ${player.strike_rate}</p>
                        <p>Economy: ${player.economy}</p>
                    `;
                    playerList.appendChild(playerDiv);
                });
            })
            .catch(error => console.error('Error:', error));
    }
    
    // Event listeners
    document.getElementById('compareButton').addEventListener('click', comparePlayers);
    tournamentSelect.addEventListener('change', loadTournamentPlayers);
    playerTypeSelect.addEventListener('change', loadTournamentPlayers);
    
    // Initial load of tournament players
    loadTournamentPlayers();
}); 