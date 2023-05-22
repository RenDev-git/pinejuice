# script made by rendev 2023 

import os
import requests
import zipfile
from tqdm import tqdm
import shutil

version = input("Choose a version: ")

initial_url = f"https://github.com/pineappleEA/pineapple-src/releases/download/EA-{version}/Windows-Yuzu-EA-{version}.zip"


# folder path in which yuzu is downloaded and extracted this is by defualt will be made in the directory of the script
folder_path = "YuzuEa"

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# send a request to check the validty of the connection
response = requests.head(initial_url, allow_redirects=True)

# Check if the response is successful 
if response.status_code == 200:
    final_url = response.url

    # clear data inside the YuzuEa folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    # Installing 
    zip_path = os.path.join(folder_path, f"Windows-Yuzu-EA-{version}.zip")
    response = requests.get(final_url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024 
    progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)
    with open(zip_path, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(folder_path)
    os.remove(zip_path)

    intermediate_folder = None
    for root, dirs, files in os.walk(folder_path):
        for dir_name in dirs:
            if dir_name.startswith('yuzu-windows-msvc-early-access'):
                intermediate_folder = dir_name
                break
        if intermediate_folder:
            break

    intermediate_folder_path = os.path.join(folder_path, intermediate_folder)
    for item in os.listdir(intermediate_folder_path):
        item_path = os.path.join(intermediate_folder_path, item)
        if os.path.isfile(item_path):
            shutil.move(item_path, folder_path)
        else:
            shutil.move(item_path, os.path.join(folder_path, item))

    shutil.rmtree(intermediate_folder_path)

    print("Installation successful!")
else:
    print(f"Error: {response.status_code}")
