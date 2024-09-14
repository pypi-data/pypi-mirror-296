# CodeCache

CodeCache is a Python package that allows developers to analyze their codebase and cache the context using the Gemini API's context caching feature. This tool helps in generating summaries and insights about your codebase, enabling efficient querying and interaction with large codebases.

## Features

- **Codebase Analysis**: Recursively analyzes your codebase, generating summaries for each file.
- **Context Caching**: Utilizes the Gemini API to cache the context of your codebase, reducing the need to pass the same input tokens repeatedly.
- **Querying**: Allows querying the cached context to get insights or answers related to your codebase.
- **Summarization**: Supports both quick and detailed summaries of your codebase.
- **Customizable**: Configurable options for ignoring files/directories, setting cache TTL, and choosing summary modes.
- **CLI Interface**: Provides a user-friendly command-line interface for all functionalities.

## Installation

You can install CodeCache via pip:

```bash
pip install codecache
```

Alternatively, you can install it from source:

```bash
git clone https://github.com/DineshRai/codecache.git
cd codecache
pip install .
```

### Prerequisites

- Python 3.7 or higher
- Gemini API key (you can get one from Google AI Studio)

## Usage

### Setting Up the Environment

Before using CodeCache, you need to set the `GEMINI_API_KEY` environment variable:

```bash
export GEMINI_API_KEY='your_api_key_here'
```

You can also create a `.env` file in your project root:

```
GEMINI_API_KEY=your_api_key_here
```

### Command-Line Interface

CodeCache provides a CLI with several commands. You can get help by running:

```bash
codecache --help
```

#### Analyzing and Caching Context

To analyze your codebase and cache the context:

```bash
codecache cache [DIRECTORY] [OPTIONS]
```

- `DIRECTORY`: The root directory of your codebase (default is the current directory).
- Options:
  - `--ignore-file`: Path to a custom ignore file. If not provided, `.codecachignore` in the root directory will be used if it exists.
  - `--ttl`: Cache time-to-live in seconds (default: 3600).
  - `--summary-mode`: Summary mode to use (quick or detailed, default: quick).
  - `--model`: Gemini model to use (e.g., gemini-1.5-flash-001).
  - `--verbose` or `-v`: Enable verbose output.

Example:

```bash
codecache cache . --ttl 7200 --summary-mode detailed --model gemini-1.5-pro-001 --verbose
```

#### Querying the Cached Context

To query the cached context:

```bash
codecache query CACHE_KEY QUERY
```

- `CACHE_KEY`: The cache key returned when you cached the context.
- `QUERY`: The question or query you want to ask about your codebase.

Example:

```bash
codecache query your_cache_key "What does the CacheManager class do?"
```

#### Other Commands

- List cached contexts: `codecache list-caches`
- Update cache TTL: `codecache update-ttl CACHE_KEY NEW_TTL`
- Delete a cached context: `codecache delete-cache CACHE_KEY`

## Configuration

### Ignore Files

You can specify files or directories to ignore during analysis by creating a `.codecachignore` file in your project root:

```
# Ignore all .pyc files
*.pyc

# Ignore the build directory
build/

# Ignore specific files
secret_config.py
```

Alternatively, you can specify a custom ignore file using the `--ignore-file` option.

### Config File

You can configure default settings by creating a `.codebase_context` file in your project root (in TOML format):

```toml
[settings]
gemini_model = "gemini-1.5-flash-001"
default_ttl = 3600
ignore_file = ".codecachignore"
```

## Examples

### Quick Start

Analyze and Cache Context:

```bash
codecache cache .
```

Query the Cached Context:

```bash
codecache query your_cache_key "Explain the purpose of the Summarizer class."
```

### Logging and Verbose Output

To enable verbose logging, add the `--verbose` or `-v` flag to any command:

```bash
codecache cache . --verbose
```

## Development and Contribution

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Write your code and tests.
4. Submit a pull request.

### Setting Up for Development

```bash
git clone https://github.com/DineshRai/codecache.git
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

### Running Tests

We use pytest for testing. To run tests:

```bash
pytest tests/
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Google Gemini API for the context caching feature.
- Click for the command-line interface.
- Python dotenv for managing environment variables.

## Contact

For questions, feedback, or issues related to CodeCache:

- GitHub: [@DineshRai](https://github.com/DineshRai)
- Email: drai89@gmail.com
- Bug reports and feature requests: Please use the [GitHub issue tracker](https://github.com/DineshRai/codecache/issues)

For security-related concerns, please email directly rather than creating a public issue.
