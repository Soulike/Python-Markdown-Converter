from .MDConverter import MDConverter

converter = MDConverter()

with open('./test.md', 'r') as inFile:
    with open('./output.html', 'w') as outFile:
        outFile.write(converter.makeHtml(inFile.read()))
