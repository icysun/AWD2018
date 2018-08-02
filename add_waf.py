#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Coding By : IcySun
# @Date:   2018-05-26
'''
功能说明：
	0x00、修改web服务器密码
	0x01、对目标web服务器做waf防护，上传waf，包含waf文件
	0x02、对目标web路径做文件监控，对新增文件删除
	0x03、备份Web目录、删除web目录、还原web路径，给web路径附权 chmod 755 -R 
	0x04、WAF、Monitor给权限，chmod 755
'''
import paramiko

hostname = 'ip' #服务器IP地址
port = 22
web_path = r'/var/www/html/'
waf_path = r'/tmp/log/waf.php'
monitor_path = r'/tmp/log/M_64'
ser_user = 'user'  #服务器账户
ser_pass = 'PASS'  #服务器密码
new_pass = 'NEWPASS'
creat_logpath_cmd = "mkdir -p /tmp/log/ && chmod 777 -R /tmp/log/" 
waf_and_monitor = 'chmod 777 -R /tmp/log/*'
chg_pass = 'echo -e '+'"'+ser_pass+'\\n'+new_pass+'\\n'+new_pass+'"'+' | passwd'
back_web = 'cd %s && tar -cf /tmp/web.tar . && rm -rf %s* && cp /tmp/web.tar ~/. && tar -xf /tmp/web.tar .' % (web_path,web_path)
chmod_cmd = 'chmod 755 -R /var/www/html/*'
begin_mon = 'nohup /tmp/log/M_64 -w %s &' % (web_path)
sed_waf_add_cmd = '''sed -i "4s|.*|web_path = '%s'|" /tmp/log/waf_loader.py''' % web_path
sed_waf_del_cmd = '''sed -i "4s|.*|web_path = '%s'|" /tmp/log/waf_Unloader.py''' % web_path
add_wafphp = 'python /tmp/log/waf_loader.py'

try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, port=port, username=ser_user, password=ser_pass)
    stdin, stdout, stderr = ssh.exec_command(creat_logpath_cmd)
    transport = paramiko.Transport((hostname, port))
    transport.connect(username=ser_user, password=ser_pass)
    sftp = paramiko.SFTPClient.from_transport(transport)
    local_waf = './waf.php'
    remove_waf = '/tmp/log/waf.php'
    sftp.put(local_waf, remove_waf)
    local_add_waf = './waf_loader.py'
    remove_add_waf = '/tmp/log/waf_loader.py'
    sftp.put(local_add_waf,remove_add_waf)
    local_del_waf = './waf_Unloader.py'
    remove_del_waf = '/tmp/log/waf_Unloader.py'
    sftp.put(local_del_waf,remove_del_waf)
    local_monitor = './M_64'
    remove_monitor = '/tmp/log/M_64'
    sftp.put(local_monitor, remove_monitor)
    transport.close()
    stdin, stdout, stderr = ssh.exec_command(back_web)
    print(stdout.read())
    stdin, stdout, stderr = ssh.exec_command(chmod_cmd)
    print(stdout.read())
    stdin, stdout, stderr = ssh.exec_command(waf_and_monitor)
    print(stdout.read())
    stdin, stdout, stderr = ssh.exec_command(sed_waf_add_cmd)
    print(stdout.read())
    stdin, stdout, stderr = ssh.exec_command(sed_waf_del_cmd)
    print(stdout.read())
    stdin, stdout, stderr = ssh.exec_command(add_wafphp)
    print(stdout.read())
    stdin, stdout, stderr = ssh.exec_command(begin_mon,timeout=5)
    #stdin, stdout, stderr = ssh.exec_command(chg_pass)
    #print(stdout.read())
    ssh.close()
except Exception, e:
    print e
