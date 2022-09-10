import lightkurve as lk
import numpy as np
import matplotlib.pyplot as plt


def download_lc(radec, path, mission = "TESS"):
    search_result = lk.search_lightcurve(radec, mission = mission)
    lcs = search_result.download_all(download_dir = path)
    return lcs

class LightCurveSimulator():
    def __init__(self,lc, error = 0.1):
        if issubclass(type(lc), (lk.lightcurve.KeplerLightCurve, lk.lightcurve.TessLightCurve)):
            self.lc = lc
        elif type(lc) == str:
            self.lc = lk.io.read(lc)
        self.newlc = self.lc.copy()
        self.error = error
        
    def add_error(self):
        l = len(self.newlc["flux"])
        self.newlc["flux"][np.random.randint(l)] += self.newlc["flux"].mean()*self.error
    
    def plot(self, title = "Original and Bumped Lightcurves", **kwargs):
        
        fig, axs = plt.subplots(2,1)
        self.lc.plot(ax=axs[0], **kwargs)
        axs[0].legend(loc = 'upper left')
        self.newlc.plot(ax=axs[1], **kwargs)
        label = f"Bumped {self.lc.meta['OBJECT']}"
        axs[1].legend(labels = [label], loc = 'upper left')
        plt.suptitle(title)

