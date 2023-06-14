# FARM FLOW - TRADING AS FARM SHARE 

Farm Flow is a web-based platform that aims to connect farmers with buyers, streamline the supply chain process, and empower farmers to sell their produce directly to consumers. 

Live link to the project
[Farm Share](https://farmshare.co.ke/)

## Table of Contents

- [Project Overview](#project-overview)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

Farm Flow is a web-based platform designed to address the challenges faced by farmers in accessing markets, managing their farms efficiently, and maximizing their profits. It aims to connect farmers with buyers, streamline the supply chain process, and empower farmers to sell their produce directly to consumers. By providing a user-friendly platform that enables efficient farm management and market access, Farm Flow seeks to expand farmers' market reach, improve farm management practices, and increase their profits. The success of Farm Flow will be measured by the number of farmers successfully connected with buyers and the adoption of planning, tracking, and data-driven decision-making tools leading to improved crop yields and farm profitability.


Live link to the project
[Farm Share](https://farmshare.co.ke/)

## Installation


`setup`

Create a virtual environment and activate it with the following commands. 

1. Windows
```bash
python -m venv myenv
```

```bash
myenv\Scripts\activate.bat
```

2. Linux

``` bash 
python3 -m venv myenv 
```

```bash
source venv/bin/activate  
```


`install dependancies`

Upon creating a virtual environment, proceed to install the project dependencies with the following command

```bash
pip install -r requirements.txt
```

`Start database`

Next step  is to start the database. On a new terminal run the following command

1. Windows

```bash
pg_ctl start
```
2. Linux

```bash
sudo systemctl start postgresql.service 
```

`Migrations`

Once the database is up and running - migrate the db 

```bash
python manage.py migrate 
```

`Run Locally`

Once all the above steps are done - proceed to run the project locally by running the following command. 

```bash
python manage.py runserver
```

`Run All Tests`
```bash 
python manage.py test
```

`Run Specific Test`
```bash 
python manage.py test <app_name>.tests.<TestClassName>.<test_method_name>
```

## Usage

1. Landing on the Farm Share homepage, users can select the "Farmer Login" button to access the "Value Chain Login" screen.
2. New users have the option to register for a new account by clicking on "Sign Up".
3. Existing users can log in using their established username and password, or they can choose to authenticate via Google.
4. Upon successful login, users are directed to their dashboard.
5. On the dashboard, users can add a value chain by selecting the "Add Value Chain" option on the value chain card. Note that attempting to add a pre-existing value chain will generate an error message.
6. Users can add a crop by selecting the "Add Crop" option on the crop card. They need to provide details such as the crop's name, description, and associated value chain. After successfully adding a crop, the user is redirected to the homepage, and a success message is displayed.
7. Users can add a farm by selecting the "Add Farm" option on the farm card. They should provide farm details such as location, crops grown, farm size, soil test results, water source, and farming type.
8. Once a farm is successfully added, a success message is displayed, and both an email and an SMS (if a phone number is provided) are sent to the user. Additionally, an email notification is sent to the admin.
9. The admin verifies and approves the farm submission via their dashboard. After approval, an approval notification is sent to the user through email and SMS (if a phone number is provided).
10. The dashboard's farm and crop counts are updated, and the details of farms and crops are displayed under the "List of Crops" and "List of Farms" sections.
11. Users can check the health of their crops by uploading crop pictures in the "Crop Disease Checker" available under the "Resources" menu.
Weather information and forecasts specific to the farm can be accessed under the "Current Weather" and "Weather Forecast" sections.
12. Users have access to soil data, satellite tracking, satellite images of their farms, and the UV index under the "Agro Monitoring" in the "Agrotech" menu.
13. Farm trends can be visualized through various charts such as graphs, bar charts, and pie charts, accessible under the "Charts" menu.
14. Users can view crop production tables under the "Tables" menu.
16. Users have the option to log out of the system.
17. Users can visit the online shop to view and manage their listed produce for sale

## Features

1. Agro Monitoring - Users can access soil data, satellite tracking, satellite images of their farms, and UV
index

2. Crop Disease Checker - Checks crop health by uploading a crop picture

3. Weather Forecast - Provides weather information and forecasts for the farm

4. WhatsApp - Provides live communication via WhatsApp

5. Shop - Buyers can access farmers end produces and purchase. 


## Technologies Used


1. Django - Our Python framework used on the backend.
2. PostgreSQL - The project's database. 
3. Railway - Deployment/Hosting services.
4. WordPress - Frontend of our project
5. WooCommerce - Powering the shop
6. HTML, CSS, JavaScript - Project's interactivity

## Contributing

Want to contribute? Great!

To fix a bug or enhance an existing module, follow these steps:

1. Fork the repo
2. Create a new branch (git checkout -b improve-feature)
3. Make the appropriate changes in the files
4. Add changes to reflect the changes made
5. Commit your changes (git commit -am 'Improve feature')
6. Push to the branch (git push origin improve-feature)
8. Create a Pull Request

Known Bugs
If you find a bug (the website couldn't handle the query and / or gave undesired results), kindly [Open Issue](https://github.com/KabuyaSamuel/Farm-Flow/issues/new)   by including your search query and the expected result.

If you'd like to request a new function, feel free to do so by going to [New Function](https://github.com/KabuyaSamuel/Farm-Flow/issues/new). Please include sample queries and their corresponding results.

Please provide feedback on our project at [Padlet](https://padlet.com/samuelkabuya/farmflow-feedback-padlet-g95u07gsjwyig7sd). Your thoughts and suggestions are valuable to us. FarmFlow Team!


## License

MIT License




