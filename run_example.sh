#!/bin/bash
docker build -t django-rest-swagger-example .
docker run --rm -p 8000:8000 -v $(pwd):/code -ti django-rest-swagger-example
