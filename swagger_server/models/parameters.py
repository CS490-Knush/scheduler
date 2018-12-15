# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class Parameters(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, computation_nodes: List[str]=None, storage_nodes: List[str]=None):  # noqa: E501
        """Parameters - a model defined in Swagger

        :param computation_nodes: The computation_nodes of this Parameters.  # noqa: E501
        :type computation_nodes: List[str]
        :param storage_nodes: The storage_nodes of this Parameters.  # noqa: E501
        :type storage_nodes: List[str]
        """
        self.swagger_types = {
            'computation_nodes': List[str],
            'storage_nodes': List[str]
        }

        self.attribute_map = {
            'computation_nodes': 'computationNodes',
            'storage_nodes': 'storageNodes'
        }

        self._computation_nodes = computation_nodes
        self._storage_nodes = storage_nodes

    @classmethod
    def from_dict(cls, dikt) -> 'Parameters':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Parameters of this Parameters.  # noqa: E501
        :rtype: Parameters
        """
        return util.deserialize_model(dikt, cls)

    @property
    def computation_nodes(self) -> List[str]:
        """Gets the computation_nodes of this Parameters.


        :return: The computation_nodes of this Parameters.
        :rtype: List[str]
        """
        return self._computation_nodes

    @computation_nodes.setter
    def computation_nodes(self, computation_nodes: List[str]):
        """Sets the computation_nodes of this Parameters.


        :param computation_nodes: The computation_nodes of this Parameters.
        :type computation_nodes: List[str]
        """
        if computation_nodes is None:
            raise ValueError("Invalid value for `computation_nodes`, must not be `None`")  # noqa: E501

        self._computation_nodes = computation_nodes

    @property
    def storage_nodes(self) -> List[str]:
        """Gets the storage_nodes of this Parameters.


        :return: The storage_nodes of this Parameters.
        :rtype: List[str]
        """
        return self._storage_nodes

    @storage_nodes.setter
    def storage_nodes(self, storage_nodes: List[str]):
        """Sets the storage_nodes of this Parameters.


        :param storage_nodes: The storage_nodes of this Parameters.
        :type storage_nodes: List[str]
        """
        if storage_nodes is None:
            raise ValueError("Invalid value for `storage_nodes`, must not be `None`")  # noqa: E501

        self._storage_nodes = storage_nodes
