"""Learning notMnist dataset."""

from __future__ import print_function
import imageio
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import tarfile
from IPython.display import display, Image
from sklearn.linear_model import LogisticRegression
from six.moves.urllib.request import urlretrieve
from six.moves import cPickle as pickle
from logzero import logger

num_classes = 10
np.random.seed(133)

url = 'https://commondatastorage.googleapis.com/books1000/'
last_percent_reported = None
data_root = os.getcwd()


def download_progress_hook(count, block_size, total_size):
    """Display progress bar."""
    global last_percent_reported
    percent = int(count * block_size * 100 / total_size)
    if last_percent_reported != percent:
        if percent % 5 == 0:
            sys.stdout.write("%s%%" % percent)
            sys.stdout.flush()
        else:
            sys.stdout.write(".")
            sys.stdout.flush()
        last_percent_reported = percent


def maybe_download(filename, expected_bytes, force=False):
    """Download a file if not present anc check size."""
    dest_filename = os.path.join(data_root, filename)
    if force or not os.path.exists(dest_filename):
        logger.info('Attempting to download: ', filename)
        filename, _ = urlretrieve(url + filename, dest_filename, reporthook=download_progress_hook)
        logger.info('Download Complete!')
    statinfo = os.stat(dest_filename)
    if statinfo.st_size == expected_bytes:
        print('Found and verified', dest_filename)
    else:
        raise Exception('Failed to verify' + dest_filename + '. Can you get it with a browser?')
