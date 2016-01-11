import re

rgba = r".*(rgba?\(\d+,\s*\d+,\s*\d+,?\s*\d*\.*\d*\)).*"
hexc = r".*(#[A-Fa-f0-9]{6}).*"


def match(r, s):
  return re.match(r, s) != None


def groups(r, s):
  if match(r, s):
    return re.match(r, s).groups()
  else:
    return [None]


def to_dict(file):
  dict = {}
  with open(file) as inf:
    for line in inf:
      color = groups(rgba, line)[0]
      if color is None:
        color = groups(hexc, line)[0]
      if color is not None:
        if dict.get(color) is None:
          dict[color] = 0
        dict[color] += 1
  return dict


def to_sorted_array(dict):
  arr = []
  for key, value in dict.iteritems():
    arr.append({'color': key, 'num': value})
  arr.sort(key=lambda obj: obj['num'])
  arr = list(reversed(arr))
  return arr


def to_color_map(dict, initial=None):
  if not initial:
    initial = {}
  i = 0
  result = initial
  for obj in to_sorted_array(dict):
    if not obj['color'] in result:
      key = "@color" + `i`
      result[obj['color']] = key
      i += 1
  return result


def convert_file(file, newfile):
  dict = to_dict(file)
  initial_color_map = {}

  with open(file.replace('.less','_header.less')) as header:
    for line in header:
      split = line.split(':')
      color = split[1].split(';')[0].strip()
      variable = split[0].strip()
      initial_color_map[color] = variable

  color_map = to_color_map(dict, initial_color_map)

  open(newfile, 'w').close()

  with open(newfile, 'a') as converted:
    for color, variable in color_map.iteritems():
      converted.write(variable + ": " + color + ";\n")

  with open(newfile, 'a') as converted:
    converted.write("\n")

  with open(file) as original:
    with open(newfile, 'a') as converted:
      lines = original.readlines()
      for i, line in enumerate(lines):
        for color, variable in color_map.iteritems():
          if color in line:
            line = line.replace(color, variable)
        converted.write(line)


convert_file('temp.less', 'temp-converted.less')
