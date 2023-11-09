import json
import subprocess
import unittest
from copy import copy

from simple_cpe import SimpleCPE


class SimpleCPETest(unittest.TestCase):
    KEYS = [
        "part",
        "vendor",
        "product",
        "version",
        "update",
        "edition",
        "language",
        "sw_edition",
        "target_sw",
        "target_hw",
        "other",
    ]
    CPE_23_FS_PREFIX = "cpe:2.3:"
    cpe_fs = (
        f"{CPE_23_FS_PREFIX}a:microsoft:internet_explorer:8.0.6001:beta:*:*:*:*:*:*"
    )

    @classmethod
    def setUpClass(cls) -> None:
        cls.cpe_dict = cls._fs_to_dict(cls.cpe_fs)

    def test_correct_fs(self) -> None:
        res = SimpleCPE(self.cpe_fs).get_values()
        self.assertEqual(res, self.cpe_dict)
        self.assertEqual(list(res.keys()), self.KEYS)
        self.assertEqual(res["other"], "ANY")

    def test_incorrect_fs(self) -> None:
        incorrect_dict = copy(self.cpe_dict)
        incorrect_dict["part"] = "incorrect-part"
        incorrect_fs = self._dict_to_fs(incorrect_dict)
        with self.assertRaises(ValueError):
            SimpleCPE(incorrect_fs)

        incorrect_dict = copy(self.cpe_dict)
        incorrect_dict["vendor"] = incorrect_dict["vendor"] + "#"
        incorrect_fs = self._dict_to_fs(incorrect_dict)
        with self.assertRaises(ValueError):
            SimpleCPE(incorrect_fs)

        incorrect_dict = copy(self.cpe_dict)
        incorrect_dict.pop("other")
        incorrect_fs = self._dict_to_fs(incorrect_dict)
        with self.assertRaises(ValueError):
            SimpleCPE(incorrect_fs)

    def test_shell_command_with_correct_fs(self) -> None:
        process = subprocess.run(
            ["python", "simple_cpe.py", self.cpe_fs], check=False, capture_output=True
        )
        out = process.stdout.decode()
        res = json.loads(out.replace("'", '"'))
        self.assertEqual(res, self.cpe_dict)

    def test_shell_command_with_incorrect_fs(self) -> None:
        incorrect_fs = self.cpe_fs[:-2]
        process = subprocess.run(
            ["python", "simple_cpe.py", incorrect_fs], check=False, capture_output=True
        )
        out = process.stderr.decode()
        self.assertIn("ValueError", out)
        self.assertEqual(process.returncode, 1)

    @classmethod
    def _fs_to_dict(cls, fs: str) -> dict[str, str]:
        cpe = fs[len(cls.CPE_23_FS_PREFIX) :].split(":")
        return {
            cls.KEYS[i]: cpe[i] if cpe[i] != "*" else "ANY"
            for i in range(len(cls.KEYS))
        }

    def _dict_to_fs(self, fs_dict: dict) -> str:
        return self.CPE_23_FS_PREFIX + ":".join(
            ["*" if value == "ANY" else value for value in fs_dict.values()]
        )


if __name__ == "__main__":
    unittest.main()
