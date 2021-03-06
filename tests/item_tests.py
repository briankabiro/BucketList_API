import json
from tests import TestBase


class TestItems(TestBase):

    def test_item_is_created(self):
        # test to check item is created
        self.create_bucket(self.token)
        rv = self.create_item(self.token)
        self.assertIn('sleep', str(rv.data))

    def test_item_is_updated(self):
        """ test to check item is updated """
        self.create_bucket(self.token)
        self.create_item(self.token)

        rv = self.client.put(
            '/bucketlists/1/items/1',
            headers=self.headers,
            data=self.item1)
        self.assertIn(
            "updated successfully",
            rv.data.decode())
        self.assertEqual(rv.status_code, 200)

    def test_item_is_deleted(self):
        # test to check that an item is deleted from bucketlist
        self.create_bucket(self.token)
        self.create_item(self.token)

        self.client.delete(
            '/bucketlists/1/items/1',
            headers=self.headers)

        response = self.client.get(
            '/bucketlists/1', headers=self.headers)
        data = json.loads(response.data)

        self.assertEqual(len(data['items']), 0)

    def test_search_functionality_on_items(self):
        # test to check search items
        self.create_bucket(self.token)
        self.create_item(self.token)
        response = self.client.get(
            '/bucketlists/1/items/?q=sleep',
            headers=self.headers)
        data = json.loads(response.data)
        self.assertIn('sleep', str(data))

    def test_pagination_when_getting_items(self):
        # test to check pagination when getting items
        self.create_bucket(self.token)
        for i in range(1, 12):
            self.create_item(self.token)

        response = self.client.get(
            '/bucketlists/1/items/?limit=5',
            headers=self.headers)

        data = json.loads(response.data)
        self.assertEqual(len(data), 5)

    def test_pagination_with_multiple_pages(self):
        self.create_bucket(self.token)
        for i in range(1, 6):
            self.create_item(self.token)

        response = self.client.get(
            '/bucketlists/1/items/?limit=3&page=2',
            headers=self.headers)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)

    def test_when_limit_is_not_integer(self):
        self.create_bucket(self.token)
        self.create_item(self.token)

        response = self.client.get(
            '/bucketlists/1/items/?limit=a',
            headers=self.headers)
        self.assertEqual(response.status_code, 400)

    def test_when_page_is_not_integer(self):
        self.create_bucket(self.token)
        self.create_item(self.token)

        response = self.client.get(
            '/bucketlists/1/items/?limit=1&page=a',
            headers=self.headers)
        self.assertEqual(response.status_code, 400)

    def test_done_is_either_true_or_false(self):
        self.create_bucket(self.token)
        self.create_item(self.token)
        rv = self.client.put(
            '/bucketlists/1/items/1',
            headers=self.headers,
            data={"done": "t"})

        self.assertEqual(rv.status_code, 400)

    def test_either_done_or_description_is_required(self):
        self.create_bucket(self.token)
        self.create_item(self.token)
        rv = self.client.put(
            '/bucketlists/1/items/1',
            headers=self.headers)

        self.assertEqual(rv.status_code, 400)

    def test_it_validates_bucketlist_id_when_updating(self):
        self.create_bucket(self.token)
        self.create_item(self.token)
        rv = self.client.put(
            '/bucketlists/2/items/1',
            headers=self.headers,
            data=self.item)
        self.assertEqual(rv.status_code, 404)

    def test_it_validates_item_id_when_updating(self):
        self.create_bucket(self.token)
        self.create_item(self.token)
        rv = self.client.put(
            '/bucketlists/1/items/2',
            headers=self.headers,
            data=self.item)
        self.assertEqual(rv.status_code, 404)

