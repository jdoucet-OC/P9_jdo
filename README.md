# P9_jdo

## Introduction

This python project is a django-based web application that allows users to create tickets which can be then answered by other users, with a review system.  
Users can follow each others.  
Any followed user's activity can be seen in the homepage.  

## Install
1.Download the github project, unzip it in the folder of your choosing  
2.Using a terminal, place yourself in the project folder and create a virtual environnement using :  
`python -m venv env`  
3.Activate the virtual environnement using :  
windows : `env/Scripts/activate.bat`  
linux / mac : `source env/bin/activate`  
4.Install the python packages needed to run the programm using :  
`pip install -r requirements.txt`  
5.Run the launcher using :  
`python main.py`  

## Flake-8 Report
To generate a Flake8-html report, use :  
`flake8 --format=html --htmldir=flake-report`  
