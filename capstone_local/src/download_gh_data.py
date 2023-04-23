import argparse
import os
import threading

import requests

def download_hourly_data(date, hour, output_dir):
    url = f"https://data.gharchive.org/{date}-{hour}.json.gz"
    file_name = os.path.join(output_dir, f"{date}-{hour}.json.gz")
    response = requests.get(url)
    
    with open(file_name, 'wb') as f:
        f.write(response.content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--date", 
        help="Date in the format 'YYYY-MM-DD' (e.g. 2023-04-01)"
    )
    parser.add_argument(
        "--output_dir", 
        help="Directory to store output files"
    )
    args = parser.parse_args()

    date = args.date
    output_dir = args.output_dir
    hours = range(0, 24)

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    threads = []
    timestamps = [(date, hour, output_dir) for hour in hours]
    for timestamp in timestamps:
        t = threading.Thread(target=download_hourly_data, args=timestamp)
        threads.append(t)
        t.start()
    for thread in threads:
        thread.join()
