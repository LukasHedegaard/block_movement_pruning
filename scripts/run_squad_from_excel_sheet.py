import os
import subprocess
from hparams.parse_hparams import parse_excel_hparams
import math
from pathlib import Path


def flatten_list(original_list):
    return [element for sublist in original_list for element in sublist]


def try_int(val):
    if isinstance(val, float) and val.is_integer():
        return int(val)
    return val


if __name__ == "__main__":
    df = parse_excel_hparams(
        sheet_name="Details - SQuAD", remove_distil=True, remove_global=True
    )

    logs_dir = Path("wandb")
    logs_dir.mkdir(parents=True, exist_ok=True)

    processes = []
    for i, row in df.iterrows():
        identifier = f"{row['EXP ID']}_{row['Effective encoder remain weights %']:.1f}%"

        # Select a particular run based on its id here:
        if row["Marker"] != "*":
            # if identifier not in {
            #     # Corresponds to row 5 in /hparams/hyperparameters.xlsx sheet "Details - SQuAD"
            #     "l0_1.0_1.0_1_1_l0_*._3e-5_1e-1_l0_constant_2.197_10_epoch_0.1%",
            #     "topK_1.0_*_1_2_null_0._3e-5_1e-2_topK_constant_0._10_epochs_0.3%",
            #     "topK_1.0_*_1_2_null_0._3e-5_1e-2_topK_constant_0._10_epochs_0.1%",
            #     "l1_0._0.1_1_2_l1_*_3e-5_1e-2_sigmoied_threshold_constant_0._10_epochs_0.1%",
            # }:
            # print(f"Skipping run {i}: {identifier}")
            continue
        else:
            row["Marker"] = float("nan")

        print(f"Spawning run {i}: {identifier}")
        command = [
            "python",
            "block_movement_pruning/masked_run_squad.py",
            "--identifier",
            identifier,
            "--overwrite_output_dir",
            "--output_dir",
            "runs/",
            "--data_dir",
            "squad_data",
            "--train_file",
            "train-v1.1.json",
            "--predict_file",
            "dev-v1.1.json",
            "--do_train",
            "--do_eval",
            "--do_lower_case",
            "--model_type",
            "masked_bert",
            "--model_name_or_path",
            "bert-base-uncased",
            "--mask_block_rows",
            "32",
            "--mask_block_cols",
            "32",
            "--splopa_prototypes_not_shared",
            *flatten_list(
                [
                    (f"--{k}", str(try_int(v)))
                    for k, v in row[5:].to_dict().items()
                    if isinstance(v, str) or not math.isnan(v)
                ]
            ),
        ]

        fpath = logs_dir / f"{identifier}.txt"
        if fpath.exists():
            os.remove(fpath)

        f = open(str(fpath), "a")
        f.write("******* Command: *******\n")
        f.write(" ".join(command))
        f.write("\n************************\n")

        print(command)
        # processes.append((subprocess.Popen(command, stdout=f), f))
        subprocess.call(command, stdout=f)

    for (p, f) in processes:
        p.wait()
        f.close()
