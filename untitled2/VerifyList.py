import requests

URLS = [
    'http://cmverify.spreadtrum.com:8080/jenkins/view/Verify/job/gerrit_do_verify_sprdroid8.x/build?delay=0sec',
]

def get_html():
    for url in URLS:
        res = requests.get(url)
        return res.content

if __name__ == '__main__':
    print get_html()