
function showNotification(message, duration = 5000) {
    const notificationPanel = document.getElementById('notification-panel');

    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.innerHTML = `
        <p class="notification-content">${message}</p>
        <button class="close-notification">&times;</button>
    `;

    notificationPanel.appendChild(notification);

    setTimeout(() => {
        notification.classList.add('show');
    }, 100);

    const closeButton = notification.querySelector('.close-notification');
    closeButton.addEventListener('click', () => {
        notification.remove();
    });

    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 5000);
    }, duration);
}


document.addEventListener('DOMContentLoaded', () => {
const resourceButton = document.getElementById('resource-button');
const resourcePanel = document.getElementById('resource-panel');
const closeResourcePanelBtn = document.getElementById('close-resource-panel');

resourceButton.addEventListener('click', toggleResourcePanel);
closeResourcePanelBtn.addEventListener('click', toggleResourcePanel);

let resourceMonitoringInterval;
let lastNetworkUsage = 0;
let lastTimestamp = performance.now();
let networkSamples = [];
let frameTimes = [];
const maxDataPoints = 60; // 1 minute of data at 1 update per second

function toggleResourcePanel() {
resourcePanel.classList.toggle('active');
if (resourcePanel.classList.contains('active')) {
    startResourceMonitoring();
} else {
    stopResourceMonitoring();
}
}

function startResourceMonitoring() {
updateResourceUsage();
resourceMonitoringInterval = setInterval(updateResourceUsage, 1000);
}

function stopResourceMonitoring() {
clearInterval(resourceMonitoringInterval);
}

function updateResourceUsage() {
updateCPUUsage();
updateMemoryUsage();
updateNetworkUsage();
updateDOMNodes();
updateEventListeners();
updateNetworkLatency();
updatePageLoadTime();
}

function updateGraph(graphId, value, maxValue) {
const graph = document.getElementById(graphId);
const bar = document.createElement('div');
bar.style.height = `${(value / maxValue) * 100}%`;
bar.style.width = `${100 / maxDataPoints}%`;
bar.style.backgroundColor = getColorForValue(value / maxValue);
bar.style.float = 'left';

if (graph.childElementCount >= maxDataPoints) {
    graph.removeChild(graph.firstChild);
}

graph.appendChild(bar);
}

function getColorForValue(value) {
if (value < 0.5) return '#4CAF50';
if (value < 0.75) return '#FFC107';
return '#F44336';
}

function updateCPUUsage() {
const cpuUsage = estimateCPUUsage();
document.getElementById('cpu-usage-value').textContent = `${cpuUsage.toFixed(2)}%`;
updateGraph('cpu-usage-graph', cpuUsage, 100);
}

function updateMemoryUsage() {
if (performance.memory) {
    const usedJSHeapSize = performance.memory.usedJSHeapSize / (1024 * 1024);
    const totalJSHeapSize = performance.memory.totalJSHeapSize / (1024 * 1024);
    const usagePercentage = (usedJSHeapSize / totalJSHeapSize) * 100;
    
    document.getElementById('memory-usage-value').textContent = `${usedJSHeapSize.toFixed(2)} MB / ${totalJSHeapSize.toFixed(2)} MB`;
    updateGraph('memory-usage-graph', usagePercentage, 100);
} else {
    document.getElementById('memory-usage-value').textContent = 'Not available';
}
}

function updateNetworkUsage() {
const currentNetworkUsage = performance.getEntriesByType('resource').reduce((total, entry) => total + entry.transferSize, 0);
const currentTimestamp = performance.now();
const timeDiff = (currentTimestamp - lastTimestamp) / 1000; // in seconds
const usage = (currentNetworkUsage - lastNetworkUsage) / timeDiff;

networkSamples.push(usage);
if (networkSamples.length > maxDataPoints) networkSamples.shift();
const averageUsage = networkSamples.reduce((a, b) => a + b, 0) / networkSamples.length;

const usageInMbps = (averageUsage * 8) / (1024 * 1024); // Convert to Mbps
document.getElementById('network-usage-value').textContent = `${usageInMbps.toFixed(2)} Mbps`;
updateGraph('network-usage-graph', usageInMbps, 10); // Adjust max value as needed

lastNetworkUsage = currentNetworkUsage;
lastTimestamp = currentTimestamp;
}

function updateDOMNodes() {
const nodeCount = document.getElementsByTagName('*').length;
document.getElementById('dom-nodes-value').textContent = nodeCount;
updateGraph('dom-nodes-graph', nodeCount, 5000); // Adjust max value as needed
}

function updateEventListeners() {
const approximateListenerCount = estimateEventListeners();
document.getElementById('event-listeners-value').textContent = approximateListenerCount;
updateGraph('event-listeners-graph', approximateListenerCount, 1000); // Adjust max value as needed
}



function updateNetworkLatency() {
const resources = performance.getEntriesByType('resource');
if (resources.length > 0) {
    const totalLatency = resources.reduce((sum, resource) => sum + resource.duration, 0);
    const averageLatency = totalLatency / resources.length;
    document.getElementById('network-latency-value').textContent = `${averageLatency.toFixed(2)} ms`;
    updateGraph('network-latency-graph', averageLatency, 1000); // Adjust max value as needed
} else {
    document.getElementById('network-latency-value').textContent = 'N/A';
}
}

function updatePageLoadTime() {
const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
document.getElementById('page-load-time-value').textContent = `${loadTime.toFixed(2)} ms`;
}

function estimateCPUUsage() {
const start = performance.now();
let count = 0;
while (performance.now() - start < 5) {
    count++;
}
return Math.min((5 / count) * 1000, 100); // Adjust scale as needed
}

function estimateEventListeners() {
let count = 0;
const elements = document.getElementsByTagName('*');
for (let i = 0; i < elements.length; i++) {
    count += getEventListeners(elements[i]).length;
}
return count;
}

function getEventListeners(element) {
const listeners = [];
const allProperties = Object.getOwnPropertyNames(element);
for (let i = 0; i < allProperties.length; i++) {
    if (allProperties[i].startsWith('on')) listeners.push(allProperties[i]);
}
return listeners;
}

// Start monitoring frame rate
requestAnimationFrame(updateFrameRate);
});


document.addEventListener('DOMContentLoaded', function() {
var profilePic = document.getElementById('profile-pic');

profilePic.onerror = function() {
    this.src = '/pic';
};
});


  document.addEventListener('DOMContentLoaded', () => {
    // ... (existing event listeners) ...

    const profilePic = document.getElementById('profile-pic');

    profilePic.addEventListener('click', () => {
        window.open("/authentication/dashboard", "_blank");
    });
});


document.addEventListener('DOMContentLoaded', () => {
const hamburgerMenu = document.querySelector('.hamburger-menu');
const hamburgerIcon = document.querySelector('.hamburger-icon');

hamburgerIcon.addEventListener('click', () => {
hamburgerMenu.classList.toggle('active');
});

// Close menu when clicking outside
document.addEventListener('click', (e) => {
if (!hamburgerMenu.contains(e.target) && hamburgerMenu.classList.contains('active')) {
    hamburgerMenu.classList.remove('active');
}
});

// Prevent menu from closing when clicking inside
hamburgerMenu.addEventListener('click', (e) => {
e.stopPropagation();
});

// Add event listeners for menu items
document.getElementById('filter-button').addEventListener('click', toggleFilterPanel);
document.getElementById('history-button').addEventListener('click', toggleHistoryPanel);
});


function toggleLyrics() {
    const lyricsContainer = document.getElementById('lyrics-container');
    lyricsContainer.style.display = lyricsContainer.style.display === 'none' ? 'block' : 'none';
}

function fetchAndDisplayLyrics(videoId) {
const lyricsContainer = document.getElementById('lyrics-container');
const lyricsContent = document.getElementById('lyrics-content');
const lyricsSource = document.getElementById('lyrics-source');

lyricsContent.textContent = 'Loading lyrics...';
lyricsSource.textContent = '';
lyricsContainer.style.display = 'block';

fetch(`/lyrics/${videoId}`)
.then(response => response.json())
.then(data => {
    if (data.status === 'success') {
        lyricsContent.textContent = data.lyrics;
        lyricsSource.textContent = `By ${data.source}`;
        lyricsContainer.style.display = 'block';
    } else {
        lyricsContainer.style.display = 'none';
    }
})
.catch(error => {
    console.error('Error fetching lyrics:', error);
    lyricsContainer.style.display = 'none';
});
}

// Add event listener for the toggle lyrics button
document.getElementById('toggle-lyrics-btn').addEventListener('click', toggleLyrics);


const NUM_HEADER_BARS = 40; // Increase the number of bars

function createHeaderBeatBars() {
    const container = document.querySelector('.header-beat-container');
    container.innerHTML = '';
    headerBeatBars = [];

    for (let i = 0; i < NUM_HEADER_BARS; i++) {
        const bar = document.createElement('div');
        bar.className = 'header-beat-bar';
        container.appendChild(bar);
        headerBeatBars.push(bar);
    }
}

function updateHeaderBeatBars() {
    if (!audioContext || !analyser || !currentSong || !currentSong.playing()) return;

    analyser.getByteFrequencyData(dataArray);

    const barCount = headerBeatBars.length;
    const highestFrequency = 255;
    const barHeight = 20;

    for (let i = 0; i < barCount; i++) {
        const index = Math.floor(i * analyser.frequencyBinCount / barCount);
        const value = dataArray[index];
        const percent = value / highestFrequency;
        const height = percent * barHeight;
        headerBeatBars[i].style.height = `${height}px`;
        headerBeatBars[i].style.opacity = percent + 0.2;
    }

    requestAnimationFrame(updateHeaderBeatBars);
}


document.addEventListener('DOMContentLoaded', () => {
const includeOutUniverseToggle = document.getElementById('include-out-universe');

includeOutUniverseToggle.addEventListener('change', () => {
localStorage.setItem('includeOutUniverse', includeOutUniverseToggle.checked);
});

// Set initial state
includeOutUniverseToggle.checked = localStorage.getItem('includeOutUniverse') === 'true';
});


let showModePanel;
let isShowModeActive = false;

// Modify the toggleShowModePanel function
function toggleShowModePanel() {
    showModePanel = document.getElementById('show-mode-panel');
    showModePanel.classList.toggle('hidden');
    isShowModeActive = !showModePanel.classList.contains('hidden');
    document.body.classList.toggle('show-mode-active', isShowModeActive);

    if (isShowModeActive) {
        updateShowModeInfo();
    }
}

// Add this function to update the show mode panel information
function updateShowModeInfo() {
    const artwork = document.getElementById('show-mode-artwork');
    const title = document.getElementById('show-mode-title');
    const artist = document.getElementById('show-mode-artist');

    if (currentSong) {
        artwork.src = document.getElementById('full-player-artwork').src;
        title.textContent = document.getElementById('full-player-title').textContent;
        artist.textContent = document.getElementById('full-player-artist').textContent;
    } else {
        artwork.src = '/static/default_artwork.jpg';
        title.textContent = 'No song playing';
        artist.textContent = 'Unknown artist';
    }
}


function checkClipboardForYouTube() {
    if (navigator.clipboard) {
        navigator.clipboard.readText()
            .then(text => {
                if (isYouTubeUrl(text)) {
                    const processedLinks = JSON.parse(localStorage.getItem('processedYouTubeLinks') || '[]');
                    if (!processedLinks.includes(text)) {
                        showYouTubePopup(text);
                    }
                }
            })
            .catch(err => console.error('Failed to read clipboard contents: ', err));
    }
}

function isYouTubeUrl(url) {
    // Regular expression to match YouTube video and shorts URLs
    const youtubeVideoRegex = /^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com\/(?:watch\?v=|shorts\/)|youtu.be\/))([a-zA-Z0-9_-]{11})(\S+)?$/;
    return youtubeVideoRegex.test(url);
}

function showYouTubePopup(url) {
    const popup = document.getElementById('youtube-link-popup');
    const message = document.getElementById('popup-message');
    const randomPrompts = [
        "Ooh, I spotted a YouTube link in your clipboard! Wanna groove to that tune?",
        "Hey there, music maestro! I see you've got a YouTube link copied. Shall we give it a listen?",
        "YouTube link detected! Ready to add some new beats to your Sangeet playlist?",
        "Looks like you've got music on your mind! Want to play that YouTube track you just copied?",
        "I spy with my little eye... a YouTube link! Fancy a musical interlude?"
    ];
    const promptText = randomPrompts[Math.floor(Math.random() * randomPrompts.length)];

    message.textContent = promptText;
    popup.classList.remove('hidden');

    const closeBtn = document.getElementById('close-popup');
    const notNowBtn = document.getElementById('not-now-btn');
    const sureBtn = document.getElementById('sure-btn');

    const addToProcessedLinks = () => {
        const processedLinks = JSON.parse(localStorage.getItem('processedYouTubeLinks') || '[]');
        if (!processedLinks.includes(url)) {
            processedLinks.push(url);
            localStorage.setItem('processedYouTubeLinks', JSON.stringify(processedLinks));
        }
    };

    const closePopup = () => {
        popup.classList.add('hidden');
        addToProcessedLinks();
        closeBtn.removeEventListener('click', closePopup);
        notNowBtn.removeEventListener('click', closePopup);
        sureBtn.removeEventListener('click', handleSure);
    };

    const handleSure = () => {
        initiateYouTubePlayback(url);
        addToProcessedLinks();
        closePopup();
    };

    closeBtn.addEventListener('click', closePopup);
    notNowBtn.addEventListener('click', closePopup);
    sureBtn.addEventListener('click', handleSure);
}
function initiateYouTubePlayback(url) {
    fetch('/play_youtube', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: url }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                console.log('YouTube playback initiated');
                loadSong(data.filename);
                updateSongInfo(data.filename);
            } else {
                console.error('Failed to initiate YouTube playback:', data.message);
            }
        })
        .catch(error => console.error('Error initiating YouTube playback:', error));
}

setInterval(checkClipboardForYouTube, 5000); // Check every 5 seconds

function clearProcessedYouTubeLinks() {
    localStorage.removeItem('processedYouTubeLinks');
}
function closePopup() {
    const popup = document.getElementById('youtube-link-popup');
    popup.classList.add('hidden');

    // Remove event listeners if they exist
    const closeBtn = document.getElementById('close-popup');
    const notNowBtn = document.getElementById('not-now-btn');
    const sureBtn = document.getElementById('sure-btn');

    if (closeBtn) closeBtn.removeEventListener('click', closePopup);
    if (notNowBtn) notNowBtn.removeEventListener('click', closePopup);
    if (sureBtn) sureBtn.removeEventListener('click', handleSure);
}



function getGreeting() {
    const hour = new Date().getHours();
    let greeting, icon, theme, subtext;

    if (hour >= 5 && hour < 12) {
        greeting = "Good Morning, Melody Maker! 🌞";
        icon = "☀️";
        theme = "morning";
        subtext = "Rise and shine! Let's kickstart your day with some ear-candy tunes that'll make your breakfast jealous!";
    } else if (hour >= 12 && hour < 14) {
        greeting = "Good Noon, Rhythm Rockstar! 🕛";
        icon = "🌞";
        theme = "noon";
        subtext = "It's high time for high notes! How about a lunch break symphony to spice up your midday meal?";
    } else if (hour >= 14 && hour < 17) {
        greeting = "Good Afternoon, Harmony Hero! ☀️";
        icon = "🌤️";
        theme = "afternoon";
        subtext = "Feeling that midday slump? Let's pump up the jam and turn your afternoon into a dance-tastic adventure!";
    } else if (hour >= 17 && hour < 21) {
        greeting = "Good Evening, Twilight Troubadour! 🌆";
        icon = "🌆";
        theme = "evening";
        subtext = "As the day winds down, let's wind up some mellow melodies to paint your evening with audible colors!";
    } else {
        greeting = "Good Night, Midnight Maestro! 🌙";
        icon = "🌙";
        theme = "night";
        subtext = "The stars are out, and so are your favorite nocturnal tunes! Time to orchestrate the perfect midnight playlist!";
    }

    return { greeting, icon, theme, subtext };
}

function showGreeting() {
    const { greeting, icon, theme, subtext } = getGreeting();
    const overlay = document.getElementById('greeting-overlay');
    const content = document.getElementById('greeting-content');
    const iconElement = document.getElementById('greeting-icon');
    const textElement = document.getElementById('greeting-text');
    const subtextElement = document.getElementById('greeting-subtext');

    content.className = theme;
    iconElement.textContent = icon;
    iconElement.style.animation = 'wave 2s infinite';
    textElement.textContent = greeting;
    subtextElement.textContent = subtext;

    // Remove the overlay after 6 seconds
    setTimeout(() => {
        overlay.remove();
    }, 6000);
}

document.addEventListener('DOMContentLoaded', showGreeting);



const stars = document.querySelectorAll('.star');
const submitButton = document.getElementById('submitRating');
let selectedRating = 0;

stars.forEach(star => {
    star.addEventListener('click', () => {
        selectedRating = parseInt(star.getAttribute('data-rating'));
        updateStars();
    });
});

function updateStars() {
    stars.forEach(star => {
        const rating = parseInt(star.getAttribute('data-rating'));
        if (rating <= selectedRating) {
            star.classList.add('active');
        } else {
            star.classList.remove('active');
        }
    });
}

submitButton.addEventListener('click', () => {
    if (selectedRating > 0) {
        fetch('/rate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ rating: selectedRating }),
        })
            .then(response => response.json())
            .then(data => {
                shownotification(`Thank you for rating Sangeet ${selectedRating} stars! ${data.message}`);
            })
            .catch((error) => {
                console.error('Error:', error);

            });
    } else {

    }
});


function updateMusicStats() {
    fetch('/music_stats')
        .then(response => response.json())
        .then(data => {
            document.getElementById('total-files').textContent = data.total_files;
            const totalSpaceGB = (data.total_size / (1024 * 1024 * 1024)).toFixed(2);
            document.getElementById('total-space').textContent = `${totalSpaceGB} GB`;
        })
        .catch(error => console.error('Error fetching music stats:', error));
}

function startContinuousUpdate() {
    updateMusicStats(); // Initial update
    setInterval(updateMusicStats, 5000); // Update every 5 seconds
}



// JavaScript code goes here
let currentSong = null;
let playlist = [];
let currentIndex = 0;
let allSongs = [];
let filters = {
    year: [1900, 2023],
    genre: [],
    size: []
};
let listeningHistory = [];
let listeningTrendChart;
let audioContext;
let analyser;
let dataArray;
let beatBars;


let beatContainer;


function renderSongCards(songs) {
    const songsGrid = document.getElementById('songs-grid');
    songsGrid.innerHTML = '';

    songs.forEach(song => {
        const songCard = document.createElement('div');
        songCard.className = 'song-card';
        songCard.dataset.filename = song.filename;

        const artwork = document.createElement('img');
        artwork.src = song.thumbnail;
        artwork.onerror = function () {
            this.src = '/static/default_artwork.jpg';
        };
        artwork.alt = `${song.title} Artwork`;

        const songInfo = document.createElement('div');
        songInfo.className = 'song-info';
        songInfo.innerHTML = `
        <div class="song-title">${song.title}</div>
        <div class="song-artist">${song.artist}</div>
    `;

        songCard.appendChild(artwork);
        songCard.appendChild(songInfo);
        songsGrid.appendChild(songCard);
    });
}
function updateHeaderPlayingState(isPlaying) {
    const logoContainer = document.querySelector('.logo-container');
    if (isPlaying) {
        logoContainer.classList.add('playing');
    } else {
        logoContainer.classList.remove('playing');
    }
}

function loadSong(filename) {
if (currentSong) {
updateListeningHistory(currentSong.seek(), filename);
currentSong.unload();
}

currentSong = new Howl({
src: [`/stream/${filename}`],
format: ['flac'],
html5: true,
preload: true,
buffer: true,
onplay: () => {
    if (audioContext && audioContext.state === 'suspended') {
        audioContext.resume();
    }
    updatePlayButton();
    connectAudioSource();
    updateBeatVisualization();
    updateListeningHistory(0, filename);
    updateProgress();
},
onload: () => {
    updateSongInfo(filename);
    updateProgress();
},
onend: () => {
    updateListeningHistory(currentSong.duration(), filename);
    playNext();
},
onloaderror: (id, error) => {
    showNotification("Something Went Wrong in backned may be server issue error audio not loaded!!");
}
});

currentSong.play();
updatePlayButton();
updateActiveSong(filename);
checkAndFetchYear(filename);
updateHeaderPlayingState(true);

// Fetch lyrics immediately
const videoId = filename.replace('.flac', '');
fetchLyrics(videoId);

// Update Show Mode info if active
if (isShowModeActive) {
updateShowModeInfo();
}
}



function createBeatVisualization() {
    const beatContainer = document.createElement('div');
    beatContainer.className = 'beat-container';
    document.body.appendChild(beatContainer);

    const barCount = Math.min(analyser.frequencyBinCount, 80);
    beatBars = [];

    for (let i = 0; i < barCount; i++) {
        const bar = document.createElement('div');
        bar.className = 'beat-bar';
        bar.style.left = `${(i / barCount) * 100}%`;
        beatContainer.appendChild(bar);
        beatBars.push(bar);
    }
}


function handleAudioError(error) {
    console.error('Audio playback error:', error);
    showNotification('There was an error playing the audio. Please try again or select a different song.');

    // Attempt to recover by resetting the audio context
    if (audioContext) {
        audioContext.close().then(() => {
            audioContext = null;
            initAudio();
        });
    }
}

function optimizedUpdate() {
    updateProgress();
    if (currentSong && currentSong.playing()) {
        // Throttle beat bar updates to roughly match screen refresh rate (e.g., 60fps)
        if (Date.now() - lastBeatUpdate > 16) {
            updateBeatVisualization();
            lastBeatUpdate = Date.now();
        }
    }
    requestAnimationFrame(optimizedUpdate);
}

// Call optimizedUpdate instead of separate update functions
requestAnimationFrame(optimizedUpdate);
function checkBrowserCompatibility() {
    if (!window.AudioContext && !window.webkitAudioContext) {
        showNotification('Your browser does not support the Web Audio API. Please use a modern browser for the best experience.');
        return false;
    }
    if (!window.Howler) {
        shownotification('The Howler.js library is not loaded. Please check your internet connection and refresh the page.');
        return false;
    }
    return true;
}

// Call this function when initializing your app
if (!checkBrowserCompatibility()) {
    // Disable audio features or show a warning
}

// Call this instead of separate update functions
requestAnimationFrame(optimizedUpdate);
function updateAudioInfo() {
    const audioInfo = document.getElementById('audio-info');
    if (!audioInfo) return;

    if (!audioContext || !analyser) {
        audioInfo.innerHTML = '<p>Audio context not initialized</p>';
        return;
    }

    const sampleRate = audioContext.sampleRate;
    const fftSize = analyser.fftSize;
    const frequencyBinCount = analyser.frequencyBinCount;
    const minDecibels = analyser.minDecibels;
    const maxDecibels = analyser.maxDecibels;
    const smoothingTimeConstant = analyser.smoothingTimeConstant;

    let currentState = 'Unknown';
    if (currentSong) {
        currentState = currentSong.playing() ? 'Playing' : 'Paused';
    }

    let volumeLevel = 'Unknown';
    if (gainNode) {
        volumeLevel = Math.round(gainNode.gain.value * 100) + '%';
    }

    audioInfo.innerHTML = `
<h3>Audio System Information</h3>
<p>Audio Context State: ${audioContext.state}</p>
<p>Sample Rate: ${sampleRate} Hz</p>
<p>FFT Size: ${fftSize}</p>
<p>Frequency Bin Count: ${frequencyBinCount}</p>
<p>Analyser Range: ${minDecibels} dB to ${maxDecibels} dB</p>
<p>Smoothing Time Constant: ${smoothingTimeConstant}</p>
<p>Current Playback State: ${currentState}</p>
<p>Volume Level: ${volumeLevel}</p>
`;

    if (currentSong && currentSong._sounds && currentSong._sounds[0]) {
        const sound = currentSong._sounds[0];
        audioInfo.innerHTML += `
    <h3>Current Song Information</h3>
    <p>Duration: ${formatTime(currentSong.duration())}</p>
    <p>Current Time: ${formatTime(currentSong.seek())}</p>
    <p>Playback Rate: ${sound._rate}</p>
    <p>Is Sprite: ${sound._sprite ? 'Yes' : 'No'}</p>
    <p>Loop: ${sound._loop ? 'Yes' : 'No'}</p>
`;
    }
}

function checkAndFetchYear(filename) {
    const yearElement = document.getElementById('song-year');
    if (yearElement && yearElement.textContent === 'Year: Unknown') {
        fetch(`/year/${filename}`)
            .then(response => response.text())
            .then(year => {
                if (year && year !== 'Unknown') {
                    yearElement.textContent = `Year: ${year}`;
                    // Update the year in the song card as well
                    const songCard = document.querySelector(`.song-card[data-filename="${filename}"]`);
                    if (songCard) {
                        const cardYearElement = songCard.querySelector('.song-year');
                        if (cardYearElement) {
                            cardYearElement.textContent = `Year: ${year}`;
                        }
                    }
                }
            })
            .catch(error => console.error('Error fetching year:', error));
    }
}
// Add this function to create a single share button
function createShareButton() {
    const shareButton = document.createElement('button');
    shareButton.className = 'share-button';
    shareButton.innerHTML = '<span class="material-icons">share</span>';
    shareButton.id = 'share-button';
    return shareButton;
}


function fetchLyrics(videoId) {
const lyricsContainer = document.getElementById('lyrics-container');
const lyricsContent = document.getElementById('lyrics-content');
const lyricsSource = document.getElementById('lyrics-source');

lyricsContent.textContent = 'Loading lyrics...';
lyricsSource.textContent = '';
lyricsContainer.style.display = 'block';

fetch(`/lyrics/${videoId}`)
.then(response => response.json())
.then(data => {
    if (data.status === 'success') {
        lyricsContent.textContent = data.lyrics;
        lyricsSource.textContent = `By ${data.source}`;
        lyricsContainer.style.display = 'block';
    } else {
        lyricsContainer.style.display = 'none';
    }
})
.catch(error => {
    console.error('Error fetching lyrics:', error);
    lyricsContainer.style.display = 'none';
});
}
function copyShareLink(shareUrl, filename) {
    const icon = document.querySelector('#share-button .material-icons');

    navigator.clipboard.writeText(shareUrl).then(() => {
        icon.textContent = 'check';
        setTimeout(() => {
            icon.textContent = 'share';
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy: ', err);
    });
}
function initializeFilters(songs) {
    // Year filter
    const years = songs.map(song => song.year).filter(year => year);
    const minYear = Math.min(...years);
    const maxYear = Math.max(...years);

    const yearSlider = document.getElementById('year-slider');
    const yearDisplay = document.getElementById('year-display');

    yearSlider.min = minYear;
    yearSlider.max = maxYear;
    yearSlider.value = maxYear;

    yearDisplay.textContent = `${minYear} - ${maxYear}`;

    yearSlider.addEventListener('input', () => {
        const selectedMaxYear = parseInt(yearSlider.value);
        yearDisplay.textContent = `${minYear} - ${selectedMaxYear}`;
        filters.year = [minYear, selectedMaxYear];
    });

    // Genre filter
    const genres = [...new Set(songs.map(song => song.genre))].filter(genre => genre).sort();
    const genreFilters = document.getElementById('genre-filters');
    genreFilters.innerHTML = genres.map(genre => `
<input type="checkbox" id="genre-${genre}" class="filter-checkbox" value="${genre}">
<label for="genre-${genre}">${genre}</label>
`).join('');

    // File size filter
    const fileSizes = songs.map(song => song.size);
    const minSize = Math.min(...fileSizes);
    const maxSize = Math.max(...fileSizes);

    const sizeRanges = [
        { name: 'Small', max: 10 * 1024 * 1024 },
        { name: 'Medium', max: 50 * 1024 * 1024 },
        { name: 'Large', max: 100 * 1024 * 1024 },
        { name: 'Very Large', max: Infinity }
    ];

    const sizeFilters = document.getElementById('size-filters');
    sizeFilters.innerHTML = sizeRanges
        .filter(range => range.max > minSize)
        .map(range => `
    <input type="checkbox" id="size-${range.name}" class="filter-checkbox" value="${range.name}">
    <label for="size-${range.name}">${range.name}</label>
`).join('');

    // Event listeners for filters
    document.querySelectorAll('#genre-filters input, #size-filters input').forEach(input => {
        input.addEventListener('change', () => {
            if (input.name === 'genre') {
                filters.genre = Array.from(document.querySelectorAll('#genre-filters input:checked')).map(input => input.value);
            } else if (input.name === 'size') {
                filters.size = Array.from(document.querySelectorAll('#size-filters input:checked')).map(input => input.value);
            }
        });
    });

    // Initialize filters object
    filters = {
        year: [minYear, maxYear],
        genre: [],
        size: []
    };
}
function applyFilters() {
    const filteredSongs = allSongs.filter(song => {
        const yearMatch = song.year >= filters.year[0] && song.year <= filters.year[1];
        const genreMatch = filters.genre.length === 0 || filters.genre.includes(song.genre);
        const sizeMatch = filters.size.length === 0 || filters.size.some(range => {
            switch (range) {
                case 'Small': return song.size <= 10 * 1024 * 1024;
                case 'Medium': return song.size > 10 * 1024 * 1024 && song.size <= 50 * 1024 * 1024;
                case 'Large': return song.size > 50 * 1024 * 1024 && song.size <= 100 * 1024 * 1024;
                case 'Very Large': return song.size > 100 * 1024 * 1024;
                default: return false;
            }
        });

        return yearMatch && genreMatch && sizeMatch;
    });

    renderSongCards(filteredSongs);
    toggleFilterPanel();
}

function toggleFilterPanel() {
    document.getElementById('filter-panel').classList.toggle('active');
}

function toggleHistoryPanel() {
    document.getElementById('listening-history-panel').classList.toggle('active');
}


function deleteSong(filename, title) {
    const modal = document.getElementById('delete-confirmation-modal');
    const message = document.getElementById('delete-confirmation-message');
    const confirmButton = document.getElementById('confirm-delete');
    const cancelButton = document.getElementById('cancel-delete');

    message.textContent = `Do you want to remove "${title}" from your Sangeet collection?`;

    modal.style.display = 'block';

    confirmButton.onclick = function () {
        modal.style.display = 'none';
        performDelete(filename);
    }

    cancelButton.onclick = function () {
        modal.style.display = 'none';
    }

    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }
}

function performDelete(filename) {
    fetch('/delete_song', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ filename: filename }),
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Song deleted:', data);
            // Remove the song from the listening history
            listeningHistory = listeningHistory.filter(item => item.filename !== filename);
            // Re-render the listening history
            renderListeningHistory();
            // Remove the song from the playlist if it exists
            const index = playlist.indexOf(filename);
            if (index > -1) {
                playlist.splice(index, 1);
            }
            // If the deleted song was currently playing, stop it and move to the next song
            if (currentSong && currentSong._src === `/stream/${filename}`) {
                currentSong.stop();
                playNext();
            }
            // Refresh the main song grid
            loadPlaylist();
        })
        .catch((error) => {
            console.error('Error deleting song:', error);
            shownotification('Error deleting song. Please try again.');
        });
}

function updatePlayButton() {
    const miniPlayPauseBtn = document.getElementById('mini-play-pause-btn').querySelector('.material-icons');
    const fullPlayPauseBtn = document.getElementById('play-pause-btn').querySelector('.material-icons');
    const isPlaying = currentSong && currentSong.playing();

    miniPlayPauseBtn.textContent = isPlaying ? 'pause' : 'play_arrow';
    fullPlayPauseBtn.textContent = isPlaying ? 'pause' : 'play_arrow';
}

function updateProgress() {
    const miniProgressBar = document.getElementById('mini-progress-bar');
    const fullProgressBar = document.getElementById('full-progress-bar');
    const currentTimeSpan = document.getElementById('current-time');
    const durationSpan = document.getElementById('duration');

    if (currentSong) {
        const seek = currentSong.seek() || 0;
        const duration = currentSong.duration() || 0;
        const progress = (seek / duration) * 100 || 0;

        miniProgressBar.style.width = `${progress}%`;
        fullProgressBar.style.width = `${progress}%`;
        currentTimeSpan.textContent = formatTime(seek);
        durationSpan.textContent = formatTime(duration);


    }

    requestAnimationFrame(updateProgress);
}
function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.floor(seconds % 60);
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
}

function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    else if (bytes < 1048576) return (bytes / 1024).toFixed(2) + ' KB';
    else if (bytes < 1073741824) return (bytes / 1048576).toFixed(2) + ' MB';
    else return (bytes / 1073741824).toFixed(2) + ' GB';
}


document.addEventListener('DOMContentLoaded', createHeaderBeatBars);


function updateShuffleButton(shuffled) {
    const shuffleBtn = document.getElementById('shuffle-btn');
    const icon = shuffleBtn.querySelector('.material-icons');

    if (shuffled) {
        icon.textContent = 'check';
        setTimeout(() => {
            icon.textContent = 'shuffle';
        }, 5000);
    } else {
        icon.textContent = 'shuffle';
    }
}
function updateHeaderPlayingState(isPlaying) {
    const logoContainer = document.querySelector('.logo-container');
    if (isPlaying) {
        logoContainer.classList.add('playing');
    } else {
        logoContainer.classList.remove('playing');
    }
}
function updateShuffleButton(shuffled) {
    const shuffleBtn = document.getElementById('shuffle-btn');
    const icon = shuffleBtn.querySelector('.material-icons');

    if (shuffled) {
        icon.textContent = 'check';
        setTimeout(() => {
            icon.textContent = 'shuffle';
        }, 5000);
    } else {
        icon.textContent = 'shuffle';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    // ... (other initializations)

    const shuffleBtn = document.getElementById('shuffle-btn');
    shuffleBtn.addEventListener('click', () => {
        shufflePlaylist();
    });
});

// Modify the existing loadPlaylist function
// Modify the existing loadPlaylist function
function loadPlaylist() {
    fetch('/all_songs')
        .then(response => response.json())
        .then(songs => {
            allSongs = songs;
            playlist = songs.map(song => song.filename);
            shufflePlaylist(); // Shuffle the playlist initially
            renderSongCards(songs);
            initializeFilters(songs);
        })
        .catch(error => {
            console.error('Error fetching songs:', error);
        });
}

// Modify the shufflePlaylist function
function shufflePlaylist() {
    const currentSongFilename = currentSong ? currentSong._src.split('/').pop() : null;
    let newPlaylist = [...playlist];

    for (let i = newPlaylist.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [newPlaylist[i], newPlaylist[j]] = [newPlaylist[j], newPlaylist[i]];
    }

    // If there's a current song, make sure it's not the first in the new playlist
    if (currentSongFilename && newPlaylist[0] === currentSongFilename) {
        const indexOfCurrent = newPlaylist.findIndex(filename => filename === currentSongFilename);
        [newPlaylist[0], newPlaylist[indexOfCurrent]] = [newPlaylist[indexOfCurrent], newPlaylist[0]];
    }

    playlist = newPlaylist;
    currentIndex = currentSongFilename ? playlist.indexOf(currentSongFilename) : 0;
    updateShuffleButton(true);
    console.log('Playlist shuffled');
}

// Modify the playNext function


// Modify the playPrevious function


// Modify the existing playNext and playPrevious functions


function updateActiveSong(filename) {
    document.querySelectorAll('.song-card').forEach(card => {
        card.classList.toggle('active', card.dataset.filename === filename);
    });
}

function toggleFullPlayer() {
    document.getElementById('full-player').classList.toggle('active');
}

function toggleTheme() {
    document.body.classList.toggle('dark-mode');
    const themeToggle = document.getElementById('theme-toggle').querySelector('.material-icons');

    if (document.body.classList.contains('dark-mode')) {
        themeToggle.textContent = 'brightness_7';
        localStorage.setItem('theme', 'dark');
    } else {
        themeToggle.textContent = 'brightness_4';
        localStorage.setItem('theme', 'light');
    }

    if (listeningTrendChart) {
        updateChartTheme();
    }
}

function updateMarqueeContent(elementId, text) {
    const element = document.getElementById(elementId);
    const repeatElement = document.getElementById(elementId + '-repeat');
    element.textContent = text;
    repeatElement.textContent = text;
}

function resetMarqueeAnimation() {
    const marqueeContents = document.querySelectorAll('.marquee-content');
    marqueeContents.forEach(content => {
        content.style.animation = 'none';
        content.offsetHeight;
        content.style.animation = null;
    });
}

function updateListeningHistory(position, filename) {
    if (currentSong && filename) {
        fetch('/update_history', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                filename: filename,
                position: position,
            }),
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('History updated:', data);
                loadListeningHistory();
            })
            .catch((error) => console.error('Error updating history:', error));
    }
}

function loadListeningHistory() {
    fetch('/listening_history')
        .then(response => response.json())
        .then(history => {
            listeningHistory = history;
            renderListeningHistory();
        })
        .catch((error) => console.error('Error:', error));
}

let displayedHistoryItems = 10;

function renderListeningHistory() {
    const historyList = document.getElementById('history-list');
    historyList.innerHTML = listeningHistory.slice(0, displayedHistoryItems).map(item => {
        const isCurrentlyPlaying = currentSong && currentSong._src === `/stream/${item.filename}`;
        return `
<div class="history-item">
    <img src="/artwork2/${item.filename}" alt="${item.title} Artwork">
    <div class="history-info">
        <div class="history-title">${item.title}</div>
        <div class="history-artist">${item.artist}</div>
        <div class="history-actions">
            <a class="history-stats-link" onclick="showStatsPanel('${item.filename}')">View Stats</a>
            <a class="history-play-link" onclick="playFromHistory(this, '${item.filename}')">
                <span class="play-icon material-icons">play_arrow</span>
                <span class="spinner"></span>
                <span class="error-icon material-icons">error</span>
            </a>
            ${!isCurrentlyPlaying ? `
            <a class="history-delete-link" onclick="deleteSong('${item.filename}', '${item.title.replace("'", "\\'")}')">
                <span class="delete-icon material-icons">delete</span>
            </a>
            ` : ''}
        </div>
    </div>
</div>
`;
    }).join('');

    const viewMoreButton = document.getElementById('view-more-history');
    if (displayedHistoryItems >= listeningHistory.length) {
        viewMoreButton.style.display = 'none';
    } else {
        viewMoreButton.style.display = 'block';
    }
}

function viewMoreHistory() {
    displayedHistoryItems += 10;
    renderListeningHistory();
}

function playFromHistory(element, filename) {
    const playLink = element;
    const playIcon = playLink.querySelector('.play-icon');
    const spinner = playLink.querySelector('.spinner');
    const errorIcon = playLink.querySelector('.error-icon');

    // Hide play icon, show spinner
    playIcon.style.display = 'none';
    spinner.style.display = 'inline-block';
    errorIcon.style.display = 'none';

    const filenameWithoutExt = filename.replace('.flac', '');
    fetch(`/sangeet/playback/history/"${encodeURIComponent(filenameWithoutExt)}"`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Server error');
            }
            return response.json();
        })
        .then(data => {
            console.log('Response from playback:', data);
            // Hide spinner, show play icon
            spinner.style.display = 'none';
            playIcon.style.display = 'inline-block';
            // You can add additional logic here if needed
            // For example, updating the current playing song in the UI
        })
        .catch(error => {
            console.error('Error playing from history:', error);
            // Hide spinner, show error icon
            spinner.style.display = 'none';
            errorIcon.style.display = 'inline-block';
            // Optionally, you can set a timeout to revert to the play icon after a few seconds
            setTimeout(() => {
                errorIcon.style.display = 'none';
                playIcon.style.display = 'inline-block';
            }, 3000);
        });
}

function showStatsPanel(filename) {
    fetch(`/song_stats/${filename}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            document.getElementById('stats-title').textContent = data.title;
            document.getElementById('stats-artist').textContent = data.artist;
            document.getElementById('stats-total-listens').textContent = data.total_listens;
            document.getElementById('stats-total-time').textContent = formatTime(data.total_time);
            document.getElementById('stats-last-listened').textContent = new Date(data.last_listened).toLocaleDateString();
            document.getElementById('stats-last-position').textContent = formatTime(data.last_position);

            const historyList = document.getElementById('stats-history-list');
            historyList.innerHTML = data.history.map(item => `
                <li>
                    <span>${new Date(item.timestamp).toLocaleString()}</span>
                    <span>${formatTime(item.position)}</span>
                </li>
            `).join('');

            document.getElementById('stats-panel').style.display = 'block';
            updateListeningTrendChart(data.history);
        })
        .catch((error) => {
            console.error('Error:', error);
            shownotification('Error loading stats. Please try again.');
        });
}

function closeStatsPanel() {
    document.getElementById('stats-panel').style.display = 'none';
}

function updateListeningTrendChart(history) {
    const ctx = document.getElementById('listening-trend-chart').getContext('2d');

    if (listeningTrendChart) {
        listeningTrendChart.destroy();
    }

    const chartData = processChartData(history);

    listeningTrendChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData.labels,
            datasets: [{
                label: 'Listening Time',
                data: chartData.data,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Listening Time (minutes)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Date'
                    }
                }
            }
        }
    });

    updateChartTheme();
}

function processChartData(history) {
    const data = {};
    history.forEach(item => {
        const date = new Date(item.timestamp).toLocaleDateString();
        data[date] = (data[date] || 0) + item.position / 60; // Convert to minutes
    });

    return {
        labels: Object.keys(data),
        data: Object.values(data)
    };
}

function updateChartTheme() {
    const textColor = document.body.classList.contains('dark-mode') ? '#E0E0E0' : '#2C3E50';
    listeningTrendChart.options.scales.x.ticks.color = textColor;
    listeningTrendChart.options.scales.y.ticks.color = textColor;
    listeningTrendChart.options.plugins.legend.labels.color = textColor;
    listeningTrendChart.update();
}

function handleSeek(e, progressContainer) {
    if (currentSong) {
        const clickPosition = (e.clientX - progressContainer.getBoundingClientRect().left) / progressContainer.offsetWidth;
        const duration = currentSong.duration();
        currentSong.seek(duration * clickPosition);
    }
}


let gainNode;



// Call this function on the first user interaction
document.addEventListener('click', initAudio, { once: true });
// Update the initAudio function
function updateHeaderBeatBars() {
    if (!audioContext || !analyser || !currentSong || !currentSong.playing()) return;

    analyser.getByteFrequencyData(dataArray);

    const containerHeight = document.querySelector('.logo-container').offsetHeight;
    const maxBarHeight = containerHeight * 0.8;

    for (let i = 0; i < NUM_HEADER_BARS; i++) {
        const index = Math.floor(i * analyser.frequencyBinCount / NUM_HEADER_BARS);
        const value = dataArray[index];
        const percent = value / 255;
        const height = percent * maxBarHeight;
        headerBeatBars[i].style.height = `${height}px`;
    }

    requestAnimationFrame(updateHeaderBeatBars);
}
function initAudio() {
    if (audioContext) return;

    const AudioContext = window.AudioContext || window.webkitAudioContext;
    audioContext = new AudioContext();

    analyser = audioContext.createAnalyser();
    analyser.fftSize = 2048;
    const bufferLength = analyser.frequencyBinCount;
    dataArray = new Uint8Array(bufferLength);

    gainNode = audioContext.createGain();

    createBeatVisualization();
    createHeaderBeatBars();
}

// Update the connectAudioSource function
let isBeatBarsEnabled = true; // Start with beat bars enabled

function toggleBeatBars() {
isBeatBarsEnabled = !isBeatBarsEnabled;
const beatContainer = document.querySelector('.beat-container');
const toggleButton = document.getElementById('toggle-beat-bars');

if (isBeatBarsEnabled) {
beatContainer.style.display = 'flex';
toggleButton.querySelector('.material-icons').textContent = 'equalizer';
if (audioContext && analyser && currentSong && currentSong.playing()) {
    updateBeatVisualization();
}
} else {
beatContainer.style.display = 'none';
toggleButton.querySelector('.material-icons').textContent = 'equalizer_off';
}
}

// Modify the existing updateBeatVisualization function
function updateBeatVisualization() {
if (!analyser || !isBeatBarsEnabled) return;

analyser.getByteFrequencyData(dataArray);

for (let i = 0; i < beatBars.length; i++) {
const value = dataArray[i];
const percent = value / 255;
const height = percent * 100;
beatBars[i].style.height = `${height}vh`;
}

if (isBeatBarsEnabled) {
requestAnimationFrame(updateBeatVisualization);
}
}

// Modify the existing connectAudioSource function
function connectAudioSource() {
if (!audioContext) return;

if (currentSong && currentSong._sounds && currentSong._sounds[0] && currentSong._sounds[0]._node) {
const source = audioContext.createMediaElementSource(currentSong._sounds[0]._node);
source.connect(gainNode);
gainNode.connect(analyser);
analyser.connect(audioContext.destination);

if (isBeatBarsEnabled) {
    updateBeatVisualization();
}
} else {
console.error('Unable to connect audio source: currentSong or its properties are undefined');
}
}

// Add event listener for the new toggle button
document.addEventListener('DOMContentLoaded', () => {
// ... (existing code)

const toggleBeatBarsBtn = document.getElementById('toggle-beat-bars');
toggleBeatBarsBtn.addEventListener('click', toggleBeatBars);

// ... (existing code)
});
// Add this function to adjust the volume
function adjustVolume() {
    if (gainNode) {
        // Get the device's volume (ranges from 0 to 1)
        const deviceVolume = audioContext.destination.volume.value;

        // Set the gain value based on the device's volume
        gainNode.gain.value = deviceVolume;
    }
}

// Call the adjustVolume function whenever the device's volume changes
window.addEventListener('volumechange', adjustVolume);




let searchTimeout;

let searchSuggestions = [];




let suggestionsTimeout;


function debounceSearch() {
    clearTimeout(suggestionsTimeout);
    const searchTerm = document.getElementById('search-input').value.trim();

    if (searchTerm.length > 0) {
        suggestionsTimeout = setTimeout(() => {
            fetchSearchSuggestions(searchTerm);
        }, 100);
    } else {
        clearSearchSuggestions();
        toggleHomeAndYouTubeResults(true);
    }
}
function hideYouTubeResults() {
    toggleHomeAndYouTubeResults(true);
}
function performSearch() {
    const searchTerm = document.getElementById('search-input').value.trim();
    if (searchTerm.length > 0) {
        searchYouTube(searchTerm);
        saveSearchQuery(searchTerm);
        clearSearchSuggestions();
    }
}
function fetchSearchSuggestions(query) {
    fetch(`/search_suggestions?query=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(suggestions => {
            searchSuggestions = suggestions;
            displaySearchSuggestions();
        })
        .catch(error => console.error('Error fetching search suggestions:', error));
}

function displaySearchSuggestions() {
    const suggestionsContainer = document.getElementById('search-suggestions');
    suggestionsContainer.innerHTML = '';

    searchSuggestions.forEach(suggestion => {
        const suggestionElement = document.createElement('div');
        suggestionElement.className = 'search-suggestion';
        suggestionElement.textContent = suggestion;
        suggestionElement.addEventListener('click', () => {
            document.getElementById('search-input').value = suggestion;
            searchYouTube(suggestion);
            clearSearchSuggestions();
        });
        suggestionsContainer.appendChild(suggestionElement);
    });

    suggestionsContainer.style.display = searchSuggestions.length > 0 ? 'block' : 'none';
}

function clearSearchSuggestions() {
    const suggestionsContainer = document.getElementById('search-suggestions');
    suggestionsContainer.innerHTML = '';
    suggestionsContainer.style.display = 'none';
}

function saveSearchQuery(query) {
    fetch('/save_search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: query }),
    })
        .catch(error => console.error('Error saving search query:', error));
}

// Update the event listener for the search input
document.getElementById('search-input').addEventListener('input', debounceSearch);

// Add this event listener to handle clicks outside the search suggestions
document.addEventListener('click', (e) => {
    if (!e.target.closest('#search-container')) {
        clearSearchSuggestions();
    }
});

function searchYouTube(searchTerm) {
showLoadingIndicator();
const includeOutUniverse = localStorage.getItem('includeOutUniverse') === 'true';
fetch('/search_youtube', {
method: 'POST',
headers: { 'Content-Type': 'application/json' },
body: JSON.stringify({ 
    search_term: searchTerm,
    include_out_universe: includeOutUniverse
}),
})
.then(response => response.json())
.then(results => {
renderYouTubeResults(results);
hideLoadingIndicator();
toggleHomeAndYouTubeResults(false);
})
.catch(error => {
console.error('Error searching Sangeet universe!', error);
hideLoadingIndicator();
});
}
function renderYouTubeResults(results) {
    const resultsGrid = document.getElementById('youtube-results-grid');
    resultsGrid.innerHTML = '';

    if (results.length === 0) {
        const noResultsMessage = document.createElement('p');
        noResultsMessage.className = 'no-results-message';
        noResultsMessage.textContent = 'Sorry, we couldn\'t find anything for that search. Try adding more information to your query.';
        resultsGrid.appendChild(noResultsMessage);
        return;
    }

    const template = document.getElementById('youtube-result-template');

    results.forEach(result => {
        const songCard = template.content.cloneNode(true).querySelector('.song-card');
        songCard.querySelector('.youtube-thumbnail').src = result.thumbnail;
        songCard.querySelector('.song-title').textContent = result.title;
        songCard.querySelector('.song-artist').textContent = result.author;
        const actionButton = songCard.querySelector('.youtube-result-action');
        actionButton.textContent = result.file_exists ? 'Play Now' : 'Add to Library';
        actionButton.classList.toggle('song-exists', result.file_exists);
        actionButton.addEventListener('click', () => handleYouTubeAction(result.id, actionButton));
        resultsGrid.appendChild(songCard);
    });

    console.log('Rendered YouTube results:', results.length);
}

function handleYouTubeAction(videoId, button) {
    const filename = `${videoId}.flac`;
    if (button.classList.contains('song-exists')) {
        loadSong(filename);
    } else {
        downloadYouTubeAudio(videoId, button, filename);
    }
}

function downloadYouTubeAudio(videoId, button, filename) {
    button.textContent = 'Adding To Sangeet';
    button.classList.add('adding-to-sangeet');
    button.disabled = true;

    fetch('/download_youtube', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ video_id: videoId }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'completed') {
                button.textContent = 'Play Now';
                button.classList.remove('adding-to-sangeet');
                button.disabled = false;
                button.classList.add('song-exists');
                loadPlaylist();
                loadSong(filename);
            } else {
                throw new Error('Download failed');
            }
        })
        .catch(error => {
            console.error('Error downloading:', error);
            button.textContent = 'Error';
            button.classList.remove('adding-to-sangeet');
            button.disabled = false;
            setTimeout(() => {
                button.textContent = 'Add to Library';
            }, 3000);
        });
}
function updateSongInfo(filename) {
fetch(`/metadata/${filename}`)
.then(response => response.json())
.then(metadata => {
    // Update mini player
    updateMarqueeContent('mini-player-title', metadata.title || 'Unknown Title');
    document.getElementById('mini-player-artist').textContent = metadata.artist || 'Unknown Artist';

    const miniPlayerArtwork = document.getElementById('mini-player-artwork');
    miniPlayerArtwork.src = metadata.thumbnail;
    miniPlayerArtwork.onerror = function () {
        this.src = '/static/default_artwork.jpg';
    };

    // Update full player
    updateMarqueeContent('full-player-title', metadata.title || 'Unknown Title');
    document.getElementById('full-player-artist').textContent = metadata.artist || 'Unknown Artist';

    const fullPlayerArtwork = document.getElementById('full-player-artwork');
    fullPlayerArtwork.src = metadata.thumbnail;
    fullPlayerArtwork.onerror = function () {
        this.src = '/static/default_artwork.jpg';
    };

    // Update song details
    document.getElementById('song-title').textContent = `Title: ${metadata.title || 'Unknown'}`;
    document.getElementById('song-artist').textContent = `Artist: ${metadata.artist || 'Unknown'}`;
    document.getElementById('song-album').textContent = `Album: ${metadata.album || 'Unknown'}`;
    document.getElementById('song-year').textContent = `Year: ${metadata.year || 'Unknown'}`;
    document.getElementById('song-genre').textContent = `Genre: ${metadata.genre || 'Unknown'}`;
    document.getElementById('song-bitrate').textContent = `Bitrate: ${metadata.bitrate || 'Unknown'}`;
    document.getElementById('song-sample-rate').textContent = `Sample Rate: ${metadata.sample_rate || 'Unknown'}`;
    document.getElementById('song-channels').textContent = `Channels: ${metadata.channels || 'Unknown'}`;
    document.getElementById('song-file-size').textContent = `File Size: ${formatFileSize(metadata.file_size)}`;
    document.getElementById('song-duration').textContent = `Duration: ${formatTime(metadata.duration)}`;

    // Update download link
    const downloadLink = document.getElementById('song-download');
    downloadLink.href = metadata.download;
    downloadLink.innerHTML = '<i class="material-icons">file_download</i>';
    downloadLink.title = 'Download';
    downloadLink.setAttribute('download', '');

    // Update share button
    let shareButton = document.getElementById('share-button');
    if (!shareButton) {
        shareButton = createShareButton();
        downloadLink.parentNode.insertBefore(shareButton, downloadLink.nextSibling);
    }
    shareButton.onclick = function (e) {
        e.preventDefault();
        copyShareLink(metadata.share, filename);
    };

    // Update show mode info if active
    if (isShowModeActive) {
        updateShowModeInfo();
    }

    // Update song card if it exists
    const songCard = document.querySelector(`.song-card[data-filename="${filename}"]`);
    if (songCard) {
        let yearElement = songCard.querySelector('.song-year');
        if (!yearElement) {
            yearElement = document.createElement('div');
            yearElement.className = 'song-year';
            songCard.querySelector('.song-info').appendChild(yearElement);
        }
        yearElement.textContent = `Year: ${metadata.year || 'Unknown'}`;
    }

    resetMarqueeAnimation();

    // Check and fetch the year if it's unknown
    if (metadata.year === 'Unknown' || !metadata.year) {
        checkAndFetchYear(filename);
    }

    // Set media session metadata
    if ('mediaSession' in navigator) {
        navigator.mediaSession.metadata = new MediaMetadata({
            title: `Sangeet - ${metadata.title}`,
            artist: metadata.artist,
            album: metadata.album,
            artwork: [
                { src: metadata.thumbnail, sizes: '96x96', type: 'image/jpeg' },
                { src: metadata.thumbnail, sizes: '128x128', type: 'image/jpeg' },
                { src: metadata.thumbnail, sizes: '192x192', type: 'image/jpeg' },
                { src: metadata.thumbnail, sizes: '256x256', type: 'image/jpeg' },
                { src: metadata.thumbnail, sizes: '384x384', type: 'image/jpeg' },
                { src: metadata.thumbnail, sizes: '512x512', type: 'image/jpeg' },
            ]
        });
    }
})
.catch(error => {
    console.error('Error fetching metadata:', error);
});
}

// Media session action handlers
function handleMediaSessionAction(action) {
switch (action) {
case 'play':
    togglePlayPause();
    break;
case 'pause':
    togglePlayPause();
    break;
case 'previoustrack':
    playPrevious();
    break;
case 'nexttrack':
    playNext();
    break;
default:
    break;
}
}

// Set up media session action handlers
if ('mediaSession' in navigator) {
navigator.mediaSession.setActionHandler('play', () => handleMediaSessionAction('play'));
navigator.mediaSession.setActionHandler('pause', () => handleMediaSessionAction('pause'));
navigator.mediaSession.setActionHandler('previoustrack', () => handleMediaSessionAction('previoustrack'));
navigator.mediaSession.setActionHandler('nexttrack', () => handleMediaSessionAction('nexttrack'));
}

function togglePlayPause() {
if (currentSong) {
if (currentSong.playing()) {
    currentSong.pause();
} else {
    currentSong.play();
}
} else if (playlist.length > 0) {
loadSong(playlist[currentIndex]);
}
updatePlayButton();

// Update media session playback state
if ('mediaSession' in navigator) {
navigator.mediaSession.playbackState = currentSong && currentSong.playing() ? 'playing' : 'paused';
}
}

function playPrevious() {
currentIndex = (currentIndex - 1 + playlist.length) % playlist.length;
loadSong(playlist[currentIndex]);

// Update media session playback state
if ('mediaSession' in navigator) {
navigator.mediaSession.playbackState = 'playing';
}
}

function playNext() {
currentIndex = (currentIndex + 1) % playlist.length;
loadSong(playlist[currentIndex]);

// Update media session playback state
if ('mediaSession' in navigator) {
navigator.mediaSession.playbackState = 'playing';
}
}

function startCustomCheck() {
function checkCustom() {
fetch('/checkcustom')
    .then(response => response.text())
    .then(data => {
        if (data === "check") {
            fetch('/share')
                .then(response => response.json())
                .then(metadata => {
                    // Check if the shared song is different from the currently playing one
                    if (currentSong && currentSong._src === `/stream/${metadata.filename}`) {
                        console.log('Shared song is the same as the currently playing one. Ignoring.');
                    } else {
                        // Load and play the shared song
                        loadSong(metadata.filename);

                        // Update the UI with the new song information
                        updateSongInfo(metadata.filename);

                        // You might want to update other parts of the UI here
                        // For example, updating the playlist or current song display
                    }
                })
                .catch(error => console.error('Error fetching shared song:', error));
        }
    })
    .catch(error => console.error('Error checking custom:', error))
    .finally(() => {
        // Schedule the next check in 2 seconds
        setTimeout(checkCustom, 2000);
    });
}

// Start the initial check
checkCustom();
}
function toggleHomeAndYouTubeResults(showHome) {
    document.getElementById('songs-grid').style.display = showHome ? 'grid' : 'none';
    document.getElementById('search-results-container').style.display = showHome ? 'none' : 'block';
}
function setCookie(name, value, days) {
    const expires = new Date();
    expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
    document.cookie = name + '=' + value + ';expires=' + expires.toUTCString() + ';path=/';
}

function getCookie(name) {
    const nameEQ = name + "=";
    const ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

document.addEventListener('DOMContentLoaded', () => {
    const cautionPane = document.getElementById('cautionPane');
    const agreementCheckbox = document.getElementById('agreementCheckbox');
    const understandButton = document.getElementById('understandButton');

    // Function to disable all controls except the checkbox and understand button
    function disableControls(disabled) {
        const controls = document.querySelectorAll('button, input, a');
        controls.forEach(control => {
            if (control !== agreementCheckbox && control !== understandButton) {
                control.disabled = disabled;
                if (disabled) {
                    control.style.pointerEvents = 'none';
                } else {
                    control.style.pointerEvents = '';
                }
            }
        });
    }

    // Check if the user has already agreed
    const hasAgreed = getCookie('sangeetAgreed');

    if (!hasAgreed) {
        // Show the caution pane if the user hasn't agreed before
        cautionPane.style.display = 'flex';
        disableControls(true);

        // Enable/disable the continue button based on checkbox state
        agreementCheckbox.addEventListener('change', () => {
            understandButton.disabled = !agreementCheckbox.checked;
        });

        // Hide the caution pane, enable controls, and set cookie when the user agrees and clicks "Continue to Sangeet"
        understandButton.addEventListener('click', () => {
            if (agreementCheckbox.checked) {
                cautionPane.style.display = 'none';
                disableControls(false);
                setCookie('sangeetAgreed', 'true', 365); // Set cookie to expire after 1 year
            }
        });
    } else {
        // If the user has already agreed, don't show the caution pane and enable all controls
        cautionPane.style.display = 'none';
        disableControls(false);
    }
});

function showLoadingIndicator() {
    document.getElementById('loading-indicator').style.display = 'block';
}

function hideLoadingIndicator() {
    document.getElementById('loading-indicator').style.display = 'none';
}

document.addEventListener('DOMContentLoaded', () => {
    loadPlaylist();
    loadListeningHistory();
    initAudio();
    startContinuousUpdate();
    updateAudioInfo();
    startCustomCheck();
    updateProgress();
    const searchInput = document.getElementById('search-input');
    const searchBtn = document.getElementById('search-btn');
    const clearSearchBtn = document.getElementById('clear-search-btn');

    searchInput.addEventListener('input', () => {
        clearSearchBtn.style.display = searchInput.value ? 'block' : 'none';
        debounceSearch();
    });

    clearSearchBtn.addEventListener('click', () => {
        searchInput.value = '';
        clearSearchBtn.style.display = 'none';
        clearSearchSuggestions();
        toggleHomeAndYouTubeResults(true);
    });

    searchBtn.addEventListener('click', performSearch);

    // Handle Enter key in search input
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            performSearch();
        }
    });

    // Prevent closing suggestions when clicking on the input
    searchInput.addEventListener('click', (e) => {
        e.stopPropagation();
    });

    document.addEventListener('click', (e) => {
        if (!e.target.closest('#search-container')) {
            clearSearchSuggestions();
        }
    });

    document.getElementById('mini-player').addEventListener('click', (e) => {
        if (!e.target.closest('.control-btn')) {
            toggleFullPlayer();
        }
    });

    const shuffleBtn = document.getElementById('shuffle-btn');
    shuffleBtn.addEventListener('click', shufflePlaylist);

    const showModeBtn = document.getElementById('show-mode-btn');
    const closeShowModeBtn = document.getElementById('close-show-mode-btn');

    showModeBtn.addEventListener('click', toggleShowModePanel);
    closeShowModeBtn.addEventListener('click', toggleShowModePanel);

    const miniProgressContainer = document.getElementById('mini-progress-container');
    const fullProgressContainer = document.getElementById('full-progress-container');

    miniProgressContainer.addEventListener('click', (e) => handleSeek(e, miniProgressContainer));
    fullProgressContainer.addEventListener('click', (e) => handleSeek(e, fullProgressContainer));

    document.getElementById('mini-play-pause-btn').addEventListener('click', togglePlayPause);

    document.addEventListener('keydown', (e) => {
        if (e.code === 'Space' && e.target !== searchInput) {
            e.preventDefault();
            togglePlayPause();
        } else if (e.code === 'ArrowLeft') {
            playPrevious();
        } else if (e.code === 'ArrowRight') {
            playNext();
        }
    });
    document.getElementById('view-more-history').addEventListener('click', viewMoreHistory);

    document.getElementById('songs-grid').addEventListener('click', (e) => {
        const songCard = e.target.closest('.song-card');
        if (songCard) {
            e.preventDefault();
            const filename = songCard.dataset.filename;
            currentIndex = playlist.indexOf(filename);
            loadSong(filename);
        }
    });

    document.getElementById('theme-toggle').addEventListener('click', toggleTheme);
    document.getElementById('filter-button').addEventListener('click', toggleFilterPanel);
    document.getElementById('close-filter-panel').addEventListener('click', toggleFilterPanel);
    document.getElementById('history-button').addEventListener('click', toggleHistoryPanel);
    document.getElementById('close-history-panel').addEventListener('click', toggleHistoryPanel);
    document.getElementById('close-button').addEventListener('click', toggleFullPlayer);
    document.getElementById('play-pause-btn').addEventListener('click', togglePlayPause);
    document.getElementById('prev-btn').addEventListener('click', playPrevious);
    document.getElementById('next-btn').addEventListener('click', playNext);
    document.getElementById('apply-filters-btn').addEventListener('click', applyFilters);
    document.getElementById('close-stats-panel').addEventListener('click', closeStatsPanel);

    document.getElementById('stats-panel').addEventListener('click', (e) => {
        if (e.target === document.getElementById('stats-panel')) {
            closeStatsPanel();
        }
    });

    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-mode');
        document.getElementById('theme-toggle').querySelector('.material-icons').textContent = 'brightness_7';
    }

    console.log('Music player initialized successfully');
    setInterval(checkClipboardForYouTube, 5000);
    clearProcessedYouTubeLinks();
});


document.addEventListener('DOMContentLoaded', () => {
const settingsButton = document.getElementById('settings-button');
const settingsPanel = document.getElementById('settings-panel');
const closeSettingsBtn = document.getElementById('close-settings-btn');

if (settingsButton && settingsPanel && closeSettingsBtn) {
console.log('Settings elements found');

settingsButton.addEventListener('click', function(e) {
    e.preventDefault();
    console.log('Settings button clicked');
    settingsPanel.classList.toggle('active');
});

closeSettingsBtn.addEventListener('click', function() {
    settingsPanel.classList.remove('active');
});
} else {
console.error('One or more settings elements not found:');
console.error('Settings button:', settingsButton);
console.error('Settings panel:', settingsPanel);
console.error('Close settings button:', closeSettingsBtn);
}
const embedBtn = document.getElementById('embed-btn');
embedBtn.addEventListener('click', () => {
if (currentSong) {
    const hostid = "{{ hostid }}";
// Your existing JavaScript code
const songId = currentSong._src.split('/').pop().replace('.flac', '');
const embedUrl = `${hostid}/v3/embed/details/sangeet/all//${songId}`;
    
    // Open the URL in a new tab
    window.open(embedUrl, '_blank');

    // Visual feedback
    const icon = embedBtn.querySelector('.material-icons');
    const originalText = icon.textContent;
    icon.textContent = 'open_in_new';
    setTimeout(() => {
        icon.textContent = originalText;
    }, 2000);
} else {
    shownotification('No song is currently playing.');
}
});


});
document.addEventListener('DOMContentLoaded', () => {
  
    const cleanupBtn = document.getElementById('cleanup-btn');
    const cleanupConfirmation = document.getElementById('cleanup-confirmation');
    const cleanupNo = document.getElementById('cleanup-no');
    const cleanupYes = document.getElementById('cleanup-yes');
    const cleanupSpinner = document.getElementById('cleanup-spinner');
    const cleanupStatus = document.getElementById('cleanup-status');



    cleanupBtn.addEventListener('click', () => {
        cleanupConfirmation.style.display = 'block';
    });

    cleanupNo.addEventListener('click', () => {
        cleanupConfirmation.style.display = 'none';
    });

    cleanupYes.addEventListener('click', () => {
        cleanupConfirmation.style.display = 'none';
        cleanupSpinner.style.display = 'block';
        cleanupStatus.textContent = 'Cleaning up...';

        fetch('/cleanup', { method: 'POST' })
            .then(response => {
                if (response.ok) {
                    return response.json();
                }
                throw new Error('Cleanup failed');
            })
            .then(data => {
                cleanupStatus.textContent = 'Cleanup successful. Reloading...';
                setTimeout(() => {
                    location.reload(); // Reload the page to reflect changes
                }, 1500);
            })
            .catch(error => {
                cleanupStatus.textContent = 'Error: ' + error.message;
                setTimeout(() => {
                    cleanupSpinner.style.display = 'none';
                }, 2000);
            });
    });
});
