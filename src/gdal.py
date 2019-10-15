from osgeo import gdal, osr

class Gdal():

    def __init__(self, filename):
        self.filename = filename

    def open(self):
        """""

        Returns:
            dataset {gdal_object} -- acilan goruntuyu dondurur.
        """

        self.dataset = gdal.Open(self.filename)

        return self.dataset

    def get_bands(self):
        """""
        
        Returns:
            band_list {dict}-- goruntuden gelen band'lari dict list olarak dondurur.
        """

        if self.dataset:
            band_list = {}
            for index in range(1, self.dataset.RasterCount):
                self.band = self.dataset.GetRasterBand(index)
                band_list[index] = self.band
            
        return band_list
    
    def get_band(self, band_number = 1):
        """""
        
        Keyword Arguments:
            band_number {int} -- donrulmek istenen band numarasidir. (default: {1})
        
        Returns:
            [type] -- [description]
        """

        self.band = self.dataset.GetRasterBand(band_number)

        return self.band

    def im2array(self):
        """""
        
        Arguments:
            band {img} -- array'e donusturulmek istenen goruntu
                            band gdal objesi olmali
        
        Returns:
            array -- goruntuden array'e
        """
        self.array = self.band.ReadAsArray()
        return self.array

    def get_prj(self):
        """""
        
        Returns:
            prj {prj} -- projeksiyon sistemini dondurur.
        """
        self.prj = self.dataset.GetProjection()

        return self.prj

    def write_one_array(self,
                        driver="GTiff",
                        outfile_name="data/out.tif",
                        *,
                        eType=gdal.GDT_Float32,
                        X_clustered,
                        prj):
        """""[summary]
        
        Keyword Arguments:
            driver {str} -- [veri formati] (default: {"GTiff"})
            outfile_name {str} -- [cikti goruntu path'i] (default: {"data/out.tif"})
            eType {[type]} -- [cografi veri tipi] (default: {gdal.GDT_Float32})
            X_clustered {array} -- cluster edilen array 
        """
        self.driver = gdal.GetDriverByName(driver)
        self.x_size = self.array.shape[1]
        self.y_size = self.array.shape[0]
        out_dataset = self.driver.Create(outfile_name, self.x_size, self.y_size, eType=eType)
        out_dataset.SetProjection(prj)
        out_dataset.GetRasterBand(1).WriteArray(X_clustered)
        return out_dataset

    def array2raster(self,
                    driver="GTiff",
                    outfile_name="data/out.tif",
                    eType=gdal.GDT_Float32,
                    *,
                    X_clustered):
        """""[summary]
        
        Keyword Arguments:
            driver {str} -- [veri formati] (default: {"GTiff"})
            outfile_name {str} -- [cikti goruntu path'i] (default: {"data/out.tif"})
            eType {[type]} -- [cografi veri tipi] (default: {gdal.GDT_Float32})
            X_clustered {array} -- cluster edilen array 
        """
        raster = self.dataset
        geotransform = raster.GetGeoTransform()
        originX = geotransform[0]
        originY = geotransform[3]
        pixelWidth = geotransform[1]
        pixelHeight = geotransform[5]
        cols = raster.RasterXSize
        rows = raster.RasterYSize

        driver = gdal.GetDriverByName(driver)
        outRaster = driver.Create(outfile_name, cols, rows, 1, eType)
        outRaster.SetGeoTransform((originX, pixelWidth, 0, originY, 0, pixelHeight))
        outband = outRaster.GetRasterBand(1)
        outband.WriteArray(X_clustered)
        outRasterSRS = osr.SpatialReference()
        outRasterSRS.ImportFromWkt(raster.GetProjectionRef())
        outRaster.SetProjection(outRasterSRS.ExportToWkt())
        outband.FlushCache()
        return True
class Utils():

    @staticmethod
    def im2array_out(band):
        """""
        
        Arguments:
            band {img} -- array'e donusturulmek istenen goruntu
                            band gdal objesi olmali
        
        Returns:
            array -- goruntuden array'e
        """
        return band.ReadAsArray()

