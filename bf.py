import tensorflow as tf
import numpy as np
import pandas as pd

from tensorflow.examples.tutorials.mnist import input_data

input = open("tflow.txt", "r")
signal = open("signal_tflow.txt", "r")

flavor = []
pt = []
eta = []
njets = []
bs = 0
ls = 0

COLUMNS = ["flavor", "pt", "eta", "njets"]

for line in input:
    words = line.split()
    
    if words[0] == "5":
        flavor.append(1)
        bs+=1
    else:
        flavor.append(0)
        ls+=1
    pt.append(float(words[1]))
    eta.append(float(words[2]))
    njets.append(float(words[3]))

print bs
print ls

sflavor = []
spt = []
seta = []
snjets = []

for line in input:
    if line[0] == "5":
        sflavor.append(1)
        bs+=1
    else:
        sflavor.append(0)
        ls+=1
    spt.append(line[1])
    seta.append(line[2])
    snjets.append(line[3])

df_train = pd.read_csv(
    tf.gfile.Open('tflow.txt'),
    names=COLUMNS,
    skipinitialspace=True)
df_test = pd.read_csv(
    tf.gfile.Open('signal_tflow.txt'),
    names=COLUMNS,
    skipinitialspace=True,
    skiprows=1)
