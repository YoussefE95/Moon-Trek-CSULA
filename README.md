# Moon Trek CSULA

## Install:

1. Download [NodeJs](https://nodejs.org/en/download/) and [Anaconda](https://www.anaconda.com/). Make sure to add conda to your path when installing on Windows (it will ask)

2. Set up MoonTrek anaconda environment. In your terminal, run the following commands:

    ```
    conda create --name MoonTrek
    conda activate MoonTrek
    conda install python=3.7.9 django=3.1.7 numpy=1.20.1 opencv pillow=8.1.2 pytz=2021.1 sqlparse=0.4.1
    python -m pip install opencv-contrib-python==3.4.2.17
    ```

3. Clone this repository

4. Install dependencies. In a terminal, navigate to the base directory and run these commands:

    ```
    cd client
    npm install
    cd ../server
    npm install
    ```

5. Create a file called 'config.json' with the same contents of 'sample.config.json' in the server/api/jpl directory. Assuming you're still in the server directory from last step, run the following command:

    ```
    cp api/jpl/sample.config.json api/jpl/config.json
    ```

    Note: The IP and port are available only to developers for security purposes

6. To run, we need two terminal instances. In one cd to the client directory and run:
    ```
    npm run dev
    ```
    In the other one, cd to the server directory and run:
    ```
    npm run dev
    ```
