"""MPEG-4 File Processing Errors"""


class InvalidMP4Error(RuntimeError):
    """This error is raised when an invalid MP4 has been found.
    
    A file is primarily invalid when it does not have a proper
    header with an "ftyp" FourCC code or is smaller than 8 bytes in size.
    The file might also have been corrupted (truncated).
    """

    def __init__(self, *args):
        super().__init__(*args)
