"""
AgroScan AI — Safety Fact Checker Unit Tests
Verifies that high-risk banned pesticides and unsupported chemical claims are detected and sanitized.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.verification.fact_checker import FactChecker

class TestFactChecker(unittest.TestCase):

    def test_banned_chemical_sanitization(self):
        unsafe_answer = "You should spray Monocrotophos and Endosulfan at 5ml/L every 2 days."
        evidence = [{"claim": "Use biological control and registered fungicides."}]

        res = FactChecker.verify_and_sanitize_response(unsafe_answer, evidence)
        self.assertTrue(res["passed"])
        self.assertNotIn("Monocrotophos", res["sanitized_answer"])
        self.assertNotIn("Endosulfan", res["sanitized_answer"])
        self.assertIn("approved", res["sanitized_answer"].lower())

    def test_safe_response_preserved(self):
        safe_answer = "Apply cold-pressed Neem Oil (3000 ppm @ 4 ml/L) or Wettable Sulphur under label instructions."
        evidence = [{"claim": "Neem oil and wettable sulphur are effective."}]

        res = FactChecker.verify_and_sanitize_response(safe_answer, evidence)
        self.assertTrue(res["passed"])
        self.assertIn("Neem Oil", res["sanitized_answer"])

if __name__ == "__main__":
    unittest.main()
