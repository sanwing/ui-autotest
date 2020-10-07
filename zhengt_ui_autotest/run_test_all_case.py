#coding:utf-8
import unittest
import os,time,sys
import HTMLReport

# 项目根目录
base_dir = os.getcwd()

#待执行用例的目录
def allcase():
    case_path=os.path.join(base_dir, 'testcases/test_test')
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
    # OA session
    # unittest.TestCase.variables = {'h3bpmportal': sys.argv[1]}
    #     # # 邮件接收人
    #     # receiver = sys.argv[2]
    #     # receiver = receiver.split(',')
    # receiver = ['465397470@qq.com']
    # unittest.TestCase.variables = {'h3bpmportal': 'E8B9C62C74DC498569F8E36615459585'}

    # # 设置报告路径
    # if sys.platform == 'win32':
    #     report_path = os.path.join(base_dir, 'report/test/%s.html'%(time.strftime('%Y%m%d_%H%M%S')))
    # else:
    #     report_path = '/home/zhengt_ui_autotest/report/test/%s.html'%(time.strftime('%Y%m%d_%H%M%S'))
    # fp = open(report_path,"wb")

    runner = HTMLReport.TestRunner(report_file_name=time.strftime('%Y%m%d_%H%M%S'),  # 报告文件名，如果未赋值，将采用“test+时间戳”
                                   output_path='test',  # 保存文件夹名，默认“report”
                                   title='测试报告',  # 报告标题，默认“测试报告”
                                   description='无测试描述',  # 报告描述，默认“测试描述”
                                   thread_count=1,  # 并发线程数量（无序执行测试），默认数量 1
                                   thread_start_wait=3,  # 各线程启动延迟，默认 0 s
                                   sequential_execution=False,  # 是否按照套件添加(addTests)顺序执行，
                                   # 会等待一个addTests执行完成，再执行下一个，默认 False
                                   # 如果用例中存在 tearDownClass ，建议设置为True，
                                   # 否则 tearDownClass 将会在所有用例线程执行完后才会执行。
                                   # lang='en'
                                   lang='cn'  # 支持中文与英文，默认中文
                                   )
    # 执行测试用例套件
    runner.run(allcase())


    # # 执行测试
    # runner=HTMLTestRunner.HTMLTestRunner(stream=fp,
    #                                      title="OA-UI自动化测试报告",
    #                                      description="用例执行情况：")
    # result = runner.run(allcase())
    # failure_count = result.failure_count
    # run_result = True if failure_count == 0 else False
    # if run_result:
    #     print('所有用例测试通过')
    # else:
    #     print('失败的用例数量[%d]'%failure_count)
    # fp.close()
    # 发送邮件
    # main(report_path, receiver, run_result)
