import chardet, re


def encode(path):
   rawdata = open(path, "rb").readline()
   return chardet.detect(rawdata)['encoding']

def removing_excess(value):

   regex_excess = re.compile("[().\s+\\n-]")

   return list(map(lambda x: regex_excess.sub("", x), value)) if type(value) == list else regex_excess.sub("", value)
