"""不打印日志版"""
import requests as r
import time
import config

class CloudMusic:
    def __init__(self,api,phone,password):
        self.api = api
        self.phone=phone
        self.password=password
        self.s=r.session()

    def get(self,url):
        return self.s.get(self.api+url)

    def login(self):
        """登录"""
        res = self.get('/login/cellphone?phone=%s&password=%s' % (self.phone, self.password))
        data=res.json()
        if data.get('account'):
            return data.get('account').get('id')
        return None

    def refresh(self):
        """刷新登录状态"""
        res=self.get('/login/refresh')
        data=res.json()
        if data.get('code')==200:
            return True
        print(data)
        return False

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
        """签到"""
        res = self.get('/daily_signin')
        data = res.json()
        print(data)



"""不打印日志版"""
import requests as r
import time
import config

class CloudMusic:
    def __init__(self,api,phone,password):
        self.api = api
        self.phone=phone
        self.password=password
        self.s=r.session()

    def get(self,url):
        return self.s.get(self.api+url)

    def login(self):
        """登录"""
        res = self.get('/login/cellphone?phone=%s&password=%s' % (self.phone, self.password))
        data=res.json()
        if data.get('account'):
            return data.get('account').get('id')
        return None

    def refresh(self):
        """刷新登录状态"""
        res=self.get('/login/refresh')
        data=res.json()
        if data.get('code')==200:
            return True
        print(data)
        return False

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
        """签到"""
        res = self.get('/daily_signin')
        data = res.json()
        print(data)


if __name__=='__main__':
    api=config.api
    phone=config.phone
    password=config.password
    print('开始登录')
    cm=CloudMusic(api,phone,password)
    uid=cm.login()
    if not uid:
        print('登录失败')
        exit(0)
    print('【uid=%s】'%uid)
    try:
        print('开始签到')
        cm.qiandao()
        print('开始处理日推歌单')
        if int(time.strftime('%H'))<8:
            print('不到8点，不处理')
            exit(0)

        list_name = '每日推荐'  # 固定歌单名，不再带日期
        print('固定歌单名 list_name=%s' % list_name)
        user_music_list = cm.getUserMusicList(uid)
        if list_name in user_music_list:
            print('已有固定歌单：%s' % list_name)
            list_id = user_music_list[list_name]
        else:
            print('创建固定歌单：%s' % list_name)
            list_id = cm.createMusicList(list_name)
        print('歌单id list_id=%s' % list_id)

        # 先清空歌单里的旧歌
        old_music_ids = cm.getMusicListDetail(list_id)
        if len(old_music_ids) > 0:
            old_ids_str = ','.join(old_music_ids)
            cm.removeMusicFromList(list_id, old_ids_str)
            print('已清空旧歌曲：%s' % old_ids_str)
        else:
            print('歌单目前是空的，无需清空')

        # 获取今天的日推并全部加入
        print('获取日推歌曲：')
        day_music_ids = cm.getDaySend()
        print(day_music_ids)
        if len(day_music_ids) > 0:
            music_ids = ','.join(day_music_ids)
            res = cm.addMusicToList(list_id, music_ids)
            if res:
                print('添加日推列表：%s【成功】' % (music_ids))
            else:
                print('添加日推列表：%s【失败】' % (music_ids))
    except:
        print('error')
