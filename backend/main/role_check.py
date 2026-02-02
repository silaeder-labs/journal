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
    token = 'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJvcTJ3cXlkSUtXa3ZDUUgzVXBPQUZxeDV2c295MUMyazZzckJ6R3pzSGVRIn0.eyJleHAiOjE3NzAwNTc1ODMsImlhdCI6MTc3MDA1NzI4MywiYXV0aF90aW1lIjoxNzcwMDU3MjgzLCJqdGkiOiJvbnJ0YWM6YWJlYmFmZGQtYzY0Ni04MjA0LTMzZDYtZWI2MTY0YzVlMjM1IiwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDo4MDgwL3JlYWxtcy9teXJlYWxtIiwiYXVkIjoiYWNjb3VudCIsInN1YiI6ImU1ODViY2JhLWNhYmUtNGI5Mi1iZGFmLTdhMjI4MmUzYTM3ZSIsInR5cCI6IkJlYXJlciIsImF6cCI6Im15YXBwIiwic2lkIjoiQ0g2a3NQSWlqQ19VTUFRZWVMU2wxRlQwIiwiYWNyIjoiMSIsImFsbG93ZWQtb3JpZ2lucyI6WyIvKiJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiZGVmYXVsdC1yb2xlcy1teXJlYWxtIiwib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIGVtYWlsIHByb2ZpbGUiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsIm5hbWUiOiJmaXJzdE5hbWUgbGFzdE5hbWUiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJ1c2VybmFtZSIsIm1pZGRsZV9uYW1lIjoibWlkZGxlIE5hbWUiLCJnaXZlbl9uYW1lIjoiZmlyc3ROYW1lIiwiZmFtaWx5X25hbWUiOiJsYXN0TmFtZSIsImNsYXNzIjo5LCJlbWFpbCI6ImVtYWlsQGV4YW1wbGUuY29tIn0.oFB4nLiveUssxk3eLWhTC63FZRUfIVyehcqWlBwiByf5V5rbNBibDb1Ye3wO2yxdNJ9JUtWiiBsdsNVBINZf_bIw0VtgWS67IGlSsQZj5nPDr4fRmHa8p7ZX-fagZWuXqMOCvOK_nSgMvPgvcPAjRMfICsc_xPLUY5ckfcVQGa2lLDPz_TtWeIhXtg0j1W4b0SkYpooTaoT0VgWe-hgSOUiRnu3OheJKEWHqsrAWnt9W-v2ZtR-7cKIWnE577conN2EtinEwD6qDilz30bK55taRIhni_njo33gslvROJOWCmYJkWxejCVeHjmd40MBLw9f3dgv2ybLZnBXCFfz7zw'
    print(is_teacher(token))
    
