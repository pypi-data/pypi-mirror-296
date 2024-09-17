# codi-requests-oauthlib

wrapper around requests-oauthlib that alows for refreshing tokens if they are expired, with out a refresh url

## Example Usage

```python
config = dotenv_values("tests.env")
client = OAuthClient(
    client_id=config.get("CLIENT_ID"),
    client_secret=config.get("CLIENT_SECRET"),
    token_url=config.get("TOKEN_URL"),
    base_url=config.get("BASE_URL"),
    scope=config.get("SCOPE")
)
# this is for a Tyler API call example
url = f"{config.get("BASE_URL")}/Prod/munisopenapi/hosts/EAM/odata/HR/v2/employees?$filter=employeeActiveStatusCode eq 'A'"
resp = client.session.get(url)
```