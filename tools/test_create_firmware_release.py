import unittest

from create_firmware_release import (
    LEGAL_WORDS,
    METADATA_END_WORD,
    METADATA_START_WORD,
    build_reserved_image,
    goto_word,
    inspect_binary,
)


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

    def test_build_reserves_metadata_region_with_execution_guards(self):
        source = b"\x01\x00\x02\x00"
        image = build_reserved_image(source, 1)
        self.assertEqual(len(image), LEGAL_WORDS * 2)
        self.assertEqual(image[:4], source)
        self.assertEqual(int.from_bytes(image[METADATA_START_WORD * 2:METADATA_START_WORD * 2 + 2], "little"), goto_word(METADATA_START_WORD))
        self.assertEqual(int.from_bytes(image[METADATA_END_WORD * 2:METADATA_END_WORD * 2 + 2], "little"), goto_word(METADATA_END_WORD))
        self.assertEqual(image[(METADATA_START_WORD + 1) * 2:(METADATA_START_WORD + 2) * 2], b"\xff\xff")

    def test_rejects_code_collision_with_metadata_region(self):
        with self.assertRaisesRegex(ValueError, "collides"):
            build_reserved_image(b"\x01\x00", METADATA_START_WORD)


if __name__ == "__main__":
    unittest.main()
