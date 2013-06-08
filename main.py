
import urllib
import urllib2
import string 
import random
import cookielib
import json


#To get a new session id
def reload():
    global cj,opener_for_reload,new_session
    url="http://pizzaonline.dominos.co.in/slot-machine/"
    opener_for_reload.open(url)    
    for cookie in cj:
        new_session=cookie.value
    retry()


#To get new coupon
def retry():
    global cj,opener_for_retry,new_session,ff,count
    for iter in range(5):
        values = {      'session_id' : new_session }
        data = urllib.urlencode(values)
        url="http://pizzaonline.dominos.co.in/slot-machine/process-slot.php"
        f=opener_for_retry.open(url,data)
        output = f.read(1000)
        d = json.loads(output)
        try:
            if(d['slot_result']=='1' or d['slot_result']=='2D' or d['slot_result']=='3' or d['slot_result']=='3A'):
                new_coupon="<coupon>\n\n"+"\tCoupon Code : "+d['unique_coupon']+"\n\n"+"\tCoupon Description : "+d['coupon_description']+"\n\n"+"\tSession id : "+new_session+"\n\n</coupon>\n\n"
                ff.write(new_coupon);
                new_session='dummy'
                print str(count)+" coupons fetched so far" 
                count=count+1
                break
        except:
            pass
    reload()

count=1
cj=cookielib.CookieJar()
opener_for_reload=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener_for_retry=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
new_session='dummy'
opener_for_reload.addheaders = [
                ('Host', 'pizzaonline.dominos.co.in'),
                ('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'),
                ('Accept'        , 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                ('Accept-Language' , 'en-us,en;q=0.5'),
                ('Connection'    ,  'keep-alive'),
                ('Referer'       ,'http://pizzaonline.dominos.co.in/slot-machine/')
                ]
opener_for_retry.addheaders = [
                ('Host', 'pizzaonline.dominos.co.in'),
                ('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'),
                ('Accept'        , '*/*'),
                ('Accept-Language' , 'en-us,en;q=0.5'),
                ('Connection'    ,  'keep-alive'),
                ('Referer'       ,'http://pizzaonline.dominos.co.in/slot-machine/'),
                ('Content-Type','application/x-www-form-urlencoded; charset=UTF-8'),
                ('X-Requested-With','XMLHttpRequest')
                ]
        

#uncomment to get a random file name everytime instead of dominos-coupons.log
#ff=open(''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(15)),'a')

#File to open for writing coupons
ff=open('dominos-coupons.log','a')
reload()
