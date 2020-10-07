#coding:utf-8
import unittest
import os,time,sys
import HTMLReport
from common.send_msg import custom_config_send_email

# 项目根目录
base_dir = os.getcwd()

#待执行用例的目录
def allcase():
    case_path=os.path.join(base_dir,'testcases/test_oa')
    testcase=unittest.TestSuite()
    discover=unittest.defaultTestLoader.discover(case_path,
                                                 pattern='test*.py',
                                                 top_level_dir=None)
    #discover方法筛选出来的用例，循环添加到测试套件中
    for test_suite in discover:
        for test_case in test_suite:
            #添加用例到testcase
            testcase.addTest(test_case)
    return testcase


if __name__=="__main__":
    # 邮件接收人
    # receiver = sys.argv[1]
    # receiver = receiver.split(',')

    receiver = ['465397470@qq.com']
    report_name = time.strftime('%Y%m%d_%H%M%S')
    runner = HTMLReport.TestRunner(report_file_name=report_name,  # 报告文件名，如果未赋值，将采用“test+时间戳”
                                   output_path='report/oa',  # 保存文件夹名，默认“report”
                                   title='OA常规检查',  # 报告标题，默认“测试报告”
                                   description='对OA系统主要功能进行常规验证',  # 报告描述，默认“测试描述”
                                   thread_count=1,  # 并发线程数量（无序执行测试），默认数量 1
                                   thread_start_wait=3,  # 各线程启动延迟，默认 0
                                   sequential_execution=False,  # 是否按照套件添加(addTests)顺序执行，
                                   # 会等待一个addTests执行完成，再执行下一个，默认 False
                                   # 如果用例中存在 tearDownClass ，建议设置为True，
                                   # 否则 tearDownClass 将会在所有用例线程执行完后才会执行。
                                   # lang='en'
                                   lang='cn'  # 支持中文与英文，默认中文
                                   )
    # 执行测试用例套件
    result = runner.run(allcase())
    if result.failure_count > 0 or result.error_count > 0:
        run_status = False
    else:
        run_status = True
    report_filepath = os.path.join(os.getcwd(), 'report/oa/%s.html'%report_name)
    custom_config_send_email(report_filepath, receiver, run_status)
