"""
Description
"""

import os, sys
sys.path.insert(0, os.path.abspath("."))
from import_mgmt import *


def read_raster(raster):
    with rio.open(raster) as src:
        raster_np = src.read(1, masked=True)
        nodatavalue = src.nodata  # storing nodatavalue of raster
        meta = src.meta.copy()
        print('Number of active cells (non-masked) of raster ', raster, ': ', np.ma.count(raster_np))
    return raster_np, nodatavalue, meta, meta['crs'], meta['dtype']


def jaccard(a, b):
    """Creates a ...

    Args:
        a (float):
        b (float):

    Returns:
        ``float``: ``jac``
    """
    jac = 1 - (a * b) / (2 * abs(a) + 2 * abs(b) - a * b)
    return jac


def f_similarity(centrall_cell, neighbours):
    """ Calculates the similarity function for each pair of values (fuzzy numerical method)

    :param centrall_cell: float, cell under analysis in map A
    :param neighbours: np.array of floats, neighbours in map B
    :return: np.array of floats, each similarity between each of two cells
    """
    simil_neigh = np.zeros(np.shape(neighbours))
    for index, entry in np.ndenumerate(neighbours):
        simil_neigh[index] = 1 - (abs(entry - centrall_cell)) / max(abs(entry), abs(centrall_cell))
    return simil_neigh


def squared_error(centrall_cell, neighbours):
    """ Calculates the error measure fuzzy rmse

    :param centrall_cell: float, cell under analysis in map A
    :param neighbours: np.array of floats, neighbours in map B
    :return: np.array of floats, each similarity between each of two cells
    """

    simil_neigh = (neighbours - centrall_cell) ** 2
    return simil_neigh


class FuzzyComparison:
    """ Performing fuzzy map comparison
                :param rasterA: string, path of the raster to be compared with rasterB
                :param rasterB: string, path of the raster to be compared with rasterA
                :param neigh: integer, neighborhood being considered (number of cells from the central cell), default is 4
                :param halving_distance: integer, distance (in cells) to which the membership decays to its half, default is 2
    """

    def __init__(self, rasterA, rasterB, neigh=4, halving_distance=2):
        self.raster_A = rasterA
        self.raster_B = rasterB
        self.neigh = neigh
        self.halving_distance = halving_distance
        self.array_A, self.nodatavalue, self.meta_A, self.src_A, self.dtype_A = read_raster(self.raster_A)
        self.array_B, self.nodatavalue_B, self.meta_B, self.src_B, self.dtype_B = read_raster(self.raster_B)

        if halving_distance <= 0:
            print('Halving distance must be at least 1')
        if self.nodatavalue != self.nodatavalue_B:
            print('Warning: Maps have different NoDataValues, I will use the NoDataValue of the first map')
        if self.src_A != self.src_B:
            sys.exit('MapError: Maps have different coordinate system')
        if self.dtype_A != self.dtype_B:
            print('Warning: Maps have different data types, I will use the datatype of the first map')

    def neighbours(self, array, x, y):
        """ Captures the neighbours and their memberships
        :param array: array A or B
        :param x: int, cell in x
        :param y: int, cell in y
        :return: np.array (float) membership of the neighbours (without mask), np.array (float) neighbours' cells (without mask)
        """

        x_up = max(x - self.neigh, 0)
        x_lower = min(x + self.neigh + 1, array.shape[0])
        y_up = max(y - self.neigh, 0)
        y_lower = min(y + self.neigh + 1, array.shape[1])

        # Masked array that contains only neighbours
        neigh_array = array[x_up: x_lower, y_up: y_lower]
        neigh_array = np.ma.masked_where(neigh_array == self.nodatavalue, neigh_array)

        # Distance (in cells) of all neighbours to the cell in x,y in analysis
        i, j = np.indices(neigh_array.shape)
        i = i.flatten() - (x - x_up)
        j = j.flatten() - (y - y_up)
        d = np.reshape((i ** 2 + j ** 2) ** 0.5, neigh_array.shape)

        # Calculate the membership based on the distance decay function
        memb = 2 ** (-d / self.halving_distance)

        # Mask the array of memberships
        memb_ma = np.ma.masked_array(memb, mask=neigh_array.mask)

        return memb_ma[~memb_ma.mask], neigh_array[~neigh_array.mask]

    def fuzzy_numerical(self, comparison_name, save_dir, map_of_comparison=True):
        """ Compares a pair of raster maps using fuzzy numerical spatial comparison

        :param save_dir: string, directory where to save the results
        :param comparison_name: string, name of the comparison
        :param map_of_comparison: boolean, create map of comparison in the project directory if True
        :return: Global Fuzzy Similarity and comparison map
        """

        print('Performing fuzzy numerical comparison...')
        # Two-way similarity, first A x B then B x A
        s_AB = np.full(np.shape(self.array_A), self.nodatavalue, dtype=self.dtype_A)
        s_BA = np.full(np.shape(self.array_A), self.nodatavalue, dtype=self.dtype_A)

        #  Loop to calculate similarity A x B
        for index, central in np.ndenumerate(self.array_A):
            if not self.array_A.mask[index]:
                memb, neighboursA = self.neighbours(self.array_B, index[0], index[1])
                f_i = np.ma.multiply(f_similarity(self.array_A[index], neighboursA), memb)
                if f_i.size != 0:
                    s_AB[index] = np.nanmax(f_i)  # takes max without propagating nan

        #  Loop to calculate similarity B x A
        for index, central in np.ndenumerate(self.array_B):
            if not self.array_B.mask[index]:
                memb, neighboursB = self.neighbours(self.array_A, index[0], index[1])
                f_i = np.ma.multiply(f_similarity(self.array_B[index], neighboursB), memb)
                if f_i.size != 0:
                    s_BA[index] = np.nanmax(f_i)  # takes max without propagating nan

        S_i = np.minimum(s_AB, s_BA)

        # Mask cells where there's no similarity measure
        S_i_ma = np.ma.masked_where(S_i == self.nodatavalue, S_i, copy=True)

        # Overall similarity
        S = S_i_ma.mean()

        # Save results
        self.save_results(S, save_dir, comparison_name)

        # Fill nodatavalues into array
        S_i_ma_fi = np.ma.filled(S_i_ma, fill_value=self.nodatavalue)

        # Saves comparison raster
        if map_of_comparison:
            self.save_comparison_raster(S_i_ma_fi, save_dir, comparison_name)

        return S

    def fuzzy_rmse(self, comparison_name, save_dir, map_of_comparison=True):
        """ Compares a pair of raster maps using fuzzy root mean square error as spatial comparison

        :param comparison_name: string, name of the comparison
        :param save_dir: string, directory where to save the results of the map comparison
        :param map_of_comparison: boolean, if True it creates map of of local squared errors (in the project directory)

        :return: global fuzzy RMSE and comparison map
        """

        print('Performing fuzzy RMSE comparison...')

        # Two-way similarity, first A x B then B x A
        s_AB = np.full(np.shape(self.array_A), self.nodatavalue, dtype=self.dtype_A)
        s_BA = np.full(np.shape(self.array_A), self.nodatavalue, dtype=self.dtype_A)

        #  Loop to calculate similarity A x B
        for index, central in np.ndenumerate(self.array_A):
            if not self.array_A.mask[index]:
                memb, neighboursA = self.neighbours(self.array_B, index[0], index[1])
                f_i = np.ma.divide(squared_error(self.array_A[index], neighboursA), memb)
                if f_i.size != 0:
                    s_AB[index] = np.amin(f_i)

        #  Loop to calculate similarity B x A
        for index, central in np.ndenumerate(self.array_B):
            if not self.array_B.mask[index]:
                memb, neighboursB = self.neighbours(self.array_A, index[0], index[1])
                f_i = np.ma.divide(squared_error(self.array_B[index], neighboursB), memb)
                if f_i.size != 0:
                    s_BA[index] = np.amin(f_i)

        S_i = np.maximum(s_AB, s_BA)

        # Mask cells where there's no similarity measure
        S_i_ma = np.ma.masked_where(S_i == self.nodatavalue, S_i, copy=True)

        # Overall similarity
        S = (S_i_ma.mean()) ** 0.5

        # Save results
        self.save_results(S, save_dir, comparison_name)

        # Fill nodatavalues into array
        S_i_ma_fi = np.ma.filled(S_i_ma, fill_value=self.nodatavalue)

        # Save comparison raster
        if map_of_comparison:
            self.save_comparison_raster(S_i_ma_fi, save_dir, comparison_name)

        return S

    def save_results(self, measure, dir, name):
        """Saves a results file"""
        if '.' not in name[-4:]:
            name += '.txt'
        result_file = dir + '/' + name
        lines = ["Fuzzy numerical spatial comparison \n", "\n", "Compared maps: \n",
                 str(self.raster_A) + "\n", str(self.raster_B) + "\n", "\n", "Halving distance: " +
                 str(self.halving_distance) + " cells  \n", "Neighbourhood: " + str(self.neigh) + " cells  \n", "\n"]
        file1 = open(result_file, "w")
        file1.writelines(lines)
        file1.write('Average fuzzy similarity: ' + str(format(measure, '.4f')))
        file1.close()

    def save_comparison_raster(self, array_local_measures, dir, file_name):
        """Create map of comparison"""
        if '.' not in file_name[-4:]:
            file_name += '.tif'
        comp_map = dir + "/" + file_name
        raster = rio.open(comp_map, 'w', **self.meta_A)
        raster.write(array_local_measures, 1)
        raster.close()
