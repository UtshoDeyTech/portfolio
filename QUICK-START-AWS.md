# 🚀 Quick Start - AWS EC2 Deployment

Deploy your portfolio in 5 minutes!

## Step 1: Launch EC2 Instance

1. **Go to AWS Console** → EC2 → Launch Instance
2. **Choose**: Ubuntu Server 22.04 LTS (Free tier eligible)
3. **Instance Type**: t2.medium (recommended) or t2.micro (minimal)
4. **Create Key Pair**: Download `.pem` file (save it safely!)
5. **Security Group** - Add these rules:
   ```
   SSH      (22)   → Your IP
   HTTP     (80)   → 0.0.0.0/0
   HTTPS    (443)  → 0.0.0.0/0
   ```
6. **Storage**: 20 GB minimum
7. Click **Launch Instance**

## Step 2: Connect to Your Server

```bash
# On your local machine (Windows PowerShell/Git Bash)

# Make key secure (Linux/Mac)
chmod 400 your-key.pem

# Connect via SSH
ssh -i your-key.pem ubuntu@YOUR-EC2-PUBLIC-IP
```

Replace `YOUR-EC2-PUBLIC-IP` with the IP shown in AWS Console.

## Step 3: Clone & Deploy

```bash
# Once connected to EC2, run these commands:

# Install git
sudo apt update && sudo apt install -y git

# Clone repository
git clone YOUR-REPO-URL
cd portfolio

# Make script executable
chmod +x deploy-aws.sh

# Run deployment (this does EVERYTHING!)
sudo bash deploy-aws.sh
```

## Step 4: Follow the Prompts

The script will ask you:

1. **"Do you have a custom domain?"**
   - Type `n` if using IP address
   - Type `y` if you have a domain (e.g., `myportfolio.com`)

2. **"Create Django superuser?"**
   - Type `y` to create admin account
   - Enter username, email, password

## Step 5: Access Your Site! 🎉

- **Website**: `http://YOUR-EC2-PUBLIC-IP`
- **Admin**: `http://YOUR-EC2-PUBLIC-IP/admin`

That's it! Your portfolio is LIVE! 🚀

---

## 🆘 Troubleshooting

### Can't access website?

**Check Security Group**:
1. Go to EC2 Console
2. Select your instance
3. Click "Security" tab
4. Verify ports 80 and 443 are open to `0.0.0.0/0`

### See error page?

```bash
# Check logs
docker-compose logs -f
```

### Need to restart?

```bash
cd ~/portfolio
docker-compose restart
```

---

## 📝 Next Steps

### Add Your Content

1. Go to admin panel: `http://YOUR-IP/admin`
2. Login with superuser credentials
3. Add your projects, blogs, experience

### Set Up Custom Domain (Optional)

1. **Point domain to EC2**:
   - Go to your domain registrar
   - Add A Record: `@ → YOUR-EC2-IP`

2. **Re-run deployment**:
   ```bash
   cd ~/portfolio
   sudo bash deploy-aws.sh
   ```
   - This time answer `y` for custom domain
   - Script will set up SSL automatically!

### Enable HTTPS

If you have a domain, the script sets up SSL automatically!

---

## 🔄 Update Your Site

```bash
# Connect to EC2
ssh -i your-key.pem ubuntu@YOUR-EC2-IP

# Pull latest changes
cd ~/portfolio
git pull

# Restart
docker-compose restart
```

---

## 💾 Backup Database

```bash
# Export from admin panel
# Or run this command:
docker-compose exec backend python manage.py dumpdata > backup.json
```

---

## ✅ That's All!

Your portfolio is now:
- ✅ Live on the internet
- ✅ Running with Docker
- ✅ Served via Nginx
- ✅ Auto-restarts on reboot
- ✅ Ready for your content!

Enjoy! 🎉
