import requests

json_data = """{"parameter": [{"name": "LAVA_SERVER", "value": "10.0.70.68"},
{"name": "LAVA_USER", "value": "apuser"}, {"name": "LAVA_PASSWORD", "value": "<DEFAULT>"},
{"name": "up_build_id", "value": "%s"}, {"name": "up_jobname", "value": "%s"},
{"name": "up_verifier", "value": "%s"}, {"name": "up_build_result", "value": "pass"},
{"name": "up_change_url", "value": "%s"}, {"name": "up_module", "value": "%s"},
{"name": "build_list", "value": "%s"},
{"name": "testpara", "value": "%s"},
{"name": "test_case", "value": "%s"}, {"name": "build_type", "value": "full"},
{"name": "imgnum", "value": "%s"}, {"name": "stable", "value": "%s"},
{"name": "monkeytime", "value": "%s"}, {"name": "monkey_device_amount", "value": "%s"},
{"name": "upstream_type", "value": "%s"}], "statusCode": "303", "redirectTo": ".", "Jenkins-Crumb":"41cb5e2d8719ea8a12571f6e102b9752"}"""

def get_json_data(up_build_id, up_jobname, up_verifier, up_change_url, up_module, build_list, testpara,\
				  test_case, imgnum, stable, monkeytime,  monkey_device_amount, upstream_type):

	str = json_data%(up_build_id, up_jobname, up_verifier, up_change_url, up_module, build_list, testpara,\
				  test_case, imgnum, stable, monkeytime,  monkey_device_amount, upstream_type)
	return str

data_str = 'name=LAVA_SERVER&value=10.0.70.68&name=LAVA_USER&value=apuser&' \
		   'name=LAVA_PASSWORD&value=%3CDEFAULT%3E&name=up_build_id&' \
		   'value={up_build_id}&name=up_jobname&value={up_jobname}&' \
		   'name=up_verifier&value={up_verifier}&name=up_build_result&' \
		   'value=pass&name=up_change_url&value={up_change_url}&' \
		   'name=up_module&value={up_module}&name=build_list&value={build_list}&' \
		   'name=testpara&value={testpara}&name=test_case&value={test_case}&' \
		   'name=build_type&value={build_type}&name=imgnum&value={imgnum}&' \
		   'name=stable&value={stable}&name=monkeytime&value={monkeytime}&' \
		   'name=monkey_device_amount&value={monkey_device_amount}&name=upstream_type&' \
		   'value={upstream_type}&statusCode=303&redirectTo=.&' \
		   'Jenkins-Crumb=41cb5e2d8719ea8a12571f6e102b9752&json={json}&Submit=Build'
# .format(up_build_id=49588,
# 																			   up_jobname="sprdroid8.1_trunk_18b",
#                                                                                up_verifier="mingmin.ling",
#                                                                                up_change_url="http://cmverify.spreadtrum.com:8080/jenkins/job/gerrit_do_verify_sprdroid8.x/49588/",
# 																			   up_module="poweron",
#                                                                                build_list="sprdroid8.1_trunk:sp9832e_1h10_oversea-userdebug-native",
# 																			   testpara="{poweron[adbcheck,poweron]}",
#                                                                                test_case="default",
# 																			   build_type="",
#                                                                                imgnum=1,
# 																			   monkey_device_amount=1,
#                                                                                stable="latest",
# 																			   monkeytime="not",
# 																			   upstream_type="verify",
# 																			   json=json_data)

def get_query_data(up_build_id, up_jobname, up_verifier, up_change_url, up_module, build_list, testpara
                   , test_case, imgnum, monkey_device_amount, stable, upstream_type, monkeytime, json_data):
    str = data_str.format(up_build_id=up_build_id,
                   up_jobname=up_jobname,
                   up_verifier=up_verifier,
                   up_change_url=up_change_url,
                   up_module=up_module,
                   build_list=build_list,
                   testpara=testpara,
                   test_case=test_case,
                   build_type="",
                   imgnum=imgnum,
                   monkey_device_amount=monkey_device_amount,
                   stable=stable,
                   monkeytime=monkeytime,
                   upstream_type=upstream_type,
                   json=json_data)
    return str

header = {
	"Host": "10.0.64.29:8080",
	"Connection": "keep-alive",
	"Content-Length": "1980",
	"Cache-Control": "max-age=0",
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	"Origin": "http://10.0.64.29:8080",
	"Upgrade-Insecure-Requests": "1",
	"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/49.0.2623.108 Chrome/49.0.2623.108 Safari/537.36",
	"Content-Type": "application/x-www-form-urlencoded",
	"Referer": "http://10.0.64.29:8080/jenkins/job/lava_test/build?delay=0sec",
	"Accept-Encoding": "gzip, deflate",
	"Accept-Language": "zh-CN,zh;q=0.8",
	"Cookie": "JSESSIONID.7f3e4cce=node01153t9i1c32i11fsryl34gtteb77339.node0",
}

url = "http://10.0.64.29:8080/jenkins/job/lava_test/build?delay=0sec"



def resubmit(data_str):
    resp = requests.post(url=url, headers=header, data=data_str)
    return resp
