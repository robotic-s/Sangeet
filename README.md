# Sangeet

# Sangeet - Your Personal Music Universe

Sangeet is a feature-rich music platform that brings a personalized and immersive listening experience to music lovers. Built with Python and Flask on the backend and JavaScript on the frontend, Sangeet offers a range of features to enhance your music journey.

## Features

- **Personalized Music Library**: Build and manage your own music collection.
- **YouTube Integration**: Search and play music directly from YouTube.
- **Dynamic Search**: Find and download songs from various sources.
- **Lyrics Display**: View synchronized lyrics for supported songs.
- **Audio Visualization**: Enjoy beat-synchronized visual effects while listening.
- **Playlist Management**: Create, edit, and shuffle playlists.
- **Listening History**: Keep track of your listening habits and view statistics.
- **Dark Mode**: Toggle between light and dark themes for comfortable viewing.
- **Responsive Design**: Enjoy Sangeet on various devices and screen sizes.
- **Sangeet Radio**: Discover new music with the integrated radio feature.
- **User Authentication**: Secure user accounts and personalized experiences.
- **Embed Sharing**: Share your favorite songs with embedded players.
- **And much more**

## Tech Stack

- Backend: Python, Flask
- Frontend: HTML, CSS, JavaScript
- Database: SQLite
- Audio Processing: yt-dlp, Mutagen
- Authentication: Flask-Login (implied)
- And much more

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/robotic-s/Sangeet.git
   cd sangeet
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Go to the .env file and add all necessary details..



4. Run the application:
   ```
   python sangeet.py
   ```

6. Access Sangeet in your web browser at `http://localhost:80`

## Usage

- Register for an account or log in if you already have one.
- Use the search bar to find songs or paste YouTube links.
- Click on a song to play it, or use the "Add to Library" button for YouTube results.
- Explore features like  listening history, and audio visualizations and much more.
- Adjust settings and toggle dark mode using the buttons in the top right corner.






## Getting Started with Docker

To run SangeetPro using Docker, follow these steps:

1. Pull the Docker image:
   ```
   docker pull universerobotics/sangeetvr1:latest
   ```

2. Create a `.env` file in the same directory where you'll run the Docker command. Add the following environment variables to the file:

   ```
   HOST=your_host
   MAIL=your_mail
   PASS=your_google_app_password
   SPOTIFYID=your_spotify_client_id
   SPOTIFYSECRET=your_spotify_client_secret
   ```

   Replace the values with your actual configuration:
   - `HOST`: Your host, e.g., `localhost:80`, `:4500`, `127.0.0.1:80`, or `192.168.0.1:4500` (include your actual port)
   - `MAIL`: Your email address for sending OTPs
   - `PASS`: Your Google Mail app password
   - `SPOTIFYID`: Your Spotify client ID
   - `SPOTIFYSECRET`: Your Spotify client secret

3. Run the Docker container:
   ```
   docker run -d \
     --name sangeetpro \
     -p same_as_host:80 \
     --env-file .env \
     --restart always \
     universerobotics/sangeetvr1:latest
   ```

   This command does the following:
   - Runs the container in detached mode (`-d`)
   - Names the container "sangeetpro"
   - Maps port 6700 on the host to port 80 in the container
   - Uses the environment variables from the `.env` file
   - Sets the container to always restart
   - Uses the latest version of the SangeetPro image

4. Access the application by opening a web browser and navigating to `http://localhost:6700` (or the appropriate host and port you've configured).

## Troubleshooting

If you encounter any issues, please check the following:
- Ensure Docker is installed and running on your system
- Verify that the `.env` file is in the correct location and contains valid information
- Check that the required ports are not being used by other applications





## Contributing

Contributions to Sangeet are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

Sangeet is a personal project and should not be used as a distributor for music or to charge others for music. Please use Sangeet responsibly and respect all applicable copyright laws and regulations.

## DISCLAIMER:
This project (Sangeet) is for educational and personal use only. It is not intended for commercial use or for violating YouTube's terms of service or any copyright laws. The creator of this project is not responsible for any misuse of this code. By using this code, you agree to use it at your own risk and in compliance with all applicable laws and terms of service. DO NOT use this code to download copyrighted content without permission.
## Acknowledgements

- YouTube for providing the vast library of music
- All open-source libraries used in this project

---

Created with ♪♫ by Sandesh Kumar
