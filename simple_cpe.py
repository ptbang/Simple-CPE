from cpe.cpe2_3_fs import CPE2_3_FS


class SimpleCPE(CPE2_3_FS):
    def get_values(self) -> dict[str, str]:
        values = self.get(CPE2_3_FS.KEY_APP)[0]  # type: ignore
        return {
            key: "ANY" if str(value) == "<ANY>" else str(value)
            for key, value in values.items()
        }


if __name__ == "__main__":
    import argparse
    from pprint import pprint

    parse = argparse.ArgumentParser()
    parse.add_argument("fs", help="string cpe v2.3")
    args = parse.parse_args()

    cpe = SimpleCPE(args.fs)
    pprint(cpe.get_values(), indent=4, sort_dicts=False)
