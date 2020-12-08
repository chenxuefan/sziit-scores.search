## 技术栈 🀄️

- Django
- requests
- rsa
- nginx

## 项目简介 ➖

此项目旨在「**方便同学查询学科成绩**」，以往查询成绩的方式主要为

1. 登录教务系统，查看成绩，需要连接学校内网，过程较为繁琐
2. 登录今日校园app，较方便，不过会遇到找不到入口的问题
3. 校内公众号后台入口，也很OK

本项目亮点 - 省去了中间的繁琐环节，**仅通过一个网址入口登录，即可跳转成绩页面，显示在校所有科目的成绩及对应学分等**，成绩数据来源为学校教务系统，戳👇

- 查询地址 - 「[https://scores.search.billie52707.cn/](https://scores.search.billie52707.cn/)」

- 项目仓库 - 「[https://github.com/chenxuefan/sziit-scores.search](https://github.com/chenxuefan/sziit-scores.search)」

## 项目截图 🤚

![image-20201208223301976](https://billie-s-album.oss-cn-beijing.aliyuncs.com/img/image-20201208223301976.png)/*查询页面，背景为学校内景*/

![image-20201208223403560](https://billie-s-album.oss-cn-beijing.aliyuncs.com/img/image-20201208223403560.png)/*查询结果页面*/

## CentOS7下部署Django项目 🧵

技术栈 - **centos7+nginx+uwsgi+python3+django**

做好了整个Django项目就可以上线到服务器了，**服务器**是阿里云的，**域名**是用之前的域名申请的二级域名，具体的流程参考这篇官方文档 - 「[https://www.django.cn/article/show-4.html#banqian](https://www.django.cn/article/show-4.html#banqian)」

整个部署过程简单概括分三块 - django、uwsgi、nginx

1. 将做好的项目上传到服务器之后，部署运行这个项目所需的环境，最后能够让这个Django项目能够运行起来

2. 配置uwsgi，在项目根目录下创建`mysite.xml`文件，添加如下代码，运行此文件

   ```
   <uwsgi>    
      <socket>127.0.0.1:8997</socket> <!-- 内部端口，自定义 --> 
      <chdir>/data/wwwroot/mysite/</chdir> <!-- 项目路径 -->            
      <module>mysite.wsgi</module>  <!-- mysite为wsgi.py所在目录名--> 
      <processes>4</processes> <!-- 进程数 -->     
      <daemonize>uwsgi.log</daemonize> <!-- 日志文件 -->
   </uwsgi>
   ```

3. 添加nginx配置文件，即配置`nginx.conf`文件，具体代码参考上方的文档，其中的对应参数需参考上一步的代码，这个过程为使得文件生效，需重启nginx和uwsgi服务，用到的命令：

   ```shell
   systemctl start/stop/restart nginx #启动/关闭/重启nginx
   service nginx start/stop/restart #启动/关闭/重启nginx
   killall nginx #杀死所有nginx进程
   
   uwsgi -x mysite.xml #运行xml文件
   killall uwsgi #杀死所有uwsgi进程
   ```

完结撒花 🌹