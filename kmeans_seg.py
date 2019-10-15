from src.gdal import Gdal, Utils
import gdal
from sklearn import cluster


gdal_object = Gdal("data/clipped_2.tif")
gdal_object.open()
band = gdal_object.get_band(1)
img = gdal_object.im2array()
prj = gdal_object.get_prj()
X = img.reshape((-1, 1))

k_means = cluster.KMeans(n_clusters=4)
k_means.fit(X)
X_clustered = k_means.labels_
X_clustered = X_clustered.reshape(img.shape)

gdal_object.write_one_array(driver="GTiff",outfile_name="data/out.tif",X_clustered=X_clustered,prj=prj)
print(prj)
