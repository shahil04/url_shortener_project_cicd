name: Deploy Docker App to EC2

on:
  push:
    branches:
      - master

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout Code
      uses: actions/checkout@v4

    - name: Login to Docker Hub
      run: |
        echo "${{ secrets.DOCKER_PASSWORD }}" | docker login \
        -u "${{ secrets.DOCKER_USERNAME }}" --password-stdin

    - name: Build Docker Image
      run: |
        docker build -t ${{ secrets.DOCKER_USERNAME }}/url-shortener:latest .

    - name: Push Docker Image
      run: |
        docker push ${{ secrets.DOCKER_USERNAME }}/url-shortener:latest

    - name: Deploy on EC2
      uses: appleboy/ssh-action@v1.0.0
      with:
        host: ${{ secrets.EC2_HOST }}
        username: ${{ secrets.EC2_USER }}
        key: ${{ secrets.EC2_KEY }}
        script: |
          docker stop url-shortener || true
          docker rm url-shortener || true
          docker pull ${{ secrets.DOCKER_USERNAME }}/url-shortener:latest
          docker run -d \
            --restart=always \
            -p 80:8000 \
            --name url-shortener \
            ${{ secrets.DOCKER_USERNAME }}/url-shortener:latest



# name: Flask CI

# on:
#   push:
#     branches: ["master"]

# jobs:
#   build:
#     runs-on: ubuntu-latest

#     steps:
#     # 1️⃣ Checkout code
#     - name: Checkout Repository
#       uses: actions/checkout@v3

#     # 2️⃣ Setup Python
#     - name: Set up Python
#       uses: actions/setup-python@v4
#       with:
#         python-version: "3.10"

#     # 3️⃣ Install dependencies
#     - name: Install dependencies
#       run: |
#         pip install -r requirements.txt

#     # 4️⃣ Run basic Flask check
#     - name: Run Flask Test
#       run: |
#         python -m py_compile app.py

#     - name: Debug Secrets (TEMP)
#       run: |
#         echo "Username length: ${#DOCKER_USERNAME}"
#       env:
#         DOCKER_USERNAME: ${{ secrets.DOCKER_USERNAME }}

#     # 5️⃣ Login to Docker Hub
#     - name: Docker Login
#       run: |
#         echo "${{ secrets.DOCKER_PASSWORD }}" | docker login \
#           -u "${{ secrets.DOCKER_USERNAME }}" --password-stdin

#     # 6️⃣ Build Docker image
#     - name: Docker Build
#       run: |
#         docker build -t shahil004/url-shortener:latest .

#     # 7️⃣ Push Docker image
#     - name: Docker Push
#       run: |
#         docker push shahil004/url-shortener:latest
