# coding=utf-8
import smtplib, time, os
import sys
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

# 发送邮箱服务器
smtpserver = 'smtp.263.net'

# 发送邮箱
sender = 'qskjzf@zhengtongauto.net'

# 发送邮箱用户/密码
username = 'qskjzf@zhengtongauto.net'
password = '123pass1'

# 发送报告时间
default_send_report_time = '08:10:00'


def send_mail_html(file, receiver):
    '''发送html内容邮件'''

    # 发送邮件主题
    t = time.strftime("%m-%d %H:%M:%S", time.localtime())
    subject = 'OA常规检查报告[%s]'% str(t)

    # 读取html文件内容
    with open(file, 'rb') as fp:
        mail_body = fp.read()

    # 组装邮件内容和标题，中文需参数‘utf-8’，单字节字符不需要
    msg = MIMEText(mail_body, _subtype='html', _charset='utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg["From"] = formataddr(["测试组",sender])
    msg['To'] = ",".join(receiver)
    # 登录并发送邮件
    try:
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver)
        smtp.login(username, password)
        smtp.sendmail(sender, receiver, msg.as_string())
    except Exception as e:
        print("邮件发送失败！")
    else:
        print("邮件发送成功！")
    finally:
        smtp.quit()


def send_mail_html_contains_attachment(file, receiver):
    '''发送html内容邮件'''

    # 发送邮件主题
    t = time.strftime("%m-%d %H:%M:%S", time.localtime())
    subject = 'OA常规检查报告[%s]'% str(t)

    # 创建一个带附件的实例
    message = MIMEMultipart()
    message['From'] = formataddr(["测试组",sender])
    message['To'] = ",".join(receiver)
    message['Subject'] = Header(subject, 'utf-8')

    # 邮件正文内容
    with open(file, 'rb') as fp:
        mail_body = fp.read()
    message.attach(MIMEText(mail_body, _subtype='html', _charset='utf-8'))

    # 构造附件
    att1 = MIMEText(open(file, 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    att1["Content-Disposition"] = 'attachment; filename="detail_report.html"'
    message.attach(att1)

    # 登录并发送邮件
    try:
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver)
        smtp.login(username, password)
        smtp.sendmail(sender, receiver, message.as_string())
    except Exception as e:
        print("邮件发送失败！")
    else:
        print("邮件发送成功！")
    finally:
        smtp.quit()



def custom_config_send_email(file, receiver, result):
    """邮件发送规则：八点运行的那次发送邮件，其余时间根据运行结果是否成功来发送邮件，成功则不发送，失败则发送"""

    # 当天八点五分时的毫秒数
    cur_date = time.strftime("%Y-%m-%d", time.localtime()) + ' %s' % default_send_report_time
    stamp1 = time.strptime(cur_date, "%Y-%m-%d %H:%M:%S")
    time1_stamp = int(time.mktime(stamp1))

    # 任务执行开始时间的毫秒数
    stamp2 = int(time.time())

    if stamp2 < time1_stamp:
        send_mail_html_contains_attachment(file, receiver)
    else:
        if not result:
            send_mail_html_contains_attachment(file, receiver)
        else:
            print('测试任务全部测试通过，不发送邮件')



if __name__ == '__main__':
    report_name = 'C:\\Users\\86173\\Desktop\\Zhengt-api-daily-check-593.html'
    report_detail_name = 'C:\\Users\\86173\\Desktop\\Zhengt-api-daily-check-1329.jtl'

    # 邮件报告路径
    report_name = sys.argv[1]
    # 邮件接收人
    receiver = sys.argv[2]



