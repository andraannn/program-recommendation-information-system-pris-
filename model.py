import pandas as pd
from admissions_predictor import prediction_per_program
from recommendation_logic import recommend_program
import argparse
from db import conn

# Function to fetch data from PostgreSQL and convert it to a list of dictionaries
def get_data_from_postgresql(query, params=None):
    try:

        # Fetch data using parameters
        data = pd.read_sql(query, conn, params=params)
        
        # List of grade columns
        grade_columns = [
            'oralcommunication', 'reading_and_writing', 'generalmath', 'statisticsandprobability', 
            'earthandlifescience', 'physicalscience', 'earthscience', 'personaldevelopment', 
            'mediaandinformationliteracy', 'introductiontothephilosophyofthehumanperson', 
            'understandingculturesocietyandpolitics', 'disasterreadinessandrisk_reduction', 
            'contemporaryphilippineartsfromtheregions', 't21stcenturyliteraturefromthephilippinesandtheworld', 
            'pagbasaatpagsusuringibatibangtekstotungosapananaliksik', 'komunikasyonatpananaliksiksawikaatkulturangpilipino', 
            'physicaleducationandhealth', 'physicaleducationandhealth2', 'physicaleducationandhealth3', 
            'physicaleducationandhealth4', 'appliedeconomicsbusiness', 'ethicsandsocial_responsibility', 
            'f1_fundamentalsofaccountancybusinessandmanagement1', 'f2_fundamentalsofaccountancybusinessandmanagement2', 
            'businessmath', 'businessfinance', 'organizationandmanagement', 'principlesofmarketing', 
            'businessmarketing', 'businessenterpriseandsimulation', 'precalculus', 'basiccalculus', 'genbio1', 
            'genbio2', 'genphysics1', 'genphysics2', 'genchem1', 'genchem2', 'humanities1_politics', 
            'humanities2_intro', 'socialscience1', 'organizationandmanagement2', 'appliedeconomics2', 
            'introtoworldreligionsandsytembeliefs', 'creativewriting', 'philippinepiliticsandgovernance', 
            'creativewriting_malikhaing_pagsulat', 'creativenonfiction', 'introductiontoworldreligionsandbeliefsystems', 
            'community_engagementsolidarityandcitizenship', 'philippinepoliticsandgovernance', 
            'disciplinesandideasinthesocialsciences', 'safetyandfirstaid', 'humanmovement', 'fundamentalsofcoaching'
        ]
        
        # Convert specified fields to numeric, setting invalid values to NaN
        for col in grade_columns:
            if col in data.columns:  # Check if column exists in data
                data[col] = pd.to_numeric(data[col], errors='coerce')
                
    except Exception as e:
        print(f"Error fetching data from PostgreSQL: {e}")
        return None
    
    return data.to_dict(orient='records')

# Function to insert recommendations into PostgreSQL
def insert_recommendations_into_postgresql(conn, recommendations, student_id):
    try:
        # Prepare SQL insert statement
        insert_query = '''
        INSERT INTO recommended_course (rc_id, weighted_avg, rc1, rc2, rc3, rc4, rc5, rc6, rc7, rc8, rc9, rc10)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''

        # Extract the top recommendations
        top_recs = recommendations.head(10)  # Only take the top 10 recommendations
        weighted_avg = top_recs['Final_Score'].mean() if 'Final_Score' in top_recs else 0

        # Prepare the values for insertion
        values = [
            student_id,  # rc_id
            weighted_avg,
        ] + top_recs['Program'].tolist() + [None] * (10 - len(top_recs))  # Fill the remaining with None if less than 10

        # Execute insert statement
        with conn.cursor() as cursor:
            cursor.execute(insert_query, values)
            conn.commit()  # Commit the changes

    except Exception as e:
        print(f"Error inserting recommendations into PostgreSQL: {e}")

# Function to update recommendations in PostgreSQL
def update_recommendations_in_postgresql(conn, recommendations, student_id):
    try:
        cursor = conn.cursor()

        # Prepare SQL update statement
        update_query = '''
        UPDATE recommended_course
        SET weighted_avg = %s, rc1 = %s, rc2 = %s, rc3 = %s, rc4 = %s, 
            rc5 = %s, rc6 = %s, rc7 = %s, rc8 = %s, rc9 = %s, rc10 = %s
        WHERE rc_id = %s;
        '''

        # Extract the top recommendations
        top_recs = recommendations.head(10)  # Only take the top 10 recommendations
        weighted_avg = top_recs['Final_Score'].mean() if 'Final_Score' in top_recs else 0

        # Prepare the values for update
        values = [
            weighted_avg,
        ] + top_recs['Program'].tolist() + [None] * (10 - len(top_recs))  # Fill the remaining with None if less than 10
        values.append(student_id)  # Add student ID for the WHERE clause

        # Execute the update statement
        cursor.execute(update_query, values)
        
        # Commit changes
        conn.commit()

    except Exception as e:
        print(f"Error updating recommendations in PostgreSQL: {e}")
        conn.rollback()  # Rollback in case of error

    finally:
        cursor.close()

# Main function that processes data and makes recommendations
def main(data, prefered_course, n_rec=10):
    data: pd.DataFrame = prediction_per_program(data)  # Get predictions per program
    recommendations: pd.DataFrame = recommend_program(data, prefered_course, n_rec=n_rec)  # Get recommendations
    return recommendations

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process student data and recommend programs.")
    parser.add_argument('--n_rec', type=int, default=10, help='Number of recommendations to generate (default: 10)')
    parser.add_argument('--output_path', type=str, default='./', help='Path to the output CSV file (default: Current Directory)')

    args = parser.parse_args()

    # SQL query to retrieve student data
    query = ''' 
    SELECT sp.s_id, sp.sex, sp.religion, sp.city_home, sp.province_home, sp.track, sp.name_hs, sp.address_hs, sp.father_occupation, 
       sp.mother_occupation, sp.father_tribe, sp.mother_tribe, sp.ap, sp.lu, sp.ma, sp.sc, sp.pref_course1, sp.pref_course2,
       CAST(sg.oralcommunication AS INTEGER), CAST(sg.reading_and_writing AS INTEGER), 
       CAST(sg.generalmath AS INTEGER), CAST(sg.statisticsandprobability AS INTEGER), 
       CAST(sg.earthandlifescience AS INTEGER), CAST(sg.physicalscience AS INTEGER), 
       CAST(sg.earthscience AS INTEGER), CAST(sg.personaldevelopment AS INTEGER), 
       CAST(sg.mediaandinformationliteracy AS INTEGER), CAST(sg.introductiontothephilosophyofthehumanperson AS INTEGER), 
       CAST(sg.understandingculturesocietyandpolitics AS INTEGER), CAST(sg.disasterreadinessandrisk_reduction AS INTEGER), 
       CAST(sg.contemporaryphilippineartsfromtheregions AS INTEGER), CAST(sg.t21stcenturyliteraturefromthephilippinesandtheworld AS INTEGER), 
       CAST(sg.pagbasaatpagsusuringibatibangtekstotungosapananaliksik AS INTEGER), 
       CAST(sg.komunikasyonatpananaliksiksawikaatkulturangpilipino AS INTEGER), 
       CAST(sg.physicaleducationandhealth AS INTEGER), CAST(sg.physicaleducationandhealth2 AS INTEGER), 
       CAST(sg.physicaleducationandhealth3 AS INTEGER), CAST(sg.physicaleducationandhealth4 AS INTEGER), 
       CAST(sg.appliedeconomicsbusiness AS INTEGER), CAST(sg.ethicsandsocial_responsibility AS INTEGER), 
       CAST(sg.f1_fundamentalsofaccountancybusinessandmanagement1 AS INTEGER), 
       CAST(sg.f2_fundamentalsofaccountancybusinessandmanagement2 AS INTEGER), 
       CAST(sg.businessmath AS INTEGER), CAST(sg.businessfinance AS INTEGER), 
       CAST(sg.organizationandmanagement AS INTEGER), CAST(sg.principlesofmarketing AS INTEGER), 
       CAST(sg.businessmarketing AS INTEGER), CAST(sg.businessenterpriseandsimulation AS INTEGER), 
       CAST(sg.precalculus AS INTEGER), CAST(sg.basiccalculus AS INTEGER), CAST(sg.genbio1 AS INTEGER), 
       CAST(sg.genbio2 AS INTEGER), CAST(sg.genphysics1 AS INTEGER), CAST(sg.genphysics2 AS INTEGER), 
       CAST(sg.genchem1 AS INTEGER), CAST(sg.genchem2 AS INTEGER), CAST(sg.humanities1_politics AS INTEGER), 
       CAST(sg.humanities2_intro AS INTEGER), CAST(sg.socialscience1 AS INTEGER), 
       CAST(sg.organizationandmanagement2 AS INTEGER), CAST(sg.appliedeconomics2 AS INTEGER), 
       CAST(sg.introtoworldreligionsandsytembeliefs AS INTEGER), CAST(sg.creativewriting AS INTEGER), 
       CAST(sg.philippinepiliticsandgovernance AS INTEGER), CAST(sg.creativewriting_malikhaing_pagsulat AS INTEGER), 
       CAST(sg.creativenonfiction AS INTEGER), CAST(sg.introductiontoworldreligionsandbeliefsystems AS INTEGER), 
       CAST(sg.community_engagementsolidarityandcitizenship AS INTEGER), CAST(sg.philippinepoliticsandgovernance AS INTEGER), 
       CAST(sg.disciplinesandideasinthesocialsciences AS INTEGER), CAST(sg.safetyandfirstaid AS INTEGER), 
       CAST(sg.humanmovement AS INTEGER), CAST(sg.fundamentalsofcoaching AS INTEGER)
    FROM student_profile sp
    JOIN student_grade_shs sg ON sp.s_id = sg.g_shs_id
    '''

    # Fetch data from PostgreSQL
    student_records = get_data_from_postgresql(query)

    if student_records:

        for student in student_records:
            id = student.pop('s_id')  # Use student ID
            prefered_courses = [student.pop('pref_course1'), student.pop('pref_course2')]  # Extract preferred courses
            recs = main(student, prefered_course=prefered_courses, n_rec=args.n_rec)
            recs["id"] = id  # Add the student ID back to the recommendations

            # Insert recommendations into the PostgreSQL table
            insert_recommendations_into_postgresql(conn, recs, id)

        # Close the connection after all inserts
        conn.close()
    else:
        print("No data retrieved from PostgreSQL.")