import subprocess


def pdfunite(*sourcefiles, destfile):

    args = ["/usr/bin/pdfunite"]
    args.extend(*sourcefiles)
    args.append(destfile)
    print(args)
    subprocess.run(args)
