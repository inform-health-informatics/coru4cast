## Notes

Getting started
Open sublime
3 pane layout
Use ipython after activating pipenv 


```sh
pipenv shell
ipython
```

## Todos

- [ ] @TODO: (2018-12-07)  set up method to dockerise a notebook; plan to use a dockerised notebook environment to manage python dependencies


## Log

### 2018-12-07
git init
pipenv shell


### 2018-12-06
created folder on GAE with relevant structure, data and docs


# Scratch

to work here then simply run from the terminal at the project root

```
docker run -p 8888:8888 jupyter/datascience-notebook
```

then copy-paste the url and token into your local browser

e.g.

```
http://172.16.149.155:8888/?token=fbb75b7f44cdbfb28fcdf8ec54f7a9c5c4b9ea8f36f40a2b
```

which will then sign you in and navigate you to

```
http://172.16.149.155:8888/tree/work
```

- TODO: having problems with mounting the correct directory

