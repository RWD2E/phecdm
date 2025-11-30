# **1. Motivation**

### **1.1 Purpose of the Dataset**

- Why was this dataset created?
    
- What problem(s) does it address?
    
- What research/clinical/AI tasks is it intended to support?
    
- Was it created for internal use, public release, regulatory submission, benchmarking, or commercial use?
    

### **1.2 Dataset Creators and Funders**

- Organizations/institutions involved
    
- Names/roles of creators
    
- Funding sources (grants, contracts, industry partnerships)
    

### **1.3 Target Users / Intended Audience**

- Who is the dataset for? (e.g., clinicians, researchers, ML practitioners, policymakers)
    
- What types of analyses are envisioned?
    

### **1.4 Ethical or Societal Motivation**

- Specific gaps or harms the dataset aims to address
    
- Stakeholders involved in shaping the dataset
    

---

# **2. Dataset Composition**

### **2.1 Data Modalities**

- Types of raw data (e.g., EHR, imaging, labs, claims, sensor data, PROs, genomics, NLP text)
    
- Structured vs. unstructured components
    
- Number of tables/files
    

### **2.2 Data Instances**

- Number of records (patients, visits, images, rows)
    
- Distribution by site, geography, demographics, timeframe
    

### **2.3 Key Variables / Features**

- Summary of major fields (e.g., demographics, exposures, outcomes, covariates)
    
- Controlled vocabularies used (LOINC, ICD-10, SNOMED, RxNorm, CPT)
    

### **2.4 Labeling / Annotation**

- Are labels human-annotated, algorithmically derived, or externally sourced?
    
- Who performed labeling? Expertise level?
    
- Annotation instructions or codebooks available?
    

### **2.5 Missingness & Noise Characteristics**

- Common missing fields
    
- Known data quality issues
    
- Duplicate records, inconsistencies, measurement error, concept drift
    

### **2.6 Demographic Composition (if applicable)**

- Age, sex, race/ethnicity distributions
    
- Representativeness relative to target population
    
- Special populations included/excluded (e.g., rural, VA, pediatrics)
    

### **2.7 Sensitive Attributes**

- What sensitive data exist (PHI, identifiers, geolocation)?
    
- How were PHI fields handled or suppressed?
    

---

# **3. Data Collection Process**

### **3.1 Data Sources**

- Primary sources (EHR systems, devices, surveys, claims datasets, wearables)
    
- Sites/institutions contributing data
    
- Data capture systems (Epic, Cerner, VA VistA, REDCap, registries)
    

### **3.2 Timeframe**

- Period of data collection
    
- Update frequency (one-time, yearly, continuously refreshed)
    

### **3.3 Collection Methods**

- Automated extraction, clinician entry, sensor capture, manual chart review, surveys
    
- Sampling strategies
    
- Inclusion and exclusion criteria
    

### **3.4 Consent and User Agreement**

- Was consent obtained? What type?
    
- Waiver of consent? IRB category?
    
- HIPAA basis for data sharing (de-identified, LDS, full PHI under IRB/DUA)?
    

### **3.5 Data Collectors**

- Individuals or devices that collected the data
    
- Measurement instrument details (e.g., BP monitors, imaging modalities, lab analyzers)
    

### **3.6 Safety, Privacy, and Compliance Considerations**

- De-identification and PPRL processes
    
- Security controls (data enclave, child accounts, encryption methods)
    

---

# **4. Preprocessing, Cleaning, and Labeling**

### **4.1 Preprocessing Steps**

- Data cleaning, normalization, mapping, harmonization
    
- Transformations applied (scaling, tokenization, image preprocessing, filtering)
    
- Timestamp normalization and alignment methods
    

### **4.2 Derivations**

- Derived fields (e.g., BMI, Charlson, comorbidity flags, risk scores)
    
- Feature engineering pipelines
    
- Natural language processing steps (e.g., note section tagging, entity extraction)
    

### **4.3 Quality Assurance / Validation**

- Known error-checking procedures
    
- Outlier detection
    
- Data quality metrics
    
- Manual validation samples
    

### **4.4 Versioning**

- Dataset versions
    
- Changelog with differences across versions
    
- Deprecation policy
    

---

# **5. Uses**

### **5.1 Recommended Uses**

- Typical use cases (ML model training, benchmarking, prediction, descriptive epidemiology, causal inference, target trial emulation)
    
- Clinical research areas supported
    

### **5.2 Out-of-Scope / Not Recommended Uses**

- Use cases for which the dataset is **inappropriate or unsafe**
    
- Clinical decision-making without validation
    
- Patient-level diagnosis or treatment prediction
    
- Generalization to populations not represented
    

### **5.3 Known Use Cases**

- Publications, reports, codebases
    
- Prior ML benchmarks or regulatory uses
    

### **5.4 Ethical Considerations for Use**

- Potential for bias, unfairness, or harm
    
- Guidance for responsible use
    
- Impact on minoritized communities, rural populations, etc.
    

---

# **6. Distribution**

### **6.1 How the Dataset is Made Available**

- Public download, controlled access, enclave, VPN, Snowflake reader account, secure research environment
    
- Distribution format (CSV, Parquet, SQL schema, FHIR bundles, imaging DICOM)
    

### **6.2 Access Restrictions**

- IRB required? Data Use Agreement? License terms?
    
- Commercial use restrictions
    
- PHI/LDS/De-identified data limits
    
- Export controls or international restrictions
    

### **6.3 Licensing**

- Creative Commons, open data, proprietary, or custom license
    
- Citation requirements
    
- Redistribution policies
    

### **6.4 Runtime or Platform Requirements**

- Codebooks, APIs, viewer tools
    
- Special software needed (e.g., PyTorch, MATLAB, Snowpark, OMOP/PCORnet analytics environment)
    

---

# **7. Maintenance**

### **7.1 Dataset Maintainers**

- Individuals, labs, data coordinating centers
    
- Contact information
    

### **7.2 Update Policy**

- How often is the dataset updated?
    
- How are errors or bugs reported?
    
- Process for submitting correction requests
    

### **7.3 Long-Term Stewardship**

- Archiving plan
    
- Data retention policy
    
- End-of-life plan for the dataset
    
- Sustainability plan (funding, hosting, governance)
    

---

# **8. Limitations & Caveats**

### **8.1 Provenance Limitations**

- Missing metadata, partially observed variables
    
- Site heterogeneity
    
- Device variability
    

### **8.2 Biases**

- Selection bias
    
- Measurement bias
    
- Demographic bias
    
- Confounding
    
- Site-specific coding practices
    

### **8.3 Statistical Limitations**

- Small sample size
    
- Unreliable ground truth
    
- Temporal drift
    
- Non-random treatment allocation
    

### **8.4 Privacy and Security Risks**

- Re-identification risk
    
- Sensitive features (ZIP codes, dates)
    
- Known vulnerabilities
    

---

# **9. Additional Documentation**

### **9.1 Codebook & Schema**

- Variable names, types, ranges
    
- Controlled terminology mappings
    

### **9.2 Data Model Specification**

- CDISC, PCORnet, OMOP, FHIR, Sentinel, custom schema
    

### **9.3 Governance Artifacts**

- DUAs, BAAs, IRB protocols, SOPs
    
- Access logs, audit records
    
- PPRL documentation
    

### **9.4 References & Links**

- Publications
    
- GitHub repositories
    
- Technical documentation
    
- Protocols or study registration (e.g., ClinicalTrials.gov)