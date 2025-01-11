#!/bin/bash

# First, remove old directories if they exist
rm -rf 0*

# Create main directories and subdirectories
directories=(
    "llm-basics/environment-setup"
    "llm-basics/model-api-usage"
    "prompt-engineering/core-concepts"
    "prompt-engineering/optimization-techniques"
    "rag-applications/rag-basics"
    "rag-applications/advanced-rag"
    "function-calling/function-calling-basics"
    "function-calling/tool-integration"
    "agent-development/agent-basics"
    "agent-development/multi-agent-collaboration"
    "multimodal-applications/image-processing"
    "multimodal-applications/audio-processing"
    "llm-fine-tuning/fine-tuning"
    "llm-fine-tuning/deployment-and-optimization"
    "enterprise-projects/full-project-development"
    "enterprise-projects/deployment-and-maintenance"
)

# Create directories, index.md files and .gitkeep files
for dir in "${directories[@]}"; do
    # Create directory
    mkdir -p "$dir"
    # Create index.md instead of lesson.md
    touch "$dir/index.md"
    # Create .gitkeep
    touch "$dir/.gitkeep"
    # Also create .gitkeep in parent directory
    parent_dir=$(dirname "$dir")
    touch "$parent_dir/.gitkeep"
done

# Add AI Coding directories
mkdir -p ai-coding/code-generation-basics
mkdir -p ai-coding/code-optimization
mkdir -p ai-coding/ai-testing

# Create index.md files for AI Coding
touch ai-coding/code-generation-basics/index.md
touch ai-coding/code-optimization/index.md
touch ai-coding/ai-testing/index.md

# Create .gitkeep files
touch ai-coding/.gitkeep
touch ai-coding/code-generation-basics/.gitkeep
touch ai-coding/code-optimization/.gitkeep
touch ai-coding/ai-testing/.gitkeep

echo "Directory structure created successfully with .gitkeep files!" 