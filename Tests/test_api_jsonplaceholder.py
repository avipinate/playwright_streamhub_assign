
import pytest
from playwright.sync_api import sync_playwright

BASE_URL = "https://jsonplaceholder.typicode.com"

def test_with_long_title():
    with sync_playwright() as p:
        request_context = p.request.new_context(base_url=BASE_URL, ignore_https_errors=True)

        long_title = "A" * 10000

        response = request_context.post(
            "/posts",
            data={
                "title": long_title,
                "body": "Test body",
                "userId": 1
            }
        )

        print("Status Code:", response.status) #it will always return 201 as it's a fake API

        assert response.status in [201, 400], "Unexpected status code"

        request_context.dispose()


def test_with_special_characters():
    with sync_playwright() as p:
        request_context = p.request.new_context(base_url=BASE_URL, ignore_https_errors=True)

        response = request_context.post(
            "/posts",
            data={
                "title": "@@@###$$$%%%^^^&&&***((()))",
                "body": "<script>alert('XSS')</script>",
                "userId": 1
            }
        )

        print("Status Code:", response.status)

        assert response.status in [201, 400]

        request_context.dispose()


def test_missing_userid():
    with sync_playwright() as p:
        request_context = p.request.new_context(base_url=BASE_URL, ignore_https_errors=True)

        response = request_context.post(
            "/posts",
            data={
                "title": "Missing userId test",
                "body": "Test body"
                # userId is missing
            }
        )

        print("Status Code:", response.status)

        assert response.status in [201, 400]

        response_json = response.json()
        assert "userId" not in response_json, "'userId' is missing"

        request_context.dispose()
