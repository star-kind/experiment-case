# experiment-case

<hr>

## Project Introduction

This is a web project based on the Python Flask framework, which implements login registration, email modification, and password modification functions. The database uses SQLite3, the project entry is hinge.py, and the first address is http://127.0.0.1:8085/ . The backend code is placed in the backstage directory, HTML template files are placed in the front/template directory, and JS/CSS/Assets are placed in the static directory. In addition, the project also implements token verification and AES algorithm encryption functions.

<hr>

## Installation dependencies

Run the following command in the project root directory to install the required dependencies：

```
pip install -r requirements.txt
```

<hr>

## Run Project

Run the following command in the project root directory to start the project：

```
python hinge.py
```

### Attention

I used gunicorn+gevent to launch this web application, and the correct approach is as follows:

```
cd src;
chmod+x gunicorn-start.sh;
bash gunicorn-start.sh;
```

<hr>

## Directory structure

```
src
├── backstage
│       ├── consts
│       │
│       ├── logger
│       │
│       ├── persist
│       │
│       └── produce
│
├── config
│
├── databases
├── journals
├── static
│       ├── css
│       ├── images
│       └── js
└── templates
```

<hr>

# Necessary steps

- Run generate before running the: generate_pth.py, obtain the pth file, then move the pth file to the directory: /path/[python directory]/\*/lib/${python --version}/site-packages/

- Run script: `retrieval-site-pkgs` to find directory: `site-packages`

- Check if it has been added to the system path: `type-sys-path`

<hr>

## Function Description

1. Login function: Users enter their email and password, and after successful verification, they will be redirected to the personal center page.
2. Registration function: Users enter their password and email, and after successful verification, create a new user and redirect to the login page.
3. Modify email function: Users enter their password and new email, and after successful verification, update their email information.
4. Password modification function: Users enter their old and new passwords, and after successful verification, update their password information.
5. Token verification: Generate a token when the user logs in and store it on the client side. Attach this token to the request header for authentication each time a request is made.
6. AES algorithm encryption: When users register or change passwords, use AES algorithm to encrypt sensitive information to protect data security.
7. Added blog encryption and decryption capabilities.

<hr>

## Docker

- Docker creates an image named 'test1':

```
docker build -t 'test1' .
```

- Docker backend (-d) runs web applications (port numbers must be consistent, otherwise some resources may be 404)：

```
# test1 is docker image name
docker run -t -i -d -p 8085:8085 test1
```

<hr>

## Remote use Docker image

Q: I created a Docker image called test1 on computer A, how to run test1 on computer B?

A: To run test1 on computer B, you need to first transfer test1 from computer A to computer B, and then use the Docker command on computer B to run the image.
The specific steps are as follows：

1. Export test1 as a tar file on computer A：

```
docker save -o test1.tar test1
```

- 2. Copy the test1.tar file to computer B.

  - 2.1 Install docker at computer B:
    omit...

  - 2.2 Add users to Docker group:

    ```
    sudo usermod -aG docker $USER
    ```

  - 2.3 View Docker Group Members:
    ```
    getent group docker | cut -d: -f4
    ```

3. Load the test1. tar file on computer B：

```
docker load -i test1.tar
```

4. Backend run test1 image：

```
docker run -d -p 8085:8085 test1
```

<hr>

## Identify

lub2304-1-stki-sz15

<hr>

## Nginx

- Edit nginx.conf,add new content as follow(SSL certificate needs to be generated through OpenSSL):

```
    upstream flask01 {
            server 127.0.0.1:8085;
    }

    server {
            # listening
            listen 81 ssl;

            server_name localhost;

            # SSL configuration
	          ssl_certificate			  /opt/nginx/certificates/server1/server1.crt;
	          ssl_certificate_key		/opt/nginx/certificates/server1/server1.key;

            # default request url
            location / {

            # Request forwarded to Gunicorn server
            proxy_pass http://flask01;

            # Set the request header and pass the header information to the server side
            proxy_set_header Host $host;
        }
    }

```

- check

```
nginx -t
```

- reload

```
nginx -s reload
```

- visit: https://IP_ADDRESS:Nginx.PORT

<hr>
