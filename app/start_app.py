import argparse
from pathlib import Path

from config import AppConfig
from port.adapter.sagemaker import train, serve


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", type=str)
    parser.add_argument("--local", action="store_true")
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()

    if args.local:
        dataset_path = Path("../data/dataset/")
        artifact_path = Path("../data/artifacts/")
    else:
        dataset_path = Path("/opt/ml/input/data/training/")
        artifact_path = Path("/opt/ml/model/")

    AppConfig.instance(args.local, artifact_path)

    if args.command == "train":
        train.run(dataset_path, artifact_path)
    elif args.command == "serve":
        serve.run(args.host, args.port)
    else:
        raise ValueError(f"invalid command: {args.command}")


if __name__ == "__main__":
    main()
