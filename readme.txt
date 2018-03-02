改项目是模仿着tinkerpatch平台写的，偷了个懒直接连页面都是照着扣的，毕竟不是商用只是公司内部用的


1、创建数据库
create database `tinkerpatch` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
（必须设置character，否则报错）

2、生成迁移脚本
python manage.py makemigrations [app]
app为对应的应用名称；app参数不存在是则默认为所有的适合条件的app

3、迁移数据
python manage.py migrate

4、创建后台超级管理员
python manage.py createsuperuser

5、运行系统
python manage.py runserver

