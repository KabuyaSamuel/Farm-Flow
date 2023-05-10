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


```bash
pip install -r requirements.txt
```

`Start database`

1. Windows

```bash
pg_ctl start
```
2. Linux

```bash
sudo systemctl start postgresql.service 
```

`Migrations`
```bash
python manage.py migrate 
```

`Run Locally`

```bash
python manage.py runserver
```

