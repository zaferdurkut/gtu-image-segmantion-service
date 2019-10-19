from src.gdal import Gdal, Utils
import gdal
from utils.utils import *
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import json


@timerfunc
def kemans_distance(clusters, array, metric, out_dir):
    """""
    
    Arguments:
        clusters {list} -- baslangic ve bitis arasinda belli step ile olsuturulmus number_of_clusters sayisi
        array {array} -- goruntuden elde edilmis array
        outfile_name {png} -- cikacak grafik pathi
        metric {text} -- https://docs.scipy.org/doc/scipy-0.15.1/reference/generated/scipy.spatial.distance.cdist.html
        out_dir {path} -- verilerin cikacagi path
    Returns:
        [type] -- [description]
    """
    algorithm_path = create_path(out_dir,'Elbow_Method'); create_directory(algorithm_path)
    values_path = create_path(algorithm_path,'values'); create_directory(values_path)
    graphs_path = create_path(algorithm_path,'graphs'); create_directory(graphs_path)

    meandist_json = {}
    meandist=[]
    for number_of_clusters  in clusters:
        model=KMeans(n_clusters=number_of_clusters) # 
        model.fit(array)
        value = sum( 
            np.min( 
                cdist(array, model.cluster_centers_, metric), axis=1)) / array.shape[0]
        meandist.append(value)
        meandist_json[number_of_clusters] = value

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



    plt.plot(clusters, meandist)
    plt.xlabel('Number of clusters')
    plt.ylabel('Average distance')
    plt.title('Selecting k with the Elbow Method') 
    plt.savefig(create_path(graphs_path,'euclidean.png'))
    plt.clf()

    plt.plot(clusters, diffrences)
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
def kmeans_cluster2raster_example(img, array, outfile_name, driver,n_clusters):
    """""
    Bu method verilen bir band icin kmeans clustirng yapilarak 
    ilgili clustirng sonucunu ayni extent icin tif olarak kayit
    edilmesini amaclayarak hazirlanmistir.
    
    Arguments:
        img {[gdal object]} -- [ham goruntunun gdal ile acilmis hali]
        array {[type]} -- [goruntuden arraye donusturulmus array]
        outfile_name {[type]} -- [cikti dizini]
        driver {[type]} -- [cikcak goruntu formati]
    
    Raises:
        e: errors
    
    Returns:
        [Boolean] -- [Status is True]
    """

    try:
        k_means = KMeans(n_clusters=n_clusters)
        k_means.fit(array)
        X_clustered = k_means.labels_
        X_clustered = X_clustered.reshape(img.shape)
        gdal_object.array2raster(driver=driver, outfile_name=outfile_name, X_clustered=X_clustered)
        return True
    except Exception as e:
        raise e