import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from tqdm import tqdm
from nltk.tokenize import sent_tokenize
import nltk

from utils import assign_reddit_threads  # Ensure this module is accessible and correctly imported


class DeliberationIntensity:
    def __init__(self, model_name='all-mpnet-base-v2', verbose=False, **kwargs):
        """
        Initialize the DeliberationIntensity class with a SentenceTransformer model and optional configurations.

        Parameters:
        - model_name (str): The name of the sentence transformer model to be used.
        - verbose (bool): Whether to print verbose output.
        - kwargs (dict): Optional arguments to update default column names.
        """
        try:
            self.model = SentenceTransformer(model_name)
        except Exception as e:
            raise ValueError(f"Error loading model '{model_name}': {e}")
        
        nltk.download('punkt', quiet=True)  # Download required NLTK tokenizers quietly
        self.verbose = verbose

        # Default column names, updated based on provided kwargs
        self.columns = {
            'group': 'thread_id',  # Group identifier (e.g., thread ID)
            'text': 'text',        # Text data
            'author': 'author',    # Author of the text
            'argument': 'argument',# Argument flag (1 if it's an argument, 0 otherwise)
            'id': 'id',            # Unique identifier for the message
            'speech': 'text'       # Speech or text data used in some methods
        }
        self.columns.update(kwargs)  # Update column names if provided

    def count_sentences(self, text):
        """
        Count the number of sentences in the given text.

        Parameters:
        - text (str): The input text.

        Returns:
        - int: The number of sentences in the text.
        """
        if pd.isna(text) or not text.strip():
            return 0
        return len(sent_tokenize(text))

    def calculate_d_cluster(self, df, threshold=0.6):
        """
        Calculate D_Cluster scores for each group in the DataFrame based on text embeddings.

        Parameters:
        - df (DataFrame): Input DataFrame containing text data.
        - threshold (float): Threshold for community detection.

        Returns:
        - DataFrame: A DataFrame with D_Cluster scores per group.
        """
        if self.verbose:
            print("Calculating D_Cluster...")
        
        unique_groups = df[self.columns['group']].unique()
        df = df[df[self.columns['argument']] == 1]  # Only consider arguments

        d_cluster_scores = []

        for group in tqdm(unique_groups, desc="Calculating D_Cluster", disable=not self.verbose):
            group_df = df[df[self.columns['group']] == group]
            texts = group_df[self.columns['text']].tolist()

            if len(texts) == 0:
                continue

            try:
                embeddings = self.model.encode(texts, show_progress_bar=self.verbose)
            except Exception as e:
                raise RuntimeError(f"Error encoding texts for group {group}: {e}")

            clusters = util.community_detection(embeddings, min_community_size=1, threshold=threshold)
            num_clusters = len(clusters)
            num_arguments = len(group_df)

            d_cluster = num_clusters / num_arguments if num_arguments > 0 else 0
            d_cluster_scores.append((group, d_cluster))

        d_cluster_df = pd.DataFrame(d_cluster_scores, columns=[self.columns['group'], 'd_cluster'])
        return d_cluster_df

    def argumentativeness(self, df):
        """
        Calculate argumentativeness for each group based on the number of arguments and sentence counts.

        Parameters:
        - df (DataFrame): Input DataFrame containing speech and argument data.

        Returns:
        - dict: Argumentativeness scores for each group.
        """
        if self.verbose:
            print("Calculating argumentativeness...")

        unique_groups = df[self.columns['group']].unique()
        argumentativeness_by_group = {}

        for group in tqdm(unique_groups, desc="Processing groups", disable=not self.verbose):
            group_df = df[df[self.columns['group']] == group]
            
            # Add speech length by counting sentences
            group_df['speech_length'] = group_df[self.columns['speech']].apply(self.count_sentences)
            
            # Aggregate arguments and speech lengths by author and id
            argumentativeness = group_df.groupby([self.columns['author'], self.columns['id']]).agg({
                self.columns['argument']: 'sum',
                'speech_length': 'sum'
            }).reset_index()

            # Scale arguments for some reason (as per your original code logic)
            argumentativeness[self.columns['argument']] *= 3
            
            total_speech_length = argumentativeness['speech_length'].sum()
            num_arguments = argumentativeness[self.columns['argument']].sum()

            argumentativeness_by_group[group] = num_arguments / total_speech_length if total_speech_length > 0 else 0

        return argumentativeness_by_group

    def calculate_d_arg(self, df):
        """
        Calculate D_Arg for each group based on argumentativeness.

        Parameters:
        - df (DataFrame): Input DataFrame.

        Returns:
        - DataFrame: A DataFrame with D_Arg scores per group.
        """
        if self.verbose:
            print("Calculating D_Arg...")

        arg_df = self.argumentativeness(df)
        d_arg_scores = [(group, d_arg) for group, d_arg in arg_df.items()]
        d_arg_df = pd.DataFrame(d_arg_scores, columns=[self.columns['group'], 'd_arg'])
        return d_arg_df

    def calculate_deliberation_intensity(self, df, threshold=0.6):
        """
        Calculate Deliberation Intensity Score (DIS) for each group.

        Parameters:
        - df (DataFrame): Input DataFrame.
        - threshold (float): Threshold for clustering detection.

        Returns:
        - DataFrame: A DataFrame containing DIS scores for each group.
        """
        if self.verbose:
            print("Calculating Deliberation Intensity...")

        # Calculate D_Cluster
        d_cluster_df = self.calculate_d_cluster(df, threshold)

        # Calculate D_Arg
        d_arg_df = self.calculate_d_arg(df)

        # Merge D_Cluster and D_Arg data
        dis_df = pd.merge(d_cluster_df, d_arg_df, on=self.columns['group'])

        # Calculate a_1 and a_2 based on arguments and turns
        num_argument_df = df[(df[self.columns['argument']] == 1) & (df[self.columns['text']].notna())]
        num_arguments = num_argument_df.groupby(self.columns['group'])[self.columns['argument']].sum().reset_index(name='num_arguments')
        num_turns = df.groupby(self.columns['group'])[self.columns['id']].nunique().reset_index(name='num_turns')
        
        a_df = pd.merge(num_arguments, num_turns, on=self.columns['group'])

        # Sigmoid scaling for arguments and turns
        a_df['a_1'] = 1 / (1 + np.exp(-a_df['num_arguments']))
        a_df['a_2'] = 1 / (1 + np.exp(-a_df['num_turns']))

        # Normalize a_1 and a_2
        a_df['sigma_1'] = a_df['a_1'] / (a_df['a_1'] + a_df['a_2'])
        a_df['sigma_2'] = a_df['a_2'] / (a_df['a_1'] + a_df['a_2'])

        # Merge with DIS DataFrame
        dis_df = pd.merge(dis_df, a_df[[self.columns['group'], 'sigma_1', 'sigma_2', 'num_arguments', 'num_turns']], on=self.columns['group'])

        # Calculate final Deliberation Intensity Score (DIS)
        dis_df['dis'] = (dis_df['sigma_1'] * dis_df['d_cluster']) + (dis_df['sigma_2'] * dis_df['d_arg'])

        return dis_df

    def plot_ecdf(self, *dfs, labels=None, output_path=None):
        """
        Plot Empirical Cumulative Distribution Function (ECDF) for the provided data.

        Parameters:
        - dfs (list of DataFrames): A list of DataFrames to plot.
        - labels (list of str): Optional list of labels corresponding to the DataFrames.
        - output_path (str): Optional path to save the plot. If None, the plot will be displayed.
        """
        sns.set_context("talk")
        sns.set_style("whitegrid")
        plt.rc('font', family='STIXGeneral')

        if not dfs:
            raise ValueError("At least one DataFrame must be provided.")

        if labels and len(labels) != len(dfs):
            raise ValueError("The number of labels must match the number of DataFrames.")

        if labels is None:
            labels = [f'Dataset {i+1}' for i in range(len(dfs))]

        plt.figure(figsize=(14, 10))

        for i, df in enumerate(tqdm(dfs, desc="Plotting ECDFs", disable=not self.verbose)):
            dis = np.sort(df['dis'])
            ecdf = np.arange(1, len(dis) + 1) / len(dis)
            sns.lineplot(x=dis, y=ecdf, marker=False, linestyle='-', label=labels[i])

            if i > 0 and self.verbose:
                # T-test to compare distributions
                try:
                    t_stat, p_value = stats.ttest_ind(np.sort(dfs[0]['dis']), dis, equal_var=False)
                    print(f"T-test results for {labels[0]} vs {labels[i]}:")
                    print(f"T-statistic: {t_stat}")
                    print(f"P-value: {p_value}")
                    print(f"The difference is {'statistically significant' if p_value < 0.05 else 'not statistically significant'}.")
                except Exception as e:
                    print(f"Error performing T-test between {labels[0]} and {labels[i]}: {e}")

        plt.xlabel('Deliberation Intensity Score', fontsize=28)
        plt.ylabel('Cumulative Percentage of Threads', fontsize=28)
        plt.legend(title='Datasets', title_fontsize='28', fontsize='28')
        plt.tight_layout()

        if output_path:
            try:
                plt.savefig(output_path, format='png', dpi=600)
            except Exception as e:
                print(f"Error saving the plot to {output_path}: {e}")
        else:
            plt.show()
