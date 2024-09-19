import html2text
import logging
import openai
import re
import requests
import sys
import warnings

from bs4 import BeautifulSoup

from typing import Optional, Union, List
from contextlib import contextmanager

html2text_markdown_converter = html2text.HTML2Text()
html2text_markdown_converter.wrap_links = False
html2text_markdown_converter.ignore_links = False
html2text_markdown_converter.body_width = 0  # Disable line wrapping

SYSTEMPROMPT = (
    "I have scraped a webpage, converted it from HTML into Markdown format, "
    "and enumerated its lines with line numbers. What kind of page is this? "
    "Is it primarily human-readable content? Is it an index or table of "
    "contents that refers the reader to other material? Is it an article? "
    "Is it a whole series of articles? Be descriptive."
)
PROMPT_HUMAN_READABLE_CHECK = (
    "Is this content human-readable? Please respond with one word: Yes or No."
)
PROMPT_LINE_FILTER = """
The scrape includes a lot of unimportant "boilerplate" text that isn't relevant to the substance or content of the page. These unimportant lines include things like navigation menus, copyright notices, affiliate links, user login links, and so on. I'd like your help filtering out these unimportant non-content lines.

Go through each line of the scrape (they're numbered for your convenience). For each line, label it with a one- or two-word description, followed by a dash, followed by either "keep" or "discard".

If a line is blank, ignore it entirely. Skip over it in your output.

Here's an example of what your response should look like (note that in this example, line 4 was a blank line, hence why it was omitted):
1. Header logo - discard
2. Title - keep
3. Menu link - discard
5. Menu link - discard
6. Body text - keep
7. Body text - keep
8. Advertisement - discard
etc.
"""

LOGGER = logging.getLogger("webpage2content")


# With the help of this function, we can prevent urllib3 from spewing obnoxious
# warnings about SSL certificates and other HTTP-related stuff while fetching URLs.
@contextmanager
def suppress_warnings():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        yield


# Fix a ridiculous formatting error in which sometimes links get double slashes.
def _remove_double_slashes(url: str):
    m = re.match(r"^(\w+)\:(/*)(.*)", url)
    if not m:
        # Doesn't start with a protocol designator. Doesn't look like a URL.
        return url

    protocol = m.group(1)

    s = m.group(3)
    s = re.sub(r"/+", "/", s)

    retval = f"{protocol}://{s}"
    return retval


def _get_page_as_markdown(url: str) -> str:
    if not url:
        return
    url = f"{url}"
    url = _remove_double_slashes(url)

    response = None

    try:
        # Get the site's presumed base URL from the URL itself.
        url_proto, url_therest = url.split("//")
        url_domain = url_therest.split("/")[0]
        base_url = f"{url_proto}//{url_domain}"
    except Exception:
        # Log the exception with traceback
        LOGGER.exception(
            f'Exception in _get_page_as_markdown while trying to parse URL (string is not a valid URL): "{url}"'
        )
        return None

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.126 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        }

        with suppress_warnings():
            response = requests.get(
                url,
                timeout=60,
                verify=False,
                headers=headers,
            )
    except Exception:
        # Log the exception with traceback
        LOGGER.exception("Exception in _get_page_as_markdown while fetching page")
        return None

    if not response:
        LOGGER.warning(f"No content retrieved from URL: {url}")
        return None

    if response.status_code != 200:
        LOGGER.warning(f"Fetch failed for URL: {url}")
        return None

    # Look for an HTML tag to confirm that this is in fact HTML content.
    # Look for a <base> tag to get the base URL.
    # If it doesn't exist, just keep the base URL that was gleaned from the target URL.
    try:
        content = response.content.decode("utf-8", errors="ignore")
        soup = BeautifulSoup(content, "html.parser")

        html_tag = soup.find("html")
        if not html_tag:
            LOGGER.warning("_get_page_as_markdown failed because no html tag")
            return None

        base_tag = soup.find("base")
        if base_tag:
            base_url = base_tag["href"]
    except Exception:
        # Log the exception with traceback
        LOGGER.exception("Exception in _get_page_as_markdown while parsing HTML")
        return None

    html_content = response.text
    html2text_markdown_converter.baseurl = base_url

    markdown_content = None
    try:
        markdown_content = html2text_markdown_converter.handle(html_content)
    except Exception:
        # Log the exception with traceback
        LOGGER.exception("Exception in _get_page_as_markdown while converting HTML")
        return None

    if not markdown_content:
        return None

    # We'll now strip lines and consolidate whitespace.
    lines = markdown_content.splitlines()
    lines = [line.strip() for line in lines]
    markdown_content = "\n".join(lines)
    markdown_content = re.sub(r"\n\n\n+", "\n\n", markdown_content)

    return markdown_content


def _call_gpt(
    conversation: Union[str, dict, List[dict]], openai_client: openai.OpenAI
) -> str:
    if isinstance(conversation, str):
        conversation = [{"role": "user", "content": conversation}]
    elif isinstance(conversation, dict):
        conversation = [conversation]

    answer_full = ""
    while True:
        LOGGER.debug(
            f"webpage2content._call_gpt calling chat completion "
            f"with conversation of {len(conversation)} messages. "
            f"Last message is {len(conversation[-1]['content'])} chars long."
        )

        completion = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=conversation,
            temperature=0,
        )

        answer = completion.choices[0].message.content
        answer_full += answer + "\n"

        LOGGER.debug(
            f"webpage2content._call_gpt got answer of length {len(answer)}, "
            f"appending to full answer currently at length {len(answer_full)}"
        )

        conversation.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )
        conversation.append(
            {
                "role": "user",
                "content": "Please continue from where you left off.",
            }
        )

        if completion.choices[0].finish_reason == "length":
            LOGGER.debug(
                "webpage2content._call_gpt finish reason length, continuing loop"
            )
            continue

        break

    answer_full = answer_full.strip()
    return answer_full


def webpage2content(url: str, openai_client: openai.OpenAI):
    if type(url) != str:
        LOGGER.warning("webpage2content got a URL that isn't a string.")
        return None

    url = url.strip()
    if not url:
        LOGGER.warning("webpage2content got empty URL.")
        return None

    markdown = _get_page_as_markdown(url)
    if not markdown:
        return None

    if not isinstance(markdown, str):
        LOGGER.error("markdown somehow came back as something other than a string.")
        return None

    markdown = markdown.strip()
    if not markdown:
        return None

    mdlines = markdown.splitlines()
    mdlines = [f"{linenum+1}. {linetext}" for linenum, linetext in enumerate(mdlines)]
    markdown_with_linenums = "\n".join(mdlines)

    # TODO: Break up the markdown into pieces if the webpage is too big.
    conversation = [
        {"role": "system", "content": SYSTEMPROMPT},
        {"role": "user", "content": markdown_with_linenums},
    ]

    # First, we get the AI to describe the page to us in its own words.
    # We are uninterested in this answer. We just want it to have this conversation
    # with itself so that it knows what's going to be important in subsequent steps.
    try:
        LOGGER.debug(f"webpage2content is asking GPT to describe {url}")
        gptreply_page_description = _call_gpt(
            conversation=conversation,
            openai_client=openai_client,
        )
        LOGGER.debug(f"webpage2content asked GPT to describe {url}")
        conversation.append(
            {
                "role": "assistant",
                "content": gptreply_page_description,
            }
        )
    except Exception:
        LOGGER.exception("Exception in webpage2content determining content type")
        return None

    # Next, we simply ask it whether or not the content is human-readable.
    try:
        LOGGER.debug(f"webpage2content is determining human readability of {url}")
        conversation.append({"role": "user", "content": PROMPT_HUMAN_READABLE_CHECK})
        gptreply_is_human_readable = _call_gpt(
            conversation=conversation,
            openai_client=openai_client,
        )

        is_human_readable = "yes" in gptreply_is_human_readable.lower()
        if not is_human_readable:
            LOGGER.warning(f"Page at URL {url} is not human-readable")
            return None
        else:
            LOGGER.debug(f"webpage2content confirmed human readability of {url}")

    except Exception:
        LOGGER.exception("Exception in webpage2content checking human readability")
        return None

    # At last, we call it with the line filtration prompt.
    try:
        LOGGER.debug(f"webpage2content is querying line filtration for {url}")
        conversation[-1] = {"role": "user", "content": PROMPT_LINE_FILTER}
        gptreply_line_filtration = _call_gpt(
            conversation=conversation,
            openai_client=openai_client,
        )
        LOGGER.debug(f"webpage2content has queried line filtration for {url}")

    except Exception:
        LOGGER.exception("Exception in webpage2content choosing lines to filter")
        return None

    mdlines = markdown.splitlines()
    filterlines = gptreply_line_filtration.splitlines()

    LOGGER.debug(f"webpage2content is iterating through line filtration for {url}")

    for filterline in filterlines:
        try:
            linenumstr, linetext = filterline.split(".", maxsplit=1)
            linenum = int(linenumstr) - 1

            if linetext.lower().endswith("discard"):
                mdlines[linenum] = ""

        except Exception as ex:
            LOGGER.debug(f"Nonthreatening exception during line filtration: {ex}")
            pass

    markdown = "\n".join(mdlines)
    markdown = re.sub(r"\n\n\n+", "\n\n", markdown)
    markdown = markdown.strip()

    LOGGER.debug(f"webpage2content has constructed filtered markdown for {url}")
    return markdown


def main():
    import argparse
    import dotenv
    import os

    # Read the version from the VERSION file
    with open(os.path.join(os.path.dirname(__file__), "VERSION"), "r") as version_file:
        version = version_file.read().strip()

    parser = argparse.ArgumentParser(
        description=(
            "A simple Python package that takes a web page (by URL) and extracts its "
            "main human-readable content. It uses LLM technology to remove all of the "
            "boilerplate webpage cruft (headers, footers, copyright and accessibility "
            "notices, advertisements, login and search controls, etc.) that isn't part "
            "of the main content of the page."
        )
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {version}",
        help="Show the version number and exit.",
    )

    parser.add_argument(
        "-l",
        "--log-level",
        help="Sets the logging level. (default: %(default)s)",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    )

    parser.add_argument(
        "-u",
        "--url",
        help="The URL to read.",
        type=str,
    )
    parser.add_argument(
        "url_arg",
        help="Same as --url, but specified positionally.",
        type=str,
        nargs="?",
    )

    parser.add_argument(
        "-k",
        "--key",
        help="OpenAI API key. If not specified, reads from the environment variable OPENAI_API_KEY.",
        type=str,
        default="",
    )
    parser.add_argument(
        "key_arg",
        help="Same as --key, but specified positionally.",
        type=str,
        nargs="?",
    )

    parser.add_argument(
        "-o",
        "--org",
        help="OpenAI organization ID. If not specified, reads from the environment variable OPENAI_ORGANIZATION. "
        "If no such variable exists, then organization is not used when calling the OpenAI API.",
        type=str,
        default="",
    )
    parser.add_argument(
        "org_arg",
        help="Same as --org, but specified positionally.",
        type=str,
        nargs="?",
    )

    args = parser.parse_args()

    if args.log_level:
        log_level = logging.getLevelName(args.log_level)
        LOGGER.setLevel(log_level)

    dotenv.load_dotenv()

    openai_api_key = args.key or args.key_arg or os.getenv("OPENAI_API_KEY")
    openai_org_id = args.org or args.org_arg or os.getenv("OPENAI_ORGANIZATION_ID")
    url = args.url or args.url_arg

    if not url:
        parser.error("URL is required.")
    if not openai_api_key:
        parser.error("OpenAI API key is required.")

    openai_client = openai.OpenAI(api_key=openai_api_key, organization=openai_org_id)

    s = webpage2content(
        url=url,
        openai_client=openai_client,
    )
    print(s)


if __name__ == "__main__":
    main()
