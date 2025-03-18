import json
from config import *
from django.shortcuts import render, redirect
from .forms import SearchUserForm, EditUserForm
from logs import logger
from django.http import HttpResponse
from crud_operations import *
from redis_operations import *

collections = operation("user_db", "users")
myredis = redis_ops()

def search_user(request):
    try:
        form = SearchUserForm()
        user_data = None
        if request.method == "POST":
            logger.info(f"API: 'search_user' , PostParams:{dict(request.POST).items()}")
            form = SearchUserForm(request.POST)
            if form.is_valid():
                user_id = form.cleaned_data["user_id"]
                user_data = collections.read({"user_id": user_id}, {"_id":0})  
                if user_data:
                    logger.info(f"User found: {user_data}")
                else:
                    logger.warning(f"No user found with ID: {user_id}")
            else:
                logger.info(f"form error occured in search_user : {form.errors}")
        return render(request, "search.html", {"form": form, "user_data": user_data})
    except Exception as e:
        logger.error(f"Error Occurred in search_user(): {e}")
        return redirect("error")


       

def edit_user(request):
    form = EditUserForm()
    message = ""
    user_data = None
    try: 
        if request.method == "POST":
            logger.info(f"API: 'edit_user' , PostParams:{dict(request.POST).items()}")
            form = EditUserForm(request.POST)
            if form.is_valid():
                userid = str(form.cleaned_data["userid"])
                firstname = form.cleaned_data["firstname"]
                lastname = form.cleaned_data["lastname"]
                gender = form.cleaned_data["gender"]
                dob = form.cleaned_data["dob"]

                existing_user = collections.read({"user_id": userid})

                if existing_user:
                    collections.update(
                        {"user_id": userid},
                        {"firstname": firstname,"lastname": lastname, "gender": gender, "dob": str(dob)} 
                    )
                    message = "User updated successfully"
                    logger.info(f"Updated User {userid}")

                    user_data = collections.read({"user_id": userid})
                    logger.info(f"Updated User Data: {user_data}")
                    return redirect('success')
                else:
                    message = "User not found. No changes were made."
                    logger.warning(f"Attempted to update non-existent user: {userid}")
                    return HttpResponse(json.dumps({"status":"FAILURE", "statuscode":500, "msg": "User not found"}), content_type = "application/json")            
            else:
                logger.info(f"form error occured in edit_user : {form.errors}")
        return render(request, "edit_user.html", {"form": form, "message": message, "user_data": user_data})
    except Exception as e:
        logger.error(f"Error Occurred in edit_user(): {e}")
        return redirect('error')


def send_otp(request):
    try:
        if request.method == "POST":
            logger.info(f"API: 'send_otp' , PostParams:{dict(request.POST).items()}")
            user_id = request.POST.get("user_id") 
            otp = generate_otp()
            myredis.redis_set(user_id, DEFAULT_OTP_TIMEOUT, otp)
            logger.info(f"UserId: {user_id}, OTP: {otp}")
            return HttpResponse(json.dumps({"status":"SUCCESS", "statuscode":200, "msg" : "OTP sent successfully!"}), content_type="application/json")
        return HttpResponse(json.dumps({"status":"FAILURE", "statuscode":500, "msg": "Invalid request received, only 'POST' request are allowd."}), content_type = "application/json")
    except Exception as e:
        logger.info(f"Error Occured in send_otp {e}")
        return redirect('error')
            

def verify_otp(request):
    try:
        if request.method == "POST":
            logger.info(f"API: 'verify_otp' , PostParams:{dict(request.POST).items()}")
            user_id = request.POST.get("user_id")
            entered_otp = request.POST.get("enteredotp")
            correct_otp = myredis.redis_get(user_id)
            if correct_otp == entered_otp:
                return HttpResponse(json.dumps({"status":"SUCCESS", "statuscode":200, "msg": "✅ OTP Verified Successfully!"}), content_type = "application/json")
            else:
                return HttpResponse(json.dumps({"status":"FAILURE", "statuscode":500, "msg": "❌ Invalid OTP! Try again."}), content_type = "application/json")
        else:
            return HttpResponse(json.dumps({"status":"FAILURE", "statuscode":500, "msg": "Invalid request received, only 'POST' request are allowd."}), content_type = "application/json")
    except Exception as e:
            logger.info(f"Error Occured in verify_otp {e}")
            return redirect('error')