import vk_api
import os
#from tokens import VK_TOKEN


VK_TOKEN = None
# with open("vkbot/tokenvk.txt") as f:
#     VK_TOKEN = f.read().strip()

VK_TOKEN = os.environ["VK_TOKEN"]

# vk session init
vk_session = vk_api.VkApi(token=VK_TOKEN)
vk = vk_session.get_api()


# search group (count=10)
def search_group(request):
    all_groups = vk.groups.search(q=request, count=10)

    ids = []
    for group in all_groups['items']:
        ids.append(str(group['id']))
    ids = ','.join(ids)
    groups = vk.groups.getById(group_ids=ids, is_closed=0)
    return groups


# get new post (count=1)
def get_post(owner_id):
    try:
        post = vk.wall.get(access_token=VK_TOKEN, owner_id=-owner_id, count=1)['items'][0]
        new_date = int(post['date'])
        post_id = post['id']
        post_text = post['text']
        link = f'https://vk.com/public{owner_id}?w=wall{-owner_id}_{post_id}'
        return post_text, link, new_date
    except:
        print(owner_id, '--*ERROR*')
        return None
   


   
    
    
        






    
