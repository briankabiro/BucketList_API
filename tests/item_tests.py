from tests import TestBase
import json

class ItemTests(TestBase):

    def Test_item_is_created(self):
        # test to check item is created
        response = self.create_bucket(self.token)
        rv = self.create_item(self.token)
        data = json.loads(rv.data)
        self.assertIn('go to zanzibar', str(rv.data))

    def Test_item_is_updated(self):
        # test to check item is updated
        self.create_bucket(self.token)
        self.create_item(self.token)

        rv = self.client.put(
            '/bucketlists/1/items/1', headers=self.headers, data=self.item1)

        self.assertEqual(rv.status_code, 201)

    def Test_item_is_deleted(self):
        # test to check that an item is deleted from bucketlist
        self.create_bucket(self.token)
        self.create_item(self.token)

        self.client.delete('/bucketlists/1/items/1', headers=self.headers)

        response = self.client.get(
            '/bucketlists/1', headers=self.headers)
        data = json.loads(response.data)

        self.assertEqual(len(data['items']), 0)

    def Test_search_functionality_on_items(self):
        # test to check search items
        self.create_bucket(self.token)
        self.create_item(self.token)
        response = self.client.get(
            '/bucketlists/1/items/?q=go to zanzibar', headers=self.headers)
        data = json.loads(response.data)
        self.assertIn('go to zanzibar', str(data))

    def Test_pagination_when_getting_items(self):
        # test to check pagination when getting items
        self.create_bucket(self.token)
        for i in range(1, 12):
            self.create_item(self.token)

        response = self.client.get(
            '/bucketlists/1/items/?limit=5', headers=self.headers)

        data = json.loads(response.data)
        self.assertEqual(len(data), 5)
