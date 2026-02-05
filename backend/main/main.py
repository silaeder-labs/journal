import os
import sys
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import get_database as gt
import database_api as db_api
import keycloak_auth as auth
from set_mesh_id import set_mesh_id_to_database
from config import URL

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from database.config import get_connection

# === Models ===

class TextIn(BaseModel):
    text: str

# === App Setup ===

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

base_path = os.path.dirname(os.path.abspath(__file__))
frontend_path = os.path.abspath(os.path.join(base_path, "..", "..", "frontend"))

app.mount("/static", StaticFiles(directory=frontend_path), name="static")

# === HTML Pages ===

@app.get("/")
def root():
    return FileResponse(os.path.join(frontend_path, "auth", "index.html"))

@app.get("/auth")
def auth_page():
    return FileResponse(os.path.join(frontend_path, "auth", "index.html"))

@app.get("/statistic")
def statistic_page():
    return FileResponse(os.path.join(frontend_path, "subjects", "statistic", "index.html"))

@app.get("/statistic-me")
def statistic_me_page():
    return FileResponse(os.path.join(frontend_path, "subjects", "statistic-me", "index.html"))

@app.get("/user/{user_id}")
def user_page(user_id: str):
    return FileResponse(os.path.join(frontend_path, "user", "index.html"))

@app.get("/users")
def users_page():
    return FileResponse(os.path.join(frontend_path, "users", "index.html"))

@app.get("/set-mesh-id")
def set_mesh_id_page():
    return FileResponse(os.path.join(frontend_path, "set_mesh_id", "index.html"))

@app.get("/skills")
def skills_page():
    return FileResponse(os.path.join(frontend_path, "skills", "index.html"))

# === Auth Endpoints ===

@app.get("/api/login")
def login():
    return {"auth_url": f"{auth.KEYCLOAK_URL}/realms/{auth.REALM}/protocol/openid-connect/auth?client_id={auth.CLIENT_ID}&redirect_uri={URL}/api/callback&response_type=code&scope=openid"}

@app.get("/api/callback")
def callback(code: str):
    try:
        token = auth.keycloak_openid.token(
            grant_type='authorization_code',
            code=code,
            redirect_uri=f"{URL}/api/callback"
        )
        user_info = auth.keycloak_openid.decode_token(token['access_token'], validate=True)
        conn = get_connection()
        auth.upsert_user(user_info, conn)
        conn.close()
        return RedirectResponse(url=f"/auth?access_token={token['access_token']}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Auth failed: {str(e)}")

# === API Endpoints ===

# == Marks ==
@app.post("/api/user-average-marks-by-user-id")
def get_user_average_marks_by_mesh_id(data: TextIn, user = Depends(auth.get_current_user)):
    return {"marks": db_api.get_student_marks_by_mesh_id(db_api.convert_from_normal_id_to_mesh_id(int(data.text)))}

@app.post("/api/user-average-marks-by-mesh-id")
def get_user_average_marks_by_mesh_id(data: TextIn, user = Depends(auth.get_current_user)):
    return {"marks": db_api.get_student_marks_by_mesh_id(data.text)}

@app.post("/api/user-average-marks-by-token-mesh-id")
def get_user_marks_without_id(user = Depends(auth.get_current_user)):
    return {"marks": db_api.get_student_marks_by_mesh_id(user["mesh_id"])}

# == Columns ==

@app.post("/api/table-columns-by-table-name")
def get_table_columns_by_table_name(data: TextIn, user = Depends(auth.get_current_user)):
    return {"columns": db_api.get_table_columns(data.text)}

# == Users ==

@app.get("/api/all-users-info")
def get_all_users_info(user = Depends(auth.get_current_user)):
    return {"users_info": db_api.get_all_students_info()}

# == Skills ==

@app.get("/api/user-skills-by-user-id")
def get_all_users_info(user = Depends(auth.get_current_user)):
    return {"skills": db_api.get_student_skills_by_id(db_api.convert_from_mesh_id_to_normal_id(user["mesh_id"]))}



@app.post("/api/average_marks_by_id")
def get_average_marks_by_id(data: TextIn, user = Depends(auth.get_current_user)):
    return {"result": gt.get_results_by_user_id(data.text, "average_marks")}

@app.post("/api/skills_by_id")
def get_skills_by_user_id(user = Depends(auth.get_current_user)):
    return {"result": gt.get_results_by_user_id(gt.get_mesh_id_by_keycloak_id(user["sub"]), "skills")}

@app.get("/api/average_marks_columns")
def get_average_marks_columns(user = Depends(auth.get_current_user)):
    return gt.get_columns_in_database("average_marks")

@app.get("/api/skills_columns")
def get_average_marks_columns(user = Depends(auth.get_current_user)):
    return gt.get_columns_in_database("skills")

@app.get("/api/get-users")
def get_users(user = Depends(auth.get_current_user)):
    return gt.get_all_users()

@app.post("/api/set-mesh-id")
def set_mesh_id(data: TextIn, user = Depends(auth.get_current_user)):
    set_mesh_id_to_database(data.text, user["sub"])
    return {"success": True}
