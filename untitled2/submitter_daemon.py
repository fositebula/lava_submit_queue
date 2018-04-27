import re
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtpd import COMMASPACE
from multiprocessing import Process

import requests
import time
import logging
import logging.handlers
import json
import subprocess
import random
import smtplib

PID_FILE = "submitter.pid"

JOB_SOURCE_URL = "http://10.0.70.63/lava_v2/lava_submit/poptmp/"
UPDATE_JOB_SOURCE_URL = "http://10.0.70.63/lava_v2/lava_submit/updatetmp/"
LOG_FILE = "./lava_submitter.log"
LOG_LEVEL = logging.INFO
logger = logging.getLogger(__name__)

TO_SOMEONE = ["dongpl@spreadst.com"]
MAIL_ACCOUNT = "pl.dong@spreadtrum.com"
PASSWD = "123@afAF"
MAIL_FROM = "LAVA Submitter <pl.dong@unisoc.com>"
SMPT_HOST = "smtp.unisoc.com"
SMPT_PORT = 587
DOCMD = "ehlo"

CIRCLE = 18

def update_django_submit(**kwargs):
    id = kwargs.get("id")
    jobid = kwargs.get("jobid")
    log = kwargs.get("running_log")
    data = {"id":id, "jobid":jobid}
    files = [('log', (log, open(log, 'rb')))]

    res = requests.post(UPDATE_JOB_SOURCE_URL, data=data, files=files)

    if res.status_code == 200:
        logger.info("update successfully: {} {} {}".format(id, jobid, log))
        return 200
    else:
        logger.error("update fail: {} {} {}, response code {}".format(id, jobid, log, res.status_code))
        return res.status_code

def send_mail(sub, content, send_mail_list):
    try:
        mail_obj = smtplib.SMTP(SMPT_HOST, SMPT_PORT)
        mail_obj.docmd(DOCMD, MAIL_ACCOUNT)
        mail_obj.starttls()
        mail_obj.login(MAIL_ACCOUNT, PASSWD)
        msg = MIMEMultipart()
        msg['From'] = MAIL_FROM
        msg['To'] = COMMASPACE.join(send_mail_list)
        msg['Subject'] = sub
        con = MIMEText(content, 'html', 'utf-8')
        msg.attach(con)
        mail_obj.sendmail(MAIL_ACCOUNT, send_mail_list, msg.as_string())
        mail_obj.quit()
    except:
        traceback.print_exc()
        logger.error(traceback.format_exc())


def logger_init():
    logger.setLevel(level = LOG_LEVEL)
    handler = logging.FileHandler(LOG_FILE)
    handler.setLevel(LOG_LEVEL)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def get_job():
    try:
        job_info = requests.get(JOB_SOURCE_URL).content
        logger.info(job_info)
        job_ret = json.loads(job_info)
        return job_ret
    except ValueError:
        return job_info
    except Exception as e:
        send_mail('Submit Daemon Exception', traceback.format_exc(), TO_SOMEONE)
        logger.error(traceback.format_exc())
        raise e

def get_time_stamp():
    ltime = time.localtime()
    return time.strftime("%Y%m%d%H%M%S", ltime)

def get_random_str():
    return "".join(random.sample(list("abcdefghigklmnop"), 5))

def call_submitter(data):
    print data
    if "No data" in data or len(data) == 0:
        logger.info("No Data From Lava Queue server.")
        print "No Data From Lava Queue server."
        return
    try:
        cmd_parm = ["python", "submit_job_168_v2.py", data["branch"], data["project"], data["build_id"], data["submit_user"], data["verify_url"],
                    data["gerrit_id"], data["port"], data["compile_user"], data["module"], data["test_cases"],
                    data["manual_test_case"], data["phone_number"],  data["test_description"], data["project_num"],
                    data["test_task_type"]]

        out_log_file_name = "submitting_log/{}_{}_{}_out".format(get_time_stamp(), get_random_str(), data["build_id"])
        out_fd = open(out_log_file_name, 'wrb')
        err_log_file_name = "submitting_log/{}_{}_{}_err".format(get_time_stamp(), get_random_str(), data["build_id"])
        err_fd = open(err_log_file_name, 'wrb')

        log = subprocess.Popen(cmd_parm, stdout=out_fd, stderr=err_fd)
        logger.info("submit_job_168_v2.py PRAM: %s"%str(data))
        logger.info("PID: %s"%str(log.pid))
        log.wait()
        if log.returncode != 0:
            update_django_submit(id=data["id"], jobid="", running_log=err_log_file_name)
            content = "<b>submit_job_168_v2.py</b><br>"
            content += "<p>%s</p>"%log.returncode
            subject = "%s submit occur some error!"%data.get("build_id")
            send_mail(subject, content, TO_SOMEONE)
            update_django_submit(id=data["id"], jobid="", running_log=err_fd.name)
        else:
            update_django_submit(id=data["id"], jobid="", running_log=out_fd.name)

    except:
        send_mail('Submit Daemon Exception', traceback.format_exc(), TO_SOMEONE)
        traceback.print_exc()

def main():
    logger_init()
    logger.info("********************* >>>main starting<<< *********************")
    while True:
        j_data = get_job()
        call_submitter(j_data)
        time.sleep(CIRCLE)

if __name__ == "__main__":
    p = Process(target=main)
    p.start()
    print p.pid
    with open(PID_FILE, "w") as fd:
        fd.write(str(p.pid))
    p.join()