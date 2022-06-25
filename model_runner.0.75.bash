#!/bin/bash

INTERACTANTS=3
N=4096
MAX_STEPS=100
ENSEMBLE_SIZE=50
INITIAL_MAG=0.5
DB_NAME="csssa2022.db"
LOG_FILE="log.txt"

# Run all combinations of models with a single database

python main.py matrix   dyn     l2dr    $INTERACTANTS $N $MAX_STEPS $ENSEMBLE_SIZE $INITIAL_MAG $DB_NAME
python main.py matrix   dyn     hc      $INTERACTANTS $N $MAX_STEPS $ENSEMBLE_SIZE $INITIAL_MAG $DB_NAME
python main.py matrix   dyn     pl      $INTERACTANTS $N $MAX_STEPS $ENSEMBLE_SIZE $INITIAL_MAG $DB_NAME
python main.py matrix   dyn     er      $INTERACTANTS $N $MAX_STEPS $ENSEMBLE_SIZE $INITIAL_MAG $DB_NAME

python main.py matrix   hord    l2dr    $INTERACTANTS $N $MAX_STEPS $ENSEMBLE_SIZE $INITIAL_MAG $DB_NAME
python main.py matrix   hord    hc      $INTERACTANTS $N $MAX_STEPS $ENSEMBLE_SIZE $INITIAL_MAG $DB_NAME
python main.py matrix   hord    pl      $INTERACTANTS $N $MAX_STEPS $ENSEMBLE_SIZE $INITIAL_MAG $DB_NAME
python main.py matrix   hord    er      $INTERACTANTS $N $MAX_STEPS $ENSEMBLE_SIZE $INITIAL_MAG $DB_NAME
 
python main.py abm      dyn     l2dr    $INTERACTANTS $N $MAX_STEPS $ENSEMBLE_SIZE $INITIAL_MAG $DB_NAME
python main.py abm      dyn     hc      $INTERACTANTS $N $MAX_STEPS $ENSEMBLE_SIZE $INITIAL_MAG $DB_NAME
python main.py abm      dyn     pl      $INTERACTANTS $N $MAX_STEPS $ENSEMBLE_SIZE $INITIAL_MAG $DB_NAME
python main.py abm      dyn     er      $INTERACTANTS $N $MAX_STEPS $ENSEMBLE_SIZE $INITIAL_MAG $DB_NAME

python main.py abm      hord    l2dr    $INTERACTANTS $N $MAX_STEPS $ENSEMBLE_SIZE $INITIAL_MAG $DB_NAME
python main.py abm      hord    hc      $INTERACTANTS $N $MAX_STEPS $ENSEMBLE_SIZE $INITIAL_MAG $DB_NAME
python main.py abm      hord    pl      $INTERACTANTS $N $MAX_STEPS $ENSEMBLE_SIZE $INITIAL_MAG $DB_NAME
python main.py abm      hord    el      $INTERACTANTS $N $MAX_STEPS $ENSEMBLE_SIZE $INITIAL_MAG $DB_NAME

