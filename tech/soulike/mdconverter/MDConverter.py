from tech.soulike.mdconverter.regex import *


class MDConverter:

    def makeHtml(self, code):

        result = code
        # 处理代码
        result = self.__convertCodeBlocks(result)
        # 处理行内元素
        result = self.__convertHeadings(result)
        result = self.__convertInlines(CODE, result, '<code>')
        result = self.__convertInlines(STRONG, result, '<strong>')
        result = self.__convertInlines(ITALIC, result, '<i>')
        # 处理链接和图片，注意这两个有顺序要求，必须先图片后链接
        result = self.__convertImages(result)
        result = self.__convertLinks(result)

        result = self.__convertBlockquotes(result)
        result = self.__convertLists(result)
        return result

    def __convertHeadings(self, code):
        results = HEADING.search(code)
        while results is not None:
            level = len(results.group(1))
            convertedStr = '<h{0}>{1}</h{2}>\n'.format(level, results.group(2), level)
            code = re.sub(HEADING, convertedStr, code, 1)
            results = HEADING.search(code)
        return code

    def __convertInlines(self, regex, code, startTag):
        results = regex.search(code)
        while results is not None:
            convertedStr = '{0}{1}{2}'.format(startTag, results.group(1), startTag[:1] + '/' + startTag[1:])
            code = re.sub(regex, convertedStr, code, 1)
            results = regex.search(code)
        return code

    def __convertImages(self, code):
        regex = IMAGE
        results = regex.search(code)
        while results is not None:
            convertedStr = '<img src="{1}" alt="{0}" />'.format(results.group(1), results.group(2))
            code = re.sub(regex, convertedStr, code, 1)
            results = regex.search(code)
        return code

    def __convertLinks(self, code):
        regex = LINK
        results = regex.search(code)
        while results is not None:
            convertedStr = '<a href="{1}">{0}</a>'.format(results.group(1), results.group(2))
            code = re.sub(regex, convertedStr, code, 1)
            results = regex.search(code)
        return code

    def __convertBlockquotes(self, code):
        regex = BLOCKQUOTE
        blockcodePartSearchResult = regex.search(code)

        # 找到所有块引用，一块一块的处理
        while blockcodePartSearchResult is not None:
            partCode = blockcodePartSearchResult.group(1)  # 某一块的代码
            originalPartCode = blockcodePartSearchResult.group(1)
            partRegex = BLOCKQUOTE_ITEM  # 代码内部替换用正则

            blockquoteSearchResultInPart = partRegex.search(partCode)  # 找到一个引用行
            lastBlockquoteLevel = 0  # 上一次处理的引用行的级别，用于计算嵌套引用
            maxBlockquoteLevel = -1  # 最大引用行级别，用于在最后补充闭合标签
            convertedStr = '<blockquote><p>'

            while blockquoteSearchResultInPart is not None:
                currentBlockQuoteLevel = len(blockquoteSearchResultInPart.group(2))
                if currentBlockQuoteLevel > maxBlockquoteLevel:
                    maxBlockquoteLevel = currentBlockQuoteLevel
                blockquoteLevelDiff = currentBlockQuoteLevel - lastBlockquoteLevel  # 看看这一个匹配和上一个匹配是不是一个等级的块引用，如果不是就得特殊处理
                lastBlockquoteLevel = currentBlockQuoteLevel

                if blockquoteLevelDiff > 0:
                    convertedStr += '</p>'
                if blockquoteLevelDiff < 0:
                    blockquoteLevelDiff = 0

                blockquoteContent = blockquoteSearchResultInPart.group(3)

                convertedStr += '<blockquote>' * blockquoteLevelDiff + '<p>' * (blockquoteLevelDiff % 2) + \
                                blockquoteContent
                partCode = re.sub(partRegex, convertedStr, partCode, 1)
                convertedStr = ''
                blockquoteSearchResultInPart = partRegex.search(partCode)  # 再次查找在这个代码块里面还有没有块引用

            # 补充闭合标签
            partCode += '</p></blockquote>'
            partCode += '</blockquote>' * maxBlockquoteLevel

            code = re.sub(originalPartCode, partCode, code, 1)

            nextSearchStartIndex = blockcodePartSearchResult.end()  # 记录一下下次应该从哪里开始匹配
            blockcodePartSearchResult = regex.search(code, nextSearchStartIndex)
        return code

    def __convertLists(self, code):
        regex = LIST

        listPartSearchResult = regex.search(code)
        while listPartSearchResult is not None:
            partCode = listPartSearchResult.group(1)

            partRegex = LIST_ITEM
            partSearchResult = partRegex.search(partCode)
            lastListLevel = 0

            closeTagStack = []

            if self.__isOrderedList(partCode) is True:
                convertedStr = '<ol>'
                closeTagStack.append('</ol>')
                isOrderedItem = True
            else:
                convertedStr = '<ul>'
                closeTagStack.append('</ul>')
                isOrderedItem = False

            while partSearchResult is not None:
                currentListLevel = len(partSearchResult.group(2)) // 4
                listLevelDiff = currentListLevel - lastListLevel
                lastListLevel = currentListLevel

                listContent = partSearchResult.group(3)

                if listLevelDiff < 0:
                    convertedStr += closeTagStack.pop()
                    for i in range(2 * (-listLevelDiff)):
                        convertedStr += closeTagStack.pop()
                elif listLevelDiff > 0:
                    if self.__isOrderedList(partSearchResult.group(0)) is True:
                        convertedStr += '<ol>'
                        closeTagStack.append('</ol>')
                        isOrderedItem = True
                    else:
                        convertedStr += '<ul>'
                        closeTagStack.append('</ul>')
                        isOrderedItem = False
                elif len(closeTagStack) is not 1:
                    convertedStr += closeTagStack.pop()

                    if self.__isOrderedList(partSearchResult.group(0)) is not isOrderedItem:
                        isOrderedItem = not isOrderedItem
                        convertedStr += closeTagStack.pop()
                        if isOrderedItem is True:
                            convertedStr += '<ol>'
                            closeTagStack.append('</ol>')
                        else:
                            convertedStr += '<ul>'
                            closeTagStack.append('</ul>')

                convertedStr += '<li>' + listContent
                closeTagStack.append('</li>')
                partCode = re.sub(partRegex, convertedStr, partCode, 1)
                convertedStr = ''
                partSearchResult = partRegex.search(partCode)
            for i in range(len(closeTagStack)):
                partCode += closeTagStack.pop()
            code = re.sub(listPartSearchResult.group(1), partCode, code, 1)
            nextSearchStartIndex = listPartSearchResult.end()
            listPartSearchResult = regex.search(code, nextSearchStartIndex)
        return code

    def __isOrderedList(self, listItem):
        typeSearchResult = LIST_ITEM_TYPE.search(listItem)
        if typeSearchResult.group(2) is not None and typeSearchResult.group(2).isdigit():
            return True
        else:
            return False

    def __convertCodeBlocks(self, code):
        regex = CODE_BLOCK
        results = regex.search(code)
        while results is not None:
            convertedStr = '<pre><code class="{0} language-{0}">{1}</code></pre>'.format(results.group(1),
                                                                                         results.group(2))
            code = re.sub(regex, convertedStr, code, 1)
            results = regex.search(code)
        return code
