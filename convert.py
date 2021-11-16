from __future__ import absolute_import
from __future__ import print_function
import os

for filename in os.listdir('.'):
    if filename.endswith('.py'):
        os.system("modernize -w " + filename + " --no-six")
        print(("Converting", filename + "..."))