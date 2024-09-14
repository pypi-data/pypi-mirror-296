"""Web Utilities"""


import platform
import re
import traceback

from collections import OrderedDict, namedtuple
from urllib.parse import urlparse, parse_qs
from typing import Any, NamedTuple


def get_file_name_from_url(url: str) -> str:
    """Parses an URL and returns the last part which usually is a
    file name or directory/section.
    
    :param url: The URL to parse.
    :type url: str
    
    :return: The last part of the path ie. everything after the
        last slash excluding the query string.
    :rtype: str
    """
    parsed_url = urlparse(url)

    last_part = parsed_url.path.split('/')[-1]

    return last_part


def get_qs_dict(url: str) -> dict[str, list[str]]:
    """Returns an URL query string as key-value dictionary.

    Please note that query parameters can be specified multiple times
    thus the value for a specific key is a list of strings,
    not a single string.

    :param url: The URL to parse for a query string.
    :type url: str

    :return: A dictionary of query parameters.
    :rtype: dict[str, list[str]]
    """
    parsed_url = urlparse(url)
    qs = parsed_url.query
    parsed_qs = parse_qs(qs)

    return parsed_qs


def get_qs_dict_flat(url: str) -> dict[str, str]:
    """Returns an URL query string as key-value dictionary.

    This utility function returns a flattened dictionary of
    query arguments, ie.: Query parameters can be specified
    multiple times - this function only yields the first argument
    of each parameter. Empty parameters are mapped to empty string.
    
    :param url: The URL to parse for a query string.
    :type url: str

    :return: A flattened dictionary of query parameters
        (first element of query argument or empty string).
    :rtype: dict[str, str]
    """
    parsed_qs = get_qs_dict(url)

    flattened_qs = OrderedDict()

    for key in parsed_qs.keys():

        if parsed_qs[key] is None or len(parsed_qs[key]) == 0:
            flattened_qs[key] = ''
        
        flattened_qs[key] = parsed_qs[key][0]

    return flattened_qs


def get_qs_value(url: str, key: str, default: Any=None) -> Any:
    """Returns the value of a specific key of an URL query string.
    
    :param url: The URL to parse for a query string.
    :type url: str

    :param key: The key in the query string (&key1=value1&key2=value2 ...)
        whose value to return.
    :type key: str

    :param default: The default value to return if the
        key was not found.
    :type default: Any

    :return: The value of `key` in the query string or `default` otherwise.
    :rtype: Any
    """
    parsed_qs = get_qs_dict(url)

    result = parsed_qs.get(key, default)

    if result is default:
        return result
    
    if len(result) == 0:
        return None
    
    return result[0]


def split_url(url: str) -> NamedTuple:
    """Splits an URL into absolute base and file name URLs
    without query strings or anchors.

    Example URL:

        https://my.server/some/path/interesting.txt?k1=v1&a2=b4
    
    Becomes:

        (
            base_url='https://my.server/some/path',
            file_url='https://my.server/some/path/interesting.txt'
        )

    :param url: The URL string to split.
    :type url: str

    :return: A `NamedTuple` called `SplitURL` with keys (`base_url`, `file_url`).
    :rtype: NamedTuple
    """
    parsed_url = urlparse(url)

    # URL without query string et al
    file_url = f'{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}'

    # Base URL
    base_url = file_url.rsplit('/', 1)[0]

    SplitURL = namedtuple('SplitURL', ['base_url', 'file_url'])

    return SplitURL(base_url, file_url)


def open_url(url_to_open: str) -> None:
    """Opens an URL in a browser window.
    
    :param url_to_open: The URL to open in the browser.
    :type url_to_open: str
    """
    try:
        import webbrowser
        webbrowser.open(url_to_open, new=0, autoraise=True)

    except Exception:
        pass


def guess_user_agent(user_agents: dict, based_on_browser: str, default_ua: str) -> str:
    """Returns the guessed browser's user agent or a default one.
    
    :param user_agents: A dictionary of user agents for guessing.
    :type user_agents: dict

    :param based_on_browser: Basis browser identifier. (TODO: clarify/rename)
    :type based_on_browser: str

    :param default_ua: The fallback user-agent string.
    :type default_ua: str

    :return: The guessed browser's user agent or the default one.
    :rtype: str
    """

    if based_on_browser == 'Microsoft Edge':
        based_on_browser = 'Edg' # msedge only reports "Edg" as its identifier

        # could do the same for opera, opera gx, brave. but those are not supported by @jnrbsn's repo. so we just return chrome ua
        # in general his repo, does not provide the most accurate latest user-agents, if I am borred some time in the future,
        # I might just write my own similar repo and use that instead

    os_name = platform.system()

    try:
        if os_name == "Windows":
            for user_agent in user_agents:
                if based_on_browser in user_agent and "Windows" in user_agent:
                    match = re.search(r'Windows NT ([\d.]+)', user_agent)
                    if match:
                        os_version = match.group(1)
                        if os_version in user_agent:
                            return user_agent

        elif os_name == "Darwin":  # macOS
            for user_agent in user_agents:
                if based_on_browser in user_agent and "Macintosh" in user_agent:
                    match = re.search(r'Mac OS X ([\d_.]+)', user_agent)
                    if match:
                        os_version = match.group(1).replace('_', '.')
                        if os_version in user_agent:
                            return user_agent

        elif os_name == "Linux":
            for user_agent in user_agents:
                if based_on_browser in user_agent and "Linux" in user_agent:
                    match = re.search(r'Linux ([\d.]+)', user_agent)
                    if match:
                        os_version = match.group(1)
                        if os_version in user_agent:
                            return user_agent

    except Exception:
        raise RuntimeError(f'Regexing user-agent from online source failed: {traceback.format_exc()}')

    # TODO: Print, return value?
    #print_warning(f"Missing user-agent for {based_on_browser} & OS: {os_name}. Chrome & Windows UA will be used instead.")

    return default_ua
