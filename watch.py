import requests

url = 'https://api.lootbox.eu'


def nullfunc(*args, **kwargs):
    pass


def auth(func):
    def wrapper(*args, **kwargs):
        if args[0].user:
            return func(*args, **kwargs)
        else:
            print("User isn't authenticated, please set user.")
    return wrapper


class Watch(object):
    def __init__(self):
        self.user = None
        self.region = None
        self.platform = None
        self.a_url = url + '/{p}/{r}/{t}'

    def set_user(self, user, platform, region):
        if isinstance(user, str):
            self.user = user.replace('#', '-')
        platforms = ['pc', 'xbl', 'psn']
        if platform not in platforms:
            print("Invalid platform. Options: pc, xbl, psn")
            return
        self.platform = platform
        regions = ['us', 'eu']
        if region.lower() not in regions:
            print("Invalid region. Options: us, eu.")
            return
        self.region = region.lower()
        self.a_url = self.a_url.format(p=self.platform,
                                       r=self.region,
                                       t=self.user)

    def get_stats(self, path):
        n_url = self.a_url + path
        return requests.get(n_url).json()

    @auth
    def achievements(self):
        path = '/achievements'
        return self.get_stats(path)

    @auth
    def heroes_summary(self):
        path = '/allHeroes/'
        r1 = self.get_stats(path)
        path = '/heroes'
        r1['hero_playtimes'] = self.get_stats(path)
        return r1

    @auth
    def platforms(self):
        path = '/get-platforms'
        return self.get_stats(path)

    @auth
    def hero(self, hero):
        path = '/hero/{h}'.format(h=hero)
        return self.get_stats(path)

    @auth
    def profile(self):
        path = '/profile'
        return self.get_stats(path)

    def patch_notes(self):
        return requests.get(url + '/patch_notes').json()
