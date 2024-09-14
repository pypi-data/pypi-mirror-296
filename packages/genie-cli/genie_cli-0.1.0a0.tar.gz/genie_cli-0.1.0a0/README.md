# Genie CLI

Genie CLI is a command-line tool designed to generate AEA (Autonomous Economic Agent) agents using human-level language. This tool leverages various libraries to provide a seamless experience for developers.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Installation

To install the Genie CLI, you need to have Python 3.8 or higher. You can install the dependencies using the following command:

The project uses rye as package manager, process to install rye:
[Rye Installation](https://rye.astral.sh/guide/installation/)

```sh
rye sync
```

## Usage

To use the Genie CLI, you can run the following command:

```sh
genie
```

This will start the CLI and you can follow the prompts to generate AEA agents.

## Project Structure

The project is organized as follows:

```
genie-cli/
├── src/
│   ├── genie_cli/
│   │   ├── prompts/
│   │   │   └── behaviour_prompts.py
│   │   ├── widgets/
│   │   │   ├── prompt_input.py
│   │   │   └── chatbox.py
│   │   └── __main__.py
├── pyproject.toml
├── README.md
└── .gitignore
```

### Key Files

- **`pyproject.toml`**: Contains project metadata and dependencies.
- **`src/genie_cli/prompts/behaviour_prompts.py`**: Contains prompt templates for generating behavior plans.
- **`src/genie_cli/widgets/prompt_input.py`**: Defines the `PromptInput` widget for user input.
- **`src/genie_cli/widgets/chatbox.py`**: Defines the `Chatbox` widget for displaying messages.

## Dependencies

The project relies on several key dependencies:

- `textual>=0.67.1`
- `litellm>=1.40.9`
- `rich>=13.7.1`
- `click-default-group>=1.2.4`
- `click>=8.1.7`
- `humanize>=4.9.0`
- `xdg-base-dirs>=6.0.1`
- `pyperclip>=1.9.0`
- `python-dotenv>=1.0.1`
- `requests>=2.32.3`
- `types-requests>=2.32.0.20240907`

For development, the project also uses:

- `mypy>=1.11.2`

## Development

To set up the development environment, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/genie-cli.git
    cd genie-cli
    ```

2. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Run the CLI:
    ```sh
    genie
    ```

## Contributing

We welcome contributions! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License

This project is licensed under the Valory License. See the [LICENSE](LICENSE) file for details.
