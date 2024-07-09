# Utiliser une image de base compatible AWS Lambda
FROM public.ecr.aws/lambda/python:3.10

RUN yum -y install tar gzip zlib freetype-devel \
    gcc \
    ghostscript \
    lcms2-devel \
    libffi-devel \
    libimagequant-devel \
    libjpeg-devel \
    libraqm-devel \
    libtiff-devel \
    libwebp-devel \
    make \
    openjpeg2-devel \
    rh-python36 \
    rh-python36-python-virtualenv \
    sudo \
    tcl-devel \
    tk-devel \
    tkinter \
    which \
    xorg-x11-server-Xvfb \
    zlib-devel \
    && yum clean all

# Copier les fichiers requirements et le script Python
COPY requirements.txt .

# Installer les dépendances Python spécifiées dans requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# COPY python /app/python
# ENV PYTHONPATH=/app/python

COPY models/bald_classifity.h5 models/bald_classifity.h5
COPY models/final_model.keras models/final_model.keras
COPY lambda_function.py .
COPY hair_segmenter.tflite .

# Définir le point d'entrée de la fonction Lambda
CMD ["lambda_function.lambda_handler"]