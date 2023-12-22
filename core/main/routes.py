import secrets,os
from flask import render_template,url_for,request,redirect,send_from_directory,abort,flash,Blueprint,send_file,make_response,session
import datetime
import uuid
from PIL import Image
from core import app
from flask import jsonify
import time as t
import pymongo
from pymongo import MongoClient
from core.product.gptprompts import *

uri = "<YOUR CREDENTIALS>"
mongo_client = MongoClient(uri)
db = mongo_client['<database>']
collection = db['<collection>']

main = Blueprint('main',__name__)

@main.route("/")
def index():
    return render_template('index.html')

@main.route("/process-input",methods=['POST'])
def process_input():
    input_dat = request.form['input']
    
    base_idea, detailed_idea = clarify_idea(input_dat)
    market_size = genai_market_analysis(base_idea)
    value_proposition = genai_value_proposition(detailed_idea)
    target_audience = genai_target_audience(base_idea)
    pricing_strategy = genai_pricing_strategy(detailed_idea,market_size)
    go_to_market = genai_gtm(detailed_idea,pricing_strategy,target_audience)

    idea_id = str(uuid.uuid4())

    data = {
        '_id': idea_id,
        'idea_clarity' : {
            'one_line_idea':base_idea,
            'detailed_idea':detailed_idea,
        },
        
        'idea_validation': {
            'problem_identification': '',
            'target_audience':target_audience,
            'market_size':market_size,
            'competitors':''
        },
        'business_model' : {
            'value_proposition':value_proposition,
            'pricing_strategy':pricing_strategy,
            'gtm':go_to_market,
        },
        'product_development' : {
            'mvp':'',
            'tech_stack':'',
            'roadmap':'',
        },
    }
    collection.insert_one(data)
    return jsonify({'response': 'success', 'data': idea_id})