# standards.py
# Definitions of IEEE 830-1998 and ISO/IEC/IEEE 29148:2018 SRS Standards with aliases

STANDARDS = {
    "IEEE-830-1998": {
        "title": "IEEE Std 830-1998 (Classic SRS Standard)",
        "description": "The classic IEEE standard recommending a highly structured, system-feature-centric SRS layout.",
        "sections": [
            {
                "id": "1",
                "name": "Introduction",
                "required": True,
                "weight": 5,
                "keywords": ["introduction", "intro"],
                "anchors": ["This section provides an overview of the software requirements specification document.", "The introduction section of the system specifications."],
                "aliases": ["Introduction", "Intro", "Document Overview", "1. Introduction"]
            },
            {
                "id": "1.1",
                "name": "Purpose",
                "required": True,
                "weight": 3,
                "keywords": ["purpose", "objective", "goal", "aim"],
                "anchors": ["Delineate the purpose of this document and its target software system.", "The objective and goal of this requirements specification."],
                "aliases": ["Purpose", "Document Purpose", "Objective", "Objectives", "Goal", "Goals", "1.1 Purpose"]
            },
            {
                "id": "1.2",
                "name": "Scope",
                "required": True,
                "weight": 3,
                "keywords": ["scope", "boundaries", "extent"],
                "anchors": ["Define the scope of the software application being developed.", "Identify the software products to be produced, their benefits, and objectives."],
                "aliases": ["Scope", "Project Scope", "System Scope", "Boundaries", "1.2 Scope"]
            },
            {
                "id": "1.3",
                "name": "Definitions, Acronyms, and Abbreviations",
                "required": True,
                "weight": 2,
                "keywords": ["definitions", "acronyms", "abbreviations", "glossary"],
                "anchors": ["Provide definitions of all terms, acronyms, and abbreviations required to interpret the SRS.", "Glossary of terms and abbreviations used in the software specification."],
                "aliases": ["Definitions, Acronyms, and Abbreviations", "Definitions", "Acronyms", "Abbreviations", "Glossary", "Definitions and Acronyms", "1.3 Definitions, Acronyms, and Abbreviations"]
            },
            {
                "id": "1.4",
                "name": "References",
                "required": True,
                "weight": 2,
                "keywords": ["references", "bibliography", "citations"],
                "anchors": ["Provide a complete list of all documents referenced elsewhere in the SRS.", "List of references, source standards, or books used for building the software spec."],
                "aliases": ["References", "Referenced Documents", "Bibliography", "Citations", "1.4 References"]
            },
            {
                "id": "1.5",
                "name": "Overview",
                "required": False,
                "weight": 1,
                "keywords": ["overview", "document organization"],
                "anchors": ["Describe what the rest of the SRS contains and how the document is organized.", "Overview of the remainder of this specifications document."],
                "aliases": ["Overview", "Document Organization", "Document Structure", "1.5 Overview"]
            },
            {
                "id": "2",
                "name": "Overall Description",
                "required": True,
                "weight": 5,
                "keywords": ["overall description", "general description", "product overview"],
                "anchors": ["Describe the general factors that affect the product and its requirements.", "A high-level general description of the system and its contextual dependencies."],
                "aliases": ["Overall Description", "General Description", "Product Overview", "Product Description", "2. Overall Description"]
            },
            {
                "id": "2.1",
                "name": "Product Perspective",
                "required": True,
                "weight": 3,
                "keywords": ["product perspective", "context", "relations"],
                "anchors": ["Put the product into perspective with other related products or systems.", "System context diagram, hardware interfaces, software interfaces, or system constraints."],
                "aliases": ["Product Perspective", "System Context", "Context", "Perspective", "System Perspective", "2.1 Product Perspective"]
            },
            {
                "id": "2.2",
                "name": "Product Functions",
                "required": True,
                "weight": 4,
                "keywords": ["product functions", "features", "capabilities", "use cases summary"],
                "anchors": ["Provide a summary of the major functions that the software will perform.", "A high-level list or explanation of features that the system supports."],
                "aliases": ["Product Functions", "System Features", "Product Features", "Features", "System Capabilities", "Major Functions", "2.2 Product Functions"]
            },
            {
                "id": "2.3",
                "name": "User Classes and Characteristics",
                "required": True,
                "weight": 3,
                "keywords": ["user classes", "user characteristics", "actors", "personas"],
                "anchors": ["Identify the various user classes that you anticipate will use this product.", "Descriptions of user types, their educational levels, technical expertise, and roles."],
                "aliases": ["User Classes and Characteristics", "User Characteristics", "User Classes", "Actors", "Users", "Target Audience", "User Profiles", "2.3 User Classes and Characteristics"]
            },
            {
                "id": "2.4",
                "name": "Operating Environment",
                "required": True,
                "weight": 3,
                "keywords": ["operating environment", "platform", "target environment"],
                "anchors": ["Identify the hardware, operating system, and hardware platform the software runs on.", "The system deployment environments, platform constraints, and server requirements."],
                "aliases": ["Operating Environment", "Environment", "Operating Platform", "Deployment Platform", "Target Environment", "2.4 Operating Environment"]
            },
            {
                "id": "2.5",
                "name": "Design and Implementation Constraints",
                "required": True,
                "weight": 3,
                "keywords": ["constraints", "limitations", "restrictions"],
                "anchors": ["Describe any items or issues that will limit the developer's options.", "Regulatory policies, hardware limitations, language requirements, or development standards."],
                "aliases": ["Design and Implementation Constraints", "Constraints", "Limitations", "Restrictions", "Implementation Constraints", "Design Constraints", "2.5 Design and Implementation Constraints"]
            },
            {
                "id": "2.6",
                "name": "Assumptions and Dependencies",
                "required": True,
                "weight": 2,
                "keywords": ["assumptions", "dependencies"],
                "anchors": ["List each assumed factor that could affect the requirements stated in this SRS.", "Third-party libraries, external hardware availability, or assumptions about user browsers."],
                "aliases": ["Assumptions and Dependencies", "Assumptions", "Dependencies", "Assumptions & Dependencies", "2.6 Assumptions and Dependencies"]
            },
            {
                "id": "3",
                "name": "Specific Requirements",
                "required": True,
                "weight": 5,
                "keywords": ["specific requirements", "system features", "functional requirements"],
                "anchors": ["This section contains all software requirements to a level of detail sufficient for designers.", "Detailed list of functional and non-functional requirements for developers."],
                "aliases": ["Specific Requirements", "System Features", "Functional Requirements", "Detailed Requirements", "Requirements Details", "3. Specific Requirements"]
            },
            {
                "id": "3.1",
                "name": "External Interface Requirements",
                "required": True,
                "weight": 4,
                "keywords": ["external interface", "user interface", "hardware interface", "software interface", "communication interface"],
                "anchors": ["Detailed description of all inputs and outputs of the software system.", "Detailed user interface UI specifications, hardware bindings, and communication protocols."],
                "aliases": [
                    "External Interface Requirements", "External Interfaces", "Interfaces", "User Interfaces", 
                    "4. External Interface Requirements", "4. External Interfaces", "Section 4 - External Interfaces", "External Interface Requirements (Section 4)", "3.1 External Interface Requirements"
                ]
            },
            {
                "id": "3.2",
                "name": "Functional Requirements",
                "required": True,
                "weight": 5,
                "keywords": ["functional requirements", "system features", "actions", "inputs and outputs"],
                "anchors": ["Specify individual functional requirements, use cases, inputs, processes, and outputs.", "Detailed software features, user actions, system responses, and workflows."],
                "aliases": ["Functional Requirements", "System Features", "System Capabilities", "Detailed Functions", "3.2 Functional Requirements"]
            },
            {
                "id": "3.3",
                "name": "Performance Requirements",
                "required": True,
                "weight": 3,
                "keywords": ["performance", "response time", "throughput", "latency"],
                "anchors": ["Specify static and dynamic numerical requirements placed on the software.", "System response times, transactions per second, memory constraints, and performance targets."],
                "aliases": ["Performance Requirements", "Performance", "System Performance", "Non-Functional Performance", "3.3 Performance Requirements"]
            },
            {
                "id": "3.4",
                "name": "Logical Database Requirements",
                "required": False,
                "weight": 2,
                "keywords": ["database requirements", "data model", "logical schema"],
                "anchors": ["Specify the logical requirements for any information that is to be stored in a database.", "ER diagrams, logical database schema, data integrity constraints, or data entities."],
                "aliases": ["Logical Database Requirements", "Database Requirements", "Data Model", "Data Schemas", "Database Schemata", "3.4 Logical Database Requirements"]
            },
            {
                "id": "3.5",
                "name": "Design Constraints",
                "required": False,
                "weight": 2,
                "keywords": ["design constraints", "standards compliance"],
                "anchors": ["Specify constraints imposed by other standards or platform compliance.", "Specific programming languages, structural architectures, or compliance standards."],
                "aliases": ["Design Constraints", "Design Limitations", "Architectural Constraints", "Implementation Constraints", "3.5 Design Constraints"]
            },
            {
                "id": "3.6",
                "name": "Software System Attributes",
                "required": True,
                "weight": 3,
                "keywords": ["system attributes", "security", "reliability", "maintainability", "safety"],
                "anchors": ["Non-functional system attributes such as security, reliability, availability, and safety.", "Security controls, encryption standards, MTBF criteria, or ease of maintenance."],
                "aliases": ["Software System Attributes", "System Attributes", "Security", "Reliability", "Quality Attributes", "System Quality Attributes", "3.6 Software System Attributes"]
            }
        ]
    },
    "ISO-IEC-IEEE-29148-2018": {
        "title": "ISO/IEC/IEEE 29148:2018 (Modern SRS Standard)",
        "description": "The modern ISO/IEC/IEEE international standard that replaces the older IEEE 830 standard, emphasizing life-cycle processes and systems engineering.",
        "sections": [
            {
                "id": "1",
                "name": "Introduction",
                "required": True,
                "weight": 5,
                "keywords": ["introduction", "intro"],
                "anchors": ["Provide an introduction to the system and the document contents."],
                "aliases": ["Introduction", "Intro", "Document Overview", "1. Introduction"]
            },
            {
                "id": "1.1",
                "name": "Purpose",
                "required": True,
                "weight": 3,
                "keywords": ["purpose", "document purpose"],
                "anchors": ["Describe the purpose of the software requirements specification document."],
                "aliases": ["Purpose", "Document Purpose", "Objective", "Objectives", "Goal", "Goals", "1.1 Purpose"]
            },
            {
                "id": "1.2",
                "name": "Scope",
                "required": True,
                "weight": 3,
                "keywords": ["scope", "system scope"],
                "anchors": ["Define the scope of the system or software application under development."],
                "aliases": ["Scope", "Project Scope", "System Scope", "Boundaries", "1.2 Scope"]
            },
            {
                "id": "1.3",
                "name": "Product Overview",
                "required": True,
                "weight": 4,
                "keywords": ["product overview", "system context", "functions", "limitations"],
                "anchors": ["High-level description of the system, including its functions, perspective, and operational limitations."],
                "aliases": ["Product Overview", "System Context", "Context", "System Perspective", "1.3 Product Overview"]
            },
            {
                "id": "1.4",
                "name": "Definitions and Acronyms",
                "required": True,
                "weight": 2,
                "keywords": ["definitions", "acronyms", "abbreviations", "glossary"],
                "anchors": ["Definitions, terminology, abbreviations, and acronyms used in the specifications."],
                "aliases": ["Definitions and Acronyms", "Definitions", "Acronyms", "Abbreviations", "Glossary", "Definitions, Acronyms, and Abbreviations", "1.4 Definitions and Acronyms"]
            },
            {
                "id": "2",
                "name": "References",
                "required": True,
                "weight": 2,
                "keywords": ["references", "referenced documents", "citations"],
                "anchors": ["Listing of all documents, standards, or materials cited or referenced in the SRS."],
                "aliases": ["References", "Referenced Documents", "Bibliography", "Citations", "2. References"]
            },
            {
                "id": "3",
                "name": "Specific Requirements",
                "required": True,
                "weight": 5,
                "keywords": ["specific requirements", "detailed requirements"],
                "anchors": ["The core specifications containing functional, non-functional, usability, and design requirements."],
                "aliases": ["Specific Requirements", "System Features", "Functional Requirements", "Detailed Requirements", "Requirements Details", "3. Specific Requirements"]
            },
            {
                "id": "3.1",
                "name": "Functional Requirements",
                "required": True,
                "weight": 5,
                "keywords": ["functional requirements", "capabilities", "use cases", "functions"],
                "anchors": ["Detailed capabilities, inputs, processes, and outputs expected from the system software."],
                "aliases": ["Functional Requirements", "System Features", "System Capabilities", "Detailed Functions", "3.1 Functional Requirements"]
            },
            {
                "id": "3.2",
                "name": "Usability Requirements",
                "required": True,
                "weight": 3,
                "keywords": ["usability", "human factors", "accessibility", "user experience"],
                "anchors": ["Detailed specifications of ease-of-use, learning curve, accessibility standards, and GUI layouts."],
                "aliases": ["Usability Requirements", "Usability", "Human Factors", "Accessibility", "3.2 Usability Requirements"]
            },
            {
                "id": "3.3",
                "name": "Performance Requirements",
                "required": True,
                "weight": 3,
                "keywords": ["performance", "response times", "latency", "scalability"],
                "anchors": ["Performance metrics including system load capability, transactional speeds, and CPU/memory constraints."],
                "aliases": ["Performance Requirements", "Performance", "System Performance", "Non-Functional Performance", "3.3 Performance Requirements"]
            },
            {
                "id": "3.4",
                "name": "Logical Database Requirements",
                "required": False,
                "weight": 2,
                "keywords": ["database requirements", "logical schema", "data requirements"],
                "anchors": ["Logical schema structure, query parameters, relational models, or database constraints."],
                "aliases": ["Logical Database Requirements", "Database Requirements", "Data Model", "Data Schemas", "Database Schemata", "3.4 Logical Database Requirements"]
            },
            {
                "id": "3.5",
                "name": "Design Constraints",
                "required": True,
                "weight": 3,
                "keywords": ["design constraints", "architectural constraints", "implementation constraints"],
                "anchors": ["Imposed boundaries on design, tech stacks, architectural styles, or legacy bindings."],
                "aliases": ["Design Constraints", "Design Limitations", "Architectural Constraints", "Implementation Constraints", "3.5 Design Constraints"]
            },
            {
                "id": "3.6",
                "name": "Software System Attributes",
                "required": True,
                "weight": 3,
                "keywords": ["system attributes", "security", "reliability", "maintainability", "safety"],
                "anchors": ["Quality attributes of the system, including encryption, backup frequency, safety standards, and MTBF."],
                "aliases": ["Software System Attributes", "System Attributes", "Security", "Reliability", "Quality Attributes", "System Quality Attributes", "3.6 Software System Attributes"]
            },
            {
                "id": "3.7",
                "name": "Supporting Information",
                "required": False,
                "weight": 2,
                "keywords": ["supporting information", "appendix", "appendices"],
                "anchors": ["Other documents, appendices, indices, diagrams, or context models that clarify requirements."],
                "aliases": ["Supporting Information", "Appendix", "Appendices", "Indices", "Supporting Details", "3.7 Supporting Information"]
            }
        ]
    }
}
