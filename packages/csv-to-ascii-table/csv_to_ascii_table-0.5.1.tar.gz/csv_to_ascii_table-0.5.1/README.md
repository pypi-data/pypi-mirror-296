# CSV to ASCII Table Converter

This package provides an asynchronous CSV to ASCII table converter. It reads CSV files and outputs them as formatted ASCII tables.

## Features

- Asynchronous file I/O for improved performance with large files
- Customizable column width and alignment
- Option to limit the number of rows displayed
- Support for output to file or console
- Error handling for file operations and CSV parsing

## Installation

You can install the package using pip: `pip install csv-to-ascii-table`

## Usage

Here's a basic example of how to use the converter:

```
import asyncio
from csv_to_ascii_table import CSVToASCIITable

async def main():
    converter = CSVToASCIITable('path/to/your/file.csv', max_width=30, max_rows=100, align='<')
    await converter.run()

if __name__ == "__main__":
    asyncio.run(main())
```