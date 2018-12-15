# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class JobParamsJobs(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, data_file: str=None, spark_program: str=None):  # noqa: E501
        """JobParamsJobs - a model defined in Swagger

        :param data_file: The data_file of this JobParamsJobs.  # noqa: E501
        :type data_file: str
        :param spark_program: The spark_program of this JobParamsJobs.  # noqa: E501
        :type spark_program: str
        """
        self.swagger_types = {
            'data_file': str,
            'spark_program': str
        }

        self.attribute_map = {
            'data_file': 'dataFile',
            'spark_program': 'sparkProgram'
        }

        self._data_file = data_file
        self._spark_program = spark_program

    @classmethod
    def from_dict(cls, dikt) -> 'JobParamsJobs':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The JobParams_jobs of this JobParamsJobs.  # noqa: E501
        :rtype: JobParamsJobs
        """
        return util.deserialize_model(dikt, cls)

    @property
    def data_file(self) -> str:
        """Gets the data_file of this JobParamsJobs.


        :return: The data_file of this JobParamsJobs.
        :rtype: str
        """
        return self._data_file

    @data_file.setter
    def data_file(self, data_file: str):
        """Sets the data_file of this JobParamsJobs.


        :param data_file: The data_file of this JobParamsJobs.
        :type data_file: str
        """

        self._data_file = data_file

    @property
    def spark_program(self) -> str:
        """Gets the spark_program of this JobParamsJobs.


        :return: The spark_program of this JobParamsJobs.
        :rtype: str
        """
        return self._spark_program

    @spark_program.setter
    def spark_program(self, spark_program: str):
        """Sets the spark_program of this JobParamsJobs.


        :param spark_program: The spark_program of this JobParamsJobs.
        :type spark_program: str
        """

        self._spark_program = spark_program
