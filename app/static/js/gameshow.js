class Gameshow
{
	constructor(name)
	{
		this.name = name
		this.websocket = io("/", { path: "/socket.io", transports: ["websocket", "polling"], reconnection: true });
		this.websocket.on('connect', (event) => { console.log("Connected"); });
		this.websocket.on('disconnect', (event) => { console.log("Disconnected"); });
		this.websocket.on('error', (event) => { console.log("Error"); });
		this.websocket.on('state', (event) => { this.renderState(event); });
		this.websocket.on('event', (event) => { this.handleMessage(event); });

		this.websocket.connect();
	}

	advanceRound()
	{
		this.websocket.emit("advance_round");
	}

	advanceSubround()
	{
		this.websocket.emit("advance_subround");
	}

	playerAwardPoints(playerIndex, awardedPoints)
	{
		this.websocket.emit("player_award_points", playerIndex, playerAwardPoints);
	}

	playerAdvancePosition(playerIndex, positionAdvancement)
	{
		this.websocket.emit("player_advance_position", playerIndex, positionAdvancement);
	}

	playMainIntro()
	{
		this.websocket.emit("play_main_intro");
	}

	playRoundIntro()
	{
		this.websocket.emit("play_round_intro");
	}

	startGame()
	{
		this.websocket.emit("start_game");
	}

	endGame()
	{
		this.websocket.emit("end_game");
	}

	restartGame()
	{
		if (confirm("Weet je zeker dat je het spel opnieuw wilt starten? Alle voortgang gaat verloren!")) {
			this.websocket.emit("restart_game");
		}
	}

	hostSkipVideo()
	{
		this.websocket.emit("host_skip_video");
	}

	renderState(event)
	{
		console.log("Received state");
		console.log(event);
	}
}