from abc import ABC
from http import HTTPStatus
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse


class CommonTest(ABC, TestCase):
    path_name: str = None
    template_name: str = None
    title: str = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._es_update_patcher = patch("django_elasticsearch_dsl.registries.registry.update")
        cls._es_delete_patcher = patch("django_elasticsearch_dsl.registries.registry.delete")
        cls._es_update_patcher.start()
        cls._es_delete_patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls._es_update_patcher.stop()
        cls._es_delete_patcher.stop()
        super().tearDownClass()

    def setUp(self) -> None:
        self.path = reverse(self.path_name) if self.path_name else None

    def common_test(self):
        if self.path is not None:
            response = self.client.get(self.path)
            self.assertEqual(response.status_code, HTTPStatus.FOUND)
