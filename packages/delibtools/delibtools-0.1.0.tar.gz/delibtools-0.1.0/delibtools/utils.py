import pandas as pd
import numpy as np
from tqdm import tqdm

def assign_reddit_threads(df):
    """
    Generate unique thread_ids for Reddit posts using CPU optimization.
    
    Parameters:
    - df (DataFrame): A pandas DataFrame with 'id' and 'parent_id' columns.
    
    Returns:
    - Series: A pandas Series containing the generated thread_ids for each row in the DataFrame.
    """
    # Create a mapping of id to its index in the DataFrame
    id_to_index = {id_: idx for idx, id_ in enumerate(df['id'])}
    
    # Initialize an empty array for thread_ids
    thread_ids = np.empty(len(df), dtype=object)
    
    # Dictionary to map children to their parents
    children = {}
    for idx, parent_id in enumerate(df['parent_id']):
        if pd.notna(parent_id):
            # Process top-level post ids (t3_) and comment ids (t1_)
            if parent_id.startswith('t3_'):
                children.setdefault(parent_id[3:], []).append(idx)
            elif parent_id.startswith('t1_'):
                children.setdefault(parent_id[3:], []).append(idx)
    
    # Process each row to assign thread_ids with progress bar
    for idx in tqdm(range(len(df)), desc="Generating thread IDs"):
        # If thread_id already assigned, skip
        if thread_ids[idx] is not None:
            continue
        
        id_ = df.iloc[idx]['id']
        parent_id = df.iloc[idx]['parent_id']
        
        if pd.isna(parent_id) or parent_id == id_:
            # Assign thread_id to top-level posts (self-references or no parent)
            thread_ids[idx] = id_
        elif parent_id.startswith('t3_'):
            # Reply to top-level post
            thread_ids[idx] = parent_id[3:]
        elif parent_id.startswith('t1_'):
            # Reply to another comment
            parent_idx = id_to_index.get(parent_id[3:])
            if parent_idx is not None and thread_ids[parent_idx] is not None:
                thread_ids[idx] = thread_ids[parent_idx]
            else:
                # If parent is not found or not yet assigned, use current post id
                thread_ids[idx] = id_
        
        # Propagate thread_id to all children recursively
        stack = children.get(id_, [])
        while stack:
            child_idx = stack.pop()
            if thread_ids[child_idx] is None:
                thread_ids[child_idx] = thread_ids[idx]
                # Add children of the current child to the stack
                stack.extend(children.get(df.iloc[child_idx]['id'], []))
    
    return pd.Series(thread_ids, index=df.index)
