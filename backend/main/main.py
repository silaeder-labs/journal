import os
from fastapi import FastAPI, Depends
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import get_database as gt
import keycloak_auth as auth
from set_mesh_id import set_mesh_id_to_database

app = FastAPI()

base_path = os.path.dirname(os.path.abspath(__file__))
frontend_path = os.path.abspath(os.path.join(base_path, "..", "..", "frontend"))

app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
def root():
    return FileResponse(os.path.join(frontend_path, "auth", "index.html"))

@app.get("/statistic")
def get_statistic_page():
    html_file = os.path.join(frontend_path, "subjects", "statistic", "index.html")
    return FileResponse(html_file)

@app.get("/statistic-me")
def get_statistic_page():
    html_file = os.path.join(frontend_path, "subjects", "statisticme", "index.html")
    return FileResponse(html_file)

@app.get("/users")
def get_statistic_page():
    html_file = os.path.join(frontend_path, "subjects", "users", "index.html")
    return FileResponse(html_file)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/set-mesh-id")
def get_statistic_page():
    html_file = os.path.join(frontend_path, "set_mesh_id", "index.html")
    return FileResponse(html_file)

@app.get("/api/hello")
def hello(user = Depends(auth.get_current_user)):
    return {"message": "Привет от FastAPI 🚀", "user": user['preferred_username']}

class TextIn(BaseModel):
    text: str

@app.post("/api/user_marks") #af73452e-bbbb-443d-83a2-423f78cd003e
def reverse_text(data: TextIn, user = Depends(auth.get_current_user)):
    return {"result": gt.get_results_by_user_id(data.text)}

@app.post("/api/user_marks_without_id")
def reverse_text(user = Depends(auth.get_current_user)):
    return {"result": gt.get_results_by_user_id(str(user["mesh_id"]))}

@app.get("/api/columns")
def get_columns(user = Depends(auth.get_current_user)):
    return gt.get_columns_in_database()

@app.get("/api/get-users")
def get_columns(user = Depends(auth.get_current_user)):
    return gt.get_all_users()

@app.get("/api/login")
def login():
    return {"auth_url": f"{auth.KEYCLOAK_URL}/realms/{auth.REALM}/protocol/openid-connect/auth?client_id={auth.CLIENT_ID}&redirect_uri=http://localhost:8000/api/callback&response_type=code&scope=openid"}

@app.post("/api/set-mesh-id")
def set_mesh_id(data: TextIn, user = Depends(auth.get_current_user)):
    set_mesh_id_to_database(data.text, user["sub"])

@app.get("/api/callback")
def callback(code: str):
    from fastapi.responses import RedirectResponse
    import psycopg2
    token = auth.keycloak_openid.token(
        grant_type='authorization_code',
        code=code,
        redirect_uri='http://localhost:8000/api/callback'
    )
    user_info = auth.keycloak_openid.decode_token(token['access_token'], validate=True)
    conn = psycopg2.connect(user="test_superuser", password="passwords", host="127.0.0.1", port="5432", database="marks")
    auth.upsert_user(user_info, conn)
    conn.close()
    return RedirectResponse(url=f"/auth?access_token={token['access_token']}")

@app.get("/auth")
def auth_page():
    return FileResponse(os.path.join(frontend_path, "auth", "index.html"))
