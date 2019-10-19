from src.gdal import Gdal, Utils
import gdal
from utils.utils import timerfunc
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
import pandas as pd
import numpy as np
import matplotlib.pylab as plt

data = "data/clipped_2.tif"
n_clusters=3
clusters=range(1,10,2)


@timerfunc
def cluster2raster(img, array, outfile_name, driver):
    try:
        k_means = KMeans(n_clusters=n_clusters)
        k_means.fit(array)
        X_clustered = k_means.labels_
        X_clustered = X_clustered.reshape(img.shape)
        gdal_object.array2raster(driver=driver, outfile_name=outfile_name, X_clustered=X_clustered)
        return True
    except Exception as e:
        raise e


@timerfunc
def kemans_distance(clusters,array):

    meandist=[]
    for k in clusters:
        model=KMeans(n_clusters=k)
        model.fit(array)
        clusassign=model.predict(array)
        meandist.append(sum(np.min(cdist(array, model.cluster_centers_, 'euclidean'), axis=1))
    / array.shape[0])

    plt.plot(clusters, meandist)
    plt.xlabel('Number of clusters')
    plt.ylabel('Average distance')
    plt.title('Selecting k with the Elbow Method') # pick the fewest number of clusters that reduces the average distance
    plt.savefig('data/euclidean.png')
    
    return True

gdal_object = Gdal(data)
gdal_object.open()
band = gdal_object.get_band(1)
img = gdal_object.im2array()
array = img.reshape((-1, 1))


# kemans_distance(clusters,array)

cluster2raster(img,array,"data/out.tif","GTiff")
