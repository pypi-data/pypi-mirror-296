# UniParse

A Python library to parse PDF, DOCX, and TXT files.

## Installation

```bash
pip install mylibrary
```

## How to Use
```python
from UniParse import FileParser

parser = FileParser('path/to/your/file.pdf')
content = parser.parse()
print(content)
```

## Features
- Parse text from PDF files
- Extract content from DOCX documents
- Read text from TXT files