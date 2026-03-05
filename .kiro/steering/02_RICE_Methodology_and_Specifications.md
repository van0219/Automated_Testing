---
inclusion: auto
name: rice-methodology
description: RICE methodology (Reports, Interfaces, Conversions, Enhancements), ANA-050 functional specifications, DES-020 technical specifications, requirements analysis, deliverables. Use when working with RICE items or specification documents.
---

# RICE Methodology and Specifications

## Table of Contents

- [Overview](#overview)
- [What is RICE?](#what-is-rice)
- [RICE Categories Explained](#rice-categories-explained)
  - [Reports (R)](#reports-r)
  - [Interfaces (I)](#interfaces-i)
  - [Conversions (C)](#conversions-c)
  - [Enhancements (E)](#enhancements-e)
- [RICE Item Lifecycle](#rice-item-lifecycle)
- [ANA-050 Functional Specification](#ana-050-functional-specification)
- [DES-020 Technical Specification](#des-020-technical-specification)
- [Document Relationships](#document-relationships)
- [ANA-050 Requirement Analysis Guidelines](#ana-050-requirement-analysis-guidelines)
  - [Step 1: Identify RICE Type](#step-1-identify-rice-type-first-step---critical)
  - [Step 2: Determine IPA vs LPL Requirement](#step-2-determine-ipa-vs-lpl-requirement)
  - [Step 3: Determine Solution Deliverables](#step-3-determine-solution-deliverables)
  - [Step 4: Separate IPA vs LPL Requirements](#step-4-separate-ipa-vs-lpl-requirements)
- [Solution Deliverables by RICE Type](#solution-deliverables-by-rice-type)
- [IPA vs LPL Determination](#ipa-vs-lpl-determination)
- [Separating IPA vs LPL Requirements](#separating-ipa-vs-lpl-requirements)
- [Automated RICE Analysis](#automated-rice-analysis)
- [Document Formatting Standards](#document-formatting-standards)
- [Best Practices](#best-practices)
- [Related Steering Files](#related-steering-files)
- [Summary](#summary)

## Overview

**RICE** is a standard ERP project methodology representing the four major categories of deliverables tracked during Infor FSM system design, configuration, and enhancement processes.

**Key Principle**: Every RICE item represents a complete solution that may include:

- One or more IPAs (main + subprocesses)
- LPL configuration code
- File channels
- Menu definitions
- Form modifications
- Security configurations
- Combined ANA-050 + DES-020 specification document

**Related Tools**:

- Document analysis tools in `ReusableTools/` can help analyze specification documents
- Use `pdf_study_reader.py` for PDF specifications or `docx_image_extractor.py` for Word documents

## What is RICE?

| Letter | Category | Description |
|--------|----------|-------------|
| **R** | Reports | System outputs containing data summaries, detailed views, or analytics |
| **I** | Interfaces | Connections between FSM and external systems for data exchange |
| **C** | Conversions | Data migration from legacy systems into FSM |
| **E** | Enhancements | Customizations extending standard functionality |

## RICE Categories Explained

### Reports (R)

**Purpose**: Outputs generated from FSM containing data summaries, detailed views, or analytics

**Common Implementations**:

- Infor BI reports
- FSM Lists
- Spreadsheet Designer
- Custom report generation

**Characteristics**:

- Read-only data access
- Scheduled or on-demand execution
- Various output formats (PDF, Excel, CSV)
- Support decision-making and operations

**Typical Deliverables**:

- Report specification document
- Report definition files
- Testing guide
- User documentation

### Interfaces (I)

**Purpose**: Connections between Infor FSM and other systems for data exchange

**Common Implementations**:

- **CIS (Configurable Integration Solution)** - No-code interface builder for standard patterns
- **Custom IPA** - Process automation for complex data integration
- ION - Infor's integration platform
- Web Services - REST/SOAP APIs
- File-based integrations - SFTP, File Channels

**Characteristics**:

- Bidirectional or unidirectional data flow
- Scheduled or event-triggered
- Data transformation and mapping
- Error handling and logging

**Typical Deliverables**:

- IPA process files (.lpd)
- File Channel configurations
- Field mapping specifications
- Interface testing guide
- Deployment procedures
- Combined ANA-050 + DES-020 specification

**Key Insight**: IPA is most commonly used for Interfaces where data or processes move between FSM and external systems.

### Conversions (C)

**Purpose**: Data migration from legacy systems into FSM

**Common Implementations**:

- IPA for data transformation
- Data Migrator tools
- ETL (Extract, Transform, Load) processes
- Custom migration scripts

**Characteristics**:

- One-time or phased execution
- Data cleansing and validation
- Legacy system mapping
- Rollback procedures

**Typical Deliverables**:

- Data mapping specifications
- Conversion scripts/IPAs
- Data validation reports
- Rollback procedures
- Testing and validation guide

### Enhancements (E)

**Purpose**: Customizations or extensions to standard FSM functionality

**Common Implementations**:

- **IPA and/or LPL** - Custom workflows and UI changes
- Business class extensions
- Custom fields and validations
- Specialized processing logic

**Characteristics**:

- Meets unique business requirements
- May include both process automation (IPA) and UI changes (LPL)
- Requires thorough testing
- Ongoing maintenance considerations

**Typical Deliverables**:

- IPA process files (if workflow automation)
- LPL configuration code (if UI changes)
- Menu definitions
- Form modifications
- Security configurations
- Testing guide
- Combined ANA-050 + DES-020 specification

## RICE Item Lifecycle

### 1. Requirements Gathering

- Business stakeholders define needs
- Functional requirements documented
- Scope and objectives established

### 2. Analysis (ANA-050)

- Functional specification created
- RICE type identified
- IPA vs LPL determination made
- Requirements separated and analyzed

### 3. Design (DES-020)

- Technical specification created
- Solution architecture defined
- Field mappings documented
- Implementation approach detailed

### 4. Development

- IPA processes created
- LPL configurations implemented
- File channels configured
- Integration points established

### 5. Testing

- Unit testing
- Integration testing
- User Acceptance Testing (UAT)
- Performance validation

### 6. Deployment

- Migration to production
- User training
- Documentation delivery
- Post-deployment support

### 7. Maintenance

- Ongoing support
- Enhancement requests
- Issue resolution
- Documentation updates

## ANA-050 Functional Specification

### Purpose

- **Blueprint for Implementation**: Detailed guide for developers, testers, and business analysts
- **Alignment**: Clear communication of business requirements to technical teams
- **Reference**: Used throughout project lifecycle for design, development, testing, and UAT

### Standard Sections

1. **Introduction** - High-level process/feature overview
2. **Scope** - Inclusions and exclusions
3. **Business Requirements** - Detailed business perspective requirements
4. **Process Flow** - Workflow diagrams and step-by-step descriptions
5. **Data Requirements** - Data sources, fields, validation rules
6. **User Roles & Permissions** - Access control definitions
7. **Integration Points** - ION, SFTP, API interfaces
8. **Error Handling** - Error scenarios and management strategies
9. **Reporting & Notifications** - Reports, alerts, email requirements
10. **Approval Workflow** - Approval steps and routing details (if applicable)
11. **Appendix** - Supporting information

### Key Content

- Business objectives and scenarios
- Functional requirements with acceptance criteria
- Process flow diagrams
- Field mapping tables
- Business rules and validation logic
- User interface requirements
- Integration specifications
- Test scenarios

## DES-020 Technical Specification

### Purpose

- **Technical Blueprint**: Provides developers with clear implementation instructions
- **Alignment**: Ensures technical implementation matches business requirements
- **Reference**: Used throughout development, testing, deployment, and maintenance

### Standard Sections

1. **Introduction** - Technical solution overview and objectives
2. **Technical Architecture** - System components and interaction diagrams
3. **Data Mapping & Transformation** - Field mappings and transformation logic
4. **Interface Specifications** - API definitions, file formats, integration points
5. **Configuration Details** - System settings, environment variables, parameters
6. **Security & Access Controls** - User roles, permissions, data protection
7. **Error Handling & Logging** - Error management and logging strategies
8. **Development Steps** - Detailed build and deployment instructions
9. **Testing & Validation** - Technical test cases and validation procedures
10. **Appendix** - Supporting diagrams, tables, references

### Key Content

- Technical architecture diagrams
- Detailed field mappings with data types
- IPA process activity specifications
- LPL configuration code
- File channel configurations
- Security configurations
- Deployment procedures
- Technical test cases

## Document Relationships

### ANA-050 → DES-020 Flow

- **ANA-050** defines the "what" (business requirements)
- **DES-020** defines the "how" (technical implementation)
- **Combined Template** merges both for comprehensive documentation

### Usage in Project Lifecycle

- **Project Initiation**: ANA-050 establishes requirements
- **Design & Development**: DES-020 guides technical implementation
- **Testing & UAT**: Both serve as validation references
- **Documentation**: Record for maintenance and enhancements

### Relationship to IPA Development

Both specifications serve as primary inputs for:

- IPA flow design and implementation
- LPL script development
- Integration configuration (ION, File Channels)
- Application configuration setup
- Test case creation and validation
- User acceptance criteria

## ANA-050 Requirement Analysis Guidelines

**AI Action**: When analyzing ANA-050 documents, follow this 4-step process in order.

### Step 1: Identify RICE Type (FIRST STEP - CRITICAL)

**Every ANA-050 document represents a RICE item.** Before any technical analysis, identify the RICE category.

**How to Identify RICE Type from ANA-050**:

1. **Check document title and RICE ID**
   - Example: "FPI-ANA-050-MATCH-REPORT" suggests Interface
   - Example: "CLIENT-ANA-050-INVOICE-APPROVAL" suggests Enhancement

2. **Look for keywords in content**:
   - "extract", "import", "export", "integration" → **Interface**
   - "report", "analytics", "dashboard" → **Report**
   - "migration", "conversion", "legacy data" → **Conversion**
   - "workflow", "approval", "UI change", "new field" → **Enhancement**

3. **Analyze business objectives**:
   - Data exchange with external systems → **Interface**
   - Information delivery to users → **Report**
   - One-time data load → **Conversion**
   - Process improvement or customization → **Enhancement**

### Step 2: Determine IPA vs LPL Requirement

**Based on RICE type and requirements, determine if IPA, LPL, or both are needed:**

| Requirement Type | IPA Required | LPL Required | Workunit Created |
|------------------|--------------|--------------|------------------|
| Data integration with external system | ✅ Yes | ❌ No | ✅ Yes |
| Scheduled data extract/export | ✅ Yes | ❌ No | ✅ Yes |
| File-triggered processing | ✅ Yes | ❌ No | ✅ Yes |
| Approval workflow | ✅ Yes | Maybe | ✅ Yes |
| UI form modification only | ❌ No | ✅ Yes | ❌ No |
| New field on business class | ❌ No | ✅ Yes | ❌ No |
| Menu/navigation change only | ❌ No | ✅ Yes | ❌ No |
| LPL action triggering process | ✅ Yes | ✅ Yes | ✅ Yes |

**Key Insight**: Interfaces (the "I" in RICE) typically use either CIS (no-code) for standard patterns or Custom IPA for complex logic where data or processes move between FSM and external systems.

### Step 3: Determine Solution Deliverables

**Based on RICE type and IPA/LPL determination, identify required deliverables:**

#### Interface (I) - File-Triggered

```text
Deliverables:
├── 00_Solution_Summary.md
├── 01_Requirements_Analysis.md
├── 02_IPA_Technical_Specification.md
├── 03_[ProjectName].lpd (IPA file)
├── 04_File_Channel_Configuration.md  ← REQUIRED for file-triggered
├── 05_Testing_Guide.md
├── 06_Deployment_Guide.md
└── ANA-050_DES-020_Combined_Specification.docx
```

#### Interface (I) - Scheduled Outbound

```text
Deliverables:
├── 00_Solution_Summary.md
├── 01_Requirements_Analysis.md
├── 02_IPA_Technical_Specification.md
├── 03_[ProjectName].lpd (IPA file)
├── 05_Testing_Guide.md  ← NO File Channel (scheduled via Process Server Admin)
├── 06_Deployment_Guide.md
└── ANA-050_DES-020_Combined_Specification.docx
```

#### Enhancement (E) - LPL Only (No IPA)

```text
Deliverables:
├── 00_Solution_Summary.md
├── 01_Requirements_Analysis.md
├── 07_LPL_Configuration_Codes.md
├── 08_Menu_Definitions.lpl (if needed)
├── 09_Form_Modifications.lpl (if needed)
├── 10_Field_Configurations.lpl (if needed)
├── 05_Testing_Guide.md
├── 06_Deployment_Guide.md
└── ANA-050_DES-020_Combined_Specification.docx
```

#### Enhancement (E) - IPA + LPL

```text
Deliverables:
├── 00_Solution_Summary.md
├── 01_Requirements_Analysis.md
├── 02_IPA_Technical_Specification.md
├── 03_[ProjectName].lpd (IPA file)
├── 07_LPL_Configuration_Codes.md
├── [LPL files as needed]
├── 05_Testing_Guide.md
├── 06_Deployment_Guide.md
└── ANA-050_DES-020_Combined_Specification.docx
```

### Step 4: Separate IPA vs LPL Requirements

When analyzing ANA-050 documents, distinguish between:

#### **IPA Flow Requirements** (Process Automation)

- Approval routing logic and approver determination
- Email notifications and content
- Workflow actions (Approve, Return, Reject)
- Business class queries and data retrieval
- Process flow logic and branching
- Integration with external systems
- Error handling and exception management
- Scheduled data extraction
- File processing and transformation

#### **Configuration Console Requirements** (LPL/UI Changes)

- Field protection and read-only settings
- Form field display and visibility
- Default value population
- Required field validation
- UI layout and formatting
- Service/Process Definition enablement
- Form behavior and user experience
- Menu and navigation changes
- List configurations
- Security class updates

**Analysis Approach**:

1. **Identify UI/Form Changes**: Requirements mentioning "hide fields", "protect fields", "display", "default values" are Configuration Console tasks
2. **Focus IPA Scope**: Extract only approval logic, notifications, and process flow requirements
3. **Separate Concerns**: UI modifications require LPL changes via Configuration Console, not IPA flows
4. **Document Both**: Clearly separate IPA requirements from Configuration Console requirements in analysis

## Solution Deliverables by RICE Type

### Reports (R)

**Typical Deliverables**:

- Report specification document
- Report definition files (BI, Spreadsheet Designer)
- Data source configurations
- Testing guide
- User documentation
- ANA-050 + DES-020 specification

**IPA/LPL**: Usually neither (unless report generation is automated via IPA)

### Interfaces (I)

**Typical Deliverables**:

- **CIS Configuration** (for standard patterns) - No-code interface builder
- **Custom IPA process files (.lpd)** (for complex logic) - Process automation
- File Channel configurations (if file-triggered)
- Field mapping specifications
- Interface testing guide
- Deployment procedures
- Error handling documentation
- ANA-050 + DES-020 specification

**IPA/LPL**: CIS (no-code) or Custom IPA required, LPL optional

**CIS vs Custom IPA Decision**:
- Use CIS for standard outbound/inbound file interfaces
- Use Custom IPA for complex business logic, approval workflows, multi-step processes

### Conversions (C)

**Typical Deliverables**:

- Data mapping specifications
- Conversion scripts/IPAs
- Data validation reports
- Rollback procedures
- Testing and validation guide
- ANA-050 + DES-020 specification

**IPA/LPL**: IPA common, LPL optional

### Enhancements (E)

**Typical Deliverables**:

- IPA process files (if workflow automation)
- LPL configuration code (if UI changes)
- Menu definitions
- Form modifications
- Security configurations
- Testing guide
- ANA-050 + DES-020 specification

**IPA/LPL**: Both common, depends on requirements

## IPA vs LPL Determination

### When IPA is Required

- **Data Integration**: Exchanging data with external systems
- **Scheduled Processing**: Automated data extraction or transformation
- **File Processing**: Triggered by file arrival or scheduled
- **Approval Workflows**: Multi-step approval processes with notifications
- **Business Logic**: Complex processing that spans multiple business classes
- **Error Handling**: Sophisticated error management and recovery

### When LPL is Required

- **UI Modifications**: Form layout, field visibility, protection
- **Field Defaults**: Populating default values
- **Validation Rules**: Client-side or server-side validation
- **Menu Changes**: Adding or modifying navigation
- **List Configurations**: Custom list views and filters
- **Security**: Role-based access control
- **Form Behavior**: Custom actions and event handling

### When Both are Required

- **Approval Workflows with UI**: Process automation + form modifications
- **Triggered Processes**: LPL button/action triggers IPA process
- **Complex Enhancements**: Both process logic and UI changes needed
- **Integrated Solutions**: End-to-end functionality requiring both layers

## Separating IPA vs LPL Requirements

### Example: Invoice Approval Enhancement

**IPA Requirements** (Process Automation):

- Determine approver based on invoice amount and department
- Send email notification to approver
- Wait for approval action
- Escalate if no response within 2 business days
- Update invoice status upon approval/rejection
- Log all approval actions

**LPL Requirements** (UI/Configuration):

- Protect invoice amount field after submission
- Hide approval history section from non-approvers
- Add "Submit for Approval" button to invoice form
- Display approval status indicator
- Set default values for department and cost center
- Enable Service Definition for approval process

**Key Distinction**: IPA handles the workflow logic and automation, LPL handles the user interface and form behavior.

## Automated RICE Analysis

## Document Formatting Standards

### Combined ANA-050 + DES-020 Template

**Purpose**: Single document approach for complete project specification

**Structure**:

- **Title Page**: Infor logo, project name, RICE ID
- **Document Control**: Version history, reviewers, approvers
- **Table of Contents**: Auto-generated with hyperlinks
- **Functional Specifications** (Sections 2-3): Business requirements, process flows, interface specs
- **Technical Design** (Section 4): Solution architecture, configurations, implementation
- **Testing Process** (Section 5): Test steps and validation
- **Appendix** (Section 6): Artifacts and supporting documentation

**Key Formatting**:

- **Page Size**: A4 (8.27" x 11.69")
- **Font**: Arial (NOT Calibri)
- **Headings**: H1 (14pt, ALL CAPS), H2 (14pt, Title Case), H3 (12pt, ALL CAPS), H4 (12pt, Title Case)
- **Tables**: Black header background, white text, 8pt font
- **Colors**: Infor Blue (#13A3F7) for highlights

**Critical**: NO "Part I" or "Part II" headers - use continuous numbered sections

## Best Practices

### RICE Item Management

1. **Single Source of Truth**: One RICE item = one complete solution
2. **Clear Scope**: Define inclusions and exclusions upfront
3. **Traceability**: Maintain requirements traceability throughout lifecycle
4. **Version Control**: Track all changes to specifications and deliverables
5. **Stakeholder Alignment**: Regular reviews with business and technical teams

### Specification Development

1. **Start with ANA-050**: Define business requirements before technical design
2. **Collaborate**: Involve business analysts, developers, and testers
3. **Be Specific**: Provide detailed field mappings, business rules, and test scenarios
4. **Use Examples**: Include sample data and expected outcomes
5. **Review Thoroughly**: Multiple review cycles before development begins

### IPA vs LPL Separation

1. **Analyze First**: Determine IPA vs LPL requirements before development
2. **Separate Concerns**: Keep process automation (IPA) separate from UI (LPL)
3. **Document Both**: Clearly document both IPA and LPL requirements
4. **Test Independently**: Test IPA processes and LPL configurations separately
5. **Integrate Last**: Combine and test end-to-end after individual testing

### Solution Delivery

1. **Complete Package**: Deliver all required deliverables per RICE type
2. **Documentation**: Provide comprehensive testing and deployment guides
3. **Training**: Include user documentation and training materials
4. **Support**: Plan for post-deployment support and maintenance
5. **Knowledge Transfer**: Ensure client team can maintain the solution

## Related Steering Files

- `00_Kiro_General_Rules.md` - Reusable Tools (IPA Analyzer)
- `01_IPA_and_IPD_Complete_Guide.md` - IPA/IPD concepts and implementation
- `06_FSM_Business_Classes_and_API.md` - RICE tracking and business classes
- `07_CIS_Configurable_Integration_Solution.md` - CIS interface builder for standard patterns
- `10_IPA_Report_Generation.md` - IPA peer review and client handover documentation

## Summary

**RICE methodology** provides a structured approach to managing Infor FSM implementation projects:

- **R**eports - Information delivery
- **I**nterfaces - Data integration (most common for IPA)
- **C**onversions - Data migration
- **E**nhancements - Customizations (often IPA + LPL)

**Key Principles**:

1. One RICE item = one complete solution (may include multiple IPAs + LPL)
2. ANA-050 defines "what", DES-020 defines "how"
3. IPA handles process automation, LPL handles UI/configuration
4. Separate concerns early in analysis phase
5. Maintain traceability throughout lifecycle

**Automated Support**:

- IPA Analyzer can automatically identify RICE type from ANA-050
- Validates requirements traceability
- Identifies gaps between specification and implementation
- Provides context-aware recommendations

This methodology ensures consistent, high-quality solution delivery across all Infor FSM projects.
