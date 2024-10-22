def get_course_definition(course_code):
    course_definitions = {
        # COE 
        "BSCE": {
            "definition": "The Bachelor of Science in Civil Engineering (BSCE) is an undergraduate academic degree program that focuses on the design, construction, and maintenance of infrastructure such as buildings, bridges, and transportation systems.",
            "url": "https://www.msuiit.edu.ph/academics/colleges/coe/programs/civil/bsce.pdf",
            "display_name": "BACHELOR OF SCIENCE IN CIVIL ENGINEERING (BSCE)"
        },
        "BSEE": {
            "definition": "The Bachelor of Science in Electrical Engineering (BSEE) is an undergraduate academic degree program that focuses on the design, development, testing, and maintenance of electrical and electronic systems and devices. It provides students with a solid foundation in electrical engineering principles, theories, and practices, as well as practical skills in electrical circuit analysis, electronics, microprocessors, and electrical power systems.",
            "url": "https://drive.google.com/file/d/1yK2INWCLNnIQcK7rEVxwj8vqzC6q6xgh/view",
            "display_name": "BACHELOR OF SCIENCE IN ELECTRICAL ENGINEERING (BSEE)"
        },
        
        "BSMETE": {
            "definition": "The Bachelor of Science in Metallurgical Engineering (BSMETE) is an undergraduate academic degree program that focuses on the study of the properties, extraction, processing, and applications of metals and other materials. It provides students with a strong foundation in metallurgy, materials science, and engineering principles, as well as practical skills in laboratory testing, materials synthesis, and process optimization.",
            "url": "https://www.msuiit.edu.ph/academics/colleges/coe/programs/ccme/bs-metallurgical-engineering.php",
            "display_name": "BACHELOR OF SCIENCE METALLURGICAL ENGINEERING (BSMETE)"
        },
        
        "BSCHE": {
            "definition": "The Bachelor of Science in Chemical Engineering (BSCHE) is an undergraduate academic degree program that focuses on the application of chemical engineering principles to design, develop, and operate processes and facilities for the production of goods and services. It provides students with a comprehensive understanding of chemical engineering principles, theories, and practices, as well as practical skills in process design, optimization, and operation.",
            "url": "https://www.msuiit.edu.ph/academics/colleges/coe/programs/cet/bsche.pdf",
            "display_name": "BACHELOR OF SCIENCE IN CHEMICAL ENGINEERING (BSCHE)"
        },
        
        "BSEsE": {
            "definition": "The Bachelor of Science in Electronics Engineering (BSEsE) is an undergraduate academic degree program that focuses on the study of electronics principles and their practical application in various industries. It provides students with a solid foundation in electronics engineering theories, practices, and hands-on skills.",
            "url": "https://drive.google.com/file/d/14gQ-hhQkeCbQAcBmFQnBHmETK0X2pxBI/view",
            "display_name": "BACHELOR OF SCIENCE IN ELECTRONICS ENGINEERING (BSEsE)"
        },
                
        "BSCPE": {
            "definition": "The Bachelor of Science in Computer Engineering (BSCPE) is an undergraduate academic degree program that focuses on the design, development, and application of computer hardware and software. It provides students with a solid foundation in computer engineering principles, theories, and practices, as well as practical skills in computer programming, circuit analysis, and digital systems design.",
            "url": "https://drive.google.com/file/d/1CabDRaVUKhJPQIhFgAloGNlMV_nGARZA/view",
            "display_name": "BACHELOR OF SCIENCE IN COMPUTER ENGINEERING (BSCPE)"
        },
        
        "BSME": {
            "definition": "The Bachelor of Science in Mechanical Engineering (BSME) is an undergraduate academic degree program that focuses on the design, development, and application of mechanical systems and devices. It provides students with a solid foundation in mechanical engineering principles, theories, and practices, as well as practical skills in mechanical design, analysis, and testing.",
            "url": "https://www.msuiit.edu.ph/academics/colleges/coe/programs/esme/BSME-Prospectus.pdf",
            "display_name": "BACHELOR OF SCIENCE IN MECHANICAL ENGINEERING (BSME)"
        },
        
        "BET-CET": {
            "definition": "The Bachelor of Engineering Technology - Civil Engineering Technology (BET-CET) is an undergraduate academic degree program that focuses on the practical application of civil engineering principles and technologies in various industries. It provides students with a solid foundation in civil engineering principles, theories, and practices, as well as practical skills in civil engineering design, construction, and operations.",
            "url": "https://drive.google.com/file/d/1R5o4u9DRsZORDvR26NhCaveBRv4KOzVd/view",
            "display_name": "BACHELOR OF ENGINEERING TECHNOLOGY - CIVIL ENGINEERING TECHNOLOGY (BET-CET)"
        },
        
        "BET-MMT": {
            "definition": "The Bachelor of Engineering Technology - Metallurgy and Materials Engineering Technology (BET-MMT) program provides students with practical skills in metallurgy and materials engineering. It focuses on the application of metallurgical principles and materials science in industrial processes.",
            "url": "https://drive.google.com/file/d/1voztZKVDcMREDtsP_4U-Wdelq6fcsHz4/view",
            "display_name": "BACHELOR OF ENGINEERING TECHNOLOGY - METALLURGY AND MATERIALS ENGINEERING TECHNOLOGY (BET-MMT)"
        },
        
        "BSEM": {
            "definition": "The Bachelor of Science in Mining Engineering (BSEM) is an undergraduate academic degree program that focuses on the extraction, processing, and utilization of mineral resources. Students learn about mining operations, mineral exploration, environmental considerations, and sustainable resource management.",
            "url": "https://drive.google.com/file/d/1yK2INWCLNnIQcK7rEVxwj8vqzC6q6xgh/view",
            "display_name": "BACHELOR OF SCIENCE IN MINING ENGINEERING (BSEM)"
        },
        
        "BSIAM": {
            "definition": "The Bachelor of Science in Industrial Automation & Mechatronics (BSIAM) is an undergraduate academic degree program that focuses on the design, development, and application of automation and mechatronics systems in various industries. It provides students with a solid foundation in automation and mechatronics principles, theories, and practices, as well as practical skills in designing and developing automation systems.",
            "url": "https://drive.google.com/file/d/1XYhOq2fU2U4L4Jn5Iixc-BWxa6DgmojL/view", 
            "display_name": "BACHELOR OF SCIENCE IN INDUSTRIAL AUTOMATION & MECHATRONICS (BSIAM)"
        }, 
        
        "BSCERE": {
            "definition": "The Bachelor of Science in Ceramics Engineering (BSCERE) is an undergraduate academic degree program that focuses on the design, development, and application of ceramic materials and their products. It provides students with a solid foundation in ceramics engineering principles, theories, and practices, as well as practical skills in ceramics design, testing, and manufacturing.",
            "url": "https://www.msuiit.edu.ph/academics/colleges/coe/programs/ccme/bscere-062015.pdf",
            "display_name": "BACHELOR OF SCIENCE IN CERAMICS ENGINEERING (BSCERE)"
        },
        
        "BET-ELET": {
            "definition": "The Bachelor of Engineering Technology in Electrical Engineering Technology (BET-ELET) is an undergraduate academic degree program that focuses on the practical application of electrical engineering principles and technologies in various industries. It provides students with a solid foundation in electrical engineering principles, theories, and practices, as well as practical skills in electrical engineering design, construction, and operations.",
            "url": "https://drive.google.com/file/d/1qsmilkh0OnuMtdBiScvs033Rrxpx_85S/view",
            "display_name": "BACHELOR OF ENGINEERING TECHNOLOGY IN ELECTRICAL ENGINEERING TECHNOLOGY (BET-ELET)"
        },
        
        "BET-CHET": {
            "definition": "The Bachelor of Engineering Technology in Chemical Engineering Technology (BET-CHET) is an undergraduate academic degree program that focuses on the practical application of chemical engineering principles and technologies in various industries. It provides students with a solid foundation in chemical engineering principles, theories, and practices, as well as practical skills in chemical engineering design, construction, and operations.",
            "url": "https://drive.google.com/file/d/1_1rxeimng79urrS8H1UCk4DFFf9jNSOh/view",
            "display_name": "BACHELOR OF ENGINEERING TECHNOLOGY IN CHEMICAL ENGINEERING TECHNOLOGY (BET-CHET)"
        },
        
        "BET-ESET": {
            "definition": "The Bachelor of Engineering Technology in Electronics Engineering Technology (BET-ESET) is an undergraduate academic degree program that focuses on the practical application of electronics engineering principles and technologies in various industries. It provides students with a solid foundation in electronics engineering principles, theories, and practices, as well as practical skills in electronics engineering design, construction, and operations.",
            "url": "https://drive.google.com/file/d/1BE9NE9CaA154CXcDa5DN07xl-c_e-wgZ/view",
            "display_name": "BACHELOR OF ENGINEERING TECHNOLOGY IN ELECTRONICS ENGINEERING TECHNOLOGY (BET-ESET)"
        },
        
        "BET-MET": {
            "definition": "The Bachelor of Engineering Technology in Mechanical Engineering Technology (BET-MET) is an undergraduate academic degree program that focuses on the practical application of mechanical engineering principles and technologies in various industries. It provides students with a solid foundation in mechanical engineering principles, theories, and practices, as well as practical skills in mechanical engineering design, construction, and operations.",
            "url": "https://drive.google.com/file/d/1cpoMIlGIvnz0-RWDxc5LfAcC3VqOGA-E/view",
            "display_name": "BACHELOR OF ENGINEERING TECHNOLOGY IN MECHANICAL ENGINEERING TECHNOLOGY (BET-MET)"
        },
        
        "BSEnE": {
            "definition": "The Bachelor of Science in Environmental Engineering (BSEnE) is an undergraduate academic degree program that focuses on the application of engineering principles and technologies to protect and preserve the environment. It provides students with a solid foundation in environmental engineering principles, theories, and practices, as well as practical skills in environmental engineering design, construction, and operations.",
            "url": "https://www.example.com/environmental-engineering",
            "display_name": "BACHELOR OF SCIENCE IN ENVIRONMENTAL ENGINEERING (BSEnE)"
        },
        
        "BS EnvET": {
            "definition": "The Bachelor of Science in Environmental Engineering Technology (BS-EnvET) is an undergraduate academic degree program that focuses on the practical application of environmental engineering principles and technologies in various industries. It provides students with a solid foundation in environmental engineering principles, theories, and practices, as well as practical skills in environmental engineering design, construction, and operations.",
            "url": "https://www.example.com/environmental-engineering-technology",
            "display_name": "BACHELOR OF SCIENCE IN ENVIRONMENTAL ENGINEERING TECHNOLOGY (BSEnvET)"
        },

        # CSM
        "BSBIO(MCB)": {
            "definition": "The Bachelor of Science in Biology(Microbiology) - BSBIO(MCB) is an undergraduate academic degree program that focuses on the study of microorganisms, including their structure, function, and interactions with the environment and hosts.\n\nBS Biology-Microbiology programs typically cover a wide range of topics in microbiology, including microbial ecology, evolution, genetics, physiology, and pathogenesis.",
            "url": "https://www.example.com/microbiology",
            "display_name": "BACHELOR OF SCIENCE IN BIOLOGY(MICROBIOLOGY) - BSBIO(MCB)"
        },
        
        "BSBIO(AnBio)": {
            "definition": "The Bachelor of Science in Biology(Animal Biology) - BSBIO(AniBio) is an undergraduate academic degree program that focuses on the study of animals, including their structure, function, evolution, classification, and interactions with the environment.\n\nBS Biology-Animal Biology programs typically cover a wide range of topics in biology, including ecology, evolution, genetics, physiology, and conservation biology, with an emphasis on animal life.",
            "url": "https://www.msuiit.edu.ph/academics/colleges/csm/programs/biology/bs-biology-zoology.php",
            "display_name": "BACHELOR OF SCIENCE IN BIOLOGY(ANIMAL BIOLOGY) - BSBIO(AnBio)"
        },
        
        "BSCHEM": {
            "definition": "The Bachelor of Science in Chemistry (BSCHEM) is an undergraduate academic degree program that focuses on the study of the composition, properties, and reactions of matter.\n\nBSCHEM programs typically cover a wide range of topics in chemistry, including inorganic chemistry, organic chemistry, physical chemistry, analytical chemistry, and biochemistry.",
            "url": "https://www.msuiit.edu.ph/academics/colleges/csm/programs/chemistry/bs-chemistry.php",
            "display_name": "BACHELOR OF SCIENCE IN CHEMISTRY (BSCHEM)"
        }, 
        
        "BSPHYSICS": {
            "definition": "The Bachelor of Science in Physics (BSPHYSICS) is an undergraduate academic degree program that focuses on the study of the fundamental laws of the universe, including energy, matter, space, and time.\n\nBSPHYSICS programs typically cover a wide range of topics in physics, including mechanics, thermodynamics, electromagnetism, quantum mechanics, and relativity.",
            "url": "https://physics.msuiit.edu.ph/",
            "display_name": "BACHELOR OF SCIENCE IN PHYSICS (BSPHYSICS)"
        },
        
        "BSMARINE BIO": {
            "definition": "The Bachelor of Science in Marine Biology (BSMARINE BIO) is an undergraduate academic degree program that focuses on the study of the plants, animals, and microorganisms that live in the ocean and other marine environments. BSMARINE BIO programs typically cover a wide range of topics in marine biology, including marine ecology, oceanography, marine conservation, and marine biotechnology.",
            "url": "https://www.msuiit.edu.ph/academics/colleges/csm/programs/biology/bs-biology-marine.php",
            "display_name": "BACHELOR OF SCIENCE IN MARINE BIOLOGY (BSMARINE BIO)"
        },
        
        "BSBIO(Bdv)": {
            "definition": "The Bachelor of Science in Biology(Biodiversity) - BSBIO(Bdv) is an undergraduate academic degree program that focuses on the study of the variety of life forms on Earth, including their structure, function, evolution, classification, and interactions with the environment. BSBIO-Bdv programs typically cover a wide range of topics in biology, including ecology, evolution, genetics, physiology, and conservation biology, with an emphasis on biodiversity.",
            "url": "https://www.msuiit.edu.ph/academics/colleges/csm/programs/biology/bs-biology-general.php",
            "display_name": "BACHELOR OF SCIENCE IN BIOLOGY (BIODIVERSITY) - BSBIO(Bdv)"
        },
        
        "BSMATH": {
            "definition": "The Bachelor of Science in Mathematics (BSMATH) is an undergraduate academic degree program that focuses on the study of mathematical structures, theories, and applications. BSMATH programs typically cover a wide range of topics in mathematics, including algebra, analysis, geometry, and statistics.",
            "url": "https://www.msuiit.edu.ph/academics/colleges/csm/programs/math-statistics/bs-mathematics.php",
            "display_name": "BACHELOR OF SCIENCE IN MATHEMATICS (BSMATH)"
        },
        
        "BSBIO(PlBio)": {
            "definition": "The Bachelor of Science in Biology(Plant Biology) - BSBIO(PlBio) is an undergraduate degree program focused on the study of plant life. It covers topics such as plant physiology, ecology, and genetics.",
            "url": "https://www.msuiit.edu.ph/academics/colleges/csm/programs/biology/bs-biology-botany.php",
            "display_name": "BACHELOR OF SCIENCE IN BIOLOGY (PLANT BIOLOGY) - BSBIO(PlBio)"
        },
        
        "BSSTAT": {
            "definition": "The Bachelor of Science in Statistics (BSSTAT) is an undergraduate academic degree program that provides students with a solid foundation in statistical theories, principles, and methods. It prepares students for careers in various fields, such as research, healthcare, finance, and government, where statistical analysis and interpretation are essential.",
            "url": "https://www.msuiit.edu.ph/academics/colleges/csm/programs/math-statistics/bs-statistics.php",
            "display_name": "BACHELOR OF SCIENCE IN STATISTICS (BSSTAT)"
        },

        # CHS
        "BSNURSING": {
            "definition": "The Bachelor of Science in Nursing (BSNURSING) is an undergraduate academic degree program that prepares students for a career in nursing. It provides students with a comprehensive education in the principles and practices of nursing, as well as the skills and knowledge necessary to become a licensed nurse.",
            "url" : "https://www.msuiit.edu.ph/academics/colleges/nursing/programs/bs-nursing.php",
            "display_name": "BACHELOR OF SCIENCE IN NURSING (BSNURSING)"
        },

        #CED
        "BSED CHEM": {
            "definition": "The Bachelor of Secondary Education(Chemistry) - BSED(CHEM) is an undergraduate academic degree program designed to prepare students for careers as secondary school teachers specializing in chemistry education.\n\nThe BSEd in Chemistry program combines education theory and pedagogy with specialized knowledge in chemistry to equip students with the skills and competencies needed to effectively teach chemistry to secondary school students.",
            "url": "https://www.msuiit.edu.ph/academics/colleges/ced/programs/sme/FORM%205B%20BSED%20Chemistry.pdf",
            "display_name": "BACHELOR OF SECONDARY EDUCATION (CHEMISTRY) - BSED(CHEM)"
        },
        
        "BSED BIO": {
            "definition": "The Bachelor of Secondary Education(Biology) - BSED(BIO) is an undergraduate academic degree program designed to prepare students for careers as secondary school teachers specializing in biology education. The program combines educational theory and pedagogy with specialized knowledge in biology to equip students with the skills needed to effectively teach biology to secondary school students.",
            "url": "https://www.msuiit.edu.ph/academics/colleges/ced/programs/sme/Form%205B%20BSED%20Biology.pdf",
            "display_name": "BACHELOR OF SECONDARY EDUCATION (BIOLOGY) - BSED(BIO)"
        },
        
        "BTLED-IA": {
            "definition": "The Bachelor of Technology and Livelihood Education-Industrial Arts (BTLED-IA) is an undergraduate academic degree program that prepares students for careers in teaching and training in technical-vocational education and training (TVET) programs, with a focus on industrial arts. It combines education theory and pedagogy with specialized knowledge in industrial arts to equip students with the skills and competencies needed to effectively teach and train students in TVET programs.",
            "url": "https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fwww.msuiit.edu.ph%2Facademics%2Fcolleges%2Fced%2Fprograms%2Ftte%2FBTLEd-Industrial-Arts-Form-5B-Latest.docx&wdOrigin=BROWSELINK",
            "display_name": "BACHELOR OF TECHNOLOGY AND LIVELIHOOD EDUCATION-INDUSTRIAL ARTS (BTLED-IA)"
        },
        
        "BTVTED-DT": {
            "definition": "The Bachelor of Technical-Vocational Teacher Education Drafting Technology (BTVTED-DT) is an undergraduate academic degree program that prepares students for careers in teaching and training in technical-vocational education and training (TVET) programs, with a focus on drafting technology. It combines education theory and pedagogy with specialized knowledge in drafting technology to equip students with the skills and competencies needed to effectively teach and train students in TVET programs.",
            "url": "https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fwww.msuiit.edu.ph%2Facademics%2Fcolleges%2Fced%2Fprograms%2Ftte%2FBTVTEd-Drafting-Tech-Form-5B-Latest.docx&wdOrigin=BROWSELINK",
            "display_name": "BACHELOR OF TECHNICAL-VOCATIONAL TEACHER EDUCATION DRAFTING TECHNOLOGY (BTVTED-DT)"
        },
        
        "BPED" : {
            "definition": "The Bachelor of Physical Education (BPED) is an undergraduate academic degree program that prepares students for careers in physical education and sports training. The program focuses on developing knowledge and skills related to physical fitness, sports science, and coaching techniques.",
            "url": "https://www.msuiit.edu.ph/academics/colleges/ced/programs/pe/Form%205B%20Bachelor%20of%20Physical%20Education.pdf",
            "display_name": "BACHELOR OF PHYSICAL EDUCATION (BPED)"
        },
        
        "BSED PHYS": {
            "definition": "The Bachelor of Secondary Education (Physics) is an undergraduate academic degree program designed to prepare students for careers as secondary school teachers, with a focus on physics education. The program combines education theory and pedagogy with specialized knowledge in physics to equip students with the skills and competencies needed to effectively teach physics to secondary school students.",
            "url": "https://www.msuiit.edu.ph/academics/colleges/ced/programs/sme/FORM%205B%20BSED%20Physics.pdf",
            "display_name": "BACHELOR OF SECONDARY EDUCATION (PHYSICS) - BSED(PHYS)"
        },
        
        "BSED MATH": {
            "definition": "The Bachelor of Secondary Education (Mathematics) is an undergraduate degree program that prepares students to teach mathematics at the secondary school level. The program focuses on developing pedagogical skills and mathematical knowledge to effectively instruct and engage students.",
            "url": "https://www.msuiit.edu.ph/academics/colleges/ced/programs/sme/Form%205B%20BSEd%20Mathematics.pdf",
            "display_name": "BACHELOR OF SECONDARY EDUCATION (MATHEMATICS) - BSED(MATH)"
        },
        
        "BEED SCI MAT": {
            "definition": "The Bachelor of Elementary Education (Science and Mathematics) is an undergraduate degree program that prepares students to teach science and mathematics at the elementary school level. The program combines education theory and pedagogy with specialized knowledge in science and mathematics to equip students with the skills and competencies needed to effectively teach these subjects to elementary school students.",
            "url": "https://www.msuiit.edu.ph/academics/colleges/ced/programs/sme/Form%205B%20BEED%20Sci%20and%20Math.pdf",
            "display_name": "BACHELOR OF SECONDARY EDUCATION (SCIENCE AND MATHEMATICS) - BEED(SCI MAT)"
        },
        
        "BSED FIL": {
            "definition": "The Bachelor of Secondary Education (Filipino) is an undergraduate degree program that prepares students to teach Filipino language and literature at the secondary school level. The program combines education theory and pedagogy with specialized knowledge in Filipino language and literature to equip students with the skills and competencies needed to effectively teach these subjects to secondary school students.",
            "url": "https://www.msuiit.edu.ph/academics/colleges/ced/programs/pre/Form%205B%20BSEd%20Filipino.pdf",
            "display_name": "BACHELOR OF SECONDARY EDUCATION (FILIPINO) - BSED(FIL)"
        },
        
        "BEED Lang Ed": {
            "definition": "The Bachelor of Elementary Education (Language Education) is an undergraduate degree program designed to prepare students to teach language arts at the elementary level. The program focuses on developing pedagogical skills and language proficiency to effectively instruct young learners.",
            "url": "https://www.msuiit.edu.ph/academics/colleges/ced/programs/pre/Form%205B%20BEEd%20Language%20Education.pdf",
            "display_name": "BACHELOR OF ELEMENTARY EDUCATION (LANGUAGE EDUCATION) - BEED(Lang Ed)"
        },
        
        "BTLED-HE": {
            "definition": "The Bachelor of Technology and Livelihood Education - Home Economics (BTLED-HE) is an undergraduate academic degree program that prepares students for careers in teaching and training in technical-vocational education and training (TVET) programs, with a focus on home economics. It combines education theory and pedagogy with specialized knowledge in home economics to equip students with the skills and competencies needed to effectively teach and train students in TVET programs.",
            "url": "https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fwww.msuiit.edu.ph%2Facademics%2Fcolleges%2Fced%2Fprograms%2Ftte%2FBTLEd-Home-Economics-Form-5B-Latest.docx&wdOrigin=BROWSELINK",
            "display_name": "BACHELOR OF TECHNOLOGY AND LIVELIHOOD EDUCATION - HOME ECONOMICS (BTLED-HE)"
        },

        #CASS        
        "BA POL SCI": {
            "definition": "The Bachelor of Arts in Political Science (BA POL SCI) is an undergraduate academic degree program that focuses on the study of political theories, institutions, processes, and policies. It prepares students for careers in government, international relations, public service, research, and other fields related to political science.",
            "url" : "https://www.msuiit.edu.ph/academics/colleges/cass/programs/political-science/ba-political-science.php",
            "display_name": "BACHELOR OF ARTS IN POLITICAL SCIENCE (BA POL SCI)"
        },
        
        "BA ELS": {
            "definition": "The Bachelor of Arts in English Language Studies (BA ELS) is an undergraduate academic degree program that focuses on the study of language, literature, and culture. It prepares students for careers in teaching, research, writing, editing, and other language-related fields.",
            "url" : "https://www.msuiit.edu.ph/academics/colleges/cass/programs/english/ba-english-studies.php",
            "display_name": "BACHELOR OF ARTS IN ENGLISH LANGUAGE STUDIES (BA ELS)"
        },
        
        "BS PSYCH": {
            "definition": "The Bachelor of Science in Psychology (BS PSYCH) is an undergraduate academic degree program that focuses on the scientific study of behavior and mental processes. It prepares students for careers in psychology, counseling, social work, and other fields related to mental health and human services.",
            "url" : "https://www.msuiit.edu.ph/academics/colleges/cass/programs/psychology/ba-psychology.php",
            "display_name": "BACHELOR OF SCIENCE IN PSYCHOLOGY (BS PSYCH)"
        },
        
        "BS PHIL": {
            "definition": "The Bachelor of Science in Philosophy (BS PHIL) is an undergraduate academic degree program that focuses on the study of fundamental questions about existence, knowledge, values, and reality. It prepares students for careers in law, education, research, and other fields that require critical thinking and problem-solving skills.",
            "url" : "https://www.msuiit.edu.ph/academics/colleges/cass/programs/philosophy-humanities/bs-philosophy-applied-ethics.php",
            "display_name": "BACHELOR OF SCIENCE IN PHILOSOPHY (BS PHIL)"
        },
        
        "BA PSYCH": {
            "definition": "The Bachelor of Arts in Psychology (BA PSYCH) is an undergraduate academic degree program that focuses on the study of human behavior and mental processes. It prepares students for careers in psychology, counseling, social work, and other fields related to mental health and human services.",
            "url": "https://www.msuiit.edu.ph/academics/colleges/cass/programs/psychology/ba-psychology.php",
            "display_name": "BACHELOR OF ARTS IN PSYCHOLOGY (BA PSYCH)"
        },
        
        "BA HISTORY": {
            "definition": "The Bachelor of Arts in History (BA HISTORY) is an undergraduate academic degree program that focuses on the study of past events and their impact on society. It prepares students for careers in education, research, and historical preservation.",
            "url": "https://www.msuiit.edu.ph/academics/colleges/cass/programs/history/international-track.php",
            "display_name": "BACHELOR OF SCIENCE IN HISTORY (BA HISTORY)"
        },
        
        "BA FIL": {
            "definition": "Ang Batsilyer Ng Sining sa Filipino (BA FIL) ay isang undergraduate na programa sa akademikong degree na nagbibigay ng komprehensibong edukasyon sa mga estudyante sa pag-aaral ng wikang Filipino. Nakatuon ito sa paghubog ng mga mag-aaral bilang mga mahusay na komunikador at kritikal na tagapagsaliksik sa larangan ng wika at panitikan ng Pilipinas.",
            "url": "https://www.msuiit.edu.ph/academics/colleges/cass/programs/filipino/ba-filipino.php",
            "display_name": "BATSILYER NG SINING SA FILIPINO (BA FIL)"
        }, 
        
        "BA SOCIO": {
            "definition": "The Bachelor of Arts in Sociology (BA SOCIO) is an undergraduate academic degree program that focuses on the study of human social behavior, relationships, and institutions. It prepares students for careers in social work, research, education, and other fields that require a deep understanding of human societies and social phenomena.",
            "url": "https://www.msuiit.edu.ph/academics/colleges/cass/programs/sociology/ba-sociology.php",
            "display_name": "BACHELOR OF ARTS IN SOCIOLOGY (BA SOCIO)"
        },

        #CEBA        
        "BSA": {
            "definition" : "The Bachelor of Science in Accountancy (BSA) is an undergraduate academic degree program that prepares students for careers in accounting, auditing, and finance. It provides students with a comprehensive education in accounting principles, theories, and practices, as well as the skills and knowledge needed to pass the Certified Public Accountant (CPA) licensure examination.",
            "url" : "https://www.msuiit.edu.ph/academics/colleges/cbaa/programs/accountancy/index.php#bs-a",
            "display_name" : "BACHELOR OF SCIENCE IN ACCOUNTANCY (BSA)"
        },
        
        "BS HM": {
            "definition" : "The Bachelor of Science in Hospitality Management (BS HM) is an undergraduate academic degree program that focuses on preparing students for careers in the hospitality industry. The program provides students with a solid foundation in hospitality operations and management.",
            "url" : "https://www.msuiit.edu.ph/academics/colleges/cbaa/programs/hm/index.php",
            "display_name" : "BACHELOR OF SCIENCE IN HOSPITALITY MANAGEMENT (BS HM)"
        },
        
        "BSBA-MKT MGT": {
            "definition" : "The Bachelor of Science in Business Administration with a major in Marketing Management is an undergraduate academic degree program that equips students with the knowledge and skills necessary to develop and implement effective marketing strategies in a rapidly changing business environment. This program focuses on the principles of marketing, including market research, consumer behavior, brand management, and digital marketing, preparing students for careers in marketing management, research, and other related fields.",
            "url" : "https://www.msuiit.edu.ph/academics/colleges/cbaa/programs/marketing/bsba-marketing.php",
            "display_name" : "BACHELOR OF SCIENCE IN BUSINESS ADMINISTRATION (MARKETING MANAGEMENT) - BSBA-MKT(MGT)"
        },
        
        "BS ECON": {
            "definition" : "The Bachelor of Science in Economics (BS ECON) is an undergraduate academic degree program that provides students with a comprehensive understanding of economic theories, principles, and practices. It prepares students for careers in government, business, finance, and international trade, as well as for further studies in economics, business, law, and other related fields.",
            "url" : "https://www.msuiit.edu.ph/academics/colleges/cbaa/programs/economics/bs-economics.php",
            "display_name" : "BACHELOR OF SCIENCE IN ECONOMICS (BS ECON)"
        },
        
        "BS ENTREP": {
            "definition" : "The Bachelor of Science in Entrepreneurship (BS ENTREP) is an undergraduate academic degree program that focuses on equipping students with the knowledge and skills needed to start and manage successful businesses. It prepares graduates for entrepreneurial endeavors and leadership roles in the business world.",
            "url" : "https://www.msuiit.edu.ph/academics/colleges/cbaa/programs/marketing/bs-entrepreneurship.php",
            "display_name" : "BACHELOR OF SCIENCE IN ENTREPRENEURSHIP (BS ENTREP)"
        },
        
        "BSBA-B.ECON": {
            "definition" : "The Bachelor of Science in Business Administration with a major in Business Economics is an undergraduate academic degree program that provides students with a comprehensive understanding of the principles and practices of business economics. It prepares students for careers in business, government, and international trade, as well as for further studies in business, economics, law, and other related fields.",
            "url" : "https://www.msuiit.edu.ph/academics/colleges/cbaa/programs/economics/bsba-business-economics.php",
            "display_name" : "BACHELOR OF SCIENCE IN BUSINESS ADMINISTRATION (BUSINESS ECONOMICS) - BSBA(B.ECON)"
        },

        # CCS
        "BSIT": {
            "definition": "The Bachelor of Science in Information Technology (BSIT) is an undergraduate academic degree program that provides students with a comprehensive understanding of the design, development, and management of information technology systems. Graduates of the program are prepared for careers as IT professionals, software developers, network administrators, database managers, and technology consultants, among others.",
            "url": "https://www.msuiit.edu.ph/academics/colleges/ccs/programs/it/bs-it.php",
            "display_name": "BACHELOR OF SCIENCE IN INFORMATION TECHNOLOGY (BSIT)"
        },
        "BSIS": {
            "definition": "The Bachelor of Science in Information Systems (BSIS) is an undergraduate academic degree program that provides students with a comprehensive understanding of the design, development, and management of information systems and technology. Graduates of the program are prepared for careers as information systems analysts, software developers, network administrators, database managers, and technology consultants, among others.",
            "url": "https://www.msuiit.edu.ph/academics/colleges/ccs/programs/it/bs-is.php",
            "display_name": "BACHELOR OF SCIENCE IN INFORMATION SYSTEMS (BSIS)"
        },
        "BSCS": {
            "definition": "The Bachelor of Science in Computer Science (BSCS) is an undergraduate academic degree program that provides students with a comprehensive understanding of computer science principles and technologies. Graduates of the program are prepared for careers as software developers, systems analysts, IT consultants, and technology professionals.",
            "url": "https://www.msuiit.edu.ph/academics/colleges/ccs/programs/cs/bs-cs.php",
            "display_name": "BACHELOR OF SCIENCE IN COMPUTER SCIENCE (BSCS)"
        },
        "BSCA": {
            "definition": "The Bachelor of Science in Computer Applications (BSCA) is an undergraduate academic degree program that provides students with a comprehensive understanding of computer applications and technology. Graduates of the program are prepared for careers as software developers, systems analysts, IT consultants, and technology professionals in various industries.",
            "url": "https://www.msuiit.edu.ph/academics/colleges/ccs/programs/com-apps/bs-com-apps.php",
            "display_name": "BACHELOR OF SCIENCE IN COMPUTER APPLICATIONS (BSCA)"
        }
    }

    return course_definitions.get(course_code, {
        "definition": "Definition not available for this course.",
        "url": "#",
        "display_name": course_code  # Default to the course_code if no match found
    })
