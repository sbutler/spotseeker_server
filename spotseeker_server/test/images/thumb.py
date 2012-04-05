from django.utils import unittest
from django.test.client import Client
from spotseeker_server.models import Spot
from cStringIO import StringIO
from PIL import Image

class ImageThumbTest(unittest.TestCase):
    def setUp(self):
        spot = Spot.objects.create( name = "This is to test thumbnailing images" )
        spot.save()
        self.spot = spot

        self.url = '/api/v1/spot/{0}/image'.format(self.spot.pk)
        self.url = self.url

    def test_jpeg_thumbs(self):
        c = Client()
        f = open('test/resources/test_jpeg.jpg')
        response = c.post(self.url, { "description": "This is a jpeg", "image": f })
        f.close()

        new_base_location = response["Location"]

        response = c.get("{0}/thumb/{1}x{2}".format(new_base_location, 100, 100))
        data = StringIO(response.content)
        im = Image.open(data)
        self.assertEquals(response["Content-type"], "image/jpeg", "Content type of same size thumbnail is jpeg")
        self.assertEquals(im.size[0], 100, "Width on same size jpeg thumbnail is 100")
        self.assertEquals(im.size[1], 100, "Height on same size jpeg thumbnail is 100")
        self.assertEquals(im.format, 'JPEG', "Actual type of same size thumbnail is still a jpeg")

        response = c.get("{0}/thumb/{1}x{2}".format(new_base_location, 1, 100))
        data = StringIO(response.content)
        im = Image.open(data)
        self.assertEquals(response["Content-type"], "image/jpeg", "Content type of narrow thumbnail is jpeg")
        self.assertEquals(im.size[0], 1, "Width on narrow jpeg thumbnail is 1")
        self.assertEquals(im.size[1], 100, "Height on narrow jpeg thumbnail is 100")
        self.assertEquals(im.format, 'JPEG', "Actual type of narrow thumbnail is still a jpeg")

        response = c.get("{0}/thumb/{1}x{2}".format(new_base_location, 100, 1))
        data = StringIO(response.content)
        im = Image.open(data)
        self.assertEquals(response["Content-type"], "image/jpeg", "Content type of short thumbnail is jpeg")
        self.assertEquals(im.size[0], 100, "Width on short jpeg thumbnail is 100")
        self.assertEquals(im.size[1], 1, "Height on short jpeg thumbnail is 1")
        self.assertEquals(im.format, 'JPEG', "Actual type of short thumbnail is still a jpeg")

        response = c.get("{0}/thumb/{1}x{2}".format(new_base_location, 1, 1))
        data = StringIO(response.content)
        im = Image.open(data)
        self.assertEquals(response["Content-type"], "image/jpeg", "Content type of 1-pixel thumbnail is jpeg")
        self.assertEquals(im.size[0], 1, "Width on 1-pixel jpeg thumbnail is 1")
        self.assertEquals(im.size[1], 1, "Height on 1-pixel jpeg thumbnail is 1")
        self.assertEquals(im.format, 'JPEG', "Actual type of 1-pixel thumbnail is still a jpeg")

        response = c.get("{0}/thumb/{1}x{2}".format(new_base_location, 200, 200))
        data = StringIO(response.content)
        im = Image.open(data)
        self.assertEquals(response["Content-type"], "image/jpeg", "Content type of 200x200 'thumbnail' is jpeg")
        self.assertEquals(im.size[0], 200, "Width on 200x200 jpeg 'thumbnail' is 1")
        self.assertEquals(im.size[1], 200, "Height on 200x200 jpeg 'thumbnail' is 1")
        self.assertEquals(im.format, 'JPEG', "Actual type of 200x200 jpeg 'thumbnail' is still a jpeg")

        response = c.get("{0}/thumb/{1}x{2}".format(new_base_location, 100, 0))
        self.assertEquals(response.status_code, 404, "404 for no height, jpeg")

        response = c.get("{0}/thumb/{1}x{2}".format(new_base_location, 0, 100))
        self.assertEquals(response.status_code, 404, "404 for no width, jpeg")

        response = c.get("{0}/thumb/{1}x{2}".format(new_base_location, 0, 0))
        self.assertEquals(response.status_code, 404, "404 for no width or height, jpeg")

        response = c.get("{0}/thumb/{1}x{2}".format(new_base_location, 100, -100))
        self.assertEquals(response.status_code, 404, "404 for negative height, jpeg")

        response = c.get("{0}/thumb/{1}x{2}".format(new_base_location, -100, 100))
        self.assertEquals(response.status_code, 404, "404 for negative width, jpeg")

        response = c.get("{0}/thumb/{1}x{2}".format(new_base_location, "a", 100))
        self.assertEquals(response.status_code, 404, "404 for invalid width, jpeg")

        response = c.get("{0}/thumb/{1}x{2}".format(new_base_location, 100, "a"))
        self.assertEquals(response.status_code, 404, "404 for invalid height, jpeg")

    def test_png_thumbs(self):
        c = Client()
        f = open('test/resources/test_png.png')
        response = c.post(self.url, { "description": "This is a png", "image": f })
        f.close()

        new_base_location = response["Location"]

        response = c.get("{0}/thumb/{1}x{2}".format(new_base_location, 100, 100))
        data = StringIO(response.content)
        im = Image.open(data)
        self.assertEquals(response["Content-type"], "image/png", "Content type of same size thumbnail is png")
        self.assertEquals(im.size[0], 100, "Width on same size png thumbnail is 100")
        self.assertEquals(im.size[1], 100, "Height on same size png thumbnail is 100")
        self.assertEquals(im.format, 'PNG', "Actual type of same size thumbnail is still a png")

        response = c.get("{0}/thumb/{1}x{2}".format(new_base_location, 1, 100))
        data = StringIO(response.content)
        im = Image.open(data)
        self.assertEquals(response["Content-type"], "image/png", "Content type of narrow thumbnail is png")
        self.assertEquals(im.size[0], 1, "Width on narrow png thumbnail is 1")
        self.assertEquals(im.size[1], 100, "Height on narrow png thumbnail is 100")
        self.assertEquals(im.format, 'PNG', "Actual type of narrow thumbnail is still a png")

        response = c.get("{0}/thumb/{1}x{2}".format(new_base_location, 100, 1))
        data = StringIO(response.content)
        im = Image.open(data)
        self.assertEquals(response["Content-type"], "image/png", "Content type of short thumbnail is png")
        self.assertEquals(im.size[0], 100, "Width on short png thumbnail is 100")
        self.assertEquals(im.size[1], 1, "Height on short png thumbnail is 1")
        self.assertEquals(im.format, 'PNG', "Actual type of short thumbnail is still a png")

        response = c.get("{0}/thumb/{1}x{2}".format(new_base_location, 1, 1))
        data = StringIO(response.content)
        im = Image.open(data)
        self.assertEquals(response["Content-type"], "image/png", "Content type of 1-pixel thumbnail is png")
        self.assertEquals(im.size[0], 1, "Width on 1-pixel png thumbnail is 1")
        self.assertEquals(im.size[1], 1, "Height on 1-pixel png thumbnail is 1")
        self.assertEquals(im.format, 'PNG', "Actual type of 1-pixel thumbnail is still a png")

        response = c.get("{0}/thumb/{1}x{2}".format(new_base_location, 200, 200))
        data = StringIO(response.content)
        im = Image.open(data)
        self.assertEquals(response["Content-type"], "image/png", "Content type of 200x200 'thumbnail' is png")
        self.assertEquals(im.size[0], 200, "Width on 200x200 png 'thumbnail' is 1")
        self.assertEquals(im.size[1], 200, "Height on 200x200 png 'thumbnail' is 1")
        self.assertEquals(im.format, 'PNG', "Actual type of 200x200 png 'thumbnail' is still a png")

        response = c.get("{0}/thumb/{1}x{2}".format(new_base_location, 100, 0))
        self.assertEquals(response.status_code, 404, "404 for no height, png")

        response = c.get("{0}/thumb/{1}x{2}".format(new_base_location, 0, 100))
        self.assertEquals(response.status_code, 404, "404 for no width, png")

        response = c.get("{0}/thumb/{1}x{2}".format(new_base_location, 0, 0))
        self.assertEquals(response.status_code, 404, "404 for no width or height, png")

        response = c.get("{0}/thumb/{1}x{2}".format(new_base_location, 100, -100))
        self.assertEquals(response.status_code, 404, "404 for negative height, png")

        response = c.get("{0}/thumb/{1}x{2}".format(new_base_location, -100, 100))
        self.assertEquals(response.status_code, 404, "404 for negative width, png")

        response = c.get("{0}/thumb/{1}x{2}".format(new_base_location, "a", 100))
        self.assertEquals(response.status_code, 404, "404 for invalid width, png")

        response = c.get("{0}/thumb/{1}x{2}".format(new_base_location, 100, "a"))
        self.assertEquals(response.status_code, 404, "404 for invalid height, png")

    def test_gif_thumbs(self):
        c = Client()
        f = open('test/resources/test_gif.gif')
        response = c.post(self.url, { "description": "This is a gif", "image": f })
        f.close()

        new_base_location = response["Location"]

        response = c.get("{0}/thumb/{1}x{2}".format(new_base_location, 100, 100))
        data = StringIO(response.content)
        im = Image.open(data)
        self.assertEquals(response["Content-type"], "image/gif", "Content type of same size thumbnail is gif")
        self.assertEquals(im.size[0], 100, "Width on same size gif thumbnail is 100")
        self.assertEquals(im.size[1], 100, "Height on same size gif thumbnail is 100")
        self.assertEquals(im.format, 'GIF', "Actual type of same size thumbnail is still a gif")

        response = c.get("{0}/thumb/{1}x{2}".format(new_base_location, 1, 100))
        data = StringIO(response.content)
        im = Image.open(data)
        self.assertEquals(response["Content-type"], "image/gif", "Content type of narrow thumbnail is gif")
        self.assertEquals(im.size[0], 1, "Width on narrow gif thumbnail is 1")
        self.assertEquals(im.size[1], 100, "Height on narrow gif thumbnail is 100")
        self.assertEquals(im.format, 'GIF', "Actual type of narrow thumbnail is still a gif")

        response = c.get("{0}/thumb/{1}x{2}".format(new_base_location, 100, 1))
        data = StringIO(response.content)
        im = Image.open(data)
        self.assertEquals(response["Content-type"], "image/gif", "Content type of short thumbnail is gif")
        self.assertEquals(im.size[0], 100, "Width on short gif thumbnail is 100")
        self.assertEquals(im.size[1], 1, "Height on short gif thumbnail is 1")
        self.assertEquals(im.format, 'GIF', "Actual type of short thumbnail is still a gif")

        response = c.get("{0}/thumb/{1}x{2}".format(new_base_location, 1, 1))
        data = StringIO(response.content)
        im = Image.open(data)
        self.assertEquals(response["Content-type"], "image/gif", "Content type of 1-pixel thumbnail is gif")
        self.assertEquals(im.size[0], 1, "Width on 1-pixel gif thumbnail is 1")
        self.assertEquals(im.size[1], 1, "Height on 1-pixel gif thumbnail is 1")
        self.assertEquals(im.format, 'GIF', "Actual type of 1-pixel thumbnail is still a gif")

        response = c.get("{0}/thumb/{1}x{2}".format(new_base_location, 200, 200))
        data = StringIO(response.content)
        im = Image.open(data)
        self.assertEquals(response["Content-type"], "image/gif", "Content type of 200x200 'thumbnail' is gif")
        self.assertEquals(im.size[0], 200, "Width on 200x200 gif 'thumbnail' is 1")
        self.assertEquals(im.size[1], 200, "Height on 200x200 gif 'thumbnail' is 1")
        self.assertEquals(im.format, 'GIF', "Actual type of 200x200 gif 'thumbnail' is still a gif")

        response = c.get("{0}/thumb/{1}x{2}".format(new_base_location, 100, 0))
        self.assertEquals(response.status_code, 404, "404 for no height, gif")

        response = c.get("{0}/thumb/{1}x{2}".format(new_base_location, 0, 100))
        self.assertEquals(response.status_code, 404, "404 for no width, gif")

        response = c.get("{0}/thumb/{1}x{2}".format(new_base_location, 0, 0))
        self.assertEquals(response.status_code, 404, "404 for no width or height, gif")

        response = c.get("{0}/thumb/{1}x{2}".format(new_base_location, 100, -100))
        self.assertEquals(response.status_code, 404, "404 for negative height, gif")

        response = c.get("{0}/thumb/{1}x{2}".format(new_base_location, -100, 100))
        self.assertEquals(response.status_code, 404, "404 for negative width, gif")

        response = c.get("{0}/thumb/{1}x{2}".format(new_base_location, "a", 100))
        self.assertEquals(response.status_code, 404, "404 for invalid width, gif")

        response = c.get("{0}/thumb/{1}x{2}".format(new_base_location, 100, "a"))
        self.assertEquals(response.status_code, 404, "404 for invalid height, gif")



