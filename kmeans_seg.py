from src.gdal import Gdal
import gdal
from sklearn import cluster


gdal_object = Gdal("data/clipped_2.tif")
gdal_object.open()
band = gdal_object.get_band(1)
img = gdal_object.im2array_out(band)
X = img.reshape((-1, 1))

k_means = cluster.KMeans(n_clusters=12)
_ = k_means.fit(X)
X_clustered = k_means.labels_
X_clustered = X_clustered.reshape(img.shape)
driver = gdal.GetDriverByName('GTiff')
x_size = img.shape[1]
y_size = img.shape[0]
dataset = driver.Create("data/filename.tif", x_size, y_size, eType=gdal.GDT_Float32)
_ = dataset.GetRasterBand(1).WriteArray(X_clustered)
dataset.FlushCache()
print(img)
