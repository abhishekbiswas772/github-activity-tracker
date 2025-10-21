# GitHub Activity Tracker

A beautiful command-line interface (CLI) tool to fetch and display GitHub user activity in a formatted table. Built with Python and Rich for an enhanced terminal experience.

## Features

- **Beautiful Table Output** - Rich formatted tables with colors and icons
- **Filter by Event Type** - Focus on specific GitHub events
- **Export Data** - Save activity data as JSON or CSV
- **Limit Results** - Control the number of events displayed
- **Fast & Efficient** - Concurrent parsing with ThreadPoolExecutor
- **Retry Logic** - Automatic retry on API failures
- **Human-Readable Descriptions** - Clear event descriptions with icons
- **Error Handling** - Graceful error handling with helpful messages

## Requirements

- Python 3.7+
- requests
- rich

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd github-activity-tracker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Make the CLI executable (optional):
```bash
chmod +x cli.py
```

## Usage

### Basic Usage

Fetch activity for a GitHub user:
```bash
python cli.py <username>
```

Example:
```bash
python cli.py abhishekbiswas772
```

### Advanced Options

#### Limit Results
Display only the first N events:
```bash
python cli.py abhishekbiswas772 --limit 10
```

#### Filter by Event Type
Show only specific event types:
```bash
python cli.py abhishekbiswas772 --type PushEvent
```

Common event types:
- `PushEvent` - Push commits
- `WatchEvent` - Star repository
- `IssuesEvent` - Create/modify issues
- `PullRequestEvent` - Create/modify pull requests
- `ForkEvent` - Fork repository
- `CreateEvent` - Create branch/tag
- `DeleteEvent` - Delete branch/tag

#### Verbose Mode
Show additional details including ID and public status:
```bash
python cli.py abhishekbiswas772 --verbose
```

#### Export Data

Export to JSON:
```bash
python cli.py abhishekbiswas772 --export json --output activity.json
```

Export to CSV:
```bash
python cli.py abhishekbiswas772 --export csv --output activity.csv
```

Export with verbose details:
```bash
python cli.py abhishekbiswas772 --export json --output activity.json --verbose
```

### Combined Options

Combine multiple options for powerful queries:
```bash
# Get last 5 push events and export to JSON
python cli.py abhishekbiswas772 --type PushEvent --limit 5 --export json --output pushes.json

# Get verbose output with limited results
python cli.py abhishekbiswas772 --limit 20 --verbose
```

## Command-Line Arguments

| Argument | Short | Description | Example |
|----------|-------|-------------|---------|
| `username` | - | GitHub username (required) | `abhishekbiswas772` |
| `--limit` | `-l` | Limit number of events | `--limit 10` |
| `--type` | `-t` | Filter by event type | `--type PushEvent` |
| `--export` | `-e` | Export format (json/csv) | `--export json` |
| `--output` | `-o` | Output file path | `--output data.json` |
| `--verbose` | `-v` | Show detailed information | `--verbose` |

## Examples

### Example 1: Quick Activity Check
```bash
python cli.py octocat
```

### Example 2: Filter and Export
```bash
python cli.py torvalds --type PushEvent --limit 10 --export csv --output linus_pushes.csv
```

### Example 3: Detailed Analysis
```bash
python cli.py facebook --verbose --limit 15
```

## Project Structure

```
github-activity-tracker/
├── cli.py                  # CLI entry point
├── main.py                 # Core GitHub activity handler
├── models.py               # Data models
├── event_formatter.py      # Event formatting and icons
├── requirements.txt        # Dependencies
└── README.md              # Documentation
```

## How It Works

1. **API Request**: Fetches data from GitHub's `/users/{username}/events` endpoint
2. **Concurrent Parsing**: Uses ThreadPoolExecutor to parse events in parallel
3. **Data Transformation**: Converts JSON to structured Python dataclasses
4. **Formatting**: Applies human-readable descriptions and icons
5. **Display/Export**: Shows data in rich tables or exports to files

## API Rate Limits

GitHub API has rate limits:
- **Unauthenticated**: 60 requests per hour
- **Authenticated**: 5000 requests per hour

This tool currently uses unauthenticated requests. For heavy usage, consider adding GitHub token authentication.

## Error Handling

The tool handles common errors gracefully:

- **404 Error**: User not found
- **403 Error**: API rate limit exceeded
- **Network Errors**: Connection issues with retry logic
- **Invalid Input**: Missing or invalid arguments

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Built with [Rich](https://github.com/Textualize/rich) for beautiful terminal output
- Uses [GitHub REST API](https://docs.github.com/en/rest)
- Inspired by the [roadmap.sh GitHub Activity project](https://roadmap.sh/projects/github-user-activity)

## Support

If you encounter any issues or have questions:
1. Check the GitHub Issues
2. Review the API documentation
3. Ensure your Python version is 3.7+

---
This project idea is inspired from `https://roadmap.sh/projects/github-user-activity`
Made with ❤️ by developers, for developers
