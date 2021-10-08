# webapp-homework

# To build and run the API
docker build -t api-image .     
docker run -d --name api-container -p 8000:8000 api-image

# To build and run the WebApp
docker build -t streamlit-image .    
docker run -d --name container-streamlit -p 8501:8501 streamlit-image
