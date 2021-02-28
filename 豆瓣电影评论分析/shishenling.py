import re 
from bs4 import BeautifulSoup as bs
import time 
import csv
import requests
 
 
def getContent(requrl,headers,cookies,page):
    
    resp = requests.get(requrl,cookies=cookies,headers=headers)
    
    #res = requests.get(url, headers=headers)
    html_data = resp.text
    
 
    # 接下来使用bs进行爬虫
    soup = bs(html_data, 'html.parser') 
    # 所要爬取的内容所在位置
    comment_div_lits = soup.find_all('div', class_='comment-item')
    #print(type(html_data))
    #print(comment_div_lits[0])
    
    # print("第{0}页输出： ".format(int(page)))
    eachList = []
    
    if len(comment_div_lits) == 0:
        print("第 {0} 页爬取不到信息.....".format(int(page)))
        print("len(comment_div_lits): ",len(comment_div_lits))
        return 
    
    for item in comment_div_lits:
        name = ''
        score = ''
        time = ''
        comment = ''
        votes = ''
        each = []
        #<a href=(.*?) class>(.*?)</a>
        
        # 用户ID,name
        pattern_Name = re.compile(r'<a class="" href="(.*?)">(.*?)</a>')
        patter_name = pattern_Name.findall(str(item))
        if patter_name != []:
            name = str(patter_name[0][1])
        else:
            print("第 {0} 页某行有空用户ID... ".format(int(page)))
        
        # 评论星级,score
        #<span class="allstar20 rating" title="较差"></span>
        pattern = re.compile(r'<span class="allstar(.*?) rating" title="(.*?)"></span>')
        patter_score = pattern.findall(str(item))
        if patter_score == []:
            print("第 {0} 页某行有空评分星级... ".format(int(page)))
            continue        
        score = str(int(patter_score[0][0])//10)
        
        # 评论时间
        if item.find_all('span',class_='comment-time')[0].string is not None:
            time = str(item.find_all('span',class_='comment-time')[0].string.split())
        else:
            print("第 {0} 页某行评论时间为空... ".format(int(page)))
        
        # 点赞数
        if item.find_all('span',class_="votes")[0].string is not None:
            votes = item.find_all('span',class_="votes")[0].string
        else:
            print("第 {0} 页某行点赞数为0... ".format(int(page)))
            
        # 评论内容
        if item.find_all('span',class_="short")[0].string is not None: 
            comment = item.find_all('span',class_="short")[0].string
        else:
            print("第 {0} 页某行有空短评... ".format(int(page)))
            continue
        
        each = [name,score,votes,time,comment]
 
        #print([name,score,time])
        with open('./lihuanying.csv','a+',encoding='utf-8',newline='') as f:
            writer = csv.writer(f)
            writer.writerow(each)
 
def main():
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
    }
    cookie = {
        'cookies': 'viewed="30147778"; bid=puZ4S36MLEM; gr_user_id=db5b2eb2-1d86-4c69-992c-b053ddc181b7; _vwo_uuid_v2=D4B469B0980898078628EF88CDE450566|2baff6fb8d8ae9aa8de2fcbdffcda7c0; __gads=ID=55b0450105cc6e80-22e26c74fbc50050:T=1613008147:RT=1613008147:S=ALNI_MbQDt4RA_kel9M2mdJ3NpZxMilrmQ; ap_v=0,6.0; __utma=30149280.1014455827.1613008147.1613008147.1613230364.2; __utmb=30149280.0.10.1613230364; __utmc=30149280; __utmz=30149280.1613230364.2.2.utmcsr=link.csdn.net|utmccn=(referral)|utmcmd=referral|utmcct=/; ll="108288"; frodotk="cf247a4a59c056b96d6d6edf0d41042b"; push_noty_num=0; push_doumail_num=0; dbcl2="82469221:yz3MoWktodQ"; ck=eOXK'
    }
    
    for i in range(0,600,20):
        print("爬取第{0}页......".format(int(i)))
        requrl = "https://movie.douban.com/subject/26935283/comments?start=" + str(i) + "&limit=20&sort=new_score&status=P"
        getContent(requrl,headers,cookie,i)
        time.sleep(3)
    print("爬到所有数据，爬虫结束")
 
main()