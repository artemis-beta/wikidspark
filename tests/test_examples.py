import subprocess
import glob
import os

def test_examples():
    loc_dir = os.path.realpath(__file__).replace(os.path.basename(__file__), '')
    examples = glob.glob(os.path.join(loc_dir, '..', 'examples', '*.py'))
    for ex in examples:
        assert not subprocess.check_call(f'python {ex}', shell=True)
