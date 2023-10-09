import json
import urllib.request
import string
import random

channels_to_extract = 100
API_KEY = 'AIzaSyBWnJ80IuvKCPeF6KvhGrqxWkLMCfv7U1k' #your api key 

while True:
    #UCOtHosOqPe9d6vLy-8LfHzQ
    random_name = ''.join(random.choice(string.ascii_uppercase) for _ in range(random.randint(3,10))) # for random name of channel to search 
    urlData = "https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=100&q=surfing&key=AIzaSyBWnJ80IuvKCPeF6KvhGrqxWkLMCfv7U1k".format(API_KEY,channels_to_extract,random_name)
    webURL = urllib.request.urlopen(urlData)
    data = webURL.read()
    encoding = webURL.info().get_content_charset('utf-8')
    results = json.loads(data.decode(encoding))
    results_id={}
    print(results)
    if results['pageInfo']["totalResults"]>=channels_to_extract: # may return 0 result because is a random name 
        break                  # when find a result break 

for result in results['items']:
    results_id[result['id']['channelId']]=[result["snippet"]["title"],'https://www.youtube.com/channel/'+result['id']['channelId']] # get id and link of channel for all result

with open("all_info_channels.json","w") as f: # write all info result in a file json
    json.dump(results,f,indent=4)

with open("only_id_channels.json","w") as f: # write only id of channels result in a file json
    json.dump(results_id,f,indent=4)

for channelId in results_id.keys():
    print('Link --> https://www.youtube.com/channel/'+channelId) # link at youtube channel for all result


    # 1. Seach by string (use search api) 
    #     result will have -> channel id, video id
    
    #     https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=25&q=surfing&key=[YOUR_API_KEY]
    # 2. Search by channel id -> collect stats about channel

    #     https://youtube.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics&id=UC_x5XG1OV2P6uZZ5FSM9Ttw&key=[YOUR_API_KEY]

    # 3. Hit Reports API by video id or channelId and collect (Basic stats, Time-based, Geographic)
    #     GET https://youtubeanalytics.googleapis.com/v2/reports