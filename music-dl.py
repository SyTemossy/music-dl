import argparse
import sys
import os
import urllib
import requests
import json
import random

commands = []
path = sys.path[0]
dpath = sys.path[0]
autocreate = False
netease_api = {'music_url': 'http://music.163.com/song/media/outer/url?id=',
               'playlist': 'https://api.surmon.me/music/list/',
               'detail': 'http://music.163.com/api/song/detail/?id=xxxxx&ids=[xxxxx]'}
qq_api = {'info_url': 'https://u.y.qq.com/cgi-bin/musicu.fcg?format=json&data=%7B%22req_0%22%3A%7B%22module%22%3A%22vkey.GetVkeyServer%22%2C%22method%22%3A%22CgiGetVkey%22%2C%22param%22%3A%7B%22guid%22%3A%22358840384%22%2C%22songmid%22%3A%5B%22helloworld%22%5D%2C%22songtype%22%3A%5B0%5D%2C%22uin%22%3A%221443481947%22%2C%22loginflag%22%3A1%2C%22platform%22%3A%2220%22%7D%7D%2C%22comm%22%3A%7B%22uin%22%3A%2218585073516%22%2C%22format%22%3A%22json%22%2C%22ct%22%3A24%2C%22cv%22%3A0%7D%7D'}
Illicit_Chracters = {'\\', '/', ':', '?', '|', '<', '>', '*'}
prefix = '.mp3'
check_exist = True
ar_str = ''

user_agent = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
              'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36 OPR/67.0.3575.53',
              'Mozilla/5.0 (X11; U; Linux x86_64; en-ca) AppleWebKit/531.2+ (KHTML, like Gecko) Version/5.0 Safari/531.2+',
              'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko',
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
              'Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1; Microsoft; Lumia 950) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Mobile Safari/537.36 Edge/15.14977',
              'Mozilla/5.0 (Linux; Android 7.0; SM-A310F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.91 Mobile Safari/537.36 OPR/42.7.2246.114996',
              'Mozilla/5.0(Linux;Android 5.1.1;OPPO A33 Build/LMY47V;wv) AppleWebKit/537.36(KHTML,link Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36',
              'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; F5121 Build/34.0.A.1.247) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.1.944 Mobile Safari/537.36',
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0']


class core:
    def genfake(self, type):
        ua = random.choice(user_agent)
        if type == '163':
            headers = {
                'User-Agent': ua, 'Referer': 'https://music.163.com/'}
        elif type == 'qq':
            headers = {
                'User-Agent': ua, 'Referer': 'https://y.qq.com/portal/player.html'}
        return headers

    def autocreate(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def to_legal(self, filename):
        for x in Illicit_Chracters:
            filename = filename.replace(x, ar_str)
        return filename

    def download_file(self, url, filename):
        global check_exist
        if ar:
            filename = self.to_legal(filename)
        full_path = '{}\\{}{}'.format(dpath, filename, prefix)
        if os.path.exists(full_path) and check_exist:
            while True:
                r = input(
                    '{} 已存在, 是否重新下载? [y/n/yf(对以后操作都应用)/nf(对以后操作都应用)]'.format(filename))
                if r == 'y':
                    break
                elif r == 'n':
                    return False
                elif r == 'yf':
                    check_exist = True
                    break
                elif r == 'nf':
                    check_exist = False
                    return False
        urllib.request.urlretrieve(url, full_path)
        return True


class qq:
    def getsongurl(self, ori_url):
        id = ori_url[ori_url.index('song/')+5:ori_url.index('.html')]
        headers = core().genfake('qq')
        response = requests.get(qq_api['info_url'].replace(
            'helloworld', id), headers=headers)
        js = json.loads(response.text)
        global prefix
        filename = js['req_0']['data']['midurlinfo'][0]['filename']
        prefix = os.path.splitext(filename)[1]
        sip = random.choice(js['req_0']['data']['sip'])
        purl = js['req_0']['data']['midurlinfo'][0]['purl']
        url = sip + purl
        return url

    def getsongdetail(self, url):
        from bs4 import BeautifulSoup
        headers = core().genfake('qq')
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        #body > div.main > div.mod_data > div > div.data__singer
        data = soup.select(
            'body > div.main > div.mod_data > div > div.data__name > h1')
        for item in data:
            name = item.get('title')
        data = soup.select(
            'body > div.main > div.mod_data > div > div.data__singer')
        for item in data:
            artists = item.get('title')
        if artists.find('/'):
            artists = artists.replace('/', '&')
        return '{} - {}'.format(name, artists)

    def start(self, url, type):
        if type == 0:
            print('获取歌曲信息...')
            songurl = self.getsongurl(url)
            filename = self.getsongdetail(url)
            print('开始下载{}{}'.format(filename, '...'))
            r = core().download_file(songurl, filename)
            if r == True:
                print('{}下载完毕！'.format(filename))
            elif r == False:
                print('{}已存在！'.format(filename))
        elif type == 1:
            pass
        else:
            raise Exception('Invaild URL!')
            return
        pass


class netease:

    def getsongdetail(self, id):
        headers = core().genfake('163')
        body = requests.get(netease_api['detail'].replace(
            'xxxxx', id), headers=headers)
        js = json.loads(body.content)
        if js['code'] != 200:
            raise Exception('Incorrect song ID')
        name = js['songs'][0]['name']
        artist = js['songs'][0]['artists'][0]['name']
        i = 1
        while True:
            try:
                artist += '&'+js['songs'][0]['artists'][i]['name']
                i += 1
            except:
                break
        return name+' - '+artist

    def getsongurl(self, ori_url):
        ori_url = ori_url.replace('/#', '')
        parsed_url = urllib.parse.urlparse(ori_url)
        id = urllib.parse.parse_qs(parsed_url.query)['id']
        if id[0].isdecimal:
            songurl = netease_api['music_url']+id[0]
        else:
            raise Exception('Incorrect song ID')
        return songurl, id[0]
        pass

    def getplaylist(self, ori_url):
        ori_url = ori_url.replace('/#', '')
        parsed_url = urllib.parse.urlparse(ori_url)
        id = urllib.parse.parse_qs(parsed_url.query)['id']
        if id[0].isdecimal:
            listurl = netease_api['playlist']+id[0]
        else:
            raise Exception('Incorrect playlist ID')
        body = requests.get(listurl)
        js = json.loads(body.content)
        if js['status'] != 'success':
            raise Exception(js['error'])
        trackCount = int(js['result']['trackCount'])
        playlistName = js['result']['name']
        global dpath
        dpath = core().autocreate('{}\\{}'.format(dpath, playlistName))
        print('歌单信息获取成功！\n开始下载{}'.format(playlistName))
        for x in range(0, trackCount):
            self.start('{}{}'.format(
                netease_api['music_url'], js['result']['tracks'][x]['id']), 0)
            pass

    def start(self, url, type):
        prefix = '.mp3'
        global path
        if type == 1:
            print('正在获取歌单信息...')
            self.getplaylist(url)
            pass
        elif type == 0:
            print('获取歌曲信息...')
            songurl, songid = self.getsongurl(url)
            filename = self.getsongdetail(songid)
            print('开始下载{}{}'.format(filename, '...'))
            r = core().download_file(songurl, filename)
            if r == True:
                print('{}下载完毕！'.format(filename))
            elif r == False:
                print('{}已存在！'.format(filename))
            pass
        else:
            raise Exception('Invaild URL!')
            return
        pass
    pass


def argparser(argv):
    global dpath
    global ar
    argv = argv[1:len(argv)]
    try:
        parser = argparse.ArgumentParser(description=['Produce by SyTemossy'])
        parser.add_argument(
            '--input', '-i', help='Where to Download', type=str, required=True)
        parser.add_argument('--output', '-o', help='Saved Path',
                            type=str, default=dpath, required=False)
        parser.add_argument('--AutoCreate', '-ac', action='store_true', default=True,
                            help='Auto Created Path, Only Work With -t/--to', required=False)
        parser.add_argument('--AutoReplace', '-ar', action='store_true', default=False,
                            help='Auto Replace Illicit Character\nSuch as: \\, /, :, *, ?, \", <, >, |', required=False)
        args = parser.parse_args(argv)
        i = args.input
        ar = args.AutoReplace
        dpath = args.output
        autocreate = args.AutoCreate
        print('Input: ', args.input)
        print('Output: ', args.output)
        print('AutoCreate: ', args.AutoCreate)
        print('AutoReplace: ', args.AutoReplace)
        core().autocreate(dpath)
        if i.find('music.163.com/song?id=') != -1 or i.find('music.163.com/#/song?id=') != -1:
            netease().start(i, 0)
        elif i.find('music.163.com/playlist?id=') != -1 or i.find('music.163.com/#/playlist?id=') != -1:
            netease().start(i, 1)
        elif i.find('y.qq.com/n/yqq/song/') != -1:
            qq().start(i, 0)
        else:
            raise Exception('Invaild URL')
        return True
    except Exception as e:
        print(e)
        return False
    pass


if __name__ == "__main__":
    if not sys.argv[0].endswith('.py'):
        path = os.getcwd()
        dpath = os.getcwd()
    print(argparser(sys.argv))
