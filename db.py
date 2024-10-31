from flask import Flask, request, session, redirect, url_for, render_template, flash
import psycopg2
import psycopg2.extras

'''Db connection (postgreSQL)----------------------'''
 
DB_HOST = "localhost"
DB_NAME = "sasepasser"
DB_USER = "postgres"
DB_PASS = "" #db password here
 
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

'''------------------------------------------------'''