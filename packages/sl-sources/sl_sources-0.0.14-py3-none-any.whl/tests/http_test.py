from typing import Optional
from urllib.parse import urlparse

import pytest

from sl_sources.http import resolve_url, validate_url


@pytest.mark.asyncio
def test_http() -> None:
    """
    Run comprehensive tests for URL validation and resolution.

    This function tests the validate_url and resolve_url functions with
    various input cases to ensure they behave correctly.
    """
    print("Running comprehensive tests for URL validation and resolution:")

    def test_case(
        func: callable,
        input_url: str,
        expected_output: Optional[str] = None,
        should_raise: bool = False,
        base_url: Optional[str] = None,
    ) -> None:
        """
        Test a single case for URL validation or resolution.

        Parameters
        ----------
        func : callable
            The function to test (either validate_url or resolve_url).
        input_url : str
            The input URL to test.
        expected_output : Optional[str], optional
            The expected output (default is None).
        should_raise : bool, optional
            Whether the function should raise an exception (default is False).
        base_url : Optional[str], optional
            The base URL to use for resolve_url (default is None).
        """
        try:
            if base_url:
                result = func(input_url, base_url)
            else:
                result = func(input_url)
            if should_raise:
                print(
                    f"  FAIL: {func.__name__}('{input_url}') did not raise an exception as expected"
                )
            elif expected_output is not None and result != expected_output:
                print(
                    f"  FAIL: {func.__name__}('{input_url}') returned '{result}', expected '{expected_output}'"
                )
            else:
                print(f"  PASS: {func.__name__}('{input_url}') -> '{result}'")
        except ValueError as e:
            if should_raise:
                print(
                    f"  PASS: {func.__name__}('{input_url}') correctly raised ValueError: {str(e)}"
                )
            else:
                print(
                    f"  FAIL: {func.__name__}('{input_url}') raised unexpected ValueError: {str(e)}"
                )

    # Test validate_url
    print("\nTesting validate_url function:")
    validate_test_cases = [
        ("http://example.com", "http://example.com"),
        ("https://example.com", "https://example.com"),
        ("www.example.com", "https://www.example.com"),
        ("example.com", "https://example.com"),
        ("sub.example.com", "https://sub.example.com"),
        ("example.com/path", "https://example.com/path"),
        ("example.com/path?query=value", "https://example.com/path?query=value"),
        ("example.com/path#fragment", "https://example.com/path#fragment"),
        ("ftp://example.com", None, True),
        ("invalid://example.com", None, True),
        ("not a url", None, True),
        ("http:/example.com", None, True),
        ("https:/example.com", None, True),
    ]
    for case in validate_test_cases:
        test_case(validate_url, *case)

    # Test resolve_url
    print("\nTesting resolve_url function:")
    base_url = "https://example.com/base/"
    resolve_test_cases = [
        ("http://example.com", "http://example.com"),
        ("https://example.com", "https://example.com"),
        ("https://example.com/path", "https://example.com/path"),
        (
            "https://example.com/path?query=value",
            "https://example.com/path?query=value",
        ),
        ("https://example.com/path#fragment", "https://example.com/path#fragment"),
        ("//example.com", "https://example.com"),
        ("www.example.com", "https://www.example.com"),
        ("/path", "https://example.com/path", False, base_url),
        ("./path", "https://example.com/base/path", False, base_url),
        ("../path", "https://example.com/path", False, base_url),
        ("path", "https://example.com/base/path", False, base_url),
        ("example.com", "https://example.com"),
        ("://example.com", None, True),
        ("http:/example.com", None, True),
        ("not a url", None, True),
        ("/path", None, True),  # should raise when no base_url is provided
    ]
    for case in resolve_test_cases:
        test_case(resolve_url, *case)

    # Test specific links
    print("\nTesting specific links:")
    specific_links = [
        "https://arxiv.org/pdf/1706.03762",
        "https://pubmed.ncbi.nlm.nih.gov/35641793/",
        "http://www.rctn.org/bruno/papers/TN-review.pdf",
        "https://www.nature.com/articles/nrn3475.pdf",
    ]
    for link in specific_links:
        print(f"\nTesting link: {link}")
        test_case(validate_url, link)
        test_case(resolve_url, link)

        # Additional checks for resolved URL
        resolved = resolve_url(link)
        parsed = urlparse(resolved)
        if not parsed.scheme or not parsed.netloc:
            print(f"  WARN: Resolved URL may be incomplete: {resolved}")
        if parsed.scheme not in ["http", "https"]:
            print(f"  WARN: Unusual scheme in resolved URL: {parsed.scheme}")
