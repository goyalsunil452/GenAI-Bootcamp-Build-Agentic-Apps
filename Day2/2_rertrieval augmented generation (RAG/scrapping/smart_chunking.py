"""
Smart Chunking Module for RAG Systems
Provides advanced chunking strategies to reduce duplication and improve content quality
"""

import hashlib
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def create_smart_chunks(documents, chunk_size=1000, chunk_overlap=200):
    """
    Create smart chunks with deduplication and better splitting strategy

    Args:
        documents: List of documents to chunk
        chunk_size: Target size for each chunk
        chunk_overlap: Overlap between consecutive chunks

    Returns:
        List of processed and deduplicated chunks
    """
    print("Creating smart chunks with deduplication...")

    # Strategy 1: Better text splitting with semantic boundaries
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=[
            "\n\n",  # Paragraph breaks (highest priority)
            "\n",  # Line breaks
            ". ",  # Sentence endings
            "! ",  # Exclamation endings
            "? ",  # Question endings
            "; ",  # Semicolon separations
            ", ",  # Comma separations
            " ",  # Word boundaries
            "",  # Character level (last resort)
        ],
    )

    # Split documents
    all_splits = text_splitter.split_documents(documents)
    print(f"Initial chunks created: {len(all_splits)}")

    # Strategy 2: Content deduplication
    unique_chunks = _remove_duplicates(all_splits)

    # Strategy 3: Filter low-quality chunks
    quality_chunks = _filter_low_quality_chunks(unique_chunks)

    # Strategy 4: Merge very short chunks with adjacent ones
    merged_chunks = _merge_short_chunks(quality_chunks, chunk_size)

    print(f"Final chunks after merging: {len(merged_chunks)}")

    return merged_chunks


def _remove_duplicates(chunks):
    """Remove duplicate chunks based on content hash"""

    def get_content_hash(content):
        """Create a hash of normalized content for deduplication"""
        # Normalize content: lowercase, remove extra whitespace
        normalized = " ".join(content.lower().split())
        return hashlib.md5(normalized.encode()).hexdigest()

    unique_chunks = []
    seen_hashes = set()
    duplicate_count = 0

    for chunk in chunks:
        content_hash = get_content_hash(chunk.page_content)

        if content_hash not in seen_hashes:
            seen_hashes.add(content_hash)
            unique_chunks.append(chunk)
        else:
            duplicate_count += 1

    print(f"Duplicates removed: {duplicate_count}")
    print(f"Unique chunks remaining: {len(unique_chunks)}")

    return unique_chunks


def _filter_low_quality_chunks(chunks):
    """Filter out low-quality chunks"""
    quality_chunks = []

    # Define low-quality content patterns
    low_quality_patterns = [
        "404 Error",
        "This page does not exist",
        "Go back",
        "Take me home",
        "Courses",
        "Free Content",
        "Login",
        "Signup",
        "Checkout",
        "Go back home",
        "Please go back home",
        "checkout our awesome courses",
        "USER_AGENT environment variable not set",
        "consider setting it to identify your requests",
    ]

    for chunk in chunks:
        content = chunk.page_content.strip()

        # Skip chunks that are too short or contain low-quality content
        if len(content) >= 100:
            # Check if content contains any low-quality patterns
            is_low_quality = any(
                pattern.lower() in content.lower() for pattern in low_quality_patterns
            )

            # Additional check for 404-like content
            if (
                "404" in content and "Error" in content
            ) or "page does not exist" in content.lower():
                is_low_quality = True

            if not is_low_quality:
                quality_chunks.append(chunk)
            else:
                print(f"Filtered out low-quality chunk: {content[:100]}...")

    print(f"Quality chunks after filtering: {len(quality_chunks)}")

    return quality_chunks


def _merge_short_chunks(chunks, chunk_size):
    """Merge very short chunks with adjacent ones"""
    merged_chunks = []
    i = 0

    while i < len(chunks):
        current_chunk = chunks[i]

        # If current chunk is too short and there's a next chunk
        if len(current_chunk.page_content.strip()) < 200 and i + 1 < len(chunks):
            next_chunk = chunks[i + 1]

            # Merge chunks if combined length is reasonable
            combined_content = (
                current_chunk.page_content + "\n\n" + next_chunk.page_content
            )

            if len(combined_content) <= chunk_size * 1.5:  # Allow some overflow
                # Create merged chunk
                merged_chunk = Document(
                    page_content=combined_content,
                    metadata={
                        "source": current_chunk.metadata.get("source", "unknown"),
                        "merged": True,
                        "original_chunks": 2,
                    },
                )
                merged_chunks.append(merged_chunk)
                i += 2  # Skip both chunks
                continue

        merged_chunks.append(current_chunk)
        i += 1

    return merged_chunks


def post_retrieval_deduplication(documents):
    """
    Remove duplicate content after retrieval

    Args:
        documents: List of retrieved documents

    Returns:
        List of unique documents
    """
    unique_docs = []
    seen_content = set()

    for doc in documents:
        # Normalize content for comparison (first 50 words)
        normalized_content = " ".join(doc.page_content.lower().split()[:50])

        if normalized_content not in seen_content:
            seen_content.add(normalized_content)
            unique_docs.append(doc)
        else:
            print(f"Skipping duplicate content in retrieval")

    return unique_docs


def get_chunking_stats(original_chunks, final_chunks):
    """
    Get statistics about the chunking process

    Args:
        original_chunks: Number of original chunks
        final_chunks: Number of final chunks

    Returns:
        Dictionary with chunking statistics
    """
    if original_chunks == 0:
        return {
            "original_count": original_chunks,
            "final_count": final_chunks,
            "reduction_percentage": 0,
            "efficiency_gain": f"Created {final_chunks} chunks from {original_chunks} documents",
        }

    change = final_chunks - original_chunks
    if change > 0:
        # Chunks increased
        change_percentage = round((change / original_chunks) * 100, 2)
        efficiency_gain = f"Increased from {original_chunks} to {final_chunks} chunks (+{change_percentage}%)"
    elif change < 0:
        # Chunks decreased
        change_percentage = round((abs(change) / original_chunks) * 100, 2)
        efficiency_gain = f"Reduced from {original_chunks} to {final_chunks} chunks (-{change_percentage}%)"
    else:
        # No change
        change_percentage = 0
        efficiency_gain = f"No change: {original_chunks} chunks"

    return {
        "original_count": original_chunks,
        "final_count": final_chunks,
        "change_percentage": change_percentage,
        "efficiency_gain": efficiency_gain,
    }
