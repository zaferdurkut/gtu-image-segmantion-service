from src.gdal import Gdal, Utils
from utils.utils import *
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
import numpy as np
import matplotlib.pylab as plt
import json
from scipy import ndimage



@timerfunc
def kmean_clustering(gdal_object, im_dir_path, clusters, metric):
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
    img = gdal_object.im2array()
    for band_number, band in bands.items():
        print("\n Band Number: {band_number}".format(band_number=band_number))
        band_path = create_path(im_dir_path,str(band_number)); create_directory(band_path)
        img = Utils.im2array_out(band)
        array = img.reshape((-1, 1))

        meandist_json = {}
        meandist=[]
        local_varience_json = {}
        local_varience = []
        for number_of_clusters  in clusters:
            print("\tNumber of Cluster: {number_of_clusters}".format(
                number_of_clusters = number_of_clusters
            ))
            # Model Training
            model = kmean_model_train(number_of_clusters, array)
            # kmeans_distance
            meandist_value = calculate_kmeans_distance(array,model,metric)
            meandist.append(meandist_value)
            meandist_json[number_of_clusters] = meandist_value
            # local_variance
            local_varience_value = calculate_local_varience(model, array)        
            local_varience.append(local_varience_value)
            local_varience_json[number_of_clusters] = local_varience_value
        
        kmeans_distance_graph_data_export(clusters, band_path, meandist, meandist_json)
        local_variance_graph_data_export(clusters, band_path, local_varience, local_varience_json)

    print("\n\t-----------------------------------------------------------------------------\n")
    return True



@timerfunc
def calculate_local_varience(model, array):
    values = model.cluster_centers_
    labels = model.labels_
    value = ndimage.variance(array,labels)
    # print(ndimage.standard_deviation(values))
    return value

@timerfunc
def calculate_kmeans_distance(array,model,metric):
    value = sum( 
        np.min( 
            cdist(array, model.cluster_centers_, metric), axis=1)) / array.shape[0]
    return value

@timerfunc
def kmean_model_train(number_of_clusters, array):
    model = KMeans(n_clusters=number_of_clusters)
    model.fit(array)
    return model

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
def kmeans_distance(clusters, array, metric, out_dir):
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
def local_variance_graph_data_export(clusters, out_dir, meandist, meandist_json):
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
    print("\n")
    algorithm_path = create_path(out_dir,'Local_Variance'); create_directory(algorithm_path)
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


    plt.plot(clusters, meandist)
    plt.xlabel('Number of clusters')
    plt.ylabel('Varience')
    plt.title('Selecting k with the Local Varience') 
    plt.savefig(create_path(graphs_path,'varience.png'))
    plt.clf()

    plt.plot(clusters, diffrences)
    plt.xlabel('Number of clusters')
    plt.ylabel('Diffrences')
    plt.title('Selecting k with the Local Varience') 
    plt.savefig(create_path(graphs_path,'diffrences.png'))
    plt.clf()


    with open(values_path+'/data.json', 'w') as outfile:
        json.dump(meandist_json, outfile)

    with open(values_path+'/diffrences.json', 'w') as outfile:
        json.dump(diffrences_json, outfile)

    return True

@timerfunc
def local_variance(clusters, array, metric, out_dir):
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
    algorithm_path = create_path(out_dir,'Local_Variance'); create_directory(algorithm_path)
    values_path = create_path(algorithm_path,'values'); create_directory(values_path)
    graphs_path = create_path(algorithm_path,'graphs'); create_directory(graphs_path)

    meandist_json = {}
    meandist=[]
    for number_of_clusters  in clusters:
        model=KMeans(n_clusters=number_of_clusters) # 
        model.fit(array)
        X_clustered = model.labels_
        X_clustered = X_clustered.reshape(array.shape)
        label = ndimage.label(X_clustered)
        value = ndimage.variance(model, label)
        # value = ndimage.variance(array)
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
    plt.ylabel('Varience')
    plt.title('Selecting k with the Local Varience') 
    plt.savefig(create_path(graphs_path,'varience.png'))
    plt.clf()

    plt.plot(clusters, diffrences)
    plt.xlabel('Number of clusters')
    plt.ylabel('Diffrences')
    plt.title('Selecting k with the Local Varience') 
    plt.savefig(create_path(graphs_path,'diffrences.png'))
    plt.clf()


    with open(values_path+'/data.json', 'w') as outfile:
        json.dump(meandist_json, outfile)

    with open(values_path+'/diffrences.json', 'w') as outfile:
        json.dump(diffrences_json, outfile)

    return True

@timerfunc
def kmeans_cluster2raster_example(img, array, outfile_name, driver,n_clusters, gdal_object):
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
