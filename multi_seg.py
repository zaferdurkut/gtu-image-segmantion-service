from src.multi import *
from utils.utils import *
import argparse
import sys

parser = argparse.ArgumentParser(
    description='Process Kmeans Clustering Parameters')
parser.add_argument('--data',
                    metavar='data',
                    type=str,
                    help='the path to list')

parser.add_argument('--task',
                    metavar='task',
                    choices=['Optimum_Parameter',
                             'Multi_Segmentation',
                             'Multi_Segmentation_With_Optimum_Parameter'
                             ],
                    type=str,
                    help="""
                            Optimum_Parameter
                            Multi_Segmentation
                            Multi_Segmentation_With_Optimum_Parameter
                            """)

parser.add_argument('--start',
                    metavar='start',
                    default=2,
                    type=int,
                    help='start of k value')

parser.add_argument('--end',
                    metavar='end',
                    default=10,
                    type=int,
                    help='end of k value')

parser.add_argument('--step',
                    metavar='step',
                    default=2,
                    type=int,
                    help='step of k value')

parser.add_argument(
    '--metric',
    metavar='metric',
    default='euclidean',
    type=str,
    help='https://docs.scipy.org/doc/scipy-0.15.1/reference/generated/scipy.spatial.distance.cdist.html')

parser.add_argument('--k_value',
                    metavar='k_value',
                    default=4,
                    type=int,
                    help='optimum k value')

parser.add_argument('--export_vector_layer',
                    metavar='export_vector_layer',
                    choices=['Yes',
                             'No'
                             ],
                    type=str,
                    help='export_vector_layer')


args = parser.parse_args()

if args.data is None:
    print('The path specified does not exist')
    sys.exit()

#-------------------- Parameters ---------------------------------#

data = args.data
if args.task == "Optimum_Parameter" or args.task == "Multi_Segmentation_With_Optimum_Parameter":
    clusters = range(args.start, args.end, args.step)

#---------------------   Out Path  Operations ---------------------------------#

im_basename, im_dirname = get_basename_dirname(data)
im_dir_path = create_path(im_dirname, im_basename)
create_directory(im_dir_path)
segmentation_image_path = "{im_dirname}/{basename}_segmentationman.tif".format(
    basename=im_basename,
    im_dirname=im_dirname
)


#--------------------  Gdal Operations-------------------------------#

gdal_object = Gdal(data)
gdal_object.open()


if __name__ == "__main__":
    if args.task == "Optimum_Parameter":
        optimal_labels = kmean_clustering_optimal_value_search(gdal_object,
                                                               im_dir_path,
                                                               clusters,
                                                               args.metric)

    if args.task == "Multi_Segmentation_With_Optimum_Parameter":
        kmean_clustering_optimal_value_search_and_segmentation(
            gdal_object, im_dir_path, clusters, args.metric, segmentation_image_path, "GTiff")
    if args.task == "Multi_Segmentation":
        multi_band_kmeans_segmentation(args.k_value,
                                       segmentation_image_path,
                                       "GTiff",
                                       gdal_object)

    if args.export_vector_layer == "Yes":
        export_vector_layer_path = "{im_dirname}/{basename}_segmentationman_temp.shp".format(
            basename=im_basename, im_dirname=im_dirname)
        export_vector_layer(segmentation_image_path, export_vector_layer_path)


# TODO: üretilen label değerlerine karşılık gelen pixcel değerlenin pixellerindeki istatistikleri nasıl hesaplanacak
# TODO: vektörize edilen label verisinin doğruğu nasıl ölçülcek ve
# polygonize doğru bir yöntem mi?
