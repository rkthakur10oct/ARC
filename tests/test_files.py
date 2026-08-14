from tools.files import create_folder, create_file


folder = create_folder("ARC_TEST")

print("Folder:", folder)
print("Exists:", folder.exists())
print("Is directory:", folder.is_dir())

from tools.files import create_file


file = create_file("ARC_TEST.txt")

print("File:", file)
print("Exists:", file.exists())
print("Is file:", file.is_file())