# WhatsApp-Chat-HTML-Converter
This Python script is designed to transform a WhatsApp chat log, including associated media files, into an interactive HTML document. It provides an easy-to-navigate format for viewing chat histories, complete with embedded media like images, audio, and videos.

## Features
Chat Conversion: Converts Android or iOS exported WhatsApp chat log file (_chat.txt) into a formatted HTML document.<br/>
Media Embedding: Embeds images, audio, and video files directly into the chat flow, allowing for inline viewing and playback. Or let you download a non-viewable attachement such doc,pdf etc.<br/>
Versioned Output: The script generates HTML files with incremental version numbers to keep track of multiple conversions.<br/>

## Usage

1. Prepare Chat and Media Files:
  - Export your WhatsApp chat along with media files. This will typically generate a folder containing a _chat.txt file and various media files.
  - This program correctly detects sender(self) based on provided folder name(automatically) or parent folder name(which has to be named as the name of the user who exported chats) in case of both one-to-one and group chats respectively.
  - So the ideal folder structure would be to place the script in a directory right outside your exported folder containing chat(txt) and media files.
    ie    <br />
    BOB(Parent Folder)<br />
    |__ WhatsApp Chat - Alice<br />
    |__ WhatsApp Chat - AB Group<br />
    |__ script.py<br />

2. Run the Script:
  - cd to BOB(Parent Folder)
  - Run as `python3 ./whatsappChatToHTML.py` for Android, or `python3 ./whatsappChatToHTML_iOS.py` for iOS exported chat.
  - Enter folder name `WhatsApp Chat - Alice` or `WhatsApp Chat - AB Group` when prompted
  - Absolute or relative folder paths are untested

3. View and Interact with HTML:
  - The script will generate an HTML file named after the folder containing the chat log, appended with a version number (e.g., ChatFolder_v0.html).
  - Open this HTML file in a web browser to view the formatted chat.

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
