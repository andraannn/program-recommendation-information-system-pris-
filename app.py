from flask import Flask, request, session, g, redirect, url_for, render_template, flash, jsonify, send_file
import time
import json
from flask_mail import Message
from datetime import datetime, timedelta
import secrets
import psycopg2 
import psycopg2.extras
import re 
from werkzeug.security import generate_password_hash, check_password_hash
from db import conn
from email_verification import send_verification_email
from mail import mail
from forgot_password import send_password_reset_email
from werkzeug.utils import secure_filename
import os
import io
import pandas as pd
import uuid
from allowed_file import allowed_file
from model import main, insert_recommendations_into_postgresql, get_data_from_postgresql, update_recommendations_in_postgresql
from course_definition import get_course_definition


app = Flask(__name__)
app.secret_key = 'PRIS'
 
# Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'pris.msuiit@gmail.com'
app.config['MAIL_PASSWORD'] = 'rkuc wbtd fpyp mwog'
app.config['MAIL_DEFAULT_SENDER'] = 'pris.msuiit@gmail.com'

# UPLOAD FOLDER
app.config['UPLOAD_FOLDER'] = 'static/student_uploads/'

# Initialize Mail
mail.init_app(app)

UPLOAD_FOLDER = 'static/student_uploads/'
 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

'''Landing Pages Routes------------------------------------------------'''
#index.html 
@app.route('/')
def index():

    return render_template('index.html')

#about.html 
@app.route('/about')
def about():
    
    return render_template('about.html')

#courses.html 
@app.route('/programs')
def courses():
    
    return render_template('courses.html')
'''---------------------------------------------------------------------------'''


'''Authentication functions--------------------------------------------------'''

#login.html 
@app.route('/login', methods=['GET', 'POST'])
def login():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    # Check if "email" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        print(password)
 
        # Check if account exists in the users table
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        account = cursor.fetchone()
 
        if account:
            password_rs = account['password']
            print(password_rs)
            
            # Check if email is verified
            if account['email_verified']:
                # If account exists in users table in our database
                if check_password_hash(password_rs, password):
                    # Create session data, we can access this data in other routes
                    session['loggedin'] = True
                    session['u_id'] = account['u_id']
                    session['f_name'] = account['f_name']
                    session['m_name'] = account['m_name']
                    session['l_name'] = account['l_name']
                    session['email'] = account['email']
                    session['role'] = account['role']

                    # Redirect based on the user's role
                    if session['role'] == 'admin':
                        return redirect(url_for('admin_dashboard'))
                    elif session['role'] == 'student':
                        return redirect(url_for('student_dashboard'))
                    else:
                        flash('Invalid user role')
                else:
                    # Account exists but password is incorrect
                    flash('Incorrect email/password')
            else:
                # Account exists but email is not verified
                flash('Please verify your email before logging in.')
        else:
            # Account doesn't exist
            flash('Incorrect email/password')

    return render_template('login.html')

    
# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if request.method == 'POST' and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        f_name = request.form['f_name']
        m_name = request.form['m_name']
        l_name = request.form['l_name']
        password = request.form['password']
        email = request.form['email']

        _hashed_password = generate_password_hash(password)
        verification_token = secrets.token_urlsafe(16)  # Generate a secure verification token

        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        account = cursor.fetchone()

        if account:
            flash('Account already exists!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!')
        elif not f_name or not m_name or not l_name or not password or not email:
            flash('Please fill out the form!')
        else:
            cursor.execute("""
                INSERT INTO users (f_name, m_name, l_name, password, email, verification_token)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (f_name, m_name, l_name, _hashed_password, email, verification_token))
            conn.commit()

            # Send email with verification link
            send_verification_email(email, verification_token)

            flash('Please check your email to verify your account!')
            show_resend_button = True  # Set to True to render the Resend Verification Email button
            return render_template('register.html', show_resend_button=show_resend_button, email=email)

    elif request.method == 'POST':
        flash('Please fill out the form!')

    show_resend_button = False  # Default to False, no Resend Verification Email button
    return render_template('register.html', show_resend_button=show_resend_button)

# Resend Verification Email
@app.route('/resend_verification', methods=['GET'])
def resend_verification():
    email = request.args.get('email', '')

    # Initialize the session variables if they don't exist
    if 'resend_attempts' not in session:
        session['resend_attempts'] = 0
    if 'last_resend_time' not in session:
        session['last_resend_time'] = time.time()

    # Define the cooldown period (e.g., 5 minutes)
    cooldown_period = 5 * 60  # 5 minutes in seconds

    # Check if the cooldown period has passed
    current_time = time.time()
    time_since_last_attempt = current_time - session['last_resend_time']
    
    if session['resend_attempts'] >= 3 and time_since_last_attempt < cooldown_period:
        flash("You've sent too many requests. Please try again later.")
    elif session['resend_attempts'] >= 3 and time_since_last_attempt >= cooldown_period:
        # Reset the attempts counter after the cooldown period has passed
        session['resend_attempts'] = 0

    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
    account = cursor.fetchone()

    if account and session['resend_attempts'] < 3:
        # Generate a new verification token
        verification_token = secrets.token_urlsafe(16)
        cursor.execute("UPDATE users SET verification_token = %s WHERE email = %s", (verification_token, email))
        conn.commit()

        # Send email with new verification link
        send_verification_email(email, verification_token)

        # Update the resend attempts and the last resend time
        session['resend_attempts'] += 1
        session['last_resend_time'] = time.time()

        flash('Verification email resent. Please check your email!')
    elif not account:
        flash('Email not found.')

    # Always show the button
    show_resend_button = True
    return render_template('register.html', show_resend_button=show_resend_button, email=email)
                                                                                                                                                                                
# Verify Email
@app.route('/verify_email/<token>', methods=['GET'])
def verify_email(token):
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cursor.execute("SELECT * FROM users WHERE verification_token = %s", (token,))
    account = cursor.fetchone()

    if account:
        cursor.execute("UPDATE users SET email_verified = TRUE WHERE verification_token = %s", (token,))
        conn.commit()
        flash('Email verified successfully! Please Login')
    else:
        flash('Invalid verification token!')

    return redirect(url_for('login'))

@app.route('/verify_user', methods=['GET', 'POST'])
def verify_user():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()

        # Initialize session variables if they don't exist
        if 'resend_attempts' not in session:
            session['resend_attempts'] = 0
        if 'last_resend_time' not in session:
            session['last_resend_time'] = time.time()

        # Define the cooldown period (e.g., 5 minutes)
        cooldown_period = 5 * 60  # 5 minutes in seconds

        # Check if the cooldown period has passed
        current_time = time.time()
        time_since_last_attempt = current_time - session['last_resend_time']

        if session['resend_attempts'] >= 3 and time_since_last_attempt < cooldown_period:
            flash("You've sent too many requests. Please try again later.")
        elif session['resend_attempts'] >= 3 and time_since_last_attempt >= cooldown_period:
            # Reset the attempts counter after the cooldown period has passed
            session['resend_attempts'] = 0

        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        account = cursor.fetchone()

        if account and session['resend_attempts'] < 3:
            # Generate a new verification token
            verification_token = secrets.token_urlsafe(16)
            cursor.execute("UPDATE users SET verification_token = %s WHERE email = %s",
                           (verification_token, email))
            conn.commit()

            # Send email with new verification link
            send_verification_email(email, verification_token)

            # Update the resend attempts and the last resend time
            session['resend_attempts'] += 1
            session['last_resend_time'] = current_time

            flash('Verification email resent. Please check your email!')
        elif not account:
            flash('Email not found.')

        # Redirect to the same page to show the flash message
        return redirect(url_for('verify_user', email=email))

    # If GET request, render the form
    return render_template('resend_verification.html')


# Forgot Password
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Check if email exists in the database
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        account = cursor.fetchone()

        if account:
            # Generate a unique token
            reset_password_token = secrets.token_urlsafe(16)

            # Update the reset token in the database
            cursor.execute("UPDATE users SET reset_password_token = %s WHERE email = %s", (reset_password_token, email))
            conn.commit()

            # Send email with password reset link
            send_password_reset_email(email, reset_password_token)

            flash('Password reset email sent! Check your inbox/spam.')
            return redirect(url_for('login'))
        else:
            flash('Email not found. Please try again.')

    return render_template('forgot_password.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Check if token exists and is valid
    cursor.execute('SELECT * FROM users WHERE reset_password_token = %s', (token,))
    account = cursor.fetchone()

    if not account:
        flash('Invalid or expired token. Please try again.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password == confirm_password:
            # Hash the new password
            hashed_password = generate_password_hash(new_password)

            # Update the user's password in the database
            cursor.execute("UPDATE users SET password = %s, reset_password_token = NULL WHERE email = %s", (hashed_password, account['email']))
            conn.commit()

            flash('Password reset successful. You can now log in with your new password.')
            return redirect(url_for('login'))
        else:
            flash('Passwords do not match. Please try again.')

    return render_template('reset_password.html', token=token)

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('u_id', None) 
    session.pop('f_name', None)
    session.pop('m_name', None)
    session.pop('l_name', None)
    session.pop('email', None)
    session.pop('role', None) 
    # Redirect to login page
    return redirect(url_for('login'))

'''------------------------------------------------------------------------------'''



'''admin routes & functions------------------------------------------------------'''

#admin/dashboard.html 
@app.route('/admin/dashboard', methods=['GET'])
def admin_dashboard():
    if 'role' in session and session['role'] == 'admin':
       
        # Function retrieving the data
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Select user data based on unverified Emails
        cursor.execute("SELECT * FROM users WHERE email_verified = false AND role = 'student' AND status = 'unverified'")
        unverified_emails = cursor.fetchall()

        # Count of students who submitted applications but are still pending (not confirmed)
        cursor.execute("""
            SELECT COUNT(*)
            FROM applications a
            JOIN users u ON a.student_id = u.u_id
            WHERE a.status = 'Pending'
        """)
        students_applying_count = cursor.fetchone()[0]

        # Query to get students who have applied (students in applications table)
        cursor.execute("""
            SELECT u.u_id, u.f_name, u.m_name, u.l_name, u.email, u.s_date, a.status AS application_status
            FROM users u
            JOIN applications a ON u.u_id = a.student_id
            WHERE u.role = 'student'
            ORDER BY 
                CASE a.status 
                    WHEN 'Pending' THEN 0
                    WHEN 'Confirmed' THEN 1
                    ELSE 2
                END,
                u.s_date DESC
        """)
        students_applying = cursor.fetchall()
        
        # Select user data based on session u_id
        cursor.execute("SELECT * FROM users WHERE status = 'unverified' AND role = 'student' AND email_verified = true")
        user_data = cursor.fetchall()
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE status = 'unverified' AND email_verified = true AND role = 'student'")
        user_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT ROUND((COUNT(*) FILTER (WHERE email_verified = false) * 100.0 / COUNT(*)), 2) AS unverified_percentage FROM users WHERE role = 'student'")
        email_unverified = cursor.fetchone()[0]
        
        cursor.execute("SELECT ROUND((COUNT(*) FILTER (WHERE email_verified = true AND status = 'unverified') * 100.0 / COUNT(*)), 2) AS unverified_student FROM users WHERE role = 'student'")
        student_unverified = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'student' AND email_verified = false")
        unverified_email_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'student' AND email_verified = true AND status = 'unverified'")
        unverified_student_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'student'")
        overall_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'student' AND email_verified = true")
        overall_count_unv = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'student' AND status = 'verified'")
        verified_user_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT ROUND((COUNT(*) FILTER (WHERE status = 'verified') * 100.0 / COUNT(*)), 2) AS verified_percentage FROM users WHERE role = 'student'")
        user_verified = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT
                CASE
                    WHEN COUNT(*) = 0 THEN NULL
                    ELSE (SELECT pref_course1
                        FROM student_profile
                        GROUP BY pref_course1
                        ORDER BY COUNT(*) DESC
                        LIMIT 1)
                END AS most_common_pref_course1
            FROM student_profile
        """)
        most_common_pref_course1 = cursor.fetchone()[0]

        cursor.execute(""" SELECT CASE WHEN COUNT(*) = 0 THEN NULL 
                    ELSE ROUND(
                            (COUNT(*) FILTER (WHERE pref_course1 = common_value) * 100.0 / COUNT(*)), 2)
                    END AS common_value_percentage
                    FROM student_profile, (SELECT MODE() WITHIN GROUP (ORDER BY pref_course1) AS common_value FROM student_profile) AS mode_subquery """)
        common_pref_course1_percentage_row = cursor.fetchone()
        common_pref_course1_percentage = common_pref_course1_percentage_row[0] if common_pref_course1_percentage_row else None

        cursor.execute("""
            SELECT
                CASE
                    WHEN COUNT(*) = 0 THEN NULL
                    ELSE (SELECT pref_course2
                        FROM student_profile
                        GROUP BY pref_course2
                        ORDER BY COUNT(*) DESC
                        LIMIT 1)
                END AS most_common_pref_course2
            FROM student_profile
        """)
        most_common_pref_course2 = cursor.fetchone()[0]

        
        cursor.execute(""" SELECT CASE WHEN COUNT(*) = 0 THEN NULL 
                    ELSE ROUND(
                        (COUNT(*) FILTER (WHERE pref_course2 = common_value) * 100.0 / COUNT(*)), 2 )
                    END AS common_value_percentage
                    FROM student_profile, (SELECT MODE() WITHIN GROUP (ORDER BY pref_course2) AS common_value FROM student_profile) AS mode_subquery """)
        common_pref_course2_percentage_row = cursor.fetchone()
        common_pref_course2_percentage = common_pref_course2_percentage_row[0] if common_pref_course2_percentage_row else None
        
        # Query to get user details with verified grades
        cursor.execute("""
            SELECT u.u_id, u.f_name, u.m_name, u.l_name, u.s_date, u.status, sp.s_id, sp.verified_grades
            FROM users u
            LEFT JOIN student_profile sp ON u.u_id = sp.s_id
            WHERE sp.verified_grades IS NOT NULL AND u.status = 'unverified'
        """)
        students_with_verified_grades = cursor.fetchall()

        cursor.execute("""
            SELECT COUNT(*)
            FROM student_profile
            INNER JOIN users ON student_profile.s_id = users.u_id
            WHERE student_profile.verified_grades IS NOT NULL
            AND users.status = 'unverified'
        """)
        students_with_verified_grades_count = cursor.fetchone()[0]

        # Query to find the top 5 most recommended programs in rc1
        cursor.execute("""
            SELECT rc1, COUNT(rc1) AS count
            FROM recommended_course
            GROUP BY rc1
            ORDER BY count DESC
            LIMIT 5
        """)
        top_recommended_programs = cursor.fetchall()

        # Calculate the percentage for each recommended program based on the total student count
        top_recommended_programs_list = [
            {
                'program': row[0],
                'percentage': round((row[1] / overall_count) * 100, 2)
            }
            for row in top_recommended_programs
        ]

        conn.commit()
        cursor.close()

        return render_template('admin/dashboard.html', f_name=session['f_name'], m_name=session['m_name'], l_name=session['l_name'], role=session['role'], email=session['email'], students_applying=students_applying, students_applying_count=students_applying_count, student=user_data, count=user_count, unverified_emails=unverified_emails, email_unverified=email_unverified, student_unverified=student_unverified, overall_count=overall_count, unverified_email_count=unverified_email_count, unverified_student_count=unverified_student_count, most_common_pref_course1=most_common_pref_course1, common_pref_course1_percentage=common_pref_course1_percentage, most_common_pref_course2=most_common_pref_course2, common_pref_course2_percentage=common_pref_course2_percentage, students_with_verified_grades=students_with_verified_grades, students_with_verified_grades_count=students_with_verified_grades_count, overall_count_unv=overall_count_unv, verified_user_count=verified_user_count, user_verified=user_verified, top_recommended_programs=top_recommended_programs_list)
    else:
        flash('Unauthorized access, re-login')
        return redirect(url_for('login'))
    
    
# Route for verifying an email
@app.route('/verify_user_email/<int:user_id>', methods=['POST'])
def verify_user_email(user_id):
    if 'role' in session and session['role'] == 'admin':
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Update email_verified to true for the specified student_id
        cursor.execute("UPDATE users SET email_verified = true WHERE u_id = %s", (user_id,))
        
        conn.commit()
        cursor.close()
        
        return redirect(url_for('admin_dashboard'))

    else:
        flash('Unauthorized access, re-login')
        return redirect(url_for('login'))
       
# Route for verifying a student 
# recommend courses to the student
@app.route('/verify/<int:student_id>', methods=['POST'])
def verify_student(student_id):
    if 'role' in session and session['role'] == 'admin':
        try:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            
            # Update status to 'verified' for the specified student_id
            cursor.execute("UPDATE users SET status = 'verified' WHERE u_id = %s", (student_id,))
            
            # Update application status to 'Confirmed'
            cursor.execute("UPDATE applications SET status = 'Confirmed' WHERE student_id = %s", (student_id,))
            
            conn.commit()
            
            # Generate recommendations
            fetch_query = '''
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
                WHERE sp.s_id = %s;
            '''
            
            student_records = get_data_from_postgresql(fetch_query, params=(student_id,))
            
            if student_records:
                student = student_records[0]
                preferred_courses = [student.pop('pref_course1'), student.pop('pref_course2')]
                
                # Generate recommendations
                recommendations = main(student, prefered_course=preferred_courses)
                
                # Update recommendations in the `recommended_course` table
                update_recommendations_in_postgresql(conn, recommendations, student_id)
            
            return redirect(url_for('admin_dashboard'))
        
        except Exception as e:
            conn.rollback()
            flash(f"An error occurred: {str(e)}")
            return redirect(url_for('admin_dashboard'))
        
        finally:
            cursor.close()
    else:
        flash('Unauthorized access, re-login')
        return redirect(url_for('login'))

# Route for viewing user details (unverified)
@app.route('/view_unverified/<int:user_id>')
def view_unverified(user_id):
    
    if 'role' in session and session['role'] == 'admin':
        # Connect to the database
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Retrieve user details from the database based on user_id
        cursor.execute("SELECT * FROM users WHERE u_id = %s", (user_id,))
        user = cursor.fetchone()
        
        cursor.execute('SELECT * FROM student_profile WHERE s_id = %s', (user_id,))
        student_profile = cursor.fetchone()
        
        cursor.execute('SELECT * FROM student_grade_hs WHERE g_hs_id = %s', (user_id,))
        student_grade_HS = cursor.fetchone()
        
        cursor.execute('SELECT * FROM student_grade_shs WHERE g_shs_id = %s', (user_id,))
        student_grade_SHS = cursor.fetchone()

        cursor.execute('SELECT * FROM recommended_course WHERE rc_id = %s', (user_id,))
        student_rc = cursor.fetchone()
        
        # Close the cursor
        cursor.close()

        # Render the view_user.html template with the user details
        return render_template('admin/view_unverified.html', f_name=session['f_name'], m_name=session['m_name'], l_name=session['l_name'], role=session['role'], email=session['email'], user=user, profile=student_profile, grade=student_grade_SHS, grade_hs=student_grade_HS, student_rc=student_rc, get_course_definition=get_course_definition)

    else:
        flash('Unauthorized access, re-login')
        return redirect(url_for('login'))

#SASE update
@app.route('/update_sase/<int:user_id>', methods=['POST'])
def update_sase_scores(user_id):
    
    if request.method == 'POST':
        ap = request.form['aptitude']
        lu = request.form['language']
        ma = request.form['mathematics']
        sc = request.form['science']
        
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Update the student profile in the database
        cursor.execute("""
            UPDATE student_profile
            SET ap = %s, lu = %s, ma = %s, sc = %s
            WHERE s_id = %s
        """, (ap, lu, ma, sc, user_id))
        
        conn.commit()
        cursor.close()

        # Redirect to a page showing updated scores or any desired page
        return redirect(url_for('view_unverified', user_id=user_id))

    
#admin/students.html 
@app.route('/admin/students', methods=['GET'])
def admin_students():
    if 'role' in session and session['role'] == 'admin':
       
       #Function retrieving the data
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Select user data 
        cursor.execute("SELECT * FROM users where status = 'verified' and role = 'student'")
        user_data = cursor.fetchall()
        
        # Select user data 
        cursor.execute("SELECT * FROM users where status = 'unverified' and  role = 'student' and email_verified = true")
        unverified_view = cursor.fetchall()
        
        cursor.execute("SELECT count(*) FROM users where status = 'unverified' and email_verified = true and role = 'student'")
        user_count = cursor.fetchone()[0]
        
                # Query to get user details with verified grades
        cursor.execute("""
            SELECT u.u_id, u.f_name, u.m_name, u.l_name, u.s_date, u.status, sp.s_id, sp.verified_grades
            FROM users u
            LEFT JOIN student_profile sp ON u.u_id = sp.s_id
            WHERE sp.verified_grades IS NOT NULL and u.status = 'unverified'
        """)
        students_with_verified_grades = cursor.fetchall()

        cursor.execute("""
            SELECT COUNT(*)
            FROM student_profile
            INNER JOIN users ON student_profile.s_id = users.u_id
            WHERE student_profile.verified_grades IS NOT NULL
            AND users.status = 'unverified'
        """)

        students_with_verified_grades_count = cursor.fetchone()[0]
        
        conn.commit()
        cursor.close()

        return render_template('admin/students.html', f_name=session['f_name'], m_name=session['m_name'], l_name=session['l_name'], role=session['role'], email=session['email'], student=user_data, count=user_count, unve_view = unverified_view, students_with_verified_grades=students_with_verified_grades, students_with_verified_grades_count=students_with_verified_grades_count )
    else:
        flash('Unauthorized access, re-login')
        return redirect(url_for('login'))
    

# Route for viewing user details (verified)
@app.route('/view_verified/<int:user_id>')
def view_verified(user_id):
    if 'role' in session and session['role'] == 'admin':
        # Connect to the database
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Retrieve user details from the database based on user_id
        cursor.execute("SELECT * FROM users WHERE u_id = %s", (user_id,))
        user = cursor.fetchone()
        
        cursor.execute('SELECT * FROM student_profile WHERE s_id = %s', (user_id,))
        student_profile = cursor.fetchone()
        
        cursor.execute('SELECT * FROM student_grade_hs WHERE g_hs_id = %s', (user_id,))
        student_grade_HS = cursor.fetchone()
        
        cursor.execute('SELECT * FROM student_grade_shs WHERE g_shs_id = %s', (user_id,))
        student_grade = cursor.fetchone()
        
        cursor.execute('SELECT * FROM recommended_course WHERE rc_id = %s', (user_id,))
        student_rc = cursor.fetchone()
        
        # Close the cursor
        cursor.close()

        # Render the view_verified.html template with the user details
        return render_template('admin/view_verified.html', f_name=session['f_name'], m_name=session['m_name'], l_name=session['l_name'], role=session['role'], email=session['email'], user=user, profile=student_profile, grade=student_grade, grade_hs=student_grade_HS, student_rc=student_rc, get_course_definition=get_course_definition)

    else:
        flash('Unauthorized access, re-login')
        return redirect(url_for('login'))


'''-------------------------------------------------------------------------------'''

'''Student routes & functions------------------------------------------------------'''

@app.route('/student/profile')
def student_profile():
    if 'loggedin' in session and 'u_id' in session:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Select user data based on session u_id
        cursor.execute('SELECT * FROM users WHERE u_id = %s', (session['u_id'],))
        user_data = cursor.fetchone()

        # Select student profile data
        cursor.execute('SELECT * FROM student_profile WHERE s_id = %s', (session['u_id'],))
        student_profile = cursor.fetchone()
        saved_data = student_profile  # Reuse student profile data

        # Fetch high school grades
        cursor.execute("SELECT * FROM student_grade_hs WHERE g_hs_id = %s", (session['u_id'],))
        student_grades_hs = cursor.fetchone()

        # Fetch senior high school grades
        cursor.execute("SELECT * FROM student_grade_shs WHERE g_shs_id = %s", (session['u_id'],))
        student_grades_shs = cursor.fetchone()

        # Check if all high school grades are filled
        all_grades_hs_filled = student_grades_hs and all(
            student_grades_hs[field] is not None and student_grades_hs[field].strip() != ''
            for field in student_grades_hs.keys() if field != 'g_hs_id'
        )

        # Check if all senior high school grades are filled, disregarding NULL values
        all_grades_shs_filled = all(
            student_grades_shs[field] is None or student_grades_shs[field].strip() != ''
            for field in student_grades_shs.keys() if field != 'g_shs_id'
        )

        # Check if the student is unverified
        show_modal = user_data['status'] == 'unverified'
        
        # Check if the application exists
        cursor.execute("SELECT * FROM applications WHERE student_id = %s", (session['u_id'],))
        application_exists = cursor.fetchone() is not None
        
        return render_template(
            'student/profile.html',
            user=user_data,
            student=student_profile,
            show_modal=show_modal,
            saved_data=saved_data,
            all_grades_hs_filled=all_grades_hs_filled,
            all_grades_shs_filled=all_grades_shs_filled,
            application_exists=application_exists  # Pass this variable to the template
        )
    else:
        flash('Unauthorized access, please log in')
        return redirect(url_for('login'))
    
# application route
@app.route('/submit-application', methods=['POST'])
def submit_application():
    if 'loggedin' in session and 'u_id' in session:
        u_id = session['u_id']
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Check if an application already exists
        cursor.execute("SELECT * FROM applications WHERE student_id = %s", (u_id,))
        existing_application = cursor.fetchone()

        if existing_application:
            return jsonify(success=False, message='Application already submitted!'), 400

        # Fetch the data from the form
        hs_grades = request.form.get('hs_grades_filled')
        shs_grades = request.form.get('shs_grades_filled')
        edi_status = request.form.get('edi_filled')
        parent_info = request.form.get('parent_info_filled')
        verified_grades = request.form.get('verified_grades')

        # Debugging: Log the received data
        print(f"Received data: HS Grades Filled: {hs_grades}, SHS Grades Filled: {shs_grades}, EDI Filled: {edi_status}, Parent Info Filled: {parent_info}, Verified Grades: {verified_grades}")

        # Validate that all required fields are filled
        if not hs_grades or not shs_grades or not edi_status or not parent_info or not verified_grades:
            flash('Please fill out all required fields')
            return redirect(url_for('student_profile'))

        # Save the application data to the database
        try:
            cursor.execute(
                'INSERT INTO applications (student_id, hs_grades_filled, shs_grades_filled, edi_filled, parent_info_filled, verified_grades) VALUES (%s, %s, %s, %s, %s, %s)', 
                (u_id, hs_grades, shs_grades, edi_status, parent_info, verified_grades)
            )
            conn.commit()
            return jsonify(success=True, message='Application submitted successfully!')

        except Exception as e:
            conn.rollback()
            return jsonify(success=False, message=f'An error occurred: {str(e)}'), 500

        finally:
            cursor.close()  # Ensure cursor is closed

    else:
        flash('Unauthorized access, please log in')
        return redirect(url_for('login'))
    
def allowed_file(filename):
    # Define your allowed file types here
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['jpg', 'jpeg', 'png', 'pdf']

def handle_file_upload(file_key, existing_file_path):
    file = request.files.get(file_key)
    if file and file.filename and allowed_file(file.filename):
        random_string = str(uuid.uuid4().hex)[:10]
        filename = secure_filename(random_string + file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Remove existing file if it exists
        if existing_file_path:
            os.remove(os.path.join('static', existing_file_path))
        
        file.save(file_path)
        return os.path.join('student_uploads/', filename)
    elif existing_file_path:
        return existing_file_path
    return '' 

# Update profile
@app.route('/student/update', methods=['POST'])
def update_student_profile():
    if 'u_id' not in session:
        return redirect(url_for('login'))

    try:
        # Retrieve form data
        contact = request.form.get('contact', '')
        working_student = request.form.get('working_student', '')
        lgbtq_parent = request.form.get('lgbtq_parent', '')
        victim = request.form.get('victim', '')
        religion = request.form.get('religion', '')
        pwd = request.form.get('pwd', '')
        childsoloparent = request.form.get('childsoloparent', '')
        firstgenlearner = request.form.get('firstgenlearner', '')
        province_home = request.form.get('province_home', '')
        city_home = request.form.get('city_home', '')
        father_edu_attain = request.form.get('father_edu_attain', '')
        mother_edu_attain = request.form.get('mother_edu_attain', '')
        father_occupation = request.form.get('father_occupation', '')
        mother_occupation = request.form.get('mother_occupation', '')
        father_income = request.form.get('father', '')
        custom_father_income = request.form.get('custom_father_income', '')
        mother_income = request.form.get('mother', '')
        custom_mother_income = request.form.get('custom_mother_income', '')
        soloparent = request.form.get('soloparent', '')

        # Determine final father and mother income values
        father = custom_father_income if father_income == 'custom' and custom_father_income else father_income
        mother = custom_mother_income if mother_income == 'custom' and custom_mother_income else mother_income

        # Get u_id from session
        u_id = session['u_id']

        # Get existing data from the database
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM student_profile WHERE s_id = %s", (u_id,))
        saved_data = cursor.fetchone()

        # Define existing file paths
        existing_files = {
            'pwd_id_file': saved_data.get('pwd_id_file') if saved_data else None,
            'ip_id': saved_data.get('ip_id') if saved_data else None,
            'childsoloparent_file': saved_data.get('childsoloparent_file') if saved_data else None,
            '1stgenlearner_id': saved_data.get('1stgenlearner_id') if saved_data else None,
            'child_deprived_liberty_id': saved_data.get('child_deprived_liberty_id') if saved_data else None,
            'soloparent_id': saved_data.get('soloparent_id') if saved_data else None,
            'working_id': saved_data.get('working_id') if saved_data else None,
            'lgbtq_p_id': saved_data.get('lgbtq_p_id') if saved_data else None,
            'victim_id': saved_data.get('victim_id') if saved_data else None,
            'father_itr_file': saved_data.get('father_itr_file') if saved_data else None,
            'mother_itr_file': saved_data.get('mother_itr_file') if saved_data else None,
        }

        # Handle file uploads
        pwd_id_file = handle_file_upload('id_picture', existing_files['pwd_id_file']) if pwd == 'Yes' else ''
        ip_file = handle_file_upload('ip_id', existing_files['ip_id']) if request.form.get('ip_option', '') == 'Yes' else ''
        childsoloparent_file = handle_file_upload('childsoloparent_id', existing_files['childsoloparent_file']) if childsoloparent == 'Yes' else ''
        firstgenlearner_file = handle_file_upload('firstgenlearner_id', existing_files['1stgenlearner_id']) if firstgenlearner == 'Yes' else ''
        child_deprived_liberty_file = handle_file_upload('child_deprived_liberty_id', existing_files['child_deprived_liberty_id']) if request.form.get('child_deprived_liberty', '') == 'Yes' else ''
        single_file = handle_file_upload('single_id', existing_files['soloparent_id']) if soloparent == 'Yes' else ''
        working_student_file = handle_file_upload('working_id', existing_files['working_id']) if working_student == 'Yes' else ''
        lgbtq_p = handle_file_upload('lgbtq_p_id', existing_files['lgbtq_p_id']) if lgbtq_parent == 'Yes' else ''
        victim_id = handle_file_upload('victim_id', existing_files['victim_id']) if victim == 'Yes' else ''
        
        # Handle file uploads for ITRs based on income ranges
        father_itr_file = handle_file_upload('father_itr', existing_files['father_itr_file']) if father_income in ['₱250,000 - ₱499,999', '₱500,000 and over'] else None
        mother_itr_file = handle_file_upload('mother_itr', existing_files['mother_itr_file']) if mother_income in ['₱250,000 - ₱499,999', '₱500,000 and over'] else None

        # Update data in student_profile table
        cursor.execute(""" 
        UPDATE student_profile
        SET contact = %s, religion = %s, pwd = %s, childsoloparent = %s, ip = %s, ip_id = %s,
            "1stgenlearner" = %s, province_home = %s, city_home = %s, father_occupation = %s, 
            mother_occupation = %s, father = %s, mother = %s, father_tribe = %s, mother_tribe = %s, 
            permit_number = %s, pwd_id_file = %s, childsoloparent_file = %s, "1stgenlearner_id" = %s, 
            child_deprived_liberty = %s, child_deprived_liberty_id = %s, soloparent = %s, soloparent_id = %s, 
            father_edu_attain = %s, mother_edu_attain = %s, working_student = %s, working_id = %s, lgbtq_parent = %s, 
            lgbtq_p_id = %s, victim = %s, victim_id = %s, father_itr_file = %s, mother_itr_file = %s
        WHERE s_id = %s
        """, (contact, religion, pwd, childsoloparent, request.form.get('ip_option', ''), ip_file or None, 
            firstgenlearner, province_home, city_home, father_occupation, mother_occupation, father, mother, 
            request.form.get('father_tribe', ''), request.form.get('mother_tribe', ''), 
            request.form.get('permit_number', ''), pwd_id_file or None, childsoloparent_file or None, 
            firstgenlearner_file or None, request.form.get('child_deprived_liberty', ''), 
            child_deprived_liberty_file or None, soloparent, single_file or None, father_edu_attain, mother_edu_attain, 
            working_student, working_student_file or None, lgbtq_parent, lgbtq_p or None, victim, victim_id or None, father_itr_file or None, mother_itr_file or None, u_id))

        conn.commit()

    except Exception as e:
        # Log error and handle failure
        conn.rollback()
        # Example logging
        print(f"Error updating student profile: {e}")
        # Optionally, show an error message to the user
        return "An error occurred while updating your profile. Please try again."

    return redirect(url_for('student_profile'))

    
#submit grade form
@app.route('/submit_grade_form/<int:user_id>', methods=['POST'])
def submit_grade_form(user_id):
    if request.method == 'POST':
        if 'new_picture' in request.files:
            new_picture = request.files['new_picture']
            if new_picture.filename != '':
                if allowed_file(new_picture.filename):
                    filename = str(uuid.uuid4().hex[:10]) + '_' + secure_filename(new_picture.filename)
                    new_picture.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                    # Update the database with the new picture filename
                    file_path = 'student_uploads/' + filename  # Construct the file path
                    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                    cursor.execute("""
                        UPDATE student_profile
                        SET verified_grades = %s
                        WHERE s_id = %s
                    """, (file_path, user_id))
                    conn.commit()
                    cursor.close()

                    # Return a success response
                    return '', 200
                else:
                    # Invalid file type
                    return 'Invalid file type. Allowed types are png, jpg, jpeg', 400
            else:
                # No file selected
                return 'No file selected', 400
        else:
            # File not found in request
            return 'File not found in request', 400

    # Handle other cases if needed
    return '', 405

#dashboard
@app.route('/student/dashboard')
def student_dashboard():
    if 'loggedin' in session and 'u_id' in session:

        # Check if student_profile exists for the logged-in student
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM student_profile WHERE s_id = %s", (session['u_id'],))
        student_profile = cursor.fetchone()

        if student_profile:
            # If student_profile exists
            cursor.execute("SELECT * FROM student_grade_hs WHERE g_hs_id = %s", (session['u_id'],))
            student_grade_hs = cursor.fetchone()

            if student_grade_hs:
                # If student_grade_hs exists
                cursor.execute("SELECT * FROM student_grade_shs WHERE g_shs_id = %s", (session['u_id'],))
                student_grade = cursor.fetchone()

                if student_grade:
                    # If student_grade exists, go to dashboard
                    return render_template('student/dashboard.html', f_name=session['f_name'], m_name=session['m_name'], l_name=session['l_name'], role=session['role'], email=session['email'])
                else:
                    # If student_grade doesn't exist, go to input_grade
                    return redirect(url_for('input_grade'))
            else:
                # If student_grade_hs doesn't exist, redirect to input_hs
                return redirect(url_for('input_hs'))
        else:
            # If student_profile doesn't exist, go to student_input
            return redirect(url_for('student_input'))
    else:
        flash('Unauthorized access, please log in')
        return redirect(url_for('login'))
    
#input.html
@app.route('/student/input', methods=['GET', 'POST'])
def student_input():
    if request.method == 'POST':
        # Gather form data
        contact = request.form['contact']
        sex = request.form['sex']
        working_student = request.form['working_student']
        lgbtq_parent = request.form['lgbtq_parent']
        victim = request.form['victim']
        religion = request.form['religion']
        pwd = request.form['pwd']
        childsoloparent = request.form['childsoloparent']
        firstgenlearner = request.form['firstgenlearner']
        province_home = request.form['province_home']
        city_home = request.form['city_home']
        track = request.form['track']
        name_hs = request.form['name_hs']
        address_hs = request.form['address_hs']
        father_edu_attain = request.form['father_edu_attain']
        mother_edu_attain = request.form['mother_edu_attain']
        father_occupation = request.form['father_occupation']
        mother_occupation = request.form['mother_occupation']
        father = request.form['father']
        mother = request.form['mother']
        father_tribe = request.form['father_tribe']
        mother_tribe = request.form['mother_tribe']
        pref_course1 = request.form['pref_course1']
        pref_course2 = request.form['pref_course2']
        child_deprived_liberty = request.form['child_deprived_liberty']
        soloparent = request.form['soloparent']

        # Initialize file variables
        father_itr_file = ''
        mother_itr_file = ''

        # Handle ITR uploads based on the father's and mother's income
        father_needs_itr = father in ['₱250,000 - ₱499,999', '₱500,000 and over']
        mother_needs_itr = mother in ['₱250,000 - ₱499,999', '₱500,000 and over']

        # Handling 'ip' field
        ip = ''
        if 'ip_option' in request.form:
            if request.form['ip_option'] == 'Yes':
                ip = request.form['ip_group'] if request.form['ip_group'] != 'others' else request.form['ip_others']
            elif request.form['ip_option'] == 'No':
                ip = 'No'

        # Function to handle file uploads
        def handle_file_upload(field_name):
            if field_name in request.files:
                uploaded_file = request.files[field_name]
                if uploaded_file.filename != '' and allowed_file(uploaded_file.filename):
                    random_string = str(uuid.uuid4().hex)[:10]
                    filename = secure_filename(random_string + uploaded_file.filename)
                    uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    return os.path.join('student_uploads/', filename)
            return None

        # Check for different conditions and handle file uploads accordingly
        pwd_id_file = handle_file_upload('id_picture') if pwd == 'Yes' else None
        lgbtq_p_id = handle_file_upload('lgbtq_p_id') if lgbtq_parent == 'Yes' else None
        working_id = handle_file_upload('working_id') if working_student == 'Yes' else None
        victim_id = handle_file_upload('victim_id') if victim == 'Yes' else None
        childsoloparent_file = handle_file_upload('soloparent_id') if childsoloparent == 'Yes' else None
        firstgenlearner_file = handle_file_upload('firstgenlearner_id') if firstgenlearner == 'Yes' else None
        ip_file = handle_file_upload('ip_id') if request.form.get('ip_option') == 'Yes' else None
        child_deprived_liberty_file = handle_file_upload('child_deprived_liberty_id') if child_deprived_liberty == 'Yes' else None
        single_file = handle_file_upload('single_id') if soloparent == 'Yes' else None
        father_itr_file = handle_file_upload('father_itr') if father_needs_itr else None
        mother_itr_file = handle_file_upload('mother_itr') if mother_needs_itr else None

        # Get user ID from session
        u_id = session.get('u_id')

        # Insert data into the student_profile table
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(""" 
            INSERT INTO student_profile (s_id, contact, sex, religion, pwd, childsoloparent, ip, "1stgenlearner", province_home, city_home, track, name_hs, address_hs, father_occupation, mother_occupation, father, mother, father_tribe, mother_tribe, pref_course1, pref_course2, pwd_id_file, childsoloparent_file, "1stgenlearner_id", ip_id, child_deprived_liberty, child_deprived_liberty_id, soloparent, soloparent_id, father_edu_attain, mother_edu_attain, lgbtq_parent, lgbtq_p_id, working_student, working_id, victim, victim_id, father_itr_file, mother_itr_file, ap, lu, ma, sc)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            u_id, contact, sex, religion, pwd, childsoloparent, ip, firstgenlearner,
            province_home, city_home, track, name_hs, address_hs, father_occupation,
            mother_occupation, father, mother, father_tribe, mother_tribe,
            pref_course1, pref_course2,
            pwd_id_file, childsoloparent_file, firstgenlearner_file, ip_file,
            child_deprived_liberty, child_deprived_liberty_file, soloparent, single_file,
            father_edu_attain, mother_edu_attain, lgbtq_parent, lgbtq_p_id,
            working_student, working_id, victim, victim_id,
            father_itr_file, mother_itr_file, 17.0, 36.0, 16.0, 8.0
        ))

        conn.commit()

        # Redirect to input_grade after successful submission
        return redirect(url_for('input_hs'))

    # If it's a GET request or form submission failed
    if 'email' in session:
        return render_template('student/input.html', 
            f_name=session['f_name'], 
            m_name=session['m_name'], 
            l_name=session['l_name'], 
            role=session['role'], 
            email=session['email']
        )
    else:
        flash('Please log in to access this page.')
        return redirect(url_for('login'))

#input_hs.html 
@app.route('/student/input_hs', methods=['GET', 'POST'])
def input_hs():
    
    if request.method == 'POST':
        filipino9 = request.form['filipino9']
        english9 = request.form['english9']
        mathematics9 = request.form['mathematics9']
        science9 = request.form['science9']
        aralingpanlipunan9 = request.form['aralingpanlipunan9']
        edukasyonsapagpapakatao9 = request.form['edukasyonsapagpapakatao9']
        music9 = request.form['music9']
        arts9 = request.form['arts9']
        physicaleducation9 = request.form['physicaleducation9']
        health9 = request.form['health9']
        edukasyongpantahananatpangkabuhayan9 = request.form['edukasyongpantahananatpangkabuhayan9']
        technologyandlivelihoodeducation9 = request.form['technologyandlivelihoodeducation9']
        filipino10 = request.form['filipino10']
        english10 = request.form['english10']
        mathematics10 = request.form['mathematics10']
        science10 = request.form['science10']
        aralingpanlipunan10 = request.form['aralingpanlipunan10']
        edukasyonsapagpapakatao10 = request.form['edukasyonsapagpapakatao10']
        music10 = request.form['music10']
        arts10 = request.form['arts10']
        physicaleducation10 = request.form['physicaleducation10']
        health10 = request.form['health10']
        edukasyongpantahananatpangkabuhayan10 = request.form['edukasyongpantahananatpangkabuhayan10']
        technologyandlivelihoodeducation10 = request.form['technologyandlivelihoodeducation10']
        
        # Get u_id from session
        u_id = session.get('u_id')

        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Insert data into student_profile table
        cursor.execute("""
            INSERT INTO student_grade_hs(g_hs_id, filipino9, english9, mathematics9, science9, aralingpanlipunan9, edukasyonsapagpapakatao9, music9, arts9, physicaleducation9, health9, edukasyongpantahananatpangkabuhayan9, technologyandlivelihoodeducation9, filipino10, english10, mathematics10, science10, aralingpanlipunan10, edukasyonsapagpapakatao10, music10, arts10, physicaleducation10, health10, edukasyongpantahananatpangkabuhayan10, technologyandlivelihoodeducation10)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (u_id, filipino9, english9, mathematics9, science9, aralingpanlipunan9, edukasyonsapagpapakatao9, music9, arts9, physicaleducation9, health9, edukasyongpantahananatpangkabuhayan9, technologyandlivelihoodeducation9, filipino10, english10, mathematics10, science10, aralingpanlipunan10, edukasyonsapagpapakatao10, music10, arts10, physicaleducation10, health10, edukasyongpantahananatpangkabuhayan10, technologyandlivelihoodeducation10))
            
        conn.commit()
        

        # Redirect to input_grade after successful submission
        return redirect(url_for('input_grade'))

    # If it's a GET request or form submission failed
    if 'email' in session:
        return render_template('student/input_hs.html', f_name=session['f_name'], m_name=session['m_name'], l_name=session['l_name'], role=session['role'], email=session['email'])
    else:
        flash('Please log in to access this page.')
        return redirect(url_for('login'))
    

# input_grade.html
@app.route('/student/input_grade', methods=['GET', 'POST'])
def input_grade():
    u_id = session.get('u_id')
    
    if not u_id:
        flash('Please log in to access this page.')
        return redirect(url_for('login'))

    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT track FROM student_profile WHERE s_id = %s", (u_id,))
    track = cursor.fetchone()

    if request.method == 'POST':
        if not track:
            flash("Student profile not found.")
            return redirect(url_for('student_dashboard'))

        track_value = track['track']
        valid_tracks = ['STEM', 'ABM', 'HUMSS', 'GAS', 'TVL']
        if track_value not in valid_tracks:
            flash("Invalid track value.")
            return redirect(url_for('student_dashboard'))
        
        track_fields = {
            'STEM': [
                'earthandlifescience', 'physicalscience', 'earthscience', 'genbio1', 'genbio2', 
                'genphysics1', 'genphysics2', 'genchem1', 'genchem2', 'generalmath', 
                'statisticsandprobability', 'precalculus', 'basiccalculus', 'oralcommunication', 
                'reading_and_writing', 'mediaandinformationliteracy', 
                't21stcenturyliteraturefromthephilippinesandtheworld', 
                'contemporaryphilippineartsfromtheregions', 'pagbasaatpagsusuringibatibangtekstotungosapananaliksik', 
                'komunikasyonatpananaliksiksawikaatkulturangpilipino', 'personaldevelopment', 
                'introductiontothephilosophyofthehumanperson', 'understandingculturesocietyandpolitics', 
                'disasterreadinessandrisk_reduction', 'physicaleducationandhealth', 'physicaleducationandhealth2', 
                'physicaleducationandhealth3', 'physicaleducationandhealth4'
            ],
            'ABM': [
                'earthandlifescience', 'physicalscience', 'earthscience', 'generalmath', 
                'statisticsandprobability', 'businessmath', 'businessfinance', 'oralcommunication', 
                'reading_and_writing', 'mediaandinformationliteracy', 
                't21stcenturyliteraturefromthephilippinesandtheworld', 
                'contemporaryphilippineartsfromtheregions', 'pagbasaatpagsusuringibatibangtekstotungosapananaliksik', 
                'komunikasyonatpananaliksiksawikaatkulturangpilipino', 'personaldevelopment', 
                'introductiontothephilosophyofthehumanperson', 'understandingculturesocietyandpolitics', 
                'disasterreadinessandrisk_reduction', 'physicaleducationandhealth', 'physicaleducationandhealth2', 
                'physicaleducationandhealth3', 'physicaleducationandhealth4', 'organizationandmanagement', 
                'principlesofmarketing', 'businessmarketing', 'businessenterpriseandsimulation', 
                'f1_fundamentalsofaccountancybusinessandmanagement1', 
                'f2_fundamentalsofaccountancybusinessandmanagement2', 'appliedeconomicsbusiness', 
                'ethicsandsocial_responsibility'
            ],
            'HUMSS': [
                'earthandlifescience', 'physicalscience', 'earthscience', 
                'generalmath', 'statisticsandprobability', 'oralcommunication', 
                'reading_and_writing', 'mediaandinformationliteracy', 
                't21stcenturyliteraturefromthephilippinesandtheworld', 
                'contemporaryphilippineartsfromtheregions', 'creativenonfiction', 
                'pagbasaatpagsusuringibatibangtekstotungosapananaliksik', 
                'komunikasyonatpananaliksiksawikaatkulturangpilipino', 
                'creativewriting_malikhaing_pagsulat', 'personaldevelopment', 
                'introductiontothephilosophyofthehumanperson', 
                'understandingculturesocietyandpolitics', 
                'disasterreadinessandrisk_reduction', 'physicaleducationandhealth', 
                'physicaleducationandhealth2', 'physicaleducationandhealth3', 
                'physicaleducationandhealth4', 'introductiontoworldreligionsandbeliefsystems', 
                'community_engagementsolidarityandcitizenship', 
                'philippinepoliticsandgovernance', 'disciplinesandideasinthesocialsciences'
            ],
            'GAS': [
                'earthandlifescience', 'physicalscience', 'earthscience', 
                'generalmath', 'statisticsandprobability', 'oralcommunication', 
                'reading_and_writing', 'mediaandinformationliteracy', 
                't21stcenturyliteraturefromthephilippinesandtheworld', 
                'contemporaryphilippineartsfromtheregions', 'creativewriting', 
                'pagbasaatpagsusuringibatibangtekstotungosapananaliksik', 
                'komunikasyonatpananaliksiksawikaatkulturangpilipino', 
                'personaldevelopment', 'introductiontothephilosophyofthehumanperson', 
                'understandingculturesocietyandpolitics', 
                'disasterreadinessandrisk_reduction', 'physicaleducationandhealth', 
                'physicaleducationandhealth2', 'physicaleducationandhealth3', 
                'physicaleducationandhealth4', 'humanities1_politics', 
                'humanities2_intro', 'socialscience1', 'organizationandmanagement2', 
                'appliedeconomics2', 'introtoworldreligionsandsytembeliefs', 
                'philippinepiliticsandgovernance'
            ],
            'TVL': [
                'earthandlifescience', 'physicalscience', 'earthscience', 
                'generalmath', 'statisticsandprobability', 'oralcommunication', 
                'reading_and_writing', 'mediaandinformationliteracy', 
                't21stcenturyliteraturefromthephilippinesandtheworld', 
                'contemporaryphilippineartsfromtheregions', 'creativewriting', 
                'pagbasaatpagsusuringibatibangtekstotungosapananaliksik', 
                'komunikasyonatpananaliksiksawikaatkulturangpilipino', 
                'personaldevelopment', 'introductiontothephilosophyofthehumanperson', 
                'understandingculturesocietyandpolitics', 
                'disasterreadinessandrisk_reduction', 'physicaleducationandhealth', 
                'physicaleducationandhealth2', 'physicaleducationandhealth3', 
                'physicaleducationandhealth4', 'safetyandfirstaid', 
                'humanmovement', 'fundamentalsofcoaching'
            ]
        }

        try:
            # Ensure all required fields for the specific track are provided
            required_fields = track_fields.get(track_value, [])
            values = [u_id] + [
            request.form.get(field) if request.form.get(field) else None 
            for field in required_fields
            ]

            # Insert grades into the `student_grade_shs` table
            placeholders = ', '.join(['%s'] * (len(required_fields) + 1))
            cursor.execute(f"""
                INSERT INTO student_grade_shs (g_shs_id, {', '.join(required_fields)})
                VALUES ({placeholders})
            """, values)

            conn.commit()
            
            # After successfully inserting grades, generate course recommendations
            fetch_query = '''
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
            WHERE sp.s_id = %s;
            '''
            student_records = get_data_from_postgresql(fetch_query, params=(u_id,))
            
            # Assuming there's only one record for the given `u_id`
            if student_records:
                student = student_records[0]  # Get the first record
                preferred_courses = [student.pop('pref_course1'), student.pop('pref_course2')]  # Extract preferred courses
                  
                # Generate recommendations
                recommendations = main(student, prefered_course=preferred_courses)
                
                # Insert recommendations into the database
                insert_recommendations_into_postgresql(conn, recommendations, u_id)

                return redirect(url_for('student_dashboard'))
            else:
                flash("No student data found.")
                return redirect(url_for('input_grade'))
            
        except Exception as e:
            conn.rollback()
            flash(f"An error occurred: {str(e)}")
            return redirect(url_for('input_grade'))
        
        finally:
            cursor.close()

    if 'email' in session:
       return render_template('student/input_grade.html', f_name=session['f_name'], m_name=session['m_name'], l_name=session['l_name'], role=session['role'], email=session['email'], track=track)

    flash('Please log in to access this page.')
    return redirect(url_for('login'))
    
#recommendation.html 
@app.route('/student/recommendation')
def student_recommendation():
    
    if 'loggedin' in session and 'u_id' in session:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Select user data based on session u_id
        cursor.execute('SELECT * FROM users WHERE u_id = %s', (session['u_id'],))
        user_data = cursor.fetchone()
        
        cursor.execute('SELECT * FROM student_profile WHERE s_id = %s', (session['u_id'],))
        student_profile = cursor.fetchone()
        
        cursor.execute('SELECT * FROM student_grade_hs WHERE g_hs_id = %s', (session['u_id'],))
        student_grade_HS = cursor.fetchone()
        
        cursor.execute('SELECT * FROM student_grade_shs WHERE g_shs_id = %s', (session['u_id'],))
        student_grade = cursor.fetchone()
        
        cursor.execute('SELECT * FROM recommended_course WHERE rc_id = %s', (session['u_id'],))
        student_rc = cursor.fetchone()
        
        # Pass the get_course_definition function to the template context
        return render_template('student/recommendation.html', user=user_data, student=student_profile, grade=student_grade, grade_hs=student_grade_HS, student_rc=student_rc, get_course_definition=get_course_definition)        
    else:
        flash('Unauthorized access, please log in')
        return redirect(url_for('login'))
    
@app.route('/student/grades')
def student_grades():
    
    if 'loggedin' in session and 'u_id' in session:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Select user data based on session u_id
        cursor.execute('SELECT * FROM users WHERE u_id = %s', (session['u_id'],))
        user_data = cursor.fetchone()
        
        cursor.execute('SELECT * FROM student_profile WHERE s_id = %s', (session['u_id'],))
        student_profile = cursor.fetchone()
        
        cursor.execute('SELECT * FROM student_grade_hs WHERE g_hs_id = %s', (session['u_id'],))
        student_grade_HS = cursor.fetchone()
        
        cursor.execute('SELECT * FROM student_grade_shs WHERE g_shs_id = %s', (session['u_id'],))
        student_grade = cursor.fetchone()
        
        # Pass the get_course_definition function to the template context
        return render_template('student/s_grades.html', user=user_data, student=student_profile, grade=student_grade, grade_hs=student_grade_HS)        
    else:
        flash('Unauthorized access, please log in')
        return redirect(url_for('login'))

#courses.html 
@app.route('/student/courses')
def student_courses():
    
    # Check if 'email' key is present in the session
    if 'email' in session:
        return render_template('student/courses.html', f_name=session['f_name'], m_name=session['m_name'], l_name=session['l_name'], role=session['role'], email=session['email'])
    else:
        # Redirect the user to the login page or display an error message
        flash('Please log in to access this page.')
        return redirect(url_for('login'))

#about.html 
@app.route('/student/about')
def student_about():
    # Check if 'email' key is present in the session
    if 'email' in session:
        return render_template('student/about.html', f_name=session['f_name'], m_name=session['m_name'], l_name=session['l_name'], role=session['role'], email=session['email'])
    else:
        # Redirect the user to the login page or display an error message
        flash('Please log in to access this page.')
        return redirect(url_for('login'))

#print.html 
@app.route('/student/print')
def print_form():
    
    if 'loggedin' in session and 'u_id' in session:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Select user data based on session u_id
        cursor.execute('SELECT * FROM users WHERE u_id = %s', (session['u_id'],))
        user_data = cursor.fetchone()
        
        cursor.execute('SELECT * FROM student_profile WHERE s_id = %s', (session['u_id'],))
        student_profile = cursor.fetchone()
        
        cursor.execute('SELECT * FROM student_grade_hs WHERE g_hs_id = %s', (session['u_id'],))
        student_grade_HS = cursor.fetchone()
        
        cursor.execute('SELECT * FROM student_grade_shs WHERE g_shs_id = %s', (session['u_id'],))
        student_grade = cursor.fetchone()
        
        return render_template('student/print.html', user=user_data, student=student_profile, grade=student_grade, grade_hs=student_grade_HS)
        
    else:
        flash('Unauthorized access, please log in')
        return redirect(url_for('login'))


#update junior high school grade
@app.route('/student/update_JHS_grades', methods=['POST'])
def update_JHS_grades():
    
    if request.method == 'POST':
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        english9 = request.form['english9']
        filipino9 = request.form['filipino9']
        mathematics9 = request.form['mathematics9']
        science9 = request.form['science9']
        aralingpanlipunan9 = request.form['aralingpanlipunan9']
        edukasyonsapagpapakatao9 = request.form['edukasyonsapagpapakatao9']
        music9 = request.form['music9']
        arts9 = request.form['arts9']
        physicaleducation9 = request.form['physicaleducation9']
        health9 = request.form['health9']
        edukasyongpantahananatpangkabuhayan9 = request.form['edukasyongpantahananatpangkabuhayan9']
        technologyandlivelihoodeducation9 = request.form['technologyandlivelihoodeducation9']
        
        english10 = request.form['english10']
        filipino10 = request.form['filipino10']
        mathematics10 = request.form['mathematics10']
        science10 = request.form['science10']
        aralingpanlipunan10 = request.form['aralingpanlipunan10']
        edukasyonsapagpapakatao10 = request.form['edukasyonsapagpapakatao10']
        music10 = request.form['music10']
        arts10 = request.form['arts10']
        physicaleducation10 = request.form['physicaleducation10']
        health10 = request.form['health10']
        edukasyongpantahananatpangkabuhayan10 = request.form['edukasyongpantahananatpangkabuhayan10']
        technologyandlivelihoodeducation10 = request.form['technologyandlivelihoodeducation10']
        
        # Get u_id from session
        u_id = session.get('u_id')
        
         # Update data in student_profile table
        cursor.execute("""
            UPDATE student_grade_hs
            SET english9 = %s, filipino9 = %s, mathematics9 = %s, science9 = %s, aralingpanlipunan9 = %s, edukasyonsapagpapakatao9 = %s,  "music9" = %s, arts9 = %s, physicaleducation9 = %s, health9 = %s, edukasyongpantahananatpangkabuhayan9 = %s, technologyandlivelihoodeducation9 = %s, english10 = %s, filipino10 = %s, mathematics10 = %s, science10 = %s, aralingpanlipunan10 = %s, edukasyonsapagpapakatao10 = %s,  "music10" = %s, arts10 = %s, physicaleducation10 = %s, health10 = %s, edukasyongpantahananatpangkabuhayan10 = %s, technologyandlivelihoodeducation10 = %s
            WHERE g_hs_id = %s
        """, (english9, filipino9, mathematics9, science9, aralingpanlipunan9, edukasyonsapagpapakatao9, music9, arts9, physicaleducation9, health9, edukasyongpantahananatpangkabuhayan9, technologyandlivelihoodeducation9, english10, filipino10, mathematics10, science10, aralingpanlipunan10, edukasyonsapagpapakatao10, music10, arts10, physicaleducation10, health10, edukasyongpantahananatpangkabuhayan10, technologyandlivelihoodeducation10, u_id))
            
        conn.commit()

        # Redirect to input_grade after successful submission
        return redirect(url_for('student_grades'))
    
    
#update senior high school grade
@app.route('/student/update_SHS_grades', methods=['POST'])
def update_SHS_grades():
    
    if request.method == 'POST':
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
            # Get u_id from session
            u_id = session.get('u_id')
        
            # Get existing data from the database to pre-fill the form
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("SELECT track FROM student_profile WHERE s_id = %s", (u_id,))
            track = cursor.fetchone()

            # Get the track value from the track dictionary
            track_value = track['track']

            def get_form_value(field):
                return request.form.get(field) or None

            if track_value == 'STEM':
                # Insert grades for STEM track, set others to NULL
                cursor.execute("""
                    UPDATE student_grade_shs SET earthandlifescience = %s, physicalscience = %s, earthscience = %s, genbio1 = %s, genbio2 = %s, genphysics1 = %s, genphysics2 = %s, genchem1 = %s, genchem2 = %s, generalmath = %s, statisticsandprobability = %s, precalculus = %s, basiccalculus = %s, oralcommunication = %s, reading_and_writing = %s, mediaandinformationliteracy = %s, t21stcenturyliteraturefromthephilippinesandtheworld = %s, contemporaryphilippineartsfromtheregions = %s, pagbasaatpagsusuringibatibangtekstotungosapananaliksik = %s, komunikasyonatpananaliksiksawikaatkulturangpilipino = %s, personaldevelopment = %s, introductiontothephilosophyofthehumanperson = %s, understandingculturesocietyandpolitics = %s, disasterreadinessandrisk_reduction = %s, physicaleducationandhealth = %s, physicaleducationandhealth2 = %s, physicaleducationandhealth3 = %s, physicaleducationandhealth4 = %s
                    WHERE g_shs_id = %s
                """, (get_form_value('earthandlifescience'), get_form_value('physicalscience'), get_form_value('earthscience'),
                    get_form_value('genbio1'), get_form_value('genbio2'), get_form_value('genphysics1'), get_form_value('genphysics2'),
                    get_form_value('genchem1'), get_form_value('genchem2'), get_form_value('generalmath'), get_form_value('statisticsandprobability'),
                    get_form_value('precalculus'), get_form_value('basiccalculus'), get_form_value('oralcommunication'), get_form_value('reading_and_writing'),
                    get_form_value('mediaandinformationliteracy'), get_form_value('t21stcenturyliteraturefromthephilippinesandtheworld'),
                    get_form_value('contemporaryphilippineartsfromtheregions'), get_form_value('pagbasaatpagsusuringibatibangtekstotungosapananaliksik'),
                    get_form_value('komunikasyonatpananaliksiksawikaatkulturangpilipino'), get_form_value('personaldevelopment'),
                    get_form_value('introductiontothephilosophyofthehumanperson'), get_form_value('understandingculturesocietyandpolitics'),
                    get_form_value('disasterreadinessandrisk_reduction'), get_form_value('physicaleducationandhealth'),
                    get_form_value('physicaleducationandhealth2'), get_form_value('physicaleducationandhealth3'), get_form_value('physicaleducationandhealth4'), u_id))
                conn.commit()
                return redirect(url_for('student_grades'))
        
            elif track_value == 'ABM':
                # Update grades for ABM track, set others to NULL
                cursor.execute("""
                    UPDATE student_grade_shs SET earthandlifescience = %s, physicalscience = %s, earthscience = %s, generalmath = %s, statisticsandprobability = %s, businessmath = %s, businessfinance = %s, oralcommunication = %s, reading_and_writing = %s, mediaandinformationliteracy = %s, t21stcenturyliteraturefromthephilippinesandtheworld = %s, contemporaryphilippineartsfromtheregions = %s, pagbasaatpagsusuringibatibangtekstotungosapananaliksik = %s, komunikasyonatpananaliksiksawikaatkulturangpilipino = %s, personaldevelopment = %s, introductiontothephilosophyofthehumanperson = %s, understandingculturesocietyandpolitics = %s, disasterreadinessandrisk_reduction = %s, physicaleducationandhealth = %s, physicaleducationandhealth2 = %s, physicaleducationandhealth3 = %s, physicaleducationandhealth4 = %s, organizationandmanagement = %s, principlesofmarketing = %s, businessmarketing = %s, businessenterpriseandsimulation = %s, f1_fundamentalsofaccountancybusinessandmanagement1 = %s, f2_fundamentalsofaccountancybusinessandmanagement2 = %s, appliedeconomicsbusiness = %s, ethicsandsocial_responsibility = %s
                    WHERE g_shs_id = %s
                """, (get_form_value('earthandlifescience'), get_form_value('physicalscience'), get_form_value('earthscience'),
                    get_form_value('generalmath'), get_form_value('statisticsandprobability'), get_form_value('businessmath'),
                    get_form_value('businessfinance'), get_form_value('oralcommunication'), get_form_value('reading_and_writing'),
                    get_form_value('mediaandinformationliteracy'), get_form_value('t21stcenturyliteraturefromthephilippinesandtheworld'),
                    get_form_value('contemporaryphilippineartsfromtheregions'), get_form_value('pagbasaatpagsusuringibatibangtekstotungosapananaliksik'),
                    get_form_value('komunikasyonatpananaliksiksawikaatkulturangpilipino'), get_form_value('personaldevelopment'),
                    get_form_value('introductiontothephilosophyofthehumanperson'), get_form_value('understandingculturesocietyandpolitics'),
                    get_form_value('disasterreadinessandrisk_reduction'), get_form_value('physicaleducationandhealth'),
                    get_form_value('physicaleducationandhealth2'), get_form_value('physicaleducationandhealth3'), get_form_value('physicaleducationandhealth4'),
                    get_form_value('organizationandmanagement'), get_form_value('principlesofmarketing'), get_form_value('businessmarketing'),
                    get_form_value('businessenterpriseandsimulation'), get_form_value('f1_fundamentalsofaccountancybusinessandmanagement1'),
                    get_form_value('f2_fundamentalsofaccountancybusinessandmanagement2'), get_form_value('appliedeconomicsbusiness'),
                    get_form_value('ethicsandsocial_responsibility'), u_id))
                conn.commit()
                return redirect(url_for('student_grades'))
            
            elif track_value == 'HUMSS':
                # Update grades for HUMSS track, set others to NULL
                cursor.execute("""
                    UPDATE student_grade_shs SET earthandlifescience = %s, physicalscience = %s, earthscience = %s, generalmath = %s, 
                    statisticsandprobability = %s, oralcommunication = %s, reading_and_writing = %s, mediaandinformationliteracy = %s, 
                    t21stcenturyliteraturefromthephilippinesandtheworld = %s, contemporaryphilippineartsfromtheregions = %s, creativenonfiction = %s, 
                    pagbasaatpagsusuringibatibangtekstotungosapananaliksik = %s, komunikasyonatpananaliksiksawikaatkulturangpilipino = %s, 
                    creativewriting_malikhaing_pagsulat = %s, personaldevelopment = %s, introductiontothephilosophyofthehumanperson = %s, 
                    understandingculturesocietyandpolitics = %s, disasterreadinessandrisk_reduction = %s, physicaleducationandhealth = %s, 
                    physicaleducationandhealth2 = %s, physicaleducationandhealth3 = %s, physicaleducationandhealth4 = %s, 
                    introductiontoworldreligionsandbeliefsystems = %s, community_engagementsolidarityandcitizenship = %s, 
                    philippinepoliticsandgovernance = %s, disciplinesandideasinthesocialsciences = %s
                    WHERE g_shs_id = %s
                """, (request.form.get('earthandlifescience'), request.form.get('physicalscience'), request.form.get('earthscience'), 
                    request.form.get('generalmath'), request.form.get('statisticsandprobability'), request.form.get('oralcommunication'), 
                    request.form.get('reading_and_writing'), request.form.get('mediaandinformationliteracy'), 
                    request.form.get('t21stcenturyliteraturefromthephilippinesandtheworld'), request.form.get('contemporaryphilippineartsfromtheregions'), 
                    request.form.get('creativenonfiction'), request.form.get('pagbasaatpagsusuringibatibangtekstotungosapananaliksik'), 
                    request.form.get('komunikasyonatpananaliksiksawikaatkulturangpilipino'), request.form.get('creativewriting_malikhaing_pagsulat'), 
                    request.form.get('personaldevelopment'), request.form.get('introductiontothephilosophyofthehumanperson'), 
                    request.form.get('understandingculturesocietyandpolitics'), request.form.get('disasterreadinessandrisk_reduction'), 
                    request.form.get('physicaleducationandhealth'), request.form.get('physicaleducationandhealth2'), 
                    request.form.get('physicaleducationandhealth3'), request.form.get('physicaleducationandhealth4'), 
                    request.form.get('introductiontoworldreligionsandbeliefsystems'), request.form.get('community_engagementsolidarityandcitizenship'), 
                    request.form.get('philippinepoliticsandgovernance'), request.form.get('disciplinesandideasinthesocialsciences'), u_id))
                conn.commit()
                return redirect(url_for('student_grades'))
            
            elif track_value == 'GAS':
                # Update grades for GAS track, set others to NULL
                cursor.execute("""
                    UPDATE student_grade_shs SET earthandlifescience = %s, physicalscience = %s, earthscience = %s, generalmath = %s, 
                    statisticsandprobability = %s, oralcommunication = %s, reading_and_writing = %s, mediaandinformationliteracy = %s, 
                    t21stcenturyliteraturefromthephilippinesandtheworld = %s, contemporaryphilippineartsfromtheregions = %s, creativewriting = %s, 
                    pagbasaatpagsusuringibatibangtekstotungosapananaliksik = %s, komunikasyonatpananaliksiksawikaatkulturangpilipino = %s, 
                    personaldevelopment = %s, introductiontothephilosophyofthehumanperson = %s, understandingculturesocietyandpolitics = %s, 
                    disasterreadinessandrisk_reduction = %s, physicaleducationandhealth = %s, physicaleducationandhealth2 = %s, 
                    physicaleducationandhealth3 = %s, physicaleducationandhealth4 = %s, humanities1_politics = %s, humanities2_intro = %s, 
                    socialscience1 = %s, organizationandmanagement2 = %s, appliedeconomics2 = %s, introtoworldreligionsandsytembeliefs = %s, 
                    philippinepiliticsandgovernance = %s 
                    WHERE g_shs_id = %s
                """, (request.form.get('earthandlifescience'), request.form.get('physicalscience'), request.form.get('earthscience'), 
                    request.form.get('generalmath'), request.form.get('statisticsandprobability'), request.form.get('oralcommunication'), 
                    request.form.get('reading_and_writing'), request.form.get('mediaandinformationliteracy'), 
                    request.form.get('t21stcenturyliteraturefromthephilippinesandtheworld'), request.form.get('contemporaryphilippineartsfromtheregions'), 
                    request.form.get('creativewriting'), request.form.get('pagbasaatpagsusuringibatibangtekstotungosapananaliksik'), 
                    request.form.get('komunikasyonatpananaliksiksawikaatkulturangpilipino'), request.form.get('personaldevelopment'), 
                    request.form.get('introductiontothephilosophyofthehumanperson'), request.form.get('understandingculturesocietyandpolitics'), 
                    request.form.get('disasterreadinessandrisk_reduction'), request.form.get('physicaleducationandhealth'), 
                    request.form.get('physicaleducationandhealth2'), request.form.get('physicaleducationandhealth3'), 
                    request.form.get('physicaleducationandhealth4'), request.form.get('humanities1_politics'), request.form.get('humanities2_intro'), 
                    request.form.get('socialscience1'), request.form.get('organizationandmanagement2'), request.form.get('appliedeconomics2'), 
                    request.form.get('introtoworldreligionsandsytembeliefs'), request.form.get('philippinepiliticsandgovernance'), u_id))
                conn.commit()
                return redirect(url_for('student_grades'))

            ### TVL Track:
            elif track_value == 'TVL':
                # Update grades for TVL track, set others to NULL
                cursor.execute("""
                    UPDATE student_grade_shs SET earthandlifescience = %s, physicalscience = %s, earthscience = %s, generalmath = %s, 
                    statisticsandprobability = %s, oralcommunication = %s, reading_and_writing = %s, mediaandinformationliteracy = %s, 
                    t21stcenturyliteraturefromthephilippinesandtheworld = %s, contemporaryphilippineartsfromtheregions = %s, creativewriting = %s, 
                    pagbasaatpagsusuringibatibangtekstotungosapananaliksik = %s, komunikasyonatpananaliksiksawikaatkulturangpilipino = %s, 
                    personaldevelopment = %s, introductiontothephilosophyofthehumanperson = %s, understandingculturesocietyandpolitics = %s, 
                    disasterreadinessandrisk_reduction = %s, physicaleducationandhealth = %s, physicaleducationandhealth2 = %s, 
                    physicaleducationandhealth3 = %s, physicaleducationandhealth4 = %s, safetyandfirstaid = %s, humanmovement = %s, 
                    fundamentalsofcoaching = %s
                    WHERE g_shs_id = %s
                """, (request.form.get('earthandlifescience'), request.form.get('physicalscience'), request.form.get('earthscience'), 
                    request.form.get('generalmath'), request.form.get('statisticsandprobability'), request.form.get('oralcommunication'), 
                    request.form.get('reading_and_writing'), request.form.get('mediaandinformationliteracy'), 
                    request.form.get('t21stcenturyliteraturefromthephilippinesandtheworld'), request.form.get('contemporaryphilippineartsfromtheregions'), 
                    request.form.get('creativewriting'), request.form.get('pagbasaatpagsusuringibatibangtekstotungosapananaliksik'), 
                    request.form.get('komunikasyonatpananaliksiksawikaatkulturangpilipino'), request.form.get('personaldevelopment'), 
                    request.form.get('introductiontothephilosophyofthehumanperson'), request.form.get('understandingculturesocietyandpolitics'), 
                    request.form.get('disasterreadinessandrisk_reduction'), request.form.get('physicaleducationandhealth'), 
                    request.form.get('physicaleducationandhealth2'), request.form.get('physicaleducationandhealth3'), 
                    request.form.get('physicaleducationandhealth4'), request.form.get('safetyandfirstaid'), request.form.get('humanmovement'), 
                    request.form.get('fundamentalsofcoaching'), u_id))
                conn.commit()
                return redirect(url_for('student_grades'))

    # If it's not a POST request
    return redirect(url_for('login'))

def load_schools():
    try:
        with open('schools.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    
def save_schools(schools):
    with open('schools.json', 'w') as f:
        json.dump(schools, f)

@app.route('/add_school', methods=['POST'])
def add_school():
    school_name = request.form.get('school_name').strip()
    school_address = request.form.get('school_address').strip() 

    schools = load_schools()
    
    schools_lower = [s['name'].lower() for s in schools]
    school_name_lower = school_name.lower()
    
    if school_name and school_name_lower not in schools_lower:
        schools.append({"name": school_name, "address": school_address}) 
        save_schools(schools)
        
        print(f"New school added: {school_name}")
        return jsonify({"success": True, "message": "School added", "school_name": school_name, "address": school_address})
    else:
        print(f"School already exists or name is invalid: {school_name}")
        return jsonify({"success": False, "message": "School already exists or name is invalid", "school_name": school_name})

@app.route('/load_schools', methods=['GET'])
def load_schools_route():
    schools = load_schools()
    return jsonify(schools)

@app.route('/delete_grade_form/<int:user_id>', methods=['POST'])
def delete_grade_form(user_id):
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    # Fetch user and profile data
    cursor.execute('SELECT * FROM users WHERE u_id = %s', (user_id,))
    user_data = cursor.fetchone()
    cursor.execute('SELECT * FROM student_profile WHERE s_id = %s', (user_id,))
    profile = cursor.fetchone()
    
    filename = profile['verified_grades']
    
    # Delete the file if it exists
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    
    # Reset the verified_grades in the student_profile table
    cursor.execute("UPDATE student_profile SET verified_grades = NULL WHERE s_id = %s", (user_id,))

    # Optionally, remove the application entry if necessary (depending on your logic)
    cursor.execute("DELETE FROM applications WHERE student_id = %s", (user_id,))  # Delete the application

    conn.commit()
    
    flash('Grade form deleted successfully. User can now re-upload.', 'success')
    return redirect(url_for('view_unverified', user_id=user_id))

@app.route('/admin/visualization', methods=['GET'])
def admin_visualization():
    if 'role' in session and session['role'] == 'admin':
        try:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            # Count of students who submitted applications but are still pending (not confirmed)
            cursor.execute(""" 
                SELECT COUNT(*)
                FROM applications a
                JOIN users u ON a.student_id = u.u_id
                WHERE a.status = 'Pending'
            """)
            students_applying_count = cursor.fetchone()[0]  # This should return a whole number

            # Query to get students who have applied
            cursor.execute(""" 
                SELECT u.u_id, u.f_name, u.m_name, u.l_name, u.email, u.s_date, a.status AS application_status
                FROM users u
                JOIN applications a ON u.u_id = a.student_id
                WHERE u.role = 'student'
                ORDER BY u.s_date DESC
            """)
            students_applying = cursor.fetchall()

            # Query to get the count of students by sex for the gender pie chart
            cursor.execute(""" 
                SELECT sex, COUNT(*) AS count
                FROM student_profile
                GROUP BY sex
            """)
            gender_data = cursor.fetchall()

            # Convert to JSON-serializable format for gender
            pie_gender = [{'value': int(row['count']), 'name': row['sex']} for row in gender_data]  # Ensure count is an int

            # Query to get the count of students by track
            cursor.execute(""" 
                SELECT track, COUNT(*) AS count
                FROM student_profile
                WHERE track IN ('STEM', 'ABM', 'HUMSS', 'GAS', 'TVL')
                GROUP BY track
            """)
            track_data = cursor.fetchall()

            # Convert to JSON-serializable format for track
            pie_track = [{'value': int(row['count']), 'name': row['track']} for row in track_data]  # Ensure count is an int

            courses = {
                'BSCE - BACHELOR OF SCIENCE IN CIVIL ENGINEERING' : 'COE',
                'BSBIO(MCB) - BACHELOR OF SCIENCE IN BIOLOGY(MICROBIOLOGY)' : 'CSM',
                'BSEE - BACHELOR OF SCIENCE IN ELECTRICAL ENGINEERING' : 'COE',
                'BSMETE - BACHELOR OF SCIENCE METALLURGICAL ENGINEERING' : 'COE',
                'BSBIO(AnBio) - BACHELOR OF SCIENCE IN BIOLOGY(ANIMAL BIOLOGY)' : 'CSM',
                'BSCHEM - BACHELOR OF SCIENCE IN CHEMISTRY' : 'CSM',
                'BSCHE - BACHELOR OF SCIENCE IN CHEMICAL ENGINEERING' : 'COE',
                'BSPHYSICS - BACHELOR OF SCIENCE IN PHYSICS' : 'CSM',
                'BSNURSING - BACHELOR OF SCIENCE IN NURSING' : 'CHS',
                'BSEsE - BACHELOR OF SCIENCE IN ELECTRONICS ENGINEERING' : 'COE',
                'BSA - BACHELOR OF SCIENCE IN ACCOUNTANCY' : 'CEBA',
                'BSMARINE BIO - BACHELOR OF SCIENCE IN MARINE BIOLOGY' : 'CSM',
                'BSIT - BACHELOR OF SCIENCE IN INFORMATION TECHNOLOGY' : 'CCS',
                'BSCPE - BACHELOR OF SCIENCE IN COMPUTER ENGINEERING' : 'COE',
                'BA POL SCI - BACHELOR OF ARTS IN POLITICAL SCIENCE' : 'CASS',
                'BSME - BACHELOR OF SCIENCE IN MECHANICAL ENGINEERING' : 'COE',
                'BA ELS - BACHELOR OF ARTS IN ENGLISH LANGUAGE STUDIES' : 'CASS',
                'BSBIO(Bdv) - BACHELOR OF SCIENCE IN BIOLOGY (BIODIVERSITY)' : 'CSM',
                'BSMATH - BACHELOR OF SCIENCE IN MATHEMATICS' : 'CSM',
                'BSBIO(PlBio) - BACHELOR OF SCIENCE IN BIOLOGY(PLANT BIOLOGY)' : 'CSM',
                'BSED BIO - BACHELOR OF SECONDARY EDUCATION (BIOLOGY)' : 'CED',
                'BS PSYCH - BACHELOR OF SCIENCE IN PSYCHOLOGY' : 'CASS',
                'BSCS - BACHELOR OF SCIENCE IN COMPUTER SCIENCE' : 'CCS',
                'BS HM - BACHELOR OF SCIENCE IN HOSPITALITY MANAGEMENT' : 'CEBA',
                'BS PHIL - BACHELOR OF SCIENCE IN PHILOSOPHY MAJOR IN APPLIED ETHICS' : 'CASS',
                'BET-CET - BACHELOR OF ENGINEERING TECHNOLOGY - CIVIL ENGINEERING TECHNOLOGY' : 'COE',
                'BET-MMT - BACHELOR OF ENGINEERING TECHNOLOGY-METALLURGY AND MATERIALS ENGINEERING TECHNOLOGY': 'COE',
                'BSEM - BACHELOR OF SCIENCE IN MINING ENGINEERING' : 'COE',
                'BSBA-MKT MGT - BACHELOR OF SCIENCE IN BUSINESS ADMINISTRATION (MARKETING MANAGEMENT)' : 'CEBA',
                'BS ECON - BACHELOR OF SCIENCE IN ECONOMICS' : 'CEBA',
                'BSIAM - BACHELOR OF SCIENCE IN INDUSTRIAL AUTOMATION & MECHATRONICS' : 'COE',
                'BS ENTREP - BACHELOR OF SCIENCE IN ENTREPRENEURSHIP' : 'CEBA',
                'BSED CHEM - BACHELOR OF SECONDARY EDUCATION (CHEMISTRY)': 'CED',
                'BTLED-IA - BACHELOR OF TECHNOLOGY AND LIVELIHOOD EDUCATION-INDUSTRIAL ARTS': 'CED',
                'BTVTED-DT - BACHELOR OF TECHNICAL-VOCATIONAL TEACHER EDUCATION DRAFTING TECHNOLOGY' : 'CED',
                'BPED - BACHELOR OF PHYSICAL EDUCATION' : 'CED',
                'BSBA-B.ECON - BACHELOR OF SCIENCE IN BUSINESS ADMINISTRATION (BUSINESS ECONOMICS)' : 'CEBA',
                'BSED PHYS - BACHELOR OF SECONDARY EDUCATION (PHYSICS)' : 'CED',
                'BSED MATH - BACHELOR OF SECONDARY EDUCATION (MATHEMATICS)' : 'CED',
                'BSIS - BACHELOR OF SCIENCE IN INFORMATION SYSTEMS' : 'CCS',
                'BSSTAT - BACHELOR OF SCIENCE IN STATISTICS' : 'CSM',
                'BA PSYCH - BACHELOR OF ARTS IN PSYCHOLOGY' : 'CASS',
                'BEED SCI MAT - BACHELOR OF ELEMENTARY EDUCATION (SCIENCE AND MATHEMATICS)' : 'CED',
                'BSED FIL - BACHELOR OF SECONDARY EDUCATION (FILIPINO)' : 'CED',
                'BEED Lang Ed - BACHELOR OF ELEMENTARY EDUCATION (LANGUAGE EDUCATION)' : 'CED',
                'BA HISTORY - BACHELOR OF ARTS IN HISTORY' : 'CASS',
                'BSCERE - BACHELOR OF SCIENCE IN CERAMIC ENGINEERING' : 'COE',
                'BTLED-HE - BACHELOR OF TECHNOLOGY AND LIVELIHOOD EDUCATION -HOME ECONOMICS' : 'CED',
                'BA FIL - BATSILYER NG SINING SA FILIPINO' : 'CASS',
                'BA SOCIO - BACHELOR OF ARTS IN SOCIOLOGY' : 'CASS',
                'BET-ELET - BACHELOR OF ENGINEERING TECHNOLOGY-ELECTRICAL ENGINEERING TECHNOLOGY' : 'COE',
                'BET-CHET - BACHELOR OF ENGINEERING TECHNOLOGY-CHEMICAL ENGINEERING TECHNOLOGY' : 'COE',
                'BET-ESET - BACHELOR OF ENGINEERING TECHNOLOGY-ELECTRONICS ENGINEERING TECHNOLOGY' : 'COE',
                'BET-MET - BACHELOR OF ENGINEERING TECHNOLOGY-MECHANICAL ENGINEERING TECHNOLOGY' : 'COE',
                'BSEnE - BACHELOR OF SCIENCE IN ENVIRONMENTAL ENGINEERING' : 'COE',
                'BSCA - BACHELOR OF SCIENCE IN COMPUTER APPLICATIONS' : 'CCS',
                'BS EnvET - BACHELOR OF SCIENCE IN ENVIRONMENTAL ENGINEERING TECHNOLOGY' : 'COE',
            }

            course_counts = {}
            for course in courses:
                cursor.execute(""" 
                    SELECT COUNT(*) 
                    FROM student_profile 
                    WHERE pref_course1 = %s OR pref_course2 = %s
                """, (course, course))
                course_counts[course] = cursor.fetchone()[0]

            # Close cursor
            cursor.close()

            return render_template(
                'admin/visualization.html', 
                students_applying_count=students_applying_count,
                students_applying=students_applying,
                pie_gender=pie_gender,
                pie_track=pie_track,
                course_counts=course_counts,
                courses=courses,
                f_name=session['f_name'], 
                m_name=session['m_name'], 
                l_name=session['l_name'], 
                role=session['role']
            )
        except Exception as e:
            print(f"Error: {e}")  # Log the error for debugging
            flash('An error occurred while fetching data. Please try again later.')
            return redirect(url_for('admin_dashboard'))  # Redirect to a safe place
    else:
        flash('Unauthorized access, please log in as an admin.')
        return redirect(url_for('login'))
    
@app.route('/admin/export_courses', methods=['GET'])
def export_courses():
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Define courses and their corresponding departments
        courses = {
            'BSCE - BACHELOR OF SCIENCE IN CIVIL ENGINEERING': 'COE',
            'BSBIO(MCB) - BACHELOR OF SCIENCE IN BIOLOGY(MICROBIOLOGY)': 'CSM',
            'BSEE - BACHELOR OF SCIENCE IN ELECTRICAL ENGINEERING': 'COE',
            'BSMETE - BACHELOR OF SCIENCE METALLURGICAL ENGINEERING': 'COE',
            'BSBIO(AnBio) - BACHELOR OF SCIENCE IN BIOLOGY(ANIMAL BIOLOGY)': 'CSM',
            'BSCHEM - BACHELOR OF SCIENCE IN CHEMISTRY': 'CSM',
            'BSCHE - BACHELOR OF SCIENCE IN CHEMICAL ENGINEERING': 'COE',
            'BSPHYSICS - BACHELOR OF SCIENCE IN PHYSICS': 'CSM',
            'BSNURSING - BACHELOR OF SCIENCE IN NURSING': 'CHS',
            'BSEsE - BACHELOR OF SCIENCE IN ELECTRONICS ENGINEERING': 'COE',
            'BSA - BACHELOR OF SCIENCE IN ACCOUNTANCY': 'CEBA',
            'BSMARINE BIO - BACHELOR OF SCIENCE IN MARINE BIOLOGY': 'CSM',
            'BSIT - BACHELOR OF SCIENCE IN INFORMATION TECHNOLOGY': 'CCS',
            'BSCPE - BACHELOR OF SCIENCE IN COMPUTER ENGINEERING': 'COE',
            'BA POL SCI - BACHELOR OF ARTS IN POLITICAL SCIENCE': 'CASS',
            'BSME - BACHELOR OF SCIENCE IN MECHANICAL ENGINEERING': 'COE',
            'BA ELS - BACHELOR OF ARTS IN ENGLISH LANGUAGE STUDIES': 'CASS',
            'BSBIO(Bdv) - BACHELOR OF SCIENCE IN BIOLOGY (BIODIVERSITY)': 'CSM',
            'BSMATH - BACHELOR OF SCIENCE IN MATHEMATICS': 'CSM',
            'BSBIO(PlBio) - BACHELOR OF SCIENCE IN BIOLOGY(PLANT BIOLOGY)': 'CSM',
            'BSED BIO - BACHELOR OF SECONDARY EDUCATION (BIOLOGY)': 'CED',
            'BS PSYCH - BACHELOR OF SCIENCE IN PSYCHOLOGY': 'CASS',
            'BSCS - BACHELOR OF SCIENCE IN COMPUTER SCIENCE': 'CCS',
            'BS HM - BACHELOR OF SCIENCE IN HOSPITALITY MANAGEMENT': 'CEBA',
            'BS PHIL - BACHELOR OF SCIENCE IN PHILOSOPHY MAJOR IN APPLIED ETHICS': 'CASS',
            'BET-CET - BACHELOR OF ENGINEERING TECHNOLOGY - CIVIL ENGINEERING TECHNOLOGY': 'COE',
            'BET-MMT - BACHELOR OF ENGINEERING TECHNOLOGY-METALLURGY AND MATERIALS ENGINEERING TECHNOLOGY': 'COE',
            'BSEM - BACHELOR OF SCIENCE IN MINING ENGINEERING': 'COE',
            'BSBA-MKT MGT - BACHELOR OF SCIENCE IN BUSINESS ADMINISTRATION (MARKETING MANAGEMENT)': 'CEBA',
            'BS ECON - BACHELOR OF SCIENCE IN ECONOMICS': 'CEBA',
            'BSIAM - BACHELOR OF SCIENCE IN INDUSTRIAL AUTOMATION & MECHATRONICS': 'COE',
            'BS ENTREP - BACHELOR OF SCIENCE IN ENTREPRENEURSHIP': 'CEBA',
            'BSED CHEM - BACHELOR OF SECONDARY EDUCATION (CHEMISTRY)': 'CED',
            'BTLED-IA - BACHELOR OF TECHNOLOGY AND LIVELIHOOD EDUCATION-INDUSTRIAL ARTS': 'CED',
            'BTVTED-DT - BACHELOR OF TECHNICAL-VOCATIONAL TEACHER EDUCATION DRAFTING TECHNOLOGY': 'CED',
            'BPED - BACHELOR OF PHYSICAL EDUCATION': 'CED',
            'BSBA-B.ECON - BACHELOR OF SCIENCE IN BUSINESS ADMINISTRATION (BUSINESS ECONOMICS)': 'CEBA',
            'BSED PHYS - BACHELOR OF SECONDARY EDUCATION (PHYSICS)': 'CED',
            'BSED MATH - BACHELOR OF SECONDARY EDUCATION (MATHEMATICS)': 'CED',
            'BSIS - BACHELOR OF SCIENCE IN INFORMATION SYSTEMS': 'CCS',
            'BSSTAT - BACHELOR OF SCIENCE IN STATISTICS': 'CSM',
            'BA PSYCH - BACHELOR OF ARTS IN PSYCHOLOGY' : 'CASS',
            'BEED SCI MAT - BACHELOR OF ELEMENTARY EDUCATION (SCIENCE AND MATHEMATICS)': 'CED',
            'BSED FIL - BACHELOR OF SECONDARY EDUCATION (FILIPINO)': 'CED',
            'BEED Lang Ed - BACHELOR OF ELEMENTARY EDUCATION (LANGUAGE EDUCATION)': 'CED',
            'BA HISTORY - BACHELOR OF ARTS IN HISTORY': 'CASS',
            'BSCERE - BACHELOR OF SCIENCE IN CERAMIC ENGINEERING': 'COE',
            'BTLED-HE - BACHELOR OF TECHNOLOGY AND LIVELIHOOD EDUCATION -HOME ECONOMICS': 'CED',
            'BA FIL - BATSILYER NG SINING SA FILIPINO': 'CASS',
            'BA SOCIO - BACHELOR OF ARTS IN SOCIOLOGY': 'CASS',
            'BET-ELET - BACHELOR OF ENGINEERING TECHNOLOGY-ELECTRICAL ENGINEERING TECHNOLOGY': 'COE',
            'BET-CHET - BACHELOR OF ENGINEERING TECHNOLOGY-CHEMICAL ENGINEERING TECHNOLOGY': 'COE',
            'BET-ESET - BACHELOR OF ENGINEERING TECHNOLOGY-ELECTRONICS ENGINEERING TECHNOLOGY': 'COE',
            'BET-MET - BACHELOR OF ENGINEERING TECHNOLOGY-MECHANICAL ENGINEERING TECHNOLOGY': 'COE',
            'BSEnE - BACHELOR OF SCIENCE IN ENVIRONMENTAL ENGINEERING': 'COE',
            'BSCA - BACHELOR OF SCIENCE IN COMPUTER APPLICATIONS': 'CCS',
            'BS EnvET - BACHELOR OF SCIENCE IN ENVIRONMENTAL ENGINEERING TECHNOLOGY': 'COE',
        }

        # List of departments to filter by
        departments_to_export = ['COE', 'CSM', 'CHS', 'CED', 'CASS', 'CEBA', 'CSS']

        course_counts = {}
        for course, department in courses.items():
            if department in departments_to_export:  # Only export specified departments
                cursor.execute(""" 
                    SELECT COUNT(*) 
                    FROM student_profile 
                    WHERE pref_course1 = %s OR pref_course2 = %s
                """, (course, course))
                count = cursor.fetchone()[0]
                # Store the count along with the department
                course_counts[course] = {'count': count, 'department': department}

        # Prepare data for the Excel file
        course_data = [
            {'College': info['department'], 'Program': course, 'Total Students': info['count']}
            for course, info in course_counts.items()
        ]
        df = pd.DataFrame(course_data)

        # Create a BytesIO buffer to hold the Excel file
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Preferred Courses Selected')

        # Seek to the beginning of the stream
        output.seek(0)

        # Send the Excel file as a response
        return send_file(output, as_attachment=True, download_name='students_preferred_courses.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    except Exception as e:
        print(f"Error exporting courses: {e}")
        flash('An error occurred while exporting data. Please try again later.')
        return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')