import requests, json
import xml.etree.ElementTree as ET 
from datetime import date 
cookies = {
    'SESSID': 'S0FOVzZZNTkzMzY1',
    'LC_SUBJECT593365': 'ALL',
    'LC_TERM593365': '201520',
    'LC_HOURS593365': '',
    'LC_COURSE593365': '',
    'LC_TITLE593365': '',
    'LC_DEPT593365': 'ALL',
    'LC_INSTRUCTOR593365': '',
    'LC_ATTRIB593365': 'ALL',
    'LC_DESCRIPTION593365': '',
    'LC_INDP593365': 'on',
    'LC_CREDIT593365': 'ALL',
    's_fid': '737292652352B94A-2D08793FBB1D9F7B',
    'WRUID': '856361669.2096977450',
    '__CT_Data': 'gpv=4&apv_16437_www03=4&cpv_16437_www03=4&rpv_16437_www03=4',
    'SESS7c9e7ecfbc1829fd5adde284b5e03cbd': '8a3fa6d244aa6650d7fc1bbe02a8e9c9',
    '_ga': 'GA1.2.953585774.1416716822',
    '__utma': '117564634.953585774.1416716822.1446323861.1446954768.40',
    '__utmc': '117564634',
    '__utmz': '117564634.1446954768.40.35.utmccn=(referral)|utmcsr=google.com|utmcct=/|utmcmd=referral',
    'IDMSESSID': '100605285',
    'TSdde4ce': '7f525e3c932d081ef9c50a620d50871ac1558998d6c520fb5640bdb9bc0930054b7ae14e54b74eb24b7ac44f',
    'TS9c2c42': '70f9ef0036e6810c78b256c4f6558cc088089294616351615640bdb912c5ee399a5a120c',
    'webfxtab_tabPane1': '0',
    'lc_advanced': 'off',
    'L_PAGE593365': '1',
    'SEARCH': '#SearchResults',
    'L_PAGE': '1',
}

headers = {
    'Origin': 'https://selfservice.brown.edu',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.8,es;q=0.6,fr;q=0.4',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
    'Content-Type': 'text/plain;charset=UTF-8',
    'Accept': '*/*',
    'Referer': 'https://selfservice.brown.edu/ss/hwwkcsearch.P_Main',
    'Connection': 'keep-alive',
}

connect_timeout = 5
response_timeout = 20

classes = {}

for CRN in open('201520'):
    CRN = CRN.strip()
    data = 'IN_TERM=201520&IN_CRN=' + CRN + '&IN_FROM=2';

    try_again = True
    while (try_again):
        try:
            r = requests.post('https://selfservice.brown.edu/ss/hwwkcsearch.P_Detail', headers=headers, cookies=cookies, data=data, timeout=(connect_timeout, response_timeout))
            try_again = False
        except requests.exceptions.ConnectionError as e:
            print "Too slow Mojo! Trying again... "
        except requests.exceptions.ReadTimeout as e:
            print "To slow to read! Trying again..."
    print 'finished connection'
    resp = r.text
    start = resp.find('<td style="color:#B80000;">') + 27
    end = resp.find(" ", start)
    print resp[start:end]
    try: 
        seats_available = int(resp[start:end])
    except ValueError:
        print 'VALUE ERROR'
        print resp
    start = resp.find("of ", end) + 3
    end = resp.find(" Seats", start)
    print resp[start:end]
    try:
        total_seats = int(resp[start:end])
    except ValueError:
        print 'VALUE ERROR'
        print resp
    if (total_seats != 0):
        seats_taken = total_seats - seats_available
        percent_seats_taken = float(seats_taken) / float(total_seats) * 100.0 
        classes[CRN] = {'total' : total_seats, 'available' : seats_available, 'percent_taken' : percent_seats_taken}
        print 'finished CRN: ' + str(CRN) 

print '[FINISHED]'

t = date.today()
today_string = t.strftime("%d%m%y")
f = open(today_string, 'w')
f.write(json.dumps(classes))
print 'wrote JSON to ' + today_string






