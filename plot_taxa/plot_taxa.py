import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse
import sys

df = pd.read_table("Taxonomic-Binning/tax.summary.all.tab", header=0, index_col=0)
mapping_file = pd.read_table("mapping_file.tab", header=0, index_col=0)

def parse_args():
    parser = argparse.ArgumentParser(description="Filter OTU table by \
                                                 metadata column and \
                                                 plot microbial composition.")
    parser.add_argument("--input", help="OTU table file path.")
    parser.add_argument("--output", default="plots/",
                        help="Compositional plots of input data.")
    parser.add_argument("--mapping",
                        help="Mapping file containing sample metadata. ")
    parser.add_argument("-tax", "--taxonomic rank", help="taxonomic level at which to filter dataframe by")
    parser.add_argument("--col_row", default="row",
                        help="Whether abundance data of each taxonomic level is in rows or columns")
    parser.add_argument("--include_metadata", default=False,
                        help="include metadata in filtered file")
    parser.add_argument("-col", help="list of column names to be used to select subset of data")
    parser.add_argument("-sub", "--subset", help="list of metavariables to subset data by")
    parser.add_argument("-trans", default=False,
                        help="transpose data")
    parser.add_argument("-df_type", help="df, df_metadata: whether datafram contains abundance data only "
                                         " or abundance + metadata")
    return parser.parse_args()


def main():
    args = parse_arguments(sys.argv)


def search(myDict, lookup):
    for key, value in myDict.items():
        if lookup in key:
            return value
        else:
            pass


def select_taxonomic_rank(df, identifier, col_or_row, metadata=False):
    """Select taxonomic level at which to filter the dataframe by.
       Usage: df=dataframe to filter, identifier=shorthand for taxonomic level e.g. 'p__',
       col_row=whether to filter by columns or rows, metadata=include metadata variables """
    id_map = {"phylum": "__p", "class": "__c",
              "order": "__o", "family": "__f",
              "genus": "__g"
              }
    sel_id = search(id_map, identifier)
    meta = df.select_dtypes(exclude=['float64'])
    if col_or_row == "row":
        if not metadata:
            filtered = df[df.index.str.contains(sel_id)]
            return filtered
        elif metadata == True:
            filtered = df[df.index.str.contains(sel_id)]
            merged = pd.concat([meta, filtered], axis=0)
            return merged
    elif col_or_row == "column":
        if not metadata:
            filtered = df.filter(regex=sel_id, axis=1)
            return filtered
        elif metadata == True:
            filtered = df.filter(regex=sel_id, axis=1)
            merged = pd.concat([meta, filtered], axis=1)
            return merged


def select_subset(df, col, subset, col_2=None, subset2=None):
    """Select subset of data based on metadata.
    Usage: col=column containing metavariable to filter by, subset=metavariable in column to filter by,
    col_2/subset_2= select second set of metavariables to filter by"""
    if not subset2:
        df_subset = df[df[col] == subset]
        df_subset = df_subset.select_dtypes(exclude=['object'])
        return df_subset
    elif subset2:
        df_subset = df[df[col] == subset]
        df_subset_2 = df[df[col_2] == subset2]
        df_subset_2 = df_subset.select_dtypes(exclude=['object'])
        return df_subset_2


def plot_stacked_bar(df, T=None):
    """plot a stacked bar graph of microbiome compositional data"""
    if not T:
        sns.set()
        return df.plot(kind='bar', stacked=True, figsize=(15, 8), legend=True, grid=False, width=0.75)
    elif T:
        df = df.T
        sns.set()
        return df.plot(kind='bar', stacked=True, figsize=(15, 8), legend=True, grid=False, width=0.75)


def plot_area(df, T=None):
    if not T:
        sns.set()
        return df.plot(kind='area', figsize=(15, 8), legend=True, grid=False)
    elif T:
        df = df.T
        sns.set()
        return df.plot(kind='area', figsize=(15, 8), legend=True, grid=False)


def calc_plot_means(df, df_type, col=None, identifier=None, col_or_row=None):
    if df_type == "df":
        mean = df.mean()
        sns.set()
        return mean.plot(kind='pie', legend=True, grid=False, width=0.75)
    elif df_type == "df_metadata":
        taxonomic_level = select_taxonomic_rank(df, identifier, col_or_row, metadata=True)
        if col:
            mean = taxonomic_level.groupby(col).mean()
            return mean.plot(kind='bar', stacked=True, legend=True, grid=False, width=0.75)