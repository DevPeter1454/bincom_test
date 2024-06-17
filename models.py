from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import UTC, datetime



class PollingUnit(Base):
    __tablename__ = "polling_unit"
    uniqueid:Mapped[int] = mapped_column(Integer, primary_key=True)
    ward_id:Mapped[int] = mapped_column(Integer)
    lga_id:Mapped[int] = mapped_column(Integer)
    polling_unit_name:Mapped[str] = Column(String)

    # ward = relationship("Ward", back_populates="polling_units")

class Ward(Base):
    __tablename__ = "ward"
    ward_id:Mapped[int] = mapped_column(Integer)
    uniqueid:Mapped[int] = mapped_column(Integer, primary_key=True)

    ward_name:Mapped[str] = mapped_column(String)
    lga_id:Mapped[int] = mapped_column(Integer)

    # lga = relationship("LGA", back_populates="wards")

class LGA(Base):
    __tablename__ = "lga"
    lga_id:Mapped[int] = mapped_column(Integer)
    lga_name:Mapped[str] = mapped_column(String(50))
    uniqueid:Mapped[int] = mapped_column(Integer, primary_key=True)

    state_id:Mapped[int] = mapped_column(Integer, ForeignKey('state.state_id'))


# class AnnouncedLGAResult(Base):
#     __tablename__ = "announced_lga_results"
#     result_id: int = sa.field(init=False, default=None)
#     lga_id: int = sa.field(init=False, default=None)
#     party_abbreviation: str = sa.field(init=False, default=None)
#     party_score: int = sa.field(init=False, default=None)

#     result_id = Column(Integer, primary_key=True)
#     lga_id = Column(Integer)
#     party_abbreviation = Column(String)
#     party_score = Column(Integer)

class AnnouncedPUResult(Base):
    __tablename__ = "announced_pu_results"

    result_id: Mapped[int] = mapped_column(
        "result_id", autoincrement=True, nullable=False, unique=True, primary_key=True, init=False)

    entered_by_user: Mapped[str] = mapped_column(String)
    

    polling_unit_uniqueid: Mapped[str] = mapped_column(String(50))
    party_abbreviation: Mapped[str] = mapped_column(String(4))

    party_score: Mapped[str] = mapped_column(Integer)

    date_entered: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))


class AgentName(Base):
    __tablename__ = "agentname"
    email:Mapped[str] = Column(String(255))
    firstname:Mapped[str] = Column(String(255))
    lastname:Mapped[str] = Column(String(255))
    phone:Mapped[str] = Column(String(13))
    name_id:Mapped[int] = Column(Integer, primary_key = True)
    pollingunit_uniqueid:Mapped[int] = Column(Integer)



