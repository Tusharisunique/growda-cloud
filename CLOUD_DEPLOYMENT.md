# Growda Cloud Deployment Guide

## Overview
Deploy your pneumonia detection app with the trained global model to the cloud. The frontend will communicate with the cloud backend for predictions.

## Backend Deployment (FastAPI + TensorFlow)

### Files to Upload
1. `backend/global_model.keras` (19MB - your trained model)
2. `backend/main.py` (FastAPI server)
3. `backend/model.py` (model utilities)
4. `backend/requirements.txt` (Python dependencies)

### Deployment Steps

#### Option 1: PythonAnywhere
1. Create a new PythonAnywhere account
2. Go to "Web" tab → "Add a new web app"
3. Choose "Manual Configuration" → "Python 3.10"
4. Upload the backend files to your home directory
5. In the web app configuration:
   - Set working directory: `/home/yourusername/backend/`
   - Set WSGI file: `main.py`
   - Add virtualenv and install requirements
6. Start the web app

#### Option 2: Railway/Render
1. Create `Procfile` in backend directory:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

2. Create `runtime.txt`:
```
python-3.10
```

3. Upload files to Railway/Render
4. Set environment variables if needed

#### Option 3: DigitalOcean App Platform
1. Create new app
2. Upload backend files
3. Set build command: `pip install -r requirements.txt`
4. Set run command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Deploy

### Backend Endpoints Available
- `GET /` - API info
- `GET /status` - Training status (static)
- `GET /metrics/history` - Training history (static)
- `POST /predict` - Image prediction
- `GET /model/info` - Model information
- `GET /health` - Health check

## Frontend Deployment (React)

### Files to Upload
Entire `frontend/` directory

### Configuration Update
Update `frontend/.env` file:
```
VITE_API_BASE_URL=https://your-backend-url.com
```

### Deployment Steps

#### Option 1: Vercel/Netlify
1. Install Node.js dependencies: `npm install`
2. Build: `npm run build`
3. Upload `dist/` folder to Vercel/Netlify
4. Set environment variable: `VITE_API_BASE_URL=https://your-backend-url.com`

#### Option 2: GitHub Pages
1. Update `vite.config.js` for GitHub Pages
2. Build and deploy to GitHub Pages
3. Set environment variables in deployment settings

#### Option 3: Railway/Render
1. Connect GitHub repository
2. Set build command: `npm install && npm run build`
3. Set output directory: `dist`
4. Deploy

## Testing Cloud Deployment

1. **Backend Test**: Visit `https://your-backend-url.com/health`
2. **Frontend Test**: Visit `https://your-frontend-url.com`
3. **Integration Test**: Upload an image and verify prediction works

## Important Notes

- The backend uses **static mode** - no federated learning in cloud
- Model is pre-trained and loaded from `global_model.keras`
- CORS is enabled for all origins (`allow_origins=["*"]`)
- Frontend will show training history as read-only data
- All functionality remains identical to local version

## File Structure After Upload

```
cloud-backend/
├── global_model.keras
├── main.py
├── model.py
└── requirements.txt

cloud-frontend/
├── dist/ (built files)
├── src/
├── package.json
└── .env (updated with cloud URL)
```

Your app will work exactly the same as locally, but hosted on the cloud!
