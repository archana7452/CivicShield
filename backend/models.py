from sqlalchemy import Column, Integer, String, Text, DECIMAL, DateTime, Time
from backend.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(30), nullable=False)
    created_at = Column(DateTime, nullable=True)
    
class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    latitude = Column(DECIMAL(10, 7), nullable=False)
    longitude = Column(DECIMAL(10, 7), nullable=False)
    severity = Column(String(20), nullable=False)
    status = Column(String(20), default="ACTIVE")
    created_by = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=True)

class SafetyZone(Base):
    __tablename__ = "safety_zones"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    latitude = Column(DECIMAL(10, 7), nullable=False)
    longitude = Column(DECIMAL(10, 7), nullable=False)
    radius = Column(Integer, nullable=False)
    zone_type = Column(String(30), nullable=False)
    severity = Column(String(20), nullable=False)
    status = Column(String(20), default="ACTIVE")
    incident_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=True) 

class Restriction(Base):
    __tablename__ = "restrictions"

    id = Column(Integer, primary_key=True, index=True)
    zone_id = Column(Integer, nullable=False)
    action = Column(String(20), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    status = Column(String(20), default="ACTIVE")
    created_by = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=True)       

class RestrictionService(Base):
    __tablename__ = "restriction_services"

    id = Column(Integer, primary_key=True, index=True)
    restriction_id = Column(Integer, nullable=False)
    service = Column(String(50), nullable=False)    

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    zone_id = Column(Integer, nullable=True)
    message = Column(Text, nullable=False)
    alert_type = Column(String(50), nullable=False)
    status = Column(String(20), default="UNREAD")
    created_at = Column(DateTime, nullable=True)    

class EmergencyUnit(Base):
    __tablename__ = "emergency_units"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(30), nullable=False)
    unit_name = Column(String(100), nullable=False)
    latitude = Column(DECIMAL(10, 7), nullable=False)
    longitude = Column(DECIMAL(10, 7), nullable=False)
    status = Column(String(30), default="AVAILABLE")
    created_at = Column(DateTime, nullable=True)  

class WorkerLocation(Base):
    __tablename__ = "worker_locations"

    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, nullable=False)
    latitude = Column(DECIMAL(10, 7), nullable=False)
    longitude = Column(DECIMAL(10, 7), nullable=False)
    recorded_at = Column(DateTime, nullable=True)    

class CitizenReport(Base):
    __tablename__ = "citizen_reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    latitude = Column(DECIMAL(10, 7), nullable=False)
    longitude = Column(DECIMAL(10, 7), nullable=False)
    image_url = Column(String(255), nullable=True)
    status = Column(String(20), default="PENDING")
    created_at = Column(DateTime, nullable=True)    

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    action = Column(String(100), nullable=False)
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=True)    