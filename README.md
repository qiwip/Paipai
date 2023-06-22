# 拍沪牌助手

## 简单说明
在github上搜到了一些仓库，有些标记不能用了，有些实现了简单的功能，比如用键盘某些键替代鼠标操作。有点用，但是还不够，尤其是没有自动提交的功能。策略定了之后，在精确的时间点提交才是最重要的。所以写了个简单的脚本，有更好的思路可以自行改造。主要原理：使用```Selenium```操作网页，在出价页面自动填充设定的值并点击确定，进入验证码页面，人工输入验证码后，到达设定的出价时间后自动提交(仅最后一次出价会自动提交)。为了提升时间准确性，运行时会结合NTP时间来确定系统时间，防止本地时间误差较大。

## 使用步骤
因为我用的windows系统，下述均为windows的路径或操作，MAC理论可行自行摸索。
### 1.配置浏览器
拍牌站点仅支持Edge和Firefox，对比之下选择实现了Edge版本（Firefox可自行修改，难度不大）。<br>
使用```Selenium```连接并控制Edge，必须以debug模式打开浏览器：
* [Edge打开debug端口介绍](https://blog.csdn.net/m0_72760466/article/details/128748358)
* [Microsoft Edge 开发工具协议](https://learn.microsoft.com/zh-cn/microsoft-edge/devtools-protocol-chromium/)

可以按csdn帖子的方式打开debug端口，但是每次都要进命令行启动Edge，成本不大。如果想以后用Selenium做更多的事，推荐修改Edge快捷方式里的启动命令，把打开debug端口加到快捷方式里。
```"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --remote-debugging-port=9222```。启动的Edge是否打开debug端口，可以通过访问[http://127.0.0.1:9222/json/list](http://127.0.0.1:9222/json/list)验证。
<br>可能遇到的问题：
* 启动Edge前需要关闭所有Chrome和Edge窗口，否侧自测无法开启debug端口。
* 第二次拍牌使用时发现，最新版Edge会同步Chrome信息包括Chrome插件，但是又会报某些插件被拦截，导致Python脚本获取不到当前打开的正确的页面，只能通过卸载Chrome，并重置Edge设置解决。

**注意，打开debug端口是最重要的一步，如果有问题请自行解决，无法打开debug跟脚本无关，咨询这个不会回复^_^**

### 2.安装依赖的包
这里假设你已经安装了Python3和pip
```shell
cd paipai
pip install -r requirements.txt
```

### 3.配置webdriver
去微软官方网站下载Microsoft Edge的webdriver，[Edge webdriver下载地址](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/#downloads)，找到对应版本下载，解压后得到一个msedgedriver.exe
然后可以将msedgedriver.exe放到某个文件夹中，然后将路径配置到环境变量中，或者直接丢到```C:\Windows```。注意下载的版本需要和你的Edge版本一致。

### 3.配置策略
脚本实现了两次出价：第一次出价后手动确认(主要考虑是第一次出价的提交时间不需要太精确，所以手动点确认，请务必在第二次出价时间之前把第一次出价提交或取消)，第二次出价后，等待到设置的时间(如29分56秒)会自动确认。
配置部分都直接放在代码里了,主要配置项有加价值和出价时间

### 4.运行
```shell
python paipai.py
```
为了让大家能提前在模拟拍牌网站提前熟悉下脚本操作，复制了一份改了一个```paipai_simulator```。可以自行练习，这个里面的时间不准确，主要用于熟悉流程，不用关注准不准。
```shell
python paipai_simulator.py
```

最后，提前预祝大家顺利中标，如果觉得脚本有用，欢迎拍到牌再回来给个赞赏。
<img decoding="async" src="img/qrcode.png" width="50%">
