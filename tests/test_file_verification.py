from tools.files import create_folder
from verification.files import folder_exists


folder = create_folder("ARC_TEST")

verified = folder_exists(folder)

print("Folder:", folder)
print("Verified:", verified)