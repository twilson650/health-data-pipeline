library AssessedforRehabilitation version '6.2.012'

using QDM version '5.3'

include MATGlobalCommonFunctions version '2.0.000' called Global
include TJC_Overall version '7.0.000' called TJC

valueset "ONC Administrative Sex": 'urn:oid:2.16.840.1.113762.1.4.1'
valueset "Race": 'urn:oid:2.16.840.1.114222.4.11.836'
valueset "Ethnicity": 'urn:oid:2.16.840.1.114222.4.11.837'
valueset "Payer": 'urn:oid:2.16.840.1.114222.4.11.3591'
valueset "Comfort Measures": 'urn:oid:1.3.6.1.4.1.33895.1.3.0.45'
valueset "Discharge To Acute Care Facility": 'urn:oid:2.16.840.1.113883.3.117.1.7.1.87'
valueset "Discharged to Health Care Facility for Hospice Care": 'urn:oid:2.16.840.1.113883.3.117.1.7.1.207'
valueset "Discharged to Home for Hospice Care": 'urn:oid:2.16.840.1.113883.3.117.1.7.1.209'
valueset "Discharged to Rehabilitation Facility": 'urn:oid:2.16.840.1.113883.3.117.1.7.1.132'
valueset "Left Against Medical Advice": 'urn:oid:2.16.840.1.113883.3.117.1.7.1.308'
valueset "Medical Reason": 'urn:oid:2.16.840.1.113883.3.117.1.7.1.473'
valueset "Patient Expired": 'urn:oid:2.16.840.1.113883.3.117.1.7.1.309'
valueset "Patient Refusal": 'urn:oid:2.16.840.1.113883.3.117.1.7.1.93'
valueset "Rehabilitation Assessment": 'urn:oid:2.16.840.1.113762.1.4.1045.18'
valueset "Rehabilitation Therapy": 'urn:oid:2.16.840.1.113762.1.4.1045.19'

context Patient

define "SDE Ethnicity":
	["Patient Characteristic Ethnicity": "Ethnicity"]

define "SDE Payer":
	["Patient Characteristic Payer": "Payer"]

define "SDE Race":
	["Patient Characteristic Race": "Race"]

define "SDE Sex":
	["Patient Characteristic Sex": "ONC Administrative Sex"]

define "AA-ProcedureNotDone":
	["Procedure, Not Performed": "Rehabilitation Assessment"]
		union ( ["Procedure, Not Performed": "Rehabilitation Assessment"] P
				where P.negationRationale in "Medical Reason"
					or P.negationRationale in "Patient Refusal"
		)

define "AA-Procedures":
	["Procedure, Performed": "Rehabilitation Assessment"]
		union ["Procedure, Performed": "Rehabilitation Therapy"]

define "Comfort Measures During Hospitalization":
	TJC."Encounter with Principal Diagnosis and Age" A
		with "Intervention Comfort Measures" B
			such that Coalesce(start of B.relevantPeriod, B.authorDatetime)during Global."Hospitalization"(A)

define "Denominator":
	TJC."Encounter with Principal Diagnosis and Age"

define "Denominator Exclusions":
	distinct((TJC."Encounter with Principal Diagnosis and Age" Encounter
				where Encounter.dischargeDisposition in "Discharge To Acute Care Facility"
					or Encounter.dischargeDisposition in "Left Against Medical Advice"
					or Encounter.dischargeDisposition in "Discharged to Home for Hospice Care"
					or Encounter.dischargeDisposition in "Patient Expired"
					or Encounter.dischargeDisposition in "Discharged to Health Care Facility for Hospice Care"
		)
			union "Comfort Measures During Hospitalization"
	)

define "Encounter with Discharge to Rehabilitation Facility":
	TJC."Encounter with Principal Diagnosis and Age" A
		where A.dischargeDisposition in "Discharged to Rehabilitation Facility"

define "Initial Population":
	TJC."Encounter with Principal Diagnosis and Age"

define "Intervention Comfort Measures":
	["Intervention, Order": "Comfort Measures"]
		union ["Intervention, Performed": "Comfort Measures"]

define "Numerator":
	distinct((TJC."Encounter with Principal Diagnosis and Age" A
				with "AA-ProcedureNotDone" B
					such that B.authorDatetime during A.relevantPeriod
		)
			union(TJC."Encounter with Principal Diagnosis and Age" A
					with "AA-Procedures" C
						such that C.relevantPeriod starts during A.relevantPeriod
			)
			union "Encounter with Discharge to Rehabilitation Facility"
	)

