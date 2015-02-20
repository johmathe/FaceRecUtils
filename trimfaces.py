import glob
import joblib
import logging
import os
import subprocess
import sys

# Paths to binaries
G_CONVERT = 'convert'
G_DETECT = '/home/johmathe/ccv/bin/scddetect'
# Path to face model
G_FACEMODEL = '/home/johmathe/ccv/samples/face.sqlite3'
# Input and output directories
G_PATH_DATASET = '/home/johmathe/dataset/imdb_artists_women/'
G_DESTINATION = '/home/johmathe/dataset/trimmed_women'
# Number of tasks to run at the same time
G_N_THREADS = 16

logging.basicConfig(level=logging.INFO, filename='face_trimmer.log')

def Chunks(l, n):
    """Chunk data into equal subsets."""
    n = max(1, n)
    return [l[i:i + n] for i in range(0, len(l), n)]


def DetectFaces(img_path):
  """Detect faces in an image, return corresponding geometries."""
  binary_args = [G_DETECT, img_path, G_FACEMODEL]
  p = subprocess.Popen(
    binary_args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  output, err = p.communicate()
  geometries = []
  # Parse result from scddetect
  output = output.split('\n')  
  output = output[:-2]
  for l in output:
    params = [int(x) for x in l.split(' ')[:-1]]
    geometries.append(params)
  return geometries


def CropImage(img_input, img_output, geometry):
  """Crop input to output given geometry."""
  geometry_str = '%dx%d+%d+%d' % (geometry[2], geometry[3], geometry[0], geometry[1])
  subprocess.call([G_CONVERT, img_input, '-crop', geometry_str, img_output])


def TrimFacesFromPic(img_path, img_output_prefix):
  """Given an image, find out faces, crops and write to outputs"""
  geometries = DetectFaces(img_path)
  for i, g in enumerate(geometries):
    CropImage(img_path, '%s_%d.jpg' % (img_output_prefix, i), g) 
    

def FaceCropSetOfPics(pics_list):
  """Apply cropping to a set of pictures."""
  for pic in pics_list:
    # foo/var/baz/1.jpg -> 1
    img_id = pic.split('/')[-1].split('.')[0]
    artist = pic.split('/')[-2]
    logging.info('Processing artist %s - image id %s' % (artist, img_id))
    destination_dir = '%s/%s' % (G_DESTINATION, artist)
    if not os.path.exists(destination_dir):
       os.makedirs(destination_dir)
    TrimFacesFromPic(pic, '%s/%s' % (destination_dir, img_id))


if __name__ == '__main__':
  """Main entry point."""
  pics = glob.glob('%s/*/*.jpg' % G_PATH_DATASET)
  pics_subsets = Chunks(pics, G_N_THREADS)
  joblib.Parallel(n_jobs=G_N_THREADS)(
      joblib.delayed(FaceCropSetOfPics)(pic_list) for pic_list in pics_subsets)
