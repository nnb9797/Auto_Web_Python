import yaml
from module import Site, testdata

with open("testdata.yaml", encoding="utf-8"):
    site = Site(testdata["address"])

css_selector = "span.mdc-text-field__ripple"
print(site.get_element_property("css", css_selector, "height"))

xpath = '//*[@id="login"]/div[3]/button/div'
print(site.get_element_property("xpath", xpath, "color"))