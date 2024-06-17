from fastapi import FastAPI, HTTPException, Depends, status, Request
from pydantic import BaseModel
from typing import Annotated
import models
import schemas
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import select
from collections import defaultdict
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/add-pu", response_class = HTMLResponse)
async def index(request:Request):
    return templates.TemplateResponse("add_polling_unit.html", {"request": request})



@app.get("/result/polling_unit")
async def get_polling_unit(db:db_dependency):
    result = db.query(models.PollingUnit).all()
    return result

@app.get("/result/announced_pu_result")
async def get_pu_announced_result(request: Request,db:db_dependency):
    
    results = db.query(models.AnnouncedPUResult).all()

    grouped_data = defaultdict(list)


    for result in results:
        
        polling_unit_id = result.polling_unit_uniqueid
        party_abbreviation = result.party_abbreviation
        party_score = result.party_score
    
        grouped_data[polling_unit_id].append({"party_abbreviation": party_abbreviation, "party_score": party_score})

    
    grouped_data = dict(grouped_data)
    return templates.TemplateResponse("individual-polling-unit.html", {"request": request, "grouped_data": grouped_data})
   

@app.get("/result/agent_name")
async def get_agent_name(db:db_dependency):
    result = db.query(models.AgentName).all()
    return result


@app.get("/result/individual_polling_unit/{polling_unit_uniqueid}")
async def get_individual_polling_unit_result(polling_unit_uniqueid: int, db:db_dependency):
    polling_unit = db.query(models.PollingUnit).filter(models.PollingUnit.uniqueid == polling_unit_uniqueid).first()
    if not polling_unit:
        raise HTTPException(status_code=404, detail="Polling Unit not found")

    # Fetch party results for the polling unit
    party_results = db.query(models.AnnouncedPUResult)\
                      .filter(models.AnnouncedPUResult.polling_unit_uniqueid == polling_unit_uniqueid)\
                      .all()

    # Prepare response data
    results = []
    for result in party_results:
        results.append({
            "party_abbreviation": result.party_abbreviation,
            "party_score": result.party_score
        })

    return {"polling_unit_uniqueid": polling_unit_uniqueid, "results": results}


@app.get("/lgas/all")
async def get_all_lgas(db:db_dependency):
    lgas = db.query(models.LGA).all()
    return lgas

@app.get("/lga/{lga_id}/polling_unit")
async def get_lga_polling_unit(lga_id:int, db:db_dependency):
    polling_units = db.query(models.PollingUnit).filter(models.PollingUnit.lga_id == lga_id).all()
    return polling_units


@app.get("/lga/{lga_id}/result")
async def get_lga_result(lga_id: int, db: Session = Depends(get_db)):
    polling_units = db.query(models.PollingUnit).filter(models.PollingUnit.lga_id == lga_id).all()
    print(polling_units)
    lga_result = defaultdict(int)
    if len(polling_units) == 0:
        return {"lga_id": lga_id, "results": {}, "empty": True}
        
    for polling_unit in polling_units:
        party_results = db.query(models.AnnouncedPUResult)\
                      .filter(models.AnnouncedPUResult.polling_unit_uniqueid == polling_unit.uniqueid)\
                      .all()
        for result in party_results:
            lga_result[result.party_abbreviation] += result.party_score

    return {"lga_id": lga_id, "results": dict(lga_result), "empty": False}

@app.get("/lga/results", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("summed-lga-results.html", {"request": request})



# Endpoint to store results for all parties for a new polling unit
@app.post("/result/new_polling_unit")
async def store_new_polling_unit_result(
    result: schemas.NewPollingUnitResult,
    db: Session = Depends(get_db)
):

    try:
        # Create a new instance of AnnouncedPUResult model
        new_results = []
        for party_result in result.party_results:
            new_result = models.AnnouncedPUResult(
                polling_unit_uniqueid=result.polling_unit_uniqueid,
                party_abbreviation=party_result.party_abbreviation,
                party_score=party_result.party_score,
                entered_by_user = result.user_name
            )
            db.add(new_result)
            db.commit()
            db.refresh(new_result)
            new_results.append(new_result)
        
        return new_results
    
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

