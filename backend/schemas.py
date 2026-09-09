from typing import Optional
from datetime import time
from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str

    class Config:
        from_attributes = True


class IncidentCreate(BaseModel):
    type: str
    description: Optional[str] = None
    latitude: float
    longitude: float
    severity: str
    status: Optional[str] = "ACTIVE"
    created_by: Optional[int] = None


class IncidentResponse(BaseModel):
    id: int
    type: str
    description: Optional[str]
    latitude: float
    longitude: float
    severity: str
    status: str

    class Config:
        from_attributes = True


class SafetyZoneCreate(BaseModel):
    name: str
    latitude: float
    longitude: float
    radius: int
    zone_type: str
    severity: str
    status: Optional[str] = "ACTIVE"
    incident_id: Optional[int] = None


class RestrictionCreate(BaseModel):
    zone_id: int
    action: str
    start_time: str
    end_time: str
    status: Optional[str] = "ACTIVE"
    created_by: Optional[int] = None

class RestrictionServiceCreate(BaseModel):
    restriction_id: int
    service: str  

class AlertCreate(BaseModel):
    user_id: int
    zone_id: Optional[int] = None
    message: str
    alert_type: str
    status: Optional[str] = "UNREAD"      

class EmergencyUnitCreate(BaseModel):
    type: str
    unit_name: str
    latitude: float
    longitude: float
    status: Optional[str] = "AVAILABLE"    

class WorkerLocationCreate(BaseModel):
    worker_id: int
    latitude: float
    longitude: float    

class CitizenReportCreate(BaseModel):
    user_id: int
    description: str
    latitude: float
    longitude: float
    image_url: Optional[str] = None
    status: Optional[str] = "PENDING"    

class AuditLogCreate(BaseModel):
    user_id: int
    action: str
    entity_type: str
    entity_id: Optional[int] = None    

class SafetyZoneResponse(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
    radius: int
    zone_type: str
    severity: str
    status: str
    incident_id: Optional[int] = None

    class Config:
        from_attributes = True


class RestrictionResponse(BaseModel):
    id: int
    zone_id: int
    action: str
    start_time: time
    end_time: time
    status: str
    created_by: Optional[int] = None

    class Config:
        from_attributes = True


class IncidentWorkflowResponse(BaseModel):
    incident: IncidentResponse
    decision: dict
    safety_zone: SafetyZoneResponse
    restriction: RestrictionResponse    
    nearest_emergency_units: list
    deployment_recommendation: list
    deployment_status: str