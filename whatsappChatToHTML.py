import os
import html
import glob
from datetime import datetime

def detect_date_format(timestamps):
    formats = [
        '%d/%m/%Y, %H:%M:%S',  # Common format
        '%m/%d/%Y, %H:%M:%S',  # Common format
        '%Y/%m/%d, %H:%M:%S',  # Common format
        '%d/%m/%Y, %H:%M',  # Common format
        '%m/%d/%Y, %H:%M',  # Common format
        '%Y/%m/%d, %H:%M',  # Common format
        '%d/%m/%y, %H:%M',  # for Android
        '%m/%d/%y, %H:%M',  # for Android
        '%Y-%m-%d, %H:%M:%S',  # Provided format
        '%Y-%m-%dT%H:%M:%S',  # ISO 8601
        '%Y-%m-%dT%H:%M:%S.%f',  # ISO 8601 with microseconds
        '%d-%b-%Y, %H:%M:%S',  # Example: '07-Jan-2024, 08:47:05'
        '%d-%b-%y, %H:%M:%S',  # Example: '07-Jan-24, 08:47:05'
        '%d %b %Y, %H:%M:%S',  # Example: '07 Jan 2024, 08:47:05'
        '%d %b %y, %H:%M:%S'  # Example: '07 Jan 24, 08:47:05'
    ]
    for fmt in formats:
        valid_count = 0
        for timestamp_str in timestamps:
            try:
                datetime.strptime(timestamp_str, fmt)
                valid_count += 1
            except ValueError:
                pass
        if valid_count == len(timestamps):
            return fmt
    return None

def extract_timestamps(lines):
    timestamps = []
    for line in lines:
        line = line.strip().replace('\u200e', '').replace('\u202f', '')
        if line.startswith("[") and "]" in line:
            timestamp_str = line.split('] ', 1)[0].replace('[', '')
            timestamps.append(timestamp_str)
        elif ' - ' in line and ': ' in line:  # for Android
            timestamp_str = line.split(' - ', 1)[0]
            timestamps.append(timestamp_str)
    return timestamps

def extract_names(lines):
    names = set()
    for line in lines:
        line = line.strip().replace('\u200e', '').replace('\u202f', '')
        if line.startswith("[") and "]" in line:
            try:
                content = line.split('] ', 1)[1]
                if ': ' in content:
                    sender = content.split(': ', 1)[0]
                    if not sender.startswith('.'):
                        names.add(sender)
            except IndexError:
                continue
    return sorted(names)

def process_message(message_lines, last_sender, date_format, my_name):
    first_line = message_lines[0].strip().replace('\u200e', '').replace('\u202f', '')
    rest_of_message = "\n".join(message_lines[1:]).strip()

    if first_line.startswith("[") and "]" in first_line:
        timestamp_str, content = first_line.split('] ', 1)
        timestamp_str = timestamp_str.replace('[', '')
    elif first_line.startswith(tuple(f'{m}/' for m in range(1, 13))) and ' - ' in first_line and ': ' in first_line:  # for Android
        timestamp_str, content = first_line.split(' - ', 1)
    else:
        timestamp_str, content = None, first_line

    if timestamp_str:
        try:
            timestamp = datetime.strptime(timestamp_str, date_format)
            if content.startswith('.:'):
                sender = my_name
                message = content[3:]
            else:
                sender, message = content.split(': ', 1)
            message = f"{message}\n{rest_of_message}" if rest_of_message else message
        except ValueError:
            timestamp, timestamp_str, sender, message = None, '', last_sender, first_line + "\n" + rest_of_message if rest_of_message else first_line
    else:
        timestamp, timestamp_str, sender, message = None, '', last_sender, first_line + "\n" + rest_of_message if rest_of_message else first_line

    return timestamp, sender.strip(), message.strip(), timestamp_str

def is_image(file_name):
    return file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))

def is_audio(file_name):
    return file_name.lower().endswith(('.mp3', '.wav', '.ogg', '.opus'))

def is_video(file_name):
    return file_name.lower().endswith(('.mp4', '.avi', '.mov', '.wmv'))

def is_pdf(file_name):
    return file_name.lower().endswith('.pdf')

def create_media_embed(message, subfolder, senderclass):
    if message.lower() == 'null':
        # Determine call icon based on senderclass
        call_icon = '📞 Incoming call' if senderclass == 'other' else '📞 Outgoing call'
        return f'<div class="call-icon">{call_icon}</div>'
    if '(file attached)' in message or '<attached:' in message:  # for both Android and iOS
        if '(file attached)' in message:  # for Android
            file_name = message.split(' (file attached)')[0]
        else:  # for iOS
            file_name = message.split('<attached: ')[1].split('>')[0]
        file_path = html.escape(os.path.join(subfolder, file_name))
        if is_image(file_name):
            return f'<img src="{file_path}" alt="{file_name}" style="max-width: 100%;">'
        elif is_audio(file_name):
            return f'<audio controls><source src="{file_path}" type="audio/mpeg">Your browser does not support the audio element.</audio>'
        elif is_video(file_name):
            return f'<video controls><source src="{file_path}" type="video/mp4">Your browser does not support the video tag.</video>'
        elif is_pdf(file_name):
            return f'''
<object data="{file_path}" type="application/pdf" width="450px" height="700px">
    <p>Unable to display PDF file. <a href="{file_path}">Download</a> instead.</p>
</object>
'''
        else:
            return f'<a href="{file_path}">{html.escape(file_name)}</a> (file attached)'
    return html.escape(message).replace('\n', '<br>')

def get_next_version_number(folder_name):
    existing_files = glob.glob(f'{folder_name}_v*.html')
    max_version = -1
    for file in existing_files:
        version_part = os.path.basename(file).split('_v')[1]
        version_number = int(version_part.split('.html')[0])
        if version_number > max_version:
            max_version = version_number
    return max_version + 1

def get_message_start_lines(lines):
    start_lines = []
    for i, line in enumerate(lines):
        line = line.strip().replace('\u200e', '')
        if line.startswith("[") and "]" in line:
            start_lines.append(i)
        elif line.startswith(tuple(f'{m}/' for m in range(1, 13))) and ' - ' in line and ': ' in line:  # Android-specific
            start_lines.append(i)
    return start_lines

def main():
    # List subfolders in the current directory
    subfolders = [f.name for f in os.scandir(os.getcwd()) if f.is_dir()]
    valid_subfolders = []

    for folder in subfolders:
        folder_path = os.path.join(os.getcwd(), folder)
        chat_file_path_ios = os.path.join(folder_path, '_chat.txt')
        chat_file_path_android = os.path.join(folder_path, folder + '.txt')

        if os.path.isfile(chat_file_path_ios) or os.path.isfile(chat_file_path_android):
            valid_subfolders.append(folder)

    if not valid_subfolders:
        print("No valid subfolders found.")
        return

    attempts = 0
    while attempts < 2:
        print("Select a subfolder containing the chat and media files:")
        for idx, folder in enumerate(valid_subfolders):
            print(f"{idx + 1}. {folder}")

        try:
            folder_idx = int(input("Enter the number of the folder (or press Ctrl+C to interrupt): ")) - 1
            if folder_idx < 0 or folder_idx >= len(valid_subfolders):
                raise ValueError("Invalid selection.")
            subfolder = valid_subfolders[folder_idx]
            break
        except ValueError:
            attempts += 1
            print(f"Invalid input. You have {2 - attempts} attempts left.")
    else:
        print("Too many invalid attempts. Exiting.")
        return

    # Sanitize user input for path traversal
    subfolder = os.path.abspath(subfolder)
    if not os.path.isdir(subfolder):
        print("Invalid folder path.")
        return

    folder_name = os.path.basename(os.path.normpath(subfolder))

    current_dir = os.getcwd()
    subfolder_path = os.path.join(current_dir, subfolder)  # Create full path
    parent_folder_name = os.path.basename(current_dir)

    # Expecting the chat file to be named '_chat.txt' for iOS and folder_name + '.txt' for Android
    chat_file_path_ios = os.path.join(subfolder, '_chat.txt')
    chat_file_path_android = os.path.join(subfolder, folder_name + '.txt')

    # Check for the existence of the chat file for both iOS and Android
    if os.path.isfile(chat_file_path_ios):
        chat_file_path = chat_file_path_ios
    elif os.path.isfile(chat_file_path_android):
        chat_file_path = chat_file_path_android
    else:
        print(f"Chat file not found in {subfolder}.")
        return

    version_number = get_next_version_number(folder_name)
    output_html_path = f'{folder_name}_v{version_number}.html'

    with open(chat_file_path, 'r', encoding='utf-8') as chat_file:
        lines = chat_file.readlines()

    timestamps = extract_timestamps(lines)
    date_format = detect_date_format(timestamps)

    if not date_format:
        print("Could not detect timestamp format.")
        return

    names = extract_names(lines)

    attempts = 0
    while attempts < 2:
        print("Select your name from the list:")
        for idx, name in enumerate(names):
            print(f"{idx + 1}. {name}")

        try:
            name_idx = int(input("Enter the number corresponding to your name (or press Ctrl+C to interrupt): ")) - 1
            if name_idx < 0 or name_idx >= len(names):
                raise ValueError("Invalid selection.")
            my_name = names[name_idx]
            break
        except ValueError:
            attempts += 1
            print(f"Invalid input. You have {2 - attempts} attempts left.")
    else:
        print("Too many invalid attempts. Exiting.")
        return

    start_lines = get_message_start_lines(lines)
    start_lines.append(len(lines))  # Add an endpoint for the last message

    messages = []

    last_sender = 'Unknown'  # Initialize last_sender before the loop

    for i in range(len(start_lines) - 1):
        message_lines = lines[start_lines[i]:start_lines[i+1]]
        
        timestamp, sender, message, timestamp_str = process_message(message_lines, last_sender, date_format, my_name)
        
        if timestamp and sender:
            messages.append((timestamp, sender, message, timestamp_str))
            last_sender = sender  # Update last_sender within the loop
        else:
            print("couldn't detect timestamp")

    # Sort messages by timestamp
    messages.sort(key=lambda x: x[0])

    html_content = '''
<html>
<head>
<meta charset="UTF-8">
<style>
body {font-family: Arial, sans-serif; margin: 0; padding: 10px; max-width: 1500px; margin: auto;}
.date {text-align: center; color: #555; margin: 20px 0;}
.bubble {border-radius: 20px; padding: 10px 20px; margin: 2px 10px; display: inline-block; max-width: 70%;}
.me {background-color: #DCF8C6; align-self: flex-end; text-align: right;}
.other {background-color: #E5E5EA; text-align: left;}
.sender {font-weight: bold;}
.timestamp {font-size: 0.8em; color: #999;}
.me .timestamp {text-align: right;}
.left {text-align: left;}
.right {text-align: right;}
.right .bubble {margin-left: auto; margin-right: 0;}
.left .bubble {margin-right: auto; margin-left: 0;}
</style>
<script>
function createSummary() {
    var selectedMessages = document.querySelectorAll('input[name="selected_messages"]:checked');
    var summaryContent = '<html><head><meta charset="UTF-8"><style>/* same CSS styles */</style></head><body>';

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
<!-- <button onclick="createSummary()">Create Summary</button><br/><br/> -->
'''

    last_date = None
    message_id = 0

    for timestamp, sender, message, timestamp_str in messages:
        senderclass = 'me' if sender == my_name else 'other'

        message = create_media_embed(message, subfolder, senderclass)
        message_id += 1

        if timestamp and (last_date is None or timestamp.date() != last_date):
            html_content += f'<div class="date">{timestamp.strftime("%d %B %Y")}</div>'
            last_date = timestamp.date()

        alignment_class = 'right' if senderclass == 'me' else 'left'
        html_content += f'''
<div class="{alignment_class}">
    <div class="bubble {senderclass}">
        <!-- <input type="checkbox" id="msg_{message_id}" name="selected_messages" value="msg_{message_id}">
        <label for="msg_{message_id}"> -->
            <div class="sender">{html.escape(sender)}</div>
            {message}
            <div class="timestamp">{timestamp_str if timestamp else ''}</div>
        <!-- </label> -->
    </div>
</div>
'''

    html_content += '</body></html>'

    with open(output_html_path, 'w', encoding='utf-8') as output_file:
        output_file.write(html_content)

    print(f'HTML file created: {output_html_path}')

if __name__ == '__main__':
    main()
