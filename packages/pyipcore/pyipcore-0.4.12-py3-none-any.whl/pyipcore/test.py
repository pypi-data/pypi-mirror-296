import re

text = "这是一个// $# ir\n符号"
pattern = r"(//\s*\$\#)(.+)"

match = re.search(pattern, text)
if match:
    print("找到匹配:", match.group())
else:
    print("没有找到匹配")