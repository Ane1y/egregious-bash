import os.path
import re
from typing import List, Tuple

from src.Executable import BuiltIn


class Wc(BuiltIn):

    def exec(self, args: List[str]) -> int:
        files: List[str] = args
        stats: List[Tuple[int, int, int]] = []

        error: bool = False

        total_lns: int = 0
        total_wrd: int = 0
        total_bts: int = 0

        for file in files:
            try:
                with open(file, "r+") as f:
                    text = f.read()
            except OSError as e:
                print(f'wc: {e.filename}: {e.strerror}')
                error = True

            # Lines
            lns: int = text.count("\n")
            total_lns += lns

            # Words | split by spaces, filter out empty words
            wrd: int = len(list(filter(lambda word: word != "", re.split("\\s+", text))))
            total_wrd += wrd

            # Bytes
            bts: int = os.path.getsize(file)
            total_bts += bts

            stats.append((lns, wrd, bts))

        if len(files) > 1:
            stats.append((total_lns, total_wrd, total_bts))
            files.append("total")

        max_len = max([len(str(max(stat))) for stat in stats])

        for stat, file in zip(stats, files):
            for s in stat:
                print(f"{s:>{max_len}}", end=" ")
            print(file)

        if error:
            return 1
        return 0
