import os




def dirc(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
       


def setup():
    #making all dir..
    base_dir = os.getcwd()
    dirc(os.path.join(base_dir , "Databases"))
    dirc(os.path.join(base_dir , "db"))
    dirc(os.path.join(base_dir , "content"))

