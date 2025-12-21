class DeSlimsteMens extends Gameshow {
	constructor() {
		super();

		this.websocket.on('points_awarded', (pointsAwarded) => { 
			this.pointsAwarded(pointsAwarded); });
		this.websocket.on('clock_start', () => { 
			this.clockStarted(); });
		this.websocket.on('clock_stop', () => { 
			this.clockStopped(); });
		this.websocket.on('video', (filename) => { 
			AuxiliaryMedia.playVideo(filename); });
		this.websocket.on('play_main_intro_client', () => { 
			this.playMainIntroClient(); });
		this.websocket.on('play_round_intro_client', (roundText) => { 
			this.playRoundIntroClient(roundText); });
		this.websocket.on('close_video_all', () => { 
			AuxiliaryMedia.closeVideo(); });

		this._currentSubroundText = null;

		this.scoreDomBuilt = false;

		this.scores = new Scores();

		this.latestState = null;
	}

	renderState(state) {
		// First state render
		if (this.latestState == null) {
			this.latestState = state;

			// We need to make a timer so we can cancel it, basically
			this.setupTimer();

			// Timer could have started before we loaded the page!
			if (state.timer_running) {
				this.timer.start();
			}
			
			// Populate host script with player names (host only)
			if (host && state.players) {
				populateHostScriptPlayerNames(state.players);
			}
		}

		// Detect game start - automatic intro disabled, use manual intro buttons instead
		// if (!this.latestState.running && state.running && !host) {
		// 	Bumper.playBumper("De Slimste Mens Ter Wereld", true);
		// 	Sound.playSound("intro");
		// }

		// Detect game win
		if (this.latestState.running && !state.running && !host) {
			Sound.playSound("finale");
		}

		// Detect round change
		// Skip bumper/sound for interlude screens (they have their own manual trigger)
		if ((this.latestState.current_round_text != state.current_round_text) && !host) {
			if (!state.current_round_text.startsWith("Interlude_")) {
				Bumper.playBumper(state.current_round_text);
				Sound.playSound("bumper");
			}
		}
		
		// Update data-round attribute for CSS styling
		if (this.latestState.current_round_text != state.current_round_text) {
			const gameContainer = document.querySelector('.game');
			if (gameContainer && state.current_round_text) {
				gameContainer.setAttribute('data-round', state.current_round_text);
			}
		}

		// If the clock has been stopped server side (this is possible when all answers were found),
		// we need to stop our local clock
		if (!state.timer_running && this.timer.running) {
			this.clockStopped();
		}

		// Save the latest state
		this.latestState = state;

		// Pass to super method
		super.renderState(state);

		// Debug - hide interlude round names from display
		const displayRoundText = state.current_round_text.startsWith("Interlude_") ? "" : state.current_round_text;
		document.getElementById("currentround").innerHTML = displayRoundText;

		// Hide all rounds...
		let roundContainers = document.getElementsByClassName("round");
		let currentRound = state.current_round_text;
		// Only render the game if it is running
		Array.from(roundContainers).forEach(roundContainer => roundContainer.classList.remove("current"));
		if (!state.running) {
			currentRound = "start";
		}

		// ..then only show the current one
		// or render game start if host
		document.getElementById(`round_${currentRound}`).classList.add("current");

		document.body.classList.remove("unadvanced");
		// Add a specific class if to_advance is not null
		if (state.to_advance != null) {
			document.body.classList.add("unadvanced");
		}

		document.body.classList.remove("clocktogglevisible");
		// Add a specific class if clock toggle is visible
		if (state.clock_visible) {
			document.body.classList.add("clocktogglevisible");
		}

		// Round-specific rendering
		switch (state.current_round_text) {
			case "3-6-9":
				ThreeSixNine.renderState(state);
				break;
			case "Interlude_Open_deur":
				// Populate interlude scores when entering this round
				if (host) {
					populateInterludeScores(state.players);
				}
				break;
			case "Open deur":
				OpenDeur.renderState(state);
				Answers.renderAnswers(state);
				// Populate host script for Open Deur (but don't auto-show)
				if (host) {
					populateOpenDeurHostScript(state.players);
				}
				break;
			case "Interlude_Puzzel":
				// Hide Open Deur elements explicitly
				const questioneersElement = document.getElementById("round_Open deur_questioneers");
				const answersElement = document.getElementById("round_Open deur_answers");
				if (questioneersElement) questioneersElement.classList.add("d-none");
				if (answersElement) answersElement.classList.add("d-none");
				
				// Hide host script button
				if (host) {
					const hostScriptSection = document.getElementById('opendeur_host_script_section');
					if (hostScriptSection) hostScriptSection.style.display = 'none';
				}
				
				// Populate interlude scores when entering this round
				if (host) {
					populateInterludePuzzelScores(state.players);
				}
				break;
			case "Puzzel":
				Puzzel.renderState(state);
				Answers.renderAnswers(state);
				break;
			case "Galerij":
				Galerij.renderState(state);
				Answers.renderAnswers(state);
				// Populate host script only on first photo (subround 0)
				if (host && state.current_subround === 0) {
					populateGalerijHostScript(state.players);
				}
				break;
			case "Collectief geheugen":
				CollectiefGeheugen.renderState(state);
				Answers.renderAnswers(state);
				// Show intro section only on first video (subround 0)
				if (host) {
					const introSection = document.getElementById('collectief_geheugen_intro_section');
					const outroSection = document.getElementById('collectief_geheugen_outro_section');
					
					if (state.current_subround === 0) {
						if (introSection) introSection.style.display = 'block';
						if (outroSection) outroSection.style.display = 'none';
						populateCollectiefGeheugenIntro(state.players);
					} else {
						if (introSection) introSection.style.display = 'none';
					}
					
					// Show outro section after last video (when to_advance is set)
					if (state.to_advance === 'round') {
						if (outroSection) outroSection.style.display = 'block';
						populateCollectiefGeheugenOutro(state.players);
					}
				}
				break;
			case "Finale":
				Finale.renderState(state);
				Answers.renderAnswers(state);
				// Show intro section only on first question (subround 0)
				if (host) {
					const introSection = document.getElementById('finale_intro_section');
					
					if (state.current_subround === 0) {
						if (introSection) introSection.style.display = 'block';
						populateFinaleIntro(state.players);
					} else {
						if (introSection) introSection.style.display = 'none';
					}
				}
				break;
		}

		// Render scores
		// The second argument will block score updating if the timer is running
		this.scores.renderState(state, !this.timer.running);

		// Toggle the clock button UI
		// "Start klok" and "Stop klok"
		this.setClockUI(state.timer_running);

		// Render auxiliary media (if necessary)
		AuxiliaryMedia.renderState(state);

		// Host/client-specific rendering
		if (host)
		{
			this.renderStateHost(state);
		}
		else
		{
			this.renderStateGame(state);
		}
	}

	renderStateHost(state) {

	}

	renderStateGame(state) {

	}

	/* Communication */
	correct(answerValue = null)
	{
		this.websocket.emit("answer_correct", answerValue);
	}

	pass()
	{
		this.websocket.emit("answer_pass");
	}

	openDeurChoose(questioneerIndex) {
		this.websocket.emit("open_deur_choose", questioneerIndex);
	}

	pointsAwarded(pointsAwarded) {
		if (this.latestState.current_round_text != "Finale" && pointsAwarded != null) {
			this.timer.currentPoints += pointsAwarded;
			this.timer.tick(false);
		}

		if (!host && pointsAwarded != null) {
			Sound.playSound("correct");
		}
	}

	setupTimer() {
		this.timer = new Timer(this.scores,
							   this.latestState.active_player_index,
							   this.latestState.active_player.points);
	}

	clockStart() {
		this.websocket.emit("clock_start");
	}

	clockStarted() {
		this.setupTimer();
		this.timer.start();
	}

	clockStop() {
		this.websocket.emit("clock_stop");
	}

	clockStopped() {
		this.timer.stop();
	}

	clockToggle() {
		this.websocket.emit("clock_toggle");
	}

	setClockUI(timer_running) {
		document.getElementById("button_clock_toggle").innerHTML = 
			timer_running ? "Stop klok" : "Start klok";
	}

	releaseAdvance() {
		this.websocket.emit("release_advance");
	}

	playMainIntroClient() {
		if (!host) {
			Bumper.playBumper("De Slimste Mens Ter Wereld", true);
			Sound.playSound("intro");
		}
	}

	playRoundIntroClient(roundText) {
		if (!host) {
			Bumper.playBumper(roundText);
			Sound.playSound("bumper");
		}
	}
	
	playOpenDeurInterlude() {
		// Trigger Open Deur intro from interlude screen (host only)
		if (host) {
			// Show the Open Deur intro text
			showOpenDeurIntro();
			
			// Broadcast intro to all clients
			this.websocket.emit('play_round_intro', 'Open deur');
		}
	}
	
	playPuzzelInterlude() {
		// Trigger Puzzel intro from interlude screen (host only)
		if (host) {
			// Broadcast intro to all clients and advance to Puzzel round
			this.websocket.emit('play_round_intro', 'Puzzel');
		}
	}
}

dsmtw = new DeSlimsteMens();