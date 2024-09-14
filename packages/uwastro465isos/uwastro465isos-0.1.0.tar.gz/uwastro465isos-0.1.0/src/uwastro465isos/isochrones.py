import pandas
import numpy
import os

from .data import get_data_path

class Isochrone(object):
    filename = None

    def __init__(self, filename=None):
        if (filename is not None):
           self.filename = filename

        if (self.filename is not None and os.path.isfile(self.filename)):
            self.load_isochrone_file()
        else:
            raise(FileNotFoundError("No such file or directory: '%s'" % filename))
        
    def load_isochrone_file(self):
        self.iso = pandas.read_csv(self.filename, delim_whitespace=True, comment='#', )
        self.iso.loc[:, 'logAge'] = self.iso['logAge'].round(2)

    def select_isochrone(self, log_age, metallicity):
        selection = (self.iso['logAge'] == log_age) & (self.iso['MH'] == metallicity)
        sel_iso = self.iso[selection]
        # m_ini_sort = numpy.argsort(sel_iso['Mini'])
        return sel_iso.sort_values(by='Mini')
    
    def get_list_of_ages(self):
        ages = numpy.array(list(set(self.iso['logAge'])))
        return numpy.sort(ages)
    
    def get_list_of_metallicities(self):
        mh = numpy.array(list(set(self.iso['MH'])))
        return numpy.sort(mh)
    
    def get_list_of_magnitudes(self):
        cols = self.iso.columns
        good = [x for x in cols if x.endswith("mag")]
        return good
    


class Isochrone_Sloan( Isochrone ):
    filename = get_data_path("isochrones_ugriz.dat")

class Isochrone_Johnson( Isochrone ):
    filename = get_data_path("isochrones_ubvrijhk.dat")

