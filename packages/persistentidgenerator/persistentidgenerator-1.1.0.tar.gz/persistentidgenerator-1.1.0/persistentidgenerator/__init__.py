# Copyright (c) 2024 email@debmishra.me
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

# -----------------------------Program to generate sequential ids ---------------
import os

# Create variables that can be used across the module
domainSet = {
    "fx": 1,
    "hp": 2,
    "sec": 3,
    "idx": 4,
    "bmrk": 5,
    "hld": 6,
    "por": 7,
    "ent": 8,
    "oth": 0,
}
defLoc = "./"
dbPath = os.getenv("SLITE_DB_PATH")
createQuery = """CREATE TABLE IF NOT EXISTS savedID (
    category VARCHAR(20) PRIMARY KEY UNIQUE,
    last_value BIGINT)"""
droppedQuery = """CREATE TABLE IF NOT EXISTS droppedID (
    id INTEGER PRIMARY KEY,
    category VARCHAR(20),
    dropped_value BIGINT)"""
tableList = {"savedID": createQuery, "droppedID": droppedQuery}
squerySavedID = "select last_value from savedID where category=?"
uquerySavedID = "update savedID set last_value = ? where category=?"
iquerySavedID = "insert into savedID (category, last_value) values (?,?)"
iquerydroppedID = "insert into droppedID (category, dropped_value) values (?,?)"
squerydroppedIDs = "select last_value from savedID where category=?"
squerydroppedIDt = "select 1 from droppedID where category=? and dropped_value=?"
