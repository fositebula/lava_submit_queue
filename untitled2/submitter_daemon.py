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
import os

PID_FILE = "submitter.pid"

JOB_SOURCE_URL = "http://10.0.70.33:8000/lava_submit/poptmp/"
UPDATE_JOB_SOURCE_URL = "http://10.0.70.33:8000/lava_submit/updatetmp/"
LOG_FILE = "./lava_submitter.log"
LOG_LEVEL = logging.INFO
logger = logging.getLogger(__name__)

TO_SOMEONE = ["dongpl@spreadst.com"]
MAIL_COUNT = "pl.dong@spreadtrum.com"
SMPT_HOST = "10.0.1.200"
SMPT_PORT = 587
DOCMD = "ehlo"
PASSWD = "123@afAF"

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


def mail_init():
    server = smtplib.SMTP('10.0.1.200', 587)
    server.docmd(DOCMD, MAIL_COUNT)
    server.starttls()
    server.login(MAIL_COUNT, PASSWD)
    return server

def send_mail(mail_obj, sub, content, send_mail_list):
    try:
        msg = MIMEMultipart()
        msg['From'] = MAIL_COUNT
        msg['To'] = COMMASPACE.join(send_mail_list)
        msg['Subject'] = sub
        con = MIMEText(content, 'html', 'utf-8')
        msg.attach(con)
        mail_obj.sendmail(MAIL_COUNT, send_mail_list, msg.as_string())
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
        traceback.print_exc()
        logger.error(traceback.format_exc())
        raise e

def get_time_stamp():
    ltime = time.localtime()
    return time.strftime("%Y%m%d%H%M%S", ltime)

def get_random_str():
    return "".join(random.sample(list("abcdefghigklmnop"), 5))

def call_submitter(data, mail):
    print data
    if "No data" in data:
        #logger.info(data)
        return
    mail_obj = mail
    try:
        cmd_parm = ["python", "submit_job_168_v2.py", data["branch"], data["project"], data["build_id"], data["submit_user"], data["verify_url"],
                    data["gerrit_id"], data["port"], data["compile_user"], data["module"], data["test_cases"],
                    data["manual_test_case"], data["phone_number"],  data["test_description"], data["project_num"],
                    data["test_task_type"]]
        log = subprocess.Popen(cmd_parm, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out_log = log.stdout.read()
        err_log = log.stderr.read()

        log_file_name = "submitting_log/{}_{}_{}".format(get_time_stamp(), get_random_str(), data["build_id"])
        jobid = ""
        if out_log:
            find_job = re.findall("jobid:\((\d*)\)", out_log, re.S)
            if len(find_job) != 0:
                jobid = find_job[0]
                log_file_name = log_file_name + "_" + jobid
        running_log = "{}.log".format(log_file_name)
        with open(running_log, 'w') as fd:
            fd.write("*****************>>>out log<<<*****************\n")
            fd.write(out_log)
            fd.write("\n")
            fd.write("*****************>>>err log<<<*****************\n")
            fd.write(err_log)
            os.fsync(fd)
        update_django_submit(id=data.get("id"), jobid=jobid, running_log=running_log)
    except Exception as e:
        traceback.print_exc()
        content = "<b>%s</b><br>"%e.message
        content += "<p>%s</p>"%traceback.format_exc()
        subject = "%s submit occur some error!"%data.get("build_id")
        send_mail(mail_obj, subject, content, TO_SOMEONE)

def main():
    logger_init()
    mail = mail_init()
    logger.info("********************* >>>main starting<<< *********************")
    while True:
        j_data = get_job()
        call_submitter(j_data, mail)
        time.sleep(CIRCLE)

if __name__ == "__main__":
    p = Process(target=main)
    p.start()
    print p.pid
    with open(PID_FILE, "w") as fd:
        fd.write(str(p.pid))