from src.gdal import Gdal, Utils
from utils.utils import *
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
import numpy as np
import matplotlib.pylab as plt
import json
from scipy import ndimage
from sklearn.metrics import silhouette_score
from skimage.color import label2rgb
from PIL import Image
import subprocess
import os




@timerfunc
def kmean_clustering_optimal_value_search(gdal_object, im_dir_path, clusters, metric):
    """""
    Gdal ile acilan goruntu icin het bir band'ina kmeans algoritmasinin
    uygulanmasi ve algoritmalara göre segment verilerinin raporlanmasi islemin
    yapar.
    
    Arguments:
        gdal_object {gdal object} -- [gdal ile acilmis goruntu]
        im_dir_path {path} -- [rapor verilerinin yazilacagi dizin]
        clusters {list} -- [hangi aralikta tarama yapacaginin listesi]
        metric {[type]} -- [oklit uzakligi hesaplamasinda hesaplama yontemi]
    """

    bands = gdal_object.get_bands()
    raster_info = gdal_object.get_raster_info()
    multi_array = np.zeros((raster_info["row"]*raster_info["col"],raster_info["band"]))
    rgb_array = np.zeros((raster_info["row"],raster_info["col"],raster_info["band"]))
    for band_number, band in bands.items():
        array = Utils.im2array_out(band)
        multi_array[:,band_number-1] = array.reshape((raster_info["row"]*raster_info["col"], 1)).T
        rgb_array[:,:,band_number-1] = array


    meandist_json = {}
    meandist=[]
    silhouette_score_json = {}
    silhouette_score = []
    for number_of_clusters  in clusters:
        # TODO: Multi Processing eklenecek

        print("\tNumber of Cluster: {number_of_clusters}".format(
            number_of_clusters = number_of_clusters
        ))
        # # Model Training
        model = kmean_model_train(number_of_clusters, multi_array)
        # # kmeans_distance
        # meandist_value = calculate_kmeans_inertia(model)
        meandist_value = calculate_kmeans_distance(multi_array,model,metric)
        meandist.append(meandist_value)
        meandist_json[number_of_clusters] = meandist_value

        # silhouette score
        # silhouette_score_value = calculate_silhouette_score(model, multi_array,metric)        
        # silhouette_score.append(silhouette_score_value)
        # silhouette_score_json[number_of_clusters] = silhouette_score_value
    
    kmeans_distance_graph_data_export(clusters, im_dir_path, meandist, meandist_json)
    # silhouette_score_graph_data_export(clusters, im_dir_path, silhouette_score, silhouette_score_json)

    # optimal_segment = max(silhouette_score_json,key=silhouette_score_json.get)
    # print(optimal_segment)
    # optimal_segment = optimal_segment



    print("\n\t-----------------------------------------------------------------------------\n")
    return True


@timerfunc
def kmean_clustering_optimal_value_search_and_segmentation(gdal_object, im_dir_path, clusters, metric, outfile_name,driver):
    """""
    Gdal ile acilan goruntu icin het bir band'ina kmeans algoritmasinin
    uygulanmasi ve algoritmalara göre segment verilerinin raporlanmasi islemin
    yapar.
    
    Arguments:
        gdal_object {gdal object} -- [gdal ile acilmis goruntu]
        im_dir_path {path} -- [rapor verilerinin yazilacagi dizin]
        clusters {list} -- [hangi aralikta tarama yapacaginin listesi]
        metric {[type]} -- [oklit uzakligi hesaplamasinda hesaplama yontemi]
    """

    bands = gdal_object.get_bands()
    raster_info = gdal_object.get_raster_info()
    multi_array = np.zeros((raster_info["row"]*raster_info["col"],raster_info["band"]))
    rgb_array = np.zeros((raster_info["row"],raster_info["col"],raster_info["band"]))
    for band_number, band in bands.items():
        array = Utils.im2array_out(band)
        multi_array[:,band_number-1] = array.reshape((raster_info["row"]*raster_info["col"], 1)).T
        rgb_array[:,:,band_number-1] = array


    meandist_json = {}
    meandist=[]
    silhouette_score_json = {}
    silhouette_score = []
    for number_of_clusters  in clusters:
        # TODO: Multi Processing eklenecek
        print("\tNumber of Cluster: {number_of_clusters}".format(
            number_of_clusters = number_of_clusters
        ))
        # # Model Training
        model = kmean_model_train(number_of_clusters, multi_array)
        # # kmeans_distance
        # # meandist_value = calculate_kmeans_inertia(model)
        # meandist_value = calculate_kmeans_distance(array,model,metric)
        # meandist.append(meandist_value)
        # meandist_json[number_of_clusters] = meandist_value

        # silhouette score
        silhouette_score_value = calculate_silhouette_score(model, multi_array,metric)        
        silhouette_score.append(silhouette_score_value)
        silhouette_score_json[number_of_clusters] = silhouette_score_value
    
    # kmeans_distance_graph_data_export(clusters, im_dir_path, meandist, meandist_json)
    silhouette_score_graph_data_export(clusters, im_dir_path, silhouette_score, silhouette_score_json)
    # TODO: optimal değer hesabı daha yapılamıyor

    optimal_segment = max(silhouette_score_json,key=silhouette_score_json.get)
    optimal_model = kmean_model_train(optimal_segment, multi_array)
    labels = optimal_model.labels_.reshape((raster_info["row"],raster_info["col"]))

    try:
        gdal_object.array2raster(driver=driver, outfile_name=outfile_name, X_clustered=labels)
        return True
    except Exception as e:
        raise e


    print("\n\t-----------------------------------------------------------------------------\n")
    return labels


@timerfunc
def calculate_silhouette_score(model, array, metric):
    labels = model.labels_
    value = silhouette_score(array, labels, metric = metric)
    return value

@timerfunc
def calculate_kmeans_inertia(model):
    # value = sum( 
    #     np.min( 
    #         cdist(array, model.cluster_centers_, metric), axis=1)) / array.shape[0]
    value = model.inertia_
    return value

@timerfunc
def calculate_kmeans_distance(array,model,metric):
    value = cdist(array, model.cluster_centers_, metric)
    return value


@timerfunc
def kmean_model_train(number_of_clusters, array):
    # TODO: Aşağıdaki parametreler dışarıdan alacak şekilde yapıalcak
    model = KMeans(
                    n_clusters=number_of_clusters,
                    tol=1e-8,
                    max_iter=10000,
                    )
    model.fit(array)
    return model

@timerfunc
def silhouette_score_graph_data_export(clusters, out_dir, meandist, meandist_json ):
    """""
    
    Arguments:
        clusters {list} -- baslangic ve bitis arasinda belli step ile olsuturulmus number_of_clusters sayisi
        array {array} -- goruntuden elde edilmis array
        outfile_name {png} -- cikacak grafik pathi
        metric {text} -- https://docs.scipy.org/doc/scipy-0.15.1/reference/generated/scipy.spatial.distance.cdist.html
        out_dir {path} -- verilerin cikacagi pathcre
    Returns:
        [type] -- [description]
    """
    print("\n")
    algorithm_path = create_path(out_dir,'Silhouette_Score'); create_directory(algorithm_path)
    values_path = create_path(algorithm_path,'values'); create_directory(values_path)
    graphs_path = create_path(algorithm_path,'graphs'); create_directory(graphs_path)


    diffrences_json = {}
    diffrences = []
    for index in range(0,len(meandist)-1):
        value = meandist[index+1] - meandist[index] 
        diffrences.append(value)
        diffrences_json[
                        str(clusters[index])+
                        "_"+
                        str(clusters[index+1])] = value
    diffrences.append(value)



    plt.plot(clusters, meandist,'r-o')
    plt.xlabel('Number of clusters')
    plt.ylabel('Silhouette Score')
    plt.title('Selecting k with the Silhouette Score') 
    plt.savefig(create_path(graphs_path,'silhouette_score.png'))
    plt.clf()

    plt.plot(clusters, diffrences,'r-o')
    plt.xlabel('Number of clusters')
    plt.ylabel('Diffrences')
    plt.title('Selecting k with the Silhouette Score') 
    plt.savefig(create_path(graphs_path,'diffrences.png'))
    plt.clf()


    with open(values_path+'/data.json', 'w') as outfile:
        json.dump(meandist_json, outfile)

    with open(values_path+'/diffrences.json', 'w') as outfile:
        json.dump(diffrences_json, outfile)

    return True


@timerfunc
def kmeans_distance_graph_data_export(clusters, out_dir, meandist, meandist_json ):
    """""
    
    Arguments:
        clusters {list} -- baslangic ve bitis arasinda belli step ile olsuturulmus number_of_clusters sayisi
        array {array} -- goruntuden elde edilmis array
        outfile_name {png} -- cikacak grafik pathi
        metric {text} -- https://docs.scipy.org/doc/scipy-0.15.1/reference/generated/scipy.spatial.distance.cdist.html
        out_dir {path} -- verilerin cikacagi pathcre
    Returns:
        [type] -- [description]
    """
    print("\n")
    algorithm_path = create_path(out_dir,'Elbow_Method'); create_directory(algorithm_path)
    values_path = create_path(algorithm_path,'values'); create_directory(values_path)
    graphs_path = create_path(algorithm_path,'graphs'); create_directory(graphs_path)


    diffrences_json = {}
    diffrences = []
    for index in range(0,len(meandist)-1):
        value = meandist[index+1] - meandist[index] 
        diffrences.append(value)
        diffrences_json[
                        str(clusters[index])+
                        "_"+
                        str(clusters[index+1])] = value
    diffrences.append(value)



    plt.plot(clusters, meandist,'r-o')
    plt.xlabel('Number of clusters')
    plt.ylabel('Average distance')
    plt.title('Selecting k with the Elbow Method') 
    plt.savefig(create_path(graphs_path,'euclidean.png'))
    plt.clf()

    plt.plot(clusters, diffrences,'r-o')
    plt.xlabel('Number of clusters')
    plt.ylabel('Diffrences')
    plt.title('Selecting k with the Elbow Method') 
    plt.savefig(create_path(graphs_path,'diffrences.png'))
    plt.clf()


    with open(values_path+'/data.json', 'w') as outfile:
        json.dump(meandist_json, outfile)

    with open(values_path+'/diffrences.json', 'w') as outfile:
        json.dump(diffrences_json, outfile)

    return True


@timerfunc
def multi_band_kmeans_segmentation(optimal_segment, outfile_name, driver, gdal_object):
    """""
    Bu method verilen bütün bandlar icin kmeans clustirng yapilarak 
    ilgili clustirng sonucunu ayni extent icin tif olarak kayit
    edilmesini amaclayarak hazirlanmistir.
    
    Arguments:
        optimal_segment {[int]} -- cluster sayısı
        gdal_object {gdal object} -- gdal ile çalışmış görüntü
        outfile_name {[type]} -- [cikti dizini]
        driver {[type]} -- [cikcak goruntu formati]
    
    Raises:
        e: errors
    
    Returns:
        [Boolean] -- [Status is True]
    """
    bands = gdal_object.get_bands()
    raster_info = gdal_object.get_raster_info()
    multi_array = np.zeros((raster_info["row"]*raster_info["col"],raster_info["band"]))
    rgb_array = np.zeros((raster_info["row"],raster_info["col"],raster_info["band"]))

    for band_number, band in bands.items():
        array = Utils.im2array_out(band)
        multi_array[:,band_number-1] = array.reshape((raster_info["row"]*raster_info["col"], 1)).T
        rgb_array[:,:,band_number-1] = array

    optimal_model = kmean_model_train(optimal_segment, multi_array)
    labels = optimal_model.labels_.reshape((raster_info["row"],raster_info["col"]))

    try:
        gdal_object.array2raster(driver=driver, outfile_name=outfile_name, X_clustered=labels)
        return True
    except Exception as e:
        raise e


@timerfunc
def export_vector_layer(tif_path, shp_path):

    subprocess.call(['gdal_polygonize.py {tif_path}  -f "ESRI Shapefile" {shp_path}'.format(
                                                                                                tif_path=tif_path,
                                                                                                shp_path=shp_path
                                                                                            )], shell=True)



    subprocess.call(['ogr2ogr {out} {input} -sql "SELECT *, OGR_GEOM_AREA AS area FROM {table}"'.format(
                                                                                                            table=os.path.basename(shp_path)[:-4],
                                                                                                            out=shp_path[:-9]+'.shp',
                                                                                                            input=shp_path
                                                                                                        )],shell=True)
    subprocess.call(['rm -rf {files}*'.format(
                                                files=shp_path[:-3]
                                            )],shell=True)