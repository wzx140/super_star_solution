# super star solution
## 依赖
- Chrome
- [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)
- python, selenium
### 环境搭建
1. 安装 Chrome，ChromeDriver，将可执行文件目录添加至环境变量
2. `pip install -r requirements` 导入依赖

## 使用
`cd Super_star_solution`
```
> python -m start -h
usage: start.py [-h] [-save [SAVE] | -load [LOAD]]

脚本仅供学习只用

optional arguments:
  -h, --help    show this help message and exit
  -save [SAVE]  保存登录信息，默认当前目录下cookie
  -load [LOAD]  加载登录信息，默认当前目录下cookie
```
- 保存登录信息
```
> python -m start -save
请在100s内完成登录
登录成功
保存登录信息 ********/cookie
选择要学习的课程
0 ********
1 ********
2 ********
3 ********
```
- 加载登录信息
```
▶ python -m start -load
加载登录信息 ********/cookie
选择要学习的课程
0 ********
1 ********
2 ********
3 ********
```

## 更多
1. 脚本仅供学习之用，是作者在学习 selenium 时的实践项目
2. 脚本不会减少实际学习时间