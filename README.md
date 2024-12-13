## Overview
This is a simple service that classifies the given news article as fake or real. The service is built using Flask and the model is trained using the Fake and Real News Dataset from Kaggle. The model is a simple Logistic Regression model that uses TF-IDF vectorization to convert the text data into numerical data. The model is trained on the dataset and the accuracy of the model is around 98-99%.

### Dataset
The dataset used for training the model is the Fake and Real News Dataset from Kaggle. The dataset can be found [here](https://www.kaggle.com/datasets/emineyetm/fake-news-detection-datasets). The dataset contains two CSV files, one for fake news and one for real news. The dataset is used to train the model and the model is then used to classify the news articles as fake or real.

You may directly view/download the dataset from here:
- **[True.csv](/True.csv)**
- **[Fake.csv](/Fake.csv)**
### Usage
The service is hosted as a API and can be accessed using the following URL:
```
https://fake-news-detection-f27h.onrender.com/predict
```

You can use tools like Postman to send a POST request to the above URL with the following JSON data:
```json
{
    "news" : "The text of the news article"
}
```

Another option is to use curl to send a POST request to the above URL:
```bash
curl -X POST https://fake-news-detection-f27h.onrender.com/predict \ 
-H "Content-Type: application/json" \
-d '{"news": "The text of the news article"}'
```

The service will return a JSON response with the classification of the news article as either "Fake" or "Real".

### Example
Here is an example of how to use the service using curl:
```bash
curl -X POST https://fake-news-detection-f27h.onrender.com/predict \
-H "Content-Type: application/json" \
-d '{"news":"Scientists Confirm the Moon is Made of Cheese!"}'
```

The response will be:
```json
{
    "prediction": "Fake"
}
```

### Note
The service is hosted on a free tier of Render and may take some time to respond if it is inactive for a while. Please be patient and try again if the service does not respond immediately.

### Local Setup
If you want to run the service locally, you can follow these steps:
1. Clone the repository:
```bash
git clone https://github.com/YashwantBhosale/Fake-News-Detection.git
```
2. Change to the project directory:
```bash
cd Fake-News-Detection/server
```
3. Install the required dependencies:
```bash
pip install -r requirements.txt
```
4. Run the Flask server:
```bash
python app.py
```
5. The service will be available at `http://localhost:5000/`

You can now send a POST request to the local server at `/predict` route using curl or Postman as described above.

### Contributing
If you would like to contribute to this project, please feel free to fork the repository and submit a pull request. Any contributions are welcome!
 
*The project currently does not have any frontend and is only available as an API service. If you would like to contribute a frontend for the service, that would be greatly appreciated!*

**Steps for contributing**
1. Fork the repository
2. Clone the repository
```
git clone https://github.com/YashwantBhosale/Fake-News-Detection.git
```
3. Create a new branch
```
git checkout -b branch-name
```
4. Make changes
5. Commit changes
```
git commit -m "message"
```
6. Push changes
```
git push origin branch-name
```
7. Create a pull request

### About the author
- LinkedIn - [Yashwant Bhosale](https://www.linkedin.com/in/yashwant-bhosale-4ab062292/)
- GitHub - [Yashwant Bhosale](https://github.com/YashwantBhosale)

Happy coding! :heart:

