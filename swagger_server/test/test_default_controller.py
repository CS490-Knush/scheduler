# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.job_params import JobParams  # noqa: E501
from swagger_server.models.job_status import JobStatus  # noqa: E501
from swagger_server.models.parameters import Parameters  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_submit_config(self):
        """Test case for submit_config

        Submit storage and computation nodes to be optimized for cplex
        """
        body = Parameters()
        response = self.client.open(
            '/cpsc490/cplex_server/1.0.0/configure',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_submit_jobs(self):
        """Test case for submit_jobs

        Submit jobs to be run on configured server
        """
        body = JobParams()
        response = self.client.open(
            '/cpsc490/cplex_server/1.0.0/submitJobs',
            method='GET',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
