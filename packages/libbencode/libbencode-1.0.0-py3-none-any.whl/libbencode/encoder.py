from typing import Self

from .exceptions import BencodeError

class Encoder:
    """
    Bencode encoder.
    """
    
    @staticmethod
    def encode_int(data: int) -> bytes:
        """
        Encodes an integer into bencode format.
        
        Parameters:
            data (int): The integer value to encode.
        
        Returns:
            bytes: The bencoded representation of the integer.
        
        Example:
            >>> Encoder.encode_int(42)
            b'i42e'
        """
        return f"i{data}e".encode("utf-8")
    
    @staticmethod
    def encode_bytes(data: bytes) -> bytes:
        """
        Encodes bytes into bencode format.
        
        Parameters:
            data (bytes): The bytes to encode.
        
        Returns:
            bytes: The bencoded representation of the bytes.
        
        Example:
            >>> Encoder.encode_bytes(b"spam")
            b'4:spam'
        """
        return f"{len(data)}".encode("utf-8") + b":" + data
    
    @classmethod
    def encode_str(cls: type[Self], data: str) -> bytes:
        """
        Encodes a string into bencode format.
        
        Parameters:
            data (str): The string to encode.
        
        Returns:
            bytes: The bencoded representation of the string.
        
        Example:
            >>> Encoder.encode_str("spam")
            b'4:spam'
        """
        return f"{len(data)}:{data}".encode("utf-8")
    
    @classmethod
    def encode_list(cls: type[Self], data: list[int | bytes | str | list | dict | bool]) -> bytes:
        """
        Encodes a list into bencode format.
        
        Parameters:
            data (list): The list to encode. The list can contain integers, bytes, strings, lists, dictionaries or booleans.
        
        Raises:
            BencodeError: If an item in the list is of an unsupported type.
        
        Returns:
            bytes: The bencoded representation of the list.
        
        Example:
            >>> Encoder.encode_list(["spam", 42])
            b'l4:spami42ee'
        """
        encoded_list: bytes = b"l"
        for item in data:
            if isinstance(item, bool):
                encoded_list += cls.encode_bool(item)
            elif isinstance(item, int):
                encoded_list += cls.encode_int(item)
            elif isinstance(item, bytes):
                encoded_list += cls.encode_bytes(item)
            elif isinstance(item, str):
                encoded_list += cls.encode_str(item)
            elif isinstance(item, dict):
                encoded_list += cls.encode_dict(item)
            else:
                raise BencodeError(f"Unsupported type: {type(item)}; Supported types: int, bytes, str, list, dict, and bool")
        
        encoded_list += b"e"
        return encoded_list
    
    @classmethod
    def encode_dict(cls: type[Self], data: dict[bytes | str, int | bytes | str | list | dict | bool]) -> bytes:
        """
        Encodes a dictionary into bencode format.
        
        Parameters:
            data (dict): The dictionary to encode. Keys must be bytes or bytes, and values can be integers, bytes, strings, dictionaries, lists, or booleans.
        
        Raises:
            BencodeError: If a key or value in the dictionary is of an unsupported type.
        
        Returns:
            bytes: The bencoded representation of the dictionary.
        
        Example:
            >>> Encoder.encode_dict({"bar": "spam", "foo": 42})
            b'd3:bar4:spam3:fooi42ee'
        """
        encoded_dict: bytes = b"d"
        
        for key, value in data.items():
            if isinstance(key, bytes):
                encoded_dict += cls.encode_bytes(key)
            elif isinstance(key, str):
                encoded_dict += cls.encode_str(key)
            else:
                raise BencodeError(f"Unsupported dictionary key type: {type(key)}; Supported types: bytes and str")
            
            if isinstance(value, bool):
                encoded_dict += cls.encode_bool(value)
            elif isinstance(value, int):
                encoded_dict += cls.encode_int(value)
            elif isinstance(value, bytes):
                encoded_dict += cls.encode_bytes(value)
            elif isinstance(value, str):
                encoded_dict += cls.encode_str(value)
            elif isinstance(value, list):
                encoded_dict += cls.encode_list(value)
            elif isinstance(value, dict):
                encoded_dict += cls.encode_dict(value)
            else:
                raise BencodeError(f"Unsupported dictionary value type: {type(value)}; Supported types: int, bytes, str, list, dict, and bool")
        
        encoded_dict += b"e"
        return encoded_dict
    
    @classmethod
    def encode_bool(cls: type[Self], data: bool) -> bytes:
        """
        Encodes a boolean into bencode format.
        
        Parameters:
            data (bool): The boolean value to encode.
        
        Returns:
            bytes: The bencoded representation of the boolean.
        
        Example:
            >>> Encoder.encode_bool(True)
            b'i1e'
            >>> Encoder.encode_bool(False)
            b'i0e'
        """
        return cls.encode_int(int(data))
    
    @classmethod
    def encode(cls: type[Self], data: int | bytes | str | list | dict | bool) -> bytes:
        """
        Encodes data into bencode format.
        
        Parameters:
            data (int | bytes | str | list | dict | bool): The data to encode. Can be an integer, bytes, string, list, dictionary, or boolean.
        
        Raises:
            BencodeError: If the data is of an unsupported type.
        
        Returns:
            bytes: The bencoded representation of the data.
        
        Example:
            >>> Encoder.encode(42)
            b'i42e'
            >>> Encoder.encode("spam")
            b'4:spam'
        """
        if isinstance(data, bool):
            return cls.encode_bool(data)
        elif isinstance(data, int):
            return cls.encode_int(data)
        elif isinstance(data, bytes):
            return cls.encode_bytes(data)
        elif isinstance(data, str):
            return cls.encode_str(data)
        elif isinstance(data, list):
            return cls.encode_list(data)
        elif isinstance(data, dict):
            return cls.encode_dict(data)
        else:
            raise BencodeError(f"Unsupported data type: {type(data)}; Supported types: int, bytes, str, list, dict, and bool")