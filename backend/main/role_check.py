from keycloak import KeycloakOpenID
from keycloak_auth import KEYCLOAK_URL, REALM, CLIENT_ID

def is_admin(token):
    info = get_user_info(token)    
    try:
        return "admin" in info["realm_access"]["roles"]
    except:
        return False

def is_teacher(token):
    info = get_user_info(token)    
    try:
        return "teacher" in info["resource_access"][CLIENT_ID]["roles"]
    except:
        return False


def get_user_info(token):
    keycloak_openid = KeycloakOpenID(
        server_url=KEYCLOAK_URL,
        client_id=CLIENT_ID,
        realm_name=REALM
    )

    info = keycloak_openid.decode_token(token, validate=True)

    return info

if __name__ == "__main__":
    token = 'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJvcTJ3cXlkSUtXa3ZDUUgzVXBPQUZxeDV2c295MUMyazZzckJ6R3pzSGVRIn0.eyJleHAiOjE3NzAwNjYwODksImlhdCI6MTc3MDA2NTc4OSwiYXV0aF90aW1lIjoxNzcwMDY1MDgzLCJqdGkiOiJvbnJ0YWM6ZWFkMTkzNTUtNGZlMy03ODIyLTg2MTgtMDFmNDMxZDJjYzMwIiwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDo4MDgwL3JlYWxtcy9teXJlYWxtIiwiYXVkIjoiYWNjb3VudCIsInN1YiI6IjhkNTY5NmUzLWE2ZTgtNDQzMi1hODBiLWIzMjk2ZDYxNmVlNyIsInR5cCI6IkJlYXJlciIsImF6cCI6Im15YXBwIiwic2lkIjoiTDFUZEFoem1NTmlRTUJwUWRHenlyMzdkIiwiYWNyIjoiMCIsImFsbG93ZWQtb3JpZ2lucyI6WyIvKiJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiZGVmYXVsdC1yb2xlcy1teXJlYWxtIiwib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIGVtYWlsIHByb2ZpbGUiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsIm1lc2hfaWQiOiIyYzAxYWMwYi0xZWFiLTQ2NzMtYjI0My1iMTY3OWRjZDQ4ODEiLCJuYW1lIjoiZmlyc3RfbmFtZTIgbGFzdF9uYW1lMyIsInByZWZlcnJlZF91c2VybmFtZSI6InVzZXJuYW1lMSIsImdpdmVuX25hbWUiOiJmaXJzdF9uYW1lMiIsIm1pZGRsZV9uYW1lIjoibWlkZGxlX25hbWU0IiwiZmFtaWx5X25hbWUiOiJsYXN0X25hbWUzIiwiY2xhc3MiOjgsImVtYWlsIjoidXNlcmVtYWlsQGV4YW1wbGUuY29tIn0.14kvbB0kEzndJyYDbRNDNbUxuwW06YcI_XPkVO-byoEhQ_fD8tHs-thl-z7k118bB4tlu73qJqKh7El4x6TALvvO_7SzLUvQ6NLrrOfmPRYTh-dGZF-ZwVR1qHs7WOoZEfLEhCMfKToo_NgHaxj8jyFAJ8L4Hxen4sOFAa1ApyO6DMuuhD1VLL4T3PqZjy_gSduc846Sr8XDWFmI2mn1eYcmgpH9vtMHipDjeTCk2Dx1YPixRlT7O2tj6kzCwTR4kh2_R9rQB3I_Op7gDOK3JlzNL3ysWYpIDbsTTuudfVih2ZhqLK93_wukMWx8fb1jSkxK7U86XcvGcJ-jRtDe9A'
    # print(is_teacher(token))
    print(get_user_info(token))
    
