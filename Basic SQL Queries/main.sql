.header ON
.mode column

CREATE TABLE pet (name VARCHAR(20), owner VARCHAR(20), species
VARCHAR(20), sex CHAR(1), checkups SMALLINT UNSIGNED, birth DATE,
death DATE);

INSERT INTO pet (name,owner,species,sex,checkups,birth,death)VALUES
('Fluffy','Harold','cat','f',5,'2001-02-04',''),
('Claws','Gwen','cat','m',2,'2000-03-17',''),
('Buffy','Harold','dog','f',7,'1999-05-13',''),
('Fang','Benny','dog','m',4,'2000-08-27',''),
('Bowser','Diane','dog','m',8,'1998-08-31','2001-07-29'),
('Chirpy','Gwen','bird','f',0,'2002-09-11',''),
('Whistler','Gwen','bird','',1,'2001-12-09',''),
('Slim','Benny','snake','m',5,'2001-04-29','');

.print "Databases Lab 1 - Introduction to SQL"
.print
.print "Q1-1: The names of owners and their pet's name for all pets who are female"
SELECT name, owner FROM pet WHERE sex = 'f' ORDER BY name;

.print
.print "Q1-2: The names and birth dates of pets which are dogs"
SELECT name, birth FROM pet WHERE species = 'dog' ORDER BY name;

.print
.print "Q1-3: The names of the owners of birds"
SELECT DISTINCT owner FROM pet WHERE species = 'bird' ORDER BY owner;

.print
.print "Q1-4: The species of pets who are female"
SELECT species FROM pet WHERE sex = 'f' ORDER BY species;

.print
.print "Q1-5: The names and birth dates of pets which are cats or birds"
SELECT name, birth FROM pet WHERE species = 'cat' OR species = 'bird' ORDER BY name;

.print
.print "Q1-6: The names and species of pets which are cats or birds and which are female"
SELECT name, species FROM pet WHERE (species = 'cat' OR species = 'bird') AND sex = 'f' ORDER BY name;

.print
.print "Q2-1: The names of owners and their pets where the pet's name ends with “er” or “all”"
SELECT name, owner FROM pet WHERE name LIKE '%er' OR name LIKE '%all' ORDER BY name;

.print
.print "Q2-2: The names of any pets whose owner's name contains an “e”"
SELECT name FROM pet WHERE owner LIKE '%e%' ORDER BY name;

.print
.print "Q2-3: The names of all pets whose name does not end with “fy”"
SELECT name FROM pet WHERE name NOT LIKE '%fy' ORDER BY name;

.print
.print "Q2-4: All pet names whose owners name is only four characters long"
SELECT name FROM pet WHERE owner LIKE '____' ORDER BY name;

.print
.print "Q2-5: All owners whose names begin and end with one of the first five letters of the alphabet"
SELECT DISTINCT owner FROM pet WHERE owner GLOB '[A-E]*[a-e]' ORDER By owner;

.print
.print "Q3-1: The average number of check-ups that each owner has made with their pets"
SELECT owner, AVG(checkups) AS AverageCheckups FROM pet GROUP BY owner ORDER BY owner;

.print
.print "Q3-2: The number of pets of each species in ascending order"
SELECT species, COUNT(species) AS NumOfSpecies FROM pet GROUP BY species ORDER BY NumOfSpecies;

.print
.print "Q3-3: The number of pets of each species that each owner has"
SELECT owner, species, COUNT(species) AS NumOfEachSpecies FROM pet GROUP BY species, owner ORDER BY owner;

.print
.print "Q3-4: The number of distinct species of pet each owner has"
SELECT owner, COUNT(DISTINCT species) AS NumOfDistinctSpecies FROM pet GROUP BY owner ORDER BY owner;

.print
.print "Q3-5: The number of pets of each gender there are in the database, where the gender is known"
SELECT sex, COUNT(sex) AS NumOfEachSex FROM pet WHERE sex <> '' GROUP BY sex ORDER BY sex;

.print
.print "Q3-6: The number of birds each owner has"
SELECT owner, COUNT(species) AS NumOfBirds FROM pet WHERE species = 'bird' GROUP BY owner ORDER BY owner;

.print
.print "Q3-7: The total number of check-ups each owner has made with all their pets"
SELECT owner, SUM(checkups) AS TotalCheckups FROM pet GROUP BY owner ORDER BY owner;