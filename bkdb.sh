#!/bin/bash

# 保存备份个数，备份31天数据
number=31
# 备份保存路径
workdir="/home/wsl/mnt/f/wsl/project/databaseDemo"
# 备份mysql数据
mysqldump --flush-logs --single-transaction -udjango -pdjango databaseDemo | gzip > $workdir/databaseDemo_$(date +%Y%m%d_%H%M%S).sql.gz
# 恢复mysql数据
# gzip -dc $workdir/databaseDemo_*.sql.gz > $workdir/databaseDemo_*.sql
# mysql -udjango -pdjango databaseDemo < $workdir/databaseDemo_*.sql
do_delete(){
	echo -e "Prepare to delete outdated files in $workdir"
	find $workdir -name "*.sql.gz" -and -mtime +$number -type f -delete
	if [[ $? -eq 0 ]];then
		echo -e "$date delete files success!"
	else
		echo -e "$date delete files FAILED!"
	fi
}

do_delete
