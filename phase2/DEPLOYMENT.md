# Deployment Guide - Phase II

## Backend Deployment (Render.com)

### Step 1: Prepare Backend for Deployment

1. **Create `render.yaml` in backend folder:**
```yaml
services:
  - type: web
    name: hackathon-todo-backend
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DATABASE_URL
        sync: false
      - key: BETTER_AUTH_SECRET
        sync: false
      - key: BETTER_AUTH_URL
        sync: false
      - key: CORS_ORIGINS
        sync: false
      - key: PYTHON_VERSION
        value: 3.11.0
```

2. **Update `requirements.txt` to include all dependencies:**
```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlmodel==0.0.14
psycopg2-binary==2.9.9
python-dotenv==1.0.0
pydantic==2.5.3
python-multipart==0.0.6
pyjwt==2.8.0
passlib[bcrypt]==1.7.4
python-jose[cryptography]==3.3.0
```

### Step 2: Deploy on Render.com

1. Go to https://render.com and sign up/login
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name:** hackathon-todo-backend
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type:** Free

5. Add Environment Variables:
   - `DATABASE_URL`: Your Neon connection string
   - `BETTER_AUTH_SECRET`: Generate 32+ character secret
   - `BETTER_AUTH_URL`: Will add after frontend deployment
   - `CORS_ORIGINS`: Will add after frontend deployment

6. Click "Create Web Service"

7. **Copy the deployment URL** (e.g., `https://hackathon-todo-backend.onrender.com`)

### Common Render Issues & Fixes

**Issue 1: "Module not found"**
```bash
# Fix: Ensure all imports are in requirements.txt
pip freeze > requirements.txt
```

**Issue 2: "Port binding error"**
```python
# Fix: Update main.py to use PORT env variable
import os
port = int(os.getenv("PORT", 8000))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=port)
```

**Issue 3: "Database connection timeout"**
```python
# Fix: Add connection pooling in models.py
from sqlmodel import create_engine

engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10
)
```

## Frontend Deployment (Vercel)

### Step 1: Prepare Frontend

1. **Update `next.config.js`:**
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  },
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
}

module.exports = nextConfig
```

2. **Create `vercel.json` in frontend folder:**
```json
{
  "buildCommand": "npm run build",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "nextjs",
  "env": {
    "NEXT_PUBLIC_API_URL": "@next_public_api_url",
    "BETTER_AUTH_SECRET": "@better_auth_secret",
    "BETTER_AUTH_URL": "@better_auth_url",
    "DATABASE_URL": "@database_url"
  }
}
```

### Step 2: Deploy on Vercel

1. Go to https://vercel.com and sign up/login
2. Click "Add New" → "Project"
3. Import your GitHub repository
4. Configure:
   - **Framework Preset:** Next.js
   - **Root Directory:** frontend
   - **Build Command:** `npm run build`
   - **Install Command:** `npm install`

5. Add Environment Variables:
   - `NEXT_PUBLIC_API_URL`: Your Render backend URL
   - `BETTER_AUTH_SECRET`: Same as backend
   - `BETTER_AUTH_URL`: Will be auto-set to Vercel URL
   - `DATABASE_URL`: Your Neon connection string

6. Click "Deploy"

7. **Copy the deployment URL** (e.g., `https://hackathon-todo.vercel.app`)

### Step 3: Update CORS

Go back to Render.com and update environment variables:
- `BETTER_AUTH_URL`: Your Vercel URL
- `CORS_ORIGINS`: Your Vercel URL

Redeploy backend on Render.

## Verification Checklist

- [ ] Backend deployed and accessible
- [ ] Frontend deployed and accessible
- [ ] Authentication works (signup/signin)
- [ ] Tasks CRUD operations work
- [ ] CORS configured correctly
- [ ] Environment variables set
- [ ] GitHub repository updated

## Troubleshooting

### Backend Not Responding
1. Check Render logs
2. Verify DATABASE_URL is correct
3. Check if service is running

### Frontend API Errors
1. Verify NEXT_PUBLIC_API_URL in Vercel
2. Check CORS settings in backend
3. Inspect browser console for errors

### Authentication Fails
1. Ensure BETTER_AUTH_SECRET matches on both
2. Verify DATABASE_URL is accessible
3. Check Better Auth configuration
