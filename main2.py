"""不打印日志版"""
import requests as r
import time
import config
from urllib.parse import quote

class CloudMusic:
    def __init__(self,api,cookie):
        self.api = api
        self.cookie = cookie
        self.s=r.session()

    def get(self,url):
        # 对 cookie 进行 URL 编码，避免里面的特殊符号（如 %、;、=）扰乱网址解析
        safe_cookie = quote(self.cookie, safe='')
        sep = '&' if '?' in url else '?'
        full_url = self.api + url + sep + 'cookie=' + safe_cookie
        return self.s.get(full_url)

    def login(self):
        """用cookie验证登录状态"""
        res = self.get('/login/status')
        data=res.json()
        print('登录状态返回：', data)
        profile = data.get('data', {}).get('profile')
        if profile:
            return profile.get('userId')
        return None

    def createMusicList(self,name):
        """创建歌单"""
        res=self.get('/playlist/create?name=%s'%name)
        data=res.json()
        id=data.get('id')
        return id

    def getDaySend(self):
        """获取每日推荐"""
        res=self.get('/recommend/songs')
        data=res.json()
        recommend=data.get('recommend')
        ids=[]
        for item in recommend:
            ids.append(str(item.get('id')))
        return ids[::-1]

    def addMusicToList(self,list_id,music_ids):
        """添加歌单歌曲"""
        res=self.get('/playlist/tracks?op=add&pid=%s&tracks=%s'%(list_id,music_ids))
        data=res.json()
        if data.get('code')==200:
            return True
        return False

    def removeMusicFromList(self,list_id,music_ids):
        """删除歌单歌曲"""
        res=self.get('/playlist/tracks?op=del&pid=%s&tracks=%s'%(list_id,music_ids))
        data=res.json()
        if data.get('code')==200:
            return True
        return False

    def getMusicListDetail(self,list_id):
        """获取歌单详情"""
        res=self.get('/playlist/detail?id=%s'%list_id)
        data=res.json()
        playlist=data.get('playlist')
        if not playlist:
            return []
        tracks=playlist.get('tracks')
        ids=[]
        for item in tracks:
            ids.append(str(item.get('id')))
        return ids

    def getUserMusicList(self,uid):
        """获取用户歌单"""
        res=self.get('/user/playlist?uid=%s'%uid)
        data=res.json()
        playlist=data.get('playlist')
        if not playlist:
            return []
        detail={}
        for item in playlist:
            id=item.get('id')
            name=item.get('name')
            if id and name:
                detail[name]=str(id)
        return detail

    def qiandao(self):
