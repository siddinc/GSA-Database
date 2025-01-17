from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    ForeignKeyConstraint,
    Date,
    Boolean,
    Float,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from grdb.database import Base


class RamanAnalysis(Base):
    """[summary]
    
    Args:
        Base ([type]): [description]
    
    Returns:
        [type]: [description]
    """

    id = Column(Integer, primary_key=True, info={"verbose_name": "ID"})
    # set_id = Column(
    #     Integer,
    #     ForeignKey("raman_set.id"),
    #     index=True,
    #     info={"verbose_name": "Raman Set ID"},
    # )
    raman_file_id = Column(
        Integer, ForeignKey("raman_file.id", ondelete="CASCADE"), index=True
    )
    software_name = Column(String(20), info={"verbose_name": "Analysis Software"})
    software_version = Column(String(20), info={"verbose_name": "Software Version"})
    __table_args__ = (
        ForeignKeyConstraint(
            [software_name, software_version],
            ["software.name", "software.version"],
            name="fk_raman_analysis_software",
        ),
    )

    xcoord = Column(Integer, info={"verbose_name": "X Coordinate"})
    ycoord = Column(Integer, info={"verbose_name": "Y Coordinate"})
    percent = Column(
        Float,
        info={
            "verbose_name": "Characteristic Percent",
            "std_unit": "%",
            "conversions": {"%": 1},
            "required": True,
        },
    )
    d_to_g = Column(Float, info={"verbose_name": "Weighted D/G"})
    gp_to_g = Column(Float, info={"verbose_name": "Weighted G'/G"})
    d_peak_shift = Column(
        Float,
        info={"verbose_name": "D Peak Shift", "std_unit": "cm^-1", "required": False},
    )
    d_peak_amplitude = Column(
        Float, info={"verbose_name": "D Peak Amplitude", "required": False}
    )
    d_fwhm = Column(
        Float, info={"verbose_name": "D FWHM", "std_unit": "cm^-1", "required": False}
    )
    g_peak_shift = Column(
        Float,
        info={"verbose_name": "G Peak Shift", "std_unit": "cm^-1", "required": False},
    )
    g_peak_amplitude = Column(
        Float, info={"verbose_name": "G Peak Amplitude", "required": False}
    )
    g_fwhm = Column(
        Float, info={"verbose_name": "G FWHM", "std_unit": "cm^-1", "required": False}
    )
    g_prime_peak_shift = Column(
        Float,
        info={"verbose_name": "G' Peak Shift", "std_unit": "cm^-1", "required": False},
    )
    g_prime_peak_amplitude = Column(
        Float, info={"verbose_name": "G' Peak Amplitude", "required": False}
    )
    g_prime_fwhm = Column(
        Float, info={"verbose_name": "G' FWHM", "std_unit": "cm^-1", "required": False}
    )

    raman_file = relationship(
        "RamanFile",
        uselist=False,
        back_populates="raman_analysis",
        primaryjoin="RamanAnalysis.raman_file_id==RamanFile.id",
        lazy="subquery",
    )

    # raman_set = relationship(
    #     "RamanSet",
    #     back_populates="raman_spectra",
    #     foreign_keys=set_id,
    #     primaryjoin="RamanAnalysis.set_id==RamanSet.id",
    # )

    # def __repr__(self):
    #     return self._repr(
    #         id=self.id,
    #         set_id=self.set_id,
    #         raman_file_id=self.raman_file_id,
    #         software_name=self.software_name,
    #         software_version=self.software_version,
    #     )

    def json_encodable(self):
        params = [
            "percent",
            "d_peak_shift",
            "d_peak_amplitude",
            "d_fwhm",
            "g_peak_shift",
            "g_peak_amplitude",
            "g_fwhm",
            "g_prime_peak_shift",
            "g_prime_peak_amplitude",
            "g_prime_fwhm",
        ]
        json_dict = {}
        json_dict["raman_file"] = self.raman_file.json_encodable()
        for p in params:
            info = getattr(RamanAnalysis, p).info
            json_dict[p] = {
                "value": getattr(self, p),
                "unit": info["std_unit"] if "std_unit" in info else None,
            }

        return json_dict
