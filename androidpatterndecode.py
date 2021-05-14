#!/usr/bin/env python3

__author__ = 'Chris Yereaztian'

"""
This script recovers the pattern combination from Android's pattern lock.
To acquire the gesture.key file you need a rooted device.
"""

from optparse import OptionParser
import binascii

def b2s(a):
    """
    Converts bytes to str
    """
    return "".join(list(map(chr, a))) 

def read_gesture(gesture_file_loc=""):
    """
    Reads gesture.key file and converts bytes to string
    """
    try:
        gesture_file = open(gesture_file_loc, "rb")
        sha1bytes = []
        for i in range(0, 20):
            sha1hash = gesture_file.read(1)
            sha1bytes.append(binascii.hexlify(sha1hash))
            # i += 1
        sha1hash = ""
        for i in range(0, 20):
            sha1hash += b2s(sha1bytes[i])
        return(sha1hash)
    except IOError:
        print("[-] Gesture file cannot be opened. File not present or permission denied")
        exit(1)

def match_pattern(dictionary="", sha1hash=""):
    """
    Looks up hash in provided dictionary
    """
    
    sha1hash = str.upper(sha1hash)
    dictionary_file = open(dictionary, "r")
    lines = dictionary_file.readlines()
    
    for line in lines:
        if line.__contains__(sha1hash):
            index = line.index(";", 0, 10)
            pattern = line[0:index]
            print("[+] Pattern retrieved from gesture.key file is: " + pattern)
            # print(pattern.center(80))


def parse_opt():
    # Create a option parser
    
    parser = OptionParser("python3 %prog -g <gesture.key> -d <dictionary file containing sha1 hashs>.\n\rThis program is used to recover android's pattern password.")
    
    # Add options
    
    parser.add_option("-g", "--gesture", type="string", dest="gesture_file", help="Path to your gesture.key file in your local system")
    parser.add_option("-d", "--dictionary", type="string", dest="dictionary_file", help="Path to your dictionary file containing sha1 hashes in your local system")
    
    # Parse options
    
    options, arguments = parser.parse_args()
    
    # Verify all options are used
    
    if options.gesture_file and options.dictionary_file:
        # Recover the pattern from the hash
        sha1hash = read_gesture(options.gesture_file)
        match_pattern(options.dictionary_file, sha1hash)

    else:
        # Show help screen in case of missing arguments
        parser.print_help()
        exit(1)

def main():
    parse_opt()

if __name__ == "__main__":
    main()