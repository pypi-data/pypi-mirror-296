# Smart Cache Cleaner

Smart Cache Cleaner is a cross-platform Python utility for efficiently managing and cleaning cache and temporary files.

## Features

- Smart scanning of common cache and temp directories
- Customizable file filtering by size and age
- Secure deletion with file integrity checks
- Memory-efficient batch processing
- Detailed logging and verbose output options
- Cross-platform support (Windows, macOS, Linux)
- Interactive command-line interface with file-by-file decision making
- Summary of files by extension before deletion

## Installation

You can install Smart Cache Cleaner directly from PyPI:


`pip install smart-cache-cleaner`



## Usage

After installation, you can run Smart Cache Cleaner from anywhere in your terminal:


`smart-cache-cleaner [options]`



### Available options:

- `-d` or `--directory`: Specify a custom directory to scan
- `-s` or `--min-size`: Minimum file size to consider (in bytes)
- `-a` or `--max-age`: Maximum file age to consider (in days, 0 for no limit)
- `-y` or `--yes`: Skip confirmation for deletion
- `-v` or `--verbose`: Increase output verbosity

### Interactive Prompts

During the scanning process, you will be prompted for each file:

- `y`: Yes, delete this file
- `n`: No, skip this file
- `q`: Quit the scanning process

You can use the `-y` option to skip these prompts and delete all matched files automatically.

### Example:


`smart-cache-cleaner -d /path/to/custom/directory -s 1000000 -a 30`


This command would scan the specified directory, only considering files larger than 1 MB and not older than 30 days.

## Safety Features

Smart Cache Cleaner includes several safety features to protect your system and data:

- File hash verification before deletion to ensure file integrity
- Symlink protection to prevent accidental deletion of linked files
- Maximum directory depth limit to prevent infinite recursion
- Memory usage monitoring to prevent excessive memory consumption
- Batch processing to handle large directories efficiently

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

While Smart Cache Cleaner is designed with safety in mind, please use it at your own risk. Always ensure you have backups of important data before performing any cleanup operations.
