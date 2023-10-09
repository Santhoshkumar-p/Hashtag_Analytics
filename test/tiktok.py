from TikTokApi import TikTokApi
import asyncio
import os
import json

#https://github.com/davidteather/TikTok-Api/tree/main/examples
#https://www.tiktok.com/?is_copy_url=1&is_from_webapp=v1 
#https://app.brandmentions.com/h/k/fashionhaul

ms_token = 'gWl9GJxxKdUL2K28D7T_2q7W-GgnbqaqYqoNHHlxY4ZMGSZgVE5xhcDqcto2JoW2-GqKRrJ5Ef2HYkLX6TEmx1GQD7SSuee8WcWQ4CqA51EJUrGFclbz6ZkWEcBOM3mw1BuUKh1TDi2sfqrB'  # set your own ms_token

output_raw = []
output = []

def filter_related_hashtags(textExtra) -> list: 
    hashtags = [i['hashtagName'] for i in textExtra]
    return hashtags


async def get_hashtag_videos():
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
        tag = api.hashtag(name="trending")
        async for video in tag.videos(count=10):
            vid_dict = video.as_dict
            result = {}
            result.update({"nickname":vid_dict['author']['nickname']})
            result.update({"id":vid_dict['author']['uniqueId']})
            result.update({"bio":vid_dict['author']['signature']})
            result.update({"private":vid_dict['author']['privateAccount']})
            result.update({"authorstats":vid_dict['authorStats']})
            result.update({"post":{"createtime":vid_dict['createTime'], 
                                   "desc":vid_dict['desc'], 
                                   "postid":vid_dict['id'],
                                   "url":f"https://www.tiktok.com/@{vid_dict['author']['uniqueId']}/video/{vid_dict['id']}",
                                   "stats":vid_dict['stats'],
                                   "related_hashtags":filter_related_hashtags(vid_dict['textExtra'])}})

            result.update()
            output.append(result)
            output_raw.append(vid_dict)
            #print(result_json)
            #with open("./tiktok.txt","w") as f:
            #    f.write(str(result))

if __name__ == "__main__":
    asyncio.run(get_hashtag_videos())
    

#output_raw_json = json.dumps(output_raw, indent = 4)
output_json = json.dumps(output, indent = 4)

# with open('./tiktok_raw.txt','w') as f:
#     f.write(output_raw_json)

with open('./tiktok_filtered.txt','w') as f:
    f.write(output_json)