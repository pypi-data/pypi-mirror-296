from typing import Callable

from .version import __version__
from .decoder import Decoder
from .encoder import Encoder

decode: Callable[[bytes], int | bytes | str | list | dict] = Decoder.decode
encode: Callable[[int | bytes | str | list | dict | bool], bytes] = Encoder.encode