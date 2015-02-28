import sys
import tempfile
import trimfaces
import urllib
import subprocess
import artists

G_CNN_CLASSIFY = '/home/johmathe/ccv/bin/cnnclassify'
G_FACEMODEL = '/home/johmathe/starface/ccv_working_dir/starface.sqllit'

def ClassifyFace(face_path):
  binary_args = [G_CNN_CLASSIFY, face_path, G_FACEMODEL]
  p = subprocess.Popen(
    binary_args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  
  artists_found = []
  output, err = p.communicate()
  # Parse result from scddetect
  output = output.split(' ')
  for i in range(len(output) / 2 - 2):
    artist_name = artists.ARTISTS[int(output[2*i])]
    artist_prob = output[2*i+1]
    artists_found.append((artist_name, artist_prob))
  print artists_found
 
  return artists_found

def DownloadAndClassify(img_url, face_id):
  image_path = tempfile.NamedTemporaryFile().name
  print 'downloading %s to %s' % (img_url, image_path)
  urllib.urlretrieve(img_url, image_path)
  image_prefix = image_path
  results = trimfaces.TrimFacesFromPic(image_path, image_prefix)
  if len(results) == 0:
    print 'No faces found'
    return 1
  else:
    print 'Found %d faces' % len(results)
  ClassifyFace(results[face_id])

if __name__ == '__main__':
  if len(sys.argv) == 3:
    DownloadAndClassify(sys.argv[1], int(sys.argv[2]))
  else:
    DownloadAndClassify(sys.argv[1], 0)

