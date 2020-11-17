"""
Description
"""


from ..lidartools.lidartools import *


class Plant:
    """

    Args:
        species: scientific name
        name: common german name
        nativ: equals 1 if the plant is nativ, 0 if its not
        habitat: habit name of the plant
        endangered: information about the endangerment status of the plant
        waterdepthmin: minimal required water depth
        waterdepthmax: maximum depth to groundwater
        rootdepth: average root depth
        groundwatertablechange: maximum change in groundwater table that the plant can survive
        floodheightmax: maximum flood height the plant can survive
        floodloss: losses during maximum height and days that occured in plant population
        flooddurationmax: maximum day of flooding the plant can survive
    """

    def __init__(self, species, name, nativ, habitat, endangered, waterdepthmin, waterdepthmax, rootdepth, groundwatertablechange, floodheightmax, floodloss, flooddurationmax):

        self.species = species
        self.name_german = name
        self.status = nativ
        self.is_endangered = endangered
        self.habitat_in_germany = habitat
        self.minimum_waterdepth = waterdepthmin
        self.maximum_waterdepth = waterdepthmax
        self.average_root_depth = rootdepth
        self.change_of_groundwatertable = groundwatertablechange
        self.critical_flood_height = floodheightmax
        self.plant_mortality_during_critial_flooding = floodloss
        self.critical_flood_duration = flooddurationmax

    def print_habitat(self):
        """
        prints the plant parameters as string in console

        Returns:
            String in console
        """
        print('\nscientific name:\n{0}\ncommon german name:\n{1}\nstatus:\n{2}\nendangered?:\n{3}'.format(self.species,
                                                                                        str(self.name_german),
                                                                                        str(self.status),
                                                                                        str(self.habitat_in_germany),
                                                                                        str(self.is_endangered),
                                                                                        str(self.minimum_waterdepth),
                                                                                        str(self.maximum_waterdepth),
                                                                                        str(self.average_root_depth),
                                                                                        str(self.change_of_groundwatertable),
                                                                                        str(self.critical_flood_height),
                                                                                        str(self.plant_mortality_during_critial_flooding),
                                                                                        str(self.critical_flood_duration)))




