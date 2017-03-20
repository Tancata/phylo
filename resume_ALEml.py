import os

# print a list of ALE files still to reconcile (for ALEml)
to_do = [file for file in os.listdir(".") if file.endswith(".ale")]
for file in to_do:
    if os.path.exists(file + ".ml_rec"):
        continue
    else:
        print file
