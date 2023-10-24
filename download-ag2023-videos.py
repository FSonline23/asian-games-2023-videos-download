import pandas as pd
import os
import requests as req
import progressbar
 
widgets = [' [',
         progressbar.Timer(format= 'elapsed time: %(elapsed)s'),
         '] ',
           progressbar.Bar('*'),' (',
           progressbar.ETA(), ') ',
          ]

df = pd.read_csv("AsianGames2022URL_20231023.csv")
print(f"Total videos: {str(len(df))}")
try:
    start_index = int(input("Enter video start index for download to start from (Note it's index, not video no):"))
except Exception as e:
    print(e)
    start_index = 0
try:
    end_index = int(input("Enter video end index for download to end till (Note it's index, not video no):"))
except Exception as e:
    print(e)
    end_index = len(df) - 1
print(f"Downloading videos from (Start index: {str(start_index)}) to  (End index: {str(end_index)})...")
failed_urls = []
for i in range(start_index, end_index + 1):
    download_url = df["Download URL"][i]
    # print(download_url)
    print(f"Downloading video index {str(i)} of {str(end_index)}...")
    output_name = f"{df['Sport Name'][i]} - {df['Episode Title'][i]} ({str(i + 1)}).mp4"
    try:
        res = req.get(download_url, stream=True)
        file_size_mb = int(res.headers.get("Content-length")) / (1024 * 1024)
        bar = progressbar.ProgressBar(max_value=file_size_mb, widgets=widgets).start()
        with open(os.path.join(os.getcwd(), df['Sport Name'][i], output_name), "wb") as f:
            counter = 0
            for chunk in res.iter_content(chunk_size = 1024*1024): 
                if chunk: 
                    f.write(chunk)
                    counter += 1
                bar.update(counter)
    except Exception as e:
        print(e)
        print(f"Video index ({i}) failed. Skipping index and proceeding to next video...")
        failed_urls.append(download_url)
        continue

if len(failed_urls) == 0:
    print("Download operations completed successfully!")
else:
    df = pd.DataFrame({"failed_urls": failed_urls})
    df.to_csv("failed_urls.csv")
    print("Download operations completed, however some urls have failed. Please check failed_urls.csv")