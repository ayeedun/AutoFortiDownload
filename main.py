import requests
import xml.etree.ElementTree as ET
import os

# URL of the XML file
xml_url = "https://filestore.fortinet.com/forticlient/"

# Send a GET request to the XML URL
response = requests.get(xml_url)

# Parse the XML content if the request is successful
if response.status_code == 200:
    # Parse the XML content
    root = ET.fromstring(response.content)

    # Base URL for downloading files
    base_url = "https://filestore.fortinet.com/forticlient/"

    # Create a directory to store downloaded files if it doesn't exist
    os.makedirs("forticlient_files", exist_ok=True)

    # Download files specified in the XML
    for content in root.findall(".//{http://s3.amazonaws.com/doc/2006-03-01/}Contents"):
        key = content.find("{http://s3.amazonaws.com/doc/2006-03-01/}Key").text
        if key.endswith(".exe"):
            download_url = base_url + key
            file_name = os.path.join("forticlient_files", key.split("/")[-1])

            # Send a GET request to download the file
            file_response = requests.get(download_url)
            if file_response.status_code == 200:
                # Save the file to the local directory
                with open(file_name, "wb") as file:
                    file.write(file_response.content)
                print(f"Downloaded: {key}")
            else:
                print(f"Failed to download: {key}")

    print("All files downloaded successfully.")
else:
    print("Failed to retrieve the XML data. Status code:", response.status_code)