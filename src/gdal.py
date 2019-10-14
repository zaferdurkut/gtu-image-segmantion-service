from osgeo import gdal

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
        
        Returns:
            array -- goruntuden array'e
        """
        return self.band.ReadAsArray()

    @staticmethod
    def im2array_out(band):
        """""
        
        Arguments:
            band {img} -- array'e donusturulmek istenen goruntu
        
        Returns:
            array -- goruntuden array'e
        """
        return band.ReadAsArray()

