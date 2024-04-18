FROM ghcr.io/teheidoma/spring-boot-image-build-action-jdk17:0.0.2

COPY entrypoint.py /entrypoint.py

ENTRYPOINT ["python3", "/entrypoint.py"]
