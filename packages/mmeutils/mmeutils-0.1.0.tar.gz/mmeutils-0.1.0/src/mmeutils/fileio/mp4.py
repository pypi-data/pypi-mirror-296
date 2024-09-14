"""MPEG-4 Binary File Manipulation

Kudos to Alfred Gutierrez' (alfg) and Sanjeev Pandey's well-summarizing articles:

https://dev.to/alfg/a-quick-dive-into-mp4-57fo
https://sanjeev-pandey.medium.com/understanding-the-mpeg-4-moov-atom-pseudo-streaming-in-mp4-93935e1b9e9a
"""


__all__ = [
    'MP4Box',
    'hash_mp4file',
    'get_boxes',
    'hash_mp4box',
]


import _hashlib
import os

from io import BufferedReader
from pathlib import Path
from typing import Any, Callable, Iterable, Optional, Union

from ..errors.mp4 import InvalidMP4Error


class MP4Box(object):
    """Represents an MPEG-4 binary box/atom object.
    """
    def __init__(self, size_bytes: bytes, fourcc_bytes: bytes, position: int) -> None:
        self.position = position
        self.size = int.from_bytes(size_bytes, byteorder='big')
        self.fourcc = MP4Box.convert_to_fourcc(fourcc_bytes)


    def __str__(self) -> str:
        return f'MP4Box ( Position: {self.position}, FourCC: {self.fourcc}, Size: {self.size} )'


    @staticmethod
    def convert_to_fourcc(fourcc_bytes: bytes) -> str:
        """Converts FourCC file header bytes to an ASCII string.

        :param fourcc_bytes: The FourCC bytes from the header.
        :type fourcc_bytes: bytes
        
        :return: An ASCII string.
        :rtype: str
        """
        fourcc: str = ''

        try:
            fourcc = str(fourcc_bytes, encoding='ascii')
        
        except UnicodeDecodeError:
            for by in fourcc_bytes:
                # See: http://facweb.cs.depaul.edu/sjost/it212/documents/ascii-pr.htm
                # 32-126 inclusive
                by_str: str = ''

                if (by < 32 or by > 126):
                    by_str = f'[{by}]'
                
                else:
                    by_str = chr(by)

                fourcc += by_str

        return fourcc



def get_boxes(reader: BufferedReader) -> Iterable[MP4Box]:
    """Fetches all box (atom) elements from an MPEG-4 file.
    
    :param reader: A buffered reader of the MPEG-4 file to process.
    :type reader: BufferedReader

    :return: Yields (generates) `MP4Box` objects.
    :rtype: Iterable[MP4Box]
    """
    position = 0
    first = True

    while reader.peek():
        size_bytes = reader.read(4)
        fourcc_bytes = reader.read(4)
        size = int.from_bytes(size_bytes, byteorder='big')

        # Cope with wide box sizes
        if size == 1:
            size_bytes = reader.read(8)

        box = MP4Box(
            size_bytes=size_bytes,
            fourcc_bytes=fourcc_bytes,
            position=position,
        )

        if first and box.fourcc != 'ftyp':
            raise InvalidMP4Error(f'File header missing, not an MPEG-4 file.')
        
        first = False

        position += box.size

        reader.seek(position, os.SEEK_SET)

        yield box


def hash_mp4box(algorithm: _hashlib.HASH, reader: BufferedReader, box: MP4Box) -> None:
    """Hashes an MPEG-4 box atom.
    
    The hash will be updated so you can use one `algorithm` object to chain
    function calls for different boxes yielding a total hash in the object.

    `algorithm` must be a `hashlib` hash algorithm.

    :param algorithm: The `hashlib` algorithm to use.
    :type algorithm: _hashlib.HASH

    :param reader: A buffered reader of the MPEG-4 file to process.
    :type reader: BufferedReader

    :param box: The box atom within the file to calculate the hash for.
    :type box: MP4Box
    """
    CHUNK_SIZE = 1_048_576

    reader.seek(box.position, os.SEEK_SET)

    chunks = box.size // CHUNK_SIZE
    remainder = box.size - chunks*CHUNK_SIZE

    for _ in range(chunks):
        algorithm.update(reader.read(CHUNK_SIZE))
    
    algorithm.update(reader.read(remainder))


def hash_mp4file(
            algorithm,
            file_name: Union[str, Path],
            print: Optional[Callable]=None,
            use_broken_algo: bool=False,
        ) -> str:
    """Hashes an MPEG-4 file selectively.

    MPEG-4 files may have different metadata and slightly different timing
    info although the embedded streams are the same on a binary level.
    This function tries to account for that fact by only hashing the
    essential file parts.

    :param algorithm: The `hashlib` algorithm to use.
    :type algorithm: _hashlib.HASH

    :param file_name: The path/file name of the MPEG-4 file to hash.
    :type file_name: str | Path

    :param print: A print callback for text output of file and hash info.
    :type print: Optional[Callable]

    :param use_broken_algo: Use a broken algorithm to calculate the hash.
        This function miscalculated the hash in the past due to a logic
        error but legacy and remedy code may rely on it.
    :type use_broken_algo: bool

    :return: The (selective) hash of the file as string.
    :rtype: str
    """
    file_name = Path(file_name)

    if not file_name.exists():
        raise RuntimeError(f'{file_name} does not exist.')

    file_size = file_name.stat().st_size

    if file_size < 8:
        raise InvalidMP4Error(f'{file_name} is too small to be an MPEG-4 file.')

    if print is not None:
        print(f'File: {file_name}')
        print()

    with open(file_name, 'rb') as mp4file:
        
        try:
            boxes = get_boxes(mp4file)

            for box in boxes:
                if print is not None:
                    print(box)

                if use_broken_algo:
                    if box.fourcc != 'moov' and box.fourcc != 'mdat':
                        hash_mp4box(algorithm, mp4file, box)

                else:
                    if box.fourcc != 'free' and box.fourcc != 'moov':
                        hash_mp4box(algorithm, mp4file, box)
            
            if print is not None:
                print()
                print(f'Hash: {algorithm.hexdigest()}')
                print()

            return algorithm.hexdigest()

        except InvalidMP4Error as ex:
            raise InvalidMP4Error(f'{file_name}: {ex}')
