# 拍沪牌助手

## 简单说明
在github上搜到了一些仓库，有些标记不能用了，有些实现了简单的功能，比如用键盘某些键替代鼠标操作，有点用，但是还是不好用。尤其是没有自动提交的功能，策略定了之后，在精确的时间点提交才是最重要的。所以写了个简单的脚本，有更好的思路可以自行改造。主要原理：使用```Selenium```操作网页，在出价页面自动填充设定的值并点击确定，进入验证码页面，人工输入验证码后，到达设定的出价时间后自动提交(仅最后一次出价会自动提交)。为了提升时间准确性，运行时会结合NTP时间来确定系统时间，防止本地时间误差较大。

## 使用步骤
### 1.配置浏览器
拍牌站点仅支持Edge和firefox，对比之下选择实现了Edge版本，Firefox可自行修改。使用Python控制浏览器，必须以debug模式打开浏览器：
* [Edge打开debugger端口介绍](https://blog.csdn.net/m0_72760466/article/details/128748358)
* [Microsoft Edge 开发工具协议](https://learn.microsoft.com/zh-cn/microsoft-edge/devtools-protocol-chromium/)

可以按帖子的方式打开debugger端口，但是每次都要进命令行启动Edge。所以推荐修改Edge快捷方式里的启动命令，把打开debugger端口加到快捷方式里。
```"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --remote-debugging-port=9222```, 启动的Edge是否打开debugger端口，可以通过访问[http://127.0.0.1:9222/json/list](http://127.0.0.1:9222/json/list)验证。实际使用时发现，最新版Edge会同步Chrome信息包括chrome插件，但是又会报某插件被拦截，导致Python脚本获取不到当前打开的正确的页面，只能通过卸载Chrome，重置Edge设置解决。
### 2.下载脚本并安装所需包
```shell
cd paipai
pip install -r requirements.txt
```

### 3.配置策略
脚本实现了两次出价：第一次出价后手动确认(主要考虑是第一次出价的提交时间不需要太精确，所以手动确认)，第二次出价后，等待到时间(如29分56秒)自动确认。
配置部分都直接放在代码里了,主要配置项有加价值和出价时间

### 4.运行
```shell
python paipai.py
```