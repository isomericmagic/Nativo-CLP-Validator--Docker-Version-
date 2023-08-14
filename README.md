# Nativo CLP Validator
This is a dockerized version of a single page web app that I wrote while working at Nativo. Publishers setup content landing pages (CLPs) for use with the Nativo platform so they can create advertising content that matches the look and feel of other articles on their site. To avoid SEO and reporting issues, we would ask publishers to remove canonical URLs and og tags the while setting up their CLP. Here are some examples:

**Canonical URL Example**
`<link rel="canonical" href="http://www.yoursite.com/sponsored/" />`

**OG Tag Example**
`<meta property="og:url" content="http://www.yoursite.com/sponsored/" />`
 
We would also recommend adding `<meta name="robots" content="noindex, nofollow" />` on the CLP to avoid being penalized or even delisted from Google results.

This script analyzes the URL that is entered into the form field and evaluates the response from the website to determine if these elements exist on the page and make recommendations based on the response. I originally wrote it as a standalone flask app, but eventually learned Docker and figured it would be better as a Docker app since this would enable users to get it up and running without having to worry about installing Python locally and setting up a virtual environment for flask to run in.

**Usage**
You will need to install Docker. Once that's done just download the files, cd to the clp_validator directory and then run 
`docker compose up`
or 
`docker compose up --build`
if you want to rebuild the container from scratch. Then just navigate to the following url:
http://127.0.0.1:5000/
in your browser and enter the url you want to test. For example, this url:
https://www.chicagotribune.com/paid-posts/

You could also test a page that doesn't exist like this one:
https://www.nativo.com/thisisnotarealpage

and additional test urls are included in the code comments.