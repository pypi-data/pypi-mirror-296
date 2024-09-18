from typing import Any
import msgspec


class EmployeeId(msgspec.Struct):
    """A new type describing a Munis API result"""
    employeeNumber: int | None = None


class EmployeeJob(msgspec.Struct):
    employeeNumber: int | None = None
    jobClass: str | None = None


class Employee(msgspec.Struct):
    lastName: str | None
    firstName: str | None
    employeeNumber: int | None
    hireDate: str | None
    birthDate: str | None
    gender: str | None
    ethnicity: str | None
    addressLine1: str | None
    addressLine2: str | None
    addressCity: str | None
    addressState: str | None
    addressZip: str | None
    primaryTelephoneNumber: str | None
    primaryEmail: str | None
    jobClass: str | None
    summaryJobClass: str | None
    groupBU: str | None
    terminatedDate: str | None
    terminatedReason: str | None
    salaryGrade: str | None
    department: str | None
    workLocation: str | None
    scheduledTrainings: bool
    expiringCertifications: bool
    scheduledEvaluations: bool
    expiringDriverLicenses: bool
    scheduledSubstanceTesting: bool
    pendingEnrollment: str | None
    salary: float | None
    positionNumber: int | None
    supervisorEmployeeNumber: int | None
    supervisorName: str | None
    dataSet: str | None
    defaultPayTypeCode: int | None
    defaultPayTypeDescription: str | None
    lastChangedDateTime: str | None
    lastChangedByUser: str | None
    educations: Any | None
    certifications: Any | None
    laborRates: Any | None
    employeeAccruals: Any | None


class Employees(msgspec.Struct):
    """A new type describing a Munis API result"""
    value: list[Employee | None] | None = None


class EmployeeJobs(msgspec.Struct):
    """A new type describing a Munis API result"""
    value: list[EmployeeJob | None] | None = None
