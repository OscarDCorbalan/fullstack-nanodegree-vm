**TODO**: project indexed links
**TODO**: merge restaurants README file here

# Tournament Planner

_This project is part of Udacity's Full Stack Developer Nanodegree._

This project consists in implementing a **Python** module that uses a **PostgreSQL** database to keep track of players and matches in a game tournament, having two parts:
  * (**tournament.sql**) Defining the database schema (SQL table definitions).
  * (**tournament.py** ) Writing the code that will use it.
  * (**tournament_test.py**) Writing tests for the code in tournament.py.

Note that a TDD (Test-Driven Development) approach is used. The tests are located in **tournament_test.sql**.

The game tournament uses the Swiss system for pairing up players in each round: players are not eliminated, and each player should be paired with another player with the same number of wins, or as close as possible.

# How to run the project

To run the project tests, follow these steps:

1. Install [Vagrant](https://docs.vagrantup.com/v2/installation/)  if you don't have it already.
2. Grab a copy of the project. You can either:
  * Clone the repo with git: `git clone https://github.com/OscarDoc/fullstack-nanodegree-vm.git`.
  * [Clone with GitHub Desktop](github-windows://openRepo/https://github.com/OscarDoc/fullstack-nanodegree-vm).
  * [Download the latest release](https://github.com/OscarDoc/fullstack-nanodegree-vm/archive/master.zip)
3. Open a command-line window and go to the /vagrant folder of the project.
4. Once in it, run `vagrant up`. That will load the Virtual Machine, which has Python and PostgreSQL installed.
5. SSH into the machine with the username `vagrant`. Depending on your OS:
  * **NOT** Windows: just run `vagrant ssh`.
  * Windows: Running `vagrant ssh` will mourn that it's not possible and provide you an IP/port to log in. So, to log in, download [PuTTY](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html) and follow the instructions [found here](https://github.com/Varying-Vagrant-Vagrants/VVV/wiki/Connect-to-Your-Vagrant-Virtual-Machine-with-PuTTY), which basically explain how to use the Vagrant VM certificate in PuTTY.
6. Once inside the VM, run `cd /vagrant/tournament`.
7. Once inside the folder:
  * Run `psql` to go into PostgreSQL.
  * In there, run `\i tournament.sql` to create the DB.
  * Then run `\q` to go back to the shell.
8. Run `python tournament_test.py`

# What's included

Within the download you'll find the following directories and files, logically grouping common assets. You'll see something like this:
```
├── vagrant/  
│   ├── tournament/             Tournament Planner
│   │   ├──tournament_test.py   Automated tests  
│   │   ├──tournament.py        Code  
│   │   └──tournament.sql       Definition of the DB  
│   ├── Vagrantfile             Virtual machine configuration  
│   └── pg_config.sh  
└── README.md                   This file  
```

# Test cases (strikethrough means implemented)

1. ~~Old matches can be deleted.~~
2. ~~Player records can be deleted.~~
3. ~~After deleting, countPlayers() returns zero.~~
4. ~~After registering a player, countPlayers() returns 1.~~
5. ~~Players can be registered and deleted.~~
6. ~~Newly registered players appear in the standings with no matches.~~
7. ~~After a match, players have updated standings.~~
8. ~~After one match, players with one win are paired.~~
9. ~~Prevent rematches between players.~~
10. ~~Don’t assume an even number of players. If there is an odd number of players, assign one player a “bye” (skipped round). A bye counts as a free win. A player should not receive more than one bye in a tournament.~~
11. ~~Support games where a draw (tied game) is possible. This will require changing the arguments to reportMatch.~~
12. ~~When two players have the same number of wins, rank them according to OMW (Opponent Match Wins), the total number of wins by players they have played against.~~
13. ~~Support more than one tournament in the database, so matches do not have to be deleted between tournaments. This will require distinguishing between “a registered player” and “a player who has entered in tournament #123”, so it will require changes to the database schema.~~
