import unittest
from typing import Self

from libbencode.exceptions import BencodeError
from libbencode.decoder import Decoder

class TestDecoder(unittest.TestCase):
    def test_decode_int(self: Self) -> None:
        data: bytes = b"i42e"
        expected_result: tuple[int, int] = (42, 3)
        self.assertEqual(Decoder.decode_int(data), expected_result)
    
    def test_decode_int_missing_start_byte(self):
        with self.assertRaises(BencodeError) as context:
            Decoder.decode_int(b"42e")
        self.assertEqual(str(context.exception), "Integer start not found")
    
    def test_decode_int_missing_end_byte(self):
        with self.assertRaises(BencodeError) as context:
            Decoder.decode_int(b"i42")
        self.assertEqual(str(context.exception), "Integer end not found")
    
    def test_decode_int_missing_integer(self):
        with self.assertRaises(BencodeError) as context:
            Decoder.decode_int(b"ie")
        self.assertEqual(str(context.exception), "Integer not found")
    
    def test_decode_int_negative_zero(self):
        with self.assertRaises(BencodeError) as context:
            Decoder.decode_int(b"i-0e")
        self.assertEqual(str(context.exception), "Negative zero is not allowed")
    
    def test_decode_int_leading_zeros(self):
        with self.assertRaises(BencodeError) as context:
            Decoder.decode_int(b"i012e")
        self.assertEqual(str(context.exception), "Leading zeros are not permitted")
    
    def test_decode_int_invalid_format(self):
        with self.assertRaises(BencodeError) as context:
            Decoder.decode_int(b"i4a2e")
        self.assertEqual(str(context.exception), "invalid literal for int() with base 10: b'4a2'")
    
    def test_decode_str(self: Self) -> None:
        data: bytes = b"4:spam"
        expected_result: tuple[bytes, int] = (b"spam", 5)
        self.assertEqual(Decoder.decode_str(data), expected_result)
    
    def test_decode_str_with_encoding(self: Self) -> None:
        data: bytes = b"4:spam"
        expected_result: tuple[bytes, int] = ("spam", 5)
        self.assertEqual(Decoder.decode_str(data, encoding="utf-8"), expected_result)
    
    def test_decode_str_missing_colon(self):
        with self.assertRaises(BencodeError) as context:
            Decoder.decode_str(b"4spam")
        self.assertEqual(str(context.exception), "String colon not found")
    
    def test_decode_str_invalid_length(self):
        with self.assertRaises(BencodeError) as context:
            Decoder.decode_str(b"invalid:spam")
        self.assertEqual(str(context.exception), "invalid literal for int() with base 10: b'invalid'")
    
    def test_decode_str_negative_length(self):
        with self.assertRaises(BencodeError) as context:
            Decoder.decode_str(b"-4:spam")
        self.assertEqual(str(context.exception), "Negative string length is not allowed")
    
    def test_decode_str_length_mismatch(self):
        with self.assertRaises(BencodeError) as context:
            Decoder.decode_str(b"4:sp")
        self.assertEqual(str(context.exception), "String length is less than the specified length: 4")
    
    def test_decode_str_empty_string(self):
        result = Decoder.decode_str(b"0:")
        self.assertEqual(result, (b"", 1))
    
    def test_decode_list(self: Self) -> None:
        data: bytes = b"l4:spami42ee"
        expected_result: tuple[list[str, int], int] = ([b"spam", 42], 11)
        self.assertEqual(Decoder.decode_list(data), expected_result)
    
    def test_decode_list_with_encoding(self: Self) -> None:
        data: bytes = b"l4:spami42ee"
        expected_result: tuple[list[str, int], int] = (["spam", 42], 11)
        self.assertEqual(Decoder.decode_list(data, encoding="utf-8"), expected_result)
    
    def test_decode_list_empty(self):
        result = Decoder.decode_list(b"le")
        self.assertEqual(result, ([], 1))
    
    def test_decode_list_missing_start(self):
        with self.assertRaises(BencodeError) as context:
            Decoder.decode_list(b"4:spami42ee")
        self.assertEqual(str(context.exception), "List start not found")
    
    def test_decode_list_missing_end(self):
        with self.assertRaises(BencodeError) as context:
            Decoder.decode_list(b"l4:spami42e")
        self.assertEqual(str(context.exception), "List end not found")
    
    def test_decode_dict(self: Self) -> None:
        data: bytes = b"d3:bar4:spam3:fooi42ee"
        expected_result: tuple[dict[str, str | int], int] = ({b"bar": b"spam", b"foo": 42}, 21)
        self.assertEqual(Decoder.decode_dict(data), expected_result)
    
    def test_decode_dict_with_encoding(self: Self) -> None:
        data: bytes = b"d3:bar4:spam3:fooi42ee"
        expected_result: tuple[dict[str, str | int], int] = ({"bar": "spam", "foo": 42}, 21)
        self.assertEqual(Decoder.decode_dict(data, encoding="utf-8"), expected_result)
    
    def test_decode_dict_missing_start(self):
        with self.assertRaises(BencodeError) as context:
            Decoder.decode_dict(b"3:bar4:spam3:fooi42ee")
        self.assertEqual(str(context.exception), "Dictionary start not found")
    
    def test_decode_dict_missing_end(self):
        with self.assertRaises(BencodeError) as context:
            Decoder.decode_dict(b"d3:bar4:spam3:fooi42e")
        self.assertEqual(str(context.exception), "Dictionary end not found")
    
    def test_decode_dict_empty(self):
        result = Decoder.decode_dict(b"de")
        self.assertEqual(result, ({}, 1))
    
    def test_decode_invalid(self):
        with self.assertRaises(BencodeError) as context:
            Decoder.decode(b"x")
        self.assertEqual(str(context.exception), "Invalid bencode character: b'x'")

if __name__ == "__main__":
    unittest.main()