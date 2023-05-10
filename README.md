`Background`

Farm Flow is a web-based platform that aims to connect farmers with buyers, streamline the supply chain process, and empower farmers to sell their produce directly to consumers. The platform aims to address the challenges faced by farmers in accessing markets, managing their farms efficiently, and maximizing their profits. 

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

