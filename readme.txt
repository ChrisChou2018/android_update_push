初始安装连接测试数据库，修改GlobalSettings/setting DATABASES设置，测试mysql地址为192.168.1.22，端口3306，账号密码均为root
1、创建数据库
create database `UBOX_db` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
（必须设置character，否则报错）

2、生成迁移脚本
python manage.py makemigrations [app]
app为对应的应用名称；app参数不存在是则默认为所有的适合条件的app

3、迁移数据
python manage.py migrate

4、初始化图片尺寸
python manage.py initial_photosizes

5、创建后台超级管理员
python manage.py createsuperuser

6、运行系统
python manage.py runserver

