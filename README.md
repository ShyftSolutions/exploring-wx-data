# exploring-wx-data
Project overview and getting started for our "Exploring Weather Data in Python" workshop

# Getting Started
To start up your JupyterLab Notebook, simply open a terminal and navigate to this project and run:
`docker-compose up`

After Docker copmletes the build and installation, your JupyterLab session will be running at https://localhost:8888. You can navigate there in your browser and you should be prompted for a token, in your terminal where you ran the docker compose file there should be output that tells you what the token is at the end of the URL after `token=`

```
jupyter_1  | [I 2022-07-12 13:36:12.945 ServerApp] Serving notebooks from local directory: /opt/app/data
jupyter_1  | [I 2022-07-12 13:36:12.945 ServerApp] Jupyter Server 1.17.1 is running at:
jupyter_1  | [I 2022-07-12 13:36:12.945 ServerApp] http://95a73153bcc0:8888/lab?token=025ece74fd60a35a87fd88360329ae77ee34dcb742c30786
jupyter_1  | [I 2022-07-12 13:36:12.945 ServerApp]  or http://127.0.0.1:8888/lab?token=025ece74fd60a35a87fd88360329ae77ee34dcb742c30786
jupyter_1  | [I 2022-07-12 13:36:12.945 ServerApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
jupyter_1  | [C 2022-07-12 13:36:12.951 ServerApp] 
jupyter_1  |     
jupyter_1  |     To access the server, open this file in a browser:
jupyter_1  |         file:///home/jovyan/.local/share/jupyter/runtime/jpserver-7-open.html
jupyter_1  |     Or copy and paste one of these URLs:
jupyter_1  |         http://95a73153bcc0:8888/lab?token=025ece74fd60a35a87fd88360329ae77ee34dcb742c30786
jupyter_1  |      or http://127.0.0.1:8888/lab?token=025ece74fd60a35a87fd88360329ae77ee34dcb742c30786
```

# Course Material
### [Types of Weather Data](WxData.md)
### [Reference Material](References.md)