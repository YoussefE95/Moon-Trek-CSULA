FROM continuumio/miniconda3

# setup enviroments
RUN apt update -y && apt upgrade -y && \
    apt install -y tzdata nodejs npm

# setup working dir & copy source code
WORKDIR /src/
COPY . .

# setup conda & build
SHELL ["/bin/bash", "--login", "-c"]
RUN conda env create -f environment.yml && \
    conda init bash && \
    conda activate MoonTrek && \
    npm install


# dev deploy
# ENTRYPOINT ["npm", "run", "dev"]
# production deploy
ENTRYPOINT ["node", "server.js"]

EXPOSE 8888