from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
import numpy as np
import pandas as pd
import tempfile

from tensorflow.examples.tutorials.mnist import input_data

COLUMNS = ["flavor", "pt", "eta", "njets", "weight"]
CONTINUOUS_COLUMNS = [ "pt", "eta", "njets", "weight"]
CATEGORICAL_COLUMNS = []
LABEL_COLUMN = "label"

def input_fn(df):
  """Input builder function."""
  # Creates a dictionary mapping from each continuous feature column name (k) to
  # the values of that column stored in a constant Tensor.
  continuous_cols = {k: tf.constant(df[k].values) for k in CONTINUOUS_COLUMNS}
  # Creates a dictionary mapping from each categorical feature column name (k)
  # to the values of that column stored in a tf.SparseTensor.
  categorical_cols = {k: tf.Tensor(
      indices=[[i, 0] for i in range(df[k].size)],
      values=df[k].values,
      shape=[df[k].size, 1])
                      for k in CATEGORICAL_COLUMNS}
  # Merges the two dictionaries into one.
  feature_cols = dict(continuous_cols)
  feature_cols.update(categorical_cols)
  # Converts the label column into a constant Tensor.
  continuous_cols = {k: tf.constant(df[k].values) for k in CONTINUOUS_COLUMNS}
  # Creates a dictionary mapping from each categorical feature column name (k)
  # to the values of that column stored in a tf.SparseTensor.
  categorical_cols = {k: tf.Tensor(
    indices=[[i, 0] for i in range(df[k].size)],
    values=df[k].values,
    shape=[df[k].size, 1])
                      for k in CATEGORICAL_COLUMNS}
  # Merges the two dictionaries into one.
  feature_cols = dict(continuous_cols)
  feature_cols.update(categorical_cols)
  # Converts the label column into a constant Tensor.
  label = tf.constant(df[LABEL_COLUMN].values)
  # Returns the feature columns and the label.
  return feature_cols, label

def build_estimator(model_dir):
  pt = tf.contrib.layers.real_valued_column("pt")
  eta = tf.contrib.layers.real_valued_column("eta")
  njets = tf.contrib.layers.real_valued_column("njets")
  weight = tf.contrib.layers.real_valued_column("weight")
  
  wide_columns = [pt, eta, njets, weight]#, tf.contrib.layers.crossed_column([pt, eta], hash_bucket_size=int(1e4))]
  deep_columns = [
    pt,
    eta,
    njets,
    weight
  ]
  '''m = tf.contrib.learn.DNNLinearCombinedClassifier(
        model_dir=model_dir,
        linear_feature_columns=wide_columns,
        dnn_feature_columns=deep_columns,
        dnn_hidden_units=[100, 50])'''

  m = tf.contrib.learn.LinearClassifier(feature_columns=wide_columns)

  return m

def train_and_eval():
  df_train = pd.read_csv(
    tf.gfile.Open('tflow.txt'),
    names=COLUMNS,
    skipinitialspace=True,
    sep = " ")
  df_test = pd.read_csv(
    tf.gfile.Open('tflow.txt'),#'signal_tflow.txt'),
    names=COLUMNS,
    skipinitialspace=True,
    skiprows=1,
    sep = " ")

  #print df_train["flavor"]
  print(df_train["flavor"].apply(lambda y:  y%2).astype(int))
  df_train["label"] = (
     df_train["flavor"].apply(lambda x: x%2)).astype(int)
  df_test["label"] = (
    df_test["flavor"].apply(lambda x: x%2)).astype(int)

  model_dir = tempfile.mkdtemp() 
  print("model directory = %s" % model_dir)
  
  m = build_estimator(model_dir)
  m.fit(input_fn=lambda: input_fn(df_train), steps=200)
  results = m.evaluate(input_fn=lambda: input_fn(df_test), steps=1)
  print(results)
  for key in sorted(results):
      print("%s: %s" % (key, results[key]))
      
def main(_):
  train_and_eval()


if __name__ == "__main__":
  tf.app.run()
