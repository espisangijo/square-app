# Square Prediction

Inspired by GoodNotes, this project aims to solve the problem in creating squares in the application. Looking like an image data, intuitively people will work on it using image processing techniques in the feature engineering stage. However, one of the most valuable data is not taken into account when processing using aforementioned technique -- **_time_**. Time is essential in predicting whether a stroke results in a square or not.

## Scenario
Consider these 2 cases, drawing a square very quickly, and drawing an identical square very slowly, but a curve exists on the right-hand-side of the squares. The **time** affects the user's intention, whether they are drawing a square or not. Treating the problem as an image classification (e.g. using CNN) only captures the shape and will predict both of them as not a square since there is a curve on the side.

## Feature Engineering
To preserve its timeliness, we need to capture all the coordinates at every timestamp. To process the data, we can borrow a technique from text processing. **Truncation** (for long data, setting truncation threshold to e.g. covering 95% of normal distribution), **padding** (for short data, pad 0s to make the length similar), **interpolation** (get coordinates e.g. every 50ms, used to preserve the timeliness) and **normalization** (for faster training and normalizing initail drawing point to (0,0)) are the techniques commonly used in text processing that we can use in this prediction.

## Application
This project mainly focuses on the engineering side of things (feature engineering, code structure, dockerization, testing, logging and documentation) rather than machine learning. It simply uses an SVM classifier to predict, and it was trained on a tiny dataset (200 data, 100 for each class) where some of the samples are almost indistinguishable. The application allows users to add new data for retraining, perform retraining on the newly added data and predicting data based on the models trained. Initially, it comes with a base model and data (labelling done by the same application too) so it can be immediately used.

## Setup (Debug)
When debugging, you can see what happened in the backend folders where the data and models are stored. In the logging folder, you can also see changes in the logs when the application is running and APIs are called.
### Backend
To serve the backend application, these are the commands you need to run:
```bash
cd square-app/square-api
pipenv shell
pip install -r requirements.txt
gunicorn --bind 0.0.0.0:8001 app:api
```
Now the backend should be ready to serve api requests

### Frontend
To run the frontend application, these are the commands you need to run:
(node version 12.18.3)
```bash
cd square-app/square-ui
npm install
npm start
```
A browser should be up and running the frontend application
Make sure the backend is up and running if you want to send requests to the backend

## Setup (Production)
### Docker-compose
Docker compose is a tool for defining and running multi-container Docker applications. In this application, there are 2 containers. A container for the front-end and the back-end. By running the following command, it will build a docker image with the both containers ready for production stage.
```bash
cd square-app
docker-compose up -d --force-recreate
```

To stop and remove all the images created, run:
```bash
docker-compose down --rmi all
```

## How to use
User can choose to perform retraining/prediction using the toggle slider located in the top-left corner. Every time you draw, when you lift the mouse-click, it will automatically add to retraining data/predict. This is a better approach compared to using submit buttons for faster data input for retraining.

### Retraining
In retraining mode, 4 buttons are available:
1. Push data for retraining: to perform retraining (create a new data in the backend)
2. Pop from square list: remove the last appended data from square list
3. Pop from not-square list: remove the last appended data from not-square list
4. Retrain: to perform retraining (create a new model in the backend)

To label the data, there is a slider which shows "Square" or "Not Square". Toggle it to change the label you want.
Every time you finish drawing, the counter for the label you have drawn will be updated.
If you want to remove your latest input for a certain label, click on the pop button mentioned above to remove it.

### Prediction
Simply draw anything when you toggled the prediction on. It will output the prediction when you lift your mouse-click.

## Technology Stack
### Backend
For the backend, Falcon is used as the API framework because it's lightweight, very fast and help to reduce the size of the code base because of its simplicity. All APIs I previously deployed uses Falcon and it performs really well when tested using JMeter.

### Frontend
For the frontend, I use ReactJS because it has high community support, high job market popularity, and ease of use. I learned ReactJS during my free time along with it's popular full stack friends: MongoDB for database, ExpressJS for building the API, and NodeJS as its foundation.

### Containers
I used docker quite often to deploy my APIs. It's the most popular containerization tool in the market and comes very handy for deployment. People often compare Docker to VM because it serves similar purpose, but it's much more lightweight due to its OS-Level virtualization unlike VM which needs OS in every VM.

### Miscellaneous
For testing, I used PyTest because the syntax is better compared to Python's built-in unittest. Using decorators to add optional features makes PyTest better than unittest.
