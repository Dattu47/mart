# Mart - Visitor Logging & Analytics Dashboard

A modern, responsive web application built using **Flask** and **Supabase (PostgreSQL)** to record, monitor, and analyze visitor demographics and traffic patterns.

---

## 🚀 Features

- **Home Page**: Clean, premium welcoming interface for visitors and store administrators.
- **Visitor Entry Form**: An interactive form to record visitor details including gender, age group, visit date, and optional comments.
- **Interactive Dashboard**:
  - Real-time stats cards (Total Visits, Today's Visits, Gender breakdown).
  - List of all visitors sorted chronologically.
  - Analytics visual representations for visitor gender, age groups, and daily visit trends.
- **Database Backend**: Fully powered by Supabase PostgreSQL database for persistent, secure, and fast data management.

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **Database**: Supabase (PostgreSQL)
- **Frontend**: HTML5, Vanilla CSS3 (Custom styling in `static/style.css`), Template inheritance using Jinja2 (`base.html`)
- **Package Management**: Pip (`requirements.txt`)

---

## 📂 Project Structure

```text
mart/
├── static/
│   ├── style.css         # Custom responsive styling and theme
│   └── shopping.png      # Dashboard illustration/assets
├── templates/
│   ├── base.html         # Base template with common navbar/footer
│   ├── index.html        # Welcoming landing page
│   ├── form.html         # Visitor log registration form
│   └── dashboard.html    # Admin analytics dashboard
├── .env                  # Environmental variables (ignored by Git)
├── .gitignore            # Git exclusion rules
├── app.py                # Main Flask application entrypoint
└── requirements.txt      # Python dependencies
```

---

## ⚙️ Configuration & Database Setup

The application uses Supabase to store visitor records. 

### 1. Database Schema
Create a table named `visitors` in your Supabase database with the following columns:

```sql
create table visitors (
  id bigint generated always as identity primary key,
  gender text not null,
  age_group text not null,
  comment text,
  visit_date date not null,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);
```

### 2. Environment Variables
Create a file named `.env` in the root directory (do not commit this file to GitHub) and add your Supabase credentials:

```ini
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-supabase-anon-key
```

---

## 💻 Running Locally

### Prerequisites
- Python 3.8 or higher
- Pip

### Setup Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Dattu47/mart.git
   cd mart
   ```

2. **Create and activate a Virtual Environment** (optional but recommended):
   - **Windows (PowerShell)**:
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   - **macOS/Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```
   The application will start running at `http://127.0.0.1:5000/`.

---

## 📄 License
This project is open-source and available under the MIT License.
