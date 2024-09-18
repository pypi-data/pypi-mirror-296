try:
    from gen_lexer import lexer
except:
    from .gen_lexer import lexer
try:
    from gen_parser import parser, Expression, And, Or, Gene, Unknown
except: 
    from .gen_parser import parser, Expression, And, Or, Gene, Unknown

from dataclasses import dataclass
from functools import lru_cache
import polars as pl
import ply.yacc as yacc
import ply.lex as lex
from typing import List, Dict

@dataclass
class ExpressionParser:
    lexer: lex.Lexer = lexer
    parser: yacc.LRParser = parser

    def tokenize(self, data: str) -> list[lex.LexToken]:
        self.lexer.input(data)
        return list(iter(self.lexer.token, None))

    def parse(self, data: str) -> Expression:
        return self.parser.parse(data)



def distribute_rules(words: List[str], N: int) -> Dict[int, List[str]]:
    # Sort words by length
    sorted_words = sorted(words, key=len)
    
    # Initialize groups
    groups = {i: [] for i in range(N)}
    
    # Distribute words in a round-robin fashion
    for i, word in enumerate(sorted_words):
        group_index = i % N
        groups[group_index].append(word)
    
    return groups


def tree_analysis(
        tree:Expression, 
        df:pl.DataFrame):

    if isinstance(tree, Or):
        try:
            left_tree = tree.left
            right_tree = tree.right

            if not isinstance(left_tree,(Gene,Unknown)) and not isinstance(right_tree,(Gene,Unknown)):
                left = tree_analysis(
                        left_tree,
                        df)
                right = tree_analysis(
                        right_tree,
                        df)
                pair = [
                    left,
                    right
                ]
                return sum([p for p in pair if p is not None])
            if isinstance(left_tree,(Gene,Unknown)) and not isinstance(right_tree,(Gene,Unknown)):

                valor_l = tree_analysis(
                    left_tree,
                    df)
                valor_r = tree_analysis(
                    right_tree,
                    df)
                return sum([p for p in [valor_l, valor_r] if p is not None])
            if not isinstance(left_tree,(Gene,Unknown)) and isinstance(right_tree,(Gene,Unknown)):

                # just one value
                valor_r = tree_analysis(
                    right_tree,
                    df)
                valor_l = tree_analysis(
                    left_tree,
                    df)

                return sum([p for p in [valor_l, valor_r] if p  is not None])
            elif isinstance(left_tree,(Gene,Unknown)) and isinstance(right_tree,(Gene,Unknown)):
                # GENE OR GENE: sum(values) 
                a = tree_analysis(
                    left_tree,
                    df)
                b = tree_analysis(
                    right_tree,
                    df)
                return sum([p for p in [a,b] if p  is not None])
        except Exception as ex:
            raise ex

    elif isinstance(tree, And):
        left_tree = tree.left
        right_tree = tree.right
        if (
                isinstance(left_tree, (Gene, Unknown)) and 
                isinstance(right_tree, (Gene, Unknown))
        ):
            try:
                # GENE AND GENE: min(values)
                pair = [
                    tree_analysis(
                        left_tree,
                        df),
                    tree_analysis(
                        right_tree,
                        df)
                ]
                pair =[p for p in pair if p  is not None]
                
                if pair:
                    value = min(pair)
                    return value
                return None
            except Exception as ex:
                raise ex

        elif (
                isinstance(left_tree, (Gene, Unknown)) and 
                isinstance(right_tree, (And, Or))
        ):
            try:
                valor_l = tree_analysis(
                    left_tree,
                    df)
                valor_r = tree_analysis(
                    right_tree,
                    df)

                pair =[p for p in [valor_l, valor_r] if p  is not None]
                if pair:
                    value = min(pair)
                    return value
                return None
            except Exception as ex:
                raise ex
            
        elif (
                isinstance(left_tree, (And, Or)) and 
                isinstance(right_tree, (Gene, Unknown))
        ):
            try:

                # just one value
                valor_r = tree_analysis(
                    right_tree,
                    df)
                valor_l = tree_analysis(
                    left_tree,
                    df)
                pair =[p for p in [valor_l, valor_r] if p  is not None]
                if pair:
                    value = min(pair)
                    return value
                return None
            except Exception as ex:
                raise ex
        elif (
                isinstance(left_tree, (And, Or)) and 
                isinstance(right_tree, (And, Or))
        ):
            try:
                pair = [
                    tree_analysis(
                        left_tree,
                        df), 
                    tree_analysis(
                        right_tree,
                        df)
                ]

                pair =[p for p in pair if p  is not None]
                if pair:
                    value = min(pair)
                    return value
                return None
            except Exception as ex:
                raise ex
    elif isinstance(tree, (Gene, Unknown)):
        # Case GENE or UNKNOWN

        filtered_df = df.filter(
           pl.col("Gene_ID")==tree.gen
        )
        min_expression = filtered_df["Expression"].to_list()
        return min_expression.pop(0)
    else:
        return 0
