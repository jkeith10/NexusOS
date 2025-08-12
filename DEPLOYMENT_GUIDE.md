# 🚀 Real Estate Nexus OS - Deployment Guide

## **Recommended: Railway Deployment (Easiest)**

### **Step 1: Prepare Your Repository**
1. Push your code to GitHub
2. Make sure all files are committed

### **Step 2: Deploy Backend to Railway**
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway will auto-detect the Python app in `real-estate-api/`
6. Set environment variables:
   ```
   FLASK_ENV=production
   SECRET_KEY=your-secret-key-here
   ```
7. Add PostgreSQL database:
   - Click "New" → "Database" → "PostgreSQL"
   - Railway will auto-connect it
8. Update database URI in your code to use Railway's PostgreSQL

### **Step 3: Deploy Frontends to Vercel**
1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub
3. Import your repository
4. Deploy `client-portal/`:
   - Set root directory to `client-portal`
   - Framework preset: Vite
   - Build command: `npm run build`
   - Output directory: `dist`
5. Deploy `transaction-dashboard/`:
   - Set root directory to `transaction-dashboard`
   - Framework preset: Vite
   - Build command: `npm run build`
   - Output directory: `dist`

### **Step 4: Connect Frontend to Backend**
1. Get your Railway backend URL (e.g., `https://your-app.railway.app`)
2. Update the Vercel config files:
   - Replace `https://your-backend-url.railway.app` with your actual Railway URL
3. Redeploy the frontend apps

---

## **Alternative: Render Deployment**

### **Step 1: Deploy Backend to Render**
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New" → "Web Service"
4. Connect your GitHub repo
5. Configure:
   - **Name**: `nexus-os-backend`
   - **Root Directory**: `real-estate-api`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python src/main.py`
6. Add PostgreSQL database:
   - Click "New" → "PostgreSQL"
   - Connect it to your web service

### **Step 2: Deploy Frontends to Render**
1. For each React app (`client-portal`, `transaction-dashboard`):
   - Click "New" → "Static Site"
   - Connect your GitHub repo
   - Configure:
     - **Name**: `nexus-os-client-portal` (or dashboard)
     - **Root Directory**: `client-portal` (or `transaction-dashboard`)
     - **Build Command**: `npm install && npm run build`
     - **Publish Directory**: `dist`

---

## **Alternative: DigitalOcean App Platform**

### **Step 1: Deploy Backend**
1. Go to [digitalocean.com](https://digitalocean.com)
2. Navigate to App Platform
3. Click "Create App" → "Source: GitHub"
4. Select your repository
5. Configure:
   - **Source Directory**: `real-estate-api`
   - **Type**: Web Service
   - **Build Command**: `pip install -r requirements.txt`
   - **Run Command**: `python src/main.py`
6. Add PostgreSQL database from the same interface

### **Step 2: Deploy Frontends**
1. Create separate apps for each React frontend
2. Configure as Static Sites
3. Set build commands and output directories

---

## **Environment Variables**

### **Backend Environment Variables**
```
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
DATABASE_URL=your-database-url
SENDGRID_API_KEY=your-sendgrid-key
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
```

### **Frontend Environment Variables**
```
VITE_API_URL=https://your-backend-url.com/api
VITE_APP_NAME=Real Estate Nexus OS
```

---

## **Database Migration**

### **For Production Database**
1. Update the database URI in your Flask app to use the production database
2. Run database migrations:
   ```python
   with app.app_context():
       db.create_all()
   ```
3. Seed initial data if needed

---

## **Custom Domain Setup**

### **Railway + Vercel**
1. Add custom domain in Railway for backend
2. Add custom domain in Vercel for frontends
3. Update DNS records
4. Update API URLs in frontend configs

### **SSL Certificates**
- Railway: Automatic
- Vercel: Automatic
- Render: Automatic
- DigitalOcean: Automatic

---

## **Monitoring & Maintenance**

### **Health Checks**
- Backend: `/` endpoint
- Frontend: Static file serving

### **Logs**
- Railway: Built-in logging
- Vercel: Function logs
- Render: Service logs
- DigitalOcean: App logs

### **Scaling**
- Railway: Auto-scaling available
- Vercel: Automatic
- Render: Manual scaling
- DigitalOcean: Auto-scaling available

---

## **Cost Estimates**

### **Railway**
- Backend: $5-20/month
- Database: $5-20/month
- **Total**: $10-40/month

### **Vercel**
- Frontends: Free tier available
- **Total**: $0-20/month

### **Render**
- Backend: $7/month
- Database: $7/month
- Frontends: Free tier available
- **Total**: $14-28/month

### **DigitalOcean**
- Backend: $5-12/month
- Database: $15/month
- Frontends: $5/month each
- **Total**: $30-50/month

---

## **Troubleshooting**

### **Common Issues**
1. **CORS errors**: Ensure backend allows frontend domains
2. **Database connection**: Check DATABASE_URL environment variable
3. **Build failures**: Check Node.js/Python versions
4. **API 404s**: Verify API routes and proxy configuration

### **Support**
- Railway: [docs.railway.app](https://docs.railway.app)
- Vercel: [vercel.com/docs](https://vercel.com/docs)
- Render: [render.com/docs](https://render.com/docs)
- DigitalOcean: [docs.digitalocean.com](https://docs.digitalocean.com)

---

**🎉 Your Real Estate Nexus OS will be live and ready for clients!**
