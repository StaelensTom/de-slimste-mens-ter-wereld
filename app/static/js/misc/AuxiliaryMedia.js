class AuxiliaryMedia {
	static currentVideoUrl = null;
	
	static renderState(state) {
		let container = document.getElementById("container_auxiliaryMedia");
		container.classList.add("d-none");
		
		// Hide play button by default
		let playButton = document.getElementById("play_video_button");
		playButton.classList.add("d-none");

		if (state.current_question == null) {
			this.currentVideoUrl = null;
			return;
		}

		if (!("image" in state.current_question) && !("video" in state.current_question)) {
			this.currentVideoUrl = null;
			return;
		}

		if (state.current_question.image != null | state.current_question.video != null) {
			if ([ "Galerij" ].includes(state.current_round_text) && state.turn_history.length == 1 && !state.timer_running && !host) {
				return;
			}

			container.classList.remove("d-none");
		}

		let auxiliaryMediaElement = document.getElementById("auxiliaryMedia");
		if (state.current_question.image != null) {
			// Check if image is a URL (starts with http/https) or a local file
			if (state.current_question.image.startsWith('http')) {
				// External URL - use directly
				auxiliaryMediaElement.src = state.current_question.image;
			} else {
				// Local file - construct path with questions directory
				const questionsDir = state.questions_directory || 'default';
				auxiliaryMediaElement.src = `/resources/${questionsDir}/${state.current_question.image}`;
			}
		} else {
			auxiliaryMediaElement.src = "";
		}
		
		// Show play button if there's a video (for Collectief geheugen)
		if (state.current_question.video != null && state.current_round_text === "Collectief geheugen") {
			this.currentVideoUrl = state.current_question.video;
			playButton.classList.remove("d-none");
		} else {
			this.currentVideoUrl = null;
		}
	}
	
	static playVideoFromButton() {
		// Play video from the play button (for Collectief geheugen)
		if (this.currentVideoUrl) {
			this.playVideo(this.currentVideoUrl);
			// Hide play button after clicking
			let playButton = document.getElementById("play_video_button");
			playButton.classList.add("d-none");
		}
	}
	
	static playVideo(filename) {
		// Check if it's a YouTube URL
		const youtubeId = this.extractYouTubeId(filename);
		
		if (youtubeId) {
			// Use YouTube iframe in container
			let container = document.getElementById("auxiliaryMedia_youtube_container");
			let iframe = document.getElementById("auxiliaryMedia_youtube");
			
			if (!host) {
				container.classList.remove("d-none");
				iframe.src = `https://www.youtube.com/embed/${youtubeId}?autoplay=1`;
			}
			
			// Show host skip button
			if (host) {
				let hostBtn = document.getElementById("host_skip_video_btn");
				if (hostBtn) hostBtn.classList.remove("d-none");
			}
		} else {
			// Use regular video element for local files
			if (!host) {
				let auxiliaryMediaElementVideo = document.getElementById("auxiliaryMedia_video");
				auxiliaryMediaElementVideo.classList.remove("d-none");
				auxiliaryMediaElementVideo.src = `resources/${filename}`;
				auxiliaryMediaElementVideo.play();

				auxiliaryMediaElementVideo.onended = () => { 
					auxiliaryMediaElementVideo.classList.add("d-none");
					this.hideHostSkipButton();
				};
			}
			
			// Show host skip button
			if (host) {
				let hostBtn = document.getElementById("host_skip_video_btn");
				if (hostBtn) hostBtn.classList.remove("d-none");
			}
		}
	}
	
	static closeVideo() {
		// Close YouTube video
		let container = document.getElementById("auxiliaryMedia_youtube_container");
		let iframe = document.getElementById("auxiliaryMedia_youtube");
		
		container.classList.add("d-none");
		iframe.src = ""; // Stop video playback
		
		// Close regular video
		let video = document.getElementById("auxiliaryMedia_video");
		video.classList.add("d-none");
		video.pause();
		video.src = "";
		
		// Hide host skip button
		this.hideHostSkipButton();
	}
	
	static hideHostSkipButton() {
		let hostBtn = document.getElementById("host_skip_video_btn");
		if (hostBtn) hostBtn.classList.add("d-none");
	}
	
	static extractYouTubeId(url) {
		if (!url) return null;
		const patterns = [
			/(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\?\/]+)/,
			/youtube\.com\/shorts\/([^&\?\/]+)/, // YouTube Shorts support
			/^([a-zA-Z0-9_-]{11})$/ // Direct video ID
		];
		for (const pattern of patterns) {
			const match = url.match(pattern);
			if (match) return match[1];
		}
		return null;
	}
}