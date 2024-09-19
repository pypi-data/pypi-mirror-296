import unittest
from typing import Self

from libbencode.exceptions import BencodeError
from libbencode.encoder import Encoder

class TestEncoder(unittest.TestCase):
    def test_encode_int(self: Self) -> None:
        data: int = 42
        expected_result: bytes = b"i42e"
        self.assertEqual(Encoder.encode_int(data), expected_result)
    
    def test_encode_bytes(self: Self) -> None:
        data: str = b"spam"
        expected_result: bytes = b"4:spam"
        self.assertEqual(Encoder.encode_bytes(data), expected_result)
    
    def test_encode_str(self: Self) -> None:
        data: str = "spam"
        expected_result: bytes = b"4:spam"
        self.assertEqual(Encoder.encode_str(data), expected_result)
    
    def test_encode_list(self: Self) -> None:
        data: tuple[list[str, int], int] = ["spam", 42]
        expected_result: bytes = b"l4:spami42ee"
        self.assertEqual(Encoder.encode_list(data), expected_result)
    
    def test_encode_list_unsupported_type(self: Self) -> None:
        with self.assertRaises(BencodeError) as context:
            Encoder.encode_list([object()])
        self.assertEqual(str(context.exception), "Unsupported type: <class 'object'>; Supported types: int, bytes, str, list, dict, and bool")
    
    def test_encode_dict(self: Self) -> None:
        data: dict[str, str | int] = {"bar": "spam", "foo": 42}
        expected_result: bytes = b"d3:bar4:spam3:fooi42ee"
        self.assertEqual(Encoder.encode_dict(data), expected_result)
    
    def test_encode_dict_unsupported_key_type(self: Self) -> None:
        with self.assertRaises(BencodeError) as context:
            Encoder.encode_dict({42: b'spam'})
        self.assertEqual(str(context.exception), "Unsupported dictionary key type: <class 'int'>; Supported types: bytes and str")
    
    def test_encode_dict_unsupported_value_type(self: Self) -> None:
        with self.assertRaises(BencodeError) as context:
            Encoder.encode_dict({b'bar': object()})
        self.assertEqual(str(context.exception), "Unsupported dictionary value type: <class 'object'>; Supported types: int, bytes, str, list, dict, and bool")
    
    def test_encode_bool(self):
        self.assertEqual(Encoder.encode_bool(True), b'i1e')
        self.assertEqual(Encoder.encode_bool(False), b'i0e')
    
    def test_encode(self: Self):
        self.assertEqual(Encoder.encode(42), b'i42e')
        self.assertEqual(Encoder.encode(b'spam'), b'4:spam')
        self.assertEqual(Encoder.encode("spam"), b'4:spam')
        self.assertEqual(Encoder.encode([b'spam', 42]), b'l4:spami42ee')
        self.assertEqual(Encoder.encode({'bar': b'spam', 'foo': 42}), b'd3:bar4:spam3:fooi42ee')
        self.assertEqual(Encoder.encode(True), b'i1e')
        self.assertEqual(Encoder.encode(False), b'i0e')
        
        with self.assertRaises(BencodeError) as context:
            Encoder.encode(object())
        self.assertEqual(str(context.exception), "Unsupported data type: <class 'object'>; Supported types: int, bytes, str, list, dict, and bool")

if __name__ == "__main__":
    unittest.main()