from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, FileResponse
import koco_product_sqlmodel.fastapi.routes.catalog as rcat
import koco_product_sqlmodel.fastapi.routes.product_group as rpg
import koco_product_sqlmodel.fastapi.routes.family as rfam
import koco_product_sqlmodel.fastapi.routes.article as rart
import koco_product_sqlmodel.fastapi.routes.security as rsec

DESCRIPTION_STRING="""
API to KOCO MOTION Product database. Under heavy construction. 
"""

tags_metadata = [
    {"name": "Endpoints to CATALOG-data", "description":"Catalogs are collections of product groups of a distinct supplier."},
    {"name": "Endpoints to PRODUCT GROUP-data", "description":"Product groups are collections of families of articles."},
    {"name": "Endpoints to FAMILY-data", "description":"Families collect articles belonging to an article-family. They contain also additional information like description, or familiy spectables."},
    {"name": "Endpoints to ARTICLE-data", "description":"Articles collect all specifications of an article as spectables. They contain also additional information like description, urls to spec-data..."},
    {"name": "Endpoints to AUTHENTICATION data and methods", "description":"Almost all endpoints are protected and need authorization"},
    {"name": "ROOT", "description":"Redirect to static html data"},
]

app = FastAPI(
    version="0.0.3", 
    title="koco_product_api",
    description=DESCRIPTION_STRING,
    openapi_tags=tags_metadata,
)
app.mount(path="/static", app=StaticFiles(directory="src/koco_product_sqlmodel/fastapi/static"), name="static")
FAVICON_PATH="src/koco_product_sqlmodel/fastapi/static/img/favicon.ico"

app.include_router(rcat.router, prefix="/catalogs")
app.include_router(rpg.router, prefix="/product_groups")
app.include_router(rfam.router, prefix="/families")
app.include_router(rart.router, prefix="/articles")
app.include_router(rsec.router, prefix="/auth")

@app.get("/", tags=["ROOT"])
async def read_root():
    return RedirectResponse(url="/static/html/index.html")

@app.get("/favicon.ico",  include_in_schema=False)
async def serve_favicon():
    return FileResponse(path=FAVICON_PATH)

def main():
    pass

if __name__=="__main__":
    main()