import glob
G_PATH = '/home/johmathe/starface/dataset/men/'
G_TRAIN_SET = '/home/johmathe/starface/dataset/train.txt'
G_VAL_SET = '/home/johmathe/starface/dataset/val.txt'
G_VALIDATION_RATIO = 0.1


def BuildClassesFromPath(path):
  """Create classes from a path."""
  flist = glob.glob('%s/*/*.jpg' %path)
  classes = {}
  next_id = 0
  artists_to_id = {}
  for fname in flist:
    artist = fname.split('/')[-2]
    if artist not in artists_to_id:
      artists_to_id[artist] = next_id
      next_id += 1
    classes.setdefault(artists_to_id[artist], []).append(fname)
  return classes


def SplitClassesTrainVal(classes, ratio):
  """Split classes into train and validation set"""
  training = {}
  val = {}
  for i, files in classes.iteritems():
    size = len(files)
    if size < 5:
      print 'dataset for class %d is small (%d < 5)' % (i, size)
    bound = int(ratio * size)
    assert bound >= 0
    assert bound <= size
    val[i] = files[:bound-1]
    training[i] = files[bound-1:]
  return (training, val)


def WriteSetToFile(classes, path):
  """Write to text file."""
  with open(path, 'w') as f:
    for i, files in classes.iteritems():
      for path in files:
        f.write('%s %d\n' % (path, i))


if __name__ == '__main__':
  """Main entry point."""
  classes = BuildClassesFromPath(G_PATH)
  training, val = SplitClassesTrainVal(classes, G_VALIDATION_RATIO)
  WriteSetToFile(training, G_TRAIN_SET)
  WriteSetToFile(val, G_VAL_SET)
  
