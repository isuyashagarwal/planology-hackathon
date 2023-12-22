import secrets,os
from flask import render_template,url_for,request,redirect,send_from_directory,abort,flash,Blueprint,send_file,make_response,session
import datetime
import uuid
from PIL import Image
from core import app
from flask import jsonify
from core.product.gptprompts import *
import pymongo
from pymongo import MongoClient

uri = "<YOUR CREDENTIALS>"
mongo_client = MongoClient(uri)
db = mongo_client['<database>']
collection = db['<collection>']

product = Blueprint('product',__name__)

@product.route("/<idea_id>/overview/",methods=['GET','POST'])
def overview(idea_id):
    idea = collection.find_one({'_id':idea_id})
    idea_clarity = idea['idea_clarity']
    one_line_idea = idea_clarity['one_line_idea']
    detailed_idea = idea_clarity['detailed_idea']
    return render_template('ideaoverview.html',one_line_idea=one_line_idea,detailed_idea=detailed_idea,idea_id=idea_id)

@product.route("/<idea_id>/idea-validation",methods=['GET','POST'])
def ideavalidation(idea_id):
    return render_template('ideavalidation.html',idea_id=idea_id)

@product.route("/<idea_id>/business-model/",methods=['GET','POST'])
def business_model(idea_id):
    return render_template('business-model.html',idea_id=idea_id)

@product.route("/<idea_id>/product-development/",methods=['GET','POST'])
def product_development(idea_id):
    return render_template('product-development.html',idea_id=idea_id)

@product.route("/<idea_id>/idea-validationproblem-statement/",methods=['GET','POST'])
def problem_statement(idea_id):
    idea = collection.find_one({'_id':idea_id})
    statement = idea['idea_validation']['problem_identification']
    print(statement)
    if len(statement) < 2:
        print("Generating Statement")
        one_line_idea = idea['idea_clarity']['one_line_idea']
        statement = genai_problem_statement(one_line_idea)
        collection.update_one({'_id':idea_id},{'$set':{'idea_validation.problem_identification':statement}})
    statement = statement.replace('\n','<br>')
    return render_template('problem-statement.html',statement=statement)

@product.route("/<idea_id>/idea-validationtarget-audience/",methods=['GET','POST'])
def target_audience(idea_id):
    idea = collection.find_one({'_id':idea_id})
    audience = idea['idea_validation']['target_audience']
    print(audience)
    if len(audience) < 2:
        print("Generating Audience")
        one_line_idea = idea['idea_clarity']['one_line_idea']
        audience = genai_target_audience(one_line_idea)
        collection.update_one({'_id':idea_id},{'$set':{'idea_validation.target_audience':audience}})
    audience = audience.replace('\n','<br>')
    return render_template('target-audience.html',audience=audience)

@product.route("/<idea_id>/idea-validation/market-analysis/",methods=['GET','POST'])
def market_analysis(idea_id):
    idea = collection.find_one({'_id':idea_id})
    market_size = idea['idea_validation']['market_size']
    print(market_size)
    if len(market_size) < 2:
        print("Generating Market Size")
        one_line_idea = idea['idea_clarity']['one_line_idea']
        market_size = genai_market_analysis(one_line_idea)
        collection.update_one({'_id':idea_id},{'$set':{'idea_validation.market_size':market_size}})
    market_size = market_size.replace('\n','<br>')
    return render_template('market-size.html',market_size=market_size)

# @product.route("/<idea_id>/idea-validation/competitors/",methods=['GET','POST'])
# def competitors(idea_id):
#     idea = collection.find_one({'_id':idea_id})
#     competitors = idea['idea_validation']['competitors']
#     print(competitors)
#     if len(competitors) < 2:
#         print("Generating competitors")
#         detailed_idea = idea['idea_clarity']['detailed_idea']
#         competitors = genai_competitors(detailed_idea)
#         collection.update_one({'_id':idea_id},{'$set':{'idea_validation.competitors':competitors}})
#     competitors = competitors.replace('\n','<br>')
#     return render_template('competitors.html',competitors=competitors)

@product.route("/<idea_id>/business-model/value-proposition/",methods=['GET','POST'])
def value_proposition(idea_id):
    idea = collection.find_one({'_id':idea_id})
    value_proposition = idea['business_model']['value_proposition']
    print(value_proposition)
    if len(value_proposition) < 2:
        print("Generating value_proposition")
        detailed_idea = idea['idea_clarity']['detailed_idea']
        value_proposition = genai_value_proposition(detailed_idea)
        collection.update_one({'_id':idea_id},{'$set':{'business_model.value_proposition':value_proposition}})
    value_proposition = value_proposition.replace('\n','<br>')
    return render_template('value-proposition.html',value_proposition=value_proposition)

@product.route("/<idea_id>/business-model/pricing-strategy/",methods=['GET','POST'])
def pricing_strategy(idea_id):
    idea = collection.find_one({'_id':idea_id})
    pricing_strategy = idea['business_model']['pricing_strategy']
    print(pricing_strategy)
    if len(pricing_strategy) < 2:
        print("Generating Pricing Strategy")
        detailed_idea = idea['idea_clarity']['detailed_idea']
        market_size = idea['idea_validation']['market_size']
        pricing_strategy = genai_pricing_strategy(detailed_idea,market_size)
        collection.update_one({'_id':idea_id},{'$set':{'business_model.pricing_strategy':pricing_strategy}})
    pricing_strategy = pricing_strategy.replace('\n','<br>')
    return render_template('pricing-strategy.html',pricing_strategy=pricing_strategy)

@product.route("/<idea_id>/business-model/go-to-market/",methods=['GET','POST'])
def go_to_market(idea_id):
    idea = collection.find_one({'_id':idea_id})
    gtm_strategy = idea['business_model']['gtm']
    print(gtm_strategy)
    if len(gtm_strategy) < 2:
        print("Generating Pricing Strategy")
        detailed_idea = idea['idea_clarity']['detailed_idea']
        pricing_strategy = idea['business_model']['pricing_strategy']
        target_audience = idea['idea_validation']['target_audience']
        gtm_strategy = genai_gtm(detailed_idea,pricing_strategy,target_audience)
        collection.update_one({'_id':idea_id},{'$set':{'business_model.gtm':gtm_strategy}})
    gtm_strategy = gtm_strategy.replace('\n','<br>')
    return render_template('gtm.html',gtm_strategy=gtm_strategy)

@product.route("/<idea_id>/product-development/tech-stack/",methods=['GET','POST'])
def tech_stack(idea_id):
    idea = collection.find_one({'_id':idea_id})
    tech_stack = idea['product_development']['tech_stack']
    print(tech_stack)
    if len(tech_stack) < 2:
        print("Generating Tech Stack")
        detailed_idea = idea['idea_clarity']['detailed_idea']
        tech_stack = genai_tech_stack(detailed_idea)
        collection.update_one({'_id':idea_id},{'$set':{'product_development.tech_stack':tech_stack}})
    tech_stack = tech_stack.replace('\n','<br>')
    return render_template('tech-stack.html',tech_stack=tech_stack)

@product.route("/<idea_id>/product-development/roadmap/",methods=['GET','POST'])
def roadmap(idea_id):
    idea = collection.find_one({'_id':idea_id})
    roadmap = idea['product_development']['roadmap']
    print(roadmap)
    if len(roadmap) < 2:
        print("Generating roadmap")
        detailed_idea = idea['idea_clarity']['detailed_idea']
        value_proposition = idea['business_model']['value_proposition']
        roadmap = genai_roadmap(detailed_idea,value_proposition)
        collection.update_one({'_id':idea_id},{'$set':{'product_development.roadmap':roadmap}})
    roadmap = roadmap.replace('\n','<br>')
    return render_template('roadmap.html',roadmap=roadmap)
