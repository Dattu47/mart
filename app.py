from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
from supabase import create_client, Client
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# Helper to load .env file manually
def load_dotenv():
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, val = line.split('=', 1)
                    os.environ[key.strip()] = val.strip().strip('"').strip("'")

load_dotenv()

# Get Supabase configuration
def get_supabase_config():
    return {
        'url': os.environ.get('SUPABASE_URL', ''),
        'key': os.environ.get('SUPABASE_KEY', '')
    }

supabase_client = None

def get_supabase_client():
    global supabase_client
    if supabase_client is None:
        config = get_supabase_config()
        if not config['url'] or not config['key']:
            raise ValueError("Supabase URL and API Key are not configured.")
        supabase_client = create_client(config['url'], config['key'])
    return supabase_client


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/submit_visitor', methods=['POST'])
def submit_visitor():
    try:
        gender = request.form['gender']
        age_group = request.form['age_group']
        visit_date = request.form['visit_date']
        comment = request.form.get('comment', '')

        if not all([gender, age_group, visit_date]):
            flash("All fields except comment are required!", "error")
            return redirect(url_for('form'))

        client = get_supabase_client()
        client.table("visitors").insert({
            "gender": gender,
            "age_group": age_group,
            "comment": comment,
            "visit_date": visit_date
        }).execute()

        flash("Visitor data recorded successfully!", "success")
        return redirect(url_for('dashboard'))

    except Exception as e:
        flash(f"Database Error: {str(e)}", "error")
        return redirect(url_for('form'))

@app.route('/dashboard')
def dashboard():
    try:
        client = get_supabase_client()
        response = client.table("visitors").select("*").order("visit_date", desc=True).order("created_at", desc=True).execute()
        raw_visitors = response.data if response.data else []

        # Convert list of dicts to list of tuples to keep template compatibility
        visitors = []
        for v in raw_visitors:
            # In PostgreSQL/Supabase, created_at is returned as ISO-8601 string. 
            # We can format it to be more readable in the table, e.g. YYYY-MM-DD HH:MM
            created_at_raw = v.get('created_at', '')
            created_at_str = created_at_raw
            if created_at_raw and 'T' in created_at_raw:
                try:
                    # '2026-06-07T10:00:00+00:00' -> '2026-06-07 10:00'
                    dt = datetime.fromisoformat(created_at_raw.replace('Z', '+00:00'))
                    created_at_str = dt.strftime('%Y-%m-%d %H:%M')
                except Exception:
                    pass
            visitors.append((
                v.get('id'),
                v.get('gender'),
                v.get('age_group'),
                v.get('comment'),
                v.get('visit_date'),
                created_at_str
            ))

        # Compute stats in Python
        total_visits = len(raw_visitors)
        
        today_str = datetime.today().strftime('%Y-%m-%d')
        today_visits = sum(1 for v in raw_visitors if v.get('visit_date') == today_str)
        
        male_visits = sum(1 for v in raw_visitors if v.get('gender') == 'Male')
        female_visits = sum(1 for v in raw_visitors if v.get('gender') == 'Female')

        # Gender stats
        gender_counts = {}
        for v in raw_visitors:
            g = v.get('gender')
            if g:
                gender_counts[g] = gender_counts.get(g, 0) + 1
        gender_stats = list(gender_counts.items())

        # Age stats
        age_counts = {}
        for v in raw_visitors:
            a = v.get('age_group')
            if a:
                age_counts[a] = age_counts.get(a, 0) + 1
        age_stats = list(age_counts.items())

        # Date stats
        date_counts = {}
        for v in raw_visitors:
            d = v.get('visit_date')
            if d:
                date_counts[d] = date_counts.get(d, 0) + 1
        date_stats = sorted(list(date_counts.items()), key=lambda x: x[0])

        return render_template("dashboard.html",
                               visitors=visitors,
                               total_visits=total_visits,
                               today_visits=today_visits,
                               male_visits=male_visits,
                               female_visits=female_visits,
                               gender_stats=gender_stats,
                               age_stats=age_stats,
                               date_stats=date_stats)
    except Exception as e:
        flash(f"Database Error: {str(e)}", "error")
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

