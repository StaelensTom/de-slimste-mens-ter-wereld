// Host Script Management
// Functions to show/hide host introduction scripts and populate player names

function showStartHostScripts() {
	// Show all 3 start scripts in modal
	const scripts = [];
	for (let i = 1; i <= 3; i++) {
		const scriptElement = document.getElementById(`host_script_${i}`);
		if (scriptElement) {
			scripts.push(scriptElement.innerHTML);
		}
	}
	if (scripts.length > 0) {
		openHostScriptModal(scripts);
	}
}

function populateHostScriptPlayerNames(players) {
	// Populate player names in all script sections
	if (!players || players.length < 3) {
		console.warn('Not enough players to populate host script');
		return;
	}
	
	// Script 1 player names
	const player1_1 = document.getElementById('player_name_1_1');
	const player2_1 = document.getElementById('player_name_2_1');
	const player3_1 = document.getElementById('player_name_3_1');
	
	if (player1_1) player1_1.textContent = players[0].name;
	if (player2_1) player2_1.textContent = players[1].name;
	if (player3_1) player3_1.textContent = players[2].name;
	
	// Script 2 player names
	const player1_2 = document.getElementById('player_name_1_2');
	const player2_2 = document.getElementById('player_name_2_2');
	const player3_2 = document.getElementById('player_name_3_2');
	const player2_3 = document.getElementById('player_name_2_3');
	const player3_3 = document.getElementById('player_name_3_3');
	
	if (player1_2) player1_2.textContent = players[0].name;
	if (player2_2) player2_2.textContent = players[1].name;
	if (player3_2) player3_2.textContent = players[2].name;
	if (player2_3) player2_3.textContent = players[1].name;
	if (player3_3) player3_3.textContent = players[2].name;
	
	// Script 3 player names
	const player1_3 = document.getElementById('player_name_1_3');
	
	if (player1_3) player1_3.textContent = players[0].name;
}

function populateInterludeScores(players) {
	// Populate interlude screen with player scores after 3-6-9 round
	if (!players || players.length < 3) {
		console.warn('Not enough players to populate interlude');
		return;
	}
	
	// Calculate scores (subtract initial 60 seconds)
	const scores = players.map((p, idx) => ({
		index: idx,
		name: p.name,
		totalScore: p.points,
		earnedScore: p.points - 60
	}));
	
	// Sort by total score
	scores.sort((a, b) => a.totalScore - b.totalScore);
	
	const lowest = scores[0];
	const middle = scores[1];
	const highest = scores[2];
	
	// Populate individual player scores (earned during 3-6-9)
	const player1Name = document.getElementById('interlude_player1_name');
	const player1Score = document.getElementById('interlude_player1_score');
	const player2Name = document.getElementById('interlude_player2_name');
	const player2Score = document.getElementById('interlude_player2_score');
	const player3Name = document.getElementById('interlude_player3_name');
	const player3Score = document.getElementById('interlude_player3_score');
	
	if (player1Name) player1Name.textContent = players[0].name;
	if (player1Score) player1Score.textContent = players[0].points - 60;
	if (player2Name) player2Name.textContent = players[1].name;
	if (player2Score) player2Score.textContent = players[1].points - 60;
	if (player3Name) player3Name.textContent = players[2].name;
	if (player3Score) player3Score.textContent = players[2].points - 60;
	
	// Populate ranking
	const lowestName = document.getElementById('interlude_lowest_name');
	const lowestScore = document.getElementById('interlude_lowest_score');
	const middleName = document.getElementById('interlude_middle_name');
	const middleScore = document.getElementById('interlude_middle_score');
	const highestName = document.getElementById('interlude_highest_name');
	const highestScore = document.getElementById('interlude_highest_score');
	
	if (lowestName) lowestName.textContent = lowest.name;
	if (lowestScore) lowestScore.textContent = lowest.totalScore;
	if (middleName) middleName.textContent = middle.name;
	if (middleScore) middleScore.textContent = middle.totalScore;
	if (highestName) highestName.textContent = highest.name;
	if (highestScore) highestScore.textContent = highest.totalScore;
	
	// Also populate the lowest player name in script 2
	const lowestName2 = document.getElementById('interlude_lowest_name_2');
	if (lowestName2) lowestName2.textContent = lowest.name;
}

function showOpenDeurIntro() {
	// Show the Open Deur introduction text (script 2)
	const introElement = document.getElementById('interlude_opendeur_intro');
	if (introElement) {
		introElement.style.display = 'block';
		introElement.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
	}
}

function showOpenDeurHostScript() {
	// Show the Open Deur host script in modal
	const scriptElement = document.getElementById('opendeur_host_script');
	if (scriptElement) {
		openHostScriptModal(scriptElement.innerHTML);
	}
}

function populateOpenDeurHostScript(players) {
	// Populate the lowest player name in Open Deur host script
	if (!players || players.length < 3) {
		console.warn('Not enough players to populate Open Deur host script');
		return;
	}
	
	// Find player with lowest score
	const scores = players.map((p, idx) => ({
		index: idx,
		name: p.name,
		totalScore: p.points
	}));
	
	scores.sort((a, b) => a.totalScore - b.totalScore);
	const lowest = scores[0];
	
	// Populate the lowest player name
	const lowestNameElement = document.getElementById('opendeur_lowest_name');
	if (lowestNameElement) {
		lowestNameElement.textContent = lowest.name;
	}
}

function populateInterludePuzzelScores(players) {
	// Populate interlude Puzzel screen with player scores after Open Deur round
	if (!players || players.length < 3) {
		console.warn('Not enough players to populate Puzzel interlude');
		return;
	}
	
	// Sort by total score
	const scores = players.map((p, idx) => ({
		index: idx,
		name: p.name,
		totalScore: p.points
	}));
	
	scores.sort((a, b) => a.totalScore - b.totalScore);
	
	const lowest = scores[0];
	const middle = scores[1];
	const highest = scores[2];
	
	// Populate ranking
	const lowestName = document.getElementById('interlude_puzzel_lowest_name');
	const lowestScore = document.getElementById('interlude_puzzel_lowest_score');
	const middleName = document.getElementById('interlude_puzzel_middle_name');
	const middleScore = document.getElementById('interlude_puzzel_middle_score');
	const highestName = document.getElementById('interlude_puzzel_highest_name');
	const highestScore = document.getElementById('interlude_puzzel_highest_score');
	
	if (lowestName) lowestName.textContent = lowest.name;
	if (lowestScore) lowestScore.textContent = lowest.totalScore;
	if (middleName) middleName.textContent = middle.name;
	if (middleScore) middleScore.textContent = middle.totalScore;
	if (highestName) highestName.textContent = highest.name;
	if (highestScore) highestScore.textContent = highest.totalScore;
}

function showPuzzelIntro() {
	// Show the Puzzel introduction text and advance button
	const introElement = document.getElementById('interlude_puzzel_intro');
	const advanceBtn = document.getElementById('interlude_puzzel_advance_btn');
	
	if (introElement) {
		introElement.style.display = 'block';
		introElement.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
	}
	
	if (advanceBtn) {
		advanceBtn.style.display = 'block';
	}
}

function showPuzzelHostScript() {
	// Show the Puzzel host script in modal
	const scriptElement = document.getElementById('puzzel_host_script');
	if (scriptElement) {
		openHostScriptModal(scriptElement.innerHTML);
	}
}

function showGalerijHostScript() {
	// Show the Galerij host script in modal
	const scriptElement = document.getElementById('galerij_host_script');
	if (scriptElement) {
		openHostScriptModal(scriptElement.innerHTML);
	}
}

function populateGalerijHostScript(players) {
	// Populate the lowest player name in Galerij host script
	if (!players || players.length < 3) {
		console.warn('Not enough players to populate Galerij host script');
		return;
	}
	
	// Find player with lowest score
	const scores = players.map((p, idx) => ({
		index: idx,
		name: p.name,
		totalScore: p.points
	}));
	
	scores.sort((a, b) => a.totalScore - b.totalScore);
	const lowest = scores[0];
	
	// Populate the lowest player name
	const lowestNameElement = document.getElementById('galerij_lowest_name');
	if (lowestNameElement) {
		lowestNameElement.textContent = lowest.name;
	}
}

function showCollectiefGeheugenIntro() {
	const scriptElement = document.getElementById('collectief_geheugen_intro');
	if (scriptElement) {
		openHostScriptModal(scriptElement.innerHTML);
	}
}

function populateCollectiefGeheugenIntro(players) {
	if (!players || players.length < 3) return;
	
	const scores = players.map((p, idx) => ({
		index: idx,
		name: p.name,
		totalScore: p.points
	}));
	
	scores.sort((a, b) => a.totalScore - b.totalScore);
	const lowest = scores[0];
	
	const lowestNameElement = document.getElementById('collectief_geheugen_lowest_name');
	if (lowestNameElement) {
		lowestNameElement.textContent = lowest.name;
	}
}

function populateCollectiefGeheugenOutro(players) {
	if (!players || players.length < 3) return;
	
	const scores = players.map((p, idx) => ({
		index: idx,
		name: p.name,
		totalScore: p.points
	}));
	
	scores.sort((a, b) => a.totalScore - b.totalScore);
	
	const eliminated = scores[0];
	const finalist1 = scores[1];
	const finalist2 = scores[2];
	
	const eliminatedElement = document.getElementById('collectief_geheugen_eliminated_name');
	const finalist1Element = document.getElementById('collectief_geheugen_finalist1_name');
	const finalist2Element = document.getElementById('collectief_geheugen_finalist2_name');
	
	if (eliminatedElement) eliminatedElement.textContent = eliminated.name;
	if (finalist1Element) finalist1Element.textContent = finalist1.name;
	if (finalist2Element) finalist2Element.textContent = finalist2.name;
}

function showFinaleIntro() {
	const scriptElement = document.getElementById('finale_intro');
	if (scriptElement) {
		openHostScriptModal(scriptElement.innerHTML);
	}
}

function populateFinaleIntro(players) {
	if (!players || players.length < 3) return;
	
	// Get finalists (players with finalist flag)
	const finalists = players.filter(p => p.finalist);
	if (finalists.length < 2) return;
	
	// Sort by score
	finalists.sort((a, b) => a.points - b.points);
	
	const player1 = finalists[0];
	const player2 = finalists[1];
	
	const player1NameElement = document.getElementById('finale_player1_name');
	const player1ScoreElement = document.getElementById('finale_player1_score');
	const player2NameElement = document.getElementById('finale_player2_name');
	const player2ScoreElement = document.getElementById('finale_player2_score');
	const startingPlayerElement = document.getElementById('finale_starting_player');
	
	if (player1NameElement) player1NameElement.textContent = player1.name;
	if (player1ScoreElement) player1ScoreElement.textContent = player1.points;
	if (player2NameElement) player2NameElement.textContent = player2.name;
	if (player2ScoreElement) player2ScoreElement.textContent = player2.points;
	if (startingPlayerElement) startingPlayerElement.textContent = player1.name;
}

// Modal System for Host Scripts
let currentHostScripts = [];
let currentScriptIndex = 0;

function openHostScriptModal(scripts) {
	if (!Array.isArray(scripts)) {
		scripts = [scripts];
	}
	
	currentHostScripts = scripts;
	currentScriptIndex = 0;
	
	showCurrentScript();
	
	const modal = document.getElementById('hostScriptModal');
	if (modal) {
		modal.style.display = 'flex';
	}
}

function showCurrentScript() {
	const modalBody = document.getElementById('hostScriptModalBody');
	const prevBtn = document.getElementById('hostScriptPrevBtn');
	const nextBtn = document.getElementById('hostScriptNextBtn');
	const closeBtn = document.getElementById('hostScriptCloseBtn');
	
	if (!modalBody) return;
	
	modalBody.innerHTML = currentHostScripts[currentScriptIndex];
	
	// Show/hide navigation buttons
	if (currentHostScripts.length > 1) {
		if (prevBtn) prevBtn.style.display = currentScriptIndex > 0 ? 'inline-block' : 'none';
		if (nextBtn) nextBtn.style.display = currentScriptIndex < currentHostScripts.length - 1 ? 'inline-block' : 'none';
		if (closeBtn) closeBtn.textContent = currentScriptIndex === currentHostScripts.length - 1 ? 'Sluiten' : 'Alles Sluiten';
	} else {
		if (prevBtn) prevBtn.style.display = 'none';
		if (nextBtn) nextBtn.style.display = 'none';
		if (closeBtn) closeBtn.textContent = 'Sluiten';
	}
}

function navigateHostScript(direction) {
	currentScriptIndex += direction;
	if (currentScriptIndex < 0) currentScriptIndex = 0;
	if (currentScriptIndex >= currentHostScripts.length) currentScriptIndex = currentHostScripts.length - 1;
	
	showCurrentScript();
}

function closeHostScriptModal() {
	const modal = document.getElementById('hostScriptModal');
	if (modal) {
		modal.style.display = 'none';
	}
	currentHostScripts = [];
	currentScriptIndex = 0;
}
