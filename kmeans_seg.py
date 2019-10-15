from src.gdal import Gdal, Utils
import gdal
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
import pandas as pd
import numpy as np
import matplotlib.pylab as plt


gdal_object = Gdal("data/clipped_2.tif")
n_clusters = 2
clusters=range(1,50)



gdal_object.open()
band = gdal_object.get_band(1)
img = gdal_object.im2array()

X = img.reshape((-1, 1))
# k_means = KMeans(n_clusters=n_clusters)
# k_means.fit(X)
# X_clustered = k_means.labels_
# X_clustered = X_clustered.reshape(img.shape)

# gdal_object.array2raster(driver="GTiff",outfile_name="data/out.tif",X_clustered=X_clustered)


meandist=[]
for k in clusters:
    model=KMeans(n_clusters=k)
    model.fit(X)
    clusassign=model.predict(X)
    meandist.append(sum(np.min(cdist(X, model.cluster_centers_, 'euclidean'), axis=1))
/ X.shape[0])

plt.plot(clusters, meandist)
plt.xlabel('Number of clusters')
plt.ylabel('Average distance')
plt.title('Selecting k with the Elbow Method') # pick the fewest number of clusters that reduces the average distance
plt.savefig('data/euclidean.png')

