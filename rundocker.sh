#!/bin/bash

clear;docker build . -t main && docker-compose -f docker-compose.yml -p 'visitorsbook' up --remove-orphans