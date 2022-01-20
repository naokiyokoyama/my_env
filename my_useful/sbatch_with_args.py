import subprocess
import sys
import os
import itertools

sbatch_file = sys.argv[1]
args = sys.argv[2:]

dont_save = False
if '-d' in args:
    args.pop(args.index('-d'))
    dont_save = True
dont_run = False
if '-r' in args:
    args.pop(args.index('-r'))
    dont_run = True

template_name = None
if '-t' in args:
    idx = args.index('-t')
    for _ in range(2):
        template_name = args.pop(idx)
    assert template_name.endswith('.sh')

# Get template data
with open(sbatch_file) as f:
    template_data = f.read()

# Get every possible permutation of values to sweep over
permutations = itertools.product(
    *[i.split(',') for i in args]
)
for p in permutations:
    # Fill in template with permutation
    data = template_data
    for idx, arg in enumerate(p):
        data = data.replace(f'${idx+1}', arg)

    # Create and delete a temporary file
    if template_name is None:
        temp_file = sbatch_file.replace('.sh', '_'+'_'.join(p)+'.sh')
    else:
        temp_file = template_name
        for idx, arg in enumerate(p):
            temp_file = temp_file.replace(f'${idx+1}', arg)

    with open(temp_file, 'w') as f:
        f.write(data)
    try:
        print('permutation: ', p)
        if not dont_run:
            print('Running: sbatch', temp_file)
            subprocess.check_call(['sbatch', temp_file])
        print('')
    except:
        print('sbatch failed!!')

    if dont_save:
        os.remove(temp_file)
