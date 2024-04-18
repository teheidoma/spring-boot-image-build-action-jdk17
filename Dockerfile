FROM ghcr.io/teheidoma/spring-boot-image-build-action:0.0.1

COPY entrypoint.py /entrypoint.py

ENTRYPOINT ["python3", "/entrypoint.py"]
