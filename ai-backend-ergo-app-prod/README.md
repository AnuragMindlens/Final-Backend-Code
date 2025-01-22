# Django Application Documentation for Image Annotation and Posture Analysis

## Contents

1. [Overall Architecture](#overall-architecture)
2. [Flow Chart of Image Processing](#flow-chart-of-image-processing)
3. [Detailed Explanation](#detailed-explanation)
4. [Types of Models Used](#types-of-models-used)
5. [Starting the Server](#starting-the-server)


---

## Overall Architecture

### Models

#### Images Model
The Images model is used to store uploaded images in the database. It contains an image field for the uploaded image and a timestamp field to record when the image was uploaded.

### View Endpoints

1. **GenerateReport**: This endpoint generates a detailed report based on the analysis of uploaded images.
2. **SeatedPosture**: This endpoint analyzes the seated posture from an uploaded image.
3. **HandPosition**: This endpoint analyzes the hand position from an uploaded image.
4. **DeskPosition**: This endpoint analyzes the desk position from an uploaded image.
5. **Annotation**: This endpoint annotates an image with visual indicators based on the analysis.
6. **AnnotateObject**: This endpoint annotates objects within an image using the Mask2Former model.

### Image Processing Modules

1. **bodypose.py**: Contains the PoseAnalyzer class for analyzing body posture.
2. **handpose.py**: Contains the HandPoseAnalyzer class for analyzing hand positions.
3. **deskpose.py**: Contains the DeskPoseAnalyzer class for analyzing desk position.

### URLs Configuration
The urls.py file configures the URL routing for the application. It includes paths for various endpoints like seated posture, hand position, desk position, image annotation, object annotation, and report generation.

## Flow Chart of Image Processing

### Flow Overview

1. **Image Upload**: 
    - The user uploads an image via the appropriate API endpoint (seated posture, hand position, or desk position).
    
2. **Image Preprocessing**: 
    - The uploaded image is preprocessed by resizing, converting to the required format, and adjusting the contrast.

3. **Pose Analysis**: 
    - The image is analyzed using specific analyzers (PoseAnalyzer, HandPoseAnalyzer, DeskPoseAnalyzer) based on the endpoint. 
    - Each analyzer extracts landmarks and calculates relevant angles and positions.

4. **Risk and Recommendation Evaluation**: 
    - Based on the analysis, the system determines the posture's risk level (neutral, positive, or negative). 
    - Recommendations are generated for improving posture.

5. **Annotation (Optional)**: 
    - If required, the system annotates the image with visual indicators of posture analysis. 
    - Annotated images are saved or returned to the user.

6. **Report Generation**: 
    - A comprehensive report is generated that includes the analysis results and recommendations. 
    - The report is formatted and returned to the user as a response.

### Flow Chart

Below is a simplified representation of the flow:

- User Uploads Image
- Preprocess Image
   - Analyze Image with Pose Analyzer
   - Analyze Image with Hand Analyzer
   - Analyze Image with Desk Analyzer
- Evaluate Risk and Generate Recommendations
- Annotate Image if Required
   - Return Annotated Image
- Generate Report
   - Return Report

## Detailed Explanation

### Image Upload

- The user uploads an image through an API endpoint. 
- The endpoints are `/api/images/seatedposture/` for seated posture, `/api/images/handposition/` for hand position, and `/api/images/deskposition/` for desk position.

### Image Preprocessing

- The uploaded image is read and preprocessed. 
- Preprocessing steps include resizing the image, converting the image to the required format, and adjusting the contrast of the image. 
- This ensures the image is in the right condition for analysis.

### Pose Analysis

- The preprocessed image is analyzed using the appropriate analyzer based on the endpoint. 
- For seated posture, the PoseAnalyzer class is used to extract body landmarks and calculate angles related to seated posture. 
- For hand position, the HandPoseAnalyzer class is used to extract hand landmarks and analyze hand positions. 
- For desk position, the DeskPoseAnalyzer class is used to extract body landmarks and analyze desk-related posture.

### Risk and Recommendation Evaluation

- The results of the pose analysis are evaluated to determine the risk level of the posture. 
- The system identifies whether the posture is neutral, positive, or negative. 
- Recommendations are then generated based on the identified risks to help improve the user's posture.

### Annotation (Optional)

- If required, the system annotates the image with visual indicators to highlight key landmarks and angles. 
- The annotated image is either saved or returned to the user.

### Report Generation

- A detailed report is generated that summarizes the analysis results, risk levels, and recommendations. 
- The report is formatted and returned to the user as a response.

## Types of Models Used

### Mask2Former Model
The Mask2Former model is used for universal segmentation of objects within an image. It is a powerful model for instance and semantic segmentation tasks.

### MediaPipe Models

- **Pose Estimation**: The MediaPipe Pose model is used to detect body landmarks for analyzing posture.
- **Hand Tracking**: The MediaPipe Hand model is used to detect hand landmarks for analyzing hand positions.

### TensorFlow Models
TensorFlow models are used for preprocessing images and adjusting image properties.

## Starting the Server

**Prerequisites:**
- Open ports 8000 and 443 on the lightsail instance
- Use Ubuntu 22 version
- - **Note:** If used for local testing follow until the end of database setup

### SSH Key Generation

```
ssh-keygen -t ed25519 -C "<your email here>"
```

- **Issue:** \`nano into generated file and copy key\`
- Paste SSH key into settings/SSH key

### Clone Repository and Install Dependencies

```
git clone git@github.com:Mind-Lens/ai-backend.git
cd ai-backend
sudo apt update && sudo apt upgrade
sudo apt install python3.10-venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
- **Note:** If you encounter "no module named," manually install the missing module.

```
sudo apt-get install -y libgl1-mesa-glx
```

- **Note:** Ensure the git checkout is on \`ergo-app-prod\` branch.

### Database Setup

```
python manage.py makemigrations
rm db.sqlite3
python manage.py migrate
python3 manage.py collectstatic
python manage.py runserver
```

### Nginx Setup

```
sudo apt-get install nginx
sudo nano /etc/nginx/sites-available/your_project_name
```

**Content of \`/etc/nginx/sites-available/your_project_name\`:**

```
server {
  listen 80;
  server_name <ip address or url>;
  client_max_body_size 40M;
  
  location / {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    client_max_body_size 40M;
  }

  location /static/ {
    alias /aibackend/staticfiles/;
  }
}
```

```
sudo ln -s /etc/nginx/sites-available/your_project_name /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
python manage.py runserver
```

### Checkpoint

- If the program runs, Nginx works properly.

### Gunicorn Setup

```
sudo nano /etc/nginx/sites-available/your_project_name
```

**Content of \`/etc/nginx/sites-available/your_project_name\`:**

```
server {
  listen 80;
  server_name <ip address or url>;
  client_max_body_size 40M;
  
  location / {
    proxy_pass http://unix:/run/gunicorn.sock;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
  }

  location /static/ {
    alias /aibackend/staticfiles/;
  }
}
```

```
sudo nginx -t
sudo systemctl restart nginx
sudo nano /etc/systemd/system/gunicorn.service
```

**Content of \`/etc/systemd/system/gunicorn.service\`:**

```
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/ai-backend
ExecStart=/home/ubuntu/ai-backend/venv/bin/gunicorn --workers 3 --bind unix:/run/gunicorn.sock aipose.wsgi:application

[Install]
WantedBy=multi-user.target
```

```
sudo nano /etc/systemd/system/gunicorn.socket
```

**Content of \`/etc/systemd/system/gunicorn.socket\`:**

```
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock
SocketUser=ubuntu
SocketGroup=www-data
SocketMode=0770

[Install]
WantedBy=sockets.target
```

```
sudo mkdir -p /run/gunicorn
sudo chown ubuntu:www-data /run/gunicorn
sudo chmod 770 /run/gunicorn
sudo systemctl daemon-reload
sudo systemctl enable gunicorn.socket
sudo systemctl start gunicorn.socket
sudo systemctl start gunicorn.service
sudo systemctl status gunicorn.socket
sudo systemctl status gunicorn.service
sudo journalctl -u gunicorn.service
sudo tail -f /var/log/nginx/error.log
```

### Checkpoint

- Test the setup by accessing \`http://<ipaddr>/api/images/seatedposture/\`.

### Domain Name and HTTPS Setup

- Ask for a domain name from the admin and provide your public IP address.

```
sudo apt update
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx
```

### Update Nginx Configuration for HTTPS

```
sudo nano /etc/nginx/sites-available/your_site
```

**Content of \`/etc/nginx/sites-available/your_site\`:**

```
server {
  listen 80;
  server_name your_domain.com;
  return 301 https://$host$request_uri;
}

server {
  listen 443 ssl;
  server_name your_domain.com;

  ssl_certificate /etc/letsencrypt/live/your_domain.com/fullchain.pem;
  ssl_certificate_key /etc/letsencrypt/live/your_domain.com/privkey.pem;
  include /etc/letsencrypt/options-ssl-nginx.conf;
  ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

  location / {
    proxy_pass http://unix:/run/gunicorn.sock;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
  }
}
```

```
sudo nginx -t
sudo systemctl reload nginx
```

### Performance Optimization with Swap File

```
sudo swapon --show
sudo swapoff -a
sudo rm /swapfile
sudo fallocate -l 4G /swapfile
# If fallocate is not available:
# sudo dd if=/dev/zero of=/swapfile bs=1G count=4
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
sudo swapon --show
sudo nano /etc/fstab
```

Add this line to the end of \`/etc/fstab\`:

```
/swapfile none swap sw 0 0
```

- For better performance, more vCPU and RAM are recommended. The current $12 plan takes around 15 seconds per request; the $84 plan is almost instantaneous.

### References

- [Deploy Django with Nginx, Gunicorn, and SSL Certificate](https://syscrews.medium.com/deploy-django-with-nginx-gunicorn-and-ssl-certificate-ce7d037c7507)

### Final Notes

- Ensure all steps are followed in order.
- **Issues:** Highlighted sections need attention.


