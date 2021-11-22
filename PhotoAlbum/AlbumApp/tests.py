from django.test import TestCase,SimpleTestCase
from django.urls import reverse,resolve
from AlbumApp.views import gallery,photo,add,download_file

# Create your tests here.

class TestUrls(SimpleTestCase):
    
    def test_gallery_url_is_resolved(self):
        url = reverse('gallery')
        print(resolve(url))
        self.assertEquals(resolve(url).func, gallery)

    def test_photo_url_is_resolved(self):
        url = reverse('photo', args=['1'])
        print(resolve(url))
        self.assertEquals(resolve(url).func,photo)

    def test_add_url_is_resolved(self):
        url = reverse('add')
        print(resolve(url))
        self.assertEquals(resolve(url).func,add)

    def test_download_url_is_resolved(self):
        url = reverse('download',args=['1'])
        print(resolve(url))
        self.assertEquals(resolve(url).func,download_file) 





