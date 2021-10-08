# webapp-homework
## Prepared by Victor Elizondo 

## The Challenge
The homework assignment involves writing some code against Etsy's API, parsing results, and then deriving some aggregate stats from the data:
1. Sign up for an account on Etsy and obtain a set of API keys.
2. Spend a few minutes browsing Etsy, and identify a set of 10 different shops on the site.
3. Use the API to pull all items sold in the shop and extract the title and descriptions from these items.
4. With the above dataset, write an algorithm to identify the top 5 meaningful terms for each shop.
5. Write a web application to display the results

## Solution's Approach
The solution has 2 modules, an API to process the interaction with Etsy's API (abstraction layer) and a Webapp to process the extracted data and analise it to get the most meaningful terms.
For the API I used FastAPI and for the Webapp Streamlit.
For the meaningful terms extraction I used a simple feature extraction NLP algorithm using the scikit-learn library to count words along the whole text and also removing the stop-words.
Both modules have been containerized

## To build and run the API
    docker build -t api-image .     
    docker run -d --name api-container -p 8000:8000 api-image

## To build and run the WebApp
    docker build -t streamlit-image .    
    docker run -d --name container-streamlit -p 8501:8501 streamlit-image
