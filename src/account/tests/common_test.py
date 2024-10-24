from abc import ABC
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class CommonTest(ABC, TestCase):
    path_name: str = None
    template_name: str = None
    title: str = None

    def setUp(self) -> None:
        self.path = reverse(self.path_name) if self.path_name else None

    def common_test(self):
        if self.path is not None:
            response = self.client.get(self.path)
            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertTemplateUsed(response, self.template_name)
            self.assertEqual(response.context_data["title"], self.title)
