# XDU-Energy-System-small-script

## 这是什么？

​	检查对应电表账户的余额，小于15度时向配置文件`credentials.json`中的收件人（`receivers`记录的值）发送提醒邮件

​	部署到服务器上后配合宝塔面板的计划任务功能，可实现定时检查

## 开始使用

​	使用此脚本`Python`需要安装`libxduauth`模块

​	将对应信息填写至配置文件`credentials.json`

`以qq邮箱为例`

```
	"ELEC_USERNAME" : "",	//电费账户
    "ELEC_PASSWD": "",	//电费账户密码
    "host_server": "smtp.qq.com",	//qq邮箱的smtp服务器
    "sender_qq":"",	//发送者的qq号
    "pwd" : "",	//发送者邮箱授权码
    "sender" : "",	//发送者的邮箱
    "mail_subject" : "xxx寝室快没电啦（小于15度时本邮件才被发送），要交电费啦。",	//邮件标题
    "receivers" : ""	//收件人邮箱
```

​	即可







