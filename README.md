# Web Files

A simple web based file manager. Browse, create, and delete files within a given web root directory.

## About

This is a project that I've only worked on for fun. It's public because I like to share what I've learned and built with others.

Maybe you'll:
* Find it to be a useful example of a simple flask application to borrow bits and pieces from
* Run it on your home web server as an alternative to ssh/ftp
* Fork the repository as the base of your own application
* Be checking out my programming style after seeing the repository on my resume as an example of work

Regardless of your use case, please recognize that this is a project that I've only worked on for fun, and only intend to work on for fun. I accept no liability as relates to your usage of the code in this project, and I provide no support for it aside from what is written within the code and this documentation.

## Requirements

* [Docker Engine](https://docs.docker.com/engine/)
* [Docker Compose](https://docs.docker.com/compose/)
* Internet connectivity
* Files in a directory mounted on the system the docker container runs on as a web root
* Motivation to try it out

## Usage

Review the scripts (`*.sh`) and docker compose (`dev.yml`) files in the `dockers` directory. Use the scripts for convenience during development in an environment that you trust. Copy the `dev.yml` file and modify it for use in less trusted environments. Really consider implementing authentication if you'd like to run the app on an untrusted/unsecured network.

Once the application is running, just connect to its address and port in your web browser.
