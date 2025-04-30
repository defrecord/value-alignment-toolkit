#!/usr/bin/env bash
# download_hf_vitw.sh
# Downloads Values in the Wild dataset files from Hugging Face
# 
# These CSV files are stored in ./data/values_in_the_wild/ directory
# and ARE committed to GitHub as they're small and essential
#
# Usage: ./download_hf_vitw.sh

# Create data directory if it doesn't exist
mkdir -p data/values_in_the_wild

# Function to download a file with proper error handling
download_file() {
    local url="$1"
    local filename="$2"
    
    echo "Downloading: $filename"
    
    # Try using curl first
    if command -v curl > /dev/null 2>&1; then
        curl -L "$url" -o "data/values_in_the_wild/$filename" --retry 3 --silent --show-error
        if [ $? -ne 0 ]; then
            echo "Error downloading $filename with curl"
            return 1
        fi
    # Fall back to wget if curl is not available
    elif command -v wget > /dev/null 2>&1; then
        wget -q "$url" -O "data/values_in_the_wild/$filename"
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

# List of Values in the Wild dataset files
vitw_files=(
    "https://huggingface.co/datasets/Anthropic/values-in-the-wild/resolve/main/values_frequencies.csv?download=true values_frequencies.csv"
    "https://huggingface.co/datasets/Anthropic/values-in-the-wild/resolve/main/values_tree.csv?download=true values_tree.csv"
)

# Count successful and failed downloads
success_count=0
failed_count=0
failed_files=""

# Download each file
for file in "${vitw_files[@]}"; do
    # Split the string into URL and filename
    url=$(echo "$file" | cut -d' ' -f1)
    filename=$(echo "$file" | cut -d' ' -f2)
    
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
    echo "Downloaded files are in the data/values_in_the_wild directory:"
    ls -lh data/values_in_the_wild/
fi
