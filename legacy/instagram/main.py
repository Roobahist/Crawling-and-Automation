import requests
from datetime import datetime , timezone

par = dict()
par['access_token'] = 'fill_here'

base_url = 'https://graph.facebook.com/v8.0/'
r = requests.get(url = base_url + 'me/accounts' , params=par)
j = r.json()
# print(j)
# print('----------------------------')

page_id = j['data'][0]['id']

url = base_url + str(page_id)

par['fields'] = 'instagram_business_account'

r = requests.get(url, par)
j = r.json()
# print(j)
# print('----------------------------')

ig_user_id = j['instagram_business_account']['id']

print('instagram_user_id = ',ig_user_id)

def posts_data():
    print('\n')
    print('**************************************')
    print('Posts Data Started')

    for key in list(par.keys()):
        if key != 'access_token':
            par.pop(key)
    # par['fields'] = 'instagram_business_account'

    url = base_url + str(ig_user_id) + '/media'
    r = requests.get(url, par)
    j = r.json()
    # print(j)
    # print('----------------------------')

    post_endpoints = [i['id'] for i in j['data']]

    posts_data = dict()
    i = 0
    for post_id in post_endpoints:
        i += 1
        post_data = dict()

        url = base_url + str(post_id) 
        par['fields'] = 'like_count,caption,comments_count,media_type,media_url'

        r = requests.get(url , par)
        j = r.json()

        post_data['like_count'] = j['like_count']
        post_data['caption'] = j['caption']
        post_data['comments_count'] = j['comments_count']
        post_data['media_type'] = j['media_type']
        post_data['media_url'] = j['media_url']

        url += '/insights'

        if post_data['media_type'] == 'CAROUSEL_ALBUM':
            par['metric'] = 'carousel_album_engagement,carousel_album_impressions,carousel_album_reach,carousel_album_saved'
            par.pop('fields')
            r = requests.get(url,par)
            data = r.json()['data']
            for i in range (len(data)):
                name = data[i]['name']
                value = data[i]['values'][0]['value']
                post_data[name] = value

        elif post_data['media_type'] == 'IMAGE':
            par['metric'] = 'engagement,impressions,reach,saved'
            par.pop('fields')
            r = requests.get(url,par)
            data = r.json()['data']
            for i in range (len(data)):
                name = data[i]['name']
                value = data[i]['values'][0]['value']
                post_data[name] = value

        elif post_data['media_type'] == 'VIDEO':
            par['metric'] = 'engagement,impressions,reach,saved,video_views'
            par.pop('fields')
            r = requests.get(url,par)
            data = r.json()['data']
            for i in range (len(data)):
                name = data[i]['name']
                value = data[i]['values'][0]['value']
                post_data[name] = value

        else:
            print('WARNING!')
            print(post_data['media_type'])
            print('---------')

        posts_data[str(post_id)] = post_data


    f1 = open('postsdata.csv' , 'w' , encoding='utf-8')
    headers = 'post_id#$#like_count#$#caption#$#comments_count#$#media_type#$#media_url#$#engagement#$#impressions#$#reach#$#saved#$#video_views\n'
    f1.write(headers)

    keys = list(posts_data.keys())
    for post_id in keys:
        post_data = posts_data[post_id]
        like_count = post_data[list(post_data.keys())[0]]
        caption = post_data[list(post_data.keys())[1]].replace('\n','   ')
        comments_count = post_data[list(post_data.keys())[2]]
        media_type = post_data[list(post_data.keys())[3]]
        media_url = post_data[list(post_data.keys())[4]]
        engagement = post_data[list(post_data.keys())[5]]
        impressions = post_data[list(post_data.keys())[6]]
        reach = post_data[list(post_data.keys())[7]]
        saved = post_data[list(post_data.keys())[8]]
        video_views = 'not_video'

        if 'video_views' in list(post_data.keys()):
            video_views = post_data['video_views']

        to_write = str(post_id) + '#$#' + str(like_count) + '#$#' + str(caption) + '#$#' + str(comments_count) + '#$#' + str(media_type) + '#$#' + str(media_url) + '#$#' + str(engagement) + '#$#' + str(impressions) + '#$#' + str(reach) + '#$#' + str(saved) + '#$#' + str(video_views) + '\n'
        f1.write(to_write)

    print('Posts Data Done')
    print('**************************************')


def user_data():
    print('\n')
    print('**************************************')
    print('User Data Started')

    if 'fields' in list(par.keys()):
        par.pop('fields')

    par['period'] = 'day'
    par['metric'] = ['impressions, reach, follower_count, email_contacts, phone_call_clicks, text_message_clicks, get_directions_clicks, website_clicks, profile_views']

    print('==================')
    print('Since : yyyy,mm,dd')
    since = list(map(int , input('Since : ').split(',')))
    dt = datetime(since[0],since[1],since[2])
    sincetimestamp = dt.replace(tzinfo=timezone.utc).timestamp()
    par['since'] = sincetimestamp
    print('since timestamp = ',int(sincetimestamp))
    print('==================')

    print('Until : yyyy,mm,dd')
    until = list(map(int ,input('Until : ').split(',')))
    dt = datetime(until[0],until[1],until[2])
    untiltimestamp = dt.replace(tzinfo=timezone.utc).timestamp()
    par['until'] = untiltimestamp
    print('until timestamp = ',int(untiltimestamp))
    print('==================')

    url = base_url + ig_user_id + '/insights'
    
    r = requests.get(url,par)
    data = r.json()['data']

    headers = 'title#$#value#$#end_time\n'

    f2 = open('userdata.csv' , 'w' , encoding='utf-8')
    f2.write(headers)

    for i in range(len(data)):
        title = data[i]['title']
        values = data[i]['values']
        
        for j in range(len(values)):
            value = data[i]['values'][j]['value']
            end_time = data[i]['values'][j]['end_time']

            f2.write(title + '#$#' + str(value) + '#$#' + str(end_time) + '\n')
            
    print('User Data Done')
    print('**************************************')



user_data()
posts_data()

    




