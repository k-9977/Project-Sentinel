# Project Sentinel

Project Sentinel is a Python-based file integrity monitoring system that uses SHA-256 cryptographic hashing to detect unauthorized or unexpected file modifications.

## Overview

File integrity is an important part of cybersecurity. If a file is modified unexpectedly, an integrity monitoring system should be able to detect the change.

Project Sentinel creates a trusted cryptographic baseline for a file and later compares the file's current SHA-256 hash against that baseline.

## How It Works

```text
                Select File
                    |
                    v
              Calculate SHA-256
                    |
                    v
            Create Trusted Baseline
                    |
                    v
              Store Baseline
                    |
                    v
              Verify File
                    |
              +-----+-----+
              |           |
            Match      Different
              |           |
              v           v
        Integrity OK    Modified