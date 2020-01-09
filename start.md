
#### 虚拟环境   
创建conda环境django： 
```conda create -n django```
进入环境：   
```conda activate django```
退出环境：   
```conda deactivate```          

#### requirements.txt用来记录项目所有的依赖包和版本号:     
```pip freeze >requirements.txt```    

安装requirement.txt:    
```pip install -r requirements.txt```  


建立索引数据  
```python manage.py rebuild_index```

----
### Linux    
#### mysql    
启动mysql     
```sudo service mysql start ```
```mysql -u django -p ```    
password: django  

查看运行状态:     
```sudo service mysql status   ```


#### redis    
检查端口： netstat -ltnp |grep 6379    
启动：  sudo service redis-server start      
关闭：  sudo service redis-server stop      

可进入终端    
redis-cli    
查看库  
select 1
所有数据   
keys * hgetall cart_2    

#### 迁移模型
由于使用项目的User代替了django默认的User，需要先迁移项目模型
```python manage.py makemigrations databaseDemo```
```python manage.py migrate databaseDemo```
迁移django默认的模型
```python manage.py makemigrations```
```python manage.py migrate```

#### celery启动异步注册任务
#### 虚拟环境   
开启worker     
在项目目录下执行：
```python manage.py celery worker --loglevel=info```

#### nginx   
#### 启动nginx   
```sudo ln -sf /project_dict/databaseDemo.conf /etc/nginx/sites-enabled```
```sudo service nginx start```   

#### 查看nginx服务   
```ps aux|grep nginx``` 
```sudo service nginx status```

#### uwsgi
#### 启动uwsgi
```uwsgi --ini uwsgi.ini```








