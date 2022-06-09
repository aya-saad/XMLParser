import argparse


def parse_args():
    # Parse command line arguments
    ap = argparse.ArgumentParser(description="Aquagraph XML parser v1.0")
    ap.add_argument("-c", "--config", required=True,
                    help="path to config.ini file")
    # ap.add_argument("-i", "--input", required=True,
    #                help="path to input image file or directory")

    # ap.add_argument("-o", "--output", default="output",
    #                help="path to output directory (default: output)")
    ap.add_argument("-p", "--progress", action="store_true",
                    help="display progress")
    return ap.parse_args()


def walkdir(files):
    for filename in files:
        yield filename

def get_id(name):
    name_list = []

    if name is not None:
        name_id = ""
        for i in range(0, len(name)):
            name_list.append(ord(name[i]))
        for el in name_list:
            name_id += str(el)
    else:
        name_id = 0
    return int(name_id)

def get_fl_id(name):
    name_list = []
    name_id = ""
    #for i in range(0, len(name)):
    name_list.append(ord(name[0]))
    name_list.append(ord(name[len(name)-1]))
    for el in name_list:
        name_id += str(el)
    return int(name_id)

def find_key_value(key):
    val = None
    if key is not None:
        val = key.text
    return val
