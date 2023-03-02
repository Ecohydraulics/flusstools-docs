"""
Head structure for fuzzy map comparisons

Usage: ``fuzzy_comparison = FuzzyComparison()``

Descriptions will be updated by Bea
"""

from .plotter import *



def f_similarity(centre_cell, neighbours):
    """ Calculates the similarity function for each pair of values (fuzzy numerical method)

    :param centre_cell: float, cell under analysis in map A
    :param neighbours: np.array of floats, neighbours in map B
    :return: np.array of floats, each similarity between each of two cells
    """
    simil_neigh = np.zeros(np.shape(neighbours))
    for index, entry in np.ndenumerate(neighbours):
        simil_neigh[index] = 1 - (abs(entry - centre_cell)) / \
                                  max(abs(entry), abs(centre_cell))
    return simil_neigh


def squared_error(centre_cell, neighbours):
    """ Calculates the error measure fuzzy rmse

    :param centre_cell: float, cell under analysis in map A
    :param neighbours: np.array of floats, neighbours in map B
    :return: np.array of floats, each similarity between each of two cells
    """

    simil_neigh = (neighbours - centre_cell) ** 2
    return simil_neigh


class FuzzyComparison:
    """ Performing fuzzy map comparison
                :param raster_a: string, path of the raster to be compared with rasterB
                :param raster_b: string, path of the raster to be compared with rasterA
                :param neigh: integer, neighborhood being considered (number of cells from the central cell), default is 4
                :param halving_distance: integer, distance (in cells) to which the membership decays to its half, default is 2
    """

    def __init__(self, raster_a, raster_b, neigh=4, halving_distance=2):
        self.raster_a = raster_a
        self.raster_b = raster_b
        self.neigh = neigh
        self.halving_distance = halving_distance
        self.array_a, self.nodatavalue_a, self.meta_a, self.src_a, self.dtype_a = read_raster(
            self.raster_a)
        self.array_b, self.nodatavalue_b, self.meta_b, self.src_b, self.dtype_b = read_raster(
            self.raster_b)

        if halving_distance <= 0:
            print('Halving distance must be at least 1')
        if self.nodatavalue_a != self.nodatavalue_b:
            print(
                'Warning: Maps have different NoDataValues, I will use the NoDataValue of the first map')
        if self.src_a != self.src_b:
            sys.exit('MapError: Maps have different coordinate system')
        if self.dtype_a != self.dtype_b:
            print(
                'Warning: Maps have different data types, I will use the datatype of the first map')

    def get_neighbours(self, array, x, y):
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
        neigh_array = np.ma.masked_where(
            neigh_array == self.nodatavalue_a, neigh_array)

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
        s_ab = np.full(np.shape(self.array_a),
                       self.nodatavalue_a, dtype=self.dtype_a)
        s_ba = np.full(np.shape(self.array_a),
                       self.nodatavalue_a, dtype=self.dtype_a)

        #  Loop to calculate similarity A x B
        for index, central in np.ndenumerate(self.array_a):
            if not self.array_a.mask[index]:
                memb, neighbours_a = self.get_neighbours(
                    self.array_b, index[0], index[1])
                f_i = np.ma.multiply(f_similarity(
                    self.array_a[index], neighbours_a), memb)
                if f_i.size != 0:
                    # takes max without propagating nan
                    s_ab[index] = np.nanmax(f_i)

        #  Loop to calculate similarity B x A
        for index, central in np.ndenumerate(self.array_b):
            if not self.array_b.mask[index]:
                memb, neighbours_b = self.get_neighbours(
                    self.array_a, index[0], index[1])
                f_i = np.ma.multiply(f_similarity(
                    self.array_b[index], neighbours_b), memb)
                if f_i.size != 0:
                    # takes max without propagating nan
                    s_ba[index] = np.nanmax(f_i)

        S_i = np.minimum(s_ab, s_ba)

        # Mask cells where there's no similarity measure
        S_i_ma = np.ma.masked_where(S_i == self.nodatavalue_a, S_i, copy=True)

        # Overall similarity
        S = S_i_ma.mean()

        # Save results
        self.save_results(S, save_dir, comparison_name)

        # Fill nodatavalues into array
        S_i_ma_fi = np.ma.filled(S_i_ma, fill_value=self.nodatavalue_a)

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
        s_ab = np.full(np.shape(self.array_a),
                       self.nodatavalue_a, dtype=self.dtype_a)
        s_ba = np.full(np.shape(self.array_a),
                       self.nodatavalue_a, dtype=self.dtype_a)

        #  Loop to calculate similarity A x B
        for index, central in np.ndenumerate(self.array_a):
            if not self.array_a.mask[index]:
                memb, neighbours_a = self.get_neighbours(
                    self.array_b, index[0], index[1])
                f_i = np.ma.divide(squared_error(
                    self.array_a[index], neighbours_a), memb)
                if f_i.size != 0:
                    s_ab[index] = np.amin(f_i)

        #  Loop to calculate similarity B x A
        for index, central in np.ndenumerate(self.array_b):
            if not self.array_b.mask[index]:
                memb, neighbours_b = self.get_neighbours(
                    self.array_a, index[0], index[1])
                f_i = np.ma.divide(squared_error(
                    self.array_b[index], neighbours_b), memb)
                if f_i.size != 0:
                    s_ba[index] = np.amin(f_i)

        S_i = np.maximum(s_ab, s_ba)

        # Mask cells where there's no similarity measure
        S_i_ma = np.ma.masked_where(S_i == self.nodatavalue_a, S_i, copy=True)

        # Overall similarity
        S = (S_i_ma.mean()) ** 0.5

        # Save results
        self.save_results(S, save_dir, comparison_name)

        # Fill nodatavalues into array
        S_i_ma_fi = np.ma.filled(S_i_ma, fill_value=self.nodatavalue_a)

        # Save comparison raster
        if map_of_comparison:
            self.save_comparison_raster(S_i_ma_fi, save_dir, comparison_name)

        return S

    def save_results(self, measure, directory, name):
        """Saves a results file"""
        if '.' not in name[-4:]:
            name += '.txt'
        result_file = directory + '/' + name
        lines = ["Fuzzy numerical spatial comparison \n", "\n", "Compared maps: \n",
                 str(self.raster_a) + "\n", str(self.raster_b)
                 + "\n", "\n", "Halving distance: "
                 + str(self.halving_distance) + " cells  \n", "Neighbourhood: " + str(self.neigh) + " cells  \n", "\n"]
        file1 = open(result_file, "w")
        file1.writelines(lines)
        file1.write('Average fuzzy similarity: ' + str(format(measure, '.4f')))
        file1.close()

    def save_comparison_raster(self, array_local_measures, directory, file_name):
        """Create map of comparison"""
        if '.' not in file_name[-4:]:
            file_name += '.tif'
        comp_map = directory + "/" + file_name
        raster = rio.open(comp_map, 'w', **self.meta_a)
        raster.write(array_local_measures, 1)
        raster.close()
