instructions:

1) pip install -r requirements.txt
2) cd matcher_app
3) please set the user and the password of your local mysql in database.py
4) run: python setup.py
5) cd ..
6) run: python manage.py runserver

comments:

1) running  setup.py create the db, table and fill it with fake data
2) the endpoint should get a post request the parameters in body are title, skills and page (page is not required)
3) the response is json that contain the top 20 order by rating (the rating is determined by matching of skills)
4) if not given page parameter the response will be the top 20 candidates if page parameter is passed we get the according slice
5) attached postman file called Backend-gloat.postman_collection.json for example, please import this to postman while server is running 
