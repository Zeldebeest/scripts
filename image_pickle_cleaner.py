""" this script will take an image pickle and multiply the sigma values in the miller array by the gain """


def run(files, gain, prefix):
  from libtbx import easy_pickle
  for file in files:
    f = easy_pickle.load(file)
    old_miller = f['observations'][0]
    new_miller = old_miller.customized_copy(sigmas=gain * old_miller.sigmas())
    f['observations'][0] = new_miller
    easy_pickle.dump(prefix + file, f)

if __name__ == "__main__":
  import argparse
  parser = argparse.ArgumentParser("Modify experimenatal sigmas by a constant factor")
  parser.add_argument('files', type=str, nargs='+',
      help="Names of pickles to modify.")
  parser.add_argument('gain', type=float,
      help="Factor by which to multiply sigmas.")
  parser.add_argument('--prefix', '-p', default='mod-', type=str,
      help="Optional prefix for output pickles. Leave blank to overwrite files.")
  args = parser.parse_args()
  run(args.files, args.gain, args.prefix)
