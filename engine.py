from data.loader import DataLoader
from core.pipeline import Pipeline


def main():

    print("\n[V3.5 CONSOLIDATED ENGINE]\n")

    # 1. load data
    loader = DataLoader()
    matches = loader.load()

    print(f"[DATA] loaded matches: {len(matches)}")

    # 2. init pipeline
    pipe = Pipeline()

    # 3. train
    pipe.train(matches)
    print("[TRAIN] completed")

    # 4. predict sample
    sample = matches[0]
    pred = pipe.predict(sample["home"], sample["away"], sample["odds"])

    print("\n[PREDICTION SAMPLE]")
    print(sample["home"], "vs", sample["away"])
    print(pred)


if __name__ == "__main__":
    main()
