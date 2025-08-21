# 🚀 AI JobChain - Run Application Guide

## 📋 Prerequisites

### Backend Requirements:
- Python 3.8 or higher
- pip (Python package manager)

### Frontend Requirements:
- Node.js 16 or higher
- npm (Node package manager)

## 🎯 Quick Start (Windows)

### Step 1: Setup Backend
```bash
# Navigate to backend directory
cd ai-jobchain-connect-backend

# Run setup script (Windows)
run-backend.bat

# Or manually:
python -m venv .venv
.\.venv\Scripts\Activate
pip install -r requirements.txt
```

### Step 2: Setup Frontend
```bash
# Navigate to frontend directory
cd ai-jobchain-connect

# Run setup script (Windows)
run-frontend.bat

# Or manually:
npm install
```

### Step 3: Start Backend Server
```bash
# In backend directory
cd ai-jobchain-connect-backend
start-server.bat

# Or manually:
.venv\Scripts\activate.bat
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### Step 4: Start Frontend Server
```bash
# In frontend directory (new terminal)
cd ai-jobchain-connect
start-frontend.bat

# Or manually:
npm run dev
```

## 🎯 Quick Start (Mac/Linux)

### Step 1: Setup Backend
```bash
# Navigate to backend directory
cd ai-jobchain-connect-backend

# Make script executable and run
chmod +x run-backend.sh
./run-backend.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-minimal.txt
```

### Step 2: Setup Frontend
```bash
# Navigate to frontend directory
cd ai-jobchain-connect

# Make script executable and run
chmod +x run-frontend.sh
./run-frontend.sh

# Or manually:
npm install
```

### Step 3: Start Backend Server
```bash
# In backend directory
cd ai-jobchain-connect-backend
chmod +x start-server.sh
./start-server.sh

# Or manually:
source venv/bin/activate
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### Step 4: Start Frontend Server
```bash
# In frontend directory (new terminal)
cd ai-jobchain-connect
chmod +x start-frontend.sh
./start-frontend.sh

# Or manually:
npm run dev
```

## 🌐 Access URLs

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **Django Admin**: http://localhost:8000/admin

## 📁 Project Structure

```
ai-jobchain/
├── ai-jobchain-connect/          # Frontend (React + Vite)
│   ├── run-frontend.sh          # Frontend setup (Mac/Linux)
│   ├── run-frontend.bat         # Frontend setup (Windows)
│   ├── start-frontend.sh        # Start frontend server (Mac/Linux)
│   ├── start-frontend.bat       # Start frontend server (Windows)
│   └── src/
│       └── components/
│           └── ProfileSetup/    # Profile setup components
│
└── ai-jobchain-connect-backend/  # Backend (Django)
    ├── run-backend.sh           # Backend setup (Mac/Linux)
    ├── run-backend.bat          # Backend setup (Windows)
    ├── start-server.sh          # Start backend server (Mac/Linux)
    ├── start-server.bat         # Start backend server (Windows)
    ├── requirements-minimal.txt  # Minimal dependencies
    └── backend/
        └── apps/
            └── users/           # User management
```

## 🔧 Manual Commands

### Backend Setup (Manual)
```bash
cd ai-jobchain-connect-backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate.bat
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements-minimal.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Start server
python manage.py runserver
```

### Frontend Setup (Manual)
```bash
cd ai-jobchain-connect

# Install dependencies
npm install

# Start development server
npm run dev
```

## 🛠️ Troubleshooting

### Backend Issues:

#### Virtual Environment Not Found
```bash
# Recreate virtual environment
rm -rf venv  # Mac/Linux
# or
rmdir /s venv  # Windows

python -m venv venv
```

#### Django Not Found
```bash
# Activate virtual environment and reinstall
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate.bat  # Windows

pip install -r requirements-minimal.txt
```

#### Migration Errors
```bash
# Reset database (development only)
rm db.sqlite3  # Mac/Linux
# or
del db.sqlite3  # Windows

python manage.py makemigrations
python manage.py migrate
```

### Frontend Issues:

#### Node Modules Not Found
```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json  # Mac/Linux
# or
rmdir /s node_modules & del package-lock.json  # Windows

npm install
```

#### Port Already in Use
```bash
# Kill process on port 5173
lsof -ti:5173 | xargs kill -9  # Mac/Linux
# or
netstat -ano | findstr :5173  # Windows (then kill PID)
```

## 🎯 Testing the Application

1. **Start both servers** (backend on port 8000, frontend on port 5173)
2. **Open browser** to http://localhost:5173
3. **Test ProfileSetup** by navigating to the profile setup component
4. **Check API endpoints** at http://localhost:8000/api/users/profile/

## 📝 Environment Variables

Create `.env` files if needed:

### Frontend (.env)
```env
VITE_API_BASE_URL=http://localhost:8000/api
VITE_FIREBASE_API_KEY=your_firebase_key
VITE_FIREBASE_AUTH_DOMAIN=your_firebase_domain
VITE_FIREBASE_PROJECT_ID=your_project_id
VITE_FIREBASE_STORAGE_BUCKET=your_storage_bucket
VITE_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
VITE_FIREBASE_APP_ID=your_app_id
VITE_FIREBASE_MEASUREMENT_ID=your_measurement_id
```

### Backend (.env)
```env
DEBUG=True
SECRET_KEY=your_secret_key
ALLOWED_HOSTS=localhost,127.0.0.1
```

## 🚀 Production Deployment

For production, use:
- **Backend**: `requirements.txt` (full dependencies)
- **Frontend**: `npm run build` (production build)
- **Database**: PostgreSQL instead of SQLite
- **Web Server**: Nginx + Gunicorn

---

**🎉 Your AI JobChain application is now ready to run!**
