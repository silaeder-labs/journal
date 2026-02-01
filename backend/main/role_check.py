from keycloak import KeycloakOpenID
from keycloak_auth import KEYCLOAK_URL, REALM, CLIENT_ID

def is_admin(token):
    keycloak_openid = KeycloakOpenID(
        server_url=KEYCLOAK_URL,
        client_id=CLIENT_ID,
        realm_name=REALM
    )

    info = keycloak_openid.decode_token(token, validate=True)
    return "admin" in info["realm_access"]["roles"]

def is_teacher(token):
    keycloak_openid = KeycloakOpenID(
        server_url=KEYCLOAK_URL,
        client_id=CLIENT_ID,
        realm_name=REALM
    )

    info = keycloak_openid.decode_token(token, validate=True)
    return "teacher" in info["resource_access"][CLIENT_ID]["roles"]

if __name__ == "__main__":
    token = 'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJvcTJ3cXlkSUtXa3ZDUUgzVXBPQUZxeDV2c295MUMyazZzckJ6R3pzSGVRIn0.eyJleHAiOjE3Njk5NjQ4MjYsImlhdCI6MTc2OTk2NDUyNiwiYXV0aF90aW1lIjoxNzY5OTY0NTI2LCJqdGkiOiJvbnJ0YWM6NTFhNjkyZWQtYzk5Ny1lZjkzLWQwMTMtYjcyYzgxNWRjZWNjIiwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDo4MDgwL3JlYWxtcy9teXJlYWxtIiwiYXVkIjoiYWNjb3VudCIsInN1YiI6IjA3NDg1ZDdkLWZjYzItNDdkZi1iYjIwLWEyNjMxNDgzYWMzNCIsInR5cCI6IkJlYXJlciIsImF6cCI6Im15YXBwIiwic2lkIjoiendHWXM0SU51S05nQS04c3JlM3lxZ2hkIiwiYWNyIjoiMSIsImFsbG93ZWQtb3JpZ2lucyI6WyIvKiJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiZGVmYXVsdC1yb2xlcy1teXJlYWxtIiwib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiJdfSwicmVzb3VyY2VfYWNjZXNzIjp7Im15YXBwIjp7InJvbGVzIjpbInRlYWNoZXIiXX0sImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIGVtYWlsIHByb2ZpbGUiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsIm5hbWUiOiJhYm9iYSBhYm9iYSIsInByZWZlcnJlZF91c2VybmFtZSI6ImFib2JhIiwiZ2l2ZW5fbmFtZSI6ImFib2JhIiwiZmFtaWx5X25hbWUiOiJhYm9iYSIsImVtYWlsIjoiYWJvYmFAZXhhbXBsZS5jb20ifQ.tctw99s_68HVnQTDbADzSwGQIpPyb6xmfg6pKyBFrtjW-RXBmj5L7FKABjDIIOInRNbaeS9tkWODIVub6GzeOblB7MGVxPObt-IW8zT5SvkjqM-XnL7hhi1znevx_j7cUcfZyzwQ5JAAolZv_wwCNorritFBoPj3Q4zrUyuj1ujpW3maTx3XAKrHJyFqAu-Y3lro9bpt00vdIgv85qurwdW44PA1sI1SSPDq3-S0KzsMr81uzfjO7bnJzlF3nkwV5dC_r2DthFuxTMDYv1W5vk-sVQz7Mti0t1zrCM-SwruLTHEMSdHSmGB2Ut2BUUfOiuq5zvxpslNltu3yObRTNA'
    print(is_teacher(token))
