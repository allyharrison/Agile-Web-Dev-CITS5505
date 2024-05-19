# Agile_Sem1_2024_Project

CITS5505 Agile Web Development Project due Sunday, May 19th, 2024.

## TABLE OF CONTENTS

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#group-members">Group Members</a>
    </li>
    <li>
      <a href="#stack-used">STACK USED</a>
    </li>
    <li>
      <a href="#local-development">Local Development</a>
    </li>
    <li>
      <a href="#deploying">Deploying</a>
    </li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

![image](https://github.com/allyharrison/Agile-Web-Dev-CITS5505/assets/131132228/407e3ab8-a097-4dfe-aa28-3d446991658e)

Our Website is all about food! FOODIE HUB is designed to be the one stop shop for all foodies, looking for something to eat? Look no further, the foodie hubs offers a variety of recipes. Looking for a recipe similar to one your Grandma made years ago but don't know where to start? Ask our Foodie hub community to help you discover and remake delicious flavours and meals! How about finding a new favourite place to east? Foodie hub has this recommendation as well!

Foodie Hub offers the chance to interact with like minded and taste-budded people a like. Check us out!

## Group Members 
# Group Members

| UWA ID       | Name          | Github Username |
|--------------|---------------|-----------------|
| 22974467     | Stevie Dahlin | St-d603         |
| 22581066      | Alexandra Harrison        | allyharrison|
| 23754739      | Neha Neha        | neha200796|
| 23244793      | Kartik Bhalala        | kartikbhalala|


### STACK USED

<img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white"/> <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white"/> <img src="https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E"/>

## Local Development

To run the project locally, first set up a `venv`, then `pip install` `requirements-dev` and then run flask.

```sh
# Activate virtual environment
python3 -m venv tmp-env
source tmp-env/bin/activate

# Install dependencies
pip install -r requirements-dev.txt # (this includes requirements.txt)

# Apply migrations
flask db upgrade 8f09b1c4c9ea

# Launch container for search
docker run --name elasticsearch -d --rm -p 9200:9200 --memory="2GB" -e discovery.type=single-node -e xpack.security.enabled=false -t docker.elastic.co/elasticsearch/elasticsearch:8.11.1

# Start app
flask run
```

If you would like to run with "livereload", run `python local_dev.py` instead of calling `flask run`.
This works well if you are editing HTML/CSS, not so great for editing Python files.

```sh
python local_dev.py
```

# Deploying

When deploying to production, only install `requirements.txt` (don't install `requirements-dev.txt`)

```sh
pip install -r requirements.txt
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>
