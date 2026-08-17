from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

FIGS_DIR = Path(__file__).parent.parent / "outputs" / "figures"
FIGS_DIR.mkdir(parents=True, exist_ok=True)


def _fmt_month(ax, dates):
    """Formata eixo X com labels 'Mês/Ano' a partir de datetime index."""
    labels = [d.strftime("%b/%y").capitalize() for d in dates]
    ax.set_xticks(range(len(dates)))
    ax.set_xticklabels(labels, rotation=0)


def plot_hybrid_sales(df: pd.DataFrame) -> Path:
    df = df.copy()
    df["mes_dt"] = pd.to_datetime(df["mes"])
    df = df.sort_values("mes_dt")

    pivot = df.pivot(index="mes_dt", columns="marca", values="unidades")

    fig, ax = plt.subplots(figsize=(8, 5))
    pivot.plot(kind="bar", ax=ax, width=0.7, color=["#1f77b4", "#ff7f0e"])

    ax.set_title("Vendas de Híbridos: BYD vs Fiat", fontsize=13, fontweight="bold")
    ax.set_ylabel("Unidades vendidas", fontsize=11)
    ax.set_xlabel("")
    ax.tick_params(axis="x", labelsize=10)
    ax.legend(title="Marca", frameon=False)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):,}".replace(",", ".")))

    _fmt_month(ax, pivot.index)

    for container in ax.containers:
        ax.bar_label(container, fmt="%d", fontsize=9, padding=4)

    fig.text(
        0.5,
        0.02,
        "Fonte: Fenabrave (volume absoluto de unidades). Meses disponíveis: Nov/25, Jan/26, Jul/26.",
        ha="center",
        fontsize=8,
        color="gray",
    )

    fig.tight_layout(rect=[0, 0.06, 1, 1])
    out_path = FIGS_DIR / "hybrid_sales.png"
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return out_path


def plot_market_share(df: pd.DataFrame) -> Path:
    df = df.copy()
    df["mes_dt"] = pd.to_datetime(df["mes"])
    df = df.sort_values("mes_dt")

    # últimos 6 meses disponíveis
    last_6 = df["mes_dt"].drop_duplicates().sort_values().tail(6)
    df = df[df["mes_dt"].isin(last_6)]

    pivot = df.pivot(index="mes_dt", columns="grupo", values="participacao_pct")
    pivot = pivot[["Stellantis", "Chinesas", "Outras"]]

    fig, ax = plt.subplots(figsize=(10, 5))
    pivot.plot(kind="bar", ax=ax, width=0.75, color=["#d62728", "#2ca02c", "#7f7f7f"])

    ax.set_title("Participação de Mercado: Stellantis vs Marcas Chinesas (últimos 6 meses)", fontsize=13, fontweight="bold")
    ax.set_ylabel("Participação (%)", fontsize=11)
    ax.set_xlabel("")
    ax.tick_params(axis="x", labelsize=9)
    ax.legend(title="Grupo", frameon=False)
    ax.set_ylim(0, 65)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.1f}%"))

    _fmt_month(ax, pivot.index)

    for container in ax.containers:
        ax.bar_label(container, fmt="%.1f%%", fontsize=7.5, padding=3)

    months_str = ", ".join([d.strftime("%b/%y").capitalize() for d in pivot.index])
    fig.text(
        0.5,
        0.02,
        f"Fonte: Fenabrave (participação percentual %). Meses: {months_str}.",
        ha="center",
        fontsize=8,
        color="gray",
    )

    fig.tight_layout(rect=[0, 0.06, 1, 1])
    out_path = FIGS_DIR / "market_share.png"
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return out_path


if __name__ == "__main__":
    from load_data import load_hybrid_sales, load_market_share

    print("Gerando gráfico de híbridos...")
    plot_hybrid_sales(load_hybrid_sales())
    print("Gerando gráfico de market share...")
    plot_market_share(load_market_share())
    print("Pronto.")