from django.test import TestCase
from app.google_calendar import safe_linkify


class SafeLinkifyTests(TestCase):

    def test_https_link_converted(self):
        text = 'Visit https://example.com for more.'
        expected = 'Visit <a href="https://example.com">https://example.com</a> for more.'
        self.assertEqual(safe_linkify(text), expected)

    def test_www_link_converted(self):
        text = 'Go to www.example.com for info.'
        expected = 'Go to <a href="https://www.example.com">www.example.com</a> for info.'
        self.assertEqual(safe_linkify(text), expected)

    def test_email_converted(self):
        text = 'Contact us at info@example.com.'
        expected = 'Contact us at <a href="mailto:info@example.com">info@example.com</a>.'
        self.assertEqual(safe_linkify(text), expected)

    def test_links_already_wrapped_are_ignored(self):
        text = 'Visit <a href="https://example.com">https://example.com</a>.'
        self.assertEqual(safe_linkify(text), text)

    def test_mixed_links_and_emails(self):
        text = 'See www.test.com or email john@doe.com or visit https://example.org'
        result = safe_linkify(text)
        self.assertIn('<a href="https://www.test.com">www.test.com</a>', result)
        self.assertIn('<a href="mailto:john@doe.com">john@doe.com</a>', result)
        self.assertIn('<a href="https://example.org">https://example.org</a>', result)

    def test_quote_escaping(self):
        text = 'Quote test "https://example.com"'
        result = safe_linkify(text)
        self.assertIn('\\"https://example.com\\"', result.replace('"', '\\"'))