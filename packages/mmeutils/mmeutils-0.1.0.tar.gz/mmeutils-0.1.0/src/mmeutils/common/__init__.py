"""Common Utility Functions"""


import os
import platform
import subprocess

from pathlib import Path
from typing import Any, Iterable, List, Union


def batch_list(input_list: List[Any], batch_size: int) -> Iterable[List[Any]]:
    """Yields successive n-sized batches from input_list.
    
    :param input_list: An arbitrary list to split into equal-sized chunks.
    :type input_list: List[Any]

    :param batch_size: The number of elements in a chunk to
        split the list into. Batch size must be >= 1.
    :type batch_size: int

    :return: An iterable of sub-lists of size `batch_size`.
    :rtype: Iterable[List[Any]]
    """
    if batch_size < 1:
        raise ValueError(f'batch_list(): Invalid batch size of {batch_size} is less than 1.')

    for i in range(0, len(input_list), batch_size):
        yield input_list[i:i + batch_size]


def open_location(filepath: Union[str, Path]) -> bool:
    """Opens a directory in the platform's respective file manager application.

    :param filepath: The directory path.
    :type filepath: str | Path

    :return: True when the folder was opened or False otherwise.
    :rtype: bool
    """
    plat = platform.system()

    if not os.path.isfile(str(filepath)) and not os.path.isdir(str(filepath)):
        return False
    
    # tested below and they work to open folder locations
    if plat == 'Windows':
        # verified works
        os.startfile(str(filepath))

    elif plat == 'Linux':
        # verified works
        subprocess.run(['xdg-open', str(filepath)], shell=False)
        
    elif plat == 'Darwin':
        # verified works
        subprocess.run(['open', str(filepath)], shell=False)

    return True
