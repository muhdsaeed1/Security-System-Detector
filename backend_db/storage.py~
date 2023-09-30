import os
import threading
import requests
import ffmpeg
from datetime import datetime
import json
import uuid

API_ENDPOINT = "http://127.0.0.1:5000/motion_detected"

def save_to_file(path):
    # Generate a UUID4 identifier
    unique_id = str(uuid.uuid4())

    # Get the current date and time
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Create a dictionary to store the data
    data = {
        'path': path,
        'current_date': current_date,
        'id': unique_id
    }

    # Serialize the data to JSON format
    json_data = json.dumps(data, indent=4)

    # Define the filename for the JSON file
    filename = 'db.json'

   # Check if the file already exists
    if os.path.exists(filename):
        # If the file exists, load existing data
        with open(filename, 'r') as file:
            existing_data = json.load(file)
        
        # Append the new data to the existing data
        existing_data.append(data)

        # Write the updated data back to the file
        with open(filename, 'w') as file:
            json.dump(existing_data, file, indent=4)
        
        print(f'Data appended to {filename}')
    else:
        # If the file doesn't exist, create a new one with the new data
        with open(filename, 'w') as file:
            json.dump([data], file, indent=4)

        print(f'New data saved to {filename}')
    return "http://127.0.0.1:5000/video/"+unique_id


""" def upload_to_bucket(blob_name, path_to_file):
    blob = bucket.blob(blob_name)
    blob.content_type = 'video/mp4'

    blob.upload_from_filename(path_to_file)

    blob.patch()
    blob.make_public()

    os.remove(path_to_file)

    print(f"A new file by the name of {blob_name} was created in your bucket {BUCKET_NAME}")
    return blob.public_url
 """
def get_path(id):
    filename = "db.json"
    with open(filename, 'r') as file:
            existing_data = json.load(file)
            for data in existing_data:
                if data["id"] == id:
                    return data["path"]
    return "File not found"


def handle_detection(path_to_file):
    def action_thread(path_to_file):
        output_path = path_to_file.split(".mp4")[0] + "-out.mp4"
        ffmpeg.input(path_to_file).output(output_path, vf='scale=-1:720').run()
        os.remove(path_to_file)
        url = save_to_file(output_path)
        data = {
            "url": url,
        }
        requests.post(API_ENDPOINT, json=data)
    
    thread = threading.Thread(target=action_thread, args=(path_to_file,))
    thread.start()


def list_videos_in_date_range(start_date, end_date, extension=".mp4"):
    # Convert the string dates to datetime objects
    start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
    end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
    filename = 'db.json'
    matching_files = []

    # Iterate over the blobs (objects) in the bucket
    with open(filename, 'r') as file:
        base_url = "http://127.0.0.1:5000/video/"
        for vid in json.load(file):
            if vid['path'].endswith(extension):
                created_date = datetime.strptime(vid['current_date'], '%Y-%m-%d')
                # Check if blob creation date is within the desired range
                if start_datetime <= created_date <= end_datetime:
                    matching_files.append({"url": base_url+vid['id'], "date": vid["current_date"]})

    return matching_files