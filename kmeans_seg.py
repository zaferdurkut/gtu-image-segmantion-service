from src.kmeans import *
from utils.utils import *


#-------------------- Parameters ---------------------------------#

data = "data/clipped_2.tif"
clusters=range(1,100,10)

#---------------------   Out Path  Operations ---------------------------------#

im_basename, im_dirname = get_basename_dirname(data)
im_dir_path = create_path(im_dirname,im_basename)
create_directory(im_dir_path)


#--------------------  Gdal Operations-------------------------------#

gdal_object = Gdal(data)
gdal_object.open()
# band = gdal_object.get_band(1)
# img = gdal_object.im2array()
# array = img.reshape((-1, 1))

#----------------------------------------------------------#




if __name__ == "__main__":
    kmean_clustering(gdal_object, im_dir_path,clusters,'euclidean')


    # kemans_distance(clusters,array, 'euclidean',im_dir_path)
    # kmeans_cluster2raster_example(img,array,"data/out.tif","GTiff",3, gdal_object)

