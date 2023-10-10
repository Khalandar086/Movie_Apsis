



Create Table actors(
id serial unique,
first_name varchar(225),
last_name varchar(225),
industry varchar(225),
gender  varchar(225),
dob date
);


Create Table movies
(id serial unique,
name varchar(225),
director varchar(225),
languages varchar(225),
production  varchar(225),
rating real
);


Create Table movieactors
(
movie_id int references movies(id),
actors_id int references actors(id)
);
