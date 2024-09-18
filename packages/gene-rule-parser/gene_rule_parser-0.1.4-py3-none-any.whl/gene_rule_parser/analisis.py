import typer
from pathlib import Path
from rich import print
import pandas as pl
from gene_rule_parser import ExpressionParser, tree_analysis, Gene, distribute_rules

app = typer.Typer()


@app.command()
def run(rule:str, dfpath:Path):
    dataframe = pl.read_csv(dfpath)
    print(f"Rule:{rule}")
    print(ExpressionParser)
    parser = ExpressionParser()
    tokens = parser.tokenize(rule)
    print(tokens)
    tree = parser.parse(rule)
    dataframe["Gene_ID"] = dataframe["Gene_ID"].str.upper()
    result = tree_analysis(tree, dataframe)
    print(tree)
    print(result)

if __name__=="__main__":
    app()
