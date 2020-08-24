import json

from django.test import TestCase, RequestFactory

from papermerge.core.views.decorators import (
    smart_dump,
    json_response
)


class TestDecorators(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_smart_dump(self):
        ret = json.dumps({'msg': "OK"})

        self.assertEqual(
            smart_dump("OK"),
            ret
        )

        self.assertEqual(
            smart_dump({'msg': "OK"}),
            ret
        )

    def test_json_response_1(self):
        ret = json.dumps({'msg': "OK"})

        def view_ok(request):
            return "OK"

        view = json_response(view_ok)
        request = self.factory.get('/blah')
        ret = view(request)

        self.assertEqual(
            ret.status_code,
            200
        )

        self.assertEqual(
            json.loads(ret.content),
            {'msg': "OK"}
        )

    def test_json_response_2(self):
        def view_ok(request):
            return {"key1": "value1", "key2": "value2"}

        view = json_response(view_ok)
        request = self.factory.get('/blah')
        ret = view(request)

        self.assertEqual(
            ret.status_code,
            200
        )

        self.assertEqual(
            json.loads(ret.content),
            {"key1": "value1", "key2": "value2"}
        )

    def test_json_response_3(self):
        def view_bad_request(request):
            return "There was an error", 400

        view = json_response(view_bad_request)
        request = self.factory.get('/blah')
        ret = view(request)

        self.assertEqual(
            ret.status_code,
            400
        )

        self.assertEqual(
            json.loads(ret.content),
            {'msg': "There was an error"}
        )

    def test_json_response_4(self):
        def view_bad_request(request):
            return {"key1": "value1"}, 400

        view = json_response(view_bad_request)
        request = self.factory.get('/blah')
        ret = view(request)

        self.assertEqual(
            ret.status_code,
            400
        )

        self.assertEqual(
            json.loads(ret.content),
            {"key1": "value1"}
        )
