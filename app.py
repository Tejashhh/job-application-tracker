from flask import Flask, render_template, request, redirect, url_for, flash  # Added flash here
import mysql.connector
import json
from database import get_db_connection

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Add this for flash messages to work

def get_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='HHH###azzing_559',
        database='job_tracker'
    )

@app.route('/')
def dashboard():
    """Show statistics overview"""
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    # Get counts
    cursor.execute("SELECT COUNT(*) as count FROM companies")
    total_companies = cursor.fetchone()
    
    cursor.execute("SELECT COUNT(*) as count FROM jobs")
    total_jobs = cursor.fetchone()
    
    cursor.execute("SELECT COUNT(*) as count FROM applications")
    total_apps = cursor.fetchone()
    
    cursor.execute("SELECT COUNT(*) as count FROM contacts")
    total_contacts = cursor.fetchone()
    
    # Get status breakdown for applications
    cursor.execute("""
        SELECT status, COUNT(*) as count 
        FROM applications 
        GROUP BY status
    """)
    status_stats = cursor.fetchall()
    
    # Get recent applications
    cursor.execute("""
        SELECT a.*, j.job_title, c.company_name 
        FROM applications a
        JOIN jobs j ON a.job_id = j.job_id
        JOIN companies c ON j.company_id = c.company_id
        ORDER BY a.application_date DESC LIMIT 5
    """)
    recent_applications = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('dashboard.html', 
                         total_companies=total_companies,
                         total_jobs=total_jobs,
                         total_apps=total_apps,
                         total_contacts=total_contacts,
                         status_stats=status_stats,
                         recent_applications=recent_applications)

# ==================== COMPANIES CRUD ====================

@app.route('/companies')
def list_companies():
    """List all companies"""
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM companies ORDER BY company_name")
    companies = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('companies.html', companies=companies)

@app.route('/companies/add', methods=['GET', 'POST'])
def add_company():
    """Add a new company"""
    if request.method == 'POST':
        # Get form data
        company_name = request.form['company_name']
        industry = request.form.get('industry', '')
        website = request.form.get('website', '')
        city = request.form.get('city', '')
        state = request.form.get('state', '')
        notes = request.form.get('notes', '')
        
        # Insert into database
        conn = get_db()
        cursor = conn.cursor()
        query = """INSERT INTO companies 
                   (company_name, industry, website, city, state, notes) 
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        values = (company_name, industry, website, city, state, notes)
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Company added successfully!', 'success')  # Fixed: changed Flask to flash
        return redirect(url_for('list_companies'))
    
    # GET request - show the form
    return render_template('company_form.html', company=None)

@app.route('/companies/edit/<int:company_id>', methods=['GET', 'POST'])
def edit_company(company_id):
    """Edit a company"""
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        # Update the company
        query = """UPDATE companies 
                   SET company_name=%s, industry=%s, website=%s, 
                       city=%s, state=%s, notes=%s 
                   WHERE company_id=%s"""
        values = (
            request.form['company_name'],
            request.form.get('industry', ''),
            request.form.get('website', ''),
            request.form.get('city', ''),
            request.form.get('state', ''),
            request.form.get('notes', ''),
            company_id
        )
        cursor.execute(query, values)
        conn.commit()
        flash('Company updated successfully!', 'success')  # Fixed: changed Flask to flash
        cursor.close()
        conn.close()
        return redirect(url_for('list_companies'))
    
    # GET request - show the form with existing data
    cursor.execute("SELECT * FROM companies WHERE company_id = %s", (company_id,))
    company = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not company:
        flash('Company not found!', 'error')  # Fixed: changed Flask to flash
        return redirect(url_for('list_companies'))
    
    return render_template('company_form.html', company=company)

@app.route('/companies/delete/<int:company_id>')
def delete_company(company_id):
    """Delete a company"""
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM companies WHERE company_id = %s", (company_id,))
        conn.commit()
        flash('Company deleted successfully!', 'success')  # Fixed: changed Flask to flash
    except Exception as e:
        flash(f'Error deleting company: {str(e)}', 'error')  # Fixed: changed Flask to flash
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('list_companies'))

# ==================== JOBS CRUD ====================

@app.route('/jobs')
def list_jobs():
    """List all jobs with company names"""
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT j.*, c.company_name 
        FROM jobs j
        JOIN companies c ON j.company_id = c.company_id
        ORDER BY j.date_posted DESC
    """)
    jobs = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('jobs.html', jobs=jobs)

@app.route('/jobs/add', methods=['GET', 'POST'])
def add_job():
    """Add a new job"""
    if request.method == 'POST':
        # Handle requirements - collect all requirements[] fields
        requirements = request.form.getlist('requirements[]')
        # Filter out empty strings
        requirements = [r.strip() for r in requirements if r.strip()]
        requirements_json = json.dumps(requirements)
        
        conn = get_db()
        cursor = conn.cursor()
        query = """INSERT INTO jobs 
                   (company_id, job_title, job_type, salary_min, salary_max, 
                    job_url, date_posted, requirements) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (
            request.form['company_id'],
            request.form['job_title'],
            request.form['job_type'],
            request.form.get('salary_min') or None,
            request.form.get('salary_max') or None,
            request.form.get('job_url', ''),
            request.form.get('date_posted') or None,
            requirements_json
        )
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
        flash('Job added successfully!', 'success')  # Fixed: changed Flask to flash
        return redirect(url_for('list_jobs'))
    
    # GET request - show form with companies dropdown
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT company_id, company_name FROM companies ORDER BY company_name")
    companies = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('job_form.html', companies=companies, job=None)

@app.route('/jobs/edit/<int:job_id>', methods=['GET', 'POST'])
def edit_job(job_id):
    """Edit a job"""
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        # Handle requirements
        requirements = request.form.getlist('requirements[]')
        requirements = [r.strip() for r in requirements if r.strip()]
        requirements_json = json.dumps(requirements)
        
        query = """UPDATE jobs 
                   SET company_id=%s, job_title=%s, job_type=%s, 
                       salary_min=%s, salary_max=%s, job_url=%s, 
                       date_posted=%s, requirements=%s 
                   WHERE job_id=%s"""
        values = (
            request.form['company_id'],
            request.form['job_title'],
            request.form['job_type'],
            request.form.get('salary_min') or None,
            request.form.get('salary_max') or None,
            request.form.get('job_url', ''),
            request.form.get('date_posted') or None,
            requirements_json,
            job_id
        )
        cursor.execute(query, values)
        conn.commit()
        flash('Job updated successfully!', 'success')  # Fixed: changed Flask to flash
        cursor.close()
        conn.close()
        return redirect(url_for('list_jobs'))
    
    # GET request - show form with existing data
    cursor.execute("SELECT * FROM jobs WHERE job_id = %s", (job_id,))
    job = cursor.fetchone()
    
    # Get companies for dropdown
    cursor.execute("SELECT company_id, company_name FROM companies ORDER BY company_name")
    companies = cursor.fetchall()
    
    # Parse requirements JSON
    if job and job['requirements']:
        try:
            job['requirements_list'] = json.loads(job['requirements'])
        except:
            job['requirements_list'] = []
    
    cursor.close()
    conn.close()
    
    if not job:
        flash('Job not found!', 'error')  # Fixed: changed Flask to flash
        return redirect(url_for('list_jobs'))
    
    return render_template('job_form.html', companies=companies, job=job)

@app.route('/jobs/delete/<int:job_id>')
def delete_job(job_id):
    """Delete a job"""
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM jobs WHERE job_id = %s", (job_id,))
        conn.commit()
        flash('Job deleted successfully!', 'success')  # Fixed: changed Flask to flash
    except Exception as e:
        flash(f'Error deleting job: {str(e)}', 'error')  # Fixed: changed Flask to flash
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('list_jobs'))

# ==================== APPLICATIONS CRUD ====================

@app.route('/applications')
def list_applications():
    """List all applications"""
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.*, j.job_title, c.company_name 
        FROM applications a
        JOIN jobs j ON a.job_id = j.job_id
        JOIN companies c ON j.company_id = c.company_id
        ORDER BY a.application_date DESC
    """)
    applications = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('applications.html', applications=applications)

@app.route('/applications/add', methods=['GET', 'POST'])
def add_application():
    """Add a new application"""
    if request.method == 'POST':
        # Handle interview data JSON
        interview_data = request.form.get('interview_data', '')
        if not interview_data:
            interview_data = '{}'
        
        conn = get_db()
        cursor = conn.cursor()
        query = """INSERT INTO applications 
                   (job_id, application_date, status, resume_version, 
                    cover_letter_sent, interview_data) 
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        values = (
            request.form['job_id'],
            request.form['application_date'],
            request.form['status'],
            request.form.get('resume_version', ''),
            True if request.form.get('cover_letter_sent') else False,
            interview_data
        )
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
        flash('Application added successfully!', 'success')  # Fixed: changed Flask to flash
        return redirect(url_for('list_applications'))
    
    # GET request - show form with jobs dropdown
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT j.job_id, j.job_title, c.company_name 
        FROM jobs j
        JOIN companies c ON j.company_id = c.company_id
        ORDER BY c.company_name, j.job_title
    """)
    jobs = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('application_form.html', jobs=jobs, application=None)

@app.route('/applications/edit/<int:application_id>', methods=['GET', 'POST'])
def edit_application(application_id):
    """Edit an application"""
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        interview_data = request.form.get('interview_data', '{}')
        
        query = """UPDATE applications 
                   SET job_id=%s, application_date=%s, status=%s, 
                       resume_version=%s, cover_letter_sent=%s, interview_data=%s 
                   WHERE application_id=%s"""
        values = (
            request.form['job_id'],
            request.form['application_date'],
            request.form['status'],
            request.form.get('resume_version', ''),
            True if request.form.get('cover_letter_sent') else False,
            interview_data,
            application_id
        )
        cursor.execute(query, values)
        conn.commit()
        flash('Application updated successfully!', 'success')  # Fixed: changed Flask to flash
        cursor.close()
        conn.close()
        return redirect(url_for('list_applications'))
    
    # GET request - show form with existing data
    cursor.execute("SELECT * FROM applications WHERE application_id = %s", (application_id,))
    application = cursor.fetchone()
    
    cursor.execute("""
        SELECT j.job_id, j.job_title, c.company_name 
        FROM jobs j
        JOIN companies c ON j.company_id = c.company_id
        ORDER BY c.company_name, j.job_title
    """)
    jobs = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    if not application:
        flash('Application not found!', 'error')  # Fixed: changed Flask to flash
        return redirect(url_for('list_applications'))
    
    return render_template('application_form.html', jobs=jobs, application=application)

@app.route('/applications/delete/<int:application_id>')
def delete_application(application_id):
    """Delete an application"""
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM applications WHERE application_id = %s", (application_id,))
        conn.commit()
        flash('Application deleted successfully!', 'success')  # Fixed: changed Flask to flash
    except Exception as e:
        flash(f'Error deleting application: {str(e)}', 'error')  # Fixed: changed Flask to flash
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('list_applications'))

# ==================== CONTACTS CRUD ====================

@app.route('/contacts')
def list_contacts():
    """List all contacts"""
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT ct.*, c.company_name 
        FROM contacts ct
        JOIN companies c ON ct.company_id = c.company_id
        ORDER BY ct.last_name, ct.first_name
    """)
    contacts = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('contacts.html', contacts=contacts)

@app.route('/contacts/add', methods=['GET', 'POST'])
def add_contact():
    """Add a new contact"""
    if request.method == 'POST':
        conn = get_db()
        cursor = conn.cursor()
        query = """INSERT INTO contacts 
                   (company_id, first_name, last_name, job_title, email, phone, linkedin_url, notes) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (
            request.form['company_id'],
            request.form['first_name'],
            request.form['last_name'],
            request.form.get('job_title', ''),
            request.form.get('email', ''),
            request.form.get('phone', ''),
            request.form.get('linkedin_url', ''),
            request.form.get('notes', '')
        )
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
        flash('Contact added successfully!', 'success')  # Fixed: changed Flask to flash
        return redirect(url_for('list_contacts'))
    
    # GET request - show form with companies dropdown
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT company_id, company_name FROM companies ORDER BY company_name")
    companies = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('contact_form.html', companies=companies, contact=None)

@app.route('/contacts/edit/<int:contact_id>', methods=['GET', 'POST'])
def edit_contact(contact_id):
    """Edit a contact"""
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        query = """UPDATE contacts 
                   SET company_id=%s, first_name=%s, last_name=%s, job_title=%s, 
                       email=%s, phone=%s, linkedin_url=%s, notes=%s 
                   WHERE contact_id=%s"""
        values = (
            request.form['company_id'],
            request.form['first_name'],
            request.form['last_name'],
            request.form.get('job_title', ''),
            request.form.get('email', ''),
            request.form.get('phone', ''),
            request.form.get('linkedin_url', ''),
            request.form.get('notes', ''),
            contact_id
        )
        cursor.execute(query, values)
        conn.commit()
        flash('Contact updated successfully!', 'success')  # Fixed: changed Flask to flash
        cursor.close()
        conn.close()
        return redirect(url_for('list_contacts'))
    
    # GET request - show form with existing data
    cursor.execute("SELECT * FROM contacts WHERE contact_id = %s", (contact_id,))
    contact = cursor.fetchone()
    
    cursor.execute("SELECT company_id, company_name FROM companies ORDER BY company_name")
    companies = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    if not contact:
        flash('Contact not found!', 'error')  # Fixed: changed Flash to flash (lowercase)
        return redirect(url_for('list_contacts'))
    
    return render_template('contact_form.html', companies=companies, contact=contact)

@app.route('/contacts/delete/<int:contact_id>')
def delete_contact(contact_id):
    """Delete a contact"""
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM contacts WHERE contact_id = %s", (contact_id,))
        conn.commit()
        flash('Contact deleted successfully!', 'success')  # Fixed: changed Flask to flash
    except Exception as e:
        flash(f'Error deleting contact: {str(e)}', 'error')  # Fixed: changed Flask to flash
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('list_contacts'))

# ==================== JOB MATCH FEATURE ====================

@app.route('/job-match', methods=['GET', 'POST'])
def job_match():
    """Job matching feature - ranks jobs by skill match percentage"""
    matches = []
    user_skills = []
    
    if request.method == 'POST':
        # Get and clean user skills
        skills_text = request.form.get('skills', '')
        # Split by commas, strip whitespace, filter out empty strings
        user_skills = [s.strip() for s in skills_text.split(',') if s.strip()]
        
        if user_skills:
            # Get all jobs with requirements
            conn = get_db()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT j.job_id, j.job_title, j.requirements, c.company_name 
                FROM jobs j
                JOIN companies c ON j.company_id = c.company_id
                WHERE j.requirements IS NOT NULL 
                AND j.requirements != '[]'
                AND j.requirements != ''
            """)
            jobs = cursor.fetchall()
            cursor.close()
            conn.close()
            
            for job in jobs:
                try:
                    # Parse job requirements from JSON
                    if job['requirements']:
                        # Handle both string and already-parsed JSON
                        if isinstance(job['requirements'], str):
                            job_requirements = json.loads(job['requirements'])
                        else:
                            job_requirements = job['requirements']
                        
                        # Ensure it's a list
                        if isinstance(job_requirements, list) and job_requirements:
                            # Convert to lowercase for case-insensitive matching
                            user_set = set(s.lower() for s in user_skills)
                            job_set = set(s.lower() for s in job_requirements)
                            
                            # Calculate match
                            matched_skills = user_set & job_set
                            match_percentage = round((len(matched_skills) / len(job_set)) * 100)
                            
                            # Only include jobs with at least some match
                            if match_percentage > 0:
                                matches.append({
                                    'job_id': job['job_id'],
                                    'job_title': job['job_title'],
                                    'company_name': job['company_name'],
                                    'match_percentage': match_percentage,
                                    'matched_skills': list(matched_skills),
                                    'missing_skills': list(job_set - user_set),
                                    'total_skills': len(job_set)
                                })
                except (json.JSONDecodeError, TypeError) as e:
                    print(f"Error parsing requirements for job {job.get('job_id')}: {e}")
                    continue
            
            # Sort by match percentage (highest first)
            matches.sort(key=lambda x: x['match_percentage'], reverse=True)
    
    # Convert user_skills back to comma-separated string for the form
    user_skills_str = ', '.join(user_skills) if user_skills else ''
    
    return render_template('job_match.html', matches=matches, user_skills=user_skills_str)

if __name__ == '__main__':
    app.run(debug=True)