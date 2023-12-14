# WhatsApp-Chat-HTML-Converter
This Python script is designed to transform a WhatsApp chat log, including associated media files, into an interactive HTML document. It provides an easy-to-navigate format for viewing chat histories, complete with embedded media like images, audio, and videos.

## Features
Chat Conversion: Converts a WhatsApp chat log file (_chat.txt) into a formatted HTML document.
Media Embedding: Embeds images, audio, and video files directly into the chat flow, allowing for inline viewing and playback.
Interactive Summary Creation: Users can select specific messages using checkboxes and generate a summary HTML document containing only the chosen messages.
Versioned Output: The script generates HTML files with incremental version numbers to keep track of multiple conversions.

## Usage

1. Prepare Chat and Media Files:
  - Export your WhatsApp chat along with media files. This will typically generate a folder containing a _chat.txt file and various media files.

2. Run the Script:
  - Place the script in a directory separate from your chat and media files.
  - Run the script. When prompted, enter the path to the folder containing your exported WhatsApp chat and media files.

3. View and Interact with HTML:
  - The script will generate an HTML file named after the folder containing the chat log, appended with a version number (e.g., ChatFolder_v0.html).
  - Open this HTML file in a web browser to view the formatted chat.
  - Use checkboxes next to each message to select messages.
  - Click the “Create Summary” button to open a new HTML document with only the selected messages.

4. Summary HTML:
  - The summary HTML is displayed in a new browser window or tab.
  - This document can be saved manually from the browser for record-keeping or sharing.

## Requirements
  - Python environment (Python 3.x recommended).
  - The script must be run in an environment where it can accept input (like a command line or terminal).
  - A web browser for viewing the generated HTML files.

## Notes
  - The script handles paths with spaces and most special characters. Enclose the path in quotes if it contains spaces.
  - Paths should follow the format of the operating system (e.g., backslashes \ on Windows, forward slashes / on Unix-like systems).
  - The generated HTML file is best viewed in modern web browsers that support HTML5.

## To-Do
  - Add the ability to select messages and media and create a "summary" html

## Disclaimer
  - This script is intended for personal use and should be used responsibly and ethically.
  - Ensure that you have the right to convert and view the chat history, respecting the privacy and consent of all parties involved in the chat.
