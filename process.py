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


def to_color_map(dict):
  i = 0
  result = {}
  for obj in to_sorted_array(dict):
    key = "@color" + `i`
    result[key] = obj['color']
    i += 1
  return result


def convert_file(file, newfile):
  dict = to_dict(file)
  color_map = to_color_map(dict)

  open(newfile, 'w').close()

  with open(newfile, 'a') as converted:
    for variable, color in color_map.iteritems():
      converted.write(variable + ": " + color + ";\n")

  with open(newfile, 'a') as converted:
      converted.write("\n")

  with open(file) as original:
    with open(newfile, 'a') as converted:
      lines = original.readlines()
      for i, line in enumerate(lines):
        for variable, color in color_map.iteritems():
          if color in line:
            line = line.replace(color, variable)
        converted.write(line)

convert_file('temp.less', 'temp-converted.less')
