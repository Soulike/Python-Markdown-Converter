import re

# 行内元素
HEADING = re.compile('^(#+) (.*)[\r\n]*', re.MULTILINE)
CODE = re.compile('`([^`\r\n]+)`')
STRONG = re.compile('\*\*(.+)\*\*')
ITALIC = re.compile('\*(.+)\*')

# 图片与链接
IMAGE = re.compile('!\[(.+)\]\((.+)\)')
LINK = re.compile('\[(.+)\]\((.+)\)')

# 引用
# 用于判定引用块
BLOCKQUOTE = re.compile('(?:<.+?>.*</.+?>|<.+?/>)*\s*(> .+?)(?:\s{2,}|<\w+>|$)', re.DOTALL)
# 用于在引用块内匹配内容
BLOCKQUOTE_ITEM = re.compile('(<\w+>)*>(>*) (.+)')

# 列表
# 用于判定列表块
LIST = re.compile('(?:<.+?>.*</.+?>|<.+?/>)*((?:(?: {4})*(?:([\-*+]|\d\.) .+?\r?\n?))+)(?:\s{2,}|<\w+>|$)', re.DOTALL)
# 用于在列表内匹配内容
LIST_ITEM = re.compile('(<\w+>)*( *)(?:[*\-+]|\d\.) (.+)')
# 用于判定列表项类型
LIST_ITEM_TYPE = re.compile('\s*((\d+)\.|[\-*+]) .*')

# 代码块
# 代码块判定
CODE_BLOCK = re.compile('^```(\w+)?\r?\n(.+)```$', re.DOTALL | re.MULTILINE)

# 普通文本
# 在文件起始的普通文本
PLAIN_TEXT_START = re.compile('^{.+}')
# 在文件结尾的普通文本
PLAIN_TEXT_END = re.compile('')
# 在标签之间的普通文本
PLAIN_TEXT_MID = re.compile('')
