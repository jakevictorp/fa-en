
import sys, getopt, codecs, os, re

#NOTE: many of these characters are Arabic-specific, but they will be retained in case of certain "non-Persianized"
#loan-words, quotes from the Quran, etc.        Modifications made by Jake Perl
buck2uni = {"'": u"\u0621",  # hamza-on-the-line
            "|": u"\u0622",  # madda
            ">": u"\u0623",  # hamza-on-'alif
            "&": u"\u0624",  # hamza-on-waaw
            "<": u"\u0625",  # hamza-under-'alif
            "}": u"\u0626",  # hamza-on-yaa'
            "A": u"\u0627",  # bare 'alif
            "b": u"\u0628",  # baa'
            "P": u"\u0629",  # taa' marbuuTa (changed from "p" to "P" to free up "p" for the Persian letter pe)
            "t": u"\u062A",  # taa'
            "^": u"\u062B",  # thaa' (changed from "v" to "^" in order to free up "v" for Persian vaav, also the
                                # symbol "^" resembles the Farsi shorthand for the three dots above the letter thaa')
            "j": u"\u062C",  # jiim
            "H": u"\u062D",  # Haa'
            "x": u"\u062E",  # khaa'
            "d": u"\u062F",  # daal
            "*": u"\u0630",  # dhaal
            "r": u"\u0631",  # raa'
            "z": u"\u0632",  # zaay
            "s": u"\u0633",  # siin
            "$": u"\u0634",  # shiin
            "S": u"\u0635",  # Saad
            "D": u"\u0636",  # Daad
            "T": u"\u0637",  # Taa'
            "Z": u"\u0638",  # Zaa' (DHaa')
            "E": u"\u0639",  # cayn
            "G": u"\u063A",  # ghayn (to be transliterated as "G" instead of "g" to free up "g" for Persian gaaf)
            "_": u"\u0640",  # taTwiil
            "f": u"\u0641",  # faa'
            "q": u"\u0642",  # qaaf
            "k": u"\u0643",  # kaaf
            "l": u"\u0644",  # laam
            "m": u"\u0645",  # miim
            "n": u"\u0646",  # nuun
            "h": u"\u0647",  # haa'
            "v": u"\u0648",  # vaav (changed from "w" to "v" to better represent Farsi phonetics)
            "Y": u"\u0649",  # 'alif maqSuura
            "y": u"\u064A",  # yaa'
            "F": u"\u064B",  # fatHatayn
            "N": u"\u064C",  # Dammatayn
            "K": u"\u064D",  # kasratayn
            "a": u"\u064E",  # fatHa
            "u": u"\u064F",  # Damma
            "i": u"\u0650",  # kasra
            "~": u"\u0651",  # shaddah
            "o": u"\u0652",  # sukuun
            "`": u"\u0670",  # dagger 'alif
            "{": u"\u0671",  # waSla
            #The following are additional Persian-specific or other extra characters to be transliterated
            #Added by Jake Perl
            "1": u"\u06F1",  # one
            "2": u"\u06F2",  # two
            "3": u"\u06F3",  # three
            "4": u"\u0664",  # four (Arabic-specific, included in case of mis-encoded numerals)
            "5": u"\u0665",  # five (Arabic-specific, included in case of mis-encoded numerals)
            "6": u"\u0666",  # six (Arabic-specific, included in case of mis-encoded numerals)
            "4": u"\u06F4",  # four (different from Arabic)
            "5": u"\u06F5",  # five (different from Arabic)
            "6": u"\u06F6",  # six (different from Arabic)
            "7": u"\u06F7",  # seven
            "8": u"\u06F8",  # eight
            "9": u"\u06F9",  # nine
            "0": u"\u06F0",  # zero
            "y": u"\u06CC",  # ye (in Farsi, ye is encoded differently due to differences in representation
                                # depending on position. The Arabic ye (u064A above) will still be included in case
                                # of mis-encodings or Arabic language text, and both with be transliterated as "y")
            "k": u"\u06A9",  # kaaf (sometimes final position kaaf is represented differently in Farsi than in Arabic,
                                #so this kaaf is included in addition to u0643 above, as they are both considered to be
                                #the same letter in Farsi
            "g": u"\u06AF",  # gaaf (does not exist in Arabic)
            "p": u"\u067E",  # pe (does not exist in Arabic)
            "J": u"\u0698",  # zhe (does not exist in Arabic)
            "C": u"\u0686",  # che (does not exist in Arabic)
            }

# For a reverse transliteration (Unicode -> Buckwalter), a dictionary
# which is the reverse of the above buck2uni is essential.

uni2buck = {}

# Iterate through all the items in the buck2uni dict.
for (key, value) in buck2uni.items():
    # The value from buck2uni becomes a key in uni2buck, and vice
    # versa for the keys.
    uni2buck[value] = key

# Declare some global variables...


inFilename_no_ext = (input("Type name of file (without extension) to be transliterated: "))  # Name of filename containing input.
inFilename = inFilename_no_ext + ".xml"
outFilename = inFilename_no_ext + "_translit.xml"  # Name of filename to send the output
#outFilename = "wiki0.fa-en_translit.xml"  # Name of filename to send the output
inEnc = "UTF-8"  # The text encoding of the input file
outEnc = "UTF-8"  # The text encoding for the output file
ignoreChars = ""  # If lines begin with these symbols, ignore.
columnRange = ""  # Holds columns numbers to transliterate.
delimiter = ""  # Holds user-defined column delimiter.
reverse = 1  # When equal to 1, perform reverse transliteration, i.e.,
# Unicode -> Buckwalter.

# A function to print to screen the usage details of this script.

def usage():
    print
    "Usage:", sys.argv[0], "-i INFILE -o OUTFILE [-g CHARS -c RANGE -d CHAR"
    print
    "       -r -e INPUT_ENCODING, -E OUTPUT ENCODING]"
    print
    "      ", sys.argv[0], "-l"
    print
    "      ", sys.argv[0], "-h"
    print
    ""
    print
    "  -i INFILE, --input=INFILE:"
    print
    "    Path to text file to be transliterated to Unicode."
    print
    "  -o OUTFILE, --output=OUTFILE:"
    print
    "    Path of file to output the newly transliterated text."
    print
    "  -e ENC, --input-encoding=ENC:"
    print
    "    Specify the text encoding of the source file. Default: latin_1."
    print
    "  -E ENC, --output-encoding=ENC:"
    print
    "    Specify the text encoding of the target file. Default: utf_8."
    print
    "  -g CHARS, --ignore-lines=CHARS:"
    print
    "    Will not transliterate lines that start with any of the CHARS"
    print
    "    given. E.g., -g #; will not alter lines starting with # or ;."
    print
    "    (May need to be -g \#\; on some platforms. See README.txt.)"
    print
    "  -c RANGE, --columns=RANGE:"
    print
    "    If in columns, select columns to apply transliteration. Can be"
    print
    "    comma separated numbers, or a range. E.g., -c 1, -c 1-3, -c 1,3."
    print
    "  -d CHAR, --delimiter=CHAR:"
    print
    "    Specify the delimiter that defines the column if using the -c"
    print
    "    option above. Default is ' ' (space)."
    print
    "  -r, --reverse:"
    print
    "    Reverses the transliteration, i.e., Arabic to Buckwalter."
    print
    "    When used, it will change the default input encoding to utf_8 and"
    print
    "    output encoding to latin_1"
    print
    "  -l, --list-encodings:"
    print
    "    Displays all supported file encodings."
    print
    "  -h, --help:"
    print
    "    Displays this page."
    print
    ""


# A function to print to screen all the available encodings supported by
# Python.

def displayEncodings():
    print
    "Codec		Aliases				Languages"
    print
    "ascii		646, us-ascii 			English"
    print
    "cp037 		IBM037, IBM039 			English"
    print
    "cp424 		EBCDIC-CP-HE, IBM424		Hebrew"
    print
    "cp437 		437, IBM437 			English"
    print
    "cp500 		EBCDIC-CP-BE, EBCDIC-CP-CH, IBM500 	Western Europe"
    print
    "cp737						Greek"
    print
    "cp775 		IBM775				Baltic languages"
    print
    "cp850 		850, IBM850 			Western Europe"
    print
    "cp852 		852, IBM852 			Central and Eastern Europe"
    print
    "cp855 		855, IBM855 			Bulgarian, Byelorussian, Macedonian, Russian, Serbian"
    print
    "cp856 		 	 			Hebrew"
    print
    "cp857 		857, IBM857 			Turkish"
    print
    "cp860 		860, IBM860 			Portuguese"
    print
    "cp861 		861, CP-IS, IBM861		Icelandic"
    print
    "cp862 		862, IBM862 			Hebrew"
    print
    "cp863 		863, IBM863 			Canadian"
    print
    "cp864 		IBM864				Arabic"
    print
    "cp865 		865, IBM865 			Danish, Norwegian"
    print
    "cp869 		869, CP-GR, IBM869 		Greek"
    print
    "cp874 	  					Thai"
    print
    "cp875 	  					Greek"
    print
    "cp1006 	  					Urdu"
    print
    "cp1026 		ibm1026				Turkish"
    print
    "cp1140 		ibm1140				Western Europe"
    print
    "cp1250 		windows-1250 			Central and Eastern Europe"
    print
    "cp1251 		windows-1251 			Bulgarian, Byelorussian, Macedonian, Russian, Serbian"
    print
    "cp1252 		windows-1252 			Western Europe"
    print
    "cp1253 		windows-1253 			Greek"
    print
    "cp1254 		windows-1254 			Turkish"
    print
    "cp1255 		windows-1255 			Hebrew"
    print
    "cp1256 		windows-1256 			Arabic"
    print
    "cp1257 		windows-1257		 	Baltic languages"
    print
    "cp1258 		windows-1258		 	Vietnamese"
    print
    "latin_1		iso-8859-1, iso8859-1, 8859, cp819, latin, latin1, L1	West Europe"
    print
    "iso8859_2 	iso-8859-2, latin2, L2		Central and Eastern Europe"
    print
    "iso8859_3 	iso-8859-3, latin3, L3		Esperanto, Maltese"
    print
    "iso8859_4 	iso-8859-4, latin4, L4		Baltic languagues"
    print
    "iso8859_5 	iso-8859-5, cyrillic		Bulgarian, Byelorussian, Macedonian, Russian, Serbian"
    print
    "iso8859_6 	iso-8859-6, arabic		Arabic"
    print
    "iso8859_7 	iso-8859-7, greek, greek8	Greek"
    print
    "iso8859_8 	iso-8859-8, hebrew		Hebrew"
    print
    "iso8859_9 	iso-8859-9, latin5, L5		Turkish"
    print
    "iso8859_10 	iso-8859-10, latin6, L6 	Nordic languages"
    print
    "iso8859_13 	iso-8859-13			Baltic languages"
    print
    "iso8859_14 	iso-8859-14, latin8, L8		Celtic languages"
    print
    "iso8859_15 	iso-8859-15			Western Europe"
    print
    "koi8_r						Russian"
    print
    "koi8_u						Ukrainian"
    print
    "mac_cyrillic	maccyrillic			Bulgarian, Byelorussian, Macedonian, Russian, Serbian"
    print
    "mac_greek	macgreek			Greek"
    print
    "mac_iceland	maciceland			Icelandic"
    print
    "mac_latin2	maclatin2, maccentraleurope	Central and Eastern Europe"
    print
    "mac_roman 	macroman 			Western Europe"
    print
    "mac_turkish 	macturkish 			Turkish"
    print
    "utf_16 		U16, utf16 			all languages"
    print
    "utf_16_be 	UTF-16BE 			all languages (BMP only)"
    print
    "utf_16_le 	UTF-16LE 			all languages (BMP only)"
    print
    "utf_7 		U7 				all languages"
    print
    "utf_8 		U8, UTF, utf8 			all languages"


def parseIgnoreString(string):
    symbols = []

    for char in string:
        symbols.append(char)

    return symbols


# Begin parsing the command-line arguments...

try:
    (options, args) = getopt.getopt(sys.argv[1:], "i:o:e:E:g:c:d:rlh",
                                    ["input=", "output=", "input-encoding=", "output-encoding=",
                                     "ignore-lines=", "columns=", "delimiter=" "reverse", "list-encodings",
                                     "help"])

except getopt.GetoptError:
    # print help information and exit:
    usage()
    sys.exit(1)

# Loop over all arguments supplied by the user.
for (x, y) in options:
    if x in ("-h", "--help"):
        usage()
        sys.exit(0)

    if x in ("-l", "--list-encodings"):
        displayEncodings()
        sys.exit(0)

    if x in ("-i", "--input"): inFilename = y
    if x in ("-o", "--output"): outFilename = y
    if x in ("-e", "--input-encoding"): inEnc = y
    if x in ("-E", "--output-encoding"): outEnc = y
    if x in ("-r", "--reverse"): reverse = 1
    if x in ("-g", "--ignore-lines"): ignoreChars = y
    if x in ("-c", "--columns"): columnRange = y
    if x in ("-d", "--delimiter"):
        delimiter = y
        # Tabs come in off the command line from "\\t" to "\t". However,
        # that's equivalent to "\\t" from python's point of view.
        # Therefore replace any inputted "tabs" with proper tabs before
        # proceeding.
        delimiter = delimiter.replace("\\t", "\t")
        # Do some error checking
        if len(delimiter) > 1:
            print >> sys.stderr, "Delimeter should only be a single character. Using first character" + delimiter[0]
            delimiter = delimiter[0]

        if buck2uni.get(delimiter):
            print >> sys.stderr, "Invalid delimiter. \"" + delimiter + "\" is part of the Buckwalter character set."
            print >> sys.stderr, "This will obviously cause much confusion as a delimiter!"
            print >> sys.stderr, "Please try again. Aborting..."
            sys.exit(1)

# If no delimiter was set then, set the default to " " (space)
if not delimiter:
    delimiter = " "

# If user didn't specify the encoding of the input file, then revert to
# defaults. The defaults can depending on the direction of
# transliteration:
#
# Buckwalter -> Unicode, default = latin1
# Unicode -> Buckwalter, default = utf_8


if not inEnc:
    if reverse:
        inEnc = "utf_8"
    else:
        inEnc = "latin_1"

# Similarly, if user didn't specify the encoding of the output file,
# then revert to defaults. The defaults can depending on the direction
# of transliteration:
#
# Buckwalter -> Unicode, default = utf_8
# Unicode -> Buckwalter, default # = latin_1

if not outEnc:
    if reverse:
        outEnc = "latin_1"
    else:
        outEnc = "utf_8"

# Ok, let's get the files open!

# Providing a file for output was specified...
if outFilename:
    try:
        # Create a file object, set it to "write" mode using the
        # specified output encoding.
        outFile = codecs.open(outFilename, "w", outEnc)

    except IOError as msg:
        # A problem occurred when trying to open this file. Report to
        # user...
        print
        msg
        sys.exit(1)

# Script can not work without somewhere to store the transliteration.
# Exit.
else:
    print
    "Must specify a file to use store the output! Aborting..."
    sys.exit(1)

# Providing a file for input was specified...
if inFilename:
    try:
        # Create a file object, set it to "read" mode using the
        # specified input encoding.
        inFile = codecs.open(inFilename, "r", inEnc)

    except IOError as msg:
        # A problem occurred when trying to open this file. Report to
        # user...
        print
        msg
        sys.exit(1)

# This script requires a file to read from. Exit.
else:
    print
    "Must specify a file to use as input! Aborting..."
    sys.exit(1)


def getColsFromRange(cRange):
    columns = []
    hyphenSearch = re.compile(r'-')

    rangeElements = cRange.split(",")

    for i in rangeElements:
        # If it contains a hyphen (e.g., 1-3)
        if hyphenSearch.search(i):
            [start, end] = i.split("-")
            columns = columns + range(int(start) - 1, int(end))
        else:
            columns.append(int(i) - 1)

    return columns


# This function transliterates a given string. It checks the direction
# of the transliteration and then uses the appropriate dictionary. A
# transliterated string is returned.

def transliterate(inString, lineNumber):
    out = ""

    if columnRange:
        columns = getColsFromRange(columnRange)

        # Split the line on the delimiter
        lineCols = inString.split(delimiter)

        # Iterate over each column. If it's one of the ones in the range
        # specified, then transliterate, otherwise just output column
        # unchanged.

        for i in range(len(lineCols)):

            # If first column, then don't prefix the delimiter
            if i == 0:
                if i in columns:
                    out = transliterateString(lineCols[i])
                else:
                    out = lineCols[i]
            else:
                if i in columns:
                    out = out + delimiter + transliterateString(lineCols[i])
                else:
                    out = out + delimiter + lineCols[i]

    else:
        out = transliterateString(inString)

    return out


def transliterateString(inString):
    out = ""

    # For normal Buckwalter -> Unicode transliteration..
    if not reverse:

        # Loop over each character in the string, inString.
        for char in inString:
            # Look up current char in the dictionary to get its
            # respective value. If there is no match, e.g., chars like
            # spaces, then just stick with the current char without any
            # conversion.
            out = out + buck2uni.get(char, char)

    # Same as above, just in the other direction.
    else:

        for char in inString:
            out = out + uni2buck.get(char, char)

    return out


# while 1:
#	line = inFile.readline().strip()
#	line = line.decode(inEnc)
#	if not line:
#		break

# process string
#	outFile.write(transliterate(line) + os.linesep)

# Read in the lines of the input file.
lines = inFile.readlines()

currentLineNumber = 1
# Loop over each line
for line in lines:
    line = line.strip()
    try:
        # Transliterate the current line, and then write the output to
        # file.

        if not ignoreChars:
            outFile.write(transliterate(line, currentLineNumber) + " " + os.linesep)
        else:
            if line[0] in parseIgnoreString(ignoreChars):
                outFile.write(line + " " + os.linesep)
            else:
                outFile.write(transliterate(line, currentLineNumber) + " " + os.linesep)

        currentLineNumber = currentLineNumber + 1

    except UnicodeError as msg:
        # A problem when writing occurred. Report to user...
        print
        msg
        sys.exit(1)

# All done! Better close the files used before terminating...
inFile.close()
outFile.close()

# ... and relax! :)

