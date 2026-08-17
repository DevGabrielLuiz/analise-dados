from pathlib import Path
import pandas as pd

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"


def load_hybrid_sales() -> pd.DataFrame:
    path = RAW_DIR / "hybrid_sales.csv"
    df = pd.read_csv(path)
    expected_cols = {"mes", "marca", "unidades"}
    assert set(df.columns) == expected_cols, f"Colunas inesperadas: {set(df.columns)}"
    return df


def load_market_share() -> pd.DataFrame:
    path = RAW_DIR / "market_share.csv"
    df = pd.read_csv(path)
    expected_cols = {"mes", "grupo", "participacao_pct"}
    assert set(df.columns) == expected_cols, f"Colunas inesperadas: {set(df.columns)}"
    return df


if __name__ == "__main__":
    hybrids = load_hybrid_sales()
    market = load_market_share()
    print("Híbridos:")
    print(hybrids)
    print("\nMarket Share:")
    print(market)