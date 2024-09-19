from typing import Self

from .exceptions import BencodeError

class Decoder:
    """
    Bencode decoder.
    """
    
    @staticmethod
    def decode_int(data: bytes) -> tuple[int, int]:
        """
        Decodes a bencoded integer from bytes.
        
        Parameters:
            data (bytes): Bencoded integer.
        
        Returns:
            tuple[int, int]: The decoded integer and the position of the end byte.
        
        Raises:
            BencodeError: If the bencoded integer is malformed.
                - If the start byte 'i' is missing.
                - If the end byte 'e' is missing.
                - If there is no integer between 'i' and 'e'.
                - If the integer contains invalid characters, negative zero, or leading zeros.
        
        Example:
            >>> Decoder.decode_int(b"i42e")
            (42, 3)
        """
        start: int = data.find(b"i")
        if start == -1:
            raise BencodeError("Integer start not found")
        
        end: int = data.find(b"e")
        if end == -1:
            raise BencodeError("Integer end not found")
        
        if start+1 == end:
            raise BencodeError("Integer not found")
        
        if data[start+1:start+2] == b"-" and data[start+2:start+3] == b"0":
            raise BencodeError("Negative zero is not allowed")
        
        if data[start+1:start+2] == b"0" and start+2 != end:
            raise BencodeError("Leading zeros are not permitted")
        
        try:
            return (int(data[start+1:end]), end)
        except ValueError as exc:
            raise BencodeError(exc) from None
    
    @staticmethod
    def decode_str(data: bytes, encoding: str | None = None) -> tuple[bytes | str, int]:
        """
        Decodes a bencoded string from bytes.
        
        Parameters:
            data (bytes): Bencoded string.
            encoding (str | None): Optional encoding for string conversion. If None, returns bytes.
        
        Returns:
            tuple[bytes | str, int]: The decoded string and the position of the end byte.
        
        Raises:
            BencodeError: If the bencoded string is malformed.
                - If the colon separator is missing.
                - If the string length is negative or not matching the specified length.
                - If the string contains invalid characters.
        
        Example:
            >>> Decoder.decoded_str(b"4:spam")
            (b'spam', 5)
        """
        colon: int = data.find(b":")
        if colon == -1:
            raise BencodeError("String colon not found")
        
        try:
            length: int = int(data[:colon])
        except ValueError as exc:
            raise BencodeError(exc) from None
        
        if length < 0:
            raise BencodeError("Negative string length is not allowed")
        
        decoded_str: bytes = data[colon+1:colon+1 + length]
        if len(decoded_str) < length:
            raise BencodeError(f"String length is less than the specified length: {length}")
        
        return (decoded_str.decode(encoding) if encoding else decoded_str, colon+length)
    
    @classmethod
    def decode_list(cls: type[Self], data: bytes, encoding: str | None = None) -> tuple[list[int | bytes | str | list | dict], int]:
        """
        Decodes a bencoded list from bytes.
        
        Parameters:
            data (bytes): Bencoded list.
            encoding (str | None): Optional encoding for string conversion. If None, returns bytes.
        
        Returns:
            tuple[list[int | bytes | str | list | dict], int]: The decoded list and the position of the end byte.
        
        Raises:
            BencodeError: If the bencoded list is malformed.
                - If the start byte 'l' is missing.
                - If the end byte 'e' is missing or list elements are invalid.
        
        Example:
            >>> Decoder.decode_list(b"l4:spami42ee")
            ([b'spam', 42], 11)
        """
        start: int = data.find(b"l")
        if start == -1:
            raise BencodeError("List start not found")
        
        pos: int = start + 1
        length: int = len(data[pos:]) + 1
        
        items: list[bytes | str | int | list | dict] = []
        while pos < length:
            char: bytes = data[pos:pos+1]
            item: int | bytes | str | list | dict
            end: int
            if char == b"i":
                item, end = cls.decode_int(data[pos:])
                items.append(item)
                pos += end + 1
            elif b"0" <= char <= b"9":
                item, end = cls.decode_str(data[pos:], encoding)
                items.append(item)
                pos += end + 1
            elif char == b"l":
                item, end = cls.decode_list(data[pos:], encoding)
                items.append(item)
                pos += end + 1
            elif char == b"d":
                item, end = cls.decode_dict(data[pos:], encoding)
                items.append(item)
                pos += end + 1
            elif char == b"e":
                break
            else:
                raise BencodeError(f"Invalid character {char!r} at index {pos}")
        else:
            raise BencodeError("List end not found")
        
        return (items, pos)
    
    @classmethod
    def decode_dict(cls: type[Self], data: bytes, encoding: str | None = None) -> tuple[dict[bytes | str, int | bytes | str | list | dict], int]:
        """
        Decodes a bencoded dictionary from bytes.
        
        Parameters:
            data (bytes): Bencoded dictionary.
            encoding (str | None): Optional encoding for string conversion. If None, returns bytes.
        
        Returns:
            tuple[dict[bytes | str, int | bytes | str | list | dict], int]: The decoded dictionary and the position of the end byte.
        
        Raises:
            BencodeError: If the bencoded dictionary is malformed.
                - If the start byte 'd' is missing.
                - If the end byte 'e' is missing or dictionary entries are invalid.
        
        Example:
            >>> Decoder.decode_dict(b"d3:bar4:spam3:fooi42ee")
            ({b'bar': b'spam', b'foo': 42}, 21)
        """
        start: int = data.find(b"d")
        if start == -1:
            raise BencodeError("Dictionary start not found")
        
        pos: int = start + 1
        length: int = len(data[pos:]) + 1
        
        decoded_dict: dict[bytes | str, int | bytes | str | list | dict] = {}
        while pos < length:
            # Extract key.
            char: bytes = data[pos:pos+1]
            
            if char == b"e":
                break
            elif not b"0" <= char <= b"9":
                raise BencodeError(f"Invalid dictionary key character {char!r} at index {pos}")
            
            key: bytes | str
            end: int
            key, end = cls.decode_str(data[pos:], encoding)
            pos += end + 1
            
            # Extract value.
            char = data[pos:pos+1]
            value: int | bytes | str | list | dict
            
            if char == b"i":
                value, end = cls.decode_int(data[pos:])
                decoded_dict[key] = value
                pos += end + 1
            elif b"0" <= char <= b"9":
                value, end = cls.decode_str(data[pos:], encoding)
                decoded_dict[key] = value
                pos += end + 1
            elif char == b"l":
                value, end = cls.decode_list(data[pos:], encoding)
                decoded_dict[key] = value
                pos += end + 1
            elif char == b"d":
                value, end = cls.decode_dict(data[pos:], encoding)
                decoded_dict[key] = value
                pos += end + 1
            else:
                raise BencodeError(f"Invalid value character {char!r} at index {pos}")
        else:
            raise BencodeError("Dictionary end not found")
        
        return (decoded_dict, pos)
    
    @classmethod
    def decode(cls: type[Self], data: bytes, encoding: str | None = None) -> int | bytes | str | list | dict:
        """
        Decodes bencoded data from bytes into a Python object.
        
        Parameters:
            data (bytes): Bencoded data.
            encoding (str | None): Optional encoding for string conversion. If None, returns bytes.
        
        Returns:
            int | bytes | str | list | dict: The decoded Python object.
        
        Raises:
            BencodeError: If the bencoded data is invalid or malformed.
        """
        char: bytes = data[0:1]
        if char == b"i":
            return cls.decode_int(data)[0]
        elif b"0" <= char <= b"9":
            return cls.decode_str(data, encoding)[0]
        elif char == b"l":
            return cls.decode_list(data, encoding)[0]
        elif char == b"d":
            return cls.decode_dict(data, encoding)[0]
        else:
            raise BencodeError(f"Invalid bencode character: {char!r}")