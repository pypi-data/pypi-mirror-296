from KKRtoVAMPIRE.utils import *
from os.path import exists
from os import mkdir
class Converter():
    """Class to convert a SPR-KKR input files to a .ucf file for VAMPIRE simulations.
    """
    def __init__(self, path, system_name, include_dmi=False, include_anisotropy=True, crop_thresholds=[0]):
        """Initializes the Converter object.

        Args:
            path (str): Path to the SPR-KKR input files.
            system_name (str): "seedname" - name of the system.
            include_dmi (bool, optional): Include DMI in the .ucf file. Defaults to False.
            include_anisotropy (bool, optional): Include anisotropy in the .ucf file. Defaults to True.
            crop_thresholds (list, optional): List of crop thresholds. Defaults to [0].
        """
        self.path = path
        self.system_name = system_name

    def convert(self, path_out, crop_thresholds=[0], include_dmi=False, include_anisotropy=True):
        if not exists(path_out): mkdir(path_out)
        sprkkr_to_vampire_ucf(path_in=self.path, path_out=path_out, system_name=self.system_name, crop_thresholds=crop_thresholds, \
                            include_dmi=include_dmi, include_anisotropy=include_anisotropy)
