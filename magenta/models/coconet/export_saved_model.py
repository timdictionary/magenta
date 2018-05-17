"""Command line utility for exporting Coconet to SavedModel."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
# internal imports
import tensorflow as tf

from magenta.models.coconet import lib_graph
from magenta.models.coconet import lib_saved_model
from magenta.models.coconet import lib_tfsampling


FLAGS = tf.app.flags.FLAGS
flags = tf.app.flags
flags.DEFINE_string('checkpoint', None,
                    'Path to the checkpoint to export.')
flags.DEFINE_string('destination', None,
                    'Path to export SavedModel.')
flags.DEFINE_bool('use_tf_sampling', True,
                  'Whether to export with sampling in a TF while loop.')


def main(unused_argv):
  if FLAGS.checkpoint is None or not FLAGS.checkpoint:
    raise ValueError(
        'Need to provide a path to checkpoint directory.')
  if FLAGS.destination is None or not FLAGS.destination:
    raise ValueError(
        'Need to provide a destination directory for the SavedModel.')
  model = None
  if FLAGS.use_tf_sampling:
    model = lib_tfsampling.CoconetSampleGraph(FLAGS.checkpoint)
    model.instantiate_sess_and_restore_checkpoint()
  else:
    model = lib_graph.load_checkpoint(FLAGS.checkpoint)
  tf.logging.info('Loaded graph.')
  lib_saved_model.export_saved_model(model, FLAGS.destination,
                                     [tf.saved_model.tag_constants.SERVING],
                                     FLAGS.use_tf_sampling)
  tf.logging.info('Exported SavedModel to %s.', FLAGS.destination)


if __name__ == '__main__':
  tf.app.run()
