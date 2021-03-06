# WELCOME
欢迎使用“钱笔记”小软件！这里是使用指南：  
“钱笔记”是一款简（jian）单（lou）的记账软件，它可以帮助你轻松地给过去的收支做个笔记，同时规划未来的收支。打开“钱笔记”你会看到：  
![钱笔记主界面展示的信息](https://scontent.flhr4-1.fna.fbcdn.net/v/t1.0-9/120201730_981681605632413_4419689436265402525_n.jpg?_nc_cat=106&_nc_sid=730e14&_nc_ohc=CLZF-kV6AQoAX_ACEk5&_nc_ht=scontent.flhr4-1.fna&oh=bbfcc36fee11b4e43b4772f176591643&oe=5F958190)  
【img-1 钱笔记主界面展示的信息】  
它会展示你最近的余额，分析一段时间的具体收支状况，还能帮你制定未来的收支计划。我们下面来看看具体该怎么使用：

# 首次启动
“钱笔记“在首次启动时，请选择使用语言（支持中文与英文），并选择基础记账货币单位。  
![选择语言与记账货币单位](https://scontent.flhr4-1.fna.fbcdn.net/v/t1.0-9/120222039_981681595632414_4167018673430069392_n.jpg?_nc_cat=106&_nc_sid=730e14&_nc_ohc=vbbd2bl_0IwAX8uXbi2&_nc_ht=scontent.flhr4-1.fna&oh=b338fbcb6086608dca3c6e28b71b05fa&oe=5F92F75E)  
【img -2 选择语言与记账货币单位】

# 建立时间块
时间块是“钱笔记”的基础记账单位，一个时间块代表了一段时间内的收支情况，其中包括时间段、总收支和具体的收支分类等信息。  
初始化完成后，程序将建立你第一个时间块。之后在程序主界面你可以通过输入“c”来建立更多的时间块。  
在这里，输入开始和结束时间，然后输入余额和总收支。  
在录入余额和收支时，你可以用加号“+“来连接多笔录入，如“3000 + 5000”。  
而在数额后面加上其他货币代码，如”5000 + 300 GBP“，程序会根据实时汇率将300英镑换算为你的基础货币。   
![录入时间余额总收支等信息](https://scontent.flhr4-2.fna.fbcdn.net/v/t1.0-9/120130746_981681598965747_3686618327456559972_n.jpg?_nc_cat=111&_nc_sid=730e14&_nc_ohc=fIGX2eZNLr8AX-IUvEH&_nc_ht=scontent.flhr4-2.fna&oh=c0a71c54fe62ac9c43aa75c23dbfaff1&oe=5F9460FB)  
【img-3 录入时间余额总收支等信息】  
完成输入后，根据菜单提示，记录你具体的收支分类，这里记录的信息会最终会显示在程序主界面中：  
![记录收支分类的界面](https://scontent.flhr4-2.fna.fbcdn.net/v/t1.0-9/120231944_981681648965742_6185699462404596599_n.jpg?_nc_cat=109&_nc_sid=730e14&_nc_ohc=JKW61zzXr9UAX_9tFgM&_nc_ht=scontent.flhr4-2.fna&oh=81018e40b5ffe318381d2fbdc9515796&oe=5F948152)  
【img-5 记录收支分类的界面】  
这时你可以根据自己的账单给这段时间的收支做个笔记，正数为收入，负数为支出。  
在数额后加上货币代码（如 + 吃饭 15 GBP）可进行货币转换，输入“n + 备注”可以添加备注。  
当全部录入完成，输入f便可结束输入。  
在程序主界面，输入“m + 空格 + 时间块代码”可修改一个时间块；输入“d + 空格 + 时间块代码”可删除一个时间块。  
输入“s + 空格 + 时间块代码”可查看一个或多个时间块的统计。  
![多个时间块统计](https://scontent.flhr4-2.fna.fbcdn.net/v/t1.0-9/120233915_981681705632403_2742498295101731314_n.jpg?_nc_cat=103&_nc_sid=730e14&_nc_ohc=d_7SgbonF6UAX-z7Puw&_nc_ht=scontent.flhr4-2.fna&oh=4e0e5b391c66e829871cb0f86a337d9d&oe=5F92C77F)    
【img-7 多个时间块统计】

# 建立计划块
计划块是用来规划未来可预知的收支项目，让你对未来的所剩余额一目了然。  
![计划块展示未来可预知的收支](https://scontent.flhr4-1.fna.fbcdn.net/v/t1.0-9/120246488_981681695632404_1435386818964876334_n.jpg?_nc_cat=104&_nc_sid=730e14&_nc_ohc=KTQ1FCKFiG0AX8vcZ6v&_nc_ht=scontent.flhr4-1.fna&oh=82b2f82ad1ec8fc7ae7241cf2790b432&oe=5F930876)  
【img-6 计划块展示未来可预知的收支】  
输入“+”建立一个计划块，输入“- + 空格 + 代码”删除一个计划块。  
之后程序主界面会显示所有未来的计划收支，而过去的计划收支会被自动隐藏。  

# 其他
程序会在每次你打开和关闭时，各自动建立备份，备份可在memo_backup文件夹中找到。如果手滑删错东西，可通过用备份恢复。  
不幸的是，exe文件会被系统报毒。原因是所使用的封装程序pyinstaller经常被用来制作病毒，所以杀毒软件将所有用该封装程序制作且不带签名的程序自动归类为病毒。  
解决方法是将该程序加入系统杀毒软件白名单，或者直接用python运行 .py script。  

Sept 2020  
By Tianci

# 欢迎关注我的公众号：Tianci Says  
![公众号二维码](https://scontent.flhr4-2.fna.fbcdn.net/v/t1.0-9/120201725_981686538965253_4553260194552814877_o.jpg?_nc_cat=103&_nc_sid=730e14&_nc_ohc=2jfsTPkiI9sAX9ovl1H&_nc_ht=scontent.flhr4-2.fna&oh=147c097df57f78de9c98da09c64c83bd&oe=5F94422C)
 



