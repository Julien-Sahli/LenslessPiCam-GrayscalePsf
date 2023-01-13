import os
import pathlib as plib
from datetime import datetime


def make_dir(name, data_fp):

    save = os.path.basename(data_fp).split(".")[0]
    timestamp = datetime.now().strftime("_%d%m%d%Y_%Hh%M")
    save = name + save + timestamp
    save = plib.Path(__file__).parent / save
    original = save
    i = 0
    while os.path.exists(save):
        i += 1
        save = plib.Path(str(original) + "-" + str(i))
    save.mkdir(exist_ok=False)
    return save
