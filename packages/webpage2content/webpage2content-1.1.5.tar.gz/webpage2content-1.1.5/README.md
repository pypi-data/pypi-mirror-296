# webpage2content

A simple Python package that takes a web page (by URL) and extracts its main human-readable content. It uses LLM technology to remove all of the boilerplate webpage cruft (headers, footers, copyright and accessibility notices, advertisements, login and search controls, etc.) that isn't part of the main content of the page.

## Installation

```bash
pip install webpage2content
```

## Usage

### Python

```python
import openai
from webpage2content import webpage2content

text = webpage2content("http://mysite.com", openai.OpenAI(api_key="your_openai_api_key"))
print(text)
```

### CLI

You can invoke `webpage2content` from the command line.

```cmd
webpage2content https://slashdot.org/
```

If you don't have your `OPENAI_API_KEY` environment variable set, you can pass it to the CLI invocation as a second argument.

```cmd
webpage2content https://slashdot.org/ sk-ABCD1234
```

You can also specify the OpenAI organization ID if needed.

```cmd
webpage2content https://slashdot.org/ sk-ABCD1234 org-5678
```

### Additional CLI Options

- **Logging Level**: You can set the logging level using the `-l` or `--log-level` option.

  ```cmd
  webpage2content -l DEBUG https://slashdot.org/
  ```

- **Version**: Display the version number of the package.

  ```cmd
  webpage2content -v
  ```

- **Help**: Display help information.
  ```cmd
  webpage2content -h
  ```

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key.
- `OPENAI_ORGANIZATION_ID`: Your OpenAI organization ID (optional).

## .env File Support

The CLI will honor `.env` files for setting environment variables. Create a `.env` file in the same directory with the following content:

```
OPENAI_API_KEY=your_openai_api_key
OPENAI_ORGANIZATION_ID=your_openai_organization_id
```

## Example

```cmd
webpage2content -l INFO https://example.com/ sk-ABCD1234 org-5678
```

This command will extract the main content from `https://example.com/` using the provided OpenAI API key and organization ID, with logging set to `INFO` level.

```

```
