import jsonlines
import csv

#word_list = ['iowa', 'more voter', 'than citizen']
#word_list = ['biden', 'american flag', 'remove']
word_list = ['trump', 'economy', 'best', 'ever']

#file_name = 'Biden_american_flag_remove'
#file_name = 'trump_economy_best_even'
file_name = '2 trump_economy_best_ever'


seperator = ', '
def separate_http(s):
    n = s.find('http')
    if n == -1:
        return [s,'']
    else:
        return [s[0:n],s[n:]]


with open(file_name+'.csv', 'a+', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Date', 'Text', 'http Link', 'Quoted Text', 'User', 'Original User', 'Matching Keywords',
                     'Not Matching Keywords', 'Hashtags', 'User mentions', 'Profile creation date', 'Location'])
cnt = 0
cnt_match = 0
tw_ht = {}
with jsonlines.open(file_name+'.jsonl') as reader:
    for obj in reader:
        cnt += 1
        u0 = '@'+obj['user']['screen_name']
        match_w = []
        no_match_w = []

        if "retweeted_status" in obj:
            if "extended_tweet" in obj['retweeted_status']:
                s0 = obj['retweeted_status']['extended_tweet']['full_text'].lower()
            else:
                s0 = obj['retweeted_status']['text'].lower()
        elif "extended_tweet" in obj:
            s0 = obj['extended_tweet']['full_text'].lower()
        else:
            s0 = obj['text'].lower()

        if "quoted_status" in obj:
            u1 = '@' + obj['quoted_status']['user']['screen_name']
            q = 1
            if 'extended_tweet' in obj['quoted_status']:
                s1 = obj['quoted_status']['extended_tweet']['full_text'].lower()
            else:
                s1 = obj['quoted_status']['text'].lower()
        else:
            u1 = " "
            q = 0
            s1 = " "

        [s0_txt, s0_http] = separate_http(s0)

        s_all = s0+s1

        for w in word_list:
            if w in s_all:
                match_w.append(w)
            else:
                no_match_w.append(w)

        if len(no_match_w) == 0:
            cnt_match += 1

        hashtags = []
        for i in range(len(obj['entities']['hashtags'])):
            hashtags.append(obj['entities']['hashtags'][i]['text'])

        user_mentions = []
        for i in range(len(obj['entities']['user_mentions'])):
            user_mentions.append(obj['entities']['user_mentions'][i]['screen_name'])

        if s0_txt in tw_ht:
            tw_ht[s0_txt].append([obj['created_at'], s0_txt.replace(';', ''), s0_http, s1.replace(';', ''), u0, u1,
                                  seperator.join(match_w), seperator.join(no_match_w), seperator.join(hashtags),
                                  seperator.join(user_mentions), obj['user']['created_at'], obj['user']['location']])
        else:
            tw_ht[s0_txt] = [[obj['created_at'], s0_txt.replace(';', ''), s0_http, s1.replace(';', ''), u0, u1,
                              seperator.join(match_w), seperator.join(no_match_w), seperator.join(hashtags),
                              seperator.join(user_mentions), obj['user']['created_at'], obj['user']['location']]]





for tw_txt in tw_ht:
    for tw in tw_ht[tw_txt]:
        with open(file_name+'.csv', 'a+', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(tw)


with open(file_name+'.csv', 'a+', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Matching percentage: '+str(float(cnt_match/cnt*100)), ' ', ' ', ' ', ' ', ' ', ' ', ' '])

