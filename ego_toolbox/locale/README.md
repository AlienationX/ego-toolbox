# Read Me

```shell
mkdir locale

# 1. 创建对应的语言django.po文件
python manage.py makemessages -l en      # 英文
python manage.py makemessages -l zh_Hans # 简体中文（注意下划线）

# 2. 编辑.po文件
# 打开 locale/en/LC_MESSAGES/django.po
# 添加翻译，例如：
# msgid "Welcome to our website!"
# msgstr "Welcome to our website!"

# 3. 检查翻译覆盖率，更新所有翻译文件。检查.po文件中是否有未翻译的字符串
python manage.py makemessages -a

# 4. 编译成 .mo文件
python manage.py compilemessages
```
