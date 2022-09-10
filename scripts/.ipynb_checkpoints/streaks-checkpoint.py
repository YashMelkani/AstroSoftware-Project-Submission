from astropy.io import fits
from astropy import time 
from ztfquery import query
import matplotlib.pyplot as plt
import numpy as np
import os


def display_fit(path, **kwargs):
    img = get_img(path)
    plt.imshow(img, **kwargs)
    plt.show()    

def get_img(path):
    try:
        hdul = fits.open(path)
        img = hdul[0].data
        hdul.close()
        return img
    except:
        print(f"Could not open file at {path}")
        
def find_streak(path, percentile_thresh = 0.05):
    
    img = get_img(path)
    percentile_val = np.percentile(img,percentile_thresh*100)
    
    #check for verticle streaks
    vmeans = np.mean(img, axis = 0)
    vidxs = np.where(vmeans<percentile_val)
    print(vmeans[434], percentile_val)
    
    #check for horizontal streaks
    hmeans = np.mean(img, axis = 1)
    hidxs = np.where(hmeans<percentile_val)
    
    return hidxs, vidxs

def download_ZTF(ra, dec, tstart, tend, metatable_path = None,  kind = "sci", kind_type = "sciimg.fits"):
    zquery = query.ZTFQuery()
    zquery.load_metadata(kind=kind, radec=[ra,dec], size=0.01, sql_query=f"obsjd BETWEEN {tstart} AND {tend}")
    zquery.download_data(kind_type, nprocess=1, show_progress=True)
    metatable = zquery.metatable
    if metatable_path is not None:
        zquery.metatable.to_csv(metatable_path)
    return metatable

def get_ZTF_path(ra, dec, tstart, tend, kind = "sci", kind_type = "sciimg.fits"):
    zquery = query.ZTFQuery()
    zquery.load_metadata(kind=kind, radec=[ra,dec], size=0.01, sql_query=f"obsjd BETWEEN {tstart} AND {tend}")
    return zquery.get_data(kind_type, show_progress=False)

