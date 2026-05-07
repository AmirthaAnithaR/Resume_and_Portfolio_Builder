# Deployment Guide - Resume + Portfolio Builder

## Deploying to Vercel

### Prerequisites
1. GitHub account with the repository pushed
2. Vercel account (free at vercel.com)
3. Environment variables configured

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```

### Step 2: Connect to Vercel
1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import your GitHub repository
4. Select the `resume-portfolio-builder` folder as root directory

### Step 3: Configure Environment Variables
In Vercel dashboard, add these environment variables:
- `FLASK_ENV`: `production`
- `SECRET_KEY`: Generate a secure key (use `python -c "import secrets; print(secrets.token_hex(32))"`)

### Step 4: Deploy
Click "Deploy" - Vercel will automatically build and deploy your app

### Important Notes
⚠️ **Database Limitation**: 
- Current setup uses SQLite which doesn't persist on Vercel
- For production, upgrade to PostgreSQL or MongoDB
- Temporary solution: Use Vercel KV (Redis) or Supabase

### Upgrade to PostgreSQL (Recommended)
1. Create a Supabase account (free tier available)
2. Create a PostgreSQL database
3. Update `database.py` to use PostgreSQL instead of SQLite
4. Add database URL to Vercel environment variables

### Your Deployment URL
After deployment, your app will be available at:
`https://your-project-name.vercel.app`

### Troubleshooting
- Check Vercel logs: Dashboard → Project → Deployments → Logs
- Ensure all dependencies are in `requirements.txt`
- Verify `vercel.json` configuration
- Check that templates folder is included in deployment
