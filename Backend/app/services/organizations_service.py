from fastapi import HTTPException,status
from app.db.database import get_db
from sqlalchemy import func,desc,asc
from app.model.miscellaneous import Miscellaneous
from app.model.user import User
from sqlalchemy.orm import Session
from app.model.organizations import Organizations
from app.schemas.organizations_schema import OrganizationCreate,OrganizationUpdate,StatusUpdate
from datetime import datetime
import bcrypt
from typing import Optional ,List,Dict
from sqlalchemy.exc import IntegrityError,SQLAlchemyError
from app.model.roles import Roles
from app.model.user import User 
from app.model.miscellaneous import Miscellaneous
from app.services.email_service import EmailService
import secrets
import string ,os




def generate_password(length=12):
    """Generate a secure random password."""
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

def create_organization(db: Session, organization: OrganizationCreate):
    try:
        # Fetch the ID for 'inactive' status
        inactive_status_id = db.query(Miscellaneous.miscellaneous_id).filter(Miscellaneous.value == 'inactive').scalar()
        
        # Create the organization entry
        db_organization = Organizations(
            organization_iD=organization.organization_iD,
            org_name=organization.org_name,
            status=inactive_status_id,
            email=organization.email,
            created_by_id=organization.created_by_id,
            created=organization.created or datetime.utcnow(),
        )

        # Add and commit the organization to the database
        db.add(db_organization)
        db.commit()
        db.refresh(db_organization)

        # Fetch the organization ID
        org_id = db_organization.org_id
        
        # Fetch the ID for 'admin' role
        admin_role_id = db.query(Roles.role_id).filter(Roles.role_name == 'admin').scalar()

        # Create the user entry
        db_user = User(
            username=organization.username,
            email=organization.email,
            phone_number=organization.phone_number,
            role_id=admin_role_id,
            org_id=org_id,
            status=inactive_status_id,
            created_by_id=organization.created_by_id or org_id,
            created=datetime.utcnow(),
        )

        # Add and commit the user to the database
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return {
            "message": "Organization and user created successfully"
        }
        
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Integrity Error: {str(e.orig)}")
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database Error: {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected Error: {str(e)}")



def get_organization(db: Session, org_id: int) -> dict:
    # Fetch the organization
    try:
        db_organization = db.query(Organizations).filter(Organizations.org_id == org_id).first()
        if db_organization is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
        
        # Fetch the related user data
        db_user = db.query(User).filter(User.org_id == org_id).first()
        
        # Prepare the response data
        response = {
            "org_id": db_organization.org_id,
            "organization_iD": db_organization.organization_iD,
            "org_name": db_organization.org_name,
            "username": db_user.username if db_user else None,
            "email": db_user.email if db_user else db_organization.email,
            "password":db_user.password,
            "phone_number": db_user.phone_number if db_user else None,
            "role_id": db_user.role_id if db_user else None,
            "status": db_organization.status,
            "created_by_id": db_organization.created_by_id,
            "updated_by_id": db_user.created_by_id if db_user else db_organization.updated_by_id,
            "created": db_organization.created,
            "updated": db_organization.updated
        }
        
        return response 
    except SQLAlchemyError as e:
            # Handle SQLAlchemy-related errors
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database Error: {str(e)}")
        
 

def get_all_organizations(db: Session) -> List[Dict]:
    try:
        db_organizations = db.query(Organizations).all()
        responses = []

        # Fetch all users in a single query to avoid N+1 query issue
        user_ids = [org.org_id for org in db_organizations]
        db_users = db.query(User).filter(User.org_id.in_(user_ids)).all()
        user_dict = {user.org_id: user for user in db_users}

        for db_organization in db_organizations:
            db_user = user_dict.get(db_organization.org_id, None)
            
            response = {
                "org_id": db_organization.org_id,
                "organization_iD": db_organization.organization_iD,
                "org_name": db_organization.org_name,
                "username": db_user.username if db_user else None,
                "email": db_user.email if db_user else db_organization.email,
                "password": db_user.password if db_user else None,
                "phone_number": db_user.phone_number if db_user else None,
                "role_id": db_user.role_id if db_user else None,
                "status": db_organization.status,
                "created_by_id": db_organization.created_by_id,
                "updated_by_id": db_user.created_by_id if db_user else db_organization.updated_by_id,
                "created": db_organization.created,
                "updated": db_organization.updated
            }
            responses.append(response)
    
        return responses
    except SQLAlchemyError as e:
        # Handle SQLAlchemy-related errors
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database Error: {str(e)}")
    

def get_organization_by_email(db: Session,email:str)->Optional[Organizations]:
    return db.query(Organizations).filter(Organizations.email==email).first()

def check_role_exists(db: Session, role_id: int) -> bool:
    return db.query(Roles).filter(Roles.role_id == role_id).first() is not None

def check_user_exists(db: Session, user_id: int) -> bool:
    return db.query(User).filter(User.user_id == user_id).first() is not None

def check_miscellaneous_exists(db: Session, status_id: int) -> bool:
    return db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id == status_id).first() is not None


def update_organization(db: Session, org_id: int, organization_update: OrganizationUpdate):
    # Fetch the organization
    db_organization = db.query(Organizations).filter(Organizations.org_id == org_id).first()
    if db_organization is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")

    # Update the organization fields
    for field, value in organization_update.dict(exclude_unset=True).items():
        setattr(db_organization, field, value)

    # Fetch the related user if necessary
    if organization_update.username or organization_update.email or organization_update.phone_number:
        db_user = db.query(User).filter(User.org_id == org_id).first()
        if db_user:
            if organization_update.username:
                db_user.username = organization_update.username
            if organization_update.email:
                db_user.email = organization_update.email
            if organization_update.phone_number:
                db_user.phone_number = organization_update.phone_number
            if organization_update.updated_by_id:
                db_user.updated_by_id = organization_update.updated_by_id
            if organization_update.updated:
                db_user.updated = organization_update.updated

            try:
                db.add(db_user)
                db.commit()
                db.refresh(db_user)
            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error updating user: {str(e)}")

    try:
        db.add(db_organization)
        db.commit()
        db.refresh(db_organization)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error updating organization: {str(e)}")

    return db_organization


def status_update(db: Session, org_id: int, data: StatusUpdate):
    # Fetch the organization and its current status
    organization = db.query(Organizations).filter(Organizations.org_id == org_id).first()
    if not organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")

    current_status_id = organization.status

    # Fetch the current status type from the Miscellaneous table
    current_status = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id == current_status_id).first()
    if not current_status:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Current status not found in Miscellaneous table")

    # Fetch the new status type from the Miscellaneous table based on the data.status
    new_status = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id == data.status).first()
    if not new_status:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="New status not found in Miscellaneous table")

    # Update the status only if the new status is different
    if current_status.miscellaneous_id != data.status:
        # Check if the current status is inactive and the new status is active
        if current_status.value == 'inactive' and new_status.value == 'active':
            if not organization.email_sent:
                # Generate and hash a new password
                generated_password = generate_password()
                hashed_password = bcrypt.hashpw(generated_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

                # Proceed with updating the status to active
                organization.status = data.status
                organization.email_sent = True  # Mark email as sent
                if data.updated_by_id is not None:
                    organization.updated_by_id = data.updated_by_id
                if data.updated is not None:
                    organization.updated = data.updated

                # Commit the changes to the organization table
                try:
                    db.commit()
                    db.refresh(organization)
                except Exception as e:
                    db.rollback()
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error updating organization: {str(e)}")

                # Update the User table with the new password and same status
                db_user = db.query(User).filter(User.org_id == org_id).first()
                if db_user:
                    db_user.status = data.status
                    if data.updated_by_id is not None:
                        db_user.updated_by_id = data.updated_by_id
                    if data.updated is not None:
                        db_user.updated = data.updated

                    db_user.password = hashed_password  # Set new hashed password

                    try:
                        db.commit()
                        db.refresh(db_user)
                    except Exception as e:
                        db.rollback()
                        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error updating user: {str(e)}")

                    # Prepare and send the email
                    email_service = EmailService()
                    subject = "Your Organization's Status has been Updated"
                    body = f"""
                    Dear {db_user.email},

                    The status of your organization has been successfully updated to active.

                    Please log in with the following details:

                    Username: {db_user.email}
                    Password: {generated_password}
                    """

                    try:
                        email_service.send_email(organization.email, subject, body)
                    except Exception as e:
                        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error sending email: {str(e)}")

            else:
                # If email has already been sent, just update the status without changing the password
                organization.status = data.status
                if data.updated_by_id is not None:
                    organization.updated_by_id = data.updated_by_id
                if data.updated is not None:
                    organization.updated = data.updated

                # Commit the changes to the organization table
                try:
                    db.commit()
                    db.refresh(organization)
                except Exception as e:
                    db.rollback()
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error updating organization: {str(e)}")

                # Update the User table with the same status
                db_user = db.query(User).filter(User.org_id == org_id).first()
                if db_user:
                    db_user.status = data.status
                    if data.updated_by_id is not None:
                        db_user.updated_by_id = data.updated_by_id
                    if data.updated is not None:
                        db_user.updated = data.updated

                    try:
                        db.commit()
                        db.refresh(db_user)
                    except Exception as e:
                        db.rollback()
                        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error updating user: {str(e)}")

        else:
            # Handle status updates that do not require sending an email
            organization.status = data.status
            if data.updated_by_id is not None:
                organization.updated_by_id = data.updated_by_id
            if data.updated is not None:
                organization.updated = data.updated

            # Commit the changes to the organization table
            try:
                db.commit()
                db.refresh(organization)
            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error updating organization: {str(e)}")

            # Update the User table with the same status
            db_user = db.query(User).filter(User.org_id == org_id).first()
            if db_user:
                db_user.status = data.status
                if data.updated_by_id is not None:
                    db_user.updated_by_id = data.updated_by_id
                if data.updated is not None:
                    db_user.updated = data.updated

                try:
                    db.commit()
                    db.refresh(db_user)
                except Exception as e:
                    db.rollback()
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error updating user: {str(e)}")

    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Status is the same as current status")

    return {"detail": "Updated successfully"}
