Follow the instruction, codes are provided in each number.

1. Create db and name it sasepasser, 
	
	CREATE DATABASE sasepasser;

2. Create table for authentication, name it users.

	CREATE TABLE users (
  		u_id SERIAL PRIMARY KEY, 
  		f_name VARCHAR(255),
  		m_name VARCHAR(255),
  		l_name VARCHAR(255),
  		password VARCHAR(255),
  		role VARCHAR(255) DEFAULT 'student',
  		s_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  		email VARCHAR(255),
        status VARCHAR(10) DEFAULT 'unverified',
        email_verified BOOLEAN DEFAULT FALSE,
        verification_token VARCHAR(255),
        reset_password_token VARCHAR(255)
		);

3. REGISTER account for admin, and in the PgAdmin4, update the `role` = 'admin', `email` = 'verified', and `status` = 'verified'.


4. Create table for student profile, name it `student_profile`

	CREATE TABLE student_profile (
    	s_id INT REFERENCES users(u_id),
        contact VARCHAR(20),
    	sex VARCHAR(10),
        working_student VARCHAR(5),
        working__id VARCHAR(225),
        lgbtq_parent VARCHAR(5),
        lgbtq_p_id VARCHAR(225),
        victim VARCHAR(5),
        victim_id VARCHAR(225),
        religion VARCHAR(100),
        pwd VARCHAR (5),
        pwd_id_file VARCHAR (255),
        childsoloparent VARCHAR(5),
        childsoloparent_file VARCHAR (255),
        ip VARCHAR (25),
        ip_id VARCHAR (255),
        "1stgenlearner" VARCHAR (100),
        "1stgenlearner_id" VARCHAR (255),
        child_deprived_liberty VARCHAR(5),
        child_deprived_liberty_id VARCHAR(255),
        soloparent VARCHAR(5),
        soloparent_id VARCHAR(255),
        province_home VARCHAR(100),
    	city_home VARCHAR(100),
    	track VARCHAR(100),
    	name_hs VARCHAR(100),
    	address_hs VARCHAR(100),
        father_edu_attain VARCHAR(100),
        mother_edu_attain VARCHAR(100),
        father_occupation VARCHAR(100),
        mother_occupation VARCHAR(100),
    	father VARCHAR(100),
    	mother VARCHAR(100),
        bothparentsworking VARCHAR(5),
        father_itr_file VARCHAR(255),
        mother_itr_file VARCHAR(255),
    	father_tribe VARCHAR(100),
    	mother_tribe VARCHAR(100),
        pref_course1 VARCHAR(100),
        pref_course2 VARCHAR(100),
        permit_number varchar(100),
    	ap FLOAT,
    	lu FLOAT,
    	ma FLOAT,
    	sc FLOAT,
        verified_grades VARCHAR (255)
	);

5. Create table for junior high school grades, name it `student_grade_hs`

    CREATE TABLE student_grade_hs (
        g_hs_id INT REFERENCES users(u_id),
        filipino9 VARCHAR(5),
        english9 VARCHAR(5),
        mathematics9 VARCHAR(5),
        science9 VARCHAR(5),
        aralingpanlipunan9	VARCHAR(5),	
        edukasyonsapagpapakatao9 VARCHAR(5),
        music9 VARCHAR(5),
        arts9 VARCHAR(5),
        physicaleducation9 VARCHAR(5), 		
        health9 VARCHAR(5),		
        edukasyongpantahananatpangkabuhayan9 VARCHAR(5),	
        technologyandlivelihoodeducation9 VARCHAR(5),
        filipino10 VARCHAR(5),	
        english10 VARCHAR(5),
        mathematics10 VARCHAR(5),
        science10 VARCHAR(5),
        aralingpanlipunan10 VARCHAR(5),
        edukasyonsapagpapakatao10 VARCHAR(5),	
        music10	VARCHAR(5),
        arts10	VARCHAR(5),
        physicaleducation10 VARCHAR(5),		
        health10 VARCHAR(5),
        edukasyongpantahananatpangkabuhayan10 VARCHAR(5),
        technologyandlivelihoodeducation10 VARCHAR(5)
    );

6. Create table for student grade SHS, name it `student_grade_shs`

	CREATE TABLE student_grade_shs (
	    g_shs_id INT REFERENCES users(u_id),
        oralcommunication VARCHAR(5),
        reading_and_writing VARCHAR(5),
        generalmath VARCHAR(5),
        statisticsandprobability VARCHAR(5),
        earthandlifescience VARCHAR(5),
        physicalscience VARCHAR(5),
        earthscience VARCHAR(5),
        personaldevelopment VARCHAR(5),
        mediaandinformationliteracy VARCHAR(5),
        introductiontothephilosophyofthehumanperson VARCHAR(5),
        understandingculturesocietyandpolitics VARCHAR(5),
        disasterreadinessandrisk_reduction VARCHAR(5),
        contemporaryphilippineartsfromtheregions VARCHAR(5),
        t21stcenturyliteraturefromthephilippinesandtheworld VARCHAR(5),
        pagbasaatpagsusuringibatibangtekstotungosapananaliksik VARCHAR(5),
        komunikasyonatpananaliksiksawikaatkulturangpilipino VARCHAR(5),
        physicaleducationandhealth VARCHAR(5),
        physicaleducationandhealth2 VARCHAR(5),
        physicaleducationandhealth3 VARCHAR(5),
        physicaleducationandhealth4 VARCHAR(5),
        appliedeconomicsbusiness VARCHAR(5),
        ethicsandsocial_responsibility VARCHAR(5),
        f1_fundamentalsofaccountancybusinessandmanagement1 VARCHAR(5),
        f2_fundamentalsofaccountancybusinessandmanagement2 VARCHAR(5),
        businessmath VARCHAR(5),
        businessfinance VARCHAR(5),
        organizationandmanagement VARCHAR(5),
        principlesofmarketing VARCHAR(5),
        businessmarketing VARCHAR(5),
        businessenterpriseandsimulation VARCHAR(5),
        precalculus VARCHAR(5),
        basiccalculus VARCHAR(5),
        genbio1 VARCHAR(5),
        genbio2 VARCHAR(5),
        genphysics1 VARCHAR(5),
        genphysics2 VARCHAR(5),
        genchem1 VARCHAR(5),
        genchem2 VARCHAR(5),
        humanities1_politics VARCHAR(5),
        humanities2_intro VARCHAR(5),
        socialscience1 VARCHAR(5),
        organizationandmanagement2 VARCHAR(5),
        appliedeconomics2 VARCHAR(5),
        introtoworldreligionsandsytembeliefs VARCHAR(5),
        creativewriting VARCHAR(5),
        philippinepiliticsandgovernance VARCHAR(5),
        creativewriting_malikhaing_pagsulat VARCHAR(5),
        creativenonfiction VARCHAR(5),
        introductiontoworldreligionsandbeliefsystems VARCHAR(5),
        community_engagementsolidarityandcitizenship VARCHAR(5),
        philippinepoliticsandgovernance VARCHAR(5),
        disciplinesandideasinthesocialsciences VARCHAR(5),
        safetyandfirstaid VARCHAR(5),
        humanmovement VARCHAR(5),
        fundamentalsofcoaching VARCHAR(5)
        );

7. Create table for the courses recommended. name it "recommended_course"

        CREATE TABLE recommended_course (
            rc_id INT REFERENCES users(u_id),
            weighted_avg FLOAT,
            rc1 TEXT,
            rc2 TEXT,
            rc3 TEXT,
            rc4 TEXT,
            rc5 TEXT,
            rc6 TEXT,
            rc7 TEXT,
            rc8 TEXT,
            rc9 TEXT,
            rc10 TEXT
);

8. Create table for the application. name it "applications"
        
        CREATE TABLE applications (
            application_id SERIAL PRIMARY KEY,
            student_id INT NOT NULL,
            hs_grades_filled BOOLEAN NOT NULL,
            shs_grades_filled BOOLEAN NOT NULL,
            edi_filled BOOLEAN NOT NULL,
            parent_info_filled BOOLEAN NOT NULL,
            verified_grades BOOLEAN NOT NULL,
            status VARCHAR(20) DEFAULT 'Pending',
            submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES student_profile(s_id)
        );
                    
                