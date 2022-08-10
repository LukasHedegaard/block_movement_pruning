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
    df = parse_excel_hparams(sheet_name="Details - SQuAD")

    logs_dir = Path("remote/scripts/logs/baselines")
    logs_dir.mkdir(parents=True, exist_ok=True)

    processes = []
    for i, row in df.iterrows():
        identifier = f"{row['EXP ID']}_{row['Effective encoder remain weights %']:.2f}%"
        # if row["Effective encoder remain weights %"] <= 100:
        #     continue

        if identifier not in {
            #     # "l1_0._0.1_1_2_l1_*_3e-5_1e-2_sigmoied_threshold_constant_0._10_epochs_93.64%",
            #     # "l1_0._0.1_1_2_l1_*_3e-5_1e-2_sigmoied_threshold_constant_0._10_epochs_13.87%",
            "magnitude_1.0_*_1_2_null_0._3e-5_0._magnitude_null_0._10_epochs_60.10%"
        }:
            # if "magnitude" not in identifier:
            continue
        print(f"Spawning run {i}: {identifier}")
        # continue
        command = [
            "python",
            "block_movement_pruning/masked_run_squad.py",
            # "remote/scripts/run_squad.py",
            "--identifier",
            identifier,
            "--overwrite_output_dir",
            "--output_dir",
            "runs/squad-bert-base-uncased-finetuned",
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

        processes.append((subprocess.Popen(command, stdout=f), f))

    for (p, f) in processes:
        p.wait()
        f.close()