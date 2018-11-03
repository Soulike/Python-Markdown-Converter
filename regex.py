import re

# 行内元素
HEADING = re.compile('^(#{1,6}) (.*)', re.MULTILINE)
CODE = re.compile('`([^`\r\n]+)`')
STRONG = re.compile('(?:\r?\n)*[*]{2}(.+)[*]{2}')
ITALIC = re.compile('(?:\r?\n)*[*](.+)[*]')
HORIZONTAL_LINE = re.compile('^-{3,}', re.MULTILINE)

# 图片与链接
IMAGE = re.compile('!\[(.+?)\]\((.+?)\)')
LINK = re.compile('\[(.+?)\]\((.+?)\)')

# 引用
# 用于判定引用块
BLOCKQUOTE = re.compile('^(> .+)+', re.DOTALL | re.MULTILINE)
# 用于在引用块内匹配内容
BLOCKQUOTE_ITEM = re.compile('^>(>*) (.+?)$', re.MULTILINE)

# 列表
# 用于判定列表块
LIST = re.compile('(^(?: {4})*(?:[\-*+]|\d\.) .+)+', re.DOTALL | re.MULTILINE)
# 用于在列表内匹配内容
LIST_ITEM = re.compile('^((?: {4})*)(?:[*\-+]|\d\.) (.+?)$', re.MULTILINE)
# 用于判定列表项类型
LIST_ITEM_TYPE = re.compile('\s*((\d+)\.|[\-*+]) .*')


# 代码块
# 代码块判定
CODE_BLOCK = re.compile('^```(\w+)?\r?\n(.+?)```$', re.DOTALL | re.MULTILINE)

# 普通文本
PLAIN_TEXT = re.compile('(?:^(\S*\s?\S+)\s{2,})|(?:\s{2,}(\S*\s?\S+)$)', re.MULTILINE)

NOT_PLAIN_TEXT = re.compile('\s*</?[\w\s-]+/?>\s*')
