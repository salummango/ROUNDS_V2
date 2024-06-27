document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');

    searchInput.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            const query = searchInput.value;

            if (query.length > 2) {
                fetch(`/search/?query=${encodeURIComponent(query)}`, {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        return response.json();
                    })
                    .then(data => {
                        searchResults.innerHTML = '';
                        if (data.results && data.results.length > 0) {
                            data.results.forEach(team => {
                                let teamHtml = `
                                <div class="card mb-3">
                                    <div class="card-body">
                                        <h5 class="card-title">${team.team_name}</h5>
                                        <p class="card-text">Stadium: ${team.team_stadium}</p>
                                        <p class="card-text">City: ${team.team_city}</p>
                                        <p class="card-text">Status: ${team.team_status}</p>
                                        <h6>Fixtures:</h6>
                                        <ul>`;
                                team.fixtures.forEach(fixture => {
                                    teamHtml += `<li>${fixture.home_team} vs ${fixture.away_team} on ${new Date(fixture.match_date).toLocaleString()}</li>`;
                                });
                                teamHtml += `
                                        </ul>
                                    </div>
                                </div>`;
                                searchResults.innerHTML += teamHtml;
                            });
                        } else {
                            searchResults.innerHTML = '<p>No teams found.</p>';
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        searchResults.innerHTML = '<p>Error fetching results. Please try again.</p>';
                    });
            } else {
                searchResults.innerHTML = '';
            }
        }
    });
});