#!/usr/bin/env bash
# download_papers.sh
# Downloads research papers related to AI alignment and values
# 
# These PDFs are stored in .cache directory and NOT committed to GitHub
# Usage: ./download_papers.sh
#
# Note: The .cache directory should be added to .gitignore

# Create .cache directory if it doesn't exist
mkdir -p .cache

# Function to download a file with proper error handling
download_file() {
    local url="$1"
    local filename="$2"
    
    echo "Downloading: $filename"
    
    # Try using curl first
    if command -v curl > /dev/null 2>&1; then
        curl -L "$url" -o ".cache/$filename" --retry 3 --silent --show-error
        if [ $? -ne 0 ]; then
            echo "Error downloading $filename with curl"
            return 1
        fi
    # Fall back to wget if curl is not available
    elif command -v wget > /dev/null 2>&1; then
        wget -q "$url" -O ".cache/$filename"
        if [ $? -ne 0 ]; then
            echo "Error downloading $filename with wget"
            return 1
        fi
    else
        echo "Error: Neither curl nor wget is installed"
        exit 1
    fi
    
    echo "Successfully downloaded: $filename"
    return 0
}

# List of papers to download
papers=(
    "https://assets.anthropic.com/m/18d20cca3cde3503/original/Values-in-the-Wild-Paper.pdf values-in-the-wild.pdf"
    "https://www-cdn.anthropic.com/de8ba9b01c9ab7cbabf5c33b80b7bbc618857627/Model_Card_Claude_3.pdf claude-3-model-card.pdf"
    "https://proceedings.neurips.cc/paper_files/paper/2023/file/a74b697bce4cac6c91896372abaa8863-Paper-Datasets_and_Benchmarks.pdf dices-dataset.pdf"
    "https://proceedings.neurips.cc/paper_files/paper/2024/file/515c62809e0a29729d7eec26e2916fc0-Paper-Conference.pdf questioning-survey-responses-llm.pdf"
    "https://arxiv.org/pdf/2212.08073 constitutional-ai-paper.pdf"
    "https://openreview.net/pdf?id=zKDSfGhCoK personality-traits-llm.pdf"
    "https://openreview.net/pdf?id=zl16jLb91v measuring-representation-opinions.pdf"
    "https://mental.jmir.org/2024/1/e55988/PDF llm-alignment-human-values-mental-health.pdf"
    "https://dl.acm.org/doi/pdf/10.1145/3630106.3658979 collective-constitutional-ai.pdf"
    "https://arxiv.org/pdf/2110.07574 can-machines-learn-morality.pdf"
    "https://proceedings.neurips.cc/paper_files/paper/2024/file/be2e1b68b44f2419e19f6c35a1b8cf35-Paper-Datasets_and_Benchmarks_Track.pdf prism-alignment-dataset.pdf"
    "https://aclanthology.org/2024.knowllm-1.10.pdf beyond-probabilities-misalignment.pdf"
    "https://aclanthology.org/2025.coling-main.567.pdf cultural-alignment-llm-hofstede.pdf"
    "https://aclanthology.org/2024.findings-emnlp.891.pdf llm-consistency-value-questions.pdf"
    "https://arxiv.org/pdf/2307.16180 llm-personality-mbti.pdf"
    "https://aclanthology.org/2022.findings-acl.165.pdf bbq-bias-benchmark.pdf"
    "https://journals.sagepub.com/doi/pdf/10.1177/17456916231214460 ai-psychometrics.pdf"
)

# Count successful and failed downloads
success_count=0
failed_count=0
failed_files=""

# Download each paper
for paper in "${papers[@]}"; do
    # Split the string into URL and filename
    url=$(echo "$paper" | cut -d' ' -f1)
    filename=$(echo "$paper" | cut -d' ' -f2)
    
    # Download the file
    if download_file "$url" "$filename"; then
        ((success_count++))
    else
        ((failed_count++))
        failed_files="$failed_files$filename, "
    fi
done

# Print summary
echo ""
echo "Download Summary:"
echo "-----------------"
echo "Successfully downloaded: $success_count files"
echo "Failed downloads: $failed_count files"
if [ $failed_count -gt 0 ]; then
    echo "Failed files: ${failed_files%, }"
fi

# Check if any files were downloaded
if [ $success_count -gt 0 ]; then
    echo ""
    echo "Downloaded files are in the .cache directory:"
    ls -lh .cache/
fi
