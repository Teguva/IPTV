import csv
import requests
from io import StringIO

# URL for the CSV file from Google Sheets
csv_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSMvWRL4XRip6SZT21jxkR_Ep0Rheo3kLSpx5AoFbaGFvPs65-pEgHUuxO91aGmUs03IYfLCc-pd4-Z/pub?output=csv'

# Function to download the CSV file from the URL
def download_csv(url):
    response = requests.get(url)
    if response.status_code == 200:
        return StringIO(response.content.decode('utf-8'))
    else:
        print("Failed to download CSV file")
        return None

# Function to read the CSV file and process the data
def process_csv(input_file):
    channels = []
    
    # Reading from the input file (which is a StringIO object after downloading)
    reader = csv.DictReader(input_file)
    
    for row in reader:
        # Ensure all required fields are present
        if 'ID' in row and 'NAME' in row and 'Stream URL' in row and 'Logo URL' in row:
            channel = {
                'channel_id': row['ID'],
                'channel_name': row['NAME'],
                'hls_url': row['Stream URL'],
                'logo_url': row['Logo URL'],
                'quality': row['Quality']
            }
            channels.append(channel)
    
    return channels

# Function to generate the M3U8 file
def generate_m3u8(channels, output_file):
    with open(output_file, 'w', encoding='utf-8') as m3u8_file:
        # Write the M3U8 header
        m3u8_file.write('#EXTM3U\n')
        
        # Write each channel to the M3U8 file in the required format
        for channel in channels:
            m3u8_file.write(f'#EXTINF:-1 tvg-id={channel["channel_id"]} tvg-name="{channel["channel_name"]}" tvg-logo="{channel["logo_url"]}",{channel["channel_name"]} {channel["quality"]}\n')
            m3u8_file.write(f'#EXT-X-STREAM-INF:RESOLUTION=1920x1080,BANDWIDTH=5000000\n')
            m3u8_file.write(f'{channel["hls_url"]}\n')
            m3u8_file.write('\n')

# Example usage
output_file = 'output.m3u8'  # Desired M3U8 file path

# Download and process the CSV data
csv_data = download_csv(csv_url)
if csv_data:
    channels = process_csv(csv_data)
    generate_m3u8(channels, output_file)
    print(f'M3U8 file generated: {output_file}')
else:
    print("Failed to generate M3U8 file due to CSV download error.")
