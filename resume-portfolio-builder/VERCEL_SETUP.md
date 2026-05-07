# Vercel Deployment Setup - Complete Guide

## ✅ Files Created for Deployment

1. **vercel.json** - Vercel configuration
2. **wsgi.py** - WSGI entry point
3. **.gitignore** - Git ignore rules
4. **DEPLOYMENT.md** - Detailed deployment guide
5. **deploy.sh** - Automated deployment script

## 🚀 Quick Start (3 Steps)

### Step 1: Commit and Push
```bash
cd resume-portfolio-builder
git add .
git commit -m "Add Vercel deployment configuration"
git push origin main
```

### Step 2: Connect to Vercel
1. Visit https://vercel.com
2. Sign in with GitHub
3. Click "New Project"
4. Select your repository
5. Set **Root Directory** to `resume-portfolio-builder`
6. Click "Deploy"

### Step 3: Configure Environment Variables
In Vercel Dashboard:
1. Go to Settings → Environment Variables
2. Add:
   - `FLASK_ENV` = `production`
   - `SECRET_KEY` = (generate with: `python -c "import secrets; print(secrets.token_hex(32))"`)

## 📊 Your Deployment Info

**Framework**: Flask (Python)
**Database**: SQLite (local - ⚠️ not persistent on Vercel)
**Build Time**: ~30 seconds
**Deployment URL**: `https://your-project-name.vercel.app`

## ⚠️ Important: Database Persistence

**Current Issue**: SQLite database won't persist between deployments on Vercel

**Solutions**:

### Option 1: Use Vercel KV (Redis) - Quick Fix
```bash
vercel env add KV_URL
```

### Option 2: Migrate to PostgreSQL - Recommended
1. Create free Supabase account: https://supabase.com
2. Create PostgreSQL database
3. Update `database.py` to use PostgreSQL
4. Add `DATABASE_URL` to Vercel environment variables

### Option 3: Use MongoDB Atlas - Alternative
1. Create free MongoDB account: https://mongodb.com/cloud/atlas
2. Create cluster and database
3. Update `database.py` to use MongoDB
4. Add `MONGODB_URI` to Vercel environment variables

## 📝 Environment Variables Needed

```
FLASK_ENV=production
SECRET_KEY=your-generated-secret-key
DATABASE_URL=your-database-url (if using PostgreSQL)
MONGODB_URI=your-mongodb-url (if using MongoDB)
```

## 🔗 Your Live App

After deployment, your app will be available at:
```
https://your-project-name.vercel.app
```

## 📞 Support

- Vercel Docs: https://vercel.com/docs
- Flask Docs: https://flask.palletsprojects.com
- Supabase Docs: https://supabase.com/docs

## ✨ Features Deployed

✅ User Registration & Login
✅ Resume Builder with 3 Templates
✅ Digital Portfolio
✅ PDF Download
✅ Responsive Design
✅ Teal Blue Color Scheme

---

**Status**: Ready for deployment! 🎉
