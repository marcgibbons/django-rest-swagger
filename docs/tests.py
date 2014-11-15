from django.test import LiveServerTestCase
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from PIL import Image
import time
import os.path


class ImageExtractionAndTests(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox();
        self.browser.implicitly_wait(3)
        self.browser.get(self.live_server_url)
        import time
        # let swagger load itself
        # todo - figure out what swagger is doing and wait on that
        time.sleep(1)

    def tearDown(self):
        self.browser.quit()

    def by_css(self, css_str, many=False, src=None):
        src = src or self.browser
        if many:
            return src.find_elements_by_css_selector(css_str)
        else:
            return src.find_element_by_css_selector(css_str)

    def save_screenshot(self, element, file_name):
        nom = 'swagger.png'
        self.browser.save_screenshot(nom)
        location = element.location
        size = element.size
        im = Image.open(nom)
        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']
        im = im.crop((left, top, right, bottom))
        im.save(os.path.join('source','_static',file_name))

    def get_toggle(self, endpoint):
        path = self.by_css(".path", src=endpoint)
        return self.by_css(".toggleOperation", src=path)

    def get_model_lines(self, endpoint):
        sgc = self.by_css(".signature-container", src=endpoint)
        desc = self.by_css(".description", src=sgc)
        span = self.by_css("span.strong", src=desc)
        divs = self.by_css("div", many=True, src=desc)
        return span, divs

    def test_cigars(self):
        cigars = self.by_css("#resource_cigars")
        a = self.by_css("a[href='#!/cigars']", src=cigars)
        a.click()
        time.sleep(1)
        cigars = self.by_css("#resource_cigars")
        endpoints = self.by_css("li.endpoint", many=True, src=cigars)
        self.assertEqual(len(endpoints), 8)
        a2 = self.by_css("a[href='#!/cigars/Cigar_0_1_2_3_4_5_6']")
        WebDriverWait(self.browser, 10).until(
            lambda b: a2.is_displayed()
        )

        endpoints = [e for e in endpoints 
                     if self.get_toggle(e).text == '/api/cigars/']
        toggle = self.get_toggle(endpoints[0])
        toggle.click()
        time.sleep(1)
        span, divs = self.get_model_lines(endpoints[0])
        self.assertEqual(span.text, "CigarSerializer {")
        self.assertEqual(len(divs), 10)
        self.assertEqual(divs[0].text, "url (url),")
        self.assertEqual(divs[1].text, "id (integer),")
        self.assertEqual(divs[2].text, "name (string): Cigar Name,")
        self.assertEqual(divs[3].text, "colour (string),")
        self.assertEqual(divs[4].text, "form (multiple choice) = ['parejo' or 'torpedo' or 'pyramid' or 'perfecto' or 'presidente'],")
        self.save_screenshot(cigars, "cigar.png")

    def test_artisan_cigars(self):
        cigars = self.by_css("#resource_artisan_cigars")
        a = self.by_css("a[href='#!/artisan_cigars']", src=cigars)
        a.click()
        time.sleep(1)
        cigars = self.by_css("#resource_artisan_cigars")
        endpoints = self.by_css("li.endpoint", many=True, src=cigars)
        self.assertEqual(len(endpoints), 8)
        a2 = self.by_css("a[href='#!/artisan_cigars/Artisan_Cigar_0_1_2_3_4_5_6']")
        WebDriverWait(self.browser, 10).until(
            lambda b: a2.is_displayed()
        )

        endpoints = [e for e in endpoints 
                     if self.get_toggle(e).text == '/api/artisan_cigars/{pk}/set_price/']
        toggle = self.get_toggle(endpoints[0])
        toggle.click()
        time.sleep(1)
        e = endpoints[0]
        sgc = self.by_css(".signature-container", many=True, src=e)
        self.assertEqual(len(sgc), 0)
        http_method = self.by_css(".http_method", src=e)
        self.assertEqual(http_method.text, "POST")
        self.save_screenshot(cigars, "artisan_cigar.png")
    
    def test_manufacturer_list(self):
        manufacturers = self.by_css("#resource_manufacturers")
        a = self.by_css(
            "a[href='#!/manufacturers']", 
            src=manufacturers
        )
        a.click()
        time.sleep(1)
        manufacturers = self.by_css("#resource_manufacturers")
        def is_from_list(endpoint):
            return self.get_toggle(endpoint).text == '/api/manufacturers/'
        def get_endpoints():
            return [e for e in self.by_css("li.endpoint", many=True, src=manufacturers)
                         if self.get_toggle(e).text == '/api/manufacturers/']

        WebDriverWait(self.browser, 10).until(lambda b: len(get_endpoints()) == 2)
        for e in get_endpoints():
            toggle = self.get_toggle(e)
            toggle.click()
            content = self.by_css(".content", src=e)
            # wait for animation
            time.sleep(1)
            span, divs = self.get_model_lines(e)
            self.assertEqual(span.text, "ManufacturerSerializer {")
            self.assertEqual(len(divs), 3)
            self.assertEqual(divs[0].text, "id (integer),")
            self.assertEqual(divs[1].text, "name (string): name of company,")
            self.assertEqual(divs[2].text, "country (field)")
            http_method = self.by_css(".http_method", src=e)
            self.save_screenshot(e, "manufacturerList-%s.png" % http_method.text)
            toggle.click()

    def test_find_jambalaya(self):
        jambalaya = self.by_css("#resource_jambalaya_find")
        a = self.by_css(
            "a[href='#!/jambalaya_find']", 
            src=jambalaya
        )
        a.click()
        time.sleep(1)
        jambalaya = self.by_css("#resource_jambalaya_find")
        def get_endpoints():
            return [e for e in self.by_css("li.endpoint", many=True, src=jambalaya)
                         if self.get_toggle(e).text == '/api/jambalaya_find/']

        WebDriverWait(self.browser, 10).until(lambda b: len(get_endpoints()) == 1)
        e = get_endpoints()[0]
        toggle = self.get_toggle(e)
        toggle.click()
        content = self.by_css(".content", src=e)
        # wait for animation
        time.sleep(1)
        span, divs = self.get_model_lines(e)
        self.assertEqual(span.text, "JambalayaSerializer {")
        self.assertEqual(len(divs), 2)
        self.assertEqual(divs[0].text, "id (integer),")
        self.assertEqual(divs[1].text, "recipe (string)")
        http_method = self.by_css(".http_method", src=e)
        self.save_screenshot(jambalaya, "jambalaya_find-%s.png" % http_method.text)
        toggle.click()
