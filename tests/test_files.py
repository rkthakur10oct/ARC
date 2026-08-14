from tools.files import create_folder


folder = create_folder("ARC_TEST")

print("Folder:", folder)
print("Exists:", folder.exists())
print("Is directory:", folder.is_dir())