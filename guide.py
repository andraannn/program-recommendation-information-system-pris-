        # earthandlifescience = request.form['EarthAndLifeScience']
        # physicalscience = request.form['PhysicalScience']
        # earthscience = request.form['EarthScience']
        # genbio1  = request.form['GenBio1']
        # genbio2  = request.form['GenBio2']
        # genphysics1 = request.form['GenPhysics1']
        # genphysics2 = request.form['GenPhysics2']
        # genchem1 = request.form['GenChem1']
        # genchem2 = request.form['GenChem2']
        # generalmath = request.form['GeneralMath']
        # statisticsandprobability = request.form['StatisticsAndProbability']
        # precalculus = request.form['PreCalculus']
        # basiccalculus = request.form['BasicCalculus']
        # oralcommunication = request.form['OralCommunication']
        # reading_and_writing = request.form['Reading_and_Writing']
        # mediaandinformationliteracy = request.form['MediaandInformationLiteracy']
        # t21stcenturyliteraturefromthephilippinesandtheworld = request.form['t21stCenturyLiteratureFromThePhilippinesAndTheWorld']
        # contemporaryphilippineartsfromtheregions = request.form['ContemporaryPhilippineArtsFromTheRegions']
        # pagbasaatpagsusuringibatibangtekstotungosapananaliksik = request.form['PagbasaAtPagsusuriNgIbatIbangTekstoTungoSaPananaliksik']
        # komunikasyonatpananaliksiksawikaatkulturangpilipino = request.form['KomunikasyonAtPananaliksikSaWikaAtKulturangPilipino']
        # personaldevelopment = request.form['PersonalDevelopment']
        # introductiontothephilosophyofthehumanperson = request.form['IntroductionToThePhilosophyOfTheHumanPerson']
        # understandingculturesocietyandpolitics = request.form['UnderstandingCultureSocietyAndPolitics']
        # disasterreadinessandrisk_reduction = request.form['DisasterReadinessAndRisk_Reduction']
        # physicaleducationandhealth = request.form['PhysicalEducationAndHealth']
        # physicaleducationandhealth2 = request.form['PhysicalEducationAndHealth2']
        # physicaleducationandhealth3 = request.form['PhysicalEducationandHealth3']
        # physicaleducationandhealth4 = request.form['PhysicalEducationAndHealth4']
        # businessmath = request.form['BusinessMath']
        # businessfinance = request.form['BusinessFinance']
        # organizationandmanagement  = request.form['OrganizationAndManagement']
        # principlesofmarketing = request.form['PrinciplesOfMarketing']
        # businessmarketing = request.form['BusinessMarketing']
        # businessenterpriseandsimulation = request.form['BusinessEnterpriseAndSimulation']
        # f1_fundamentalsofaccountancybusinessandmanagement1 = request.form['F1_FundamentalsOfAccountancyBusinessAndManagement1']
        # f2_fundamentalsofaccountancybusinessandmanagement2 = request.form['F2_FundamentalsofAccountancyBusinessAndManagement2']
        # appliedeconomicsbusiness = request.form['AppliedEconomicsBusiness']
        # ethicsandsocial_responsibility = request.form['EthicsAndSocial_Responsibility']
        # creativenonfiction = request.form['CreativeNonfiction']
        # creativewriting_malikhaing_pagsulat = request.form['CreativeWriting_Malikhaing_Pagsulat']
        # introductiontoworldreligionsandbeliefsystems = request.form['IntroductionToWorldReligionsAndBeliefSystems']
        # community_engagementsolidarityandcitizenship = request.form['Community_EngagementSolidarityAndCitizenship']
        # philippinepoliticsandgovernance = request.form['PhilippinePoliticsandGovernance']
        # disciplinesandideasinthesocialsciences = request.form['DisciplinesAndIdeasInTheSocialSciences']
        # creativewriting = request.form['CreativeWriting']
        # humanities1_politics = request.form['Humanities1_Politics']
        # humanities2_intro = request.form['Humanities2_intro']
        # socialscience1 = request.form['Humanities2_intro']
        # socialscience1 = request.form['SocialScience1']
        # organizationandmanagement2 = request.form['OrganizationAndManagement2']
        # appliedeconomics2 = request.form['AppliedEconomics2']
        # introtoworldreligionsandsytembeliefs = request.form['IntroToWorldReligionsAndSytemBeliefs']
        # philippinepiliticsandgovernance = request.form['PhilippinePiliticsAndGovernance']
        # safetyandfirstaid = request.form['SafetyAndFirstAid']
        # humanmovement = request.form['HumanMovement']
        # fundamentalsofcoaching  = request.form['FundamentalsOfCoaching']


       # Insert data into student_grade table
#         # Set grades not related to the chosen track as NULL
#         if track == 'STEM':
#             # Insert grades for STEM track, set others to NULL
#             cursor.execute("""
#                 INSERT INTO student_grade (g_id, 
#                                             earthandlifescience,
#                                             physicalscience,
#                                             earthscience,
#                                             genbio1,
#                                             genbio2,
#                                             genphysics1,
#                                             genphysics2,
#                                             genchem1,
#                                             genchem2,
#                                             generalmath,
#                                             statisticsandprobability,
#                                             precalculus,
#                                             basiccalculus,

#                                             oralcommunication,
#                                             reading_and_writing,
#                                             mediaandinformationliteracy,
#                                             t21stcenturyliteraturefromthephilippinesandtheworld,
#                                             contemporaryphilippineartsfromtheregions,

#                                             pagbasaatpagsusuringibatibangtekstotungosapananaliksik,
#                                             komunikasyonatpananaliksiksawikaatkulturangpilipino,
#                                             personaldevelopment,
#                                             introductiontothephilosophyofthehumanperson,
#                                             understandingculturesocietyandpolitics,
#                                             disasterreadinessandrisk_reduction,
#                                             physicaleducationandhealth,
#                                             physicaleducationandhealth2,
#                                             physicaleducationandhealth3,
#                                             physicaleducationandhealth4)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#             """, (u_id, earthandlifescience, physicalscience,
#                                             earthscience,
#                                             genbio1,
#                                             genbio2,
#                                             genphysics1,
#                                             genphysics2,
#                                             genchem1,
#                                             genchem2,
#                                             generalmath,
#                                             statisticsandprobability,
#                                             precalculus,
#                                             basiccalculus,

#                                             oralcommunication,
#                                             reading_and_writing,
#                                             mediaandinformationliteracy,
#                                             t21stcenturyliteraturefromthephilippinesandtheworld,
#                                             contemporaryphilippineartsfromtheregions,

#                                             pagbasaatpagsusuringibatibangtekstotungosapananaliksik,
#                                             komunikasyonatpananaliksiksawikaatkulturangpilipino,
#                                             personaldevelopment,
#                                             introductiontothephilosophyofthehumanperson,
#                                             understandingculturesocietyandpolitics,
#                                             disasterreadinessandrisk_reduction,
#                                             physicaleducationandhealth,
#                                             physicaleducationandhealth2,
#                                             physicaleducationandhealth3,
#                                             physicaleducationandhealth4 ))
#         elif track == 'ABM':
#             # Insert grades for ABM track, set others to NULL
#             cursor.execute("""
#                 INSERT INTO student_grade (g_id, 
# earthandlifescience,
# physicalscience,
# earthscience,

# generalmath,
# statisticsandprobability,
# businessmath,
# businessfinance,

# oralcommunication,
# reading_and_writing,
# mediaandinformationliteracy,
# t21stcenturyliteraturefromthephilippinesandtheworld,
# contemporaryphilippineartsfromtheregions,

# pagbasaatpagsusuringibatibangtekstotungosapananaliksik,
# komunikasyonatpananaliksiksawikaatkulturangpilipino,
# personaldevelopment,
# introductiontothephilosophyofthehumanperson,
# understandingculturesocietyandpolitics,
# disasterreadinessandrisk_reduction,
# physicaleducationandhealth,
# physicaleducationandhealth2,
# physicaleducationandhealth3,
# physicaleducationandhealth4,
# organizationandmanagement,
# principlesofmarketing,
# businessmarketing,
# businessenterpriseandsimulation,
# f1_fundamentalsofaccountancybusinessandmanagement1,
# f2_fundamentalsofaccountancybusinessandmanagement2,
# appliedeconomicsbusiness,
# ethicsandsocial_responsibility)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,)
#             """, (u_id, 
# earthandlifescience,
# physicalscience,
# earthscience,

# generalmath,
# statisticsandprobability,
# businessmath,
# businessfinance,

# oralcommunication,
# reading_and_writing,
# mediaandinformationliteracy,
# t21stcenturyliteraturefromthephilippinesandtheworld,
# contemporaryphilippineartsfromtheregions,

# pagbasaatpagsusuringibatibangtekstotungosapananaliksik,
# komunikasyonatpananaliksiksawikaatkulturangpilipino,
# personaldevelopment,
# introductiontothephilosophyofthehumanperson,
# understandingculturesocietyandpolitics,
# disasterreadinessandrisk_reduction,
# physicaleducationandhealth,
# physicaleducationandhealth2,
# physicaleducationandhealth3,
# physicaleducationandhealth4,
# organizationandmanagement,
# principlesofmarketing,
# businessmarketing,
# businessenterpriseandsimulation,
# f1_fundamentalsofaccountancybusinessandmanagement1,
# f2_fundamentalsofaccountancybusinessandmanagement2,
# appliedeconomicsbusiness,
# ethicsandsocial_responsibility))
       
#         elif track == 'HUMSS':
#             # Insert grades for HUMSS track, set others to NULL
#             cursor.execute("""
#                 INSERT INTO student_grade (g_id, 
# earthandlifescience,
# physicalscience,
# earthscience,

# generalmath,
# statisticsandprobability,
# oralcommunication,
# reading_and_writing,
# mediaandinformationliteracy,
# t21stcenturyliteraturefromthephilippinesandtheworld,
# contemporaryphilippineartsfromtheregions,
# creativenonfiction,

# pagbasaatpagsusuringibatibangtekstotungosapananaliksik,
# komunikasyonatpananaliksiksawikaatkulturangpilipino,

# creativewriting_malikhaing_pagsulat,

# personaldevelopment,
# introductiontothephilosophyofthehumanperson,
# understandingculturesocietyandpolitics,
# disasterreadinessandrisk_reduction,
# physicaleducationandhealth,
# physicaleducationandhealth2,
# physicaleducationandhealth3,
# physicaleducationandhealth4,
# introductiontoworldreligionsandbeliefsystems,
# community_engagementsolidarityandcitizenship,
# philippinepoliticsandgovernance,
# disciplinesandideasinthesocialsciences)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#             """, (u_id, earthandlifescience,
# physicalscience,
# earthscience,

# generalmath,
# statisticsandprobability,
# oralcommunication,
# reading_and_writing,
# mediaandinformationliteracy,
# t21stcenturyliteraturefromthephilippinesandtheworld,
# contemporaryphilippineartsfromtheregions,
# creativenonfiction,

# pagbasaatpagsusuringibatibangtekstotungosapananaliksik,
# komunikasyonatpananaliksiksawikaatkulturangpilipino,

# creativewriting_malikhaing_pagsulat,

# personaldevelopment,
# introductiontothephilosophyofthehumanperson,
# understandingculturesocietyandpolitics,
# disasterreadinessandrisk_reduction,
# physicaleducationandhealth,
# physicaleducationandhealth2,
# physicaleducationandhealth3,
# physicaleducationandhealth4,
# introductiontoworldreligionsandbeliefsystems,
# community_engagementsolidarityandcitizenship,
# philippinepoliticsandgovernance,
# disciplinesandideasinthesocialsciences))
            
#         elif track == 'GAS':
#             # Insert grades for GAS track, set others to NULL
#             cursor.execute("""
#                 INSERT INTO student_grade (g_id,
# earthandlifescience,
# physicalscience,
# earthscience,

# generalmath,
# statisticsandprobability,

# oralcommunication,
# reading_and_writing,
# mediaandinformationliteracy,
# t21stcenturyliteraturefromthephilippinesandtheworld,
# contemporaryphilippineartsfromtheregions,
# creativewriting,

# pagbasaatpagsusuringibatibangtekstotungosapananaliksik,
# komunikasyonatpananaliksiksawikaatkulturangpilipino,

# personaldevelopment,
# introductiontothephilosophyofthehumanperson,
# understandingculturesocietyandpolitics,
# disasterreadinessandrisk_reduction,
# physicaleducationandhealth,
# physicaleducationandhealth2,
# physicaleducationandhealth3,
# physicaleducationandhealth4,
# humanities1_politics,
# humanities2_intro,
# socialscience1,
# organizationandmanagement2,
# appliedeconomics2,
# introtoworldreligionsandsytembeliefs,
# philippinepiliticsandgovernance)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#             """, (u_id, earthandlifescience,
# physicalscience,
# earthscience,

# generalmath,
# statisticsandprobability,

# oralcommunication,
# reading_and_writing,
# mediaandinformationliteracy,
# t21stcenturyliteraturefromthephilippinesandtheworld,
# contemporaryphilippineartsfromtheregions,
# creativewriting,

# pagbasaatpagsusuringibatibangtekstotungosapananaliksik,
# komunikasyonatpananaliksiksawikaatkulturangpilipino,

# personaldevelopment,
# introductiontothephilosophyofthehumanperson,
# understandingculturesocietyandpolitics,
# disasterreadinessandrisk_reduction,
# physicaleducationandhealth,
# physicaleducationandhealth2,
# physicaleducationandhealth3,
# physicaleducationandhealth4,
# humanities1_politics,
# humanities2_intro,
# socialscience1,
# organizationandmanagement2,
# appliedeconomics2,
# introtoworldreligionsandsytembeliefs,
# philippinepiliticsandgovernance))
            
#         elif track == 'TVL':
#             # Insert grades for TVL track, set others to NULL
#             cursor.execute("""
#                 INSERT INTO student_grade (g_id,
# earthandlifescience,
# physicalscience,
# earthscience,

# generalmath,
# statisticsandprobability,

# oralcommunication,
# reading_and_writing,
# mediaandinformationliteracy,
# t21stcenturyliteraturefromthephilippinesandtheworld,
# contemporaryphilippineartsfromtheregions,
# creativewriting,

# pagbasaatpagsusuringibatibangtekstotungosapananaliksik,
# komunikasyonatpananaliksiksawikaatkulturangpilipino,

# personaldevelopment,
# introductiontothephilosophyofthehumanperson,
# understandingculturesocietyandpolitics,
# disasterreadinessandrisk_reduction,
# physicaleducationandhealth,
# physicaleducationandhealth2,
# physicaleducationandhealth3,
# physicaleducationandhealth4,
# safetyandfirstaid,
# humanmovement,
# fundamentalsofcoaching )
#                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#             """, (u_id, earthandlifescience,
# physicalscience,
# earthscience,

# generalmath,
# statisticsandprobability,

# oralcommunication,
# reading_and_writing,
# mediaandinformationliteracy,
# t21stcenturyliteraturefromthephilippinesandtheworld,
# contemporaryphilippineartsfromtheregions,
# creativewriting,

# pagbasaatpagsusuringibatibangtekstotungosapananaliksik,
# komunikasyonatpananaliksiksawikaatkulturangpilipino,

# personaldevelopment,
# introductiontothephilosophyofthehumanperson,
# understandingculturesocietyandpolitics,
# disasterreadinessandrisk_reduction,
# physicaleducationandhealth,
# physicaleducationandhealth2,
# physicaleducationandhealth3,
# physicaleducationandhealth4,
# safetyandfirstaid,
# humanmovement,
# fundamentalsofcoaching ))