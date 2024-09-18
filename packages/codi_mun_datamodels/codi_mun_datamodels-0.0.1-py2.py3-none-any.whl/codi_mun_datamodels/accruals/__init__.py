import msgspec


class AccrualShort(msgspec.Struct):
    employeeNumber: int | None
    accrualDescription: str | None
    available: float | None


class EmployeeAccrual(msgspec.Struct):
    employeeNumber: int | None
    employeeAccruals: list[AccrualShort] | None


class Accrual(msgspec.Struct):
    employeeName: str | None
    employeeNumber: int | None
    jobClass: str | None
    accrualType: str | None
    accrualDescription: str | None
    available: float | None
    used: float | None
    location: str | None
    soyDate: str | None
    unitOfMeasure: str | None
    hourlyEquivalentAvailable: float | None
    hourlyEquivalentUsed: float | None
    dataSet: str | None


class Accruals(msgspec.Struct):
    """A new type describing a Munis API result"""
    value: list[EmployeeAccrual] | None
