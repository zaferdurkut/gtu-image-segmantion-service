from src.kmeans import *
from utils.utils import *
import argparse
import sys

parser = argparse.ArgumentParser(description='Process Kmeans Clustering Parameters')
parser.add_argument('--data',
                       metavar='data',
                       type=str,
                       help='the path to list')
parser.add_argument('--start',
                       metavar='start',
                       default=2,
                       type=int,
                       help='the path to list')
parser.add_argument('--end',
                       metavar='end',
                       default=10,
                       type=int,
                       help='the path to list')
parser.add_argument('--step',
                       metavar='step',
                       default=2,
                       type=int,
                       help='the path to list')

parser.add_argument('--metric',
                       metavar='metric',
                       default='euclidean',
                       type=str,
                       help='https://docs.scipy.org/doc/scipy-0.15.1/reference/generated/scipy.spatial.distance.cdist.html')
                       

args = parser.parse_args()

if args.data is None:
    print('The path specified does not exist')
    sys.exit()

#-------------------- Parameters ---------------------------------#

data = args.data
clusters=range(args.start,args.end,args.step)

#---------------------   Out Path  Operations ---------------------------------#

im_basename, im_dirname = get_basename_dirname(data)
im_dir_path = create_path(im_dirname,im_basename)
create_directory(im_dir_path)


#--------------------  Gdal Operations-------------------------------#

gdal_object = Gdal(data)
gdal_object.open()





if __name__ == "__main__":
    kmean_clustering(gdal_object, im_dir_path,clusters,args.metric)
    
    # kmeans_distance(clusters,array, 'euclidean',im_dir_path)
    # kmeans_cluster2raster_example(img,array,"data/out.tif","GTiff",3, gdal_object)

