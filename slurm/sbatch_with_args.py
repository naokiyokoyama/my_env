import argparse
import itertools
import os.path as osp

from sbatch_glob import sbatch_all


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("sbatch_file")
    parser.add_argument("parameters", nargs="+")
    parser.add_argument("-g", "--generate-only", action="store_true")
    parser.add_argument("-t", "--template-name")
    args = parser.parse_args()
    run(**vars(args))


def run(
    sbatch_file,
    parameters,
    generate_only=False,
    template_name=None,
):
    assert osp.isfile(sbatch_file), f"{sbatch_file} does not exist!"
    if template_name is not None:
        assert template_name.endswith(".sh")

    # Get data from template slurm file
    with open(sbatch_file) as f:
        template_data = f.read()

    # Get every possible permutation of values to sweep over
    permutations = itertools.product(*[i.split(",") for i in parameters])
    sbatch_files = []
    for p_idx, p in enumerate(permutations):
        print("permutation: ", p)
        # Generate name for new file
        if template_name is None:
            out_name = sbatch_file.replace(".sh", "_" + "_".join(p) + ".sh")
        else:
            out_name = template_name
            for idx, arg in enumerate(p):
                out_name = out_name.replace(f"${idx + 1}", arg)

        # Fill in $ values in template with permutation, where $0 is the name of the
        # file being generated with no extension
        data = template_data
        out_name_no_ext, _ = osp.splitext(out_name)
        out_name_no_ext = osp.basename(out_name_no_ext)
        for idx, arg in enumerate([out_name_no_ext] + p):
            data = data.replace(f"${idx}", arg)

        with open(out_name, "w") as f:
            f.write(data)

        # Queue file for execution
        sbatch_files.append(out_name)

    if not generate_only:
        sbatch_all(sbatch_files)


if __name__ == "__main__":
    main()
