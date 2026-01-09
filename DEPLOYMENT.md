# Deployment Guide - Phase II

## Prerequisites

- GitHub account
- Render.com account (for backend)
- Vercel account (for frontend)
- Neon database already created

---

## Part 1: Deploy Backend to Render.com

### Step 1: Prepare Backend for Production

1. **Update `main.py`** - Add production-ready CORS:
```python
from fastapi.middleware.cors import CORSMiddleware
import os

# Get CORS origins from environment variable
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

2. **Ensure `requirements.txt` is complete** (already provided above)

### Step 2: Deploy on Render.com

1. **Go to**: https://render.com
2. **Sign in** with GitHub
3. **Click**: "New +" → "Web Service"
4. **Connect** your GitHub repository: `salmansalim1/hackathon-todo`
5. **Configure**:
   - Name: `hackathon-todo-backend`
   - Region: Choose closest to you
   - Branch: `main`
   - Root Directory: `phase2/backend`
   - Runtime: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. **Add Environment Variables**:
   - `DATABASE_URL`: Your Neon connection string
   - `SECRET_KEY`: Generate with: `openssl rand -hex 32`
   - `CORS_ORIGINS`: `https://your-frontend-url.vercel.app` (update after frontend deployment)
7. **Click**: "Create Web Service"

**Wait 5-10 minutes** for deployment to complete.

### Step 3: Test Backend
```bash
# Replace with your Render URL
curl https://hackathon-todo-backend.onrender.com/
```

Should return: `{"message":"Todo API is running"}`

---

## Part 2: Deploy Frontend to Vercel

### Step 1: Prepare Frontend for Production

Update **`lib/api.ts`** with production backend URL:
```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
```

### Step 2: Deploy on Vercel

1. **Go to**: https://vercel.com
2. **Sign in** with GitHub
3. **Click**: "Add New" → "Project"
4. **Import** your repository: `salmansalim1/hackathon-todo`
5. **Configure**:
   - Framework Preset: `Next.js`
   - Root Directory: `phase2/frontend`
6. **Add Environment Variables**:
   - `NEXT_PUBLIC_API_URL`: `https://hackathon-todo-backend.onrender.com`
   - `BETTER_AUTH_SECRET`: Generate with: `openssl rand -hex 32`
   - `BETTER_AUTH_URL`: (Will be provided after first deployment)
   - `DATABASE_URL`: Your Neon connection string
7. **Click**: "Deploy"

### Step 3: Update Environment Variables

After first deployment:

1. Copy your Vercel URL (e.g., `https://hackathon-todo-xyz.vercel.app`)
2. **Go to**: Vercel Dashboard → Your Project → Settings → Environment Variables
3. **Update**: `BETTER_AUTH_URL` with your Vercel URL
4. **Redeploy**: Go to Deployments → Click ⋯ → "Redeploy"

### Step 4: Update Backend CORS

1. Go to Render Dashboard → Your Backend Service → Environment
2. Update `CORS_ORIGINS` to: `https://your-vercel-url.vercel.app`
3. Click "Save Changes" (will auto-redeploy)

---

## Part 3: Verify Deployment

### Test Backend
```bash
curl https://hackathon-todo-backend.onrender.com/api/test
```

### Test Frontend
1. Visit your Vercel URL
2. Sign up for an account
3. Create a task
4. Verify task appears in list

---

## Troubleshooting

### Backend Issues

**Error: Module not found**
- Check `requirements.txt` has all dependencies
- Redeploy on Render

**Error: Database connection failed**
- Verify `DATABASE_URL` in Render environment variables
- Check Neon database is active

### Frontend Issues

**Error: API connection failed**
- Verify `NEXT_PUBLIC_API_URL` points to Render backend
- Check backend CORS includes Vercel URL

**Error: Authentication not working**
- Verify `BETTER_AUTH_SECRET` is set
- Check `DATABASE_URL` is correct

---

## URLs Checklist

After deployment, you should have:

- ✅ Backend URL: `https://hackathon-todo-backend.onrender.com`
- ✅ Frontend URL: `https://hackathon-todo-xyz.vercel.app`
- ✅ GitHub Repo: `https://github.com/salmansalim1/hackathon-todo`

---

## Next Steps

- Create demo video (max 90 seconds)
- Submit via hackathon form
- Prepare for Phase III (AI Chatbot)
