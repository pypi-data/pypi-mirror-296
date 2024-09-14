import json
import base64
import jwt
from datetime import datetime, timezone, timedelta

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

import ascend_sdk
from ascend_sdk.models import components, errors, operations


class ApexSecuritySource:
    apiKey: str = None
    apexClientCredsJson: str = None
    server: str = None
    accessToken: str = None
    accessTokenExpiration: datetime = None
    sdk: ascend_sdk.SDK = None

    def __init__(
        self, apexClientCredsJson: str = None, apiKey: str = None, server: str = None
    ):
        self.apexClientCredsJson = apexClientCredsJson
        self.apiKey = apiKey
        self.server = server
        try:
            self.sdk = ascend_sdk.SDK(
                security=components.Security(
                    api_key_auth=apiKey,
                    bearer_auth="",
                ),
                server_url=server,
            )
        except errors.SDKError as e:
            raise errors.SDKError("Failed to initialize ApexSecuritySource: " + str(e))

    def getSecurity(self) -> components.Security:
        if self.accessTokenStillValid():
            return components.Security(
                bearer_auth=self.accessToken,
                api_key_auth=self.apiKey,
            )
        jws = self.getJWS()
        request = components.GenerateServiceAccountTokenRequestCreate(jws=jws)
        security = operations.AuthenticationGenerateServiceAccountTokenSecurity(
            api_key_auth=self.apiKey,
        )
        try:
            response = self.sdk.authentication.generate_service_account_token(
                request=request, security=security
            )
        except errors.Status as e:
            # handle exception
            raise e
        except errors.SDKError as e:
            # handle exception
            raise e

        self.accessToken = getattr(response.token, "access_token", None)
        self.accessTokenExpiration = datetime.now()
        self.accessTokenExpiration += timedelta(minutes=(60 * 25 - 30))
        return components.Security(
            bearer_auth=self.accessToken,
            api_key_auth=self.apiKey,
        )

    def getJWS(self) -> str:
        try:
            # Parse the JSON to a dictionary
            creds_data = json.loads(self.apexClientCredsJson)

            # Extract the private key, removing headers, footers, and newlines
            private_key_content = (
                creds_data["privateKey"]
                .replace("\n", "")
                .replace("\r", "")
                .replace("-----BEGIN PRIVATE KEY-----", "")
                .replace("-----END PRIVATE KEY-----", "")
            )

            # Decode the base64 private key
            decoded_key = base64.b64decode(private_key_content)
            # Deserialize the key to RSAPrivateKey object
            private_key = serialization.load_der_private_key(
                decoded_key, password=None, backend=default_backend()
            )

            # Prepare claims for the JWT
            now_iso_date_time = datetime.now(timezone.utc).isoformat()
            claims = {
                "iss": "issuer",
                "sub": "subject",
                "name": creds_data.get("name"),
                "organization": creds_data.get("organization"),
                "datetime": now_iso_date_time,
            }

            # Create a JWT and sign it with the private key using RS256 algorithm
            encoded_jwt = jwt.encode(claims, private_key, algorithm="RS256")

            return encoded_jwt

        except errors.SDKError as e:
            raise errors.SDKError("Failed to get JWS: " + str(e))

    def accessTokenStillValid(self) -> bool:
        if self.accessToken is None:
            return False
        return (
            self.accessTokenExpiration is not None
            and self.accessTokenExpiration > datetime.now()
        )
