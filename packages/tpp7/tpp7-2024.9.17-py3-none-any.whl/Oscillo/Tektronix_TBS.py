from .Tektronix import Tektronix
import uuid, os
import numpy as np
import time
from matplotlib import pyplot as plt

class TBS(Tektronix):
    __version__ = 'TBS-1.0.3'

    modelDict = {
        "1064": (0x0699, 0x03b3), # Je ne sais pas d'où il vient !
        "1104": (0x0699, 0x03b4),  # C'est un modèle qui vient des projets de physique expérimentale
        "1052B-EDU": {0x0699, 0x0368}, # C'est une modèle qui vient de ISUPFERE
    }

    def __init__(self, device = None, ident = (None, None), model= None):
        if model is None:
            super().__init__(device, ident)
            return
        if model in self.modelDict:
            ident = ident = self.modelDict[model]
            super().__init__(device, ident)
            if model == "1052B-EDU":
                self.image_format = 'JPEG'
                self.image_extension = 'jpg'
                self.instr.max_transfer_size = 50
            if model == "1104":
                self.image_format = 'BMP'
                self.image_extension = 'bmp'
                #self.instr.max_transfer_size = 50
            return

        print('Liste des modèles de '+self.__class__.__name__+' référencés')
        print(self.modelDict)
        raise NameError("le modèle {} n'est pour le moment pas référencé".format(model))
