# Nativo CLP Validator v1.0
# usage - python3 clp_validator.py
# Here are some CLP URLs for testing purposes:
# Working page test
# https://www.chicagotribune.com/paid-posts/
# 404 test
# https://www.nativo.com/thisisnotarealpage
# No load.js test
# https://www.al.com/sponsor-content/
# 403 test
# https://www.michigansthumb.com/prepzone/article/Cass-City-drops-home-opener-to-Montrose-Hill-14401106.php
# Timeout test
# http://www.miamiherald.com/advertise/sponsored_content/
import requests
from requests.exceptions import Timeout
from requests.exceptions import MissingSchema
import re
from flask import Flask, request, render_template, Markup

def check_url(url):
    final_response_list = []
    final_response = ""
    try:
        r = requests.get(url, timeout=5)
    except Timeout:
        final_response_list.append("Error - This page took too long to respond.")
        for x in final_response_list:
            final_response += Markup('<p>' + x + '</p>')
        return final_response

    except MissingSchema:
        final_response_list.append("Error - Invalid URL.")
        for x in final_response_list:
            final_response += Markup('<p>' + x + '</p>')
        return final_response

    if r.status_code != 200:
        final_response_list.append("Error - This page did not respond with a 200 status code.")
        final_response_list.append("Response received: " + str(r.status_code))
        for x in final_response_list:
            final_response += Markup('<p>' + x + '</p>')
        return final_response

    response = str(r.text)
    response_array = response.split("</head>", maxsplit=1)
    response_array[0] += "</head>"
    head = response_array[0]
    full_link_array = [m.start() for m in re.finditer('<link', head)]
    full_meta_array = [m.start() for m in re.finditer('<meta', head)]
    full_script_array = [m.start() for m in re.finditer('<script', response)]
    link_array = []
    meta_array = []
    items_to_remove = []
    items_to_add = []
    no_js_on_page = []
    no_http_equiv_meta = True
    no_robots_meta = True

    for x in full_link_array:
        full_current_link = head[x:(x+5000)]
        current_link_array = full_current_link.split(">", maxsplit=1)
        current_link = current_link_array[0]
        if current_link.endswith('/'):
            current_link = current_link[:-1]
        current_link += "&gt;"
        link_array.append(current_link)

    for x in full_meta_array:
        full_current_meta = head[x:(x+5000)]
        current_meta_array = full_current_meta.split(">", maxsplit=1)
        current_meta = current_meta_array[0]
        if current_meta.endswith('/'):
            current_meta = current_meta[:-1]
        current_meta += "&gt;"
        meta_array.append(current_meta)

    for x in link_array:
        if 'rel="canonical' in x:
            items_to_remove.append(x)

    for x in meta_array:
        if 'property="og:' in x:
            items_to_remove.append(x)

    for x in meta_array:
        if 'http-equiv="X-UA-Compatible" content="IE=edge' in x:
            no_http_equiv_meta = False

    if no_http_equiv_meta == True:
        items_to_add.append('<meta http-equiv="X-UA-Compatible" content="IE=edge">')

    for x in meta_array:
        if 'name="robots" content="noindex, nofollow' in x:
            no_robots_meta = False

    if no_robots_meta == True:
        items_to_add.append('<meta name="robots" content="noindex, nofollow">')

    if 's.ntv.io/serve/load.js' not in response:
        no_js_on_page.append("Our load.js script was not detected. Please verify our load.js is on the page (it may have been loaded dynamically).")

    if len(items_to_remove) > 0:
        final_response_list.append("The following tags should be removed from this page:")
        for x in items_to_remove:
            y = "&lt;" + x[1:]
            final_response_list.append(y)

    if len(items_to_add) > 0:
        final_response_list.append("The following tags should be added to this page:")
        for x in items_to_add:
            y = "&lt;" + x[1:]
            final_response_list.append(y)

    if len(no_js_on_page) > 0:
        final_response_list.append("Additional information:")
        for x in no_js_on_page:
            final_response_list.append(x)

    for x in final_response_list:
        final_response += Markup('<p>' + x + '</p>')
    return final_response

app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def my_results_form():
    if request.method == 'POST':
        text = request.form['text']
        output = check_url(text)
        return render_template('results.html', output = output)
    elif request.method == 'GET':
        return render_template('index.html')

if __name__ == '__main__':
   app.run(debug = True, port = 3456, host = '0.0.0.0')