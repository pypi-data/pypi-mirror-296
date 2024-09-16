# Document Sorter

Document Sorter is a Python package that automatically organizes documents into folders based on their content similarity. It supports various file types including PDF, DOCX, XLSX, CSV, TXT, MD, and TEX.

## Features

- Searches for documents in a specified directory
- Extracts text from various file types
- Clusters documents based on content similarity using the elbow method
- Allows users to specify the number of clusters
- Supports custom keywords for folder names
- Sorts documents into folders named after the most relevant keyword for each cluster or user-specified keywords
- Supports dry run mode for testing
- Provides verbose output option for detailed information during execution

## Installation

You can install Document Sorter using pip:

```
pip install document-sorter
```

## Usage

After installation, you can use the Document Sorter from the command line:

```
document-sorter [directory_path] [OPTIONS]
```

### Options

- `directory_path`: The directory to search for documents (default: current directory)
- `--dry-run`: Perform a dry run without moving files
- `--verbose`: Print detailed information during execution
- `--clusters N`: Specify the number of clusters to use
- `--keywords KEYWORD1 KEYWORD2 ...`: Specify custom keywords for folder names

## Examples

1. Basic usage (current directory):
   ```
   document-sorter
   ```

2. Specify a directory with verbose output:
   ```
   document-sorter /path/to/documents --verbose
   ```

3. Perform a dry run:
   ```
   document-sorter /path/to/documents --dry-run
   ```

4. Specify the number of clusters:
   ```
   document-sorter /path/to/documents --clusters 5
   ```

5. Use custom keywords:
   ```
   document-sorter /path/to/documents --keywords work personal projects research
   ```

6. Combine options:
   ```
   document-sorter /path/to/documents --verbose --clusters 4 --keywords work personal projects research
   ```

## Behavior

- If neither `--clusters` nor `--keywords` are specified, the script will automatically determine the optimal number of clusters and generate keywords based on document content.
- If `--clusters` is specified without `--keywords`, the script will use the specified number of clusters and generate keywords based on document content.
- If `--keywords` is specified without `--clusters`, the script will automatically determine the optimal number of clusters and use the provided keywords for folder names.
- If both `--clusters` and `--keywords` are specified, the script will use the specified number of clusters and the provided keywords for folder names.

## Requirements

Document Sorter requires Python 3.6 or later. For a full list of dependencies, see the `requirements.txt` file.

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.