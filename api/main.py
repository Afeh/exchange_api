import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func
from .image_generator import IMAGE_PATH

from . import models, schemas, services
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/countries/refresh")
def refresh_data(db: Session = Depends(get_db)):
    try:
        result = services.refresh_countries_data(db)
        return JSONResponse(status_code=200, content=result)
    except services.ExternalServiceError as e:
        raise HTTPException(
            status_code=503,
            detail={"error": "External data source unavailable", "details": str(e)}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "Internal server error", "details": str(e)})


@app.get("/countries", response_model=List[schemas.CountryResponse])
def get_countries(
    region: Optional[str] = None,
    currency: Optional[str] = None,
    sort: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Country)
    if region:
        query = query.filter(models.Country.region == region)
    if currency:
        query = query.filter(models.Country.currency_code == currency)
    if sort == "gdp_desc":
        query = query.order_by(models.Country.estimated_gdp.desc())
    
    countries = query.all()
    return countries


@app.get("/countries/{name}", response_model=schemas.CountryResponse)
def get_country_by_name(name: str, db: Session = Depends(get_db)):
    country = db.query(models.Country).filter(func.lower(models.Country.name) == name.lower()).first()
    if not country:
        raise HTTPException(status_code=404, detail={"error": "Country not found"})
    return country


@app.delete("/countries/{name}", status_code=204)
def delete_country_by_name(name: str, db: Session = Depends(get_db)):
    country = db.query(models.Country).filter(func.lower(models.Country.name) == name.lower()).first()
    if not country:
        raise HTTPException(status_code=404, detail={"error": "Country not found"})
    db.delete(country)
    db.commit()
    return


@app.get("/status", response_model=schemas.StatusResponse)
def get_status(db: Session = Depends(get_db)):
    total_countries = db.query(models.Country).count()
    status = db.query(models.AppStatus).first()
    return {
        "total_countries": total_countries,
        "last_refreshed_at": status.last_refreshed_at if status else None
    }

@app.get("/countries/image")
def get_summary_image():
    if not os.path.exists(IMAGE_PATH):
        raise HTTPException(status_code=404, detail={"error": "Summary image not found"})
    return FileResponse(IMAGE_PATH, media_type="image/png")