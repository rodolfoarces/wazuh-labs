from pathlib import Path
import os

str1=r"C:\app\files\1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e\1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e\1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e1\1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e\1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e\1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e\1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e\1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e\1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e\1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e1\1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e\1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e\test.txt"

print("Path has: " + str(len(str1)) + " characters")
path = Path(str1)
os.makedirs( path.parent.absolute(), exist_ok=True)
text_file = open(path, "w")
text_file.write(str(len(str1)))
text_file.close()