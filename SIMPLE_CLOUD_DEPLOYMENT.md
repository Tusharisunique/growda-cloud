# Simple Cloud Deployment - Growda Pneumonia Detection

## Goal
Deploy your trained global model to the cloud so the frontend works exactly the same but hosted online.

## Architecture
```
┌─────────────────┐    ┌─────────────────┐
│   Frontend      │◄──►│  Cloud Backend  │
│   (Vercel)      │    │   (Render)      │
│                 │    │                 │
│ • React UI      │    │ • FastAPI       │
│ • Dashboard     │    │ • Global Model  │
│ • Predictions   │    │ • Static Data   │
└─────────────────┘    └─────────────────┘
```

## Step 1: Update Docker Configuration

### 1.1 Use Simple Dockerfile
```bash
cd backend
cp simple_Dockerfile Dockerfile
```

### 1.2 Update Main Entry Point
```bash
cp simple_cloud_main.py main.py
```

## Step 2: Deploy to Render (Free)

### 2.1 Go to Render.com
1. Open **render.com** → Sign up with GitHub
2. Click **"New +"** → **"Web Service"**
3. Select your **"growda-cloud"** repository

### 2.2 Configure Service
- **Name**: `growda-api`
- **Runtime**: `Docker`
- **Instance Type**: `Free`

### 2.3 Add Environment Variables
```
PYTHONPATH = /app
```

### 2.4 Deploy
Click **"Create Web Service"** and wait 2-3 minutes.

### 2.5 Get Your URL
Your URL will be: `https://growda-api.onrender.com`

## Step 3: Test Cloud Backend

Test these URLs in your browser:
- `https://growda-api.onrender.com/` (API info)
- `https://growda-api.onrender.com/health` (Health check)
- `https://growda-api.onrender.com/status` (Training status)

## Step 4: Update Frontend

### 4.1 Find API Configuration
Look for API configuration in your frontend:
```bash
cd frontend/src
# Find files with localhost or API configuration
grep -r "localhost" . || grep -r "8000" . || grep -r "api" .
```

### 4.2 Update API URL
Replace localhost with your Render URL:
```javascript
// Before
const API_URL = "http://localhost:8000"

// After  
const API_URL = "https://growda-api.onrender.com"
```

### 4.3 Deploy Frontend to Vercel
```bash
cd frontend
npm install -g vercel
vercel --prod
```

## Step 5: Test Everything

### 5.1 Test Cloud API
```bash
curl https://growda-api.onrender.com/status
```

### 5.2 Test Frontend
Open your Vercel URL and test:
- Dashboard shows training history
- Upload X-ray for prediction
- Everything works like localhost

## What Works in Cloud

✅ **Prediction**: Upload X-rays and get predictions  
✅ **Dashboard**: View training history (static)  
✅ **Model Info**: See model details  
✅ **API Endpoints**: All endpoints work  

## What Doesn't Work in Cloud

❌ **Live Training**: No federated learning (static data)  
❌ **Client Connections**: No hospital clients connect  
❌ **Real-time Updates**: Training rounds don't actually run  

## Files Created for Simple Deployment

- `simple_cloud_main.py` - Simplified FastAPI app
- `simple_Dockerfile` - Minimal Docker configuration  
- `SIMPLE_CLOUD_DEPLOYMENT.md` - This guide

## Troubleshooting

### "Model not found" Error
- Ensure `global_model.keras` is in backend directory
- Check file size (~19MB should be present)

### "Connection refused" Error
- Wait for Render deployment to complete
- Check Render logs for errors

### CORS Issues
- Simple cloud API allows all origins
- Should work with any frontend

## Cost

- **Render**: Free tier (sufficient)
- **Vercel**: Free tier (sufficient)
- **Total**: $0/month

## Next Steps

1. Deploy backend to Render
2. Update frontend API URL  
3. Deploy frontend to Vercel
4. Test complete system
5. Share your cloud URLs!

Your website will work exactly the same as localhost, but hosted on the cloud!
