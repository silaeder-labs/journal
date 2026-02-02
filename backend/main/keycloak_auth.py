from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from keycloak import KeycloakOpenID
import psycopg2
import jwt

KEYCLOAK_URL = "http://localhost:8080"
REALM = "myrealm"
CLIENT_ID = "myapp"

keycloak_openid = KeycloakOpenID(
    server_url=KEYCLOAK_URL,
    client_id=CLIENT_ID,
    realm_name=REALM
)

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/auth",
    tokenUrl=f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/token"
)

def get_db():
    conn = psycopg2.connect(
        user="test_superuser",
        password="passwords",
        host="127.0.0.1",
        port="5432",
        database="marks"
    )
    try:
        yield conn
    finally:
        conn.close()

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        return keycloak_openid.decode_token(token, validate=True)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

def upsert_user(user_info: dict, conn):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (id, keycloack_user_id, first_name, last_name, middle_name, class)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (keycloack_user_id) DO UPDATE SET
            first_name = EXCLUDED.first_name,
            last_name = EXCLUDED.last_name
    """, (
        hash(user_info['sub']) % 2147483647,
        user_info['sub'],
        user_info.get('given_name', ''),
        user_info.get('family_name', ''),
        user_info.get('middle_name', ''),
        user_info.get('class', '')
    ))
    conn.commit()
    cursor.close()

async def get_current_user(token: str = Depends(oauth2_scheme), conn = Depends(get_db)):
    user_info = verify_token(token)
    upsert_user(user_info, conn)
    return user_info
