import unittest

from create_firmware_release import inspect_binary


class FirmwareReleaseTests(unittest.TestCase):
    def test_accepts_valid_pdk13_words(self):
        data = b"\x01\x00\xff\x1f"
        self.assertEqual(inspect_binary(data), (2, 1))

    def test_rejects_odd_binary(self):
        with self.assertRaisesRegex(ValueError, "complete 16-bit"):
            inspect_binary(b"\x01")

    def test_rejects_excluded_region(self):
        with self.assertRaisesRegex(ValueError, "excluded program words"):
            inspect_binary(bytes((0x3F6 * 2) + 2))

    def test_rejects_non_13_bit_word(self):
        with self.assertRaisesRegex(ValueError, "exceeds 13 bits"):
            inspect_binary(b"\x00\x20")

    def test_rejects_trailing_host_blank_words(self):
        with self.assertRaisesRegex(ValueError, "trailing host blank"):
            inspect_binary(b"\x01\x00\xff\xff")


if __name__ == "__main__":
    unittest.main()
