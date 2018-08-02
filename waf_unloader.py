# encoding: utf-8
import os

web_path = r'D:/CCNetGame/AWD/auto/6.5/'
waf_path = r'/tmp/log/waf.php'
content_waf = '<?php include_once("' + waf_path + '");?>'
file_list = []
for sub_dirs in os.walk(web_path):
    for filename in sub_dirs[2]:
        if '.php' == filename[-4:]:
            file_list.append(os.path.join(sub_dirs[0] + '/' + filename))

for filename in file_list:
    filename = u'%s' % filename
    try:
        with open(filename) as fp:
            php_file_content = fp.read()
            fp.close()
        with open(filename, 'w') as fp:
            fp.write(php_file_content.replace(content_waf, ''))
            fp.close()
    except Exception, e:
        pass
    

print 'done'