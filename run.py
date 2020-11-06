import requests
import pandas
from bs4 import BeautifulSoup
import time
import datetime

valid_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_'


def getUserSpan(username):
    if not username:
        return ''
    reqname = ''.join([c for c in username if c in valid_chars])
    if reqname == '':
        return username
    ulink = f'https://atcoder.jp/users/{reqname}'
    req = requests.get(ulink)
    if not req.status_code == requests.codes.ok:
        return username
    soup = BeautifulSoup(req.text, 'html.parser')
    uinfo = soup.select_one('a.username span')
    return f'<a href="{ulink}">{str(uinfo)}</a>'


url = 'https://jag-icpc.org/?2020%2FTeams%2FList'
df = pandas.read_html(url)[1].fillna('')[5:].reset_index(drop=True)
res_df = df.copy()
user_columns = ['メンバー 1', 'メンバー2', 'メンバー3', 'コーチ，ココーチ']
for c in user_columns:
    for idx, username in enumerate(df[c]):
        res_df[c][idx] = getUserSpan(username)
        time.sleep(0.1)

df_html = res_df.to_html().replace('&lt;', '<').replace('&gt;', '>')

complete_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jquery.tablesorter/2.31.0/js/jquery.tablesorter.min.js"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/jquery.tablesorter/2.31.0/css/theme.default.min.css">
<title>ICPC 2020 Domestic Teams</title>
<style>
table a {text-decoration: none;}
.username > span {font-weight:bold;}
a:hover.username {text-decoration: none;}
.user-red {color:#FF0000;}
.user-orange {color:#FF8000;}
.user-yellow {color:#C0C000;}
.user-blue {color:#0000FF;}
.user-cyan {color:#00C0C0;}
.user-green {color:#008000;}
.user-brown {color:#804000;}
.user-gray {color:#808080;}
.user-unrated {color:#000000;}
.user-admin {color:#C000C0;}
.dataframe {font-size: 14px; }
</style>
<script>
$(document).ready(function() {
    $('.dataframe').tablesorter();
});
</script>
</head>
<body>
<p>This information is from <a href="https://jag-icpc.org/?2020%%2FTeams%%2FList">https://jag-icpc.org/?2020%%2FTeams%%2FList</a> (Last Update: %s)</p>
<p><b>情報の真偽に対する一切の責任を負いません</b></p>
%s
</body>
</html>
""" % (datetime.datetime.now(), df_html)

with open('index.html', 'w') as f:
    f.write(complete_html)
