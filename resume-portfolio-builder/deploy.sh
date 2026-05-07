#!/bin/bash

# Deployment script for Vercel
# Usage: ./deploy.sh

echo "🚀 Preparing for Vercel deployment..."

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not found. Initialize with: git init"
    exit 1
fi

# Add all changes
echo "📦 Staging changes..."
git add .

# Commit
echo "💾 Creating commit..."
git commit -m "Deploy to Vercel: $(date '+%Y-%m-%d %H:%M:%S')"

# Push to main branch
echo "🔄 Pushing to GitHub..."
git push origin main

echo "✅ Ready for Vercel deployment!"
echo ""
echo "Next steps:"
echo "1. Go to https://vercel.com"
echo "2. Click 'New Project'"
echo "3. Import your GitHub repository"
echo "4. Set root directory to 'resume-portfolio-builder'"
echo "5. Add environment variables (see DEPLOYMENT.md)"
echo "6. Click 'Deploy'"
echo ""
echo "Your app will be live at: https://your-project-name.vercel.app"
