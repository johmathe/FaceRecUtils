import numpy as np
import matplotlib.pyplot as plt
#%matplotlib inline
ARTISTS = {0: 'denzel_washington', 1: 'jack_nicholson', 2: 'adrien_brody', 3: 'javier_bardem', 4: 'benicio_del_toro', 5: 'eddie_murphy', 6: 'dustin_hoffman', 7: 'sean_penn', 8: 'steve_carell', 9: 'ryan_gosling', 10: 'christian_bale', 11: 'ryan_reynolds', 12: 'jackie_chan', 13: 'tom_hanks', 14: 'dev_patel', 15: 'ken_jeong', 16: 'gary_oldman', 17: 'liam_neeson', 18: 'leonardo_dicaprio', 19: 'ashton_kutcher', 20: 'matt_damon', 21: 'keanu_reeves', 22: 'johnny_depp', 23: 'colin_firth', 24: 'forest_whitaker', 25: 'morgan_freeman', 26: 'jet_li', 27: 'john_malkovich', 28: 'jeff_bridges', 29: 'bruce_willis', 30: 'edward_norton', 31: 'justin_timberlake', 32: 'brad_pitt', 33: 'joaquin_phoenix', 34: 'matthew_mcconaughey', 35: 'anthony_hopkins', 36: 'bradley_cooper', 37: 'clint_eastwood', 38: 'george_clooney', 39: 'joseph_gordon-levitt', 40: 'benedict_cumberbatch', 41: 'al_pacino', 42: 'jean_dujardin', 43: 'daniel_day-lewis', 44: 'harrison_ford', 45: 'robert_downey_jr', 46: 'will_smith', 47: 'bill_murray', 48: 'nicolas_cage', 49: 'christoph_waltz', 50: 'kevin_spacey', 51: 'zac_efron', 52: 'tom_cruise', 53: 'robert_de_niro', 54: 'jim_carrey', 55: 'jude_law', 56: 'hugh_jackman', 57: 'robert_pattinson', 58: 'jamie_foxx', 59: 'robin_williams', 60: 'ben_affleck', 61: 'samuel_l._jackson', 62: 'heath_ledger', 63: 'taylor_lautner', 64: 'channing_tatum'}
# Make sure that caffe is on the python path:
caffe_root = 'caffe/'  # this file is expected to be in {caffe_root}/examples
import sys
sys.path.insert(0, caffe_root + 'python')

MEAN_FILE = '/home/johmathe/starface/dataset/starface_mean'
MEAN_OUTPUT = '/home/johmathe/starface/dataset/starface_mean.npy'

import glob
import caffe

# Set the right path to your model definition file, pretrained model weights,
# and the image you would like to classify.
MODEL_FILE = 'FaceRecUtils/deploy_google.prototxt'
PRETRAINED = 'FaceRecUtils/caffe_google_train_iter_40000.caffemodel'
IMAGE_FILE = '/home/johmathe/dataset/test_data/data/jt2_1.jpg'

caffe.set_mode_cpu()
net = caffe.Classifier(MODEL_FILE, PRETRAINED,
                       mean=np.load(MEAN_OUTPUT),
                       channel_swap=(2,1,0),
                       raw_scale=255,
                       image_dims=(256, 256))


print net

input_image = caffe.io.load_image(IMAGE_FILE)
#plt.imshow(input_image)

prediction = net.predict([input_image])  # predict takes any number of images, and formats them for the Caffe net automatically
print 'prediction shape:', prediction[0].shape

print prediction[0]
s = sorted(prediction[0])
print 'predicted class:', prediction[0].argmax()
print 'artist : %s' % ARTISTS[prediction[0].argmax()] 
