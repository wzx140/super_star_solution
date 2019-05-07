import os
from argparse import ArgumentParser
from fetch import SuperStar

if __name__ == '__main__':
    parser = ArgumentParser(description='脚本仅供学习只用')
    group_ex = parser.add_mutually_exclusive_group()
    group_ex.add_argument('-save', type=str, nargs='?', const='cookie', help='保存登录信息，默认当前目录下cookie')
    group_ex.add_argument('-load', type=str, nargs='?', const='cookie', help='加载登录信息，默认当前目录下cookie')

    args = vars(parser.parse_args())
    star = SuperStar()
    if args['save']:
        # 这里没有判断路径合法问题
        if os.path.exists(args['save']):
            print(args['save'] + ' 已经存在')
            os._exit(0)
        star.login()
        star.save(args['save'])
        print('保存登录信息 ' + os.path.abspath(args['save']))
    elif args['load']:
        if not os.path.exists(args['load']):
            print(args['load'] + ' 路径不存在')
            os._exit(0)
        star.load(args['load'])
        print('加载登录信息 ' + os.path.abspath(args['load']))
    else:
        star.login()

    lessons = star.get_lessons()
    print('选择要学习的课程')
    for i, lesson in enumerate(lessons):
        print(str(i) + ' ' + lesson[1])

    choose = input()
    if choose.isnumeric() and 0 <= int(choose) <= len(lessons) - 1:
        star.auto_video(lessons[int(choose)])
