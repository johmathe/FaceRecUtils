import fileinput
import sys
import subprocess

G_CONVERT = 'convert'

def GetConvertCropParamsFromStdin():
  lines = []
  for l in sys.stdin:
    lines.append(l)

  lines = lines[:-1]

  cnt = 0
  convert_cmds = []
  for l in lines:
    params = [int(x) for x in l.split(' ')[:-1]]
    geometry = '%dx%d+%d+%d' % (params[2], params[3], params[0], params[1])
    output_file = '%s-h%d.jpg' % (sys.argv[1], cnt)
    convert_cmds.append('%s -crop %s %s' % (sys.argv[1], geometry, output_file))
    cnt += 1
  return convert_cmds

if __name__ == '__main__':
  params = GetConvertCropParamsFromStdin()
  for p in params:
    cmd = [G_CONVERT]
    cmd.extend(p.split(' '))
    print cmd
    subprocess.call(cmd)
