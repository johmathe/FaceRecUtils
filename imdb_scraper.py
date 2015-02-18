import bs4
import joblib
import logging
import os
import urllib
import urllib2

G_IMDB_SITE = 'http://www.imdb.com'
G_IMDB_LIST = 'http://www.imdb.com/list/ls076754881/'
# Number of threads to kick off
G_N_JOBS = 10
G_OUTPUT_DIR = '/home/johmathe/dataset/imdb_artists'
logging.basicConfig(level=logging.INFO, filename='imdb_scraper.log')


def GetPicFromImdbPage(page_url):
  """Get pic from Imdb artist page."""
  img_url = ''
  try:
      webpage = urllib2.urlopen(page_url)
      soup = bs4.BeautifulSoup(webpage.read().decode('utf8'))
  except:
      logging.error("Error getting %s" % page_url)
      raise
  for anchor in soup.find_all(id='primary-img'):
    img_url = anchor.get('src')

  for anchor in soup.find_all(title='Next image (right arrow)'):
    next_link = anchor.get('href')
  return (img_url, next_link)


def GetAllImages(starting_link, artist_name):
  next_link = ''
  starting_link = starting_link.split('?')[0]
  current_link = starting_link
  cnt = 0
  dirname = '%s/%s' % (G_OUTPUT_DIR, artist_name.strip(' ,.').lower().replace(' ', '_'))
  os.mkdir(dirname)
  while starting_link not in next_link:
    imdb_page = '%s/%s' % (G_IMDB_SITE, current_link)
    img_url, next_link = GetPicFromImdbPage(imdb_page)
    next_link = next_link.split('?')[0]
    current_link = next_link
    path = "%s/%d.jpg" % (dirname,cnt)
    logging.info('copying %s to %s' % (img_url, path))
    if img_url:
      urllib.urlretrieve(img_url, path)
      cnt += 1


def GetNamesFromList(list_url):
  """Return a list of artist tuples for a given IMDB top N list.

  Args:
    list_url: imdb url list of top N stuff

  Returns:
    [(artist, artist_id), ...]

  """
  try:
      webpage = urllib2.urlopen(list_url)
      soup = bs4.BeautifulSoup(webpage.read().decode('utf8'))
  except:
      logging.error("Error getting %s" % list_url)
      raise
  artist_name = ''
  artists = []
  for anchor in soup.find_all('div'):
    link = anchor.get('data-const')
    if link:
      artist_name = anchor.contents[1].get('alt')[9:]
      artists.append( (artist_name, link) )
  return artists


def GetFirstPhotoLink(artist_id):
  url = '%s/name/%s' % (G_IMDB_SITE, artist_id)
  try:
      webpage = urllib2.urlopen(url)
      soup = bs4.BeautifulSoup(webpage.read().decode('utf8'))
  except:
      logging.error("Error getting %s" % url)
      raise
  artist_name = ''
  artists = []
  for anchor in soup.find_all('a'):
    href = anchor.get('href')
    if artist_id in href and '/rm' in href:
      return href


def StripSiteName(url):
  return '/'.join(url.split('/')[3:])


def DownloadArtistImages(artist_name, artist_id):
  """Download imdb data for a given artist.

  Args:
    artist_name: string, the name of the artist
    artist_id: string, the id of the artist (e.g nm0388382)
  """
  try:
    logging.info('fetching images for %s ' % artist_name)
    first_link = GetFirstPhotoLink(artist_id)
    uri = StripSiteName(first_link)
    GetAllImages(first_link, artist_name)
  except:
    logging.error('Issue with artist %s' % artist_name)

if __name__ == '__main__':
  """Main entry point."""
  artist_list = GetNamesFromList(G_IMDB_LIST)
  logging.info('fetching data for: %s' % artist_list)
  joblib.Parallel(n_jobs=G_N_JOBS)(
      joblib.delayed(DownloadArtistImages)(*i) for i in artist_list)
