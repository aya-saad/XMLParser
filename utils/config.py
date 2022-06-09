# -*- coding: utf-8 -*-
"""
Created on Thu June 02 09:22:47 2022

@author: Aya Saad
"""

# import some common libraries
import configparser


class Config:
    def __init__(self, filename):
        self.config = configparser.ConfigParser()
        self.config.read(filename)

    def get_value(self, section, key):
        """
        get_value get the key value from the config.ini file
        :param section:
        :param key:
        :return: key value
        """
        if self.config.has_option(section, key):
            return self.config[section][key]
        else:
            return None
