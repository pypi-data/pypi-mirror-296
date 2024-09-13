# Simple Authorizer for Amazon API Gateway

This is a simple Lambda authorizer for Amazon API Gateway, designed to protect an HTTP API, placed behind a CloudFront distribution, from direct access. The authorizer checks a secret value from an environment variable against a value received in an HTTP header from the client (CloudFront). If the values match, access is granted.

This authorizer is lightweight and requires minimal resources, making it highly cost-effective for simple use cases. It doesn't use AWS Secrets Manager, make external network calls, or support key rotation, keeping the implementation straightforward.

## Installation

To install the package, run:

```bash
pip install amazon-api-gateway-simple-authorizer
```

## Usage

The Lambda function authorizer can be used to protect API Gateway endpoints by verifying a custom header passed by CloudFront. It compares the header value with a secret API key stored as an environment variable.

### Environment Variables

- `API_KEY`: The secret API key expected from the client (CloudFront).
- `API_KEY_HEADER_NAME`: (Optional) The name of the header that contains the API key. If not set, the default header name `"x-origin-verify"` will be used.

### Lambda Handler

The Lambda function handler is located at:

```plaintext
simple_authorizer.authorizer.handler
```

### Example Event

Here's a sample event that can be passed to the Lambda authorizer:

```json
{
    "headers": {
        "x-origin-verify": "your-secret-api-key"
    }
}
```

If the secret in the `x-origin-verify` header matches the value stored in the `API_KEY` environment variable, the request is authorized.

### Example Usage

To deploy the Lambda authorizer, follow these steps:

1. **Set up Lambda environment variables**:
   - `API_KEY`: Your secret key, e.g., `"your-secret-api-key"`.
   - `API_KEY_HEADER_NAME`: (Optional) If you want to use a custom header name, e.g., `"x-api-key"`. If not set, the default is `"x-origin-verify"`.

2. **Deploy your Lambda function** using the AWS Management Console or AWS CLI and ensure the handler is set to `simple_authorizer.authorizer.handler`.

3. **Configure API Gateway**:
   - In your API Gateway, set up a custom authorizer and select the Lambda function as the authorizer.
   - Use the matching header (default: `"x-origin-verify"`, or your custom value set by `API_KEY_HEADER_NAME`) in your CloudFront configuration to pass the API key.

### Performance and Cost Recommendations

- **Memory**: Allocate 128MB of memory to the Lambda function for optimal cost efficiency.
- **Timeout**: Set the timeout to 3 seconds, as the function is lightweight and doesn't require more time even with the cold start.
- **Caching**: Cache the authorization result for the maximum allowed time (1 hour) for both performance and cost savings.

## Limitations

- This solution does **not support key rotation**.
- It does **not integrate with AWS Secrets Manager** or any external key storage service.
- It requires manual updates for key changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Disclaimer

This software product is not affiliated with, endorsed by, or sponsored by Amazon Web Services (AWS) or Amazon.com, Inc. The use of the term "AWS" is solely for descriptive purposes to indicate that the software is compatible with AWS services. Amazon Web Services and AWS are trademarks of Amazon.com, Inc. or its affiliates.