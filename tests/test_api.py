import unittest

from api.main import list_terms, read_root


class APIFunctionTestCase(unittest.TestCase):
    def test_root_metadata_includes_roles_and_categories(self):
        payload = read_root()
        self.assertGreaterEqual(payload["count"], 50)
        self.assertIn("LLM Core", payload["categories"])
        self.assertIn("policy", payload["roles"])

    def test_role_filter_returns_only_matching_terms(self):
        results = list_terms(q=None, category=None, status=None, alias=None, role="policy")
        self.assertTrue(results)
        for term in results:
            roles = [value.lower() for value in term.get("roles", [])]
            self.assertIn("policy", roles)

    def test_alias_lookup_returns_expected_slug(self):
        results = list_terms(q=None, category=None, status=None, alias="RAG", role=None)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["slug"], "retrieval-augmented-generation")


if __name__ == "__main__":
    unittest.main()
