import os
import html
import glob
from datetime import datetime

def process_line(line, last_sender):
    line = line.strip().replace('\u200e', '')  # Strip whitespace and remove Left-to-Right Mark
    if '] ' in line:
        try:
            timestamp_str, content = line.split('] ', 1)
            timestamp = datetime.strptime(timestamp_str[1:], '%d/%m/%Y, %H:%M:%S')
        except ValueError:
            timestamp, timestamp_str = None, ''
        if content.startswith('.: '):
            sender, message = 'Me', content[3:]
        elif ': ' in content:
            sender, message = content.split(': ', 1)
        else:
            sender, message = last_sender, content
    else:
        timestamp, timestamp_str, sender, message = None, '', last_sender, line

    return timestamp, sender, message, timestamp_str

def is_image(file_name):
    return file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))

def is_audio(file_name):
    return file_name.lower().endswith(('.mp3', '.wav', '.ogg', '.opus'))

def is_video(file_name):
    return file_name.lower().endswith(('.mp4', '.avi', '.mov', '.wmv'))

def create_media_embed(message, subfolder):
    if '<attached:' in message:
        file_name = message.split('<attached: ')[1].split('>')[0]
        file_path = html.escape(os.path.join(subfolder, file_name))
        if is_image(file_name):
            return f'<img src="{file_path}" alt="{file_name}" style="max-width: 100%;">'
        elif is_audio(file_name):
            return f'<audio controls><source src="{file_path}" type="audio/mpeg">Your browser does not support the audio element.</audio>'
        elif is_video(file_name):
            return f'<video controls><source src="{file_path}" type="video/mp4">Your browser does not support the video tag.</video>'
    return html.escape(message)

def get_next_version_number(folder_name):
    existing_files = glob.glob(f'{folder_name}_v*.html')
    max_version = -1
    for file in existing_files:
        version_part = os.path.basename(file).split('_v')[1]
        version_number = int(version_part.split('.html')[0])
        if version_number > max_version:
            max_version = version_number
    return max_version + 1

def main():
    subfolder = input("Enter the path to the subfolder containing the chat and media files: ")
    folder_name = os.path.basename(os.path.normpath(subfolder))
    chat_file_path = os.path.join(subfolder, '_chat.txt')

    version_number = get_next_version_number(folder_name)
    output_html_path = f'{folder_name}_v{version_number}.html'

    with open(chat_file_path, 'r', encoding='utf-8') as chat_file:
        lines = chat_file.readlines()

    html_content = '''
<html>
<head>
<style>
body {font-family: Arial, sans-serif; margin: 0; padding: 10px;}
.date {text-align: center; color: #555; margin: 20px 0;}
.bubble {border-radius: 20px; padding: 10px 20px; margin: 2px 10px; display: inline-block; max-width: 70%;}
.me {background-color: #DCF8C6; align-self: flex-end; text-align: right;}
.other {background-color: #E5E5EA; text-align: left;}
.sender {font-weight: bold;}
.timestamp {font-size: 0.8em; color: #999;}
.me .timestamp {text-align: right;}
.left {text-align: left;}
.right {text-align: right;}
</style>
<script>
function createSummary() {
    var selectedMessages = document.querySelectorAll('input[name="selected_messages"]:checked');
    var summaryContent = '<html><head><style>/* same CSS styles */</style></head><body>';

    selectedMessages.forEach(function(msg) {
        var messageDiv = msg.closest('.bubble').outerHTML;
        summaryContent += '<div class="bubble">' + messageDiv + '</div>';
    });

    summaryContent += '</body></html>';

    var summaryWindow = window.open('');
    summaryWindow.document.write(summaryContent);
    summaryWindow.document.close();
}
</script>
</head>
<body>
<button onclick="createSummary()">Create Summary</button><br/><br/>
'''

    last_date = None
    last_sender = None
    message_id = 0
    for line in lines:
        timestamp, sender, message, timestamp_str = process_line(line, last_sender)
        message = create_media_embed(message, subfolder)
        message_id += 1

        if timestamp and (last_date is None or timestamp.date() != last_date):
            html_content += f'<div class="date">{timestamp.strftime("%d %B %Y")}</div>'
            last_date = timestamp.date()

        css_class = 'me' if sender == 'Me' else 'other'
        alignment_class = 'right' if sender == 'Me' else 'left'
        html_content += f'''
<div class="{alignment_class}">
    <div class="bubble {css_class}">
        <input type="checkbox" id="msg_{message_id}" name="selected_messages" value="msg_{message_id}">
        <label for="msg_{message_id}">
            <div class="sender">{html.escape(sender)}</div>
            {message}
            <div class="timestamp">{timestamp_str if timestamp else ''}</div>
        </label>
    </div>
</div>
'''
        last_sender = sender

    html_content += '</body></html>'

    with open(output_html_path, 'w', encoding='utf-8') as output_file:
        output_file.write(html_content)

    print(f'HTML file created: {output_html_path}')

if __name__ == '__main__':
    main()
