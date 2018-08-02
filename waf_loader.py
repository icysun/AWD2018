# encoding: utf-8
import os

web_path = r'/var/www/'
waf_path = r'/tmp/log/waf.php'
content_waf = r'<?php include_once("' + waf_path + '");?>'
file_list = []
for sub_dirs in os.walk(web_path):
    for filename in sub_dirs[2]:
        if '.php' == filename[-4:]:
            file_list.append(os.path.join(sub_dirs[0] + '/' + filename))

for filename in file_list:
    filename = u'%s' % filename
    with open(filename, 'r') as fp:
        php_file_content = fp.read()
        fp.close()
    with open(filename, 'w') as fp:
        #print php_file_content
        #fp.write(u'%s\r\n%s' % (content_waf, php_file_content))
        fp.write(content_waf + '\r\n' + php_file_content)
        fp.close()
    # print filename

print 'done'