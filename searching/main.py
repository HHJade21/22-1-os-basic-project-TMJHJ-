import os, shutil

for root, subdirs, files in os.walk(r"C:\Users\USER\Desktop\2학년\자구\강의"):
    for f in files:
        if '해싱' in f:
            file_to_move = os.path.join(root, f)
            shutil.move(file_to_move, r"C:\Users\USER\Desktop\test1\결과")