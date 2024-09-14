# Auto README Generator

Auto README Generator is a Python project designed to automate the creation of README.md files for Python projects. It leverages OpenAI's language model to generate comprehensive documentation based on the project's source code or a specified local script.

## Features

- **Generate README from OpenAI**: Create a README.md file by analyzing your project files and using OpenAI's API.
- **Generate README from Local Script**: Generate a README.md file by executing a local Python script that produces documentation.
- **Customizable Temperature**: Adjust the creativity of the OpenAI model's responses with a temperature setting.
- **Error Handling**: Robust error handling to ensure smooth execution and informative logging.

## Installation

To install the required dependencies, you can use pip:

```bash
pip install -r requirements.txt
```

Make sure to have Python 3.7 or higher installed.

## Usage

### Command Line Interface

The project provides a command-line interface (CLI) for generating README files. You can use the following commands:

1. **Generate README from OpenAI**:

   ```bash
   python -m auto_readme.cli generate-from-openai <directory> [--output-path <path>] [--temperature <float>] [--use-env-api-key]
   ```

   - `<directory>`: The path to the project directory containing Python files.
   - `--output-path`: Optional. Specify the output path for the generated README.md file.
   - `--temperature`: Optional. A float between 0 and 1 to control the creativity of the OpenAI model (default is 0.0).
   - `--use-env-api-key`: Optional. Use the OpenAI API key from the environment variable `OPENAI_API_KEY`.

2. **Generate README from Local Script**:

   ```bash
   python -m auto_readme.cli generate-from-local-script <directory> <local_script> [--output-path <path>]
   ```

   - `<directory>`: The path to the project directory containing Python files.
   - `<local_script>`: The path to the local Python script that generates the README content.
   - `--output-path`: Optional. Specify the output path for the generated README.md file.

### Example

To generate a README from OpenAI:

```bash
python -m auto_readme.cli generate-from-openai ./my_project --output-path ./my_project/README.md --temperature 0.5
```

To generate a README from a local script:

```bash
python -m auto_readme.cli generate-from-local-script ./my_project ./my_script.py --output-path ./my_project/README.md
```

Script example:

```py

# user_script.py

import sys

def main():
    # Get input from stdin
    input_data = sys.stdin.read().strip()

    # Perform some operation based on the input
    output_data = f"Processed input: {input_data}"

    # Output the result
    print(output_data)

if __name__ == "__main__":
    main()
```

## Code Structure

- `chat_models.py`: Contains functions to interact with OpenAI's API and execute local scripts.
- `cli.py`: Implements the command-line interface for generating README files.
- `custom_arg_types.py`: Defines custom argument types for command-line parsing.
- `files.py`: Contains functions for locating and processing Python files.
- `generator.py`: Handles the logic for generating README files from OpenAI or local scripts.
- `prompts.py`: Constructs prompts for the OpenAI model based on the project's files.
- `__init__.py`: Initializes the package and sets up logging.
- `__main__.py`: Entry point for the command-line interface.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgments

- [Langchain](https://langchain.com/): For providing the tools to interact with language models.
- [OpenAI](https://openai.com/): For the powerful language models that make this project possible.
