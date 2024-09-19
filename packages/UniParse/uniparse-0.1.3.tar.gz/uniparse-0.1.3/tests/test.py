from UniParse import FileParser

parser = FileParser('sample.pdf')
content = parser.parse()
print(content)