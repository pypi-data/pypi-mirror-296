"""Errors/Exceptions"""


#region Constants

EXIT_SUCCESS: int = 0
EXIT_ERROR: int = -1
EXIT_ABORT: int = -2
UNEXPECTED_ERROR: int = -3
API_ERROR: int = -4
CONFIG_ERROR: int = -5
DOWNLOAD_ERROR: int = -6

#endregion

#region Exceptions

class ConfigError(RuntimeError):
    """This error is raised when configuration data is invalid.
    
    Invalid data may have been provided by configuration file or command-line.
    """

    def __init__(self, *args):
        super().__init__(*args)


class ApiError(RuntimeError):
    """This error is raised when an API yields no or invalid results.

    This may be caused by authentication issues (invalid token),
    invalid user names or - in rare cases - changes to the API itself.
    """

    def __init__(self, *args):
        super().__init__(*args)


class ApiAuthenticationError(ApiError):
    """This specific error is raised when an API
    yields an authentication error.

    This may primarily be caused by an invalid token.
    """

    def __init__(self, *args):
        super().__init__(*args)


class DownloadError(RuntimeError):
    """This error is raised when a file could not be downloaded.

    This may be caused by network errors, proxy errors, server outages
    and so on.
    """

    def __init__(self, *args):
        super().__init__(*args)


class M3U8Error(RuntimeError):
    """This error is raised when M3U8 data is invalid eg.
    no audio and no video both.
    """

    def __init__(self, *args):
        super().__init__(*args)

#endregion


__all__ = [
    'EXIT_ABORT',
    'EXIT_ERROR',
    'EXIT_SUCCESS',
    'API_ERROR',
    'CONFIG_ERROR',
    'DOWNLOAD_ERROR',
    'UNEXPECTED_ERROR',
    'ApiError',
    'ApiAuthenticationError',
    'ConfigError',
    'DownloadError',
    'M3U8Error',
]
