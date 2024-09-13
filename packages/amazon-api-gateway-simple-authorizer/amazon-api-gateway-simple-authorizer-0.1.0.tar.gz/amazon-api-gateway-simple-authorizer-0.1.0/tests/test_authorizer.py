"""
test_authorizer.py: Unit tests for the Lambda authorizer function in the 'simple_authorizer.
authorizer' module.

This test module contains various test cases to verify the behavior of the custom Lambda
function that authorizes API Gateway requests based on an API key. The API key is provided
in the request headers and compared to a value stored in environment variables.
"""

import unittest
from unittest.mock import patch
from simple_authorizer.authorizer import handler, constant_time_compare


class TestLambdaAuthorizer(unittest.TestCase):
    """
    Unit test class for testing the Lambda authorizer module.
    
    This class includes tests to verify the functionality of the API key authorization logic, 
    ensuring correct behavior for various valid and invalid inputs. Mocking is used to simulate 
    environment variables and logging where necessary.
    """

    def setUp(self) -> None:
        """
        Set up the environment variables and any necessary initial configurations for each test.

        This method runs before every test case to mock environment variables for API key
        validation.
        """
        self.valid_api_key = 'test-valid-key'
        self.invalid_api_key = 'test-invalid-key'
        self.header_name = 'x-origin-verify'

        # Patch environment variables for each test case
        patcher = patch.dict('os.environ', {
            'API_KEY': self.valid_api_key,
            'API_KEY_HEADER_NAME': self.header_name
        })
        patcher.start()
        self.addCleanup(patcher.stop)  # Ensure patcher is stopped after each test

    @patch('simple_authorizer.authorizer.logger')
    def test_authorize_with_valid_key(self, mock_logger):  # pylint: disable=unused-argument
        """
        Test that the handler correctly authorizes a request with the valid API key.
        
        This test simulates a request with the valid API key and checks that the handler 
        returns 'isAuthorized: True'.
        """
        event = {
            'headers': {
                'x-origin-verify': self.valid_api_key  # Correct key
            }
        }

        # Call the handler and verify that authorization is granted
        result = handler(event, None)
        self.assertTrue(result['isAuthorized'])


    @patch('simple_authorizer.authorizer.logger')
    def test_authorize_with_invalid_key(self, mock_logger):  # pylint: disable=unused-argument
        """
        Test that the handler denies authorization with an invalid API key.
        
        This test simulates a request with an invalid API key and checks that the handler 
        returns 'isAuthorized: False'.
        """
        event = {
            'headers': {
                'x-origin-verify': self.invalid_api_key  # Incorrect key
            }
        }

        # Call the handler and verify that authorization is denied
        result = handler(event, None)
        self.assertFalse(result['isAuthorized'])

    @patch('simple_authorizer.authorizer.logger')
    def test_authorize_missing_api_key(self, mock_logger):  # pylint: disable=unused-argument
        """
        Test that the handler denies authorization when no API key is provided in the headers.
        
        This test simulates a request where the API key header is missing and checks that 
        'isAuthorized: False' is returned.
        """
        event = {
            'headers': {}  # No API key provided
        }

        # Call the handler and verify that authorization is denied
        result = handler(event, None)
        self.assertFalse(result['isAuthorized'])

    @patch('simple_authorizer.authorizer.logger')
    def test_error_handling(self, mock_logger):
        """
        Test that the handler denies authorization and handles exceptions gracefully.
        
        This test simulates an exception during the execution of the handler (e.g., a missing
        'headers' field in the event) and checks that 'isAuthorized: False' is returned.
        """
        # Malformed event that will raise an exception
        event = None  # Invalid event input

        # Call the handler and verify that authorization is denied due to an exception
        result = handler(event, None)
        self.assertFalse(result['isAuthorized'])

        # Check that the error was logged
        mock_logger.error.assert_called()

    @patch('simple_authorizer.authorizer.logger')
    def test_case_insensitive_header_matching(self, mock_logger):  # pylint: disable=unused-argument
        """
        Test that the handler performs case-insensitive matching for the API key header.
        
        This test ensures that the handler correctly identifies the API key header regardless 
        of the case of the header name.
        """
        event = {
            'headers': {
                'X-ORIGIN-VERIFY': self.valid_api_key  # Uppercase header name
            }
        }

        # Call the handler and verify that authorization is granted
        result = handler(event, None)
        self.assertTrue(result['isAuthorized'])


class TestConstantTimeCompare(unittest.TestCase):
    """
    Unit test class for testing the constant-time string comparison function.
    
    This class verifies the correct behavior of the constant-time string comparison function 
    to prevent timing attacks.
    """

    def test_identical_strings(self):
        """
        Test that the constant time compare function returns True for identical strings.
        
        This test checks that the function returns True when comparing two identical strings.
        """
        self.assertTrue(constant_time_compare('test', 'test'))

    def test_different_strings(self):
        """
        Test that the constant time compare function returns False for different strings.
        
        This test checks that the function returns False when comparing two different strings.
        """
        self.assertFalse(constant_time_compare('test', 'different'))

    def test_empty_strings(self):
        """
        Test that the constant time compare function returns True for two empty strings.
        
        This test checks that the function returns True when comparing two empty strings.
        """
        self.assertTrue(constant_time_compare('', ''))


if __name__ == '__main__':
    unittest.main()
