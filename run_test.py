import sys
import os
import subprocess
# To run a test run:
# python run_test.py <name of test file>

if sys.argv[1] == "-a":
    for name in os.listdir('./tests'):
        if name == "__pycache__":
            continue
        subprocess.run(["python", "-m", "tests." + name.split(".py")[0]])
else:
    for i in range(len(sys.argv) - 1):
        subprocess.run(["python", "-m", "tests." +
                       sys.argv[i + 1].split(".py")[0]])
