import os
import csv
import sys
import time
import glob
import numpy as np
import tensorflow as tf

def process_images(images,
                   graph,
                   output_operation,
                   input_operation,
                   input_height,
                   input_width,
                   input_mean,
                   input_std):
  results = []
  total = len(images)
  tf.reset_default_graph()
  tensors, fails = read_tensor_batch(images,
                                     input_height=input_height,
                                     input_width=input_width,
                                     input_mean=input_mean,
                                     input_std=input_std)
  if not tensors:
    return [], fails
  tf.reset_default_graph()
  with tf.Graph().as_default(), tf.Session(graph=graph) as sess:
    # avoid creating unnecessary nodes in the graph
    out = output_operation.outputs[0]
    in_ = input_operation.outputs[0]
    for i, (t, file_name) in enumerate(zip(tensors, images)):
      res = sess.run(out, {in_: t})
      results.append((file_name, res))
    return [(f, np.squeeze(r)) for f,r in results], fails

def read_tensor_batch(image_names, input_height=299, input_width=299,
		      input_mean=0, input_std=255):
  def _get_normalized(file_name):
    input_name = "file_reader"
    output_name = "normalized"
    file_reader = tf.read_file(file_name, input_name)
    if file_name.endswith(".png"):
      image_reader = tf.image.decode_png(file_reader, channels = 3,
                                         name='png_reader')
    elif file_name.endswith(".gif"):
      image_reader = tf.squeeze(tf.image.decode_gif(file_reader,
                                                    name='gif_reader'))
    elif file_name.endswith(".bmp"):
      image_reader = tf.image.decode_bmp(file_reader, name='bmp_reader')
    else:
      image_reader = tf.image.decode_jpeg(file_reader, channels = 3,
                                          name='jpeg_reader')
    float_caster = tf.cast(image_reader, tf.float32)
    dims_expander = tf.expand_dims(float_caster, 0);
    resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
    normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
    return normalized

  sess = tf.Session()
  try:
    normalized = []
    failures = []
    for x in image_names:
      try:
        normalized.append(_get_normalized(x))
      except:
        failures.append(x)
    result = sess.run(normalized)
  except Exception as e:
    result = []
    failures = image_names
  return result, failures

def load_graph(model_file):
  graph = tf.Graph()
  graph_def = tf.GraphDef()

  with open(model_file, "rb") as f:
    graph_def.ParseFromString(f.read())
  with graph.as_default():
    tf.import_graph_def(graph_def)
  return graph

def load_labels(label_file):
  label = []
  proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
  for l in proto_as_ascii_lines:
    label.append(l.rstrip())
  return label

input_height = 299
input_width = 299
input_mean = 0
input_std = 255
input_layer = "Mul"
output_layer = "final_result"
input_operation = lambda g, i_name: g.get_operation_by_name(i_name)
output_operation = lambda g, o_name: g.get_operation_by_name(o_name)
input_name = "import/" + input_layer
output_name = "import/" + output_layer

if __name__ == '__main__':
  print("Import this module")

