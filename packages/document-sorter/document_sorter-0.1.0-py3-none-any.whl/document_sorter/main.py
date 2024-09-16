import os
import shutil
from pathlib import Path
from tqdm import tqdm
from typing import List, Dict, Tuple, Optional
import PyPDF2
import openpyxl
import pandas as pd
import docx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import sklearn
import numpy as np
import scipy.sparse as sp
import argparse
from packaging import version

def extract_text_pdf(file_path: str) -> str:
    """Extract text from PDF files."""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        return ' '.join(page.extract_text() for page in reader.pages)

def extract_text_docx(file_path: str) -> str:
    """Extract text from DOCX files."""
    doc = docx.Document(file_path)
    return ' '.join(paragraph.text for paragraph in doc.paragraphs)

def extract_text_xlsx(file_path: str) -> str:
    """Extract text from XLSX files."""
    wb = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
    return ' '.join(str(cell.value) for sheet in wb for row in sheet.iter_rows() for cell in row if cell.value)

def extract_text_csv(file_path: str) -> str:
    """Extract text from CSV files."""
    df = pd.read_csv(file_path)
    return ' '.join(df.astype(str).values.flatten())

def extract_text_txt(file_path: str) -> str:
    """Extract text from TXT files."""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        return file.read()

def extract_text(file_path: str) -> str:
    """Extract text content from various document types."""
    try:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.pdf':
            return extract_text_pdf(file_path)
        elif ext == '.docx':
            return extract_text_docx(file_path)
        elif ext == '.xlsx':
            return extract_text_xlsx(file_path)
        elif ext == '.csv':
            return extract_text_csv(file_path)
        elif ext in ['.txt', '.md', '.tex']:
            return extract_text_txt(file_path)
        else:
            print(f"Unsupported file type: {file_path}")
            return ""
    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
        return ""

def search_documents(directory: str) -> List[str]:
    """Search for documents of specified types in the given directory."""
    documents = []
    allowed_extensions = ('.docx', '.pdf', '.md', '.txt', '.csv', '.xlsx', '.tex')
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(allowed_extensions) and len(Path(root).parts) == len(Path(directory).parts):
                documents.append(os.path.join(root, file))
    return documents

def elbow_method(distance_matrix: np.ndarray, max_clusters: int = 10) -> int:
    """Determine the optimal number of clusters using the elbow method."""
    n_samples = distance_matrix.shape[0]
    max_clusters = min(max_clusters, n_samples - 1)  # Ensure max_clusters is less than n_samples
    
    wcss = []
    for i in range(1, max_clusters + 1):
        kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
        kmeans.fit(distance_matrix)
        wcss.append(kmeans.inertia_)
    
    # Calculate the differences
    differences = np.diff(wcss)
    
    # Find the elbow point (where the difference starts to level off)
    elbow_point = np.argmin(differences) + 1
    
    return min(elbow_point + 1, n_samples)  # Ensure the returned value is not greater than n_samples

def cluster_documents(documents: List[str], n_clusters: Optional[int], verbose: bool) -> Tuple[List[int], np.ndarray]:
    """Cluster documents based on cosine similarity of their contents."""
    texts = []
    for doc in tqdm(documents, desc="Extracting text", unit="doc"):
        text = extract_text(doc)
        if text.strip():  # Only add non-empty texts
            texts.append(text)
        elif verbose:
            print(f"Warning: No text extracted from {doc}")
    
    if not texts:
        raise ValueError("No valid text could be extracted from any of the documents.")
    
    vectorizer = TfidfVectorizer(stop_words='english')
    try:
        tfidf_matrix = vectorizer.fit_transform(texts)
    except ValueError as e:
        if "empty vocabulary" in str(e):
            raise ValueError("The extracted text contains only stop words or no valid words.") from e
        raise
    
    cosine_sim = cosine_similarity(tfidf_matrix)
    distance_matrix = 1 - cosine_sim

    n_samples = len(texts)
    
    if n_samples < 3:
        if verbose:
            print(f"Only {n_samples} documents found. Skipping clustering.")
        return list(range(n_samples)), tfidf_matrix
    
    # Use elbow method to determine optimal number of clusters if not specified
    if n_clusters is None:
        n_clusters = elbow_method(distance_matrix)
        if verbose:
            print(f"Optimal number of clusters determined: {n_clusters}")
    else:
        n_clusters = min(n_clusters, n_samples)
        if verbose:
            print(f"Using user-specified number of clusters: {n_clusters}")

    # Perform clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    clusters = kmeans.fit_predict(distance_matrix)
    
    return clusters, tfidf_matrix

def get_keyword(tfidf_matrix: np.ndarray, vectorizer: TfidfVectorizer, cluster: int) -> str:
    """Get the most relevant keyword for a cluster."""
    cluster_center = tfidf_matrix[cluster].mean(axis=0)
    
    # Handle different matrix types
    if sp.issparse(cluster_center):
        cluster_center = cluster_center.toarray().flatten()
    elif isinstance(cluster_center, np.matrix):
        cluster_center = np.asarray(cluster_center).flatten()
    else:
        cluster_center = cluster_center.flatten()
    
    top_features = np.argsort(cluster_center)[-5:]
    feature_names = vectorizer.get_feature_names_out()
    return feature_names[top_features[-1]]

def sort_documents(documents: List[str], clusters: List[int], tfidf_matrix: np.ndarray, vectorizer: TfidfVectorizer, custom_keywords: Optional[List[str]] = None) -> Dict[str, List[str]]:
    """Sort documents into clusters and assign keywords."""
    sorted_docs = {}
    if custom_keywords:
        for doc, cluster in tqdm(zip(documents, clusters), desc="Sorting documents", total=len(documents), unit="doc"):
            keyword = custom_keywords[cluster % len(custom_keywords)]
            if keyword not in sorted_docs:
                sorted_docs[keyword] = []
            sorted_docs[keyword].append(doc)
    else:
        for doc, cluster in tqdm(zip(documents, clusters), desc="Sorting documents", total=len(documents), unit="doc"):
            keyword = get_keyword(tfidf_matrix, vectorizer, cluster)
            if keyword not in sorted_docs:
                sorted_docs[keyword] = []
            sorted_docs[keyword].append(doc)
    return sorted_docs

def create_folders_and_move(sorted_docs: Dict[str, List[str]], base_dir: str, dry_run: bool = False):
    """Create folders for each keyword and move documents."""
    for keyword, docs in tqdm(sorted_docs.items(), desc="Creating folders and moving documents", unit="keyword"):
        folder_path = os.path.join(base_dir, keyword)
        if not dry_run:
            os.makedirs(folder_path, exist_ok=True)
        
        for doc in docs:
            dest_path = os.path.join(folder_path, os.path.basename(doc))
            if not os.path.exists(dest_path):
                if dry_run:
                    print(f"Would move {doc} to {dest_path}")
                else:
                    shutil.move(doc, dest_path)

def main():
    parser = argparse.ArgumentParser(description="Sort documents into folders based on content similarity.")
    parser.add_argument("directory", nargs="?", default=".", help="Base directory to search for documents (default: current directory)")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without moving files")
    parser.add_argument("--verbose", action="store_true", help="Print detailed information during execution")
    parser.add_argument("--clusters", type=int, help="Specify the number of clusters to use")
    parser.add_argument("--keywords", nargs="+", help="Specify custom keywords for folder names")
    args = parser.parse_args()

    # Convert to absolute path
    directory = os.path.abspath(args.directory)

    if args.verbose:
        print(f"Searching for documents in {directory}...")
    documents = search_documents(directory)
    if args.verbose:
        print(f"Found {len(documents)} documents.")
    
    if not documents:
        print(f"Error: No documents found in the specified directory: {directory}")
        return

    try:
        if args.verbose:
            print("Clustering documents...")
        clusters, tfidf_matrix = cluster_documents(documents, args.clusters, args.verbose)

        if args.verbose:
            print("Sorting documents...")
        vectorizer = TfidfVectorizer(stop_words='english')
        vectorizer.fit_transform([extract_text(doc) for doc in documents])
        sorted_docs = sort_documents(documents, clusters, tfidf_matrix, vectorizer, args.keywords)

        if args.verbose:
            print("Creating folders and moving documents...")
        create_folders_and_move(sorted_docs, directory, args.dry_run)

        if args.verbose:
            print("Document sorting complete!")
    except ValueError as e:
        print(f"Error: {str(e)}")
        print("The script could not proceed due to the above error.")

if __name__ == "__main__":
    main()
