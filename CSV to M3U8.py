import csv

# Function to read the CSV file and process the data
def process_csv(input_file):
    channels = []
    
    with open(input_file, 'r') as file:
        reader = csv.DictReader(file)
        
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

# Function to print the channels in a readable format (optional)
def display_channels(channels):
    for channel in channels:
        print(f"Channel Name: {channel['channel_name']}")
        print(f"Channel ID: {channel['channel_id']}")
        print(f"HLS URL: {channel['hls_url']}")
        print(f"Logo URL: {channel['logo_url']}")
        print("-" * 40)

# Example usage
input_file = 'channels.csv'  # Replace with your CSV file path
output_file = 'output.m3u8'   # Desired M3U8 file path

# Process the CSV and generate M3U8 file
channels = process_csv(input_file)
generate_m3u8(channels, output_file)

print(f'M3U8 file generated: {output_file}')
