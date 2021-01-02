import requests as rq
import pandas as pd

msg_url = 'https://slack.com/api/conversations.history'
msg_headers = {'content-type': 'application/x-www-form-urlencoded'}
msg_params = {
    'token': 'xoxp-XXXXXXXXXXXX-XXXXXXXXXXXX-XXXXXXXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    'channel': 'CXXXXXXXX',
    'limit': 1000
}

msg_res = rq.get(url=msg_url, headers=msg_headers, params=msg_params)
msg = [i['ts'] for i in msg_res.json()['messages']]

emj_data = []
for m in msg:
    url = 'https://slack.com/api/reactions.get'
    head = {'content-type': 'application/x-www-form-urlencoded'}
    params = {
        'token': 'xoxp-XXXXXXXXXXXX-XXXXXXXXXXXX-XXXXXXXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
        'channel': 'CXXXXXXXX',
        'timestamp': m
    }
    res = rq.get(url=url, headers=head, params=params)
    try:
        for i in res.json()['message']['reactions']:
            emj_data.append({'ts': msg, 'name': i['name'], 'count': i['count']})
    except:
        pass

emj_df = pd.DataFrame(emj_data)
print(emj_df.groupby('name')['count'].sum().sort_values(ascending=False).head(30))