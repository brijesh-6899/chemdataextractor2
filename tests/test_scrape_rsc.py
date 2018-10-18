# -*- coding: utf-8 -*-
"""
test_scrape_rsc
~~~~~~~~~~~~~~~

Test scraping documents from the Royal Society of Chemistry.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging
import unittest

from chemdataextractor.scrape.pub.rsc import rsc_substitute, strip_rsc_html, RscSearchScraper
from selenium import webdriver


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class TestRscSubstitutor(unittest.TestCase):
    """Test escape sequences in titles/abstracts from RSC are converted to unicode characters."""

    def test_small_beta(self):
        original = 'A sensitive colorimetric strategy for sensitively monitoring cerebral [small beta]-amyloid peptides in AD based on dual-functionalized gold nanoplasmic particles'
        fixed = 'A sensitive colorimetric strategy for sensitively monitoring cerebral β-amyloid peptides in AD based on dual-functionalized gold nanoplasmic particles'
        self.assertEqual(rsc_substitute(original), fixed)

    def test_prime(self):
        original = 'Selective formation of benzo[c]cinnoline by photocatalytic reduction of 2,2[prime or minute]-dinitrobiphenyl using TiO2 and under UV light irradiation'
        fixed = 'Selective formation of benzo[c]cinnoline by photocatalytic reduction of 2,2′-dinitrobiphenyl using TiO2 and under UV light irradiation'
        self.assertEqual(rsc_substitute(original), fixed)

    def test_beta_gamma(self):
        original = '[small beta],[gamma]-Bis-substituted PNA with configurational and conformational switch: preferred binding to cDNA/RNA and cell-uptake studies'
        fixed = 'β,γ-Bis-substituted PNA with configurational and conformational switch: preferred binding to cDNA/RNA and cell-uptake studies'
        self.assertEqual(rsc_substitute(original), fixed)


class TestStripRscHtml(unittest.TestCase):

    def test_title_footnote(self):
        """Test that footnote links are removed from the end of titles."""
        html = '<span class="title_heading">Rationale for the sluggish oxidative addition of aryl halides to Au(<span class="small_caps">I</span>)<a title="Electronic supplementary information (ESI) available. CCDC 891201–891204 and 964933. For ESI and crystallographic data in CIF or other electronic format see DOI: 10.1039/c3cc48914k" href="#fn1">†</a></span>'
        stripped = '<span class="title_heading">Rationale for the sluggish oxidative addition of aryl halides to Au(I)</span>'
        self.assertEqual(strip_rsc_html.clean_html(html), stripped)


class TestRscSearchScraper(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        query_text = "Aspirin"
        scraper = RscSearchScraper(sleep_time=9)
        scrape = scraper.run(query_text)
        scrape_10 = scraper.run(query_text, 10)
        self.results = scrape.serialize()
        self.results_10 = scrape_10.serialize()

    def test_doi(self):
        self.assertTrue('doi' in self.results[0].keys())

    def test_title(self):
        self.assertTrue('title' in self.results[0].keys())

    def test_landing_url(self):
        self.assertTrue('landing_url' in self.results[0].keys())

    def test_pdf_url(self):
        self.assertTrue('pdf_url' in self.results[0].keys())

    def test_html_url(self):
        self.assertTrue('html_url' in self.results[0].keys())

    def test_journal(self):
        self.assertTrue('journal' in self.results[0].keys())

    def test_pagination(self):
        self.assertNotEqual(self.results[0], self.results_10[0])
