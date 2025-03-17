# Description
This URL shortener application demonstrates a functional Python Django web app, providing practical examples of modern DevOps practices for building, containerizing, and deploying applications. The project serves as a reference application, showcasing the full software lifecycle — from development to deployment — and highlights the integration of development and DevOps principles for delivering a complete application stack.

A key feature of this project is the provided Docker container image, which is available on Docker Hub. By simply pulling the image and running it locally, users can quickly set up a working version of the app with sample data. This offers an easy, hands-off approach to deploying the application without needing to worry about building the container from scratch, providing a hassle-free way to test and use the app.

In addition to Docker, this project includes a Kubernetes manifest that demonstrate how to deploy and manage the app in a cloud-native environment. While the app is designed to run easily on a local machine using Docker, these manifests provide a clear path to deploying the app on a Kubernetes cluster, showcasing the scalability and flexibility of containerized applications.

Although it's a simple URL shortener, this application demonstrates how small-scale apps can be effectively containerized and deployed using modern DevOps tools like Docker and Kubernetes. This makes it an ideal reference for developers looking to learn about web development, containerization, and deploying applications in a scalable, cloud-native environment.

Application stack:
- Backend: Python, Django, SQL
- Frontend: HTML, CSS, Django Templates (server-side rendering)
- Container/Orchestration: Docker, Kubernetes
- Deployment: Instructions for running the app are provided below

# Usage
I have a demo build of this application on dockerhub. There is a sqlite database in the container which is initialized with sample data
every time the container starts and is lost every time the container terminates. 

## Run on Docker

Pull the image and map localhost port 80 to container port 8000.

    - docker pull docker.io/dbrac/url_shortener:1.0
    - docker run -d -p 80:8000 docker.io/dbrac/url_shortener:1.0 


### Create and use a shortener
Open your web browser

    - Go to http://localhost
    - Create a shortener
    - Go to http://localhost/<your_shortener>

### Make it shorter

You can make this URL even shorter by adding an entry to your hosts file: 

    - 127.0.0.1 d.b

I used d.b in the application but you can make it even shorter like this:

    - 127.0.0.1 s

From your browser, go to http://d.b/<your_shortener>

### Search Shorteners

Search for shorteners from the top right of the home page. You can't search by date alone, your search must include the url, short key or tag. For demonstration purpose, all sample shorteners have an "all" tag. Enter "all" into the tags field and search.

### Update Shortener

From the search results, you can select the shortener name which will load the update view where you can update the URL of the shortener and its tags.

### Run on Kubernetes

Use the kubernetes.yaml to deploy onto kubernetes. Make sure to adjust the ingress hostname to match your environment. Check out this scripted Kubernetes cluster build if you are interested in building your own cluster: https://github.com/dbrac/k8s-cluster-build

    kubectl apply -f kubernetes.yaml

# Build

If you want to make updates to the application or rebuild the Docker image locally for any reason:

#### Docker build:

    - docker build -t <repo>/<project>:<tag>

Example using the URL shortener project:

    - docker build -t dbrac/url_shortener:1.1 .

#### Docker push

You can push the image to any container registry. You will need to replace <repo> and <project> with your own registry and project names.

Push the image to your registry:

    - docker push <repo>/<project>:<tag>

Example using the URL shortener project:

    - docker push dbrac/url_shortener:1.1

# Run locally

To run the application locally, follow these steps:


- Make sure you have Python and pip installed on your system.

- Install Python dependencies:

   ```
   pip install -r requirements.txt
   ```

- Run development web server on port 9000
    ```
    manage.py runserver 0.0.0.0:9000
    ```

- Alternatively, you can debug in VS Code using this run configuration:


    ```
    {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Python: Django",
                "type": "python",
                "request": "launch",
                "program": "${workspaceFolder}/manage.py",
                "args": [
                    "runserver",
                    "0.0.0.0:9000"
                ],
                "django": true,
                "justMyCode": false,
                "env": {
                    "PYTHONUNBUFFERED": "1"
                }
            }
        ]
    }
    ```

**Note**: This application uses SQLite for development purposes. For production environments, it is recommended to use a more scalable database like PostgreSQL or MySQL. For instructions on configuring a production-ready database, please refer to the Django documentation on database setup: https://docs.djangoproject.com/en/5.1/ref/databases/



# UI Preview

Here are some example screenshots of the user inferface:

![alt text](images/image-1.png)

![alt text](images/image-2.png)

![alt text](images/image-3.png)