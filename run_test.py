import sys
import subprocess
# To run a test run:
# python run_test.py <name of test file>
subprocess.run(["python", "-m", "tests." + sys.argv[1].split(".py")[0]])
