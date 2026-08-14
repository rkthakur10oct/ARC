from tools.files import create_file
from verification.files import file_exists


file = create_file("ARC_VERIFICATION_TEST.txt")

verified = file_exists(file)

print("File:", file)
print("Verified:", verified)