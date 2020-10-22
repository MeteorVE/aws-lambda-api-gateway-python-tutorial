#!/usr/bin/env python
#coding=utf-8

import json
from PyPtt import PTT
import re

########################

ptt_bot = PTT.API(language=PTT.i18n.language.CHINESE)
ptt_id='abc'
password='dont tell you'




def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
    info = {}
    
    print("[debuging]: ",event)

    try:
        target_board = event['board']
        read_article_number = event['num']
        if int(read_article_number) > 5:
            read_article_number = 5
        info['error'] = 'false'
    except:
        target_board = ''
    
    if target_board == '':
        target_board = 'Soft_Job'
        read_article_number = 3
        info['error'] = 'true'
    
        
    print("[debuging]: ", target_board, read_article_number)
    try:
        ptt_bot.login(ptt_id, password)
    except PTT.exceptions.LoginError:
        ptt_bot.log('登入失敗')
        sys.exit()
    except PTT.exceptions.WrongIDorPassword:
        ptt_bot.log('帳號密碼錯誤')
        sys.exit()
    except PTT.exceptions.LoginTooOften:
        ptt_bot.log('請稍等一下再登入')
        sys.exit()
    ptt_bot.log('登入成功')

    search_list = [
    #(PTT.data_type.post_search_type.KEYWORD, 'Switch'),
    ]

    
    try:
        index = ptt_bot.get_newest_index(
        PTT.data_type.index_type.BBS,
        target_board)
        print(f'該版最新文章編號 {index}')
    except:
        info['error'] = '取得看版資料時出現錯誤，請檢查該看版是否存在。'
        print('取得看版資料時出現錯誤，請檢查該看版是否存在。')
        return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': "*",
            "Access-Control-Allow-Credentials" : "true",
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': info
    };
    
    

    for current_index in range(index-int(read_article_number)+1, index+1):
        post_info = ptt_bot.get_post(
            target_board,
            post_index=current_index,
            query=True)
        print("文章編號:",current_index, "  標題:",post_info.title)
        if post_info.push_number == None:
            post_info.push_number = 0
        info[current_index] = {'title':post_info.title, 'url':post_info.web_url, 'push': post_info.push_number}
        

    ptt_bot.logout()
    # print("value1 = " + event['key1'])
    # print("value2 = " + event['key2'])
    # print("value3 ? = " + event['key3'])
    # return event['key1']  # Echo back the first key value
    #raise Exception('Something went wrong')
    return  {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': "*",
            "Access-Control-Allow-Credentials" : "true",
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': info
    };

    raise Exception('Something went wrong')

#print(lambda_handler({'board':'NTU', 'num':3}, None))