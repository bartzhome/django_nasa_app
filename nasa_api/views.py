"""
Django web app that communicates with NASA API - APOD. User can select range of dates to search pictures of the day.
App will return from date range

TODO:
    - Advanced search
        - Thumbnails
        - Number of results to return
    - Utlities
        - Sorting
"""

from django.shortcuts import render
from datetime import datetime
import requests


def home(request):
    """
    Home function handles user interaction with web application.
    If not a post request - display initial page with a todays date as default for end date
    If post request with start and end dates - validate dates, return search results or error message
    :param request: request from client side
    :return: search results or error message
    """

    # if not a post request, display page
    if request.method != "POST":
        date_now = datetime.today().strftime('%Y-%m-%d')
        return render(request, 'base.html', {'date': date_now})

    # if post request are present, continue to process post request
    if request.POST['start-date'] and request.POST['end-date']:
        # convert to date string to datetime and validate that dates are valid format
        # if not, raise value error exception
        try:
            start_date = datetime.strptime(request.POST['start-date'], '%Y-%m-%d')
            end_date = datetime.strptime(request.POST['end-date'], '%Y-%m-%d')
            date_now = datetime.today()
        except ValueError:
            message = "Incorrect data format, should be YYYY-MM-DD"
            return render(request, 'base.html', {'message': message, 'date': date_now})

        # validate that start date is less than end date and end_data is equal or less than todays date
        if start_date < end_date <= date_now:
            # convert dates back to string format
            start_date = datetime.strftime(start_date, '%Y-%m-%d')
            end_date = datetime.strftime(end_date, '%Y-%m-%d')

            # get results from search
            results = search_results(request,start_date, end_date)
            date_now = datetime.today().strftime('%Y-%m-%d')
            return render(request, 'home.html', {'results': results, 'date': date_now})

        else:
            # return with error message
            message = "Start Date must be before End Date and End Date cannot be date in future."
            return render(request, 'base.html', {'message': message, 'date': date_now})

    else:
        message = "Invalid Date Entry. Please try again."
        date_now = datetime.today().strftime('%Y-%m-%d')
        return render(request,'base.html', {'message': message, 'date': date_now})


def search_results(request,start_date, end_date):
    """
    Function makes a call to NASA APOD API to retreive data from user selected date range.
    :param request: user request data
    :param start_date: a valid start date
    :param end_date: a valid end date
    :return: return json data for date range from nasa api response or connection error message
    """

    # api key
    API_KEY = "EAnJsZsdRGv4hM0zeLUKosCya5AkJV1GP5jDHRxQ"

    # api url
    url = "https://api.nasa.gov/planetary/apod"

    # parameters used in query
    params = {'start_date': start_date,
              'end_date': end_date,
              'api_key': API_KEY}

    # try for a get request response from url with parameters
    # if not connection can be made, except and send connection error message
    try:
        response = requests.get(url=url, params=params)
        json_data = response.json()
        return json_data
    except ConnectionError:
        message = "There was a connection error. Please try again later."
        return render(request, 'base.html', {'message': message})