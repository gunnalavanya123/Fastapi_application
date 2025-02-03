from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.model.organizations import Organizations
from app.schemas.organizations_schema import OrganizationCreate
from app.services.organizations_service import create_organization,get_organization,get_all_organizations,update_organization,get_organization_by_email,check_user_exists,status_update
from typing import List,Optional,Dict
from app.schemas.organizations_schema import OrganizationUpdate,StatusUpdate




router = APIRouter()


@router.post("/organizations/",status_code=status.HTTP_201_CREATED)
def create_organization_endpoint(organization: OrganizationCreate,db: Session = Depends(get_db)):

    db_organization = get_organization_by_email(db=db, email=organization.email)
    if db_organization:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email already exists")
    
    if organization.created_by_id and not check_user_exists(db, organization.created_by_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Created By ID does not exist in user table")

        
    return create_organization(db=db, organization=organization)
     
    


@router.get("/organizations/{org_id}", response_model=Dict)
def read_organization(org_id: int, db: Session = Depends(get_db)):
    return get_organization(db=db, org_id=org_id)

@router.get("/organizations", response_model=List[Dict])
def get_all_organizations_route(db: Session = Depends(get_db)):
    return get_all_organizations(db)

@router.put("/organizations/{org_id}", response_model=OrganizationUpdate)
def update_organization_endpoint(
    org_id: int,
    organization_update: OrganizationUpdate,
    db: Session = Depends(get_db)
):
    
    if organization_update.updated_by_id and not check_user_exists(db, organization_update.updated_by_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Updated By ID does not exist in User table")

    try:
        updated_organization = update_organization(db=db, org_id=org_id, organization_update=organization_update)
        return updated_organization 
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/update-status/{id}")
def update_user_status(id: int, data: StatusUpdate, db: Session = Depends(get_db)):
    try:
        message = status_update(db, id, data)
        return message
    except HTTPException as e:
        raise e


