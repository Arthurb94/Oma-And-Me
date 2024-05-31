# Utiliser l'image de base officielle Amazon Linux 2 pour AWS Lambda
FROM public.ecr.aws/lambda/python:3.10

# Installations préliminaires
RUN yum -y update && \
    yum -y install unzip wget

# Install dependencies for OpenCV
RUN yum install -y gcc cmake git \
    libjpeg-turbo libpng libtiff libjasper openexr \
    gtk2 gtk3 \
    mesa-libGL mesa-libGL-devel mesa-libGLU mesa-libGLU-devel \
    libSM libXrender libXext

# Install Python packages
RUN pip install --upgrade pip

# Install Python packages, including OpenCV
RUN pip install opencv-python-headless keras tensorflow numpy mediapipe

# Copy the model files to the container
COPY . .

# Command to run the Lambda function handler
CMD ["lambda_function.lambda_handler"]
