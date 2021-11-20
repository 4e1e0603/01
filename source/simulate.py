# -*- coding: utf-8 -*-

import sys
import pathlib
import subprocess

data = pathlib.Path("./data")


if __name__ == "__main__":

    DELTA = 10
    STEPS = int(sys.argv[2])

    for step in range(10, STEPS, DELTA):

        with open(data / f"random_walk_(steps={step}).dat", encoding="utf-8", mode="w") as _file:
            subprocess.run(''.join(f"random_walk_main.exe 123 {step + DELTA} 1"), stdout=_file, shell=True, check=True)
            print(f"PROCESED {step} FILES\r", end="")

    print(f"PROCESED {step + DELTA} FILES\r")
