import os
import subprocess


def pdfseparate(filepath, pdfpagepattern):

    if not os.path.isfile(filepath):
        raise ValueError("Filepath %s is not a file" % filepath)

    if os.path.isdir(filepath):
        raise ValueError("Filepath %s is a directory!" % filepath)

    cmd = ' '.join([
        "/usr/bin/pdfseparate",
        filepath,
        pdfpagepattern
    ])
    print(cmd)
    ret = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        shell=True,
    )
    print(ret.stdout)
