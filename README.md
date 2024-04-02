# library_ms
Web application to track books present in the library.

# Steps to run application on your local [Using Docker]

1. Build docker image using Dockerfile. `library-ms` is image name.
   ```
   sudo docker build . -t library-ms
   ```
2. Verify if the image has been successfully built. Below command lists all the images available on docker host.
   ```
   sudo docker images
   ```
3. Run the docker compose file. Docker compose file uses the image we built in the previous step.
   ```
   sudo docker-compose up
   ```
4. Run `sudo docker ps` and copy the container ID of the library app.
5. Run the following command to access the container shell.
   ```
   sudo docker exec -it <container ID> /bin/bash
   ```
6. Once you are inside the folder /opt/app/. Run the command to create database tables.
   ```
   flask db upgrade
   ```
7. On the terminal where you have run docker compose up it will show you the IP on which application can be accessed.
5. Open the IP in your browser. To access the web application.

### Command to make the stored data persistent. [DB used currently is SQLite]

```
sudo docker run -dp 127.0.0.1:5000:5000 --name=library-app --mount type=volume,src=library-db,target=/opt/app/ library-ms
```

**Home Screen**
![Screenshot from 2024-03-26 21-19-08](https://github.com/mridubhatnagar/library_ms/assets/16894718/c9f4e273-20f5-490e-9875-da0f98a2df0b)

**Books Page**
![Screenshot from 2024-03-26 21-20-30](https://github.com/mridubhatnagar/library_ms/assets/16894718/57718dc1-7e7a-414c-8df8-b4bea1e66ddf)

**Add Books Page**
![Screenshot from 2024-03-26 21-23-15](https://github.com/mridubhatnagar/library_ms/assets/16894718/d79f583f-4393-4e82-bcd4-d8758d0e7651)

**Search Books Page**
![Screenshot from 2024-03-26 21-24-51](https://github.com/mridubhatnagar/library_ms/assets/16894718/5ffc3a42-f96f-49e7-821e-f27ec9a79e25)

**Members Page**
![Screenshot from 2024-03-26 21-25-32](https://github.com/mridubhatnagar/library_ms/assets/16894718/a140b8c4-326a-4501-a47d-30ab9a5fc4b0)

**Member Details Page**
![Screenshot from 2024-03-26 21-26-12](https://github.com/mridubhatnagar/library_ms/assets/16894718/5b642ff0-166b-4b78-a278-583b26cdfbe9)

**NOTE**
App contains of some more pages like Book Details Page, Issue Book, Return Book, Payment Details, Make Payments etc pages. Screenshot of all the pages is not added here.
