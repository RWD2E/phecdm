inspried by FHIR ValueSet Resource definition
- https://build.fhir.org/valueset.html
- https://build.fhir.org/terminologies-valuesets.html

use a selective set of keys for simplicity and minimal redundancy 
- R!: required
- O!: optional 
- C!: conditional

```json
{
  "identifier": [{ Identifier }], // R! Additional identifier for the value set (business identifier)
  "name": "<string>", // R! I Name for this value set (computer friendly, alphanumeric)
  "title": "<string>", // Name for this value set (human friendly)
  "date": "<dateTime>", // Date last changed
  "description": "<markdown>", // R! Natural language description of the value set
  "useContext": [{ UsageContext }], // The context that the content is intended to support
  "purpose": "<markdown>", // Why this value set is defined
  "topic": [{ CodeableConcept }], // E.g. Education, Treatment, Assessment, etc
  "relatedArtifact": [{ RelatedArtifact }], // Additional documentation, citations, classifications, etc
  "compose": { // Content logical definition of the value set (CLD)
    "include": [{ // R!  Include one or more codes from a code system or other value set(s)
      "system": "<string>", // The system the codes come from
      "concept": [{ // C! A concept defined in the system
        "code": "<code>", // R!  Code or expression from system
        "display": "<string>", // O! Text to display for this code for this value set in this valueset
      }],
      "filter": [{ // C! Select codes/concepts by their properties (including relationships)
        "property": "<string>", // R!  A property/filter defined by the code system
        "op": "<code>", // R!  = | is-a | descendent-of | is-not-a | regex | in | not-in | generalizes | child-of | descendent-leaf | exists
        "value": [{ code }] // R!  list of code or related expression from the system, or regex criteria, or boolean value for exists
      }]
    }]
  }
}
```

A template with minimally necessary elements
```json
{
    "id": ,
    "name": ,
    "description":, 
    "compose": { 
        "include" : [
            { 
                "system":,
                "concept": [{ 
                    "code":, 
                    "display":
                }],
                "filter": [
                    {
                        "property":,
                        "op":,
                        "value": 
                    }
                ]
            }
        ]
    }
},
```


intensional vs. extensional definition
extensional and intensional definitions are two key ways in which the objects, concepts, or referents a term refers to can be defined. They give meaning or denotation to a term
- intensional definition: gives meaning to a term by specifying **necessary and sufficient conditions** for when the term should be used. This definition is achieved by using the concept field
- extensional definition: **lists everything** that falls under that definition. This definition is achieved by using filter operator (https://build.fhir.org/valueset-filter-operator.html), 


`"system"`: the controlled terminology/code system, defined by HL7 OID registry
2(joint-iso-itu-t).16(country).840(us).1(organization).113883(hl7).6(externalCodeSystems).XXX.X.

```json
{
    "loinc":"2.16.840.1.113883.6.1",
    "icd9cm":"2.16.840.1.113883.6.2",
    "icd9proc":"2.16.840.1.113883.6.104",
    "icd10cm":"2.16.840.1.113883.6.90",
    "icd10pcs":"2.16.840.1.113883.6.4",
    "snomedct":"2.16.840.1.113883.6.96",
    "cpt4":"2.16.840.1.113883.6.12",
    "hpc":"2.16.840.1.113883.6.14",
    "ndc":"2.16.840.1.113883.6.69",
    "atc":"2.16.840.1.113883.6.77",
    "rxnorm":"2.16.840.1.113883.6.88",
    "ndfrt":"2.16.840.1.113883.6.209",
    "cvx":"2.16.840.1.113883.12.292",
    "drg":"2.16.840.1.113883.4.642.40.4.48.35"
}
```

`"property"`: the property/filter defined by the code system

```json
{
    "0": "0 decimal place",
    "1": "1 decimal place",
    "2": "2 decimal places"
}

```

`"id"` and `"name"`
https://www.commondataelements.ninds.nih.gov/amyotrophic%20lateral%20sclerosis#pane-141 

body system
Allergic/Immunologic;Cardiovascular;Constitutional symptoms (e.g., fever, weight loss);Dermatological;Ears, Nose, Mouth, Throat;Endocrine;Eyes;Gastrointestinal;Gastrointestinal/Abdominal;Genitourinary;Gynecologic/Urologic/ Renal;Hematologic/Lymphatic;Hepatobiliary;Integumentary (skin and/or breast);Musculoskeletal;Musculoskeletal (separate from ALS exam);Neurological;Neurologic/CNS;Neurological (separate from ALS exam);Oncologic;Psychiatric;Pulmonary;Respiratory;Other, specify:



Noninvasive ventilation (NIV) utilized;Loss of speech;Loss of ambulation;Percutaneous endoscopic gastrostomy (PEG)/feeding tube placement;Tracheostomy performed;Death;Walk by 17 months old;Speak his/her first words by 12 months;Speak in two word combinations by 2 years;Speak in complete sentences by 3 years;Have a cognitive/learning disability;Attend a day care group (with > 5 other children);Head control;Raise both arms above head simultaneously;Roll completely;Maintain seated position supported;Maintain seated position unsupported;Crawl- combat style;Crawl- four point;Stand with support;Cruise along furniture;Stand without support;Walk with support (hand, braces);Walk independently (without braces);Climb stairs


vs-comorb

Elixhauser Comorbidity Index
- predict risk of in-hospital mortality
- predict risk of 30-day, all-cause readmission
- https://hcup-us.ahrq.gov/toolssoftware/comorbidity/comorbidity.jsp#download 
- https://hcup-us.ahrq.gov/toolssoftware/comorbidityicd10/comorbidity_icd10.jsp

Charlson Comorbidity Index
- predict 10-year survival
- https://www.mdcalc.com/calc/3917/charlson-comorbidity-index-cci

Obstetric Comorbidity Index Score
- predict risk of SMM
- https://www.cmqcc.org/research/severe-maternal-morbidity/obstetric-comorbidity-scoring-system
- Easter et al. OB-CMI for maternal risk assessment. Am J Obstet Gynecol 2019.

