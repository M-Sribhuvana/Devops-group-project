# Step 6: Deployment Guide (Backend on Render & Frontend on Vercel)

This guide walks you through deploying your full-stack **Fruit Doctor AI** application to production as defined in Step 6 of the project architecture.

---

## 1. Deploy FastAPI Backend to Render

1. Create a free account at [Render.com](https://render.com).
2. Push your project to GitHub.
3. On Render Dashboard:
   - Click **New +** -> **Web Service**.
   - Connect your GitHub repository.
   - Set **Root Directory**: `backend`
   - Set **Runtime**: `Python 3`
   - Set **Build Command**: `pip install -r requirements.txt`
   - Set **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Under **Environment Variables**:
   - Add `GEMINI_API_KEY`: *(Your Google Gemini API Key)*
5. Click **Create Web Service**. Render will deploy your API and provide a live URL (e.g. `https://fruit-doctor-ai-backend.onrender.com`).

---

## 2. Deploy React Frontend to Vercel

1. Create a free account at [Vercel.com](https://vercel.com).
2. Click **Add New** -> **Project** and import your GitHub repository.
3. Configure project settings:
   - **Framework Preset**: `Vite`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
4. Update `frontend/vercel.json` rewrite URL to point to your live Render backend URL:
   ```json
   {
     "rewrites": [
       {
         "source": "/api/:path*",
         "destination": "https://YOUR-RENDER-BACKEND.onrender.com/api/:path*"
       }
     ]
   }
   ```
5. Click **Deploy**. Vercel will build and host your responsive web application on a fast global CDN!
