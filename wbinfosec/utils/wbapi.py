import requests

def comment_api(comment, mblogid):
    '''
    向评论区评论进行舆论风向引导
    :param comment: 评论内容
    :param mblogid: 博文编号
    '''
    if comment is None or comment == '' or mblogid is None or mblogid == '':
        return None
    url = 'https://api.weibo.com/2/comments/create.json'
    data = {'access_token':'TODO', 'comment':comment, 'id':mblogid, 'rip':'TODO'}
    infomation = requests.post(url = url, data = data, verify = False).text
    return infomation

if __name__ == '__main__':

    url = 'https://api.weibo.com/2/comments/create.json'

    data = {
        'access_token':'TODO',
        'comment':'TODO',
        'id':'TODO',
        'rip':'TODO'
    }
    infomation = requests.post(url = url, data = data, verify = False).text
    print(infomation)
